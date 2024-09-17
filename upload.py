
from flask import Flask, request, render_template
import os

app = Flask(__name__)


UPLOAD_FOLDER = './uploaded_files/'  # 指定上传文件夹
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md', 'py', 'js', 'java', 'c', 'h', 'mp4'}  # 允许的文件扩展名

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查是否有文件在请求中
        if 'file' not in request.files:
            return '没有文件部分'
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也会
        # 提交一个没有文件名的空部分
        if file.filename == '':
            return '没有选择文件'
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return '文件上传成功'
        else:
            return '不允许的文件类型'
    return render_template('./index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)