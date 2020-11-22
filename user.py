import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        
        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='this is required')
    parser.add_argument('password', type=str, required=True, help='this is required')
      

    def post(self):
        #Parse data using the defined parser
        data = UserRegister.parser.parse_args()

        #check if user already present
        if User.find_by_username(data['username']):
            return {'message':'user already registerd!'}

        #open database
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # make query to add user
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        # commit and close database
        connection.commit()
        connection.close()

        return {"message": "User created successfuly"}, 201