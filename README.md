# Coursera PY4E project - Google Review Scraper & Analysis

This is my project as part of [PY4E (Python for everybody)](https://www.coursera.org/specializations/python) course by Prof Charles Russell Severance of University of Michigan. By doing this project also helps to enforce and apply what I learnt.

I made some changes to original Google review scraper to suit my own uses, often times when i dine out i cannot decide what to try, and would refer to google review for recommendations.

What I done now was to only scrape the 4 and 5 stars reviews, then tokenize the reviews (which will break it down into individual words) and perform part-of-speech tagging to tag nouns together. So from a text of reviews, its transformed into list of nouns extracted from the review text.

Then lastly i will use [Dizex's fine-tuned BERT model](https://huggingface.co/Dizex/InstaFoodRoBERTa-NER) uploaded in hugging face, to identify the food nouns in the list of nouns.

Dizex's model uses named entity recognition (NER) which is a natural language processing (NLP) technique that finds and categorizes named entities in text into predefined categories. In this case, the model is traine using food entities on social media like informal text (e.g. Instagram, X, Reddit). It has been trained to recognize a single entity: food (FOOD).

![Alt Text](static/images/how_it_works.gif)
