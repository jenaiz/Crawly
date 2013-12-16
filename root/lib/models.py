from google.appengine.api import taskqueue
from google.appengine.ext import db

# Model for Url
#
class Url(db.Model):
    uri = db.StringProperty(required=True)
    content = db.TextProperty(required=False)
    downloaded_date = db.DateProperty()
    server = db.StringProperty(required=False)
    error = db.BooleanProperty(indexed=False)
    error_message = db.StringProperty(required=False)

# Model for Worker
#   It contains values of the workers used in the root node
#
class Worker(db.Model):
    url = db.StringProperty(required=True)
    hash_code = db.StringProperty(required=True)
    status = db.StringProperty(required=True)
    date_check = db.DateProperty()