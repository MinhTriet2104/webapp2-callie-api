from google.appengine.ext import ndb

from utils.app import ModelUtils
from category.model import Category
from author.model import Author


class Article(ModelUtils, ndb.Model):
    title = ndb.StringProperty(required=True)
    image = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.StringProperty(required=True)
    view = ndb.IntegerProperty(default=0)
    author = ndb.StructuredProperty(Author, required=True)
    category = ndb.StructuredProperty(Category, required=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()
