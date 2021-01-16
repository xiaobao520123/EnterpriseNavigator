import os
import numpy as np
from PIL import Image, ImageDraw

import cfg

# 设置CUDA可见的GPU设备
os.environ["CUDA_VISIBLE_DEVICES"] = cfg.visible_devices_str

UPLOAD_FOLDER = cfg.upload_folder
ALLOWED_EXTENSIONS = cfg.allowed_extenstions

from flask import Flask, jsonify, flash
from flask import request, redirect
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from werkzeug.utils import secure_filename

import text

app = Flask(__name__)
bootstrap = Bootstrap(app)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

# 检查是不是允许上传的文件类型
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 对上传的图片文件进行预处理
def preprocess_upload_image(image):
    filename = image.filename
    # 转换文件名到安全文件名
    filename = secure_filename(filename)
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # 保存图片文件
    image.save(img_path)
    
    # 转换颜色空间到RGB空间（去除alpha通道）
    img = Image.open(img_path).convert('RGB')
    img.save(img_path)
    return img_path

# 处理上传的文件，从中识别企业实体
def detect_enterprise_from_upload_file(file):
    img_path = preprocess_upload_image(file)
    enterprise, polygon = text.find_enterprise_from_image(img_path)
    # 如果企业实体识别失败，返回0，成功返回1
    success = int(enterprise is not None)

    result = {'success': success,
              'enterprise': enterprise,
              'polygon': polygon
              }
    return result

# 生成错误返回
def generate_err_msg(err_msg=''):
    return jsonify({
                'success': 0,
                'err_msg': err_msg
            })

# API——批量上传文件
@app.route('/api/batch', methods=['POST'])
def handle_api_batch():
    if request.method == 'POST':
        result = {}
        if 'file_selector' not in request.files:
            return 'POST参数错误，缺少参数<file_selector>!'
        files = request.files.getlist('file_selector')
        for file in files:
            if not file or file.filename == '':
                flash('无效的文件')
                continue

            filename = file.filename
            # 检查是不是允许的文件类型
            if allowed_file(filename):
                result[filename] = detect_enterprise_from_upload_file(file)
            else:
                flash('不允许的文件类型')
        return jsonify(result)
    return '禁止访问！' 

# API——单个图片文件（适用于APP端）
@app.route('/api/qcc', methods=['POST'])
def handle_app_qcc():
    if request.method == 'POST':
        if 'data' not in request.files:
            return generate_err_msg('缺少参数<data>')
        file = request.files['data']
        
        if not file or file.filename == '':
            return generate_err_msg('无效的文件')

        filename = file.filename
        # 检查是不是允许的文件类型
        if allowed_file(filename):
            raw_data = detect_enterprise_from_upload_file(file)
            return jsonify(raw_data)
        else:
            return generate_err_msg('不允许的文件类型')
    return '禁止访问！'

if __name__ == '__main__':
    app.run(host=cfg.server_host, port=cfg.server_port, debug=True)