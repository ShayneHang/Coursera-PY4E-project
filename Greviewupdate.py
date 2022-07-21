import sqlite3
from datetime import date
import Googlemapreviewscrape

'''
Googlemapreviewscrape.py is the main code to open and scrape intended google reviews
Greviewupdate.py update your existing sqlite files
'''

# updating existing database with new reviews

'''
to do before updating
1) search the latest name from database in the google map review sorted by newest
2) if unable to find, search for the 2nd latest name from database (as some users may have deleted their review)
3) change the latest name to match per step 2 at line 32
(because the code is using user name as identifier to stop updating till the latest review previously pulled)
4) change the number of times to scrolls to as much as needed at line 94 of Googlemapreviewscrape.py

note: updated new reviews and usernames will become last in the entries of the database
'''

# to update the SQL file with new reviews
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\FGJBtest.sqlite')

cur = conn.cursor()

# retrieving the names from existing SQL list
cur.execute('SELECT name FROM Usernames')
latestname = cur.fetchall() # this returns the latest username entry from SQL
latestname = latestname[0] # retrieving it out of the list, change to 1 for next latest name and so on
latestname = latestname[0] # retrieving it out of the tuple
print("make sure user:'", latestname, "' is in Google map & matches the last pull review in database")

numofreview = len(Googlemapreviewscrape.userreview)

for i in range(0, numofreview):
    a = Googlemapreviewscrape.usersnamex[i]
    b = Googlemapreviewscrape.userrating[i]
    c = Googlemapreviewscrape.userreview[i]
    d = Googlemapreviewscrape.reviewtimestamp[i]
    if a == latestname: #if found username similar to latest entry in  database, break
        break
    else:
        cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)', (a,))
        cur.execute('SELECT id FROM Usernames WHERE name = ?', (a,))
        usernames_id = cur.fetchone()[0]

        # separate table keep track of timestamp
        cur.execute('INSERT OR IGNORE INTO Timestamp (timestamp) VALUES (?)', (d,))
        cur.execute('SELECT id FROM Timestamp WHERE timestamp = ?', (d,))
        # then extracting user name's primary key for the main table as connection
        timestamp_id = cur.fetchone()[0]

        cur.execute(
            'INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_rating, users_review, timestamp_id, insert_date, outlet_name) VALUES (?,?,?,?,?,?)',
            (usernames_id, b, c, timestamp_id, date.today(), Googlemapreviewscrape.userinput))


conn.commit()

cur.close()

# close chrome
Googlemapreviewscrape.driver.quit()