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
                titlePanel(HTML('<h3>Game Experiential Topic Comparison</h3>
                                <p id="authorship">Chih-Yu Chiang • chihyuchiang@uchicago.edu</p>')),
                
                
                #--Decide primary layout
                sidebarLayout(
                  #Side bar                
                  sidebarPanel(
                    h3("Instruction"),
                    p("(Please give the app 10 seconds to initialize)"),
                    p("The table is not ordered by default (DataTables orders a table by its first column by default);
                      Ordered columns are not highlighted by default (the DataTables option orderClasses is changed from TRUE to FALSE);
                      Numeric columns are always aligned to the right, since it rarely makes sense for numbers to be aligned to the left;
                      The option autoWidth is set to FALSE by default, so that DataTables does not calculate and put hard-coded width values on the table columns;"),
                    textInput(inputId="searchText", label="", value=""),
                    actionButton(inputId="searchButton", label="search"),
                    DT::dataTableOutput(outputId="searchResult")
                  ),
                  
                  #Main panel
                  mainPanel(
                    h3("Target Title"),
                    DT::dataTableOutput(outputId="targetTitle"),
                    br(), hr(),
                    h3("Similar Titles"),                    
                    DT::dataTableOutput(outputId="similarTitle"),
                    br(), hr(),                   
                    h3("Dominant Features"), 
                    DT::dataTableOutput(outputId="dominantFeature"),
                    br(), hr(),
                    h3("Distingusishing Features"),
                    h4("Strong"),
                    DT::dataTableOutput(outputId="dStrongFeature"),
                    br(),
                    h4("Weak"),
                    DT::dataTableOutput(outputId="dWeakFeature")
                  )
                )
)