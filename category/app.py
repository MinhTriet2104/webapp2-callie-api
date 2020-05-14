import webapp2
import json
from google.appengine.ext import ndb

from .model import Category


class CategoryHandler(webapp2.RequestHandler):
    def get(self, category_id=None):
        if category_id:
            category_id = int(category_id)
            category = ndb.Key(Category, category_id).get()

            self.response.write(json.dumps(category.to_dict()))
        else:
            categories = Category.get_all()

            categories_dict = [cat.to_dict() for cat in categories]
            categories_json = json.dumps(categories_dict)

            self.response.write(categories_json)

    def post(self, category_id=None):
        if category_id:
            self.abort(405)

        json_string = self.request.body
        category_dict = json.loads(json_string)

        name = category_dict['name']

        new_cateogry = Category(name=name)
        new_cateogry.put()

        self.abort(200)