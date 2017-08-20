library(shiny)

# Front end section --------------------------------------------------------
ui <- fluidPage(title = 'Game Experiential Topic',
                # Title panel + some CSS
                titlePanel(h1("Game Experiential Topic Comparison", style = "color:#888888")),   
                
                # Side bar
                sidebarLayout(
                  sidebarPanel(
                    textInput(inputId="searchText", label="", value=""),
                    actionButton(inputId="searchButton", label="search")
                  ),
                  
                  # Main panel
                  mainPanel(
                    DT::dataTableOutput(outputId="searchResult")
                  )
                )
)