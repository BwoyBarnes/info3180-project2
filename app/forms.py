from models import *
from flask_wtf import FlaskForm
from wtforms import *

class CreateUserForm(FlaskForm):
    fName = StringField('First Name', [validators.Length(min=1, max=80)])

    lName = StringField('Last Name', [validators.Length(min=1, max=80)])
    userName = StringField('Username', [validators.Length(min=1, max=80)])
    
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.Length(max=70),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Repeat Password',[
        validators.DataRequired(),
        validators.Length(max=70),
        validators.EqualTo('password', message='Passwords must match')])
    
    imgfile = FileField('(Optional) Upload a Profile Picture')
    
    gender = SelectField('Gender', choices=[('none', '--select--'),('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')] )
    
    age = IntegerField('Age', validators=[validators.NumberRange(min=1, max=140)])
    bio = StringField('(Optional) Profile Bio', validators=[validators.Length(min=0, max=140)])

    FormSubmitted = False

    def validate_userName(form, field):
        user = UserProfile.query.filter_by(username=field.data).first()
        if user is not None: # Username already exist so we cannot proceed safely
            raise ValidationError('Username already exists.')
    
    def validate_gender(form, field):
        if field.data == "none":
            raise ValidationError('Please select a gender.')      

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])



