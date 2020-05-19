from google.appengine.ext import ndb


class Image(ndb.Model):
    image = ndb.BlobProperty()
    date_created = ndb.DateTimeProperty(auto_now_add=True)
