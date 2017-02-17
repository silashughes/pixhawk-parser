filterCURR <- function(flightlog){
  logfile <- read.csv(flightlog,header = FALSE, stringsAsFactors=FALSE)
  currlog <- logfile[logfile$V1 %in% c("CURR"), ]
  categories <- c("type", "time", "throttle", "voltage", "current", "reg_volt","total_current")
  colnames(currlog) <- categories
  currlog <- currlog[,1:length(categories)]
  currlog[,categories[2:length(categories)]] <- as.numeric(unlist(currlog[,categories[2:length(categories)]]))
  filteredlog <- currlog[which(currlog$current>2000),]
  filteredlog$minutes <- filteredlog$time/60000000
  
  return(filteredlog)
}