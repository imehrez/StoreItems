from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from resouces import Item, ItemList

import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

app = Flask(__name__)
app.secret_key = 'key'  # to authenticate and create token 
api = Api(app)

'''creates a new endpoint /auth
receives a dict {'username':'u', 'password':'p'} 
in the POST header request to /auth
returns a token'''
jwt = JWT(app, authenticate, identity)

'''Define the endpoints and if they
require a certain parameter
'''
api.add_resource(Item, '/item/<string:name>') # http://127.0.0.1:6060/item/ismail
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    # run app if this file is main
    app.run(port=config['PORTS']['flask'])