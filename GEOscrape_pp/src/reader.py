# Command line should be in format: terms.txt tsvofscrape

class Reader:
    def __init__(self) -> None:
        print("Initiating the reader")
        import pandas as pd

    def pandas_read(file):
        """
        Open up a tab delimited GEOScrape for downstream filtering
        """
        # Pandas to open data frame of our listGEOData output
        df = pd.read_csv(file, sep = "\t")
        return(df)

    def open_terms(file):
        """
        Open up a \n delimited list of terms which you consider hits
        """
        with open(file, "r") as f:
            my_terms = f.readlines()
            return(my_terms)
