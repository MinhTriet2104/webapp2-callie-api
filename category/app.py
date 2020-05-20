import webapp2
import json
import datetime
from google.appengine.ext import ndb

from .model import Category


class CategoryHandler(webapp2.RequestHandler):
    def get(self, category_id=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        if category_id:
            category_id = int(category_id)
            category = ndb.Key(Category, category_id).get()

            self.response.write(json.dumps(category.to_dict()))
        else:
            categories = Category.get_all()

            categories_dict = [cat.to_dict() for cat in categories]
            categories_json = json.dumps(categories_dict)

            self.response.write(categories_json)
        return

    def post(self, category_id=None):
        self.options()
        if category_id:
            return

        json_string = self.request.body
        category_dict = json.loads(json_string)

        name = category_dict['name']

        new_cateogry = Category(name=name)
        new_cateogry.put()

        category = Category.query(ancestor=new_cateogry.key).get()
        if category:
            return self.response.write(json.dumps(self.to_json(category)))

    def options(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'

    def to_json(self, o):
        if isinstance(o, list):
            return [self.to_json(l) for l in o]
        if isinstance(o, dict):
            x = {}
            for l in o:
                x[l] = self.to_json(o[l])
            return x
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, ndb.GeoPt):
            return {'lat': o.lat, 'lon': o.lon}
        if isinstance(o, ndb.Key):
            return o.urlsafe()
        if isinstance(o, ndb.Model):
            dct = o.to_dict()
            dct['id'] = o.key.id()
            return self.to_json(dct)
        return o
