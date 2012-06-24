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
import os
import time

from google.appengine.ext.webapp import template
from protorpc import messages
from protorpc import message_types
from protorpc import remote

class Link:
  def __init__(self, title, url, text):
    self.title = title
    self.url = url
    self.text = text

class MainHandler(webapp2.RequestHandler):
  def get(self):
    template_values = {
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

    
class SearchHandler(webapp2.RequestHandler):
  def post(self):
    l1 = Link('link 1', 'url1', 'Lorem Ipsum es simplemente el texto de relleno de las imprentas ... 1')
    l2 = Link('link 2', 'url2', 'Lorem Ipsum es simplemente el texto de relleno de las imprentas ... 2')
    l3 = Link('link 3', 'url3', 'Lorem Ipsum es simplemente el texto de relleno de las imprentas ... 3')
    links = []
    links.append(l1)
    links.append(l2)
    links.append(l3)
    template_values = {
      'query': self.request.get('q'),
      'links': links
      }

    path = os.path.join(os.path.dirname(__file__), 'results.html')
    self.response.out.write(template.render(path, template_values))
  
app = webapp2.WSGIApplication([('/', MainHandler), 
                              ('/search', SearchHandler)],
                              debug=True)

