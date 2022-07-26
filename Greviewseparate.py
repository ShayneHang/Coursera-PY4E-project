import sqlite3
from datetime import date
import Googlemapreviewscrape

'''
Googlemapreviewscrape.py is the main code to open and scrape intended google reviews
Greviewseparate.py saves different google reviews into separate sqlite files
if save different google reviews into one file, use Greviewcombine.py 
'''

# saving different google reviews into separate files

# change name of sqlite file here every time you run a new separate google reviews
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\FGJBtest.sqlite')

cur = conn.cursor()

# create tables
cur.executescript('''
DROP TABLE IF EXISTS GoogleMapReviews;
DROP TABLE IF EXISTS Usernames;
DROP TABLE IF EXISTS Timestamp;

CREATE TABLE Usernames(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
    );

CREATE TABLE Timestamp(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    timestamp TEXT UNIQUE
    ); 

CREATE TABLE GoogleMapReviews(
            usernames_id INTEGER,
            users_rating INTEGER,
            users_review TEXT,
            timestamp_id INTEGER,
            insert_date TEXT,
            outlet_name TEXT
            );
''')

# inserting into SQL table
numofreview = len(Googlemapreviewscrape.userreview)

for i in range(0, numofreview):
    a = Googlemapreviewscrape.usersnamex[i]
    b = Googlemapreviewscrape.userrating[i]
    c = Googlemapreviewscrape.userreview[i]
    d = Googlemapreviewscrape.reviewtimestamp[i]

    # creating simple relational database
    # separate table keep track of user names
    cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)', (a,))
    cur.execute('SELECT id FROM Usernames WHERE name = ?', (a,))
    # then extracting user name's primary key for the main table as connection
    usernames_id = cur.fetchone()[0]

    # separate table keep track of timestamp
    cur.execute('INSERT OR IGNORE INTO Timestamp (timestamp) VALUES (?)', (d,))
    cur.execute('SELECT id FROM Timestamp WHERE timestamp = ?', (d,))
    # then extracting user name's primary key for the main table as connection
    timestamp_id = cur.fetchone()[0]

    cur.execute(
        'INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_rating, users_review, users_review_time_stamp, insert_date, outlet_name) VALUES (?,?,?,?,?,?)',
        (usernames_id, b, c, timestamp_id, date.today(), Googlemapreviewscrape.userinput))

conn.commit()

cur.close()

# close chrome
Googlemapreviewscrape.driver.quit()