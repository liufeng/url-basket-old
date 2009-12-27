#!/usr/bin/env python

import os
import datetime
import urllib

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

class URLEntity(db.Model):
  url = db.LinkProperty()
  time = db.DateTimeProperty(auto_now_add=True)
  title = db.StringProperty()

class HomePage(webapp.RequestHandler):
  def get(self):
    url_query = URLEntity.all().order('-time')
    url_lists = url_query.fetch(10)

    template_values = {
      'urls' : url_lists,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class AddLink(webapp.RequestHandler):
  def post(self):
    newLink = URLEntity()
    url = self.request.get('url')
    if url[0:4] != 'http' or url[0:3] != 'ftp':
      url = 'http://' + url
    newLink.url = url
    newLink.title = self.getTitle(url)
    newLink.put()
    self.redirect('/')

  def getTitle(self, url):
    sock = urllib.urlopen(url)
    html = sock.read()
    sock.close()
    index1 = html.find('<title>')
    if index1 == -1:
      return None
    index2 = html.find('</title>', index1)
    return html[index1 + len('<title>'):index2].strip()

def main():
  application = webapp.WSGIApplication([('/', HomePage), ('/add', AddLink)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
