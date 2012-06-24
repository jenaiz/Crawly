import datetime
import time

from protorpc import message_types
from protorpc import remote
from protorpc import messages

class Note(messages.Message):
    text = messages.StringField(1, required=True)
    when = messages.IntegerField(2)

class RootService(remote.Service):

  @remote.method(Note, Note)
  def add_worker(self, request):
    print str(request.text)
    
    return Note(text=u'adding: ...', when=int(time.time()))