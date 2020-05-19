import webapp2
import json
import datetime
from google.appengine.ext import ndb
from google.appengine.api import images

from .model import Article
from category.model import Category
from author.model import Author
from image.model import Image

from image.app import ImageHandler


class ArticleHandler(webapp2.RequestHandler):
    def options(self, *args, **kwargs):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization, x-api-key'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE, OPTIONS'

    def get(self, article_id=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        category_id = self.request.get('category')
        if category_id:
            articles = Article.get_by_category(category_id)
            article_json = json.dumps([self.to_json(article)
                                       for article in articles])
            return self.response.write(article_json)

        if article_id:
            article_id = int(article_id)
            article = ndb.Key(Article, article_id).get()

            article_json = json.dumps(self.to_json(article))

            return self.response.write(article_json)
        else:
            articles = Article.get_all()

            article_json = json.dumps([self.to_json(article)
                                       for article in articles])

            return self.response.write(article_json)

    def post(self, article_id=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json, multipart/form-data'
        if article_id:
            return
        else:
            # json_string = self.request.body
            # article_dict = json.loads(json_string)
            imageFile = images.resize(self.request.get('image'), 480, 360)
            image = Image(image=imageFile)
            image.put()

            title = self.request.get('title')
            image_id = image.key.id()
            content = self.request.get('content')
            category = ndb.Key(Category, int(
                self.request.get('category'))).get()
            author = ndb.Key(Author, int(self.request.get('author'))).get()

            new_article = Article(
                title=title,
                image_id=image_id,
                content=content,
                category=category,
                author=author
            )
            new_article.put()

    def put(self, article_id=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        if article_id:
            article_id = int(article_id)
            article = ndb.Key(Article, article_id).get()

            # json_string = self.request.body
            # article_dict = json.loads(json_string)

            image_request = self.request.get('image')
            if image_request != '':
                imageFile = images.resize(image_request, 480, 360)
                image = Image(image=imageFile)
                image.put()

                old_image = ndb.Key(Image, article.image_id)
                old_image.delete()

                image_id = image.key.id()
                article.image_id = image_id

            title = self.request.get('title')
            content = self.request.get('content')
            category = ndb.Key(Category, int(
                self.request.get('category'))).get()
            author = ndb.Key(Author, int(self.request.get('author'))).get()

            article.title = title
            article.content = content
            # article.date = date
            article.category = category
            article.author = author

            article.put()

    def delete(self, article_id=None):
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'

        if article_id:
            article = ndb.Key(Article, int(article_id))
            article.delete()

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
