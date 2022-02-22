import http.server
from http.server import HTTPServer, SimpleHTTPRequestHandler
import http.cookies
from http.cookies import SimpleCookie
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
import ssl


class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Prevent unauthenticated access when the authenticated cookie is not set to 'true'
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/login':
            return self.do_login()
        elif self.path == '/logout':
            return self.do_logout()
        else:
            return self.send_error(404)


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
            self.send_response(302)
            self.send_header('Location', '/secure/')
            # send authenticated cookie
            return self.end_headers()
        else:
            return self.send_error(401)


    def do_logout(self):
        # Clear the cookie and redirect to the login page
        return None


    def authenticate(self, username, password):
        return username == "user" and password == "1234"


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


if __name__ == '__main__':
    server = HTTPServer(("localhost", 8443), MyServer)
    server.socket = ssl.wrap_socket(server.socket, keyfile="key.pem", certfile='cert.pem', server_side=True)
    print("Server started on https://localhost:8443")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()