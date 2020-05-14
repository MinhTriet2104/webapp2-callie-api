import webapp2

from category.app import CategoryHandler
from author.app import AuthorHandler


app = webapp2.WSGIApplication([
    (r'/category/(\d+)', CategoryHandler),
    ('/category', CategoryHandler),
    (r'/author/(\d+)', AuthorHandler),
    ('/author', AuthorHandler),
], debug=True)
