
import pymongo



class Database(object):
    #URI = 'mongodb://mongoDBAdmin:kippUt-5vussy-gisvut@development.itcteh.com:40100/'
    URI = 'mongodb://mongoDBAdmin:kippUt-5vussy-gisvut@192.168.1.30:40100/'
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
    def update(collection, query, data):
        try:
            return Database.DATABASE[collection].replace_one(query, data, upsert=True)
        except Exception as e:
            with open('not_saved_to_db.txt', 'a') as f:
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


