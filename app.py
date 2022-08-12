#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from asyncio.windows_events import NULL
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
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import Date, DateTime
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
from sqlalchemy.sql import func, or_



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# show = db.Table('show',
#     db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id'), primary_key=True),
#     db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True),
#     db.Column('start_time', db.DateTime, nullable = False),
#     db.Column('created_at', db.DateTime, nullable = False),
#     db.Column('updated_at', db.DateTime, nullable = True)

# )

class Show(db.Model):
  __tablename__ = 'Show'
  id = db.Column(db.Integer, primary_key = True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column(db.DateTime, nullable = False)
  created_at = db.Column(db.DateTime, nullable = False)
  updated_at = db.Column(db.DateTime, nullable = True)

class City_and_State_Venue(db.Model):
  __tablename__ = 'City_and_State_Venue'
  id = db.Column(db.Integer, primary_key = True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  Show = db.relationship('Venue', backref='venueCityAndState', lazy=True )

class City_and_State_Artist(db.Model):
  __tablename__ = 'City_and_State_Artist'
  id = db.Column(db.Integer, primary_key = True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  Show = db.relationship('Artist', backref='artistCityAndState', lazy=True )

class Artist_Available_Days(db.Model):
  __tablename__ = 'Artist_Available_Days'
  id = db.Column(db.Integer, primary_key = True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  date_available = db.Column(db.DateTime, nullable = False)
  created_at = db.Column(db.DateTime, nullable = False)
  updated_at = db.Column(db.DateTime, nullable = True)
  
 



class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_state_id = db.Column(db.Integer, db.ForeignKey('City_and_State_Venue.id'), nullable=True)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    Genres = db.Column(db.JSON)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    Website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), nullable = False, server_default="false")
    S_Description = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, nullable = False)
    updated_at = db.Column(db.DateTime, nullable = True)
    Show = db.relationship('Show', backref='venueshows', lazy=True )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_state_id = db.Column(db.Integer, db.ForeignKey('City_and_State_Artist.id'), nullable=False)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.JSON)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    Website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), nullable = False, server_default="false")
    S_Description = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, nullable = False)
    updated_at = db.Column(db.DateTime, nullable = True)
    # venues = db.relationship('Venue', secondary=show,backref=db.backref('artists', lazy=True))
    Show = db.relationship('Show', backref='artistshows', lazy=True )
    Available_day = db.relationship('Artist_Available_Days', backref='available', lazy=True )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# db.create_all()



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


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  # Cities = Venue.query.with_entities(Venue.city).group_by(Venue.city)
  # state = Venue.query.with_entities(Venue.state).group_by(Venue.city)
  # venues =  Venue.query.group_by(Venue.city, Venue.state).all()

  venues = Venue.query.all()
  cities = City_and_State_Venue.query.all()
  

  return render_template('pages/venues.html',venues = venues,cities=cities )

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form['search_term']
  if search_term:
    search_term = request.form['search_term']
    result = Venue.query.filter(Venue.name.ilike('%'+ search_term +'%'))
    result2 = City_and_State_Venue.query.filter(or_(City_and_State_Venue.city.ilike('%'+ search_term +'%'), City_and_State_Venue.state.ilike('%'+ search_term +'%')))
    venues_city = result2.order_by(City_and_State_Venue.id).all()
    city_sate_ID = result2.with_entities(City_and_State_Venue.id)
    venue = Venue.query.filter(Venue.city_state_id.in_(city_sate_ID)).all()
    count2 = result2.count() 
    venues = result.order_by(Venue.id).all()
    count = result.count() 
    response = {"count": count+count2,"venues" : venues, "venues_city" : venues_city, "venue":venue}
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
  
    
    # result = Venue.query.filter(Venue.name.ilike('%'+ search_term +'%'))
    # venues = result.order_by(Venue.id).all()
    # count = result.count()
    # response = {"count": count,"venues" : venues}
  else:
    response = NULL
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)
  genres = json.loads(venue.Genres)
  genres_list = ','.join(['{}'.format(value) for value in genres])
  list = str(genres_list).split(',')

  upcoming_shows_count = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).count()
  upcoming_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).all()
  past_shows_count = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time < datetime.now()).count()
  past_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time < datetime.now()).all()
 
  data = {"venue" : venue,"genres" : list ,"upcoming_shows_count" : upcoming_shows_count, "upcoming_shows" : upcoming_shows
  ,"past_shows_count" : past_shows_count, "past_shows" : past_shows }

  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  return render_template('pages/show_venue.html', data = data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website_link = request.form['website_link']
    seeking_talent = request.form.get('seeking_talent',type=bool)
    seeking_description = request.form['seeking_description']
    exists = db.session.query(City_and_State_Venue.id).filter_by(city=city, state = state).first()
    print(exists)
    if not exists:
      city_and_state_venue = City_and_State_Venue(city=city,state=state)
      db.session.add(city_and_state_venue)
      db.session.commit()
    Id =  City_and_State_Venue.query.filter_by(
    city=city, state = state).first()
    venue = Venue(name=name,
    address=address,
    phone=phone,
    Genres=genres,
    image_link=image_link,
    facebook_link=facebook_link,   
    Website_link=website_link,
    S_Description=seeking_description,
    seeking_talent=seeking_talent,
    created_at = datetime.now(),
    city_state_id =Id.id)
    
    db.session.add(venue)
    db.session.commit() 
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash(sys.exc_info(), 'error')
    # print(sys.exc_info())
  finally:
    recent_artists = Artist.query.order_by(Artist.created_at).limit(10).all()
    recent_venues = Venue.query.order_by(Venue.created_at).limit(10).all()
    data = {"recent_artists":recent_artists,"recent_venues":recent_venues}

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html',data =data)  #  print()
  
  
     
      
  

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  search_term = request.form['search_term']
  if search_term:

    result = Artist.query.filter(Artist.name.ilike('%'+ search_term +'%'))
    result2 = City_and_State_Artist.query.filter(or_(City_and_State_Artist.city.ilike('%'+ search_term +'%'), City_and_State_Artist.state.ilike('%'+ search_term +'%')))
    artists_city = result2.order_by(City_and_State_Artist.id).all()
    city_sate_ID = result2.with_entities(City_and_State_Artist.id)
    artist = Artist.query.filter(Artist.city_state_id.in_(city_sate_ID)).all()
    count2 = result2.count() 
    artists = result.order_by(Artist.id).all()
    count = result.count() 
    response = {"count": count+count2,"artists" : artists, "artists_city" : artists_city, "artist":artist}
  else:
    response = NULL
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
  
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  form = ArtistAvailabiltyForm()
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  #This was done to display each of the genres since it was return as a string.
  artist = Artist.query.get(artist_id)
  genres = json.loads(artist.genres)
  genres_list = ','.join(['{}'.format(value) for value in genres])
  list = str(genres_list).split(',')

  # show = Show.query.filter_by()
  upcoming_shows_count = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).count()
  upcoming_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).all()
  past_shows_count = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time < datetime.now()).count()
  past_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time < datetime.now()).all()

  available_days = Artist_Available_Days.query.filter_by(artist_id= artist_id).order_by(Artist_Available_Days.created_at).all()

  data = {"artist" : artist,"genres" : list ,"upcoming_shows_count" : upcoming_shows_count, "upcoming_shows" : upcoming_shows
  ,"past_shows_count" : past_shows_count, "past_shows" : past_shows , "available_days" : available_days }
  return render_template('pages/show_artist.html', data =data, form=form)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    
    artist = Artist.query.get(artist_id)
    
    artist.name = request.form['name']
    artist.genres = request.form.getlist('genres')
    city=request.form['city']
    state=request.form['state']
    exists = db.session.query(City_and_State_Artist.id).filter_by(city=city, state = state).first()

   
    if not exists:
      city_and_state_artist = City_and_State_Artist(city=city,state=state)
      
      db.session.add(city_and_state_artist)
      db.session.commit()
    Id =  City_and_State_Artist.query.filter_by(city=city, state = state).with_entities(City_and_State_Artist.id)
    artist.city_state_id = Id
    artist.phone = request.form['phone']
    artist.Website_link = request.form['website_link']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_venue = request.form.get('seeking_venue',type=bool, default=False)
    artist.S_description = request.form['seeking_description']
    artist.image_link = request.form['image_link']
    artist.update_at = datetime.now()
   
    db.session.commit()
    flash('Astist ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    flash(sys.exc_info(), 'error')
  finally:
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    return redirect(url_for('show_artist', artist_id=artist_id))
    


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  try:
   
   venue = Venue.query.get(venue_id)
   venue.name = request.form['name']
   venue.Genres = request.form.getlist('genres')
   venue.address = request.form['address']
   city=request.form['city']
   state=request.form['state']
   exists = db.session.query(City_and_State_Venue.id).filter_by(city=city, state = state).first()

   
   if not exists:
     city_and_state_venue = City_and_State_Venue(city=city,state=state)
     
     db.session.add(city_and_state_venue)
     db.session.commit()
   Id =  City_and_State_Venue.query.filter_by(city=city, state = state).with_entities(City_and_State_Venue.id)
   venue.city_state_id = Id
   venue.phone = request.form['phone']
   venue.Website_link = request.form['website_link']
   venue.facebook_link = request.form['facebook_link']
   venue.seeking_talent = request.form.get('seeking_talent',type=bool, default=False)
   venue.S_description = request.form['seeking_description']
   venue.image_link = request.form['image_link']
   venue.updated_at = datetime.now()
   db.session.commit()
   flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    db.session.rollback()
    flash(sys.exc_info(), 'error')
    # print(sys.exc_info())
  finally:

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    facebook_link = request.form['facebook_link']
    image_link = request.form['image_link']
    website_link = request.form['website_link']
    seeking_venue = request.form.get('seeking_venue',type=bool)
    seeking_description = request.form['seeking_description']
    exists = db.session.query(City_and_State_Artist.id).filter_by(city=city, state = state).first()

   
    if not exists:
      city_and_state_artist = City_and_State_Artist(city=city,state=state)
      db.session.add(city_and_state_artist)
      db.session.commit()
    Id =  City_and_State_Artist.query.filter_by(city=city, state = state).first()
    artist = Artist(
    name=name,
    phone=phone,
    genres=genres,
    image_link=image_link,
    facebook_link=facebook_link,   
    Website_link=website_link,
    S_Description=seeking_description,
    seeking_venue=seeking_venue,
    city_state_id=Id.id,
    created_at = datetime.now())
    db.session.add(artist)
    db.session.commit() 
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash(sys.exc_info(), 'error')
  finally:
    recent_artists = Artist.query.order_by(Artist.created_at).limit(10).all()
    recent_venues = Venue.query.order_by(Venue.created_at).limit(10).all()
    data = {"recent_artists":recent_artists,"recent_venues":recent_venues}
   # called upon submitting the new artist listing form
   # TODO: insert form data as a new Venue record in the db, instead
   # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html', data =data)


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
