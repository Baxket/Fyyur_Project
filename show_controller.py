

from forms import *
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
import sys
from datetime import datetime
from sqlalchemy.sql import func, or_
from models import *
from asyncio.windows_events import NULL

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = Show.query.all()
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # try:
    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    check_artist = Artist.query.get(artist_id)
    check_venue = Venue.query.get(venue_id)
    # day = start_time.strftime("%m/%d/%Y")
    
    check_if_available_date = Artist_Available_Days.query.filter_by(artist_id =artist_id).filter(func.date(Artist_Available_Days.date_available) == start_time ).all()
    today = datetime.now()
    
    # today = datetime.strptime(today, date_format_str)
    date_time = datetime. strptime(start_time, '%Y-%m-%d %H:%M:%S')
   

    if check_venue and check_artist:
         if date_time > today:

           if check_if_available_date:
             check_if_available_time = Artist_Available_Days.query.filter_by(artist_id =artist_id).filter(Artist_Available_Days.date_available < start_time ).first()
             if check_if_available_time:
               created_at = datetime.today()
               show = Show(artist_id = artist_id, venue_id = venue_id, start_time =start_time, created_at = created_at)
               db.session.add(show)
               Artist_Available_Days.query.filter_by(artist_id =artist_id).filter(func.date(Artist_Available_Days.date_available) == start_time ).delete(synchronize_session=False)
               db.session.commit()
               flash('Show was successfully listed!')
             else:
               flash('Sorry Artist is availble on this date but not around this time. Check Artist Page for more details!')
           else:
             flash('Sorry Artist is not Availble on this date. Check Artist Page for more details!')
         else:
          
           flash('Sorry, the time you entered is past')
    else:
      if not check_artist and not check_venue:
        flash('Artist and Venue entered does not exist!', 'error')
      elif not check_venue:
        flash('Venue entered does not exist!', 'error')
      elif not check_artist:
        flash('Artist entered does not exist!', 'error')
   
  # except:
  #   db.session.rollback()
  #   flash(sys.exc_info(), 'error')
  # finally:
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
