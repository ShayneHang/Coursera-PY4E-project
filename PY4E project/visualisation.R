library(tidyverse)
library(readxl)
library(dplyr) #dataframe transformation
library(readr)
library(skimr)
library(janitor)
library(readr)
library(magrittr)
library(ggplot2) #plotting
library(lubridate) #transforming date
library(ggpubr) #for pearson correlation
library(gapminder)
library(gganimate) #to animate graph
library(ggthemes) #to animate graph
library(transformr) #to animate graph
library(gifski) #to animate graph
library(sqldf) #to count number of unique values
library(stringr) #to check for string to filter


review_df <- read_csv("D:\\User\\Courses\\PY4E coursera\\project\\combinedf.csv")
view(review_df)

# review_df %>% 
#   filter(outlet == 'ichiban_boshi_waterway_point') %>% 
#   count()

# review_df %>%
#   arrange(rating) %>%
#   ggplot(aes(reviewtype, fill = as.factor(rating))) +
#   geom_bar(stat = 'count') +
#   coord_flip() +
#   ylab('number of reviews') +
#   xlab('type of reviews') +
#   scale_fill_manual(values = c('darkorange', 'orange', 'goldenrod', 'yellow3', 'yellowgreen'), 
#                     name = 'Rating', labels = c('1', '2', '3', '4', '5'))

review_df %>%
  ggplot(aes(x = fct_rev(fct_infreq(wordtag)), fill = as.factor(rating))) +
  geom_bar(stat = 'count') +
  coord_flip() +
  ylab('number of reviews') +
  xlab('type of reviews') +
  scale_fill_manual(values = c('darkorange', 'orange', 'goldenrod', 'yellow3', 'yellowgreen'), 
                    name = 'Rating', labels = c('1', '2', '3', '4', '5'))


# ggplot(data = edited_weight, aes(x = species, fill = sex)) + geom_bar(stat = "count") 



commonword_df <- read_csv("D:\\User\\Courses\\PY4E coursera\\project\\commonworddf.csv")
view(commonword_df)

commonword_df %>%
  ggplot(aes(x = fct_rev(fct_infreq(word)), fill = as.factor(rating))) +
  geom_bar(stat = 'count') +
  coord_flip() +
  xlab('top 20 common words') +
  ylab('number of reviews') +
  scale_fill_manual(values = c('darkorange', 'orange', 'goldenrod', 'yellow3', 'yellowgreen'), 
                    name = 'Rating', labels = c('1', '2', '3', '4', '5'))



commonfoodword_df <- read_csv("D:\\User\\Courses\\PY4E coursera\\project\\commonfoodworddf.csv")
view(commonfoodword_df)

commonfoodword_df %>%
  ggplot(aes(x = fct_rev(fct_infreq(foodword)), fill = as.factor(rating))) +
  geom_bar(stat = 'count') +
  coord_flip() +
  xlab('top 20 common food words') +
  ylab('number of reviews') +
  scale_fill_manual(values = c('darkorange', 'orange', 'goldenrod', 'yellow3', 'yellowgreen'), 
                    name = 'Rating', labels = c('1', '2', '3', '4', '5'))









# commonfoodword_df <- read_csv("D:\\User\\Courses\\PY4E coursera\\project\\foodwordcount.csv")
# view(commonfoodword_df)
# 
# commonfoodword_df %>% 
#   top_n(20) %>% 
#   mutate(words = fct_reorder(words, count)) %>% 
#   view()
#   ggplot() +
#   geom_col(aes(count, words))






################################################################################

daily_activities_sleep %>% 
  transform(Id = as.character(Id)) %>% 
  group_by(Id) %>% 
  summarise(avgsteps = mean(TotalSteps), avgcal = mean(Calories)) %>% 
  ggplot() +
  geom_col(aes(Id, avgsteps, fill = 'grey')) +
  geom_col(aes(Id, avgcal, fill = 'blue')) +
  geom_hline(yintercept = 10000, colour = 'black') + #10000 is the steps per day
  geom_hline(yintercept = 1800, colour = 'red', size = 0.8) + #1800 is the BMR calories
  scale_y_continuous(breaks = c(0, 1800, 5000, 10000, 15000, 20000)) +
  theme(axis.text.x = element_text(angle = 90)) +
  xlab('participant ID') +
  ylab('avg steps & calories burn per day') +
  scale_fill_manual(values = c('blue', 'grey'), name = 'Legend', labels = c('Calories', 'Steps'))