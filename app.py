#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    address_id = db.Column(db.Integer,db.ForeignKey('address.id'),nullable =False,)
    shows = db.relationship('Show',backref='venue_show',lazy = True , cascade='all,delete-orphan')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    address_id = db.Column(db.Integer,db.ForeignKey('address.id'),nullable =False)
    shows = db.relationship('Show',backref='artist_show',lazy = True)

class Address(db.Model):
      __tablename__='address'
      id = db.Column(db.Integer,primary_key=True)
      city = db.Column(db.String(),nullable= False)
      state = db.Column(db.String(),nullable = False)
      artists = db.relationship('Artist',backref='address_info_a',lazy = True)
      venues = db.relationship('Venue', backref='address_info_v' ,lazy = True)

class Show(db.Model):
      __tablename__='show'
      id = db.Column(db.Integer,primary_key = True)
      start_time =db.Column(db.DateTime(),nullable = False)
      type = db.Column(db.String(), nullable =True)
      artist_id = db.Column(db.Integer,db.ForeignKey('Artist.id'),nullable =False)
      venue_id = db.Column(db.Integer,db.ForeignKey('Venue.id',ondelete='CASCADE'),nullable =False)
      
      


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


@app.template_filter('strftime')
def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data1 =Address.query.all()

  return render_template('pages/venues.html', areas=data1);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  name =request.form['search_term']
  response1 = Venue.query.filter(Venue.name.ilike('%'+name+'%')) # Venue.query.filter_by(name = name)
  count =Venue.query.filter(Venue.name.ilike('%'+name+'%')).count()
  return render_template('pages/search_venues.html', 
  results=response1,count=count , search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  vu =Venue.query.get(venue_id)
  genres= vu.genres.split(',')

  print(genres)
  now = datetime.datetime.now()
  for sh in  vu.shows:
       
        if now < sh.start_time :
              sh.type = 'upcoming'
        else :
          sh.type = 'past'    
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=vu ,genres= genres)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  body = {}
  try:
    generies = request.form.getlist('genres')
    genstr = ",".join(map(str,generies))
    state = request.form['state']
    city = request.form['city']
    address = request.form['address']
    name = request.form['name']
    phone = request.form['phone']
    face_link = request.form['facebook_link'] 
    img_link = request.form['image_link']  #"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcReZvvWD7eGf-lXe7TVk5jUUrFPTwUrENgtXA&usqp=CAU"
   
    venue = Venue(genres= genstr ,name =name ,address =address ,phone=phone ,facebook_link =face_link
    ,image_link=img_link )
    address1 =  Address(city =city,state=state)
    addquer = Address.query.filter_by(city=city).filter_by(state=state).count()
    address1 =  Address(city =city,state=state)
    if addquer > 0:
          address1 = Address.query.filter_by(city=city).filter_by(state=state).first()
          print(addquer )
          print(address1)
          venue.address_id = address1.id
          db.session.add(venue)
          db.session.commit()
    else:
          venue.address_info_v = address1 
          db.session.add(address1)
          db.session.commit()
    body['good'] = True
  except:
    db.session.rollback()
    error = True
    print(sys.exc_info())
  finally:
        db.session.close()
  if error:
        abort(500)
  else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  

@app.route('/venues/delete/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
      
      Venue.query.filter_by(id = venue_id).delete()
      db.session.commit()
      flash('Venue Deleted Successfully ')
      return render_template('pages/home.html')

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data1 = Artist.query.all()
  
  return render_template('pages/artists.html', artists=data1)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
 
  name =request.form['search_term']
  response1 = Artist.query.filter(Artist.name.ilike('%'+name+'%')) # Venue.query.filter_by(name = name)
  count =Artist.query.filter(Artist.name.ilike('%'+name+'%')).count()
  return render_template('pages/search_artists.html', results=response1,count=count, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  ar = Artist.query.get(artist_id)
  genres= ar.genres.split(',')
 
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  now = datetime.datetime.now()
  for sh in  ar.shows:
       
        if now < sh.start_time :
              sh.type = 'upcoming'
        else :
          sh.type = 'past'      
  return render_template('pages/show_artist.html', artist=ar,genres=genres )

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
 
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist )

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
      error = false
      try :
        artist = Artist.query.get(artist_id)
        generies = request.form.getlist('genres')
        artist.genres = ",".join(map(str,generies))
        artist.name = request.form['name']
        artist.phone = request.form['phone']
        artist.facebook_link = request.form['facebook_link'] 
        artist.image_link = request.form['image_link']
        state = request.form['state']
        city = request.form['city']
        if  artist.address_info_a.city == city and artist.address_info_a.state == state :
              db.session.commit() 
        else:
              addquer = Address.query.filter_by(city=city).filter_by(state=state).count()
              if addquer > 0 :
                    address1 = Address.query.filter_by(city=city).filter_by(state=state).first()
                    artist.address_id = address1.id
                    db.session.commit()
              else :
                    address1 =  Address(city =city,state=state)
                    db.session.add(address1)
                    artist.address_info_a =address1
                    db.session.commit()
      except:
        error = true 
        db.session.rollback()
      finally:
        db.session.close()
      if error :
            form = ArtistForm()
            artist = Artist.query.get(artist_id)
            flash('Error ' + artist.name + ' was unsuccessfully updated!')
            return render_template('pages/home.html')
            return render_template('forms/edit_artist.html', form=form, artist=artist )
      else:
            flash('Artist ' + artist.name + ' successfully updated!')
            return redirect(url_for('show_artist', artist_id=artist.id))
            
                   
  

                  
             
                  
            
    
    

  

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
      error = false
      try :
        venue = Venue.query.get(venue_id)
        generies = request.form.getlist('genres')
        venue.genres = ",".join(map(str,generies))
        venue.name = request.form['name']
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        venue.facebook_link = request.form['facebook_link'] 
        venue.image_link = request.form['image_link']
        state = request.form['state']
        city = request.form['city']
        if  venue.address_info_v.city == city and venue.address_info_v.state == state :
              db.session.commit() 
        else:
              addquer = venue.query.filter_by(city=city).filter_by(state=state).count()
              if addquer > 0 :
                    address1 = Address.query.filter_by(city=city).filter_by(state=state).first()
                    venue.address_id = address1.id
                    db.session.commit()
              else :
                    address1 =  Address(city =city,state=state)
                    db.session.add(address1)
                    venue.address_info_a =address1
                    db.session.commit()
      except:
        error = true 
        db.session.rollback()
      finally:
        db.session.close()
      if error :
            form = ArtistForm()
            artist = Artist.query.get(artist_id)
            flash('Error ' + venue.name + ' was unsuccessfully updated!')
            return render_template('forms/edit_venue.html', form=form, venue=venue )
      else:
            flash('Venue ' + venue.name + ' successfully updated!')
            return redirect(url_for('show_venue', venue_id=venue.id))
      
      

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = Artist_Form_new()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
      error = False
      body = {}
      try:
        generies = request.form.getlist('genres')
        genstr = ",".join(map(str,generies))
        state = request.form['state']
        city = request.form['city']
        name = request.form['name']
        phone = request.form['phone']
        face_link = request.form['facebook_link'] 
        img_link = request.form['image_link'] #"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcReZvvWD7eGf-lXe7TVk5jUUrFPTwUrENgtXA&usqp=CAU"
        print( genstr )
        print('stste is ' + state +' ' +city)
        print("name" + name)
        print('phone' + phone)
        print('face' + face_link)
        artist = Artist(genres= genstr ,name =name  ,phone=phone ,facebook_link =face_link
        ,image_link=img_link )
        addquer = Address.query.filter_by(city=city).filter_by(state=state).count()
        address1 =  Address(city =city,state=state)
        if addquer > 0:
              address1 = Address.query.filter_by(city=city).filter_by(state=state).first()
              print(addquer )
              print(address1)
              artist.address_id = address1.id 
              db.session.add(artist)
              db.session.commit()
        else:
              artist.address_info_a = address1 
              db.session.add(address1)
              db.session.commit()
        #flash(' Artist ' + artist.name + 'inserted successfully' )
        body['good'] = True
      except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
      finally:
        db.session.close()
      if error:
            flash('An error occurred. Artist ' + artist.name+ ' could not be listed.')
            return render_template('pages/home.html')
            
      else:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
            return render_template('pages/home.html')
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
 # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows =Show.query.all()
  
  now = datetime.datetime.now()
  for sh in  shows:
       
        if now < sh.start_time :
              sh.type = 'upcoming'
        else :
              sh.type = 'past'    
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm() #show_form_new() we can use this for if we do name uniqu field in db 
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
      error = False 
      try:
        artist_id= request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']
        artist = Artist.query.get(artist_id)
        venue = Venue.query.get(venue_id)
        if artist != None  and venue !=  None :
              show = Show(start_time=start_time)
              show.artist_show = artist
              show.venue_show = venue
              db.session.add(artist)
              db.session.commit()
              flash('Show was successfully listed!')
        else:
             flash('error id of artist or venue not true.','error')
             return redirect(url_for('create_shows'))
      except:
        db.session.rollback()
        error = True
        #print(sys.exc_info())
      finally:
        db.session.close()  
      if error:
            flash('An error occurred. Show could not be listed.','error')
            return render_template('pages/home.html')
      else:
            return render_template('pages/home.html')    
            # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
 
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  
@app.route('/show/search', methods=['POST'])
def search_show():
      
      name =request.form['search_term']
      print(name)
      response1 = Artist.query.filter(Artist.name.ilike('%'+name+'%')).first()
      if response1 == None :
            response1 = Venue.query.filter(Venue.name.ilike('%'+name+'%')).first()


      print(response1.shows) 
      return render_template('pages/show.html',
       result=response1.shows, search_term=request.form.get('search_term', ''))

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
