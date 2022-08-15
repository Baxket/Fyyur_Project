from forms import *
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
import sys
from datetime import datetime
from sqlalchemy.sql import func, or_
from models import *
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


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.artistCityAndState.city
  form.state.data = artist.artistCityAndState.state
  form.phone.data = artist.phone
  form.genres.data = [genre for genre in artist.genres]
  form.facebook_link.data = artist.facebook_link
  form.image_link.data = artist.image_link
  form.website_link.data = artist.Website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.S_Description
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
  genres = artist.genres
  # #  genres = json.loads(artist.genres)
  # genres_list = ','.join(['{}'.format(value) for value in genres])
  # list = str(genres_list).split(',')

  # show = Show.query.filter_by()
  upcoming_shows_count = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).count()
  upcoming_shows = Show.query.join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time > datetime.now()).all()
  past_shows_count = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time < datetime.now()).count()
  past_shows = Show.query.join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time < datetime.now()).all()

  available_days = Artist_Available_Days.query.filter_by(artist_id= artist_id).order_by(Artist_Available_Days.created_at).all()

  data = {"artist" : artist,"genres" : genres ,"upcoming_shows_count" : upcoming_shows_count, "upcoming_shows" : upcoming_shows
  ,"past_shows_count" : past_shows_count, "past_shows" : past_shows , "available_days" : available_days }
  return render_template('pages/show_artist.html', data =data, form=form)


@app.route('/artists/delete/<artist_id>', methods=['DELETE','GET'])
def delete_artist(artist_id):
    # try:
        Artist.query.filter_by(id=artist_id).delete()
    
        db.session.commit()
        flash('This Artist has been successfully deleted!')
    # except:
    #     db.session.rollback()
    #     flash(sys.exc_info(), 'error')
    # finally:
      
        recent_artists = Artist.query.order_by(Artist.created_at).limit(10).all()
        recent_venues = Venue.query.order_by(Venue.created_at).limit(10).all()
        data = {"recent_artists":recent_artists,"recent_venues":recent_venues}
  #     called to create new shows in the db, upon submitting new show listing form
  #     TODO: insert form data as a new Show record in the db, instead
    
  #     on successful db insert, flash success
      
  #     TODO: on unsuccessful db insert, flash an error instead.
  #     e.g., flash('An error occurred. Show could not be listed.')
  #     see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        return render_template('pages/home.html', data = data)
   