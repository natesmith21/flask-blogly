from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):

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

    def get_full_name(self):

        full_name = f'{self.first_name} {self.last_name}'

        return full_name
    
class Post(db.Model):

    __tablename__= 'posts'

    id = db.Column(db.Integer, 
                primary_key=True,
                autoincrement=True
                )

    title = db.Column(db.String, 
                      nullable=False
                      )

    content = db.Column(db.String,
                         nullable=False
                         )
    
    created_at = db.Column(db.DateTime, 
                           nullable=False,
                           default =  datetime.today()
                            ) 
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='users')

    
    



