from flask import Flask
from routes.view import view
from routes.auth import auth, jwt
from routes.api import api
from models import engine, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecretKey'
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

jwt.init_app(app=app)

app.register_blueprint(view, url_prefix='/')
app.register_blueprint(auth, url_prefix='/auth/')
app.register_blueprint(api, url_prefix='/api/')

if __name__ == "__main__":
    app.run(debug=True, port=5050)
    
    