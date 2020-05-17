import webapp2

from category.app import CategoryHandler
from author.app import AuthorHandler
from article.app import ArticleHandler

from image.app import ImageHandler


app = webapp2.WSGIApplication([
    (r'/img/(\d+)', ImageHandler),
    (r'/category/(\d+)', CategoryHandler),
    ('/category', CategoryHandler),
    (r'/author/(\d+)', AuthorHandler),
    ('/author', AuthorHandler),
    (r'/article/(\d+)', ArticleHandler),
    ('/article', ArticleHandler),
], debug=True)
