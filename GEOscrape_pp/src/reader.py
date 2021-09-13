# Command line should be in format: terms.txt tsvofscrape

def open_geoscrape(geoscrape):
    """
    Open up a tab delimited GEOScrape for downstream filtering
    """
    # Pandas to open data frame of our listGEOData output
    df = pd.read_csv(geoscrape, sep = "\t")
    return(df)

def open_terms(terms):
    """
    Open up a \n delimited list of terms which you consider hits
    """
    with open(terms, "r") as reader:
        my_terms = reader.readlines()
        return(my_terms)
