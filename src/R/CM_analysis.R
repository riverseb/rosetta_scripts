library(fs)
args <- commandArgs(trailingOnly = FALSE)
dirList <- list.files("/Volumes/Groups/sherman-data/Daniel/CitL_CM/v2_CM") # creates list of files from specified directory
fastaList <- dirList[endsWith(dirList, ".fasta")] # filters dirList to just fasta files
sequences <- c()
scores <- c()
names <- c()
for (fasta in fastaList) { # loops over list of fasta files 
  x <- 1
  index <- substr(fasta, 6, 10) # gets the trial number from file name
  fastaLines <- readLines(paste("/Volumes/Groups/sherman-data/Daniel/CitL_CM/v2_CM/", fasta, sep = "")) # reads lines from fasta file
  looprange <- seq(2, length(fastaLines), 2) # sets range
  for (i in looprange) {
    if (!(fastaLines[i] %in% sequences)) {
      sequences <- c(sequences, fastaLines[i])
      name_score <- strsplit(fastaLines[i-1], split = " ")[[1]]
      name <- paste(name_score[1][1], index, sep = "")
      names <- c(names, name)
      scores <- c(scores, as.double(name_score[2][1]))
    } else {
      next
    }
  }
}

seq_df <- data.frame(names, scores, sequences)
