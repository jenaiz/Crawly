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
import jinja2

from lib import Worker

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
    def render_json(self, param):
        self.response.headers.add_headers('Content-type', 'application/json')
        self.response.out.write(param)

class Link:
  def __init__(self, title, url, text):
    self.title = title
    self.url = url
    self.text = text

class NodesHandler(Handler):
  def get(self):
    #self.render("home.html")
    q = db.GqlQuery('SELECT * FROM Worker')
    workers = q.fetch(1)
    
    self.render("home.html", workers=workers)


class MainHandler(Handler):
  def get(self):
    self.render("dashboard.html")
    

app = webapp2.WSGIApplication([('/nodes', MainHandler), 
                              ('/', NodesHandler)],
                              debug=True)
