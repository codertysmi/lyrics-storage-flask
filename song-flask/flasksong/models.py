from flasksong import db, login_manager
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def user_login(userId):
        return User.query.get(userId)

class User( db.Model , UserMixin ):
        __tablename__ = 'users'
        id = db.Column( db.Integer , primary_key = True )
        profile_pic = db.Column( db.String(64) , nullable = False , default = 'default_profile.png' )
        email = db.Column( db.String(64) , unique = True , index = True )
        username = db.Column( db.String(64) , unique = True , index = True )
        password = db.Column ( db.String(128) )
        posts = db.relationship ( 'BlogPost' , backref = 'author' , lazy = True )

        def __init__ ( self , email , username , password ):
                self.email = email
                self.username = username
                self.password = generate_password_hash ( password )
        def pass_check (self , password):
                return check_password_hash ( self.password , password )

        def __repr__(self):
                return f"user name is {self.username} and pass is {self.password}"


class BlogPost( db.Model ):

        users = db.relationship( User )

        id = db.Column ( db.Integer , primary_key = True )
        userId = db.Column ( db.Integer , db.ForeignKey('users.id') , nullable = False )
        date = db.Column ( db.DateTime , nullable = False , default = datetime.utcnow )

        title = db.Column ( db.String(128) , nullable = False )
        text = db.Column ( db.Text , nullable = False )

        def __init__(self , title , text , userId):
                self.title = title
                self.text = text
                self.userId = userId

        def __repr__(self):
                return f"blog title is {self.title} with id of {self.id}"

