# %% 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys #give access to enter button, esc button, so that we can interactive more in the webpage
from selenium.webdriver.common.by import By #new syntax to search the webpage element by ID, class, etc
from selenium.webdriver.support.ui import WebDriverWait #to let the webpage load till certain element appear then execute next code
from selenium.webdriver.support import expected_conditions as EC #to let the webpage load till certain element appear then execute next code
from selenium.webdriver.support.ui import Select

import time #to set pauses inbetween action
import re
from bs4 import BeautifulSoup
import ssl
from pathlib import Path
import sys
import pandas as pd
from datetime import datetime
import os 


#ignore SSL certificate error
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def restart_search(driver):
    search = driver.find_element("xpath", "//input[@id='searchboxinput']")
    search.clear()
    userinput = input('Search (input as specific as possible):')
    search.send_keys(userinput)
    search.send_keys(Keys.RETURN)
    time.sleep(2)

# cwd = Path.cwd()
dir_path = os.path.dirname(os.path.realpath(__file__))
service = Service(executable_path=f'{dir_path}/chromedriver.exe')

def scrape_review() -> pd.DataFrame:
    driver = webdriver.Chrome(service=service)

    # input website to go to
    driver.get('https://www.google.com/maps')
    driver.maximize_window()

    print("What restaurant would you like to search for?")

    # wait for searchbox element to load and clear its content
    search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    search.clear()

    # not suitable for searching hotel related places as their layout is different
    userinput = input('Search (input as specific as possible):')
    search.send_keys(userinput)
    # search.send_keys('ichiban boshi')
    search.send_keys(Keys.RETURN) # return is enter, so to execute the search, like pressing enter

    feed_role_locator = ("xpath", "//*[@role='feed']")
    main_role_locator = ("xpath", "//*[@role='main']")

    while True:
        feed_flag = False
        
        try: # check to see if return multiple results

            WebDriverWait(driver, 10).until(EC.presence_of_element_located(feed_role_locator))
            
            # look for the role=feed: indicate many results were returned
            # do not use feed_role_locator variable for element, it wont work
            role_feed = driver.find_element("xpath", "//*[@role='feed']")

            # then look for class "hfpxzc" which will return the name and link to the respective restaurant
            class_hfpxzc = role_feed.find_elements("xpath", '//a[@class="hfpxzc"]')

            outlet_list = [i.get_attribute('aria-label') for i in class_hfpxzc]        
            max_options = 10
            outlet_list = outlet_list[:max_options]
            
            feed_flag = True
            
        except:
            # or return 1 results only
            
            main_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(main_role_locator)
            )
            
            break

        if feed_flag:   
            
            num_options = len(outlet_list)
            
            print("Please choose an option:")
            for i, options in enumerate(outlet_list, start=1):
                print(f"{i}. {options}")        
            print("0. Restart your search again\n")
            
            while True:
                choice = input(f"Enter the option number (0-{num_options}): \n")
                
                if choice.isdigit() and 1 <= int(choice) <= num_options:
                    chosen_option = int(choice)-1
                    print(f"you have chosen: {outlet_list[chosen_option]}")
                    print("\n....loading.....\n")
                    
                    search = driver.find_element("xpath", "//input[@id='searchboxinput']")
                    search.clear()
                    search.send_keys(outlet_list[chosen_option])
                    search.send_keys(Keys.RETURN) 
                    time.sleep(3) # need to sleep here, else it will still capture there's multiple result from previous search
                    break
                
                elif choice.isdigit() and int(choice) == 0:
                    restart_search(driver)
                    break
                
                else:
                    print("Invalid choice. Please try again.\n")
                    print("Please choose an option:")
                    for i, options in enumerate(outlet_list, start=1):
                        print(f"{i}. {options}")        
                    print("0. Restart your search again\n")
                
    print('going to next step\n')
    
    start_time = datetime.now()
    
    # click the reviews button
    review_button_element = driver.find_elements("xpath", "//*[@class='Gpq6kf fontTitleSmall']")
    for ele in review_button_element:
        button_name = ele.get_attribute('outerHTML')
        if 'review' in button_name.lower():
            review_button = ele

    # click the 'review' button
    review_button.click()
    time.sleep(2)

    # find number of reviews, to calculate how many times to scroll
    num_review_xpath = ('xpath', "//*[@class='fontBodySmall']")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located(num_review_xpath))
    num_reviews_elements = driver.find_elements("xpath", "//*[@class='fontBodySmall']")

    for ele in num_reviews_elements:
        check = ele.get_attribute('outerHTML')
        
        # using beautifulsoup to get text in between those HTML tags
        soup = BeautifulSoup(check, 'html.parser')            
        tags_with_text = soup.find_all(string=True)
        for tag in tags_with_text:
            if 'review' in tag.strip():
                num_reviews = re.findall(r'\d+', tag)

    num_reviews = int(num_reviews[0])
    print(f'there are {num_reviews} reviews for {outlet_list[chosen_option]}\n')

    print(f'.....scrolling to view all reviews for parsing.....\n')


    # wait for the sort review button to come out then click
    sort_review = (By.XPATH, "//button[@aria-label='Sort reviews']")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(sort_review)).click()
    time.sleep(2)

    # wait for the dropdown options from sort to come out and then click the one with 'newest'
    dropdown_xpath = ("xpath", "//*[@class='fxNQSd']")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(dropdown_xpath))
    sort_dropdown_element = driver.find_elements("xpath", "//*[@class='fxNQSd']")

    for ele in sort_dropdown_element:
        dropdown_options = ele.get_attribute('outerHTML')
        if 'newest' in dropdown_options.lower():
            sort_newest = ele

    # click the 'sort by newest' button
    sort_newest.click()
    time.sleep(2)


    # sort review by newest (old method not working anymore)
    # sortnewest = driver.find_element(By.XPATH, "//li[@data-index='1']")
    # sortnewest.click()

    # identifying the area to scroll
    toscroll = driver.find_element(By.XPATH,
        '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]')

    # each scroll gives only 10 reviews, so 'total review'/10 gives the total number of scrolls
    # to scroll out all reviews #default is 'range(0,(round(num_reviews/10)))'
    # if only updating new reviews to database, just run ~10 scrolls will be enough use 'range(0, 10)'
    for i in range(0,(round(num_reviews/10))):
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', toscroll)
        time.sleep(1)

    print(f'.....Expanding all comments for parsing.....\n')

    # expand all comments
    count = 0
    itemstoclick = driver.find_elements(By.XPATH, '//button[@class="w8nwRe kyuRq"]')
    for i in itemstoclick:
        i.click()
        count += 1
        time.sleep(0.5) # need slow it down else will error
    print(f'Expanded {count} comments for parsing\n')

    print(f'.....Capturing all the comments for parsing.....\n')

    ### capturing the google reviews ###
    # parsing
    # driver.page_source returns then current webpage to parse
    page_elements = BeautifulSoup(driver.page_source, 'html.parser')

    # extract the element that contain each block of reviews
    review_list_elements = page_elements.find_all('div', class_="jJc9Ad")

    review_list_to_df = []
    for reviews in review_list_elements:
        
        # capturing the user name
        usernames_w_tags = reviews.find_all('div', class_="d4r55")
        username = usernames_w_tags[0].get_text()
        
        # capturing the user ratings
        users_ratings_w_tags = reviews.find_all('span', class_='kvMYJc')
        user_ratings = users_ratings_w_tags[0].get('aria-label')
        user_ratings = re.findall(r'\d+', user_ratings)
        user_ratings = int(user_ratings[0])
        
        # capturing the user reviews
        users_review_w_tags = reviews.find_all('span', class_='wiI7pd')
        if users_review_w_tags:
            users_review = users_review_w_tags[0].get_text()
        else:
            users_review = ''
        
        # capturing the review time stamp
        review_timestamp_w_tags = reviews.find_all('span', class_="rsqaWe")
        review_timestamp = review_timestamp_w_tags[0].get_text()
        
        # capturing all in a list first then append to main list.
        review_list_to_df.append([username, user_ratings, users_review, review_timestamp])    
        
    col_names = ['user_name', 'user_ratings', 'user_reviews', 'review_timestamp']

    review_df = pd.DataFrame(review_list_to_df, columns=col_names)

    print(f'{len(review_df)} reviews captured for {outlet_list[chosen_option]} ')

    end_time = datetime.now()

    print(f"\nIt took {round((end_time-start_time).total_seconds()/60, 2)}mins to run this process\n")
    
    return review_df

if __name__ == "__main__":
    scrape_review()
