# Filter for Superseries
# Filter for Bad Experiments

library(tidyverse)
library(stringr)
# setwd("GEOscrapingPipeline")

Term_Related_GSEs <- read.delim(file = "getBrainExperiments/Term_Related_GSEs.tsv", stringsAsFactors = FALSE)

Term_Related_GSEs <- Term_Related_GSEs %>%
  filter(Results == 'True' & SuperSeries == "False")

# Parse for sc info for a single GSE

main <- function(df_GSEs) { 
  for (n_row in 0:nrow(df_GSEs))
    aa <- lapply()
}
main(Term_Related_GSEs)

parse_for_negatives <- function(GSE_row) { 
  browser()
  GSE_row <- GSE_row[!is.na(GSE_row)]
  if (any(str_detect(str_to_lower(GSE_row), pattern = (".*sc.?(rna|nucl).*|.*single.?(cell|nucleus|mito|neur).*")))) 
      {
    message (paste(GSE_id, "Is likely single-cell"))
    GSE_row <- mutate(GSE_row, "scRNA" = "true")
    return(GSE_row)
    
  } else {
    GSE_row <- mutate(GSE_row, "scRNA" = "false")
    return(GSE_row)
  }
}

test1 <- lapply(Term_Related_GSEs,  FUN = parse_for_negatives)
  
stopifnot(FALSE)

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


