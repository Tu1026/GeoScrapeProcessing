
# Install New packages

packages <- c(
              "tidyverse",
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


setwd("~/Projects/Pavlab_Curators/GEOscrapingPipeline") 

# Input a data frame of GSEids and clean it up

GSE_ids <- read.delim(file = "InputPipeline.txt",
                      header = FALSE, sep = "\n",
                      stringsAsFactors = FALSE)
clean_GSE_ids<- lapply(GSE_ids[,1],
                       function(gse) str_replace(pattern = "\\.[:digit:].?", replacement =  "", string = gse))
clean_GSE_ids <- lapply(clean_GSE_ids, 
                        function(gse) str_replace(pattern = " ", replacement =  "", string = gse))

# Remove duplicates
clean_GSE_ids[duplicated(clean_GSE_ids)]
clean_GSE_ids <- clean_GSE_ids[!duplicated(clean_GSE_ids)]



data_matrix <- matrix(,
                       nrow = length(clean_GSE_ids),
                       ncol = 5)
rownames(data_matrix) <- clean_GSE_ids
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

      # First parse for superseries information.
      if (any(str_detect(html_download,
                     pattern = "This SuperSeries is composed of the SubSeries listed below."))) { 
        message(paste(GSE_id, "Was identified as a SuperSeries"))
        output_vector[1] <- 1
      } else {
        output_vector[1] <- 0
      }
      
      if (any
          (str_detect(str_to_lower(html_download), pattern = (".*sc.?(rna|nucl).*|.*single.?(cell|nucleus|mito|neur).*") )))
      {
        message (paste(GSE_id, "Is likely single-cell"))
        output_vector[2] <- 1
      } else {
        output_vector[2] <- 0
      }
      
      if (any
         (str_detect(str_to_lower(html_download), pattern = (".*(lnc|linc).?rna.*|.*long.?non.*|.?long.?n.?c.*"))))
      {
      message (paste(GSE_id, "Is likely lnc"))
        output_vector[3] <- 1
      } else {
        output_vector[3] <- 0
      }

      
      if (any
          (str_detect(str_to_lower(html_download), pattern = (".*(mi|micro|micr).?rna.*"))))
      {
        message (paste(GSE_id, "Is likely microRNA"))
        output_vector[4] <- 1
      } else {
        output_vector[4] <- 0
      }
      
      output_vector[5] <- 0
      
      return(output_vector)

      
    },
    error = function(cond) {
      message(paste(cond, "at", GSE_id))
      output_vector[5] <- 1
          })
}
    

for (GSE_id in clean_GSE_ids){
  html_download <- download_html(GSE_id)
  new_matrix_row <- parse_GSE(html_download, GSE_id)
  data_matrix[GSE_id,] <-  new_matrix_row
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



#-------------------------------------------
# Saving
# ------------------------------------------

if (!dir.exists("results")) {
  dir.create("results")
}

saveRDS(non_superseries,
        file = "results/non_superseries.rds")

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
