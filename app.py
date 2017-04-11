"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://vgglnyhq:-ywirI4EKPm6h7VPVjHxkRevD1mkUNlH@stampy.db.elephantsql.com:5432/vgglnyhq'
db = SQLAlchemy(app)

class ContosoUser(db.Model):
    lr_id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.LargeBinary)
    facebook_id = db.Column(db.Integer)
    facebook_user = db.relationship('FacebookUser', backref=db.backref('Contoso_User'))
    email = db.Column(db.String(400), unique=True)
    password = db.Column(db.String(60), nullable=False)
    registration_time = db.Column(db.DateTime)
    email_confirmation_token = db.Column(db.String(100))
    password_reminder_token = db.Column(db.String(100))
    status = db.Column(db.Integer)

    def __init__(self, email, password, timestamp):
        self.email = email
        self.password = password
        self.registration_time = timestamp

    def __repr__(self):
        return '<ContosoUser %r>' % self.email

    @property
    def serialize_email(self):
        return {
            'email': self.email
        }

    @property
    def serialize(self):
        return {
            'id': self.lr_id,
            'profile_picture': self.profile_picture,
            'facebook_id': self.facebook_id,
            'email': self.email,
            'password': self.password,
            'registration_time': self.registration_time,
            'email_confirmation_token': self.email_confirmation_token,
            'password_reminder_token': self.password_reminder_token,
            'status': self.status
        }



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

@app.route('/api')
@app.route('/api/')
def api_index():
    return 'Welcome to Contoso api' + str(datetime.datetime.utcnow())


@app.route('/api/v0')
@app.route('/api/v0/')
def api_index_v0():
    return 'Welcome to Contoso api V0' + str(datetime.datetime.utcnow())


###
# The functions below should be applicable to all Flask apps.
###

# This should never exist outside of development environment
@app.route('/api/v0/drop_and_create/mojqjkTzadQJIJXXDllEpJqdDBE3nS54ommirvUWEviHL20ZByR6MsWSrBMjk47')
def get_drop_all():
    db.drop_all()
    db.create_all()
    populate_contoso_user_table()
    return jsonify({'status': 'success'}), 200

def populate_contoso_user_table():
    db.session.add(create_one_user())
    if check_password():
        db.session.commit()
    else:
        db.session.remove()

def create_one_user():
    email = 'hikingfan@gmail.com'
    password = 'hunter2'
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
    user = ContosoUser(email, password_hash, datetime.datetime.utcnow())
    return user

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
