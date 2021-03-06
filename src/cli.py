from config import Config
import click
from apps.geoScrapeMainSwitch import GeoScrapeMainSwitch
import time
from apps.misc import formatTime
from apps.filters import HitWordsFilter


# Builiding command line options. Cannot figure out how to modularize
# click options


# Build Options into a nicely formatted list
def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


credentials_option = [
    click.option(
        '-p',
        '--password',
        help="GEMMA password"),
    click.option(
        '-u',
        '--username',
        required=True,
        help="GEMMA username")]

geoScrape_option = [
    click.option(
        '-f',
        '--file',
        help="File that contains the GEOScrape"
        ", if -g is used this is ignored"),
    click.option(
        '-o',
        '--outPutDir',
        default="",
        help="Directory where you want to output the processed GEOscrape."
        "Default at /docs/output_files, if -g is used this is ignored"),
    click.option(
        '-s',
        '--sep',
        default="\t",
        help="Delimiter you want to use for the input and output file"
        "(Only use this with -f option"),
    click.option(
        '-h',
        '--hitWordsFile',
        default="",
        help="Location of the hitTerms file."
        "Default at docs/input_files/terms.txt. Can take comma-delimited files "
        "Where the program will hit a permutation of all terms in all files"),
    click.option(
        '-g',
        '--google',
        default="",
        help="Enter the url of your google spreadsheet if you want to read "
        "and write your results to google sheets "
        "(make sure the output of geoScrape is the 'first' sheet"),
    click.option(
        '-n',
        '--noTerm',
        is_flag=True,
        help="Use this flag to filter experiments without using terms")
        ]


@click.group()
def cli():
    pass


@cli.command("process")
@add_options(credentials_option)
def process(**kwargs):
    print("placeholder")


# /* Currently only using basic regex matching for file output
# from geoScrape command line. Could improve using Sphinx, SQL fulltext search,
# or elastic search for hitTemrs */
@cli.command("geoScrape")
@add_options(geoScrape_option)
def geoScrape(**kawargs):

    # Have to initialize value this ungly way because the hash is different
    # using feature flag and comparison will not work
    if kawargs['noterm']:
        kawargs['noterm'] = HitWordsFilter

    Config.initializeProgram(kawargs)
    # Start running the application
    startTime = time.time()
    geoScrapeSwitch = GeoScrapeMainSwitch()
    geoScrapeSwitch.filterAndOutputFile()
    endTime = time.time()
    print(f'Execution took {formatTime(startTime, endTime)}')


if __name__ == "__main__":
    print('\n')
    print(
        f'                                         {Config.getSoftwareName()}'
        f' version: {Config.getVersion()} initiating')
    print("=============================================================="
          "========================================"
          "===========================")
    print('\n')
    cli()
