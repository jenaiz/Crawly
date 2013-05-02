import cgi
import webapp2
    
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from protorpc import messages
from protorpc.webapp import service_handlers
from protorpc import remote
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
    
package = 'root'

class RootRequest(messages.Message):
    message = messages.StringField(1, required=True)

class RootResponse(messages.Message):
    message = messages.StringField(1, required=True)

class RootService(remote.Service):

    @remote.method(RootRequest, RootResponse)
    def status(self, request):
        return RootResponse(message='ok')

    @remote.method(RootRequest, RootResponse)
    def add_worker(self, request):
        url = request.message
        hash_code = '000002'
        q = db.GqlQuery('SELECT * FROM Worker WHERE url = :1', url)
        worker = q.fetch(1)
        if worker == None or len(worker) == 0:
            worker = Worker(url=url, hash_code=hash_code, status='working')
            worker.put()
            return RootResponse(message=hash_code)
        else:
            return RootResponse(message=worker[0].hash_code)
        # add url to workers
        # response ok with hash code
    @remote.method(RootRequest, RootResponse)
    def start(self, request):
        workers = db.GqlQuery('SELECT * FROM Worker')
        urls = db.GqlQuery('SELECT * FROM Url')
        
        #for worker in workers:
            
        
    @remote.method(RootRequest, RootResponse)
    def job(self, request):
        url = request.message
        urls = url.split(',')
        for l in urls:
            taskqueue.add(url='/queue', params={'key': l})
      
        return RootResponse(message='urls received: ' + str(len(urls)))

class QueueHandler(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        page = crawler.crawl_web(key)
        def txn():
            url = Url.get_by_key_name(key)
            if url is None:
                url = Url(key_name=key, uri=key, content=cgi.escape(page[:100]))
            url.put()
        db.run_in_transaction(txn)


service_mappings = service_handlers.service_mapping(
        [('/root', RootService)         
        ])
#service_mappings.append(('/queue', QueueHandler))

app = webapp2.WSGIApplication(service_mappings)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()