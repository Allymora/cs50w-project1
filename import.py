import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql://umozvxqmncpnfb:560c3a8415c5a26fe6237f95deab2825dcb36d43e3cafd376fd9b4d866e6a0e3@ec2-54-91-223-99.compute-1.amazonaws.com:5432/d4ct3t7ojueffn")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                   {"isbn": isbn, "title": title, "author": author, "year": year})
        db.commit()

if __name__ == "__main__":
    main()
