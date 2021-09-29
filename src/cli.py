from config import Config
import click
from apps.geoScrapeMainSwitch import GeoScrapeMainSwitch
import time
from apps.misc import formatTime


##Builiding command line options. Cannot figure out how to modularize click options


##Have to limit thread usage because frink blocks too many
Config.setThreads()

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



#/* Currently only using basic regex matching for file output from geoScrape command line. Could improve using Sphinx, SQL fulltext search,
# or elastic search for hitTemrs */
@cli.command("geoScrape")
@add_options(geoScrape_option)
def geoScrape(**kawargs):
    startTime = time.time()
    print("Running with the options and value")
    for key, value in kawargs.items():
        if key == "sep":
            value = f"{value}"
        print(f"--{key}:{value} ")
    geoScrapeSwitch = GeoScrapeMainSwitch(kawargs["file"], kawargs["outputdir"], kawargs["hitwordsfile"], kawargs["sep"])
    geoScrapeSwitch.filterAndOutputFile()
    endTime = time.time()
    print(f'Execution took {formatTime(startTime, endTime)}')

if __name__ == "__main__":
    print('\n')
    print(f'                                         {Config.getSoftwareName()} version: {Config.getVersion()} initiating')
    print("=================================================================================================================================")
    print('\n')
    cli()