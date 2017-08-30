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
library(feather)

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
  mutate_at(vars(matches("^[0-9]+$")), funs(round(., digits=4))) %>% #Round score columns for later % display
  select(`Game Title`, `Release Date`, `ESRB Rating` = ESRB, `GS Score`, `User Score`, everything()) #Reorder columns for later display
names(df_main) <- gsub("^([0-9]+)$", "Genre \\1", names(df_main)) #Rename genre scores

#--Acquire distance matrix (based on the 7 genre scores)
RETRAIN <- FALSE
if(RETRAIN) {
  df_dist <- select(df_main, starts_with("Genre")) %>%
    dist(method="euclidean", diag=FALSE, upper=FALSE) %>% #Euclidean is enough while the genre classification was based on Cosine between games
    as.matrix() %>% #Convert a sparce matrix into dense
    saveRDS("data/df_dist.rds")
}
df_dist <- readRDS("data/df_dist.rds")


#--Read in scores of each keyword group; normalization (for identifying the differentiating features)
#../data/process/score_300_doc2vec.csv
READCSV <- FALSE
if(READCSV) {
  df_keywordScore <- fread("data/score_300_doc2vec.csv", header=TRUE) %>%
    mutate_at(vars(starts_with("group")), funs(st = scale(.))) %>% #New vars with a "st" suffix
    write_feather("data/score_300_doc2vec.feather") #Save feather to improve processing speed
}
df_keywordScore <- read_feather("data/score_300_doc2vec.feather") %>% as.data.table()


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
    #Validate the input text to not be empty
    validate(
      need(input$searchText != "", "Please enter valid text to search")
    )
    
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
  #Based on 7 genre scores
  similarTitleTb.out <- reactive({
    #Acquire target title name from selection
    targetTitle <- searchResultTb.out()[[input$searchResult_rows_selected, "Game Title"]]
    
    #Search the title in main
    targetTitleIndex <- match(targetTitle, df_main[["Game Title"]])
    
    #Use the target's index to find similar titles (with smallest dist) in df_dist
    similarTitleIndice <- sort(df_dist[ ,1])[2:6] %>% #Index 1 will be the target game itself
      names() %>% #Acquire their indices
      as.numeric()
    
    #Use the similar titles' indices to find similar titles in main
    df_main[similarTitleIndice, ]
  })
  

  #--Acquire dominant attributes
  dominantKeyTb.out <- reactive({
    #Acquire target title name from selection
    targetTitle <- searchResultTb.out()[[input$searchResult_rows_selected, "Game Title"]]
    
    #Acquire target's scores (unstanderdized) on each keyword group
    targetKeyScores <- df_keywordScore[Game == targetTitle][1] %>% #Limit to first matched entry if there are multiple
      select(matches("^group[0-9]+$")) %>%
      t() %>% #Transpose
      as.data.table(keep.rownames="keygroup") %>% #Transform rownames (group123) into one column
      setnames("V1", "score") %>% #Reset column name
      setkey(score) %>% #Set key for sorting
      .[order(-score)] %>% #Filter for top 5 absolute score (so that the list include the distinguishing features, comparatively high or low)
      .[1:5]
    
    #To get the corresponding terms, filter `df_keywordDict` by the keyword group ids, cleaned from `group123`
    targetKeyScores$keywords <- map(.x=targetKeyScores$keygroup,
                                    .f= ~ df_keywordDict[cluster == as.numeric(sub(pattern="group", replacement="", x=.x))]$keyword %>%
                                      unlist() %>%
                                      paste(collapse=", ") #Adjust typography
                                    )
    
    #Adjustments for display
    targetKeyScores[, `:=`(score = round(score, digits=2), #Round score
                           keygroup = sub(pattern="group", replacement="G", keygroup))] #Make cleaned name `GXXX`
    names(targetKeyScores) <- c("Keyword Group", "Similarity", "Keywords") #Rename

    #Return df
    targetKeyScores
  })
  

  #--Acquire distinguishing attributes
  distingushingKeyTb.out <- reactive({
    #Acquire target title name from selection
    targetTitle <- searchResultTb.out()[[input$searchResult_rows_selected, "Game Title"]]

    #Acquire target's scores (standerdized) on each keyword group
    targetKeyScores.st <- df_keywordScore[Game == targetTitle][1] %>% #Limit to first matched entry if there are multiple
      select(matches("^group[0-9]+_st$")) %>%
      t() %>% #Transpose
      as.data.table(keep.rownames="keygroup") %>% #Transform rownames (group123) into one column
      setnames("V1", "score") %>% #Reset column name
      .[ ,score.abs := abs(score)] %>% #Acquire absolute score for ranking
      setkey(score.abs) %>% #Set key for sorting
      .[order(-score.abs)] %>% #Filter for top 5 absolute score (so that the list include the distinguishing features, comparatively high or low)
      .[1:5]
      
    x <- map(.x=targetKeyScores.st$keygroup, .f= ~ ecdf(df_keywordScore[[.x]])) #Acquire cdf of each keyword score column
    y <- map2(.x=x, .y=targetKeyScores.st$score, .f= ~ .x(.y)) #Acquire percentage (position) of the scores of the target title by plugging in the scores into the cdfs
    
    #Combined into the df
    targetKeyScores.st$percentage <- unlist(y)
    
    #To get the corresponding terms, filter `df_keywordDict` by the keyword group ids, cleaned from `group123`
    targetKeyScores.st$keywords <- map(.x=targetKeyScores.st$keygroup,
                                       .f= ~ df_keywordDict[cluster == as.numeric(sub(pattern="group([0-9]+)_st", replacement="\\1", x=.x))]$keyword %>%
                                         unlist() %>%
                                         paste(collapse=", ") #Adjust typography
                                       )
    
    #Adjustments for display
    targetKeyScores.st[, `:=`(percentage = round(percentage, digits=4), #Round score
                           keygroup = sub(pattern="^group([0-9]+)_st$", replacement="G\\1", keygroup))]
    names(targetKeyScores.st) <- c("Keyword Group", "Similarity", "Similarity.abs", "Percent Rank", "Keywords") #Rename
    
    #Return df
    targetKeyScores.st
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
                    select(`Game Title`, `Release Date`, ` `), #Display only title, release date, and review link
                  selection="single",
                  options=list(pageLength=10, dom="tip", columnDefs=list(
                    list(targets=3, #Transform the 3rd column into a link
                         render=JS(
                           "function(data, type, row, meta) {",
                           "return '<span title=\"' + data + '\"><a href=\"https://www.google.com/search?q=' + data + ' video game\">search for this game</a></span>';",
                           "}")),
                    list(targets="_all", #Center text in all column
                         className="dt-center")
                  )))
  })

  #Target title 
  output$targetTitle <- DT::renderDataTable({
    if(!is.null(input$searchResult_rows_selected)) { #Display table only when target game is selected
      DT::datatable(targetTitleTb.out() %>%
                      select(-V1) %>%
                      mutate_at(vars(matches("^.+[1-9]+$")), funs(percent)), #Change into percent format
                    selection="none",
                    options=list(pageLength=1, dom="t", columnDefs=list(
                      list(targets="_all", #Center text in all column
                           className="dt-center")
                    )))
  }})
  
  #Similar title 
  output$similarTitle <- DT::renderDataTable({
    if(!is.null(input$searchResult_rows_selected)) { #Display table only when target game is selected
      DT::datatable(similarTitleTb.out() %>%
                      select(-V1) %>%
                      mutate_at(vars(matches("^.+[1-9]+$")), funs(percent)), #Change into percent format
                    selection="none",
                    options=list(pageLength=5, dom="t", columnDefs=list(
                      list(targets="_all", #Center text in all column
                           className="dt-center")
                    )))
  }})
  
  #Dominant features
  output$dominantFeature <- DT::renderDataTable({
    if(!is.null(input$searchResult_rows_selected)) { #Display table only when target game is selected
      DT::datatable(dominantKeyTb.out(),
                    selection="none",
                    options=list(pageLength=5, dom="t", columnDefs=list(
                      list(targets=c(1, 2), #Center text in column 1 and 2
                           className="dt-center"),
                      list(targets=3, #Make keyword text smaller
                           className="s-text")
                    )))
  }})
  
  #Distinguishing strong features
  output$dStrongFeature <- DT::renderDataTable({
    if(!is.null(input$searchResult_rows_selected)) { #Display table only when target game is selected
      DT::datatable(distingushingKeyTb.out() %>%
                      filter(Similarity > 0) %>%
                      select(-Similarity, -Similarity.abs) %>%
                      mutate(`Percent Rank` = percent(`Percent Rank`)), #Change into percent format
                    selection="none",
                    options=list(pageLength=5, dom="t", columnDefs=list(
                      list(targets=c(1, 2), #Center text in column 1 and 2
                           className="dt-center"),
                      list(targets=3, #Make keyword text smaller
                           className="s-text")
                    )))
  }})
  
  #Distinguishing weak features
  output$dWeakFeature <- DT::renderDataTable({
    if(!is.null(input$searchResult_rows_selected)) { #Display table only when target game is selected
      DT::datatable(distingushingKeyTb.out() %>%
                      filter(Similarity < 0) %>%
                      select(-Similarity, -Similarity.abs) %>%
                      mutate(`Percent Rank` = percent(`Percent Rank`)), #Change into percent format
                    selection="none",
                    options=list(pageLength=5, dom="t", columnDefs=list(
                      list(targets=c(1, 2), #Center text in column 1 and 2
                           className="dt-center"),
                      list(targets=3, #Make keyword text smaller
                           className="s-text")
                    )))
  }})
}