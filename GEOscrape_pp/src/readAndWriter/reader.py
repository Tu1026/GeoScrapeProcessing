# Command line should be in format: terms.txt tsvofscrape
import pandas as pd

class Reader:
    def __init__(self) -> None:
        print("Initiating the reader")

    def pandas_read(self,file, sep):
        """
        Open up a tab delimited GEOScrape for downstream filtering
        """
        # Pandas to open data frame of our listGEOData output
        df = pd.read_csv(file, sep=sep)
        return(df)

    def open_terms(self,file):
        """
        Open up a \n delimited list of terms which you consider hits
        """
        with open(file, "r") as f:
            my_terms = f.readlines()
            return(my_terms)
