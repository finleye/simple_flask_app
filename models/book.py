import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from .base import Base

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    genre = Column(String(250))

    def as_json(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'author' : self.author,
            'genre': self.genre
        }
