#!python

import sys
from flask import Flask, jsonify, request
import json

from models import Base, Book

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://catalyst:catalyst@localhost:5432/books')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/books', methods = ['GET', 'POST'])
def books():
    if request.method == 'POST':
        attrs = { permitted: request.json[permitted] for permitted in ['title', 'author', 'genre'] }

        try:
            book = Book()
            book.__dict__.update(attrs)
            session.add(book)
            session.commit()
        except:
            e = sys.exc_info()[0]
            return jsonify({'error' : 'error creating record'})

        return jsonify(book.as_json())
    elif request.method == 'GET':
        books = session.query(Book).all()
        books_map = list(map(Book.as_json, books))
        return jsonify(books_map)

@app.route("/books/<int:book_id>", methods = ['GET', 'POST', 'DELETE'])
def book(book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        attrs = { permitted: request.json[permitted] for permitted in ['title', 'author', 'genre'] }

        try:
            session.query(Book).filter_by(id=book_id).update(attrs)
            session.commit()
        except:
            e = sys.exc_info()[0]
            return jsonify({'error' : 'error updating record'})

        return jsonify(book.as_json())
    elif request.method == 'DELETE':
        try:
            session.delete(bookToDelete)
            session.commit()
        except:
            e = sys.exc_info()[0]
            return jsonify({'error' : 'error deleting record'})

        return jsonify({'status' : 'ok' })

    elif request.method == 'GET':
        return jsonify(book.as_json())


if __name__ == '__main__':
    app.run(debug=True)
