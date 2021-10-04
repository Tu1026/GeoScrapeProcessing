from pathlib import Path
import os

class Config:

    @staticmethod
    def iniHitTermsFile(customPath):
        if customPath:
            ConfigVariables.HITTERMSFILE = customPath
        else: 
            ConfigVariables.HITTERMSFILE = os.path.join(ConfigVariables.PROJECTROOTDIR, "docs/input_files/terms.txt")

    @staticmethod
    def iniOutPutDir(customPath):
        if customPath:
           ConfigVariables.OUTPUTDIR = customPath 
        else:
            ConfigVariables.OUTPUTDIR = os.path.join(ConfigVariables.PROJECTROOTDIR, "docs/output_files")


    # ####For testing only
    # @staticmethod
    # def getTestGEOScrapeFile():
    #     return os.path.join(Config.getProjectRootDir(), "docs/input_files/GEOScrape.tsv") 

    @staticmethod
    def setThreads():
        os.environ['OPENBLAS_NUM_THREADS'] = "1"

    @staticmethod
    def getVersion():
        return "1.0"

    @staticmethod
    def getSoftwareName():
        return "Post GEOScrape Processing"


class ConfigVariables():
    PROJECTROOTDIR = Path(__file__).parent.parent
    HITTERMSFILE = None
    OUTPUTDIR = None
