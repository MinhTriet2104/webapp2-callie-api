from google.appengine.ext import ndb

from utils.app import ModelUtils


class Category(ModelUtils, ndb.Model):
    name = ndb.StringProperty(required=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()
