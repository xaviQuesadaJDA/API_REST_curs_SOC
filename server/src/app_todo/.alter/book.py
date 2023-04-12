#!/usr/bin/python3

import json

class Book():

    """
    book.py conté la classe Book que és la classe principal de la nostra aplicació.
    """

    def __init__(self, title, author, genre, year, id=None):
        self._id = id
        self._title = title
        self._author = author
        self._genre = genre
        self._year = year


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._id = valor

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, valor):
        self._title = valor
    
    @property
    def author(self):
        return self._author
    
    @author.setter
    def author(self, valor):
        self._author = valor
    
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, valor):
        self._genre = valor
    
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, valor):
        self._year = valor

    def __str__(self    ):
        return json.dumps({
            "id": self._id,
            "title": self._title,
            "author": self._author,
            "genre": self._genre,
            "year": self._year
        })

# Noteu que la funció main queda fora de la definició de classe.
def main():
    un_llibre = Book("El problema dels 3 cossos", "Cixin Liu", "Ciència ficció", 2006)
    print(un_llibre)
    print(un_llibre.title)
    print(un_llibre.genre)

if __name__ == "__main__":
    main()
