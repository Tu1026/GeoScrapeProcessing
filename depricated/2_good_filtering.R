#!/usr/bin/env Rscript


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


#----------- Load processed geoscrape from prev script

processed_geoscrape <- read.delim(file = "results/processed_geoscrape.tsv",
                              sep = "\t",
                              header = TRUE,
                              stringsAsFactors = FALSE)

#----------- Load GSEs with relevant title/keyword hits as df

GSE_ids <- read.delim(file = "good_titles.txt",
                      sep = "\t",
                      header = FALSE,
                      stringsAsFactors = FALSE)
# --- Clean GSE_ids

GSE_ids <- GSE_ids %>%
  distinct(GSE_ids[1], .keep_all = TRUE)

GSE_ids[1] <- str_replace(GSE_ids[[1]],
                                   pattern = " ",
                                   replacement = "")


# ---------- select only the geoscraped GSEs with good titles

good_geoscrape <- filter(processed_geoscrape, Acc %in% GSE_ids[[1]])

#-------------------------------------------
# Filtering the data_matrix
# ------------------------------------------

affymetrix <- filter(good_geoscrape, Affy == "true")

good_geoscrape$Platforms <- str_split(good_geoscrape$Platforms, ";")
bool <- c()
for (element in good_geoscrape$Platforms) {
  if (length(element) > 1) {
    bool <- append(bool, TRUE)
  } else {
    bool <- append(bool, FALSE)
  }
}
multi <- good_geoscrape[bool,]

platform_not_in_gemma <- filter(good_geoscrape,
                          AllPlatformsInGemma == "false")

normal_GSEs <- good_geoscrape %>%
  filter(Affy == "false" &
           AllPlatformsInGemma == "true" &
           !(Acc %in% multi$Acc))

RNAseq <- good_geoscrape %>%
  filter(str_detect(string = good_geoscrape$Type,
                    pattern = "Expression profiling by high throughput sequencing"))

array <- good_geoscrape %>%
  filter(str_detect(string = good_geoscrape$Type,
                    pattern = "Expression profiling by array"))

#-------------------------------------------
# Saving
# ------------------------------------------


if (!dir.exists("results/curate_these_GSEs")) {
  dir.create(path = "results/curate_these_GSEs")
  }

write_delim(x = multi["Acc"],
            file = "results/curate_these_GSEs/multiplatform.txt",
            col_names = FALSE)

write_delim(x = platform_not_in_gemma["Acc"],
            file = "results/curate_these_GSEs/platforms_not_in_Gemma.txt",
            col_names = FALSE)

write_delim(x = affymetrix["Acc"],
            file = "results/curate_these_GSEs/affymetrix.txt",
            col_names = FALSE)

write_delim(x = normal_GSEs["Acc"],
            file = "results/curate_these_GSEs/normal_GSEs.txt",
            col_names = FALSE)

if (!dir.exists("results/technology_type")) {
  dir.create(path = "results/technology_type")
}

write_delim(x = RNAseq["Acc"],
            file = "results/technology_type/RNAseq.txt",
            col_names = FALSE)

write_delim(x = array["Acc"],
            file = "results/technology_type/array.txt",
            col_names = FALSE)


