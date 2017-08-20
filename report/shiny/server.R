"
------------------------------------------------------------
Initialization
------------------------------------------------------------
"
#Basics
library(shiny)
library(DT)
library(tidyverse)

#Run app
# runApp("../report/shiny")




"
Prepare raw data
"
#--Read in predicted scores (probability) of the 7 genres
#../data/output/df_predicted.csv
df_predicted <- read_csv("data/df_predicted.csv") %>%
  select(-Review) %>%
  filter(Source == 1) #Preserve only from GameRadar


#--Read in games' basic info; join with the score data
#../data/df_cb_main.csv
df_main <- read_csv("data/df_cb_main.csv") %>%
  left_join(y=df_predicted, by=c("Author Name"="Author", "Game Title"="Game")) %>%
  filter(CoreID == 0) %>% #Only non-core game
  select(-`Short Description`, -Source, -CoreID, -Predicted, -`Author Name`, -`Review`) %>% #Remove uncessary columns
  distinct(`Game Title`, .keep_all=TRUE) #Keep one game only one entry


#--Acquire distance matrix (based on the 7 genre scores)
df_dist <- select(df_main, num_range("", c(1:7))) %>%
  dist(method="euclidean", diag=FALSE, upper=FALSE) %>% #Euclidean is enough while the genre classification was based on Cosine between games
  as.matrix()


x <- df_dist[1,]
sort(x)[4]
#Acquire percentile
ecdf(df_dist[1,])(0.46643647)


#--Read in scores of each keyword group; normalization (for identifying the differentiating features)
#../data/process/score_300_doc2vec.csv
df_keywordScore <- read_csv("data/score_300_doc2vec.csv") %>%
  mutate_at(vars(starts_with("group")), funs(st = scale(.))) #New vars with a "st" suffix


#--Read in keyword group terms
#../data/output/keywordGroup_hierarchy_300.csv
df_keyword <- read_csv("data/keywordGroup_hierarchy_300.csv")




"
Function for Fuzzy match game title

- a = target
- b = searched list
- return = df(original searched list, distance; distance from low to high)
"
fuzzyMatch <- function(a, b, max_dist=10, top_n=20) {
  #Load the stringdist package
  require(stringdist)
  
  #Make all lower cases
  a_lower <- tolower(a)
  b_lower <- sapply(b, tolower)
  
  #Calculate restricted Damerau-Levenshtein distance (osa)
  distance <- stringdistmatrix(a_lower, b_lower, method='osa', nthread=parallel:::detectCores()) %>% t()
  
  #Make df, limit max distance, order, extract the best n results
  df <- data.frame(b, distance) %>%
    filter(distance <= max_dist) %>%
    arrange(distance) %>%
    slice(1:top_n)
  
  #Return the df
  return(df)
}

#Function testing
x <- fuzzyMatch("laysy", c("laysy", "1 lazy", "1", "1 LAZY", "laysy", "LAYSY"))








"
------------------------------------------------------------
Back end
------------------------------------------------------------
"
server <- function(input, output) {
  "
  Search game title
  "
  searchResultTb.out <- eventReactive(input$searchButton, {
    #Acquire the result game titles
    searchResult <- fuzzyMatch(input$searchText, df_main["Game Title"])
    
    #Filter df_main with the result game titles
    searchResultTb <- filter(df_main, `Game Title` %in% searchResult[[1]])
    
    #Sort the df_main according to search result distance order
    searchResultTb[match(searchResult[[1]], searchResultTb[["Game Title"]]), ] %>%
      mutate_at(vars(matches("^[1-9]+$")), funs(percent)) #Change into percent format
  })
  
  
  targetTitleTb.out <- reactive({
    searchResultTb.out()[input$searchResult_rows_selected, ] 
  })
  
  
  "
  Clear data table selection 
  "
  observeEvent(input$clearSelection, {
    dataTableProxy('queryResult') %>% selectRows(NULL)
  })
  


  
  "
  Render output
  "
  #--Output data table
  output$searchResult <- DT::renderDataTable({
    DT::datatable(searchResultTb.out(), options=list(pageLength=10, dom="tip"), selection="single")
  })
  
  output$targetTitle <- DT::renderDataTable({
    DT::datatable(targetTitleTb.out(), options=list(pageLength=1, dom="t"), selection="none")
  })
  
  output$test <- renderUI({
    HTML("test <hr>")
  })
  
}