from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import bleach
import re


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += self.get_restaurants()
                output += '<br><a href="/restaurants/new">Create a new Restaurant</a>'
                output += '</body></html>'
                self.wfile.write(output)
                return
            elif self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="/restaurants/new">'
                output += '<h2>Create a new restaurant</h2>'
                output += '<label>Name: <input type="text" name="name"></label>'
                output += '<input type="submit" value="Create">'
                output += '</form></body></html>'
                self.wfile.write(output)
                return
            elif re.search(r'/restaurants/(\d+)/edit', self.path):
                restaurant_id = int(re.search(r'/restaurants/(\d+)/edit', self.path).group(1))
                row = session.query(Restaurant).get(restaurant_id)
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<form method="POST" enctype="multipart/form-data" action="%s">' % bleach.clean(self.path)
                output += '<h2>Edit the name of the restaurant</h2>'
                output += '<p>Old name: %s</p>' % bleach.clean(row.name)
                output += '<label>New name: <input type="text" name="new-name"></label>'
                output += '<input type="submit" value="Edit">'
                output += '</form></body></html>'
                self.wfile.write(output)
                return
            elif re.search(r'/restaurants/(\d+)/delete', self.path):
                restaurant_id = int(re.search(r'/restaurants/(\d+)/delete', self.path).group(1))
                row = session.query(Restaurant).get(restaurant_id)
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<form method="POST" action="%s">' % bleach.clean(self.path)
                output += '<h2>Delete restaurant %s</h2>' % bleach.clean(row.name)
                output += '<input type="submit" value="Delete">'
                output += '</form></body></html>'
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                else:
                    raise IOError

                new_restaurant = Restaurant(name=messagecontent[0])
                session.add(new_restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('location', '/restaurants')
                self.end_headers()
            elif re.search(r'/restaurants/(\d+)/edit', self.path):
                restaurant_id = int(re.search(r'/restaurants/(\d+)/edit', self.path).group(1))
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('new-name')
                else:
                    raise IOError
                row = session.query(Restaurant).get(restaurant_id)
                if row.name != messagecontent[0]:
                    row.name = messagecontent[0]
                    session.add(row)
                    session.commit()

                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('location', '/restaurants')
                self.end_headers()
            elif re.search(r'/restaurants/(\d+)/delete', self.path):
                restaurant_id = int(re.search(r'/restaurants/(\d+)/delete', self.path).group(1))
                row = session.query(Restaurant).get(restaurant_id)
                session.delete(row)
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('location', '/restaurants')
                self.end_headers()
        except IOError:
            pass

    def get_restaurants(self):
        rows = session.query(Restaurant).all()
        msg = ''
        for row in rows:
            msg += '<p>%s</p>' % bleach.clean(row.name)
            msg += '<a href="/restaurants/%d/edit">Edit</a>' % row.id
            msg += '<br>'
            msg += '<a href="/restaurants/%d/delete">Delete</a>' % row.id
            msg += '<br>'
        return msg


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print 'Web server running on port %s' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C entered, stopping web server...'
        server.socket.close()

if __name__ == '__main__':
    main()
