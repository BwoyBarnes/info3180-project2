from . import db, bcryptHash
import datetime

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    password = db.Column(db.String(255))
    age = db.Column(db.Integer)
    bio = db.Column(db.String(140))
    gender = db.Column(db.String(10))
    image = db.Column(db.String(255))
    datecreated = db.Column(db.DateTime)

    def __init__(self, fName, lName, username, password, age, bio, gender, image):
        self.first_name = fName
        self.last_name = lName
        self.username = username
        self.password = bcryptHash.generate_password_hash(password) 
        self.age = age
        self.bio = bio
        self.gender = gender
        self.image = image
        self.datecreated = datetime.datetime.now()

        # # Creates password for db storage
        # pw_hash = bcrypt.generate_password_hash('hunter2')
        # bcryptHash.check_password_hash(pw_hash, 'hunter2') # returns True

        # # Check Password for login
        # candidate = 'secret'
        # bcrypt.check_password_hash(pw_hash, candidate)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class WishlistItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    url = db.Column(db.Text)
    thumbnail_url = db.Column(db.Text)

    def __init__(self, owner_id, title, description, url, thumbnail_url):
        self.owner_id = owner_id
        self.title = title
        self.description = description
        self.url = url
        self.thumbnail_url = thumbnail_url