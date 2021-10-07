# Command line should be in format: terms.txt tsvofscrape
import pandas as pd


class Reader:

    @staticmethod
    def pandas_read(file, sep="\t"):
        """
        Open up a tab delimited GEOScrape for downstream filtering
        """
        # Pandas to open data frame of our listGEOData output
        df = pd.read_csv(file, sep=sep, index_col=False)
        return(df)

    @staticmethod
    def read_terms(file):
        """
        Open up a \n delimited list of terms which you consider hits
        """
        with open(file, "r") as f:
            my_terms = f.read().splitlines()
            return(my_terms)
