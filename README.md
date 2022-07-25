# Coursera PY4E project - Google Review Scraper & Analysis

This is my project as part of [PY4E (Python for everybody)](https://www.coursera.org/specializations/python) course by Prof Charles Russell Severance of University of Michigan. By doing this project also helps to enforce and apply what I learnt.
  
The PY4E course introduce fundamental programming concepts including data structures, networked application program interfaces, and databases, using the Python programming language. Aim of the Capstone Project will be to use the technologies learned throughout the Specialization to design and create our own applications for data retrieval, processing, and visualization.

Hence I decided to go with writing a Google review scraper (as part of the data retrieval) and perform review sentiment analysis (as part of processing and visualisation).

Google review scraper first uses [Selenium](https://www.selenium.dev/) to access the review page of the point of interest (‘POI’), then using [Beautifulsoup](https://beautiful-soup-4.readthedocs.io/en/latest/) to pull the relevant HTML tags and parse to extract the required information out such as the username, reviews and their ratings.

After gathering the data, I append them into list and use SQLite as my database to store the data. I created 3 separate different SQL script each with different functions.
- Greviewseparate.py will save the reviews from different POI into separate SQLite files
- Greviewscombine.py will save the reviews from different POI into one same SQLite file
- Greviewupdate.py will update existing SQLite file with new reviews from previously scrapped POI

Storing the data in SQL also allows easy sharing and access. 

Lastly, is performing review sentiment analysis on the captured data. The reviews will first be grouped into four different categories – service, food, place and price because these four qualities are what mainly determined whether diners will return or choose to try out in a new restaurant. I only extracted the ratings of the reviews and tuple it with the category that it matched.

Next I combine all the reviews together as one whole text separated by space, and split them up into individual words. Then run those words through a stop words list to remove any stop words. After stop words are removed from the reviews, I use [collections](https://docs.python.org/3/library/collections.html) library to find out the top 20 most common words mentioned from all the reviews (similar to what Google map does for each POI). 

Using back the original reviews, I run them through this newly created list of top 20 most common words and extracting only the ratings of the reviews and tuple it with the word it matches. 

I repeated the same procedure but now for top 20 common food words, where the food words are extracted from the restaurant’s menu. This is to identify and gauge what is popular from their menu based on the frequency it was mentioned in the reviews. 

After all that is done, I turn the tuples into data frames before exporting them out as CSV to visualise them using R. I decided to use R as my visualisation tool as their syntax is easier to use and Rstudio itself is more powerful in creating visualisation. 

Please refer to my [report](https://github.com/hkh117/Coursera-PY4E-project/blob/master/PY4E%20project/Ichiban-Boshi-Google-Review-report.pdf) for my analysis.

# Limitations 

1. I initially tried to use Tensorflow to perform the review sentiment analysis, but it was not working out due to my limited knowledge, hence I decided to temporary go with the inflexible method of listing out keywords relating each category and filtering out the reviews accordingly. 

So the type of review analysis is limited by the list of keywords I created to filter the reviews. If this script is use to perform review analysis on a new different restaurant, the keywords will have to be tweaked to cater to the new restaurant. For example from my report I performed review analysis on Ichiban Boshi, which is a Japanese restaurant chain, so keywords used are relating to Japanese cuisine which will not be suitable for other type of none Japanese restaurants. 

2. Secondly, the sentiment of reviews is solely based on the ratings given by the diner in their reviews. So in cases where diner gave review on something negative, but with a high rating – this will result in that review falsely captured as positive. 

Take this this review below for example, this user gave a 4 out of 5 stars rating: 
  “**Service is slow due to shortage of manpower. Overall food is acceptable**”

This review will be grouped under **service** & **food** due keyword ‘service’ & ‘food’. Though it was a 4/5 stars rating, user specifically stated service was not up to standard. So in this case it will be falsely captured with a positive rating of 4/5 stars under service category. 

3) The google review scraper script does not cater to POI such as Hotels as they have different interface.


Next up I will be working to use machine learning to perform the review sentiment analysis. I will update if there is success. 

Appreciate to have any feedbacks for improvements. Thanks!
