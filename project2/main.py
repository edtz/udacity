#!/usr/bin/env python2
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
import os
import random
import string
import webapp2
import jinja2
from hashlib import sha512 as hasher

from google.appengine.ext import db


# Models
class User(db.Model):
    name = db.StringProperty(required=True)
    pwdhash = db.StringProperty(required=True)
    salt = db.StringProperty(required=True)

class Post(db.Model):
    user = db.IntegerProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Comment(db.Model):
    user = db.IntegerProperty(required=True)
    post = db.StringProperty(required=True)
    content = db.TextProperty(required=True)

class Like(db.Model):
    user = db.IntegerProperty(required=True)
    post = db.StringProperty(required=True)

# Helpers
class Handler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.messages = []
        self.user = None
        cookie = self.request.cookies.get("user")
        if cookie:
            cookie = cookie.split("|")
            user = get_user(cookie[0])
            if user and user.pwdhash == cookie[1]:
                self.user = user

    def write(self, *a, **kw):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(
            template,
            messages=self.messages,
            user=self.user,
            **kw
            ))


def get_user(name):
    return User.all().filter("name =", name).get()

def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hasher(name + pw + salt).hexdigest()
    return (h, salt)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# Views
class PostList(Handler):
    def get(self):
        self.render("post_list.html")

class PostDetail(Handler):
    def get(self):
        self.render("post_detail.html")

class PostCreate(Handler):
    def get(self):
        self.render("post_create.html")

class PostUpdate(Handler):
    def get(self):
        self.render("post_update.html")

class PostDelete(Handler):
    def get(self):
        self.render("post_delete.html")

class PostLike(Handler):
    def get(self):
        self.render("post_like.html")

class CommentCreate(Handler):
    def get(self):
        self.render("comment_create.html")

class CommentUpdate(Handler):
    def get(self):
        self.render("comment_update.html")

class CommentDelete(Handler):
    def get(self):
        self.render("comment_delete.html")

class SignupView(Handler):
    def get(self):
        if self.user:
            self.messages.append((
                'warning',
                "You can't create a new account"
                " if you're already logged in.",
            ))
        self.render("signup.html")

    def post(self):
        name = self.request.get('name')
        pwd = self.request.get('pass')
        if self.user:
            self.messages.append((
                'error',
                "You can't create a new account"
                " if you're already logged in.",
            ))
        elif get_user(name):
            self.messages.append((
                'error',
                'This username is not available.',
            ))
        else:
            (pwdhash, salt) = make_pw_hash(name, pwd)
            user = User(
                name=name,
                pwdhash=pwdhash,
                salt=salt
            )
            user.put()
            self.response.set_cookie("user", "|".join((name, pwdhash)))
            self.user = user
            self.messages.append((
                'info',
                'Thank you for registration, %s.' % user.name,
            ))
            return self.redirect("/")
        self.render("signup.html")

class LoginView(Handler):
    def get(self):
        if self.user:
            self.redirect("/")
        self.render("login.html")

    def post(self):
        if self.user:
            self.redirect("/")
        name = self.request.get('name')
        pwd = self.request.get('pass')
        user = get_user(name)
        if user:
            h1 = user.pwdhash
            h2 = make_pw_hash(name, pwd, user.salt)[0]
            if h1 == h2:
                self.response.set_cookie("user", "|".join((name, h2)))
                self.redirect("/")
        self.messages.append((
            'error',
            'Incorrect login info.',
        ))
        self.render("login.html")

class LogoutView(Handler):
    def get(self):
        if self.user:
            self.response.delete_cookie("user")
        self.redirect("/")


app = webapp2.WSGIApplication([
    ('/', PostList),
    ('/([0-9]+)', PostDetail),
    ('/newpost', PostCreate),
    ('/([0-9]+)/update', PostUpdate),
    ('/([0-9]+)/delete', PostDelete),
    ('/([0-9]+)/like', PostLike),
    ('/([0-9]+)/comment/', CommentCreate),
    ('/([0-9]+)/comment/([0-9]+)/update', CommentUpdate),
    ('/([0-9]+)/comment/([0-9]+)/delete', CommentDelete),
    ('/signup', SignupView),
    ('/login', LoginView),
    ('/logout', LogoutView),
], debug=True)
