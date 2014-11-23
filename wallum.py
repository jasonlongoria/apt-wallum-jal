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

class ResultsCalc(webapp2.RequestHandler):
    def post(self):
        calcinputs = {'window_start':self.request.get('window_start'),
                      'window_end':self.request.get('window_end'),
                      'lat':self.request.get('lat'),
                      'lon':self.request.get('lon')}
        url = "/results?" + urllib.urlencode(calcinputs)
        self.redirect(url)
        #todo: generate array of results
        #inputs: north angle, window endpoint 1, window endpoint 2, wall distance from window
        
class ResultsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.request.get('lon'))
        pass


class InputPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('input.html')
        self.response.write(template.render())

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('Hello, Walls!')
        template = JINJA_ENVIRONMENT.get_template('input.html')
        self.response.write(template.render())


application = webapp2.WSGIApplication([
    ('/results', ResultsPage),
    ('/calc', ResultsCalc),
    ('/input', InputPage),
    ('/', MainPage)
], debug=True)
