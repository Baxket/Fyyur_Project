
from forms import *
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
import sys
from datetime import datetime
from sqlalchemy.sql import func, or_
from models import *
from asyncio.windows_events import NULL


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
  genres = venue.Genres

  # list = []
  # genres = json.loads(venue.Genres)
  # genres_list = ','.join(['{}'.format(value) for value in genres])
  # list = str(genres_list).split(',')
  # for genre in genres:
    
  #   list.append(genre)
  upcoming_shows_count = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).count()
  upcoming_shows = Show.query.join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time > datetime.now()).all()
  past_shows_count = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time < datetime.now()).count()
  past_shows = Show.query.join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time < datetime.now()).all()
 
  data = {"venue" : venue,"genres" : genres ,"upcoming_shows_count" : upcoming_shows_count, "upcoming_shows" : upcoming_shows
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
    db.session.close()

    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html',data =data)  #  print()
  
  
     
      
  

@app.route('/venues/delete/<venue_id>', methods=['DELETE','GET'])
def delete_venue(venue_id):
    # try:
        Venue.query.filter_by(id=venue_id).delete()
    
        db.session.commit()
        flash('This venue has been successfully deleted!')
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
   

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    


#  Update
#  ----------------------------------------------------------------


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.venueCityAndState.city
  form.state.data = venue.venueCityAndState.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = [genre for genre in venue.Genres]
  form.facebook_link.data = venue.facebook_link
  form.image_link.data = venue.image_link
  form.website_link.data = venue.Website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.S_Description
  

  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
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
    db.session.close()

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))
