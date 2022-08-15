from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


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
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete = "CASCADE"), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete = "CASCADE"), nullable=False)
  start_time = db.Column(db.DateTime, nullable = False)
  created_at = db.Column(db.DateTime, nullable = False)
  updated_at = db.Column(db.DateTime, nullable = True)

class City_and_State_Venue(db.Model):
  __tablename__ = 'City_and_State_Venue'
  id = db.Column(db.Integer, primary_key = True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  Show = db.relationship('Venue',passive_deletes=True, backref='venueCityAndState', lazy=True )

class City_and_State_Artist(db.Model):
  __tablename__ = 'City_and_State_Artist'
  id = db.Column(db.Integer, primary_key = True)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  Show = db.relationship('Artist',passive_deletes=True, backref='artistCityAndState', lazy=True )

class Artist_Available_Days(db.Model):
  __tablename__ = 'Artist_Available_Days'
  id = db.Column(db.Integer, primary_key = True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id',ondelete = "CASCADE"), nullable=False)
  date_available = db.Column(db.DateTime, nullable = False)
  created_at = db.Column(db.DateTime, nullable = False)
  updated_at = db.Column(db.DateTime, nullable = True)
  
 



class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_state_id = db.Column(db.Integer, db.ForeignKey('City_and_State_Venue.id',ondelete = "CASCADE"), nullable=True)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    Genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    Website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), nullable = False, server_default="false")
    S_Description = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, nullable = False)
    updated_at = db.Column(db.DateTime, nullable = True)
    Show = db.relationship('Show',passive_deletes=True, backref='venueshows', lazy=True )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city_state_id = db.Column(db.Integer, db.ForeignKey('City_and_State_Artist.id',ondelete = "CASCADE"), nullable=False)
    # city = db.Column(db.String(120))
    # state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    Website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean(), nullable = False, server_default="false")
    S_Description = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, nullable = False)
    updated_at = db.Column(db.DateTime, nullable = True)
    # venues = db.relationship('Venue', secondary=show,backref=db.backref('artists', lazy=True))
    Show = db.relationship('Show',passive_deletes=True, backref='artistshows', lazy=True )
    Available_day = db.relationship('Artist_Available_Days',passive_deletes=True, backref='available', lazy=True )

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


# db.create_all()