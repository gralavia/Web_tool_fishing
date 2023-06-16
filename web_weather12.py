# -*- coding: utf-8 -*-
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
import html
import get_tide_heights
import get_temp



class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            get_html = '''
            <html>
            <head><title>Tide Height</title></head>
            <body>
            <h1>Tide Height</h1>
            <form method="POST" action="/">
            <label for="time">time(YYYY-MM-DD hh:mm:ss)</label>
            <input type="text" id="time" name="time" required><br>
            <label for="location">location</label>
            <input type="text" id="location" name="location" required><br>
            <label for="city">city</label>
            <input type="text" id="city" name="city" required><br>
            <input type="submit" value="submit">
            </form>
            </body>
            </html>
            '''

            self.wfile.write(get_html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')

            data = parse_qs(body)
            time = unquote(data.get('time', [''])[0])
            location = unquote(data.get('location', [''])[0], encoding='utf-8')
            city = unquote(data.get('city', [''])[0], encoding='utf-8')
            location = html.unescape(location)
            city = html.unescape(city)

            tide_heights = get_tide_heights.get_tide_heights(time, location)

            temp = get_temp.get_temperature(time, city)

            post_html = f'''
                   <html>
                   <head><title>Tide Height Result</title></head>
                   <body>
                   <h1>Tide Height Result</h1>
                   <p>Tide Height {tide_heights}</p>
                   <p>Pop, T, RH {temp}</p>
                   <p>{'It is safe to go fishing' if tide_heights and int(tide_heights) >= 50 and int(tide_heights) <= 100 and int(temp[0]) < 50 and int(temp[1]) <= 28 and int(temp[1]) >= 10 and int(temp[2]) <= 80  else 'It is not safe to go fishing'}</p>

                   <a href="/">Back</a>
                   </body>
                   </html>
                   '''

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(post_html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    from http.server import HTTPServer

    server_address = ('localhost', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print('Server running...')

    httpd.serve_forever()
