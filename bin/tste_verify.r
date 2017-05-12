#--Setting up
library(tidyverse)
library(scales)

#Read in triplet
triplet <- read_csv("../data/raw_survey/triplets_survey.csv", col_names=FALSE)

#Calculate observation number
obsNum <- dim(triplet)[1]

#Function for calculating the difference between distance 1 and 2
#distance 1: between the pair chosen in the survey (the similar pair)
distDif <- function(row, distMatrix) {
  distance1 <- distMatrix[row[1], row[2]]
  distance2 <- distMatrix[row[1], row[3]]
  distDif <- distance1 - distance2
}


#--Calculation
#Create lists to acommodate results
featureNum <- c(2:20, seq(25, 50, by=5))
tstes <- list()
distMatrices <- list()
errorRates <- list()
for (i in featureNum) {
  #Read in tste embedding
  tstes[[i]] <- read_csv(paste("../data/process/tste/tste_embedding_", i, ".csv", sep=""), col_names=FALSE)
  
  #Acquire distance matrices from tste embedding
  distMatrices[[i]] <- dist(tstes[[i]], method="euclidean") %>%
    as.matrix() %>%
    as.data.frame()
  
  #Acquire the two distances of each pair and Compute the difference 
  triplet[[paste("distDif", i, sep="_")]] <- apply(triplet, 1, distDif, distMatrix=distMatrices[[i]])
  
  #Compute error rates from the distance differences
  #positive = correct; negatve = error
  errorRates[[i]] <- dim(subset(triplet, triplet[[paste("distDif", i, sep="_")]] > 0))[1] / obsNum
}

#Remove nulls and transform back to vector
errorRates <- errorRates[!sapply(errorRates, is.null)] %>% unlist()


#--Plot and save
ggplot(data=NULL, mapping=aes(x=featureNum, y=errorRates)) +
  geom_line() +
  scale_y_continuous(labels=percent) +
  labs(title = "Error rate by number of feature",
       subtitle = "(Computed with Euclidean distance)",
       x = "Number of feature",
       y = "Error rate") +
  ggsave("../img/tste_verify.png")

