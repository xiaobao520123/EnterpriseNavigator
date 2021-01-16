# Application Configuration
# 识别结果表格保存目录
table_output_folder = './static/output'
# 识别预览图图片保存目录
image_preview_folder = './static/img/preview'
# 识别结果打框线条宽度
answer_line_width = 5
# 识别结果打框线条颜色
answer_line_color = 'green'

# API Configuration
allowed_extenstions = set(['bmp', 'png', 'jpg', 'jpeg'])
api_qcc_batch_detection = r"http://yourapiserver:5000/api/batch"

# Flask Configuration
# 服务器IP地址
server_host="0.0.0.0"
# 服务器端口
server_port=8080