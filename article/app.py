import webapp2
import json
import datetime
from google.appengine.ext import ndb

from .model import Article
from category.model import Category
from author.model import Author


class ArticleHandler(webapp2.RequestHandler):
    def get(self, article_id=None):
        if article_id:
            article_id = int(article_id)
            article = ndb.Key(Article, article_id).get()

            article_json = json.dumps(self.to_json(article))

            self.response.write(article_json)
        else:
            articles = Article.get_all()

            article_json = json.dumps([self.to_json(article)
                                       for article in articles])

            self.response.write(article_json)

    def post(self, article_id=None):
        if article_id:
            self.abort(405)
        else:
            json_string = self.request.body
            article_dict = json.loads(json_string)

            self.response.write(json.dumps(article_dict))
            title = article_dict['title']
            image = "https://picsum.photos/640/480"
            content = article_dict['content']
            category = ndb.Key(Category, int(article_dict['category'])).get()
            author = ndb.Key(Author, int(article_dict['author'])).get()

            new_article = Article(
                title=title,
                image=image,
                content=content,
                category=category,
                author=author
            )
            new_article.put()
            self.abort(200)

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
