#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import crawler

from google.appengine.api import taskqueue
from google.appengine.ext import db

class Url(db.Model):
  uri = db.StringProperty(required=True)
  content = db.StringProperty(required=False)
  downloaded_date = db.DateProperty()
  server = db.StringProperty(required=False)
  error = db.BooleanProperty(indexed=False)
  error_message = db.StringProperty(required=False)
  
class MainHandler(webapp2.RequestHandler):
    def get(self):
        key = self.request.get("key")
        taskqueue.add(url='/worker', params={'key': key})
        self.response.out.write('url -> ' + key)

class CounterWorker(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        #crawler.crawl_web(key)
        def txn():
            url = Url.get_by_key_name(key)
            if url is None:
                url = Url(key_name=key, uri=key)
            url.put()
        db.run_in_transaction(txn)

app = webapp2.WSGIApplication([('/', MainHandler),
                                ('/worker', CounterWorker)],
                                debug=True)
