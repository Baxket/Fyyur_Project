
from forms import *
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
import sys
from datetime import datetime
from sqlalchemy.sql import func, or_
from models import *
from asyncio.windows_events import NULL

@app.route('/artist_availabilty/add/<artist_id>', methods=['POST'])
def add_date_available(artist_id):
  form = ArtistAvailabiltyForm()
  try:
    date = request.form['available_date']

    created_at = datetime.now()
    add = Artist_Available_Days(artist_id = artist_id,date_available = date, created_at =created_at)
    db.session.add(add)
    db.session.commit()
    return flash('Date was successfully added!')

  except:
    db.session.rollback()
    return flash(sys.exc_info(), 'error')
  finally:
    recent_artists = Artist.query.order_by(Artist.created_at).limit(10).all()
    recent_venues = Venue.query.order_by(Venue.created_at).limit(10).all()
    data = {"recent_artists":recent_artists,"recent_venues":recent_venues}
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html', data = data)
  
    