import json
from posttags.request import create_post_tag, get_all_post_tags
from users.request import login_user
from users import register_user, get_user_by_id, login_user
from comments import create_comment, delete_comment, get_all_comments
from http.server import BaseHTTPRequestHandler, HTTPServer
from categories import get_all_categories, create_category
from posts import get_all_posts
from posts import create_post, get_post_by_id
from tags import get_all_tags, create_tag,  delete_tag
from posts import get_user_posts

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)
      
        if len(parsed) == 2:
            (resource, id) = parsed
            if resource == "posts":
                if id is None:
                    response = f"{get_all_posts()}"
                elif id is not None:
                    response = f"{get_post_by_id(id)}"
            if resource == "comments":
                if id is None:
                    response = f"{get_all_comments()}"
            if resource == "categories":
                if id is None:
                    response = f"{get_all_categories()}"
                elif id is not None:
                    pass
            if resource == "tags":
                if id is None:
                    response = f"{get_all_tags()}"
                elif id is not None:
                    pass
            if resource == "users":
                if id is None:
                   pass
                elif id is not None:
                   response = f"{get_user_by_id(id)}"
<<<<<<< HEAD
            if resource == "postTags":
                if id is None:
                    response = f"{get_all_post_tags()}"
=======
        
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "user_id" and resource == "posts":
                response = get_user_posts(value)
>>>>>>> main

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new 
        new_resource = None
        
        if resource == "register":
            new_resource = register_user(post_body)
        if resource == "login":
            new_resource = login_user(post_body)
        if resource == "categories":
            new_resource = create_category(post_body)
        if resource == "comments":
            new_resource = create_comment(post_body)
        if resource == "posts":
            new_resource = create_post(post_body)
        if resource == "tags":
            new_resource = create_tag(post_body)
        if resource == "postTags":
            new_resource = create_post_tag(post_body)


        self.wfile.write(f"{new_resource}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request. It deals with updating an existing row.

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "comments":
            delete_comment(id)

        if resource == "tags":
            delete_tag(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
