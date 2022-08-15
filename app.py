#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


import json
from re import I
from tracemalloc import start
from turtle import back
from typing import final
from zoneinfo import available_timezones
import dateutil.parser
import babel
from markupsafe import Markup
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from models import *
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import Date, DateTime
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
from sqlalchemy.sql import func, or_
from artist_controller import *
from venue_controller import *
from artist_availability_controller import *
from show_controller import *




#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#





#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

# @app.template_filter('timeago')
# def fromnow(date):
#   return timeago.format(date, datetime.datetime.now())

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  date_1 = '24/7/2021 11:18:08.230010'
  date_2 = '24/7/2021 11:14:18.333338'
  if date_1 > date_2:
    print("True")
  else:
    print("false")
  recent_artists = Artist.query.order_by(Artist.created_at).limit(10).all()
  recent_venues = Venue.query.order_by(Venue.created_at).limit(10).all()
  data = {"recent_artists":recent_artists,"recent_venues":recent_venues}
  return render_template('pages/home.html', data = data )


  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
