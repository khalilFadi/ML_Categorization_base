## app.R ##

# List of required packages
required_packages <- c("shiny", "shinydashboard", "DT", "tidyverse", "tm",
                       "tidytext", "RColorBrewer", "textstem", "topicmodels")

# Install and load packages
for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, dependencies = TRUE)
  }
  library(pkg, character.only = TRUE)
}

# Load Packages ####

library(shiny)
library(shinydashboard)
library(DT)
library(tidyverse) # Data Wrangling
library(tm) # Text formating
library(tidytext) # unnest_tokens function
library(RColorBrewer) #Add divergent pallets
library(textstem) # For Lemmatization
library(topicmodels) # Topic Modeling

#setwd('C:/Users/oia22/Box/REDA - Research, Evaluation & Data Analytics/Isaac/Text Analysis')
#setwd('/Users/isaacaguilar/Library/CloudStorage/Box-Box/REDA - Research, Evaluation & Data Analytics/Isaac/Text Analysis')

# LOAD DATA ---------------------------------------------------------------
# CSV file with all the comments
#file <- read.csv(file.choose(),header=TRUE)
file <- read.csv('preds.csv', header=TRUE)
file$id <- as.integer(row.names(file)) # Create id column

# Lexicon
nrc <- read.csv('nrc_lexicon.csv', header=TRUE)
#nrc <- get_sentiments("nrc")

# UI SECTION --------------------------------------------------------------
ui <- dashboardPage(
  dashboardHeader(title = "TEXT ANALYSIS"),
  dashboardSidebar(sidebarMenu(
    menuItem("Sentiment Analysis", tabName = "sa"),
    menuItem("Topic Modeling", tabName = "tm")
  )
  ),
  dashboardBody(
    tabItems(
      tabItem("sa",
              fluidPage(    
                
                # Give the page a title
                titlePanel("Sentiment Analysis"),
                
                fluidRow(
                  column(4,
                         # Check if 'state' column exists in 'file'
                         if ("state" %in% colnames(file)) {
                           selectInput("flt1",
                                       "state:",
                                       c("All",
                                         unique(as.character(file$state))))
                         } else {
                           if ("question" %in% colnames(file)) {
                             # Check if 'question' column exists in 'file'
                             selectInput("flt1",
                                         "Question:",
                                         c("All",
                                           unique(as.character(file$question))))
                           }
                         }),
                  
                  column(4,
                         # Check if 'Satisfaction' column exists in 'file'
                         if ("Satisfaction" %in% colnames(file)) {
                           sliderInput("score", "Satisfaction Score:",
                                       min = min(file$Satisfaction), max = max(file$Satisfaction),
                                       value = c(min(file$Satisfaction), max(file$Satisfaction)),
                                       step = 1)
                         }),
                  column(4,
                         selectInput("ch_type",
                                     "Graph Type:",
                                     c("Emotions", "Sentiments")))
                  
                ),
                
                # Display Sentiment Barplot
                fluidRow(column(12,
                                plotOutput("sentPlot"))),
                
                
                conditionalPanel(
                  condition = "input.ch_type == 'Sentiments'",
                  fluidRow(
                    column(6,
                           selectInput("sent",
                                       "Sentiment:",
                                       c("All", "negative", "neutral", "positive"))),
                    column(6,
                           numericInput("id_s",
                                        "Sentence id",
                                        value = 1))
                  )
                ),
                
                conditionalPanel(
                  condition = "input.ch_type == 'Emotions'",
                  fluidRow(
                    column(6,
                           selectInput("emt",
                                       "Emotions:",
                                       c("All", "negative", "sadness", "anger", "disgust", "fear", "neutral",
                                         "anticipation", "surprise", "trust", "joy", "positive")))#,
                    # column(6,
                    #        numericInput("id_s2",
                    #                     "Sentence id",
                    #                     value = 1))
                  )
                ),
                
                fluidRow(
                  column(12,
                         DT::dataTableOutput("sent_table"))#,
                  
                  # column(6,
                  #        # Display table lexicon table for a given sentence
                  #        DT::dataTableOutput("lexicon_table"))
                )
              )),
      
      tabItem("tm",
              fluidPage(
                # Give the page a title
                titlePanel("Topic Modeling"),

                fluidRow(
                  column(4,
                         # Check if 'state' column exists in 'file'
                         if ("state" %in% colnames(file)) {
                           selectInput("flt2",
                                       "state:",
                                       c("All",
                                         unique(as.character(file$state))))
                         } else {
                           if ("question" %in% colnames(file)) {
                             # Check if 'question' column exists in 'file'
                             selectInput("flt2",
                                         "Question:",
                                         c("All",
                                           unique(as.character(file$question))))
                           }
                         }),

                  column(4,
                         if ("Satisfaction" %in% colnames(file)) {
                         sliderInput("scr", "Satisfaction Score:",
                                     min = 1, max = 5,
                                     value = c(1,5))
                          }),
                  column(4,
                        numericInput("n_topics", "Enter number of Topics", value = 2, min = 0))
                ),

                DT::dataTableOutput("table")
              )
      )
    )
  )
)


# SERVER SECTION ----------------------------------------------------------
server <- function(input, output) {
  
  output$sentPlot <- renderPlot({
    data <- file
    
    #Score filtering
    if ("Satisfaction" %in% colnames(file)){
      data <- data %>% filter(Satisfaction >= as.numeric(input$score[1]) & Satisfaction <= as.numeric(input$score[2]))
    }
    
    if ("state" %in% colnames(file)){
      if (input$flt1 != "All") {
        data <- data %>% filter(state == input$flt1)
      }
    } else {
      if("question" %in% colnames(file)){
        if (input$flt1 != "All") {
          data <- data %>% filter(question == input$flt1)
        }
      }
    }
    
    if (input$ch_type == "Emotions"){
      count_df <- data.frame(table(data$emotion))
      count_df$Var1 <- factor(count_df$Var1, levels = c("negative", "sadness", "anger", "disgust", "fear","neutral",
                                                        "anticipation","surprise","trust", "joy", "positive"))
      # } else if (input$ch_type == "Emotions2"){
      #   count_df <- data.frame(table(data$emotion2))
      #   count_df$Var1 <- factor(count_df$Var1, levels = c("negative", "sadness", "anger", "disgust", "fear","neutral",
      #                                                     "anticipation","surprise","trust", "joy", "positive"))
    } else {
      count_df <- data.frame(table(data$sent))
      count_df$Var1 <- factor(count_df$Var1, levels = c("negative","neutral","positive"))
    }
    
    count_df <- count_df[order(count_df$Var1), ]
    
    # Dynamically set the title based on the selected state
    if (input$flt1 == "All") {
      title_text <- paste("Sentence", input$ch_type, "for All states")
    } else {
      title_text <- paste("Sentence", input$ch_type, "for", input$flt1)
    }
    
    if ("question" %in% colnames(file)) {
      # If 'question' column exists
      if (input$flt1 == "All") {
        title_text <- paste("Sentence", input$ch_type, "for All Questions")
      } else {
        title_text <- paste("Sentence", input$ch_type, "for", input$flt1)
      }
    } else {
      if ("state" %in% colnames(file)) {
        # If 'state' column exists
        if (input$flt1 == "All") {
          title_text <- paste("Sentence", input$ch_type, "for All states")
        } else {
          title_text <- paste("Sentence", input$ch_type, "for", input$flt1)
        }
      } else {
        # If neither 'question' nor 'state' column exists
        title_text <- "Sentiment Analysis of Text"  
      }
    }
    
    
    barplot(count_df$Freq, names.arg = count_df$Var1, 
            col = brewer.pal(11, "RdYlBu"), 
            main = title_text, 
            ylab = "Count")
  })
  
  output$sent_table <- DT::renderDataTable({
    data <- file
    
    # Score filtering
    if ("Satisfaction" %in% colnames(file)){
      data <- data %>% filter(Satisfaction >= as.numeric(input$score[1]) & Satisfaction <= as.numeric(input$score[2]))
    }
    
    # state Filtering
    if("state" %in% colnames(file)){
      if (input$flt1 != "All") {
        data <- data %>% filter(state == input$flt1)
      }
    } else {
      if("question" %in% colnames(file)){
        if (input$flt1 != "All") {
          data <- data %>% filter(question == input$flt1)
        }
      }
    }
    
    
    # FILTER FOR THOSE THAT THE SELECTED SENTIMENT IS > 0
    # Sentiment Filtering
    if (input$ch_type != 'Sentiments'){
      if (input$emt != "All"){
        data <- data %>% filter(emotion == input$emt)
      }
    } else {
      if (input$sent != "All"){
        data <- data %>% filter(sent == input$sent)
      }
    }
    
    data <- data %>% dplyr::select(id, text, sent, emotion)
    
    #show table
    datatable(data, options = list(pageLength = 10))
  })
  
  output$lexicon_table <- DT::renderDataTable({

    # Create a sample text
    if (input$ch_type != 'Sentiments'){
      text <- file %>% filter(id == input$id_s2) %>% pull(text)
    } else{
      text <- file %>% filter(id == input$id_s) %>% pull(text)
    }

    if (!is.null(text) || nchar(text) > 0){
      corpus_c <- Corpus(VectorSource(iconv(text, to="")))

      # Create DataFrame with all documents
      corpus_c <- tm_map(corpus_c, tolower)
      corpus_c <- tm_map(corpus_c, removePunctuation)
      corpus_c <- tm_map(corpus_c, removeNumbers)
      corpus_c <- tm_map(corpus_c, removeWords, stopwords("english"))
      corpus_c <- tm_map(corpus_c, stripWhitespace)
      corpus_c <- tm_map(corpus_c, lemmatize_strings)# Apply lemmatization to the corpus

      corpus_cdf <- data.frame(text = sapply(corpus_c, as.character), stringsAsFactors = FALSE)

      # Create a data frame with the text and document ID
      data <- data.frame(Document = seq_along(text), Text = corpus_cdf$text)

      # Tokenize the text
      tokens <- unnest_tokens(data, word, Text)

      # Get sentiment scores using NRC lexicon
      sentiment_scores <- tokens %>% inner_join(nrc)
    } else {
      sentiment_scores <- data.frame()
    }

    datatable(sentiment_scores, options = list(pageLength = 25))
  })
  
  # Topic MODELING
  output$table <- DT::renderDataTable({
    
    # Enter number of Topics
    num_topics <- input$n_topics
    
    data <- file
    
    if("Satisfaction" %in% colnames(file)){
      data <- data %>% filter(Satisfaction >= as.numeric(input$scr[1]) & Satisfaction <= as.numeric(input$scr[2]))
    }
    
    
    if("state" %in% colnames(file)){
      if (input$flt2 != 'All'){
        data <- data %>% filter(state == input$flt2)
      }
    } else {
      if ("question" %in% colnames(file)){
        if (input$flt2 != 'All'){
          data <- data %>% filter(question == input$flt2)
        }
      }
    }
  
    #Topic modeling
    corpus_c <- Corpus(VectorSource(iconv(data$text, to=""))) 
    corpus_c <- tm_map(corpus_c, tolower)
    corpus_c <- tm_map(corpus_c, removePunctuation)
    corpus_c <- tm_map(corpus_c, removeNumbers)
    corpus_c <- tm_map(corpus_c, removeWords, stopwords("english"))
    corpus_c <- tm_map(corpus_c, stripWhitespace)
    
    # Create a document-term matrix
    tdm_c <- DocumentTermMatrix(corpus_c)
    
    # Identify documents with no non-stopword terms
    empty_docs <- which(rowSums(as.matrix(tdm_c)) == 0)
    
    # Remove empty documents from the term-document matrix and corpus_df
    non_empty_tdm <- tdm_c[-empty_docs, ]
    
    # Fit the LDA model (Latent Dirichlet Allocation)
    lda_model_c <- LDA(non_empty_tdm, k = num_topics)

    # Show Terms in a table
    terms_df <- as.data.frame(terms(lda_model_c, 10))
    datatable(terms_df, options = list(pageLength = 10))
  })
}


# RUN SHINY APP -----------------------------------------------------------
shinyApp(ui, server)


