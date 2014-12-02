import os
import webapp2
import urllib
import jinja2
import webapp2

from math import cos
from math import sin
from math import radians
from math import pi

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
        
class GenerateResults():
    def results(self, lat):
        # cos(azimuth) = (sin(dec)*cos(lat) - cos(hour)*cos(dec)*sin(lat)) / cos(elevation)
        
        # hour angles from 6AM to 6PM = -90 to +90 degrees = -pi/2 to +pi/2 radians
        # every 2 hours = every 30 degrees
        for hour in [-90, -60, -30, 0, 30, 60, 90]:
            h_rad = radians(hour)
            
            # TODO: calculate declination based on day of year; d_rad = radians (declination)
            # prototype: declination = 0 degrees
            d_rad = 0
            
            # TODO: get latitude from input
            # prototype: latitude = 30.27 degrees (Austin)
            lat = 30.72
            l_rad = radians(lat)
            
            # solar elevation angle
            sin_elevation = cos(h_rad)*cos(d_rad)*cos(l_rad) + sin(d_rad)*sin(l_rad)
            e_rad = math.acos(sin_elevation)
            
            cos_azimuth = (sin(d_rad)*cos(l_rad) - cos(h_rad)*cos(d_rad)*sin(l_rad)) / cos(e_rad)
        
        
        
class ResultsPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.request.get('lon'))

class InputPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('input.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/results', ResultsPage),
    ('/calc', ResultsCalc),
    ('/input', InputPage),
    ('/', InputPage)
], debug=True)
