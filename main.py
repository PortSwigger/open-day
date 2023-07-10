import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler
import http.cookies
from http.cookies import SimpleCookie
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
import ssl
import json
import random
import string

class MyServer(SimpleHTTPRequestHandler):
    comments = []
    authenticated_users = {}

    def do_GET(self):
        authenticated = self.get_cookie('authenticated') == 'true'
        if '/secure' in self.path and not authenticated:
            return self.send_error(401)
        elif self.path == '/comments':
            return self.get_comments()
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/login':
            return self.do_login()
        elif self.path == '/logout':
            return self.do_logout()
        elif self.path == '/comments':
            return self.save_comment()
        else:
            return self.send_error(404)

    def get_comments(self):
        self.set_headers_for_json_response()
        self.wfile.write(json.dumps(self.comments).encode('utf-8'))

    def save_comment(self):
        authenticated = self.get_cookie('authenticated') == 'true'
        if not authenticated:
            return self.send_error(401)

        session_id = self.get_cookie('sessionId')
        if session_id == None:
            return self.send_error(401)

        user = self.authenticated_users.get(session_id, 'Unknown')

        form_data = self.parse_POST()
        
        self.comments.append({'user': user, 'comment': form_data['comment']})
        self.send_response(302)
        self.send_header('Location', '/secure')
        return self.end_headers()


    def parse_POST(self):
        content_length = int(self.headers['content-length'])
        form_data_as_bytes = parse_qs(self.rfile.read(content_length), keep_blank_values=1)

        form_data_as_strings = {}

        for key in form_data_as_bytes:
            form_data_as_strings[key.decode()] = form_data_as_bytes[key][0].decode()

        return form_data_as_strings


    def do_login(self):
        form_data = self.parse_POST()
        if self.authenticate(form_data['username'], form_data['password']):
            session_id = ''.join(random.choices(string.ascii_lowercase, k=5))
            self.authenticated_users[session_id] = form_data['username']
            self.send_response(302)
            self.send_header('Location', '/secure')
            self.send_cookie('authenticated=true')
            self.send_cookie(f'sessionId={session_id}')
            return self.end_headers()
        else:
            return self.send_error(401)


    def do_logout(self):
        session_id = self.get_cookie('sessionId')
        self.authenticated_users.pop(session_id, None)
        self.send_response(302)
        self.send_header('Location', '/')
        self.send_cookie('authenticated=false; expires=Thu, 01 Jan 1970 00:00:00 GMT')
        self.send_cookie(f'sessionId={session_id}; expires=Thu, 01 Jan 1970 00:00:00 GMT')
        return self.end_headers()


    # Should return True if the user us authenticated or False if they are not
    def authenticate(self, username, password):
        return (username == "alice" and password == "1234") or (username == "bob" and password == "5678")


    def send_cookie(self, cookie):
        self.send_header('Set-Cookie', cookie)


    def get_cookie(self, cookie):
        cookies = SimpleCookie(self.headers.get('Cookie'))
        if cookie in cookies.keys():
            return cookies[cookie].value


    def end_headers(self):
        self.send_header('Cache-Control','no-cache, no-store, must-revalidate')
        self.send_header('Pragma','no-cache')
        self.send_header('Expires','0')
        return SimpleHTTPRequestHandler.end_headers(self)

    def set_headers_for_json_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


if __name__ == '__main__':
    server = HTTPServer(("localhost", 8443), MyServer)
    server.socket = ssl.wrap_socket(server.socket, keyfile="key.pem", certfile='cert.pem', server_side=True)
    print("Server started on https://localhost:8443")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()