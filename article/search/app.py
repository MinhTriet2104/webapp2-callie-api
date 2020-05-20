from datetime import datetime

from google.appengine.api import search


def create_document(article):
    img_id = str(article.image_id)
    document = search.Document(
        fields=[
            search.TextField(name='title', value=article.title),
            search.DateField(name='date', value=datetime.now()),
            search.TextField(name='content', value=article.content),
            search.NumberField(name='view', value=article.view),
            search.TextField(name='image_id', value=img_id),
            search.TextField(name='category', value=article.category.name),
            search.TextField(name='author', value=article.author.name)
        ]
    )
    return document


def add_document_to_index(document):
    # document = create_document(article)
    index = search.Index('articles')
    index.put(document)


def simple_search(title):
    index = search.Index('articles')
    query_string = 'title = {}'.format(title)
    return index.search(query_string)
