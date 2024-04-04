import sqlite3
from datetime import date
import Googlemapreviewscrape

'''
Googlemapreviewscrape.py is the main code to open and scrape intended google reviews
Greviewcombine.py will combine all the reviews into one sqlite file
if save the different google reviews into separate file, use Greviewseparate.py 
'''

# saving separate google reviews into one sqlite file

'''
connect to an already existing sqlite file with tables created - if not, 
uncomment the 'create table' code below (line 25 - 40) to create table in new sqlite file.
Then in next subsequent run, comment/delete away that batch of code if not
it will keep erasing away previous entries
'''

conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\ichibanboshicombined.sqlite')

cur = conn.cursor()

# create tables
# cur.executescript('''
# DROP TABLE IF EXISTS GoogleMapReviews;
# DROP TABLE IF EXISTS Usernames;
# DROP TABLE IF EXISTS Timestamp;
#
# CREATE TABLE Usernames(
#     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     name TEXT UNIQUE
#     );
#
# CREATE TABLE Timestamp(
#     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     timestamp TEXT UNIQUE
#     );
#
# CREATE TABLE GoogleMapReviews(
#             usernames_id INTEGER,
#             users_rating INTEGER,
#             users_review TEXT,
#             users_review_time_stamp TEXT,
#             insert_date TEXT,
#             outlet_name TEXT
#             );
# ''')

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
        (usernames_id, b, c, timestamp_id, date.today(),
         Googlemapreviewscrape.userinput))

# save to sqlite file
conn.commit()

cur.close()

# close chrome
Googlemapreviewscrape.driver.quit()









# ################################################################################
# ### analysing the most common words ###
# '''
# choose the source of reviews from either database or re-pull the reviews into
# list again.
# '''
#
# ### if retrieving reviews from existing database, start code from here <<<<<
# conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\googlereviewx.sqlite')
# cur = conn.cursor()
# cur.execute('SELECT users_review FROM GoogleMapReviews')
# dbreviews = cur.fetchall()
# numofreview = len(dbreviews)
#
# # removing the tuples from the db reviews and inserting into list
# userreview = []
# for i in range(0, numofreview):
#     x = dbreviews[i]
#     x = x[0]
#     userreview.append(x)
# print(userreview)
#
#
# ### if retrieving reviews from current list, start code from here <<<<<
# len(userreview)
# for i in userreview:
#     print(i)
#
# # combining all the reviews into 1 whole lump
# userreviewcombined = '\n'.join(userreview)
# # print(userreviewcombined)
#
# # using nltk's library to identify out the stopwords
# stop_words = nltk.corpus.stopwords.words('english')
# stop_words.extend([',', '.', 'The', 'I', 'n', 's'])
# # print(stop_words)
# words = word_tokenize(userreviewcombined) # extracting out each word and insert into list
#
#
# # list to capture the common words
# commonword = []
# for i in words:
#     if i == 'None': # to remove my 'none' from above for those empty reviews
#         continue
#     if i not in stop_words:
#         commonword.append(i)
#
# # check
# # print(commonword)
#
# # combining all the common words into 1 chuck of text
# commonword = ' '.join(commonword)
# # print(commonword)
#
# # pulling out the common words
# commonword = re.findall('\w+', commonword)
# commonword = collections.Counter(commonword).most_common(20)
# print(commonword)
#
#
#
# ################################################################################
# ### reviews with stopword removed ###
#
# # using nltk's library to identify out the stopwords
# stop_words = nltk.corpus.stopwords.words('english')
# stop_words.extend([',', '.', 'The', 'I', 'n', 's']) #instead of append, use extend to add multiple item to the list
# print(stop_words)
#
#
# removestopword = []
#
# for i in userreview:
#     tokenized = word_tokenize(i)
#     # print(tokenized)
#     remove = [x for x in tokenized if not x in stop_words]
#     # print(remove)
#     remove = TreebankWordDetokenizer().detokenize(remove)
#     # print(remove)
#     removestopword.append(remove)
#
# len(removestopword)
#
# for i in removestopword:
#     print(i)
#
# # to view the list as dataframe
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# reviewscraper = pd.DataFrame(
#     {'Users name': usersnamex,
#      'Users rating (out of 5)': userrating,
#      'Users review': userreview,
#      'stop words removed': removestopword,
#      'Review date': reviewtimestamp,
#     }
# )
# print(reviewscraper)
#
# reviewscraper.to_csv(r'D:\User\Courses\PY4E coursera\project\googlereviewoutputstopword.csv')
#

# # what i can do now is do comparision of competitor's business and what is their most common words
# # or pull twitter API to see the comments vs how the market moves according to general public sentiment
# # thing to improve on the code will be using the wait out code below instead of setting time
# # then gitpush my code to github already
#
# # appendix for other codes not used
#
# # to clear all the list if needed
# usersnamex.clear()
# usernumreview.clear()
# userrating.clear()
# userreview.clear()
# reviewtimestamp.clear()
#
# # to view the list as dataframe
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# reviewscraper = pd.DataFrame(
#     {'Users name': usersnamex,
#      #'Users review count': usernumreview,
#      'Users rating (out of 5)': userrating,
#      'Users review': userreview,
#      'Review date': reviewtimestamp,
#     }
# )
# print(reviewscraper)
#
# # extract it out as excel
# reviewscraper.to_csv(r'D:\User\Courses\PY4E coursera\project\googlereviewoutput.csv')
#
#
# ### this method works, but it cant loop through the rest of the reviews only get the first review only
# # for i in range(0, reviewinnum):
# #     username = gmapparse.username(gmapHTML)
# #     reviewcount = gmapparse.reviewcount(gmapHTML)
# #     userrating = gmapparse.userrating(gmapHTML)
# #     reviews = gmapparse.reviews(gmapHTML)
# #     reviewtime = gmapparse.reviewtime(gmapHTML)
# #
# #     cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)',
# #                 (username,))
# #     cur.execute('SELECT id FROM Usernames WHERE name = ?', (username,))
# #     usernames_id = cur.fetchone()[0]
# #     cur.execute('INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_review_count, users_rating, users_review, users_review_time_stamp) VALUES (?,?,?,?,?)',
# #                 (usernames_id, reviewcount, userrating, reviews, reviewtime))
# #
# # conn.commit()
# #
# # cur.close()
# ################################################################################
#
#
#
# # old method to find the comments, etc, which require specific input of the jstcache ID, except for rating
# # for i in span: #differnet jstcache for different locations, e.g. century sq is 1400, ion orchard is 1519
# #     name = re.findall('jstcache="1331">(.+)<', i.decode())
# #     print(name)
# #
# # for i in span:
# #     comment = re.findall('jstcache="1149">(.+)<', i.decode())
# #     print(comment)
# #
# # for i in span:
# #     rating = re.findall('<span aria-label="(.+) "', i.decode())
# #     print(rating)
# #
# # for i in span:
# #     period = re.findall('jstcache="1144">(.+)<', i.decode())
# #     print(period)
# #
# # for i in span: #for this i cannot remove the . because some have . infront some dont have. and if i choose not to include the dot, then those which do have dot wont be found.
# #     numofreviews = re.findall('jstcache="1334">(.+)<', i.decode())
# #     print(numofreviews)
#
#
#
#
# # try:
# #     sort = WebDriverWait(driver, 10).until(
# #         EC.presence_of_element_located((By.LINK_TEXT, "Sort"))
# #     )
# #     sort.click()
# # except:
# #     driver.quit()
#
#
#
# #time.sleep(5)
#
# #driver.quit()
#
# # driver.close() #close the current tab
# # driver.quit() #close the entire browser
# # print(driver.title) #return title of the webpage
#
#
# ### source for project ###
# # https://towardsdatascience.com/scraping-google-maps-reviews-in-python-2b153c655fc2
# # https://github.com/gaspa93/googlemaps-scraper
# # https://medium.com/@isguzarsezgin/scraping-google-reviews-with-selenium-python-23135ffcc331
# # https://stackoverflow.com/questions/70589658/change-google-maps-review-sort-with-selenium creating own XPATH locators