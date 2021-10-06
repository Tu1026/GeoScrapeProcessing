from pathlib import Path
import os

class Config:
    ##Main initializing method should take from click input to set variables
    @staticmethod
    def initializeProgram(kawargs):
        Config._iniHitTermsFile(kawargs["hitwordsfile"])
        Config._iniOutPutDir(kawargs["outputdir"])
        Config._setThreads()
        ##Check no overlapping flags
        if not kawargs['file'] and not kawargs['google']:
            exit("You need to at least use one of the -f or -g flag")


        ##-------------------------------------------------------------------------Below methods should be private and not callable
    @staticmethod
    def _iniHitTermsFile(customPath):
        if customPath:
            ConfigVariables.HITTERMSFILE = customPath
        else: 
            ConfigVariables.HITTERMSFILE = os.path.join(ConfigVariables.PROJECTROOTDIR, "docs/input_files/terms.txt")

    @staticmethod
    def _iniOutPutDir(customPath):
        if customPath:
           ConfigVariables.OUTPUTDIR = customPath 
        else:
            ConfigVariables.OUTPUTDIR = os.path.join(ConfigVariables.PROJECTROOTDIR, "docs/output_files")

    @staticmethod
    def _setThreads():
        os.environ['OPENBLAS_NUM_THREADS'] = "1"



    # ####For testing only
    # @staticmethod
    # def getTestGEOScrapeFile():
    #     return os.path.join(Config.getProjectRootDir(), "docs/input_files/GEOScrape.tsv") 

    @staticmethod
    def getVersion():
        return "1.1"

    @staticmethod
    def getSoftwareName():
        return "Post GEOScrape Processing"


class ConfigVariables():
    PROJECTROOTDIR = Path(__file__).parent.parent
    HITTERMSFILE = None
    OUTPUTDIR = None

