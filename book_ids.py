from database import Database


def create_book_ids():
    Database.initialize()
    books = Database.find('books', query={})
    count = 0
    for book in books:
        count += 1
        book_id = Database.find_one('book_ids', query={'ID': book.get('ID')})
        if not book_id:
            Database.insert('book_ids', {'ID': book.get('ID')})
            print(count)

def add_title():
    books = Database.find('books_ids', query={})
    for book in books:
        if book.get('Title') == '':
            db_book = Database.find_one('book', query={'ID': book.get('ID')})


def not_uploaded():
    lines = []
    with open('not_uploaded.txt', 'r') as f:
        for line in f:
            lines.append(line)
    id_not_uploaded = [l.split('-')[0].strip() for l in lines]
    
    id_not_uploaded = list(set(id_not_uploaded))
    Database.initialize()
    for id in id_not_uploaded:
        Database.insert('big_size_books', {'ID': id})
        print(id)


def wrong_names():
    lines = []
    with open('wrong_names.txt', 'r') as f:
        for line in f:
            lines.append(line)
    


#create_book_ids()
not_uploaded()