from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class Users(db.Model):

    __tablename__= 'users'

    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True
                   )
    
    first_name = db.Column(db.String,
                           nullable=False,
                           )
    
    last_name = db.Column(db.String)

    image_url = db.Column(db.String)

