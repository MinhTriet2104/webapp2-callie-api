from google.appengine.ext import ndb

from utils.app import ModelUtils


class Author(ModelUtils, ndb.Model):
    name = ndb.StringProperty(required=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()
