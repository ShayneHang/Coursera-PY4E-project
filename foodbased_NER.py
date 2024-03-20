# %% 

from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from helpers.scraper import scrape_review


tokenizer = AutoTokenizer.from_pretrained("Dizex/FoodBaseBERT")
model = AutoModelForTokenClassification.from_pretrained("Dizex/FoodBaseBERT")

pipe = pipeline("ner", model=model, tokenizer=tokenizer)
# example = "Today's meal: Fresh olive poké bowl topped with chia seeds. Very delicious!"
# ner_entity_results = pipe(example)
# print(ner_entity_results)

'''
objective:
    - retrieve the most recommended and least recommended food, it does not mean the 
    most mentioned food is the most delicious, it must be most mentioned plus with 
    positives reviews
    
    
    # more for business owner usage
    - find out which period of the year has the most reviews, and if there's any
    seasonal trend to it
    
    - make a stats of returning customer (e.g. look for duplicate usernames in the
    review and check if their ratings has increase or decrease over time)
    
    - to identify the reviews on the food, service, cleaniness, and place in general
    
    - what are the evolution of recommended/not recommended food throughout the years

'''


# %% get the df with the reviews

reviews_df = scrape_review()

# %% 

test = reviews_df['user_reviews'][0:1].values[0]
ner_entity_results = pipe(test)
for i in ner_entity_results:
    print(i['word'])
    

# another way to fix the ## with the results is to use word proximity and determine
# which words does it belongs to


# %% 

rating_food_dict = {1: [], 2: [], 3:[], 4:[], 5:[]}
rating_food_dict_2 = {1: [], 2: [], 3:[], 4:[], 5:[]}


test_reviews_df = reviews_df[:10]

for i, data in test_reviews_df.iterrows():
    food_word_list = []
    food_word_list_2 = []
    # print(data['user_reviews'])
    # print(type(data['user_reviews']))
    ner_entity_results = pipe(data['user_reviews'])
    
    for i in ner_entity_results:
        food_word_list.append(i['word'])
    rating_food_dict[data['user_ratings']] = food_word_list
    # print(f'this is food_word_list: {food_word_list}')
    
    for words in data['user_reviews'].split():
        # print(words.lower())
        if words.lower() in food_word_list:
            # print('there is a match@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            food_word_list_2.append(words)
    rating_food_dict_2[data['user_ratings']] = food_word_list_2

print(rating_food_dict)
print(rating_food_dict_2)

