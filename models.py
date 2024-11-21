from mongoengine import Document, IntField, BooleanField, StringField, FileField

class Book(Document):
    meta = {'collection': 'books'}
    title: str = StringField(required=True)
    subtitle: str = StringField(required=True)
    language: str = StringField(required=True)
    book_id: int = IntField(required=True)
    type: str = StringField(required=True)
    year: str = StringField(default='')
    series: str = StringField(default='')
    downloaded: bool = BooleanField(required=True)
    genre: str = StringField(default='')
    name: str = StringField(default='')
    surname: str = StringField(default='')
    family: str = StringField(default='')
    skipped: bool = BooleanField(default=None)
    file_id: str = FileField(default=None)