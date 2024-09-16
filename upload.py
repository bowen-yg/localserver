from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import time
import cgi

# 创建自定义的请求处理类
class FileUploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        start_time = time.time()
        content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
        
        if content_type == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers['Content-Length'])
            fields = cgi.parse_multipart(self.rfile, pdict)
            uploaded_file = fields.get('file')[0]
            file_name = fields.get('file')[1]
            
            # 创建存储上传文件的目录
            upload_dir = 'uploaded_files'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # 保存文件到指定目录
            file_path = os.path.join(upload_dir, file_name)
            with open(file_path, 'wb') as file:
                file.write(uploaded_file)
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully.')
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'Invalid content type.')

        end_time = time.time()
        time_elapsed_ms = int((end_time - start_time) * 1000)
        print(f"Update in {time_elapsed_ms} ms")

# 启动服务器
def run_server():
    server_address = ('10.67.35.219', 8000)  # 可以根据需要修改端口号
    httpd = HTTPServer(server_address, FileUploadHandler)
    print('Server running on port 8000...')
    httpd.serve_forever()

# 运行服务器
run_server()