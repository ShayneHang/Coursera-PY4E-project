import sqlite3
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
import nltk
import re
import collections
import pandas as pd
import openpyxl # to export as excel


# extracting reviews from database
conn = sqlite3.connect(r'D:\User\Courses\PY4E coursera\project\ichiban boshi reviews 13.7.2022 2.40pm\a ichiban_boshi_main.sqlite')
cur = conn.cursor()
cur.execute('''
SELECT users_review, users_rating, outlet_name FROM GoogleMapReviews WHERE (users_review != 'None')
''')
dbreviews = cur.fetchall()
numofreview = len(dbreviews) # 2060

## creating list of keywords for respective qualities to be categorised into

service_word = ['service', 'services', 'staff', 'staffs', 'crew', 'crews', 'attitude',
                'attitudes', 'experience', 'experiences', 'friendly', 'unfriendly', 'helpful',
                'help', 'wait', 'waiting', 'understanding', 'understand', 'personal',
                'quick', 'fast', 'slow', 'complain']

food_word = ['food', 'foods', 'drink', 'drinks', 'sushi', 'nigiri', 'sashimi',
             'maki', 'dessert', 'gunkan', 'katsu', 'karaage', 'soup', 'cutlet',
             'ramen', 'don', 'soba', 'bento', 'tempura', 'handroll', 'miso', 'tasty',
             'taste', 'delicious', 'yummy', 'fresh', 'freshest', 'ingredient',
             'ingredients', 'tea', 'awful', 'appetizer', 'salad', 'makimono', 'donburi']

place_word = ['place', 'places', 'area', 'areas', 'wall', 'walls', 'ceiling',
              'ceilings', 'window', 'windows', 'door', 'doors', 'plate', 'plates',
              'bowl', 'bowls', 'utensils', 'utensil', 'spoon', 'spoons', 'fork',
              'forks', 'chopstick', 'chopsticks', 'seat', 'seats', 'table', 'tables',
              'ambience', 'atmosphere', 'lights', 'light', 'lighting', 'clean',
              'cleaniness', 'comfort', 'comfortable', 'un-comfort', 'uncomfort',
              'uncomfortable', 'oil', 'oily', 'dirty', 'dirt', 'disgust', 'disgusting',
              'insects', 'insect', 'bug', 'bugs', 'cockroach', 'cockroaches', 'rat',
              'rats', 'fly', 'flies', 'soil', 'sanitize', 'sanitise', 'floor', 'floors',
              'top', 'tops', 'dust', 'dusty', 'dusts', 'cozy']

price_word = ['price', 'prices', 'pricey', 'pricing', 'cheap', 'cheapest', 'expensive',
              'worth', 'budget', 'value', 'money', 'affordable', 'afford', 'inexpensive']


# list of words extracted from ichiban's menu
commonfoodword = ['mala', 'edamame', 'karaage', 'tofu', 'gyoza', 'chawanmushi',
                  'salad', 'amaebi', 'salmon', 'belly', 'hamachi', 'tako', 'scallop',
                  'tuna', 'hotate', 'kajiki', 'beef', 'tamago', 'inari', 'karibu',
                  'unagi', 'ebi', 'submarine', 'akami', 'cheese', 'ika', 'mayo',
                  'ebiko', 'lobster', 'tobiko', 'ikura', 'egg', 'chuka', 'octopus',
                  'wakame', 'roll', 'teriyaki', 'saba', 'shogayaki', 'katsu', 'tempura',
                  'steak', 'yaki', 'curry', 'kastu', 'don', 'jyu', 'chasoba', 'soba',
                  'udon', 'handroll', 'mentai', 'dragon']

# removing stop words - extracted from nltk function, and did some adjustment to suit my project
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
              'will', 'just', "don't", 'should', "should've", 'now', 'ain', 'aren',
              "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't",
              'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
              'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't",
              'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", "won't",
              'wouldn', "wouldn't", 'get', 'also', 'translated', "it’s", "there's",
              "that's", "he's", "her's", "there’s", "that’s", "let's", "let’s", "here's",
              "here’s"]

# check for duplicate among the word lists
check_servicefood = any(x in service_word for x in food_word)
check_serviceplace = any(x in service_word for x in place_word)
check_serviceprice = any(x in service_word for x in price_word)

if check_servicefood:
    print('there is duplicate')
else:
    print('no duplicate')

if check_serviceplace:
    print('there is duplicate')
else:
    print('no duplicate')

if check_serviceprice:
    print('there is duplicate')
else:
    print('no duplicate')


service_review = []
food_review = []
place_review = []
price_review = []

# creating function to check element in one list is in another list
def check_list(list1, list2):
    check = False

    #iterate the first list
    for x in list1:

        #iterate the second list
        for y in list2:

            if x == y:
                check = True
                return x

# i should not do elif because some comments may talk about both food and services
# so e.g. its ok to have duplicate comments in both food and services review list

# loop to check if review contain keyword, then categories it accordingly
for i in range(0, numofreview):
    x = dbreviews[i]
    tokenise = word_tokenize(x[0])
    if check_list(tokenise, food_word):
        food_review.append(x)
    if check_list(tokenise, service_word):
        service_review.append(x)
    if check_list(tokenise, place_word):
        place_review.append(x)
    if check_list(tokenise, price_word):
        price_review.append(x)

len(service_review) #786
len(food_review) #1166
len(place_review) #395
len(price_review) #322

print(place_review)

# transforming the reviews which are in tuple into dataframes
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
servicedf = pd.DataFrame(service_review, columns=['Users review', 'Users rating (out of 5)', 'outlet']) #785, inclusive of 0
fooddf = pd.DataFrame(food_review, columns=['Users review', 'Users rating (out of 5)', 'outlet']) #1165
placedf = pd.DataFrame(place_review, columns=['Users review', 'Users rating (out of 5)', 'outlet']) #394
pricedf = pd.DataFrame(price_review, columns=['Users review', 'Users rating (out of 5)', 'outlet']) #321

# testing out the appending 2 dataframe together
servicedf.append(fooddf, ignore_index=True) # if append food and service = 1951, so new value is from 786 to 1951
# so i can just calculate the ending by suming the len, then minus 1 e.g. 786+1166 = 1952 - 1 =1951
# the starting can be find by taking ending - len, then plus 1 e.g. 1951-1166 = 785 + 1 = 786

# combining all the df together into one
combineddf = pd.concat([servicedf, fooddf, placedf, pricedf], ignore_index=True)

# creating 1 more column to differentiate the type of reviews
combineddf['reviewtype'] = 'service'
combineddf

# renaming the values in the 'reviewtype' col to respective category

# food reviews is from index:
# 2668-322-395-1166 = 785+1 = 786 to
# 786+1166 = 1952-1 = 1951
combineddf.loc[786:1951, 'reviewtype'] = 'food'

# place reviews is from index:
# 2668-322-395 = 1951+1 = 1952 to
# 786+1166+395 = 2347-1 = 2346
combineddf.loc[1952:2346, 'reviewtype'] = 'place'


# price reviews is from index: using previous ending 2346+1=2347 to the end
combineddf.loc[2347:, 'reviewtype'] = 'price'

# export the df out as excel to R studio for visualisation
combineddf.to_csv(r'D:\User\Courses\PY4E coursera\project\combinedf.csv', index=False)

################################################################################
# splitting the whole reviews into individual strings

len(dbreviews) #2060

# append the reviews into a list
userreview = []
for i in dbreviews:
    userreview.append(i[0].lower())

len(userreview) #2060

# combining all the reviews into 1 whole lump
userreviewcombined = '\n'.join(userreview)

# use split to split up the lump of text into individual string
# use bracket to encapsulate all the punctuation i wanna split by
tokenisedreview = re.split('[\s+?!().,]', userreviewcombined)
print(tokenisedreview)

################################################################################
# capture the common words

commonwordlist = []
for i in tokenisedreview:
    if i not in stop_words:
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

# extracting the common word out of the tuple
topcommonword = []
for i in commonword:
    topcommonword.append(i[0])

# loop to check if review contain the keywords, then tuple the rating + key word
tagrating = []

for a in range(0,20): # for looping the 20 common words
    for i in range(0,numofreview): # to loop through the 2060 reviews
        x = dbreviews[i]
        y = x[0].lower() # to extract out the review only
        if topcommonword[a] in y: # actually use 'in' function can already, dont need tokenise
            pair = (topcommonword[a], x[1]) # tuple the rating to the food tag
            tagrating.append(pair)


len(tagrating) # 5573 review
# 1036 for number for reviews contain 'food' if i do it w/o 'range(0,20)' loop,
# but also still same 1036 reviews with 'range(0,20)' loop
# 667 count for 'good' w/o 'range(0,20)' loop
# 667 count for 'good' w/ 'range(0,20) loop
# thing to note why the number here is lesser, cause its length of review, whereas
# above is number of times 'food' is mentioned, so cause some reviews might have duplicate mentioned of word e.g. 'food'
# that's why when convert back to length of review is lesser


# check length of 'food' and 'good' make sure correct
count = 0
for i in tagrating:
    if 'good' in i:
        count += 1
print(count)

commonworddf = pd.DataFrame(test, columns=['word', 'rating'])

commonworddf.to_csv(r'D:\User\Courses\PY4E coursera\project\commonworddf.csv', index=False)



################################################################################
# capturing the common food words

# check if split review contain listed food words, then only append those words into list
commonfoodwordlist = []
for i in tokenisedreview:
    if i in commonfoodword:
        commonfoodwordlist.append(i)

tokenisedreview
# as the list already contained the individual words, can just use collections to count it
commonfoodword = collections.Counter(commonfoodwordlist).most_common(20)
commonfoodword
'''
[('salmon', 75), ('beef', 56), ('don', 43), ('soba', 40), ('katsu', 38), ('udon', 35), ('curry', 33), ('tempura', 30), ('cheese', 16), ('unagi', 15), ('salad', 15), ('roll', 14), ('teriyaki', 14), ('egg', 12), ('chawanmushi', 12), ('saba', 11), ('steak', 9), ('tuna', 8), ('belly', 7), ('mentai', 6)]
'''
# extracting out the word from tuple
topfoodword = []
for i in commonfoodword:
    topfoodword.append(i[0])


# loop to check if review contain the keywords, then tuple the rating + key word for food
tagratingfood = []

for a in range(0,20): # for looping the 20 common words
    for i in range(0,numofreview): # to loop through the 2060 reviews
        x = dbreviews[i]
        y = x[0].lower() # to extract out the review only
        if re.search(r'\b' + topfoodword[a] + r"(?!'|’)\b", y): # actually use 'in' function can already, dont need tokenise
            pair = (topfoodword[a], x[1]) # tuple the rating to the food tag
            tagratingfood.append(pair)

len(tagratingfood) # 411
print(tagratingfood)


# if re.search(r'\b' + topfoodword[a] + r'\b', y):
#     print(True)
# else:
#     print(False)

# check length of 'salmon' and 'beef' etc
count = 0
for i in tagratingfood:
    if 'beef' in i:
        count += 1
print(count)

commonfoodworddf = pd.DataFrame(tagratingfood, columns=['foodword', 'rating'])

commonfoodworddf.to_csv(r'D:\User\Courses\PY4E coursera\project\commonfoodworddf.csv', index=False)

# loop to capture don reviews only
# topfoodword[2] #don
donreviews = []

for i in range(0,numofreview): # to loop through the 2060 reviews
    x = dbreviews[i]
    y = x[0].lower()
    if x[1] > 2: continue
    if re.search(r'\b' + topfoodword[2] + r"(?!'|’)\b", y):
        donreviews.append(y)

len(donreviews)
# reviews with don - 134
# reviews with don and only 1 or 2 stars - 60
# reviews with don and only 1 or 2 stars using regex - 15

for i in donreviews:
    print(i, '\n')

a = dbreviews[2001]
b = a[0].lower()
print(b)

if topfoodword[2] in b:
    print('word found')
else:
    print('not found')



##### method to find EXACT word match in a sentence, use regex with bound #####

# all other methods dont work - in, find(), count(), index(), contain()
# 'in' method is not accurate, as it will also return true if that 'word' is only
# part of the entire word e.g. below
sentence = 'There are more trees on Earth than stars in the Milky Way galaxy'
word = 'ore'
wordx = 'moretree'

if wordx in sentence:
    print('Word found.')
else: print(False)

'''but lets says i tokenised the words, and i try again, it does not work.
so to say if i want the exact word return using 'in' method, i need to tokenise the words as shown below
but lets say i dont need exact word return e.g. i search for food, i dont mind returning 
foodie, foods - i dont tokenise the words, leave it in whole sentence and they cannot be in list 
then use 'in' method as shown above
'''

sentencex = ['i am foodie', 'foodie', "don't"]
wordy = 'food'
wordxy = 'don'

if wordxy in sentencex:
    print(True)
else:
    print(False) #return false



# find() method does not work as well cause it also works same as 'in' method above
sentence = 'There are more trees on Earth than stars in the Milky Way galaxy'
word = 'ore'

check = sentence.find(word)
print(check) #11

# count() method does not work as well cause it also works same as 'in' method above
sentence = 'There are more trees on Earth than stars in the Milky Way galaxy'
word = 'axy'

check = sentence.count(word)
print(check) #1


# index() method does not work, it works exactly as find()
sentence = 'There are more trees on Earth than stars in the Milky Way galaxy'
word = 'ore'

check = sentence.index(word)
print(check) #11

# contain() method does not work, it works exactly as find()
import operator

sentence = 'There are more trees on Earth than stars in the Milky Way galaxy'
word = 'axy'

check = operator.contains(sentence, word)
print(check) #True

# regex cannot work, think need more precious filtering
sentence = "There are more trees on Earth than stars in the Milky Way galaxy don't"
word = 'don'

# if re.search('ore', sentence):
#     print(True) #returns true
# else:
#     print(False)

# this will still match dont't but not dont due to the special character '
# if re.search('\bword\b', sentence):
#     print(True)
# else:
#     print(False)

# now is to repair all the loop with regex so will capture correct reviews

if re.search(r'\b' + word + r"(?!')\b", sentence):
    print(True)
else: print(False)





