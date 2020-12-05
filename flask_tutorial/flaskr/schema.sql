DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE Book (
    BookID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Author TEXT NOT NULL,
    AverageRating REAL,
    descp TEXT,
    PageNum INTEGER,
    PublicationYear TEXT
);

CREATE TABLE Author (
    Name TEXT PRIMARY KEY,
    workCount INTEGER
);

CREATE TABLE writtenBy (
    BookID INT NOT NULL,
    Name TEXT NOT NULL,
    PRIMARY KEY(BookID, Name),
    FOREIGN KEY(BookID) REFERENCES Book(BookID),
    FOREIGN KEY(Name) REFERENCES Author(Name)
)

CREATE TABLE readBy (
    BookID INT,
    username VARCHAR(100)
    FOREIGN KEY(BookID) REFERENCES Book(BookID), 
    FOREIGN KEY (username) REFERENCES user(username)
)

