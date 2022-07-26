import sqlite3
import re
import collections
import pandas as pd

'''
analysing reviews by using list of keywords and categorising the reviews into
groups.
'''

################################################################################
# creating function to check whether element in one list is in another list
# return will immediately break out of the loop in the first iteration,
# so 'else: continue' for it to finish looping through the whole list

def check_list(wordlist, review):

    #iterate the first list
    for x in wordlist:
        if x in review:
            return True
        else:
            continue


## creating list of keywords to categorise reviews into respective qualities
service_word = ['complain', 'service', 'staff', 'crew', 'attitude', 'experience', 'friend',
                'help', 'wait', 'understand', 'personal', 'quick', 'fast', 'slow',
                ]

food_word = ['food', 'drink', 'sushi', 'nigiri', 'sashimi', 'maki', 'dessert',
             'gunkan', 'katsu', 'karaage', 'soup', 'cutlet', 'ramen', 'soba',
             'bento', 'tempura', 'handroll', 'miso', 'taste', 'delicious', 'yummy',
             'fresh', 'ingredient', 'tea', 'awful', 'appetizer', 'salad', 'makimono',
             'donburi']

place_word = ['place', 'area', 'wall', 'ceiling', 'window', 'door', 'plate', 'bowl',
              'utensil', 'spoon', 'fork', 'chopstick', 'seat', 'table', 'ambience',
              'atmosphere', 'light', 'clean', 'comfort', 'oil', 'dirt', 'disgust',
              'insect', 'rodent', 'bug', 'cockroach', 'rat', 'fly', 'flies', 'soil',
              'sanitize', 'sanitise', 'floor', 'top', 'dust', 'cozy']

price_word = ['price', 'pricing', 'cheap', 'expensive', 'worth', 'budget', 'value',
              'money', 'afford']


# list of food words extracted from ichiban's menu
commonfoodword = ['mala', 'edamame', 'karaage', 'tofu', 'gyoza', 'chawanmushi',
                  'salad', 'amaebi', 'salmon', 'belly', 'hamachi', 'tako', 'scallop',
                  'tuna', 'hotate', 'kajiki', 'beef', 'tamago', 'inari', 'karibu',
                  'unagi', 'ebi', 'submarine', 'akami', 'cheese', 'ika', 'mayo',
                  'ebiko', 'lobster', 'tobiko', 'ikura', 'egg', 'chuka', 'octopus',
                  'wakame', 'roll', 'teriyaki', 'saba', 'shogayaki', 'katsu', 'tempura',
                  'steak', 'yaki', 'curry', 'kastu', 'don', 'jyu', 'chasoba', 'soba',
                  'udon', 'handroll', 'mentai', 'dragon']

# removing stop words - extracted from nltk stopword library, and did some adjustment to suit the project

stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
              "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself',
              'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her',
              'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them',
              'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom',
              'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
              'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
              'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or',
              'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with',
              'about', 'against', 'between', 'into', 'through', 'during', 'before',
              'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
              'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once',
              'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
              'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
              'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'can',
              'will', 'just', "don't", "don’t",'should', "should've", 'now', 'ain', 'aren',
              "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't",
              'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
              'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
              'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", "won't",
              'wouldn', "wouldn't", 'get', 'also', 'translated', "it’s", "there's",
              "that's", "he's", "her's", "there’s", "that’s", "let's", "let’s", "here's",
              "here’s"]

# check for duplicate among the different word lists
print('checking for duplicate words among different word list, if True to any below, please check')
print('service & food:', check_list(service_word, food_word))
print('service & place:', check_list(service_word, place_word))
print('service & price:', check_list(service_word, price_word))
print('food & place:', check_list(food_word, place_word))
print('food & price:', check_list(food_word, price_word))
print('place & price:', check_list(place_word, price_word))


################################################################################

# extracting reviews from database for analysing
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\ichiban boshi reviews 13.7.2022 2.40pm\ichibanboshicombined25.7.2022.sqlite')
cur = conn.cursor()
cur.execute('''
SELECT users_review, users_rating, outlet_name FROM GoogleMapReviews WHERE (users_review != 'None')
''')
dbreviews = cur.fetchall()
numofreview = len(dbreviews) # 2060

# list to segregate the reviews into
service_review = []
food_review = []
place_review = []
price_review = []

# loop to check if review contain keyword,
# extract only the ratings of the review, then categories it accordingly

for i in range(0, numofreview):
    x = dbreviews[i]
    review = x[0].lower()
    if check_list(service_word, review):
        servicepair = ('service', x[1])
        service_review.append(servicepair)
    if check_list(food_word, review):
        foodpair = ('food', x[1])
        food_review.append(foodpair)
    if check_list(place_word, review):
        placepair = ('place', x[1])
        place_review.append(placepair)
    if check_list(price_word, review):
        pricepair = ('price', x[1])
        price_review.append(pricepair)


len(service_review) # 917
len(food_review) # 1405
len(place_review) # 527
len(price_review) # 398


# transforming the reviews (in tuple) into dataframes
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
servicedf = pd.DataFrame(service_review, columns=['wordtag', 'rating'])
fooddf = pd.DataFrame(food_review, columns=['wordtag', 'rating'])
placedf = pd.DataFrame(place_review, columns=['wordtag', 'rating'])
pricedf = pd.DataFrame(price_review, columns=['wordtag', 'rating'])

# combining all the df together into one
combineddf = pd.concat([servicedf, fooddf, placedf, pricedf], ignore_index=True)

# export into CSV to visualise it in R
combineddf.to_csv(r'D:\User\Courses\PY4E coursera\project\combinedf.csv', index=False)

################################################################################
# splitting the reviews into individual words to look for the most common words

# append the reviews into a list
userreview = []
for i in dbreviews:
    userreview.append(i[0].lower())

# combining all the reviews into 1 whole lump
userreviewcombined = '\n'.join(userreview)

# use split to split up the lump of text into individual string
# use bracket to encapsulate all the punctuation i wanna split by
# doing it this way to preserve the word 'don't' as it will be split into 'don' and "'t"
# which will add into the word count for 'don' which is short for donburi in SG context
# giving inaccurate word count towards 'don'

tokenisedreview = re.split('[\s+?!().,]', userreviewcombined)

################################################################################
# capture the common words

commonwordlist = []
for i in tokenisedreview:
    if i not in stop_words: # removing stop words
        commonwordlist.append(i)

# combining all the common words into 1 chuck of text so can use regex to pull out the words
commonword = ' '.join(commonwordlist)

# pulling out the common words
commonword = re.findall('\w+', commonword)

# use collections library to count the common words
commonword = collections.Counter(commonword).most_common(20)

print(commonword)
'''
[('food', 1147), ('good', 779), ('service', 634), ('japanese', 302), ('nice', 292), ('staff', 264), ('sushi', 237), ('great', 230), ('place', 187), ('quality', 186), ('restaurant', 179), ('time', 150), ('ichiban', 146), ('price', 135), ('friendly', 133), ('set', 131), ('menu', 130), ('like', 129), ('always', 123), ('one', 115)]
'''

# creating a top 20 most common word list to group the reviews into
topcommonword = []
for i in commonword:
    topcommonword.append(i[0])

# loop to check if review contain the top 20 common words, then tuple the rating & the key word
tagrating = []

for a in range(0,20): # for looping the 20 common words
    for i in range(0,numofreview): # to loop through the 2060 reviews
        x = dbreviews[i]
        y = x[0].lower() # to extract out the review only
        if topcommonword[a] in y:
            pair = (topcommonword[a], x[1]) # tuple the rating to the food tag
            tagrating.append(pair)


commonworddf = pd.DataFrame(tagrating, columns=['word', 'rating'])

commonworddf.to_csv(r'D:\User\Courses\PY4E coursera\project\commonworddf.csv', index=False)



################################################################################
# capturing the key food words from ichiban's menu

# check if split review contain listed food words, then only append those words into list
commonfoodwordlist = []
for i in tokenisedreview:
    if i in commonfoodword:
        commonfoodwordlist.append(i)

commonfoodword = collections.Counter(commonfoodwordlist).most_common(20)
commonfoodword
'''
[('salmon', 75), ('beef', 56), ('don', 43), ('soba', 40), ('katsu', 38), ('udon', 35), ('curry', 33), ('tempura', 30), ('cheese', 16), ('unagi', 15), ('salad', 15), ('roll', 14), ('teriyaki', 14), ('egg', 12), ('chawanmushi', 12), ('saba', 11), ('steak', 9), ('tuna', 8), ('belly', 7), ('mentai', 6)]
'''

# creating top food word list to group the reviews into
topfoodword = []
for i in commonfoodword:
    topfoodword.append(i[0])

# loop to check if review contain the top food words, then tuple the rating & the key word for food
tagratingfood = []

# using regex to precisesly capture the words as compared to 'in' method above because of the word 'don'
# "don't" will be captured as 'don' using 'in' and other various methods

for a in range(0,20): # for looping the 20 common words
    for i in range(0,numofreview): # to loop through the 2060 reviews
        x = dbreviews[i]
        y = x[0].lower() # to extract out the review only
        if re.search(r'\b' + topfoodword[a] + r"(?!'|’)\b", y):
            pair = (topfoodword[a], x[1]) # tuple the rating to the food tag
            tagratingfood.append(pair)


commonfoodworddf = pd.DataFrame(tagratingfood, columns=['foodword', 'rating'])

commonfoodworddf.to_csv(r'D:\User\Courses\PY4E coursera\project\commonfoodworddf.csv', index=False)
