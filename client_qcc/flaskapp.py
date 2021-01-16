import cfg

import os
from flask import Flask
from flask import request, render_template
from flask_bootstrap import Bootstrap

import util

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = os.urandom(24)

# 客户端主页
@app.route('/', methods=['GET'])
def qcc_index():
    return render_template("index.html")

# 客户端批次上传请求处理
@app.route('/upload', methods=['POST'])
def qcc_upload():
    if request.method == 'POST':
        # Flask的一个BUG，必须先转发POST请求才能获取表单参数
        r, delay = util.batch_upload(request.headers, request.get_data())

        if 'file_selector' not in request.files:
            return '参数错误'
        
        if r.status_code != 200:
            return '远程服务器请求失败，错误代码：%d' % r.status_code

        json_data = r.json()
        
        # 转存图片文件
        file_list = request.files.getlist('file_selector')
        util.save_uploaded_file(file_list)
        
        # 处理服务器请求结果
        collections = util.process_detection_result(json_data)
        # 将识别结果写入至表格文件中
        excel_filepath = util.write_batch_detection_result(collections)

        # 计算识别速度和响应时间
        average_speed = round(len(collections) / delay, 2)
        delay = round(delay, 4)

        return render_template("view.html", 
            collections=collections, 
            delay=delay, 
            average_speed=average_speed, 
            excel_file=excel_filepath)
    return '禁止访问！'

if __name__ == '__main__':
    app.run(host=cfg.server_host, port=cfg.server_port, debug=True)