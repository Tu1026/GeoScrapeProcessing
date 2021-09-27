from pathlib import Path
import os

class Config:

    @staticmethod
    def getProjectRootDir():
        return Path(__file__).parent.parent

    @staticmethod
    def getHitTermsFile():
        return os.path.join(Config.getProjectRootDir(), "docs/input_files/terms.txt")

    @staticmethod
    def getOutPutDir():
        return os.path.join(Config.getProjectRootDir(), "docs/output_files")


    ####For testing only
    @staticmethod
    def getTestGEOScrapeFile():
        return os.path.join(Config.getProjectRootDir(), "docs/input_files/GEOScrape.tsv") 