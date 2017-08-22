"
------------------------------------------------------------
Initialization
------------------------------------------------------------
"
library(shiny)








"
------------------------------------------------------------
Frond end
------------------------------------------------------------
"
ui <- fluidPage(#--Header
                #CSS
                tags$head(tags$link(rel="stylesheet", type="text/css", href="main.css")),
  
  
                #--Set up title
                #Tab title
                title='Game Experiential Topic',
                
                #Displayed title
                titlePanel(h1("Game Experiential Topic Comparison")),   
                
                
                #--Decide layout
                sidebarLayout(
                  #Side bar                
                    sidebarPanel(
                    textInput(inputId="searchText", label="", value=""),
                    actionButton(inputId="searchButton", label="search"),
                    DT::dataTableOutput(outputId="searchResult")
                  ),
                  
                  #Main panel
                  mainPanel(
                    htmlOutput(outputId="mainHeader_1"),
                    DT::dataTableOutput(outputId="targetTitle"),
                    htmlOutput(outputId="mainHeader_2"),                    
                    DT::dataTableOutput(outputId="similarTitle")
                  )
                )

)