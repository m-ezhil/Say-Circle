from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

view = Blueprint('view', __name__)

@view.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@view.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@view.route('/home', methods=['GET'])
def home():
    return render_template('home.html', is_login=True)