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

class MainHandler(Handler):
  def get(self):
    self.render("home.html")
    
class SearchHandler(Handler):
  def post(self):
    l1 = Link('The white house is a Big House', 'url1', 'Lorem Ipsum es simplemente el texto de relleno de las imprentas ... 1 simplemente el texto de relleno de las imprentas simplemente el texto de relleno de las imprentas')
    l2 = Link('How to repair a computer', 'url2', 'Lorem Ipsum es simplemente el texto de relleno de las imprentas ... 2  simplemente el texto de relleno de las imprentas simplemente el texto de relleno de las imprentas')
    l3 = Link('link 3', 'url3', 'Lorem Ipsum es simplemente el texto de relleno de las imprentas ... 3  simplemente el texto de relleno de las imprentas simplemente el texto de relleno de las imprentas')
    links = []
    links.append(l1)
    links.append(l2)
    links.append(l3)

    self.render("list.html", query=self.request.get('q'), links=links)

class TwitterHandler(Handler):
  def get(self):
    self.render("twitter.html")

    

class SignupHandler(Handler):
  def get(self):
      self.render('signup.html', username='', email='', username_error='', password_error='', verify_error='', email_error='')
  def post(self):
      username = self.request.get('username')
      email = self.request.get('email')
      password = self.request.get('password')
      verify = self.request.get('verify')

      username_valid = valid_username(username)
      password_valid = valid_password(password)
      equal_passwords = (password == verify)
      email_valid = valid_email(email)
      if email == '':
          email_valid = True

      if (username_valid and password_valid and email_valid and equal_passwords and not user_exist(username)):
          h = make_pw_hash(username, password).split('|')
          
          a = User(username = username, password = h[0], salt = h[1], email = email)
          a.put()
          
          cookie = '%s|%s' % (a.key().id(), h[0])
          
          self.response.headers.add_header('Set-Cookie', 'user_id=%s' % str(cookie))
          
          self.redirect('/welcome')
      else:
          username_error = ''
          password_error = ''
          verify_error = ''
          email_error = ''
          if user_exist(username):
              username_error = 'That user already exists.'
          if not username_valid:
              username_error = "That's not a valid username."
          if not password_valid:
              password_error = "That's wasn't a valid password."
          if not equal_passwords:
              verify_error = "Your password didn't match."
          if email != '' and not email_valid:
              email_error = "That's not a valid email."
          self.render('signup.html', username=username, email=email, username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error)

app = webapp2.WSGIApplication([('/', MainHandler), 
                              ('/search', SearchHandler),
                              ('/twitter', TwitterHandler),
                              ('/signup', SignupHandler)],
                              debug=True)

