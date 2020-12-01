from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL,Length
from enum import Enum
from app import Artist,Venue







class ShowForm(Form):
    artist_id = StringField(
        'artist_id',
         validators=[DataRequired() ]
    )
    venue_id = StringField(
        'venue_id',
         validators=[DataRequired()],
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

 
class Genres(Enum):
    Alternative = 'Alternative'
    Blues = 'Classical'
    Classical = 'Country'
    Country = 'Electronic'
    Electronic = 'Folk'
    Folk = 'Funk'
    Funk = 'Hip-Hop'
    Hip_Hop = 'Heavy Metal'
    Heavy_Metal = 'Instrumental'
    Instrumental = 'Jazz'
    Jazz = 'Musical Theatre'
    Musical_Theatre = 'Pop'
    Pop = 'Punk'
    Punk = 'R&B'
    Reggae = 'Reggae'
    Rock_n_Roll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'


class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    image_link=StringField('image_link',
    validators=[DataRequired() ,URL(message='Enter Valid URL '),])
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    
    genres = SelectMultipleField(
        # TODO implement enum restriction
        
        'genres', validators=[DataRequired()],
        choices=[
            (member.value, name.capitalize()) for name, member in Genres.__members__.items()
            
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone',validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        # i searched for enum restriction but i can not find any resource except that i use enum with 
        #constants of states   and use function to trace all member  to do function on  name or




        'genres', validators=[DataRequired()],
        
        choices=[
            (member.value, name.capitalize()) for name, member in Genres.__members__.items()
        ]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL(message='You Must Enter Valid URL')]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

class states(Enum):
    AL =  'AL'
    AK =  'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN'
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK ='OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'

class Artist_Form_new(Form):
    name =StringField('name',
    validators=[DataRequired(message='You must Enter Name'),Length(min=5,max=20)])
    image_link=StringField('image_link',
    validators=[DataRequired() ,URL(message='Enter Valid URL '),])
    facebook_link =StringField('facebook_link',
    validators=[DataRequired(message='You Must Enter FaceBook Link '),URL(message='Enter Valid Url ')])
    phone = StringField('phone', validators=[DataRequired(message='Enter phone Number')
    ,Length(min=10,max=14)])
    city=StringField('city',validators=[DataRequired(message='Enter City Name'),Length(min=5)])
    state = SelectField(
        'state',validators=[DataRequired(message='Select State')],
        choices=[  (member.value, name) for name, member in states.__members__.items()]
    )
    genres = SelectMultipleField('genres',
    validators=[DataRequired(message='Select Multiple Genres')],
    choices=[(member.value, name.capitalize()) for name, member in Genres.__members__.items()])

#new Form  for show   we can use
class  show_form_new(Form):
    start_time = DateTimeField('start_time',validators=[DataRequired()]
    ,default= datetime.today())
    artist_name = SelectField('artist_id',validators=[DataRequired()],
    choices=[(artist.name,artist.name) for artist in Artist.query.all()])
    venue_name = SelectField('venue_id',validators=[DataRequired()],
    choices=[(venue.name,venue.name) for venue in Venue.query.all()])
