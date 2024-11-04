import requests
import os
from pyquery import PyQuery as pq

from database import Database

RATING = {
    'файл не оценен': 0,
    'файл на 1': 1,
    'файл на 2': 2,
    'файл на 3': 3,
    'файл на 4': 4,
    'файл на 5': 5
}



def get_books(skip=0, limit=1000):
    try:
        data = Database.find('books',query={})
    except Exception as e:
        print(f'{e}')
    return data


def get_search_result(book_name, sort):
    payload = {'ab': 'ab1', 't': book_name, 'sort': sort}
    try:
        r = requests.get('http://flibusta.is/makebooklist', params=payload)
    except requests.exceptions.ConnectionError:
        print('Не можах да се свържа с flibusta.is')
        return None
    

    if r.text == 'Не нашлось ни единой книги, удовлетворяющей вашим требованиям.':
        print(f'Не нашлось ни единой книги по запросу {book_name}')
        return 'No result'
    else:
        return r.text


def fetch_book_id(search_result, sort):
    doc = pq(search_result)
    if sort == 'litres':
        book_id = [pq(i)('div > a').attr.href for i in doc.find('div') if '[litres]' in pq(i).text().lower()][0]
    elif sort == 'rating':
        books = [(pq(i)('div > a').attr.href, pq(i)('img').attr.title) for i in doc.find('div')]
        # print(books)
        # pass
        book_id = sorted(books, key=lambda book: RATING[book[1]], reverse=True)[0][0]
        # book = sorted(books, key=lambda book: RATING[book[1], reverse=True)[0][0]
    else:
        book_id = doc('div > a').attr.href
    return book

if __name__ == '__main__':
    db = Database.initialize()
    books = get_books()
    for book in books:
       book_file = requests.get(f'http://flibusta.is/b/{book.get("ID")}/mobi')
       with open(f"{book['Title']}.mobi", 'wb') as f:
        f.write(book_file.content)
       print(book)