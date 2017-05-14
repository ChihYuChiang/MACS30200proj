library(tidytext)
library(scales)
library(topicmodels)
library(tidyverse)
library(sentimentr)
library(wordcloud)
library(SnowballC)
library(RColorBrewer)
library(reshape2)
library(knitr)
library(broom)
library(pander)
data(stop_words)

#--Read data, adjust encoding
data_raw <- read_csv("../data/output/df_predicted.csv") %>%
  mutate(Review = iconv(Review, "ASCII", "UTF-8"))


#--Tokenize, remove stop words, remove 0092 words
text_tidy <- data_raw %>%
  unnest_tokens(word, Review) %>%
  filter(!grepl("[0-9]+", word)) %>%
  anti_join(stop_words, by="word")


#--Text cloud - all
text_count <- text_tidy %>%
  count(word, sort=TRUE) %>%
  with(wordcloud(word, n, max.words=250, colors=brewer.pal(8, "Dark2"), random.order=FALSE))


#--Further filter to use only experiential keywords
keywords <- read_csv("../data/output/keywordGroup_hierarchy_10.csv")
text_tidy <- semi_join(text_tidy, keywords, by=c("word" = "keyword"))


#--Text cloud (only keyword)
#All
text_count <- text_tidy %>%
  count(word, sort=TRUE) %>%
  with(wordcloud(word, n, max.words=250, colors=brewer.pal(8, "Dark2"), random.order=FALSE))

#Each group
for (i in c(1:7)) {
  text_count <- text_tidy %>%
    filter(Predicted==i) %>%
    count(word, sort=TRUE) %>%
    slice(3:n()) %>%
    with(wordcloud(word, n, max.words=400, colors=brewer.pal(8, "Paired"), random.order=FALSE, scale=c(2, 0.5)))
}
