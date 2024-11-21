from mongoengine import Document, StringField, IntField, connect
import os
from models import Book


if os.getenv('MONGO_URI') is None:
    DBNAME = 'flibusta'
    DBUSER = 'mongoDBAdmin'
    DBPASS = 'kippUt-5vussy-gisvut'
    DBHOST = '192.168.1.30'
    DBPORT = 40100
    AUTH_SOURCE = 'admin'
    DATABASE_URI = f'mongodb://{DBUSER}:{DBPASS}@{DBHOST}:{DBPORT}'
else:
    DATABASE_URI = os.getenv('MONGO_URI')



connect(db=DBNAME, host=DBHOST, port=DBPORT, username=DBUSER, password=DBPASS, authentication_source=AUTH_SOURCE)
count = Book.objects.count()
print(f'Total books in database: {count}')
books = Book.objects(downloaded=True)
for book in books:
    content = book.file_id.read()
    print(f'{book.title} with id {book.book_id}')