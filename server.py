from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib
from http import HTTPStatus

# ip, port config
"""注意修改为自己的ip和端口"""
host = ('10.67.35.219', 8000)
#非常重要的配置

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            f = open("index.html", 'r')
            content = f.read()
            content = content.replace(
                '</body>', self.get_directory('.') + '</body>')
            # 里面需要传入二进制数据，用encode()函数转换为二进制数据
            self.wfile.write(content.encode())
        else:
            try:
                path = urllib.parse.unquote(self.path[1:])
                f = open(path, 'rb')
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'<h1>File Not Found</h1>')

    def do_POST(self):
        self.send_response(200)
        self.end_headers()

        self.parse_query()
        remainbytes = int(self.headers['content-length'])

        fileName = self.queries['fileName'][0]
        if not fileName:
            print("fail to find fn")
            return (False, "Can't find out file name...")

        print(fileName)
        try:
            out = open(fileName, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")

        out.write(self.rfile.read(remainbytes))
        print('finish')
        out.close()

    def parse_query(self):
        self.queryString = urllib.parse.unquote(self.path.split('?', 1)[1])
        self.queries = urllib.parse.parse_qs(self.queryString)
        print(self.queries)

    def get_directory(self, path) -> str:
        try:
            list = os.listdir(path)
        except OSError:
            self.send_error(
                HTTPStatus.NOT_FOUND,
                "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        r = []
        displaypath = os.path.abspath(path)
        title = 'Directory listing for %s' % displaypath
        r.append('<h1>%s</h1>' % title)

        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>' % (linkname, displayname))
        # print(''.join(r))
        return ''.join(r)


if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()