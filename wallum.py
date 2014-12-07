import os
import webapp2
import urllib
import jinja2
import webapp2

from math import *

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
                      'lat':self.request.get('lat')}
        url = "/output?" + urllib.urlencode(calcinputs)
        self.redirect(url)

class OutputPage(webapp2.RequestHandler):
    def get(self):
        # sin(azimuth) = -sin(hour angle)*cos(declination) / cos(elevation angle)
        sin_azimuth = []
        
        # hour angles from 6AM to 6PM = -90 to +90 degrees = -pi/2 to +pi/2 radians
        # every 2 hours = every 30 degrees
        for hour in [-90, -60, -30, 0, 30, 60, 90]:
            hour_r = radians(hour)
            for day in range(1,366):
                # declination for each day of the year
                dec_r = radians(-23.44)*cos(radians(day*360/365))
                
                # TODO: get latitude from input
                # prototype: latitude = 30.27 degrees (Austin)
                lat = 30.72
                lat_r = radians(lat)
                
                # solar elevation angle
                sin_elevation = cos(hour_r)*cos(dec_r)*cos(lat_r) + sin(dec_r)*sin(lat_r)
                ele_r = acos(sin_elevation)
                
                sin_azimuth_instant = -sin(hour_r) * cos(dec_r) / cos(ele_r)
                if sin_azimuth_instant <= 1 and sin_azimuth_instant >= -1:
                    sin_azimuth.append(sin_azimuth_instant)
                
        sin_azimuth.sort()
        mult = len(sin_azimuth)/10
        # Get the x-positions (cosines) for the divisions in the gradient
        # Sort the array, and divide it into equal 10ths
        # The first nine are the divisions for the gradient
        deciles = []
        for decile in range(1,10):
            deciles.append(sin_azimuth[decile*mult])
        
        colors = ["black", "purple", "blue", "green", "yellow", "green", "blue", "purple", "black"]
        template = JINJA_ENVIRONMENT.get_template('output.html')
        self.response.write(template.render({'deciles': deciles, 'colors': colors}))

class InputPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('input.html')
        self.response.write(template.render())

application = webapp2.WSGIApplication([
    ('/output', OutputPage),
    ('/calc', ResultsCalc),
    ('/', InputPage)
], debug=True)
