from flask import Blueprint, request, jsonify, make_response, redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from datetime import timedelta
from models import add_user, is_valid_user

auth = Blueprint('auth', __name__)
blocklist_token = set()
jwt = JWTManager()

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blocklist_token

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked. Please login again.'}), 401

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'massage':'All fields are required: email and password.'}), 400
    
    is_valid, user = is_valid_user(email, password)
    if not is_valid:
        return jsonify({'massage':'Pleace check email and password.'}), 401
    
    token = create_access_token(identity=str(user.get('id')), expires_delta=timedelta(hours=1))
    
    response = jsonify({'massage': 'Login Successfully', 'user':user})
    response.set_cookie('jwt_token', token)

    return response, 200

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_name = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not user_name or not email or not password: 
        return jsonify({'massage':'All fields are required: username, email, and password.'}), 400
    
    is_added, user = add_user(user_name,email,password)
    if not is_added: 
        return jsonify({'massage': 'User already exists.', 'user':user}), 200
    return jsonify({'massage': 'User successfully added.', 'user':user}), 200

@auth.route('/logout')
@jwt_required()
def logout():
    jwt = get_jwt()['jti']
    blocklist_token.add(jwt)
    response = jsonify({'massage':'Logout succesfully'})
    response.delete_cookie('jwt_token')
    return response, 200