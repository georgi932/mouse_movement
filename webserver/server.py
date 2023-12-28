import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from utilities.config import APP_HOST, APP_PORT


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        # Indicates that the response is HTML
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Path to the HTML file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(script_dir, '../client/index.html')

        # Opens the html file read-only
        with open(index_path, 'r') as file:
            # Converts the file contents to bytes and send it as the response body
            self.wfile.write(bytes(file.read(), 'utf-8'))


def start_http_server():
    try:
        server = HTTPServer((APP_HOST, APP_PORT), Server)
        print(f'Server started - http://{APP_HOST}:{APP_PORT}')
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("HTTP webserver closed successfully")
    except Exception as err:
        print(f"Failed to start HTTP webserver: {str(err)}")
