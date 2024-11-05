import requests
from database import Database
from gridfs import GridFS


url = 'https://flibusta.is'
valid_chars = "-_.() {}[]!@#$%^&*()+=<>?"


folder = '/Volumes/DATA/flibusta'



page_numbers = []
first_page = 2
last_page = 1999



def download_book(book):
    book_url = f'{url}/b/{book.get("ID")}/mobi'
    try:
        response = requests.get(book_url)
     
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(f'{book.get("ID")} - {book.get("Title")}\t{e}\n')
        return
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename = content_disposition.split(';')[1].split('=')[1].strip('"')
    else:
        filename = f'{str(book.get("Title")).strip()[:20]}.mobi'
        filename = ''.join(c for c in filename if c.isalnum() or c in valid_chars)
    content = b''
    
    for chunk in response.iter_content(chunk_size=8192):
        content += chunk

     
    book['type'] = filename.split('.')[-1]
    book['downloaded'] = True
    del(book['content'])
    
    try:
        file_id =fs.put(content, filename=f'{book.get("ID")}.{book.get("type")}')
        book['file_id'] = file_id
        Database.replace(
                collection= 'books',
                query = {'_id': book.get('_id')},
                data = book,
                )
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(f'{book.get("ID")} - {book.get("Title")}\n')

def get_books(skip=0, limit=1000):
    try:
        data = Database.find('books',query={'downloaded': False})
    except Exception as e:
        print(f'{e}')
    for book in data:
        print(f'Downloading {book.get("Title")} with id {book.get("ID")}')
        db_data = [ b for b in Database.find('books',query={'ID': book.get('ID')})]
        if len(db_data) > 1:
            uploaded = True if len([b for b in db_data if b.get('downloaded')]) > 0 else False
            if uploaded:
                Database.delete('books',query={'downloaded': False, 'ID': book.get('ID')})
                continue
        else:
            book = db_data[0]
        if book.get('downloaded'):
            print(f'Already downloaded {book.get("Title")} with id {book.get("ID")}')
            continue
        '''if Database.find_one('big_size_books', query={'ID': book.get('ID')}) or Database.find_one('book_ids', query={'ID': book.get('ID')}):
            print(f'Big file {book.get("Title")} with id {book.get("ID")}')
            continue'''
        download_book(book)
    return data


if __name__ == '__main__':
    db = Database.initialize()
    fs = GridFS(Database.DATABASE)
    '''books = Database.find('books', query={'downloaded': True})
    for book in books:
        content = book.get('content')
        if content:
            file_id =fs.put(content, filename=f'{book.get("ID")}.{book.get("type")}')
            Database.update(
                collection= 'books',
                query = {'_id': book.get('_id')},
                data = {'$unset': {'content': ''}, '$set': {'file_id': file_id}},
                )
            print(f'Uploaded {book.get("Title")} with id {book.get("ID")}')'''
    books = get_books()