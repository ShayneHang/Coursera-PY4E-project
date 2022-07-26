from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import ssl


# ignore SSL certificate error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# opening webpage and scroll all the way to end, if not beautifulsoup cannot retrieve everything
PATH = 'D:\Others\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get('https://order.ichibanboshi.com.sg/en_SG')

# this is generic scroll to the btm syntax
for i in range(0,15): #manually check is need around 15 scrolls to reach the btm
    driver.execute_script('window.scrollBy(0,document.body.scrollHeight)',"")
    time.sleep(1)

# using beautifulsoup to retrieve the menu items
menuHTML = BeautifulSoup(driver.page_source, 'html.parser')

menuitem = menuHTML.find_all('h3',
class_= 'sc-1acu81b-0 sc-14ntqp3-0 sc-14ntqp3-1 sc-14ntqp3-4 sc-1chvpk5-2 fdPWCs')

menuitemslist = []
wordstoremove = ['(NEW)', '(5pcs)', '(6pcs)']

for i in menuitem:
    items = re.findall('.+', i.text)
    for y in items:
        splitword = y.split()  # indicate nothing means split by spacings
        newword = [x for x in splitword if x not in wordstoremove] # remove those useless words
        newword = ' '.join(newword)
        menuitemslist.append(newword.lower())

# check
len(menuitemslist)
for i in menuitemslist:
    print(i)

# splitting the items into respective category
# used excel to identify the item indexes

appetizer = [] # 15-23
salad = [] # 24-27
sashimi = [] # 28-34
nigiri = [] # 35-57
gunkan = [] # 58-73
makimono = [] # 74-83
aLaCarte = [] # 84-100
donburi = [] # 101-106
jyu = [] # 107-109
udonSoba = [] # 110-116
handroll = [] # 117-125
assortedSushi = [] # 126-135

for i in range(15, 24):
    item = menuitemslist[i]
    appetizer.append(item)

for i in range(24, 28):
    item = menuitemslist[i]
    salad.append(item)

for i in range(28, 35):
    item = menuitemslist[i]
    sashimi.append(item)

for i in range(35, 58):
    item = menuitemslist[i]
    nigiri.append(item)

for i in range(58, 74):
    item = menuitemslist[i]
    gunkan.append(item)

for i in range(74, 84):
    item = menuitemslist[i]
    makimono.append(item)

for i in range(84, 101):
    item = menuitemslist[i]
    aLaCarte.append(item)

for i in range(101, 107):
    item = menuitemslist[i]
    donburi.append(item)

for i in range(107, 110):
    item = menuitemslist[i]
    jyu.append(item)

for i in range(110, 117):
    item = menuitemslist[i]
    udonSoba.append(item)

for i in range(117, 126):
    item = menuitemslist[i]
    handroll.append(item)

for i in range(126, 136):
    item = menuitemslist[i]
    assortedSushi.append(item)

# check
for i in appetizer:
    print(i)
for i in salad:
    print(i)
for i in sashimi:
    print(i)
for i in nigiri:
    print(i)
for i in gunkan:
    print(i)
for i in makimono:
    print(i)
for i in aLaCarte:
    print(i)
for i in donburi:
    print(i)
for i in jyu:
    print(i)
for i in udonSoba:
    print(i)
for i in handroll:
    print(i)
for i in assortedSushi:
    print(i)



