# The GEOscraping Pipeline

## Purpose

When a GEOscrape is performed, there are often false positives. This package
contains a pipeline that will help you remove some of these false positives 
(such as scRNA or lncRNA). The pipeline will also aid you in identifying 
needs to be done with each GSEid.

Unfortunatly, the pipeline is not fully automatic, as you will need to manually 
curate GSEs for relevance.

## Contents 

### Main
Contains the main scripts that you will use to run the pipeline.

### Results
Contains the output of the pipeline

## Usage
1) Clone this repository
2) Make the scripts Bash Executable. By running "chmod +x 1_html_scraping.R",
and "chmod +x 2_good_filtering.R"
3) Ensure that your GEOscrape file is within this directory
4) Run the first script of the pipeline on file by running:
  "./1_html_scraping.R <geoscrape_tsv>"
5) In the results folder there are 6 output files

lnc.txt: GSEs that are long-non-coding RNA
miRNA.txt: GSEs that are microarray
non_superseries.txt: GSEs that are not superseries
scRNA.txt: GSEs that are single cell experiments
processed_geoscrape.tsv: a TSV file containing the GSEids that should proceed
through the pipeline.

6) Open processed_geoscrape.tsv in a google sheets.
7) Curate GSEs according to the relevancy of the GSE titles
8) Place the GSE_ids that you've decided are good, within "good_titles.txt"
9) Run "./2_good_filtering.R" <processed_geoscrape.tsv> <good_titles.txt>
10) Properly curate the GSEs in the "results/curate_these_GSEs" folder within the results folder.
You can use "results/technology_type" to tell which GSEs you need to put
in the RNAseq pipeline and which can just go on the master curation list.


