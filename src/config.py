from pathlib import Path
import os
from apps.services import GoogleSheetsService


class Config:
    # Main initializing method should take from click input to set variables
    @staticmethod
    def initializeProgram(kawargs):
        Config._setHitTermsFile(kawargs["hitwordsfile"])
        Config._setOutPutDir(kawargs["outputdir"])
        Config._setThreads()
        Config._setLoadFileLocation(kawargs['file'])
        Config._setSeperator(kawargs['sep'])
        Config._setGoogleService(kawargs['google'])
        Config._setUseHitTermOrNot(kawargs['noterm'])
        Config._printAllVariables(kawargs)
        Config._checkNoOverLappingFlags(kawargs['file'], kawargs['google'])
    # -------------------------Below methods should be private and not callable

    @staticmethod
    def _setHitTermsFile(customPath):
        if customPath:
            ConfigVariables.HITTERMSFILE = customPath
        else:
            ConfigVariables.HITTERMSFILE = os.path.join(
                ConfigVariables.PROJECTROOTDIR, "docs/input_files/terms.txt")

    @staticmethod
    def _setOutPutDir(customPath):
        if customPath:
            ConfigVariables.OUTPUTDIR = customPath
        else:
            ConfigVariables.OUTPUTDIR = os.path.join(
                ConfigVariables.PROJECTROOTDIR, "docs/output_files")

    @staticmethod
    def _setThreads():
        os.environ['OPENBLAS_NUM_THREADS'] = "32"

    @staticmethod
    def _setLoadFileLocation(fileLocation):
        ConfigVariables.FILELOCATION = fileLocation

    @staticmethod
    def _setUseHitTermOrNot(noHitTerm):
        ConfigVariables.NOHITTERM = noHitTerm

    @staticmethod
    def _setGoogleService(url):
        if url:
            ConfigVariables.GOOGLESERVICE = GoogleSheetsService(url)
        else:
            ConfigVariables.GOOGLESERVICE = None

    @staticmethod
    def _setSeperator(sep):
        ConfigVariables.SEP = sep

    @staticmethod
    def _checkNoOverLappingFlags(fileLocation, googleUrl):
        if not bool(fileLocation) ^ bool(googleUrl):
            exit("You need to at least use one"
                 "of the -f or -g flag but not both")

    @staticmethod
    def _printAllVariables(kawargs):
        # Check no overlapping flags
        print("Running with the options and value")
        for key, value in kawargs.items():
            if key == "sep":
                value = f"{value}"
            print(f"--{key}:{value} ")

    # ####For testing only
    # @staticmethod
    # def getTestGEOScrapeFile():
    # return os.path.join(Config.getProjectRootDir(),
    # "docs/input_files/GEOScrape.tsv")

    @staticmethod
    def getVersion():
        return "1.3"

    @staticmethod
    def getSoftwareName():
        return "Post GEOScrape Processing"


class ConfigVariables():
    PROJECTROOTDIR = Path(__file__).parent.parent
    HITTERMSFILE = None
    OUTPUTDIR = None
    FILELOCATION = None
    SEP = None
    GOOGLESERVICE = None
    NOHITTERM = None
