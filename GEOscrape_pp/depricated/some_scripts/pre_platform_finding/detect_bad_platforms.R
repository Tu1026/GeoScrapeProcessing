#-----------------------------------
# PURPOSE: 
#-----------------------------------

# Given an output from listGEOData with the -platforms flag, filtering for only
# mouse, human and rat taxa, this script gives you a tsv file containing all of
# the geoplatforms that need to be blacklisted. 

# This script's purpose is to pre-emptively blacklist GEOplatforms that we know
# will not be usable for us. This will increase scrape efficiency, and decrease
# false positives

#-----------------------------------
# OUTPUT:
#-----------------------------------

# --- to_blacklist.tsv:
# A .tsv data.frame containing all of the GPLs that need to be blacklisted as 
# well as additional columns

# --- GPLs_to_blacklist.txt:
# A row delimited txt file containing ONLY the GPLs that need to be blacklisted


#-----------------------------------
# PACKAGES:
#-----------------------------------

library(tidyverse)
library(stringr)

#-----------------------------------
# LOAD INPUT:
#-----------------------------------

# the Input must be the output of ListGEOData with the -platforms flag for 
# only mouse, human, rat taxa. 

# If your input file is not "geoplatforms.txt" then you will need to change 
# This line to load whatever your input file is
geoplatforms <- read.delim("geoplatforms.txt") 


#-----------------------------------
# FILTERING:
#-----------------------------------

geoplatforms$Title <- str_to_lower(geoplatforms$Title)

nanostring <- geoplatforms %>%
  filter(str_detect(geoplatforms$Title, 
                    pattern = (".?nano.?string.?")))

micr <- geoplatforms %>%
  filter(str_detect(geoplatforms$Title, 
                    pattern = (".?(mi|micro).?rna")))

lnc <- geoplatforms %>%
  filter(str_detect(geoplatforms$Title, 
                    pattern = (".?(lnc|linc)|long.?non.?")))

prom <- geoplatforms %>%
  filter(str_detect(geoplatforms$Title, 
                    pattern = (".?prometh.?")))

tor <- geoplatforms %>%
  filter(str_detect(geoplatforms$Title, 
                    pattern = (".?ion.?torrent.?")))
AB <- geoplatforms %>%
  filter(str_detect(geoplatforms$Title, 
                    pattern = ("\\bab([:punct:]|[:space:]).?")))
                    
pac <- geoplatforms %>%
  filter(str_detect(geoplatforms$Title, 
                    pattern = ".?pac(bio|[:space:])"))

tech_levels <- levels(geoplatforms$TechType)
good_levels <- c("high-throughput sequencing",
                 "in situ oligonucleotide",
                 "oligonucleotide beads",
                 "spotted DNA/cDNA",
                 "spotted oligonucleotide")

bad_levels <- tech_levels [! ( tech_levels %in% good_levels) ]

bad_tech <- filter(geoplatforms, ! ( TechType %in% good_levels))


to_blacklist <- do.call(rbind, args = list(nanostring,
                                           micr,
                                           lnc,
                                           prom,
                                           tor,
                                           AB,
                                           pac,
                                           bad_tech))

#-----------------------------------
# WRITING OUTPUT:
#-----------------------------------
write_delim(x = to_blacklist,
            file = "to_blacklist.tsv",
            col_names = TRUE,
            delim = "\t")

write_delim(x = data.frame(to_blacklist$Acc),
            file = "GPLs_to_blacklist.txt",
            col_names = TRUE,
            delim = "\t")

