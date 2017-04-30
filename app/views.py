"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from forms import *
from models import *
from bs4 import BeautifulSoup
from image_getter import get_images
import random, os, datetime, requests, urlparse

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

###----------------------------------- START OF SPECIFIED API ROUTES ---------------------------------------------###
@app.route('/api/users/register', methods=["GET", "POST"])
def register():
    """Accepts user information and saves it to the database."""
    form = CreateUserForm()
    if request.method == "POST":
        form.FormSubmitted = True
        
        if form.validate_on_submit():            
            if validFileExtension(request.files['imgfile'].filename):
                file_folder = app.config['UPLOAD_FOLDER']

                # Assigns 1 of 7 default profile pics if the user has not uploaded one
                if request.files['imgfile'].filename != "":
                    file = request.files['imgfile']
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(file_folder, filename))
                else:
                    filename = randomDefaultProfilePic()
                
                # Assigns the default bio if the user has not uploaded one
                if form.bio.data == "":
                    form.bio.data = app.config['DEFAULT_BIO']

                NewProfile = UserProfile(form.fName.data, form.lName.data, form.userName.data, 
                                         form.password.data, form.age.data, form.bio.data,
                                         form.gender.data, filename)

                db.session.add(NewProfile)
                db.session.commit()

                flash('Profile created and successfully saved', 'success')
                login_user(NewProfile)
                return redirect(url_for('profile'))
        
            else:
                form.imgfile.errors.append("Invalid image file uploaded")

    return render_template('register.html',form=form)


@app.route('/api/users/login', methods=["GET", "POST"])
def login():
    """Accepts login credentials as email and password"""
    # If the user is already logged in then it will just return them to the 
    # home page instead of logging them in again
    if (current_user.is_authenticated):
        return redirect(url_for('home'))
    
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data
            
            user = UserProfile.query.filter_by(username=username).first()
            
            # Fails if username doesn't exist 
            if user is not None: 
                # Compares Bcrypt hash to see if password is correct
                if (bcryptHash.check_password_hash(user.password, password)):
                    login_user(user)
                    flash('Logged in successfully.', 'success')
                    next = request.args.get('next')
                    return redirect(url_for('home'))
            
            flash('Username or Password is incorrect.', 'danger')                
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

@app.route('/api/users/<userid>/wishlist', methods=["POST"])
def addItem(userid):
    """Used for adding items to the wishlist"""
    if request.is_json:
        data = request.get_json(force=True)
        
        NewItem = WishlistItems(userid, data["title"], data["description"], data["url"], data["thumbnail_url"])
                                
        db.session.add(NewItem)
        db.session.commit()

        result = {"error": "null",
                  "data": {
                      "item":{
                          "id": NewItem.id,
                          "title": NewItem.title,
                          "description": NewItem.description,
                          "url": NewItem.url,
                          "thumbnail_url": NewItem.thumbnail_url,
                      }
                  }, 
                  "message":"Success"}
        flash('Wishlist item added successfully', 'success')
        print "Success"
    else:
        result = {"error": "true", "data": {}, "message": "Unable add item"}
        print "failed"
    print "returning"
    return jsonify(result)


@app.route('/api/users/<userid>/wishlist', methods=["GET"])
@login_required
def userWishlistPage(userid):
    """Returns JSON data for a user's wishlist"""

    Wishlist = {"error": "null","data": {"items":[]},"message":"Success"}

    temp = WishlistItems.query.filter_by(owner_id=userid).all()

    for x in temp:
        Wishlist["data"]["items"].append({ "id": x.id,
                                        "title": x.title,
                                        "description": x.description,
                                        "url": x.url,
                                        "thumbnail_url": x.thumbnail_url, })
    
    return jsonify(Wishlist)


@app.route('/api/thumbnails', methods=["GET", "POST"])
def scrapeImages():
    """Accepts a url and returns JSON containing a list of thumbnails."""
    if request.is_json:
        Webpage = request.get_json(force=True)
        print Webpage["url"]
        images = {"error": "null", "message":"Success","thumbnails": get_images(Webpage["url"])}
        print "success"
    else:
        images = {"error": "true", "data": {}, "message": "Unable to extract thumbnails"}
        print "failed"
    print "returning"
    return jsonify(images)


@app.route('/api/users/<userid>/wishlist/<itemid>', methods=["DELETE"])
@login_required
def deleteItem(userid,itemid):
    """Deletes an item from a users' wishlist"""
    
    Item = request.get_json(force=True)
    DeleteItem = WishlistItems.query.filter_by(id=Item["itemid"]).first()

    db.session.delete(DeleteItem)
    db.session.commit()
    
    flash('Wishlist item removed successfully', 'success')
    return jsonify({ "errors": "null", "data": {},"message": "Success"})

###----------------------------------- END OF SPECIFIED API ROUTES ---------------------------------------------###


@app.route('/wishlist')
@login_required
def viewWishlistRedirect():
    """Redirects header link to proper page format to access the ViewWishlist API.
    This is used for the static links in the header to point the user 
    to the correct page to access the services of the system."""
    page = '/' + current_user.get_id() +  url_for('viewWishlistRedirect')
    return redirect(page)


@app.route('/add-wishlist')
@login_required
def wishlistRedirect():
    """Redirects header link to proper page format to access the addWishlist API.
    This is used for the static links in the header to point the user 
    to the correct page to access the services of the system."""
    page = '/' + current_user.get_id() +  url_for('wishlistRedirect')
    return redirect(page)

@app.route('/profile', methods=["GET"])
@login_required
def profile():
    """Render the users's profile page."""
    user = UserProfile.query.filter_by(id=current_user.get_id()).first_or_404()
    return render_template('profile.html', profile=user)

@app.route('/<userid>/add-wishlist')
@login_required
def addWishlistPage(userid):
    """Renders the add wishlist page"""
    return render_template('addWishlist.html')


@app.route('/<userid>/wishlist')
@login_required
def viewWishlist(userid):
    """Renders the view wishlist page"""
    return render_template('viewWishlist.html')

###
# The functions below should be applicable to all Flask apps.
###

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%d %b %Y'):
    return value.strftime(format)

def validFileExtension(filename):
    """Used during registration to test if the file being uploaded is one of the allowed formats. The formats
       allowed are 'jpg', 'jpeg' and 'png' """
    if filename == "":
        return True

    if len(filename) > 3:
        fileExt = filename[-3:]
        if (fileExt != 'jpg' and fileExt != 'peg' and fileExt != 'png'):
            return False
        return True
    return False

def randomDefaultProfilePic():
    return "default/default-" + str(random.randint(1, 7)) + ".jpg"


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to tell the browser not to cache the rendered page.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
