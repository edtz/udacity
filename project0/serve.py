'''
Creates a basic http server for a movie collection page.
'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import webbrowser
from movies_list import create_list as movies

HOST = '127.0.0.1'
PORT = 1234


class BasicRequestHandler(BaseHTTPRequestHandler):
    '''
    Single purpose request handler, sends a single page to any GET request
    '''

    def do_GET(self):
        '''
        This method will be executed on any GET requests
        '''
        # write http headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # render page and send it
        payload = self.create_page()
        self.wfile.write(bytes(payload, "utf8"))
        return

    def create_page(self):
        '''
        Renders response from templates
        TODO: Inject list from main
        '''
        # Load templates
        with open("index.html", "r") as page, open("item.html", "r") as item:
            page_template = str(page.read())
            item_template = str(item.read())
        # Get a list of movies from the other module
        list_of_movies = movies()

        items = ""
        for movie in list_of_movies:
            # Render the item template for each movie
            # and save them in accumulator
            items += item_template.format(
                img=movie.img,
                title=movie.title,
                desc=movie.desc,
                # This approach is rather hacky,
                # but we know data is normalized
                youtube_id=movie.trailer.split("=")[-1]
            )
        # Render and return the main page template with movie items
        return page_template.format(payload=items)

if __name__ == '__main__':
    # Create a new server instance
    httpd = HTTPServer((HOST, PORT), BasicRequestHandler)
    # We can open browser before server starts because
    # it's not instant to open a link while it's close
    # to instant for this app
    webbrowser.open("http://{host}:{port}".format(
        host=HOST,
        port=PORT
    ))
    httpd.serve_forever()
