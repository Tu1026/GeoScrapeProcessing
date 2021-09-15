import click
import pandas as pd
from src import Reader
from src.filters import RNATypeFilter
##Builiding command line options. Cannot figure out how to modularize click options

version = 0.01
softwareName = "Post GEO Filter"

def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

credentials_option = [click.option('-p','--password', help="GEMMA password"), 
click.option('-u','--username', required=True, help="GEMMA username")]

@click.group()
def cli():
   pass

@cli.command("process")
@add_options(credentials_option)
def process(**kwargs):
    print("placeholder")

@cli.command("test")
def test(**kawargs):
    newReader = Reader()
    df = newReader.pandas_read("/home/wlinshuan/R/GEOscrape_post_processing/GEOscrape_pp/src/GEOSrape.tsv")
    filter = RNATypeFilter(df)
    filter.filterTerms()
    frame = filter.returnFrame()
    frame.to_csv("test.csv")



if __name__ == "__main__":
    print('\n')
    print(f'                                         {softwareName} version: {version} initiating')
    print("=================================================================================================================================")
    print('\n')
    cli()