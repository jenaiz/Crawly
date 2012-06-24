import crawler
import cgi
import urllib2
#import simplejson
from django.utils import simplejson
import socket

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from protorpc import messages
from protorpc.webapp import service_handlers
from protorpc import remote
from google.appengine.api import taskqueue
from google.appengine.ext import db
from protorpc import transport

class Url(db.Model):
  uri = db.StringProperty(required=True)
  content = db.TextProperty(required=False)
  downloaded_date = db.DateProperty(auto_now_add = True)
  server = db.StringProperty(required=False)
  error = db.BooleanProperty(indexed=False)
  error_message = db.StringProperty(required=False)
  
package = 'worker'

class WorkerRequest(messages.Message):
    message = messages.StringField(1, required=True)

class WorkerResponse(messages.Message):
    message = messages.StringField(1, required=True)

class WorkerService(remote.Service):

    @remote.method(WorkerRequest, WorkerResponse)
    def status(self, request):
        return WorkerResponse(message='ok')
  
    @remote.method(WorkerRequest, WorkerResponse)
    def job(self, request):
        url = request.message
        urls = url.split(',')
        for l in urls:
            taskqueue.add(queue_name='url-crawler-queue', url='/queue', params={'key': l})
      
        return WorkerResponse(message='urls received: ' + str(len(urls)))
    
    @remote.method(WorkerRequest, WorkerResponse)
    def add_to_root(self, request):
        root = request.message

        data = simplejson.dumps({
          "message": "localhost:8081",
        })
        req = urllib2.Request(root, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()

        hash_code = simplejson.loads(response)['message']
        
        return WorkerResponse(message='hashcode = ' + str(hash_code))
        
        
class QueueHandler(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        url = Url.get_by_key_name(key)
        if url is None:
            page, links = crawler.crawl_web(key)
            def txn():
                url = Url.get_by_key_name(key)
                if url is None:
                    url = Url(key_name=key, uri=key)
                    for l in links:
                        taskqueue.add(queue_name='url-crawler-queue', url='/queue', params={'key': l})                    
                url.put()
            db.run_in_transaction(txn)

service_mappings = service_handlers.service_mapping(
        [('/worker', WorkerService)         
        ])
service_mappings.append(('/queue', QueueHandler))

application = webapp.WSGIApplication(service_mappings)

def main():
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()