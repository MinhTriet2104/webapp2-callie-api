import webapp2
from google.appengine.ext import ndb

from .model import Image


class ImageHandler(webapp2.RequestHandler):
    def get(self, image_id):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        if image_id:
            image = ndb.Key(Image, int(image_id)).get()

            self.response.headers['Content-Type'] = 'image/png, image/jpeg, image/jpg'
            self.response.write(image.image)
        else:
            self.response.write('No Image')

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
