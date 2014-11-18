import os
import webapp2
import urllib
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#todo: jquery slider for window position
#todo: jquery positioner for north direction


class InputPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('input.html')
        self.response.write(template.render())

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, Walls!')
        template = JINJA_ENVIRONMENT.get_template('input.html')
        self.response.write(template.render())
        

application = webapp2.WSGIApplication([
    ('/input', InputPage),
    ('/', MainPage)
], debug=True)
