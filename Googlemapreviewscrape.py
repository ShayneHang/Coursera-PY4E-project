from selenium import webdriver #import webdriver to use
from selenium.webdriver.common.keys import Keys #give access to enter button, esc button, so that we can interactive more in the webpage
from selenium.webdriver.common.by import By #new syntax to search the webpage element by ID, class, etc
from selenium.webdriver.support.ui import WebDriverWait #to let the webpage load till certain element appear then execute next code
from selenium.webdriver.support import expected_conditions as EC #to let the webpage load till certain element appear then execute next code
import time #to set pauses inbetween action
import re
from bs4 import BeautifulSoup
import ssl


#ignore SSL certificate error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


### loading google map for review scraping ###

# set up path to webdriver
PATH = 'D:\Others\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# input website to go to
driver.get('https://www.google.com/maps')

# wait for searchbox element to load and clear its content
search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
search.clear()

# user to key in input on what to search
# name of the place must be exact, e.g. searching 'ion orchard' will return 2 results in google map and so will not work
# not suitable for searching hotel related places as their layout is different
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
time.sleep(2)

# identifying the area to scroll
toscroll = driver.find_element(By.XPATH,
    '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
                               )

# each scroll gives only 10 reviews, so 'total review'/10 gives the total number of scrolls
# to scroll out all reviews #default is 'range(0,(round(reviewinnum/10)))'
# if only updating new reviews to database, just run ~10 scrolls will be enough use 'range(0, 10)'
for i in range(0,3):
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
    # selecting the index 0 to extract it out not as list
    usersname = str(usersname[0].strip())
    usersnamex.append(usersname)

# extracting users' rating
listratings = gmapHTML.find_all('span', class_='kvMYJc')
for x in listratings:
    listratings = re.findall('" ([0-9])+\s.+ "', x.decode())
    listratings = int(listratings[0].strip())
    userrating.append(listratings)

# extracting user reviews
listreviews = gmapHTML.find_all('span', class_='wiI7pd')
for x in listreviews:
    listreviews = re.findall('(.+)', x.text)
    # some users wont have reviews hence to check and append as 'none' if none
    if len(listreviews) == 1:
        listreviews = str(listreviews[0].strip())
        userreview.append(listreviews)
    else:
        listreviews.append('None')
        listreviews = str(listreviews[0].strip())
        userreview.append(listreviews)

# extracting users' review timestamp
listreviewperiod = gmapHTML.find_all('span', class_="rsqaWe")
for x in listreviewperiod:
    listreviewperiod = re.findall('>(.+)<', x.decode())
    listreviewperiod = str(listreviewperiod[0].strip())
    reviewtimestamp.append(listreviewperiod)

# check whether all list length are equal
# if len not equal, risk of mismatching reviews to its rating
# this is vital as rating is used to label the sentiment of reviews

if len(usersnamex) == len(userrating) == len(userreview) == len(reviewtimestamp):
    print('list length are all equal')
else:
    print('list length not equal, please check')