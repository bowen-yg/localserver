from flask import Flask, request, render_template, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploaded_files/'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md', 'py', 'js', 'java', 'c', 'h', 'mp4'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_uploaded_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            files.append(filename)
    return files

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    uploaded_files = get_uploaded_files()
    if request.method == 'POST':
        for file in request.files.getlist('file'):
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return '不允许的文件类型'
        uploaded_files = get_uploaded_files()  # 更新文件列表
    return render_template('index.html', files=uploaded_files, allowed_extensions=ALLOWED_EXTENSIONS)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(host='0.0.0.0', port=8080)