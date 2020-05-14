import webapp2
import json
from google.appengine.ext import ndb

from .model import Author


class AuthorHandler(webapp2.RequestHandler):
    def get(self, author_id=None):
        if author_id:
            author_id = int(author_id)
            author = ndb.Key(Author, author_id).get()

            self.response.write(json.dumps(author.to_dict()))
        else:
            authors = Author.get_all()

            authors_json = json.dumps([author.to_dict() for author in authors])

            self.response.write(authors_json)

    def post(self, author_id=None):
        if author_id:
            self.abort(405)

        json_string = self.request.body
        author_dict = json.loads(json_string)

        name = author_dict['name']

        new_author = Author(name=name)
        new_author.put()

        self.abort(200)
