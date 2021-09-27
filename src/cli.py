from config import Config
import click
from apps.geoScrapeMainSwitch import GeoScrapeMainSwitch
##Builiding command line options. Cannot figure out how to modularize click options

version = 0.5
softwareName = "Post GEO Filter"
###Build Options
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

credentials_option = [click.option('-p','--password', help="GEMMA password"), 
click.option('-u','--username', required=True, help="GEMMA username")]

geoScrape_option = [click.option('-f', '--file', required=True, help="File that contains the GEOScrape"),
click.option('-o', '--outPutDir', default=Config.getOutPutDir(),help="Directory where you want to output the processed GEOscrape. Default at /docs/output_files"),
click.option('-s', '--sep', default="\t", help="Delimiter you want to use for the input and output file"),
click.option('-h', '--hitWordsFile', default= Config.getHitTermsFile(), help = "Location of the hitTerms file. Default at docs/input_files/terms.txt")]

@click.group()
def cli():
   pass

@cli.command("process")
@add_options(credentials_option)
def process(**kwargs):
    print("placeholder")

@cli.command("geoScrape")
@add_options(geoScrape_option)
def geoScrape(**kawargs):
    print("Running with the options and value")
    for key, value in kawargs.items():
        if key == "sep":
            value = f"{value}"
        print(f"--{key}:{value} ")
    geoScrapeSwitch = GeoScrapeMainSwitch(kawargs["file"], kawargs["outputdir"], kawargs["hitwordsfile"], kawargs["sep"])
    geoScrapeSwitch.filterAndOutputFile()

if __name__ == "__main__":
    print('\n')
    print(f'                                         {softwareName} version: {version} initiating')
    print("=================================================================================================================================")
    print('\n')
    cli()