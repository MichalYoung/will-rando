"""
Willamette Randonneurs
  - Overview
  - Events, including pre-registration
  - Pages (static content)
"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import jsonify # For AJAX transactions
from flask import json
from flask import g

from jinja2.exceptions import TemplateNotFound  # Used for /pages/<page>
from werkzeug.exceptions import HTTPException, NotFound # ""

import logging  # For debugging

# For downloading CSV files
import csv, io

# For dates in activations.  Convention:  We
# store all dates as ISO strings, converting
# to and from human-readable forms only for
# presentation.
import arrow


# Our own modules
import config

###
# Globals
###
app = flask.Flask(__name__)
app.debug=config.get("debug")
app.secret_key = config.get("app_key")


###
# Pages (app functionality)
###

@app.route("/")
@app.route("/index")
def index():
  return flask.render_template('index.html')

    
######
#  Routes to static pages
######

@app.route("/pages/<page>")
def pages(page):
  """
  Static content (still with Jinja2 for filling in standard style)
  live in templates/pages.
  """
  app.logger.debug("Request for static page: '{}'".format(page))
  try:
    path = "pages/{}.html".format(page)
    app.logger.debug("Loading page from '{}'".format(path))
    return flask.render_template(path)
  except TemplateNotFound:
    app.logger.debug("Caught TemplateNotFound")
    # We should get TemplateNotFound exception when page URL is wrong
    raise NotFound

#########
# Download center (pdf, doc, etc)
# similar to static pages, but these live
# in 'static/downloads' since they do not need
# to be filled in with jinja2.  Download center
# itself is a template.
#########

@app.route("/downloads/<doc>")
def downloads(doc):
  """
  Static document with no template-filling.
  Downloadable docs live in static/pages.
  """
  app.logger.debug("Request for static document: '{}'".format(doc))
  try:
    path = "static/downloads/{}".format(doc)
    app.logger.debug("Download document from '{}'".format(path))
    return flask.send_file(path)
  except:
    app.logger.debug("Caught exception downloading file")
    # We should get TemplateNotFound exception when page URL is wrong
    raise NotFound


#################
# Functions used within the templates
#################

@app.template_filter( 'filt' )
def format_filt( something ):
    """
    Example of a filter that can be used within
    the Jinja2 code
    """
    return "Not what you asked for"

## Date handling

@app.template_filter('fmtdate')
def fmtdate( date ):
  """
  Turns an arrow ISO date into a human-readable
  date
  """
  return arrow.get(date).format("dddd MMM D")

@app.template_filter('short_date')
def short_date( date ):
  """
  Turns an arrow ISO date into a shorter 
  human-readable date
  """
  return arrow.get(date).format("ddd M/D")

@app.template_filter('day_of_week')
def day_of_week( date ):
  """Shortest data display is 'Tue' """
  return arrow.get(date).format("ddd")


@app.template_filter( 'nl_to_break' )
def nl_to_break( text ):
    """
    Text may have newlines, which we want to convert to <br />
    when formatting for HTML display
    """
    text=text.replace("<", "&lt;")  # To avoid HTML insertion
    text=text.replace("\r", "")
    text=text.replace("\n", "<br />")
    return text


###################
#   Error handlers
###################
@app.errorhandler(404)
def error_404(e):
  app.logger.warning("++ 404 error: {}".format(e))
  return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
  app.logger.warning("++ 500 error: {}".format(e))
  # assert app.debug == False
  return render_template('500.html'), 500

@app.errorhandler(400)
def error_400(e):
  app.logger.warning("++ 403 error: {}".format(e))
  return render_template('403.html'), 403


#############
#
# Launch
#
#############

if __name__ == "__main__":
    port = config.get("port")
    host = config.get("host")
    print("Opening on {}:{}".format(host,port))
    app.run(port=config.get("port"), host=config.get("host"))
else:
    # Running from WSGI server (gunicorn or similar), 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service. 
    """Nothing"""
    
