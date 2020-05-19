from google.appengine.ext import ndb

from utils.app import ModelUtils
from category.model import Category
from author.model import Author


class Article(ModelUtils, ndb.Model):
    title = ndb.StringProperty(required=True)
    image_id = ndb.IntegerProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.StringProperty(required=True)
    view = ndb.IntegerProperty(default=0)
    author = ndb.StructuredProperty(Author, required=True)
    category = ndb.StructuredProperty(Category, required=True)
    date_updated = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_by_category(cls, category_id):
        category_id = int(category_id)
        category = ndb.Key(Category, category_id).get()
        return cls.query(Article.category.name == category.name).fetch(8)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()
