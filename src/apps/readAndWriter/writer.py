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
        OutputSheetsFormatting.filterOnePlarformCuratableFrameArray(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(1.Ready for loading Arrays) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.filterOnePlarformCuratableFrameRNASeq(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(2.Ready for loading RNA-seq) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.filterMultiArrayPlarformCuratableFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(3. Check if you need to split platforms Arrays) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.filterMultiRNASeqPlarformCuratableFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(4. Check if you need to split platforms RNA-seq) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.nonCuratedPlatFormFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(5. Check if all platforms can be curated) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)
        OutputSheetsFormatting.unwantedFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/(Disgarded Experiments) Processed_GeoSrape_mainFrame.{format}"), sep = sep, index=False)




class OutputSheetsFormatting:
    @staticmethod
    def filterOnePlarformCuratableFrameArray(origDf, newDf):
        print("Preparing single array platform curatable list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[~newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[newDf['Type'].str.contains("array")]
        return newDf

    @staticmethod
    def filterOnePlarformCuratableFrameRNASeq(origDf, newDf):
        print("Preparing single RNA seq platform curatable list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[~newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[~newDf['Type'].str.contains("array")]
        return newDf
    
    @staticmethod
    def filterMultiArrayPlarformCuratableFrame(origDf, newDf):
        print("Preparing multiplatform curatable list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf= newDf.loc[newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[newDf['Type'].str.contains("array")]
        return newDf
        
    @staticmethod
    def filterMultiRNASeqPlarformCuratableFrame(origDf, newDf):
        print("Preparing multiplatform curatable list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[~newDf['Type'].str.contains("array")]
        return newDf 


    @staticmethod
    def groupByHitWordsFrame(origDf, newDf):
        pass
        

    @staticmethod
    def nonCuratedPlatFormFrame(origDf, newDf):
        print("Preparing non-curated platform experiments list")
        columns = newDf.columns.difference(origDf.columns)
        for column in columns:
            if column != "nonCuratedPlatofrms Filter Results":
                newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
            else:
                newDf = newDf.loc[newDf[column].str.startswith("(Failure)")]
        return newDf

    @staticmethod
    def unwantedFrame(origDf, newDf):
        print("Preparing a list of experiments that we cannot or do not want")
        columns = newDf.columns.difference(origDf.columns)
        def searchFails(row):
            for column in columns:
                if column != "nonCuratedPlatofrms Filter Results":
                    if row[column].startswith("(Failure"):
                        return True
            return False
        newDf = newDf.loc[newDf.apply(searchFails, axis=1)]
        return newDf

