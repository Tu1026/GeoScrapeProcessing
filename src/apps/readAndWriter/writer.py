from datetime import datetime
import os
import re
class Writer:

    @staticmethod
    def writeGEOScrapeToCsvs(resultsFrame, origFrame, sep, outPutDir):
        print(f"Outputing the file in your selected location at {outPutDir}")
        currTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        if sep == "\t":
            format="tsv"
        else:
            format="csv"
        ## Write main frame
        os.mkdir(os.path.join(outPutDir,currTime))
        resultsFrame.to_csv(os.path.join(outPutDir,f"{currTime}/Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.filterOnePlarformCuratableFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(1.Ready for loading) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.filterMultiPlarformCuratableFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(2. Check if you need to split platforms) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.nonCuratedPlatFormFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(3. Check if all platforms can be curated) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.unwantedFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(Disgarded Experiments) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)




class OutputSheetsFormatting:
    @staticmethod
    def filterOnePlarformCuratableFrame(origDf, newDf):
        print("Preparing single platform curatable list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf.loc[~newDf['Platforms'].str.contains(";")]
        return newDf

    @staticmethod
    def filterMultiPlarformCuratableFrame(origDf, newDf):
        print("Preparing multiplatform curatable list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf.loc[newDf['Platforms'].str.contains(";")]
        return newDf 

    @staticmethod
    def groupByHitWordsFrame(origDf, newDf):
        pass
        

    @staticmethod
    def nonCuratedPlatFormFrame(origDf, newDf):
        print("Preparing non-curated platform experiments list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            if column != "nonCuratedPlatforms":
                newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
            else:
                newDf = newDf.loc[newDf[column].str.startswith("(Failure)")]
        return newDf

    @staticmethod
    def unwantedFrame(origDf, newDf):
        print("Preparing a list of experiments that we cannot or do not want")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            if column != "nonCuratedPlatforms":
                newDf = newDf.loc[newDf[column].str.startswith("(Failure)")]
        return newDf

