#----------Install New packages
if (!("devtools" %in% installed.packages())) {
  install.packages("devtools")
}

library(devtools)


packages <- c(
  "rentrez",
  "tidyverse",
  "gemmaAPI")

new_packages <- setdiff(packages, installed.packages()[,"Package"])
install.packages(new_packages)

lapply(as.list(packages), library, character.only = TRUE)


#----------- Load non_superseries.txt from results folder

non_superseries <- read.delim(file = "results/non_superseries.txt",
                              sep = "\t",
                              header = FALSE)

# ----------- Clean up our GSE input

# Remove splits and empty spaces
non_superseries<- lapply(non_superseries[,1],
                       function(gse) str_replace(pattern = "\\.[:digit:].?", replacement =  "", string = gse))
non_superseries <- lapply(non_superseries, 
                        function(gse) str_replace(pattern = " ", replacement =  "", string = gse))
# Remove duplicates
non_superseries <- non_superseries[!duplicated(non_superseries)]


# Create data matrix for tracking
my_colnames <- c("Taxa",
                 "Num_Platforms",
                 "Platforms_Curated",
                 "Affymetrix")

data_matrix <- matrix(,
                      nrow = length(non_superseries),
                      ncol = length(my_colnames))
rownames(data_matrix) <- non_superseries
colnames(data_matrix) <- my_colnames


# ---- Download list of all platforms 

#temporary-----------------
username <- "alexadrianhamazaki"
password <- "Doglukepotato3!"

setGemmaUser(username, password)
message('Attempted to login to gemma account')


# call Gemma API to retrieve all platforms we currently have
platforms <- allPlatforms(limit = 0)


delete_troubled <- function(platform) { 
  # Some columns were having problems binding, they arn't important so I'm going
  # to delete them
  platform[["lastTroubledEvent"]] <- NULL
  platform[["lastNeedsAttentionEvent"]] <-  NULL
  platform[["lastNoteUpdateEvent"]] <-  NULL
  
  return(platform)
  }

replace_nulls <- function(platform) {
  # input a list of a single platform from the gemma API call
  # Changes all null values into N/A
  
  for (index in names(platform)) {
    if (rlang::is_empty(platform[[index]])) { 
      platform[[index]] <-  "N/A"
    }
  }
  return(platform)
}

# In order to turn the of platforms into a data frame we must coerce into a vector
# However you cannot have null values within a vector. So we must first turn them
# into "N/A"

platforms <- lapply(platforms, delete_troubled)
platforms <- lapply(platforms, replace_nulls)

cols <- names(platforms[[1]])
rows <- names(platforms)

platforms <- bind_rows(platforms)

rownames(platforms) <- rows
colnames(platforms) <- cols


use_rentrez_API <- function (GSE_id, platforms) {
  # searches entrez database for a GSE_id
  # entrez_search will return 5 IDs. These IDs can be used with entrez_summary
  # in order to get meta_data about the IDs
  
  # The IDs follow an order: GSE, GPL(s), GSMs
  
  # The 1rst id should be the ID of the GSE_id within GEO
  # The 2nd id should be the ID of one of the platforms assosiated with the GSE
  # If there is only 1 platform, then the third id should be a GSM.
  # Otherwise, the next index(s) will be the remaining GPLs. Then a GSM id
  # will show up.

  # All Ids after the first GSM will be GSMs


  search_result <- entrez_search(db = "gds",
                                 term = paste0(GSE_id,"[ACCN]"),
                                 retmax = 5 )
  
  
  # Results summary gives us meta data for Ids
  result_summary <- entrez_summary(db = "gds",
                                   id = search_result$ids)
  

  
  # Check quickly to see if the GSE is a superseries. There shouldn't be any superseries being inputed into
  # this function. Filtering won't work properly
  if (result_summary[[1]]["summary"] == "This SuperSeries is composed of the SubSeries listed below.") {
    warning ( GSE_id, "was identified as a Superseries. It is likely that it will be improperly filtered. The superseries should be haveen filtered out in previous steps")
  }
  
  # output_vector will be for tracking what a specific GSE needs to do
  # output vector will be a row of the data matrix for each GSE
  
  output_vector <- c()
  
  # ---- Taxa
  # if there is a non relevant taxa, the output vector is 0
  # If any 1 of the taxa are relevant the output vector is 1
  
  if (any
      (str_detect(result_summary[[1]]["taxon"],
                  c("Homo sapiens",  "Mus musculus", "Rattus norvegicus")))) {

    output_vector["Taxa"] <- 1
    
  } else {
    
    output_vector["Taxa"] <- 0
    
  }
  

  
  # ---- Number of Platforms
  # If the number of platforms is greater than 1, then the output vector is 1
  # If the number of platforms is 1 then the output vector is 0
  
  if (length(result_summary[[1]]["gpl"]) > 1) {
    
    output_vector["gpl"] <- 1
    
  } else {
    
    output_vector["gpl"] <- 0
  
  }
  
  # ---- Platforms Curated yet or not
  # If the GSE's platform is in the good_platforms then the output vector is 1
  # If the GSE's platform is not in the good platforms then the output vector is 0
  # If the GSE is multiplaform, then it needs to be manually looked at. So the 
  # output_vector placeholder value will be 5
  
  good_platforms <- filter(platforms,
                           troubled == FALSE &
                             needsAttention == FALSE &
                             blackListed == FALSE)
  
  result_summary[[2]]["entrytype"] == "GPL"
  
  if (output_vector["gpl"] == 1 | result_summary[[2]]["entrytype"] != "GPL") {
    
    output_vector["Platforms_Curated"] <- 5
    
  } else if (result_summary[[2]]["accession"] %in% rownames(good_platforms)) {
    
          output_vector["Platforms_Curated"] <- 1
          
        } else { 
          
          output_vector["Platforms_Curated"] <- 0
          
        }
  
  # -------Affymetrix
  # if there is a problem, output vector is 5
  # if the platform is affymetrix, output vector is 1
  # otherwise, the output vector is 0

  
  if (result_summary[[2]]["entrytype"] != "GPL") {
    
    output_vector["Affymetrix"] <- 5
    
    }
  
  else if (str_detect(result_summary[[2]]["title"], pattern = ".?(A|a)ffymetrix.?")) {
    
    output_vector["Affymetrix"] <- 1
    
  } 
  else { 
    
    output_vector["Affymetrix"] <- 0
    
  }
  
  return(output_vector)
  
}
  

main_execution <- function(non_superseries, data_matrix, platforms) {
  for (GSE_id in non_superseries) {
    output_vector <- use_rentrez_API(GSE_id, platforms)
    data_matrix[GSE_id,] <- output_vector
  }
  return(data_matrix)
}

data_matrix <- main_execution(non_superseries, data_matrix, platforms)
  

#-------------------------------------------
# Filtering the data_matrix
# ------------------------------------------

non_taxa <- data_matrix[ data_matrix[ , "Taxa"] == 0 , ]

multiplatform <- data_matrix[ data_matrix[, "Num_Platforms"] == 1 , ]

non_curated_platform <-  data_matrix[ data_matrix[, "Platforms_Curated"] == 0 , ]

affymetrix <-  data_matrix[ data_matrix[, "Affymetrix"] == 1 , ]

# TODO . If affymetrix, and prob the others, only extract 1 row, then the rownames dissapear

unknown_error <-  data_matrix[ data_matrix[, "Platforms_Curated"] == 5 | data_matrix[, "Affymetrix"] == 5 , ]

normal_GSEs <- data_matrix[ 
                              data_matrix[ , "Taxa"] == 1 &
                              data_matrix[, "Num_Platforms"] == 0 &
                              data_matrix[, "Platforms_Curated"] == 1 &
                              data_matrix[, "Affymetrix"] == 0
                              , ]

stopifnot(nrow(data_matrix) == nrow(non_taxa) + 
            nrow(multiplatform) + 
            nrow(non_curated_platform) + 
            nrow(affymetrix) + 
            nrow(unknown_error)+
            nrow(normal_GSEs))

#-------------------------------------------
# Saving
# ------------------------------------------


if (!dir.exists("results/curate_these_GSEs")) {
  dir.create(path = "results/curate_these_GSEs")
  }

write_delim(x = data.frame(rownames(non_taxa)),
            file = "results/non_relevant_taxa.txt",
            col_names = FALSE)

write_delim(x = data.frame(rownames(multiplatform)),
            file = "results/curate_these_GSEs/multiplatform.txt",
            col_names = FALSE)

write_delim(x = data.frame(rownames(non_curated_platform)),
            file = "results/curate_these_GSEs/non_curated_platform.txt",
            col_names = FALSE)

write_delim(x = data.frame(rownames(affymetrix)),
            file = "results/curate_these_GSEs/affymetrix.txt",
            col_names = FALSE)

write_delim(x = data.frame(rownames(unknown_error)),
            file = "results/curate_these_GSEs/unknown_error.txt",
            col_names = FALSE)

write_delim(x = data.frame(rownames(normal_GSEs)),
            file = "results/curate_these_GSEs/normal_GSEs.txt",
            col_names = FALSE)


