from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from helpers.scraper import scrape_review

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import RegexpParser
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")

import pprint
import re
from datetime import datetime

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

def find_string(index: int, text: str):
    start_index = text.rfind(' ', 0, index) + 1 if text[:index].rfind(' ') != -1 else 0
    end_index = text.find(' ', index)
    if end_index == -1:
        end_index = len(text)
    return text[start_index:end_index]

def clean_string(words: str):
    words = re.sub(r'[^\w\s]', '', words)
    words = re.sub(r'\n', '', words)
    # words = words.lower()
    
    return words

def noun_finder(text: str):
    # Tokenize the sentence into words
    words = word_tokenize(text)

    # Perform part-of-speech tagging
        # [('Food', 'NN'),
        #  ('was', 'VBD'),
        #  ('a', 'DT'),
        #  ('disappointing', 'JJ'),
    tagged_words = pos_tag(words)

    # Define a grammar for chunking
    # this will only connect nouns together
    # Create a chunk parser and apply chunking
    grammar = r""" NP: {<NN.*>+} """
    chunk_parser = RegexpParser(grammar)
    chunked_words = chunk_parser.parse(tagged_words)

    # Extract chunks (noun phrases)
    nouns = []
    for subtree in chunked_words.subtrees():
        if subtree.label() == 'NP':
            noun_phrase = ' '.join(word for word, pos in subtree.leaves())
            nouns.append(noun_phrase)

    return nouns

tokenizer = AutoTokenizer.from_pretrained("Dizex/FoodBaseBERT")
model = AutoModelForTokenClassification.from_pretrained("Dizex/FoodBaseBERT")
pipe = pipeline("ner", model=model, tokenizer=tokenizer)

# example = "Today's meal: Fresh olive poké bowl topped with chia seeds. Very delicious!"
# ner_entity_results = pipe(example)
# print(ner_entity_results)

# get the df with the reviews


def recommended_food():
    
    reviews_df = scrape_review()
    
    rating_food_dict = {1: [], 2: [], 3:[], 4:[], 5:[]}

    # test_reviews_df = reviews_df[20:40]

    print(f'.....parsing through the reviews.....\n')
    
    start_time = datetime.now()
    
    for i, data in reviews_df.iterrows():
        
        # refresh the word list
        food_word_list = []

        # skip empty reviews
        if data['user_reviews'] == '':
            continue
        
        
        review_text = data['user_reviews'].lower()
        
        # extracts only the nouns from the reviews.
        nouns_list = noun_finder(review_text)
        
        
        # if list not empty, use the model to check which are food and only capture those text
        if nouns_list:
            
            # using model to evaluate those captured nouns 
            ner_entity_results = pipe(nouns_list)
            
            
            for results, food_name in zip(ner_entity_results, nouns_list):
                
                # if results from model evaluation is not empty
                if results:
                    
                    # check the evaluation score
                    for scores in results:
                        
                        if scores['score'] >= 0.8:
                            
                            if food_name not in food_word_list:
                                food_word_list.append(food_name)

        # if there's food words captured, add to dict
        if food_word_list:
            rating_food_dict[data['user_ratings']].append(food_word_list)

    end_time = datetime.now()

    print(f"\nIt took {round((end_time-start_time).total_seconds()/60, 2)}mins to parse the data\n")

    print('These are the recommended food items from 4 & 5 stars reviews')
    recommended_food_list = rating_food_dict[4] + rating_food_dict[5]
    for i in recommended_food_list:
        print(i)
    
    return


if __name__ == "__main__":
    recommended_food()
