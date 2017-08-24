"
------------------------------------------------------------
Initialization
------------------------------------------------------------
"
#Basics
library(shiny)
library(DT)
library(tidyverse)
library(scales)
library(data.table)

#Run app
# runApp("../report/shiny")




"
Prepare raw data
"
#--Read in predicted scores (probability) of the 7 genres
#../data/output/df_predicted.csv
df_predicted <- fread("data/df_predicted.csv", header=TRUE) %>%
  select(-Review) %>%
  filter(Source == 1) #Preserve only from GameRadar


#--Read in games' basic info; join with the score data
#../data/df_cb_main.csv
df_main <- fread("data/df_cb_main.csv", header=TRUE) %>%
  left_join(y=df_predicted, by=c("Author Name"="Author", "Game Title"="Game")) %>%
  filter(CoreID == 0) %>% #Only non-core game
  select(-`Short Description`, -Source, -CoreID, -Predicted, -`Author Name`, -`Review`, -`File Name`) %>% #Remove uncessary columns
  distinct(`Game Title`, .keep_all=TRUE) %>% #Keep one game only one entry
  mutate_at(vars(matches("^[0-9]+$")), funs(round(., digits=4))) #Round score columns for later % display


#--Acquire distance matrix (based on the 7 genre scores)
df_dist <- select(df_main, num_range("", c(1:7))) %>%
  dist(method="euclidean", diag=FALSE, upper=FALSE) %>% #Euclidean is enough while the genre classification was based on Cosine between games
  as.matrix()


#--Read in scores of each keyword group; normalization (for identifying the differentiating features)
#../data/process/score_300_doc2vec.csv
df_keywordScore <- fread("data/score_300_doc2vec.csv", header=TRUE) %>%
  mutate_at(vars(starts_with("group")), funs(scale(.))) %>% #New vars with a "st" suffix
  as.data.table() #Coerce back to dt to avoid error


#--Read in keyword group terms and create a keyword dic
#../data/output/keywordGroup_hierarchy_300.csv
df_keyword <- fread("data/keywordGroup_hierarchy_300.csv", header=TRUE)

#Get unique keyword group ID
df_keywordDict <- distinct(df_keyword, cluster)
df_keywordDict$keyword <- map(.x=df_keywordDict$cluster, .f= ~ filter(df_keyword, cluster == .x)$keyword)


"
Function for fuzzy match game title

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
  Process outputs
  "
  #--Acquire search result titles
  searchResultTb.out <- eventReactive(input$searchButton, {
    #Acquire the result game titles
    searchResult <- fuzzyMatch(input$searchText, df_main["Game Title"])
    
    #Filter df_main with the result game titles
    searchResultTb <- filter(df_main, `Game Title` %in% searchResult[[1]])
    
    #Sort the df_main according to search result distance order
    searchResultTb[match(searchResult[[1]], searchResultTb[["Game Title"]]), ] 
  })
  
  
  #--Acquire target title basic info
  targetTitleTb.out <- reactive({
    #Use selected row number to filter the resultTb
    searchResultTb.out()[input$searchResult_rows_selected, ]
  })
  
  
  #--Acquire similar games
  similarTitleTb.out <- reactive({
    if(is.null(input$searchResult_rows_selected)){
      return(searchResultTb.out()[input$searchResult_rows_selected, ])
    }
    targetTitle <- searchResultTb.out()[[input$searchResult_rows_selected, "Game Title"]]
    targetTitleIndex <- match(targetTitle, df_main[["Game Title"]])
    similarTitleIndice <- sort(df_dist[targetTitleIndex, ])[2:6] %>%
      names() %>%
      as.numeric()
    df_main[similarTitleIndice, ]
  })
  
  
  #--Acquire distinguishing attributes
  distingushingKeyTb.out <- reactive({
    if(is.null(input$searchResult_rows_selected)){
      return(data.table(Abs = character(), V1 = character(), Percentage = character()))
    }
    targetTitle <- searchResultTb.out()[[input$searchResult_rows_selected, "Game Title"]]

    targetKeyScores <- filter(df_keywordScore, Game == targetTitle) %>%
      select(matches("^group[0-9]+$")) %>%
      t() %>%
      as.data.table(keep.rownames="keygroup") %>%
      mutate(Abs = abs(V1)) %>%
      top_n(5)
    
    x <- map(.x=targetKeyScores$keygroup, .f= ~ ecdf(df_keywordScore[[.x]]))
    y <- map2(.x=x, .y=targetKeyScores$V1, .f= ~ .x(.y))
      
    targetKeyScores$Percentage <- unlist(y)
    
    targetKeyScores$keywords <- map(.x=targetKeyScores$keygroup,
                                    .f= ~ filter(df_keywordDict, cluster == as.numeric(sub(pattern="group", replacement="", x=.x)))$keyword %>% unlist())
    targetKeyScores
  })

  
  #--Clear data table selection 
  observeEvent(input$clearSelection, {
    dataTableProxy('queryResult') %>% selectRows(NULL)
  })
  


  
  "
  Render output
  "
  #--Objects
  #Search result
  output$searchResult <- DT::renderDataTable({
    DT::datatable(searchResultTb.out() %>%
                    mutate(` ` = `Game Title`) %>%
                    select(`Game Title`, ` `), #Display only title and review link
                  selection="single",
                  options=list(pageLength=10, dom="tip", columnDefs=list(list(
                    targets=2,
                    render=JS(
                      "function(data, type, row, meta) {",
                      "return '<span title=\"' + data + '\"><a href=\"https://www.google.com/search?q=' + data + ' video game\">search for this game</a></span>';",
                      "}")
                  ))))
  })
  
  #Target title 
  output$targetTitle <- DT::renderDataTable({
    DT::datatable(targetTitleTb.out() %>%
                    select(-V1) %>%
                    mutate_at(vars(matches("^[1-9]+$")), funs(percent)), #Change into percent format
                  selection="none",
                  options=list(pageLength=1, dom="t"))
  })
  
  #Similar title 
  output$similarTitle <- DT::renderDataTable({
    DT::datatable(similarTitleTb.out() %>%
                    select(-V1) %>%
                    mutate_at(vars(matches("^[1-9]+$")), funs(percent)), #Change into percent format
                  selection="none",
                  options=list(pageLength=5, dom="t"))
  })
  
  #Distinguishing strong features
  output$dStrongFeature <- DT::renderDataTable({
    DT::datatable(distingushingKeyTb.out() %>%
                    filter(V1 > 0) %>%
                    select(-V1, -Abs) %>%
                    mutate(Percentage = percent(Percentage)), #Change into percent format
                  selection="none",
                  options=list(pageLength=5, dom="t"))
  })
  
  #Distinguishing strong features
  output$dWeakFeature <- DT::renderDataTable({
    DT::datatable(distingushingKeyTb.out() %>%
                    filter(V1 < 0) %>%
                    select(-V1, -Abs) %>%
                    mutate(Percentage = percent(Percentage)), #Change into percent format
                  selection="none",
                  options=list(pageLength=5, dom="t"))
  })

  
  #--Headers
  #Main panel
  output$mainHeader_1 <- renderUI({
    HTML("<h3>Target Game</h3>")
  })
  output$mainHeader_2 <- renderUI({
    HTML("<hr><br> <h3>Similar Games</h3>")
  })
  output$mainHeader_3 <- renderUI({
    HTML("<hr><br> <h3>Dominant Features</h3>")
  })
  output$mainHeader_4 <- renderUI({
    HTML("<hr><br> <h3>Distingusishing Features</h3>")
  })
  output$mainHeader_4_1 <- renderUI({
    HTML("<h4>Strong</h4>")
  })
  output$mainHeader_4_2 <- renderUI({
    HTML("<br> <h4>Weak</h4>")
  })
  
}