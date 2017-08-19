"
------------------------------------------------------------
Initialization
------------------------------------------------------------
"
#Basics
library(shiny)
library(DT)
library(tidyverse)

#Radar chart
library(fmsb)
library(scales)
library(RColorBrewer)




"
Prepare raw data
"
#Read in predicted scores (probability) of the 7 genres
df_predicted <- read_csv("../data/output/df_predicted.csv") %>%
  select(-Review) %>%
  filter(Source == 1) #Preserve only from GameRadar

#Read in games' basic info; join with the score data
df_main <- read_csv("../data/df_cb_main.csv") %>%
  left_join(y=df_predicted, by=c("Author Name"="Author", "Game Title"="Game")) %>%
  filter(CoreID == 0) %>% #Only non-core game
  select(-`Short Description`, -Source, -CoreID, -Predicted, -`Author Name`, -`Review`) %>% #Remove uncessary columns
  distinct(`Game Title`, .keep_all=TRUE) #Keep one game only one entry

#Acquire distance matrix (based on the 7 genre scores)
df_dist <- select(df_main, num_range("", c(1:7))) %>%
  dist(method="euclidean", diag=FALSE, upper=FALSE) %>% #Euclidean is enough while the genre classification was based on Cosine between games
  as.matrix()

x <- df_dist[1,]
sort(x)[4]
ecdf(df_dist[1,])(0.46643647)

#Read in scores of each keyword group
df_keywordScore <- read_csv("../data/process/score_300_doc2vec.csv") %>%
  mutate_at(vars(starts_with("group")), funs(st = scale(.)))

#Read in keyword group representative terms
df_keyword <- read_csv("../data/output/keywordGroup_hierarchy_300.csv")




"
Function for Fuzzy match game title

- a = target
- b = searched list
- return = df(original searched list, distance; distance from low to high)
"
fuzzyMatch <- function(a, b) {
  #Load the stringdist package
  require(stringdist)
  
  #Make all lower cases
  a_lower <- tolower(a)
  b_lower <- sapply(b, tolower)
  
  #Calculate restricted Damerau-Levenshtein distance (osa)
  distance <- stringdistmatrix(a_lower, b_lower, method='osa', nthread=parallel:::detectCores()) %>% t()
  
  #Make df, limit max distance, order, extract the best n results
  df <- data.frame(b, distance) %>%
    filter(distance <= 10) %>%
    arrange(distance) %>%
    slice(1:20)
  
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
  Filter data table according to the input
  "
  tbData <- reactive({
    #Default select all
    if(input$ESRB == "---"){
      filter(games_lda,
             `GS Score` >= input$GSScore[1],
             `GS Score` <= input$GSScore[2]
      )
    }else{
      filter(games_lda,
             `GS Score` >= input$GSScore[1],
             `GS Score` <= input$GSScore[2],
             ESRB == input$ESRB
      )
    }
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
  #--Output game topic spider plot
  output$spiderPlot <- renderPlot({
    if(is.null(input$queryResult_rows_selected)){
      return()
    }
    
    #Modify data to conform to radarchart's require form
    pltData <- tbData()[input$queryResult_rows_selected,]
    pltData <- rbind(rep(1, 4), rep(0, 4), select(pltData, 1:5))
    
    #Acquire color palette
    shapeColor <- colorRampPalette(brewer.pal(12, "Accent"))(nrow(pltData) - 2)
    
    #Plotting and plot setting
    radarchart( pltData[2:5] , axistype = 1,
                #custom polygon
                pcol = shapeColor, pfcol = shapeColor, plwd = 1, plty = 1,
                #custom the grid
                cglcol = "grey", cglty = 1, axislabcol = "grey", cglwd = 0.8,
                #custom labels
                vlcex = 1.2
    )
    
    #Add legend
    legend(-2.5, 1.2, legend = levels(as.factor(pltData$Game[3:length(pltData$Game)])), title = "Game", col = shapeColor, seg.len = 2, border = "transparent", pch = 16, lty = 1)
  })
  
  
  #--Output data table
  output$queryResult <- DT::renderDataTable({
    DT::datatable(tbData() %>%
                    mutate(`Explorative Score` = percent(`Explorative Score`),
                           `Social Score` = percent(`Social Score`),
                           `Achievemental Score` = percent(`Achievemental Score`),
                           `Sensational Score` = percent(`Sensational Score`)) %>%
                    select(Game, `Release Date`, `GS Score`, ESRB, 2:5),
                  options = list(pageLength = 25)
    )
  })
}