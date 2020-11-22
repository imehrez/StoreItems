import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

'''
Error codes
200: ok
201: created
202: delayed
400: bad request (already exists)
404: not found
500: internal server error
'''
class Item(Resource):
    # used to get the required argument only and neglect the rest
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='this is required')
    
    @classmethod
    def find_by_name(cls, name):
        '''
        looks for an entry with name in DB
        retuns tuple of row if found, otherwise returns NULL
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        #Retrieve data from database
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone() # tuple
        
        connection.close()
        return row
    
    @classmethod
    def update_item(cls, item):
        '''
        Update item {dict} into DB
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        #Update entry in table items
        entry = (item['price'], item['name'], )
        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, entry)
        connection.commit()
        connection.close()

    @classmethod
    def insert_item(cls, item):
        '''
        Insert item {dict} into DB
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        #Insert entry into table items
        entry = (item['name'], item['price'])
        insert_query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(insert_query, entry)
        connection.commit()
        connection.close()
    
    # in GET header we send 'authentication' 'JWT <token>' 
    # in headerwhich is decoded by JWT and authenticated using
    # the identity method
    @jwt_required()
    def get(self, name):
        row = Item.find_by_name(name)
        if row:
            return {'item': {'name': row[1], 'price': row[2]}}
        else:
            return {'message':'item not found'}, 404

    @jwt_required()
    def post(self, name):
        #look if item already exists
        row = Item.find_by_name(name)
        if row:
            return {'Message': f'item with name {name} already exists'}, 400
        
        request_data = Item.parser.parse_args()
        item = {'name':name, 'price':request_data['price']}

        try:
            Item.insert_item(item)
        except:
            return {'message': 'Error occured inserting into DB'}, 500

        return item, 201


    @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()

        row = Item.find_by_name(name)
        new_item = {'name':name, 'price':request_data['price']}

        if row is None:
            Item.insert_item(new_item)
        else:
            Item.update_item(new_item)
        
        return new_item, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        #Delete entry from table items
        delete_query = "DELETE FROM items where name=?"
        cursor.execute(delete_query, (name,))

        connection.commit()
        connection.close()

        return {'message', 'item deleted'}

class ItemList(Resource):
    @jwt_required()
    def get(self):
 
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
 
        #Get entries from table items
        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
       
        for row in result:
            items.append({'name':row[1], 'price':row[2]})

        connection.close()

        return {'items':items}