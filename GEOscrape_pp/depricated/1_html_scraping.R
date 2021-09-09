#!/usr/bin/env Rscript

# Install New packages

packages <- c("tidyverse",
              "data.table",
              "rstudioapi",
              "rvest",
              "stringr",
              "assertthat")

new_packages <- setdiff(packages, installed.packages()[,"Package"])
install.packages(new_packages)

#--- 

library(rvest)
library(stringr)
library(assertthat)
library(tidyverse)
library(rstudioapi)

# Input a data frame of GSEids and clean it up

raw_geoscrape <- read.delim(file = "geoscrape.txt",
                      header = TRUE,
                      sep = "\t",
                      stringsAsFactors = FALSE)

clean_geoscrape <- distinct(raw_geoscrape, Acc, .keep_all = TRUE)
clean_geoscrape$Acc <- str_replace(clean_geoscrape$Acc,
                                   pattern = " ",
                                   replacement = "")
  
# Create data_matrix for tracking

data_matrix <- matrix(,
                       nrow = nrow(clean_geoscrape),
                       ncol = 5)
rownames(data_matrix) <- clean_geoscrape$Acc
colnames(data_matrix) <- c("Superseries", "scRNA", "lnc", "miRNA", "needs_attention")



#-------Callings

#1)download html for 1 gseid
#2)Parse for superseries for 1 gseid, if its superseries make it 1 in superseries
#3)Prase for scRNA, lnc, etc for 1 gseid. If its one of those, make it a 1 in its matrix


download_html <- function(GSE_id) {
  html_download <- 
    read_html(paste0("https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=",
                     GSE_id)) %>%
    html_nodes("td") %>%
    html_text()
  return(html_download) 
}


parse_GSE <- function(html_download, GSE_id) {
  tryCatch(
    {
      output_vector <- c()
      
      # Parse for sc info
      
      if (any
          (str_detect(str_to_lower(html_download), pattern = (".*sc.?(rna|nucl).*|.*single.?(cell|nucleus|mito|neur).*") )))
      {
        message (paste(GSE_id, "Is likely single-cell"))
        output_vector["scRNA"] <- 1
      } else {
        output_vector["scRNA"] <- 0
      }
      
      # Parse for lnc
      
      if (any
         (str_detect(str_to_lower(html_download), pattern = (".*(lnc|linc).?rna.*|.*long.?non.*|.?long.?n.?c.*"))))
      {
      message (paste(GSE_id, "Is likely lnc"))
        output_vector["lnc"] <- 1
      } else {
        output_vector["lnc"] <- 0
      }

      
      if (any
          (str_detect(str_to_lower(html_download), pattern = (".*(mi|micro|micr).?rna.*"))))
      {
        message (paste(GSE_id, "Is likely microRNA"))
        output_vector["miRNA"] <- 1
      } else {
        output_vector["miRNA"] <- 0
      }
      
      output_vector["needs_attention"] <- 0
      
      return(output_vector)

      
    },
    error = function(cond) {
      message(paste(cond, "at", GSE_id))
      output_vector["needs_attention"] <- 1
          })
}
    

for (n_row in 1:nrow(clean_geoscrape)){
  row <- clean_geoscrape[n_row,]
  GSE_id <- row[[1]]
  if (row$SuperSeries == "true") { 
    data_matrix[GSE_id, "Superseries"] = 1}
  else {
    data_matrix[GSE_id, "Superseries"] = 0}
  
  html_download <- download_html(GSE_id)
  
  output_vector <- parse_GSE(html_download, GSE_id)

  data_matrix[GSE_id, 2:5] <-  output_vector
  message("")
}


#-------------------------------------------
# Filtering the data_matrix
# ------------------------------------------

superseries <- data_matrix [data_matrix[, "Superseries"] == 1,]

non_superseries <- data_matrix [data_matrix[, "Superseries"] != 1,]

scRNA <- non_superseries [ non_superseries [, "scRNA"] == 1,]

lnc <- non_superseries [ non_superseries [, "lnc"] == 1,]

miRNA <- non_superseries [ non_superseries [, "miRNA"] == 1,]

unknown_error <- non_superseries [ non_superseries [, "needs_attention"] == 1,]


main_pipe_output <- non_superseries[ non_superseries [ ,"scRNA"]==0 &
                                       non_superseries[ , "lnc"] == 0 &
                                       non_superseries[ ,"miRNA"] == 0 &
                                       non_superseries[ , "needs_attention"] == 0, ]

processed_geoscrape <- clean_geoscrape %>%
  filter(clean_geoscrape$Acc %in% rownames(main_pipe_output))

#-------------------------------------------
# Saving
# ------------------------------------------

if (!dir.exists("results")) {
  dir.create("results")
}

write_delim(x = data.frame(rownames(non_superseries)),
            file = "results/non_superseries.txt",
            col_names = FALSE)

write_delim(x = data.frame(rownames(scRNA)),
            file = "results/scRNA.txt",
            col_names = FALSE)


write_delim(x = data.frame(rownames(lnc)),
            file = "results/lnc.txt",
            col_names = FALSE)


write_delim(x = data.frame(rownames(miRNA)),
            file = "results/miRNA.txt",
            col_names = FALSE)


write_delim(x = data.frame(rownames(unknown_error)),
            file = "results/unknown_error.txt",
            col_names = FALSE)

write_delim(x = processed_geoscrape,
            file = "results/processed_geoscrape.tsv",
            delim = "\t",
            col_names = TRUE)
