
import pymongo
import os



class Database(object):
    if os.getenv('MONGO_URI') is None:
        DBNAME = 'flibusta'
        DBUSER = 'mongoDBAdmin'
        DBPASS = 'kippUt-5vussy-gisvut'
        DBHOST = '192.168.1.30'
        DBPORT = 40100
        AUTH_SOURCE = 'admin'
        URI = f'mongodb://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}'
    else:
        URI = os.getenv('MONGO_URI')
        DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['flibusta']

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert_one(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def replace(collection, query, data):
        try:
            return Database.DATABASE[collection].replace_one(query, data, upsert=True)
        except Exception as e:
            with open('not_saved_to_db.txt', 'a') as f:
                    f.write(f'{data["ID"]} - {data['Title']}\n')


    @staticmethod
    def update(collection, query, data):
        try:
            return Database.DATABASE[collection].update_one(query, data)
        except Exception as e:
            with open('not_updated_to_db.txt', 'a') as f:
                    f.write(f'{data["ID"]} - {data['Title']}\n')

    @staticmethod
    def remove(collection, query):
        try:
            Database.DATABASE[collection].delete_one(query)
            return True
        except Exception as e:
            return False


    @staticmethod
    def delete(collection, query):
        try:
            Database.DATABASE[collection].delete_many(query)
            return True
        except Exception as e:
            return False


