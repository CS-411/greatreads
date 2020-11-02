DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE Book (
    BookID INTEGER PRIMARY KEY,
    Title TEXT,
    Author TEXT,
    AverageRating REAL,
    descp TEXT,
    PageNum INTEGER,
    PublicationYear TEXT
);

CREATE TABLE Author (
    Name TEXT PRIMARY KEY,
    workCount INTEGER
);

