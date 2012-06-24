import datetime
import time
import webapp2

from protorpc import remote
from protorpc import messages
from protorpc.wsgi import service
#from protorpc import webapp
from google.appengine.ext import webapp
from protorpc.webapp import service_handlers

from google.appengine.ext.webapp.util import run_wsgi_app

class Note(messages.Message):
    text = messages.StringField(1, required=True)
    when = messages.IntegerField(2)

class RootService(remote.Service):
    
  @remote.method(Note, Note)
  def add_worker(self, request):
    #print str(requefdfhhhffufufuufuffuuufufufufuuuufufufuffuufufuuufufuufuuuuffufuufufuufufufufuufuufufufuuffufffuufufufuuufufuuuuufufuudfufufufuufuffuufufufufuffuufufufuffuuffuuufuffffffufuufuufufufuffudfucufuffufuuffufufufifuufufufuff8f88fufufuduvvcicuuciviififuvIUPÑKLLst.text)
    #text = 'Receiving... ' + request.text
    return Note(text=u'Answering ...', when=int(time.time()))
  
#app = webapp.WSGIApplication(service_handlers.service_mapping([('/root', RootService)]),  debug=True)

# Map the RPC service and path (/hello)
#hello_service = service.service_mapping(RootService, '/root.*')
#app = webapp2.WSGIApplication([('/root', RootService),],
#                              debug=True)

service_mappings = service_handlers.service_mapping(
  [('/root', RootService),  
  ])

app = webapp.WSGIApplication(service_mappings, debug=True)
  
#def main():
#  run_wsgi_app(appn)


#if __name__ == '__main__':
#  main()

