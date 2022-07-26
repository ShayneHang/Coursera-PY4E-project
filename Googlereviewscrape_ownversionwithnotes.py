from selenium import webdriver #import webdriver to use
from selenium.webdriver.common.keys import Keys #give access to enter button, esc button, so that we can interactive more in the webpage
from selenium.webdriver.common.by import By #new syntax to search the webpage element by ID, class, etc
from selenium.webdriver.support.ui import WebDriverWait #to let the webpage load till certain element appear then execute next code
from selenium.webdriver.support import expected_conditions as EC #to let the webpage load till certain element appear then execute next code
import time #to set pauses inbetween action
import re
from bs4 import BeautifulSoup
import ssl
import pandas as pd
import sqlite3
from datetime import date
import collections #to count number of most common words mentioned in review
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import openpyxl
from nltk.tokenize.treebank import TreebankWordDetokenizer


#ignore SSL certificate error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


################################################################################
### loading google map for review scraping ###
'''
Before executing, 
1) am i running for new review scrapping or update?
    if update - change the number of times to scrolls to 10 at line 94
    if new review scrap - change back to 'range(0,(round(reviewinnum/10)))'
'''


# set up path to webdriver
PATH = 'D:\Others\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# input website to go to
driver.get('https://www.google.com/maps')

'''
to find the element, right click the item i want on the webpage and inspect
then look for its relative path. dont use absolute path as it will not work after
website page owner updates or make changes
'''

# wait for searchbox element to load and clear its content
search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
search.clear()

# user to key in input on what to search
# name of the place must be exact, e.g. searching 'ion orchard' will return 2 results in google map and so will not work
userinput = input('Search (input as specific as possible):')
search.send_keys(userinput)
search.send_keys(Keys.RETURN) # return is enter, so to execute the search, like pressing enter


# find number of reviews, to calculate how many times to scroll
try:
    numreview = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,
                                "//button[@jsaction='pane.rating.moreReviews']")))
except:
    print('Error: If you see multiple results on google map, please restart and enter a more specific keyword')
reviewinnum = re.findall('(.+\s)', numreview.text)
reviewinnum = reviewinnum[0].strip()
reviewinnum = int(reviewinnum.replace(',',''))
print('total reviews:', reviewinnum)

# click the 'review' button
numreview.click()

# let the webpage load the reviews
time.sleep(2)

# click the 'sort review' button
sort = driver.find_element(By.XPATH, "//button[@aria-label='Sort reviews']") #<< uses the relative path
sort.click()

# let it load
time.sleep(1)

# sort review by newest
sortnewest = driver.find_element(By.XPATH, "//li[@data-index='1']")
sortnewest.click()

# let it load
time.sleep(1)

# identifying the area to scroll
toscroll = driver.find_element(By.XPATH,
    '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
                               )

# each scroll gives only 10 reviews, so 'total review'/10 gives the total number of scrolls
# to scroll out all reviews #default is 'range(0,(round(reviewinnum/10)))'
# if only updating new reviews to database, just run ~10 scrolls will be enough use 'range(0, 10)'
for i in range(0,(round(reviewinnum/10))):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                          toscroll
                          )
    time.sleep(1)

# expand all comments
count = 0
itemstoclick = driver.find_elements(By.XPATH, '//button[@aria-label=" See more "]')
for i in itemstoclick:
    i.click()
    count += 1
print('Expanded', count, 'comments')


################################################################################
### parsing the google reviews ###

# list to capture the reviews
usersnamex = []
usernumreview = []
userrating = []
userreview = []
reviewtimestamp = []

# parsing
# driver.page_source returns then current webpage to parse
gmapHTML = BeautifulSoup(driver.page_source, 'html.parser')

    # extracting users' name
    usersname = gmapHTML.find_all('div', class_="d4r55")
    for x in usersname:
        usersname = re.findall('.+', x.text)
        # convert to str to make sure its in correct format before inserting into SQL
        usersname = str(usersname[0].strip())
        usersnamex.append(usersname)

    # users' personal review count
    # reviewcount = gmapHTML.find_all('div', class_="RfnDt")
    # for x in reviewcount:
    #     reviewcount = re.findall('Local Guide(.+)', x.text)
    #     #some users have 0 review
    #     if len(reviewcount) == 1:
    #         reviewcount = reviewcount[0].replace('·', '').strip()
    #         usernumreview.append(reviewcount)
    #     else:
    #         reviewcount.append('None')
    #         usernumreview.append(reviewcount)
    # removing this because some google reviews dont have user's review count at all
    # and will mess up the table when inserting into SQL

    # users' rating
    listratings = gmapHTML.find_all('span', class_='kvMYJc')
    for x in listratings:
        listratings = re.findall('" ([0-9])+\s.+ "', x.decode())
        listratings = int(listratings[0].strip())
        userrating.append(listratings)

    # user reviews
    listreviews = gmapHTML.find_all('span', class_='wiI7pd')
    for x in listreviews:
        listreviews = re.findall('(.+)', x.text)
        # some users wont have reviews
        if len(listreviews) == 1:
            listreviews = str(listreviews[0].strip())
            userreview.append(listreviews)
        else:
            listreviews.append('None')
            listreviews = str(listreviews[0].strip()) #added this cause it will append as list to the list, which caused error when inserting into SQL
            userreview.append(listreviews)

    # users' review timestamp
    listreviewperiod = gmapHTML.find_all('span', class_="rsqaWe")
    for x in listreviewperiod:
        listreviewperiod = re.findall('>(.+)<', x.decode())
        listreviewperiod = str(listreviewperiod[0].strip())
        reviewtimestamp.append(listreviewperiod)

# check whether all list length are equal
if len(usersnamex) == len(userrating) == len(userreview) == len(reviewtimestamp):
    print('list length are all equal')
else:
    print('list length not equal, please check')

# for checking
# len(usersnamex)
# len(userrating)
# len(userreview)
# len(reviewtimestamp)
#len(usernumreview) ## usernumreview not in use already

################################################################################
# combining all reviews into one db
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\ichiban_boshi_main.sqlite')

cur = conn.cursor()

numofreview = len(userreview)
numofreview

for i in range(0, numofreview):
    a = usersnamex[i]
    #b = usernumreview[i]
    b = userrating[i]
    c = userreview[i]
    d = reviewtimestamp[i]

    cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)', (a,))
    cur.execute('SELECT id FROM Usernames WHERE name = ?', (a,))
    usernames_id = cur.fetchone()[0]

    cur.execute(
        'INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_rating, users_review, users_review_time_stamp, insert_date, outlet_name) VALUES (?,?,?,?,?,?)',
        (usernames_id, b, c, d, date.today(), userinput))

conn.commit()

cur.close()

driver.quit()




################################################################################
### if running initial pull of reviews, run below code
### if updating existing database with new reviews, run next batch of code

### set up SQL and insert into DB ###
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\ichiban_boshi_main.sqlite') # change name of sqlite file here

cur = conn.cursor()

# create the tables
cur.executescript(''' 
DROP TABLE IF EXISTS GoogleMapReviews;
DROP TABLE IF EXISTS Usernames;

CREATE TABLE Usernames(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
    );

CREATE TABLE GoogleMapReviews(
            usernames_id INTEGER, 
            users_review_count TEXT,
            users_rating INTEGER,
            users_review TEXT,
            users_review_time_stamp TEXT,
            insert_date TEXT,
            outlet_name TEXT
            );
''')

# inserting into SQL table
numofreview = len(userreview)
numofreview

for i in range(0, numofreview):
    a = usersnamex[i]
    #b = usernumreview[i]
    b = userrating[i]
    c = userreview[i]
    d = reviewtimestamp[i]

    cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)', (a,))
    cur.execute('SELECT id FROM Usernames WHERE name = ?', (a,))
    usernames_id = cur.fetchone()[0] #to retrieve the primary id for the users to insert into main review table

    cur.execute(
        'INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_rating, users_review, users_review_time_stamp, insert_date, outlet_name) VALUES (?,?,?,?,?,?)',
        (usernames_id, b, c, d, date.today(), userinput))

conn.commit()

cur.close()


# check
cur.execute('SELECT name, users_rating, users_review, users_review_time_stamp FROM Usernames JOIN GoogleMapReviews on Usernames.id = GoogleMapReviews.usernames_id')
df = cur.fetchall()
for i in df:
    print(i)



################################################################################
### if updating existing database with new reviews, run below code
''' 
to do before updating
1) search in the google map review for the the latest name in database from last extraction
2) if cannot find, then search for the 2nd latest name
because realised that some users may have deleted their review, if that's the case
my loop wont stop cause cannot find the exact name match
3) change the latest name to match per step 2 at line 263

note: updated new reviews and usernames will become last in the entries of the database 
instead of first. 
'''


### to update the SQL with new reviews ###
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\googlereviewx.sqlite')

cur = conn.cursor()

# retrieving the names from existing SQL list
cur.execute('SELECT name FROM Usernames')
latestname = cur.fetchall() # <<this returns the latest username entry from SQL
latestname = latestname[1] # retrieving it out of the list
latestname = latestname[0] # retrieving it out of the tuple

for i in range(0, numofreview):
    a = usersnamex[i]
    #b = usernumreview[i]
    b = userrating[i]
    c = userreview[i]
    d = reviewtimestamp[i]
    if a == latestname: #if found username similar to latest entry in  DB, break
        break
    else:
        cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)', (a,))
        cur.execute('SELECT id FROM Usernames WHERE name = ?', (a,))
        usernames_id = cur.fetchone()[0]

        cur.execute(
            'INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_rating, users_review, users_review_time_stamp, insert_date) VALUES (?,?,?,?,?)',
            (usernames_id, b, c, d, date.today()))

conn.commit()

cur.close()

driver.quit()


################################################################################
# combining all reviews into one db
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\ichiban_boshi_main.sqlite')

cur = conn.cursor()

numofreview = len(userreview)
numofreview

for i in range(0, numofreview):
    a = usersnamex[i]
    #b = usernumreview[i]
    b = userrating[i]
    c = userreview[i]
    d = reviewtimestamp[i]

    cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)', (a,))
    cur.execute('SELECT id FROM Usernames WHERE name = ?', (a,))
    usernames_id = cur.fetchone()[0]

    cur.execute(
        'INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_rating, users_review, users_review_time_stamp, insert_date) VALUES (?,?,?,?,?)',
        (usernames_id, b, c, d, date.today()))

conn.commit()

cur.close()

driver.quit()



################################################################################
### analysing the most common words ###
'''
choose the source of reviews from either database or re-pull the reviews into
list again.
'''

### if retrieving reviews from existing database, start code from here <<<<<
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\googlereviewx.sqlite')
cur = conn.cursor()
cur.execute('SELECT users_review FROM GoogleMapReviews')
dbreviews = cur.fetchall()
numofreview = len(dbreviews)

# removing the tuples from the db reviews and inserting into list
userreview = []
for i in range(0, numofreview):
    x = dbreviews[i]
    x = x[0]
    userreview.append(x)
print(userreview)


### if retrieving reviews from current list, start code from here <<<<<
len(userreview)
for i in userreview:
    print(i)

# combining all the reviews into 1 whole lump
userreviewcombined = '\n'.join(userreview)
# print(userreviewcombined)

# using nltk's library to identify out the stopwords
stop_words = nltk.corpus.stopwords.words('english')
stop_words.extend([',', '.', 'The', 'I', 'n', 's'])
# print(stop_words)
words = word_tokenize(userreviewcombined) # extracting out each word and insert into list


# list to capture the common words
commonword = []
for i in words:
    if i == 'None': # to remove my 'none' from above for those empty reviews
        continue
    if i not in stop_words:
        commonword.append(i)

# check
# print(commonword)

# combining all the common words into 1 chuck of text
commonword = ' '.join(commonword)
# print(commonword)

# pulling out the common words
commonword = re.findall('\w+', commonword)
commonword = collections.Counter(commonword).most_common(20)
print(commonword)



################################################################################
### reviews with stopword removed ###

# using nltk's library to identify out the stopwords
stop_words = nltk.corpus.stopwords.words('english')
stop_words.extend([',', '.', 'The', 'I', 'n', 's']) #instead of append, use extend to add multiple item to the list
print(stop_words)


removestopword = []

for i in userreview:
    tokenized = word_tokenize(i)
    # print(tokenized)
    remove = [x for x in tokenized if not x in stop_words]
    # print(remove)
    remove = TreebankWordDetokenizer().detokenize(remove)
    # print(remove)
    removestopword.append(remove)

len(removestopword)

for i in removestopword:
    print(i)

# to view the list as dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
reviewscraper = pd.DataFrame(
    {'Users name': usersnamex,
     'Users rating (out of 5)': userrating,
     'Users review': userreview,
     'stop words removed': removestopword,
     'Review date': reviewtimestamp,
    }
)
print(reviewscraper)

reviewscraper.to_csv(r'D:\User\Courses\PY4E coursera\project\googlereviewoutputstopword.csv')




















# what i can do now is do comparision of competitor's business and what is their most common words
# or pull twitter API to see the comments vs how the market moves according to general public sentiment
# thing to improve on the code will be using the wait out code below instead of setting time
# then gitpush my code to github already

# appendix for other codes not used

# to clear all the list if needed
usersnamex.clear()
usernumreview.clear()
userrating.clear()
userreview.clear()
reviewtimestamp.clear()

# to view the list as dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
reviewscraper = pd.DataFrame(
    {'Users name': usersnamex,
     #'Users review count': usernumreview,
     'Users rating (out of 5)': userrating,
     'Users review': userreview,
     'Review date': reviewtimestamp,
    }
)
print(reviewscraper)

# extract it out as excel
reviewscraper.to_csv(r'D:\User\Courses\PY4E coursera\project\googlereviewoutput.csv')


### this method works, but it cant loop through the rest of the reviews only get the first review only
# for i in range(0, reviewinnum):
#     username = gmapparse.username(gmapHTML)
#     reviewcount = gmapparse.reviewcount(gmapHTML)
#     userrating = gmapparse.userrating(gmapHTML)
#     reviews = gmapparse.reviews(gmapHTML)
#     reviewtime = gmapparse.reviewtime(gmapHTML)
#
#     cur.execute('INSERT OR IGNORE INTO Usernames (name) VALUES (?)',
#                 (username,))
#     cur.execute('SELECT id FROM Usernames WHERE name = ?', (username,))
#     usernames_id = cur.fetchone()[0]
#     cur.execute('INSERT OR IGNORE INTO GoogleMapReviews (usernames_id, users_review_count, users_rating, users_review, users_review_time_stamp) VALUES (?,?,?,?,?)',
#                 (usernames_id, reviewcount, userrating, reviews, reviewtime))
#
# conn.commit()
#
# cur.close()
################################################################################



# old method to find the comments, etc, which require specific input of the jstcache ID, except for rating
# for i in span: #differnet jstcache for different locations, e.g. century sq is 1400, ion orchard is 1519
#     name = re.findall('jstcache="1331">(.+)<', i.decode())
#     print(name)
#
# for i in span:
#     comment = re.findall('jstcache="1149">(.+)<', i.decode())
#     print(comment)
#
# for i in span:
#     rating = re.findall('<span aria-label="(.+) "', i.decode())
#     print(rating)
#
# for i in span:
#     period = re.findall('jstcache="1144">(.+)<', i.decode())
#     print(period)
#
# for i in span: #for this i cannot remove the . because some have . infront some dont have. and if i choose not to include the dot, then those which do have dot wont be found.
#     numofreviews = re.findall('jstcache="1334">(.+)<', i.decode())
#     print(numofreviews)




# try:
#     sort = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.LINK_TEXT, "Sort"))
#     )
#     sort.click()
# except:
#     driver.quit()



#time.sleep(5)

#driver.quit()

# driver.close() #close the current tab
# driver.quit() #close the entire browser
# print(driver.title) #return title of the webpage


### source for project ###
# https://towardsdatascience.com/scraping-google-maps-reviews-in-python-2b153c655fc2
# https://github.com/gaspa93/googlemaps-scraper
# https://medium.com/@isguzarsezgin/scraping-google-reviews-with-selenium-python-23135ffcc331
# https://stackoverflow.com/questions/70589658/change-google-maps-review-sort-with-selenium creating own XPATH locators