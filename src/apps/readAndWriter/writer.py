from datetime import datetime
import os
from apps.services import GoogleSheetsService
class Writer:

    @staticmethod
    def writeGEOScrapeToCsvs(resultsFrame, origFrame, sep, outPutDir, gService):
        print(f"Outputing the file in your selected location at {outPutDir}")
        currTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        nameForAllFrame = "Processed_GeoSrape_mainFrame" 
        nameForOnePlarformCuratableFrameArray = "(1.Ready for loading Arrays) Processed_GeoSrape_mainFrame" 
        nameForOnePlarformCuratableFrameRNA =  "(2.Ready for loading RNA-seq) Processed_GeoSrape_mainFrame"
        nameForMultiPlarformCuratableFrameArray = "(3. Check if you need to split platforms Arrays) Processed_GeoSrape_mainFrame"
        nameForMultiPlarformCuratableFrameRNA = "(4. Check if you need to split platforms RNA-seq) Processed_GeoSrape_mainFrame"
        nameForNonCuratedPlaform ="(5. Check if all platforms can be curated) Processed_GeoSrape_mainFrame" 
        nameForUnwantedFrame ="(Disgarded Experiments) Processed_GeoSrape_mainFrame"

        if gService:
            gService.createNewWorkSheetFromDf(nameForAllFrame, resultsFrame)
            gService.createNewWorkSheetFromDf(nameForOnePlarformCuratableFrameArray, OutputSheetsFormatting.filterOnePlarformCuratableFrameArray(origFrame, resultsFrame))
            gService.createNewWorkSheetFromDf(nameForOnePlarformCuratableFrameRNA, OutputSheetsFormatting.filterOnePlarformCuratableFrameRNASeq(origFrame, resultsFrame))
            gService.createNewWorkSheetFromDf(nameForMultiPlarformCuratableFrameArray, OutputSheetsFormatting.filterMultiArrayPlarformCuratableFrame(origFrame, resultsFrame))
            gService.createNewWorkSheetFromDf(nameForMultiPlarformCuratableFrameRNA, OutputSheetsFormatting.filterOnePlarformCuratableFrameRNASeq(origFrame, resultsFrame))
            gService.createNewWorkSheetFromDf(nameForNonCuratedPlaform, OutputSheetsFormatting.nonCuratedPlatFormFrame(origFrame, resultsFrame))
            gService.createNewWorkSheetFromDf(nameForUnwantedFrame, OutputSheetsFormatting.unwantedFrame(origFrame, resultsFrame))


        elif not gService:
            if sep == "\t":
                format="tsv"
            else:
                format="csv"
            ## Write main frame
            os.mkdir(os.path.join(outPutDir,currTime))
            resultsFrame.to_csv(os.path.join(outPutDir,f"{currTime}/{nameForAllFrame}.{format}"), sep = sep, index=False)
            OutputSheetsFormatting.filterOnePlarformCuratableFrameArray(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/{nameForOnePlarformCuratableFrameArray}.{format}"), sep = sep, index=False)
            OutputSheetsFormatting.filterOnePlarformCuratableFrameRNASeq(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/{nameForOnePlarformCuratableFrameRNA}.{format}"), sep = sep, index=False)
            OutputSheetsFormatting.filterMultiArrayPlarformCuratableFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/{nameForMultiPlarformCuratableFrameArray}.{format}"), sep = sep, index=False)
            OutputSheetsFormatting.filterMultiRNASeqPlarformCuratableFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/{nameForMultiPlarformCuratableFrameRNA}.{format}"), sep = sep, index=False)
            OutputSheetsFormatting.nonCuratedPlatFormFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/{nameForNonCuratedPlaform}.{format}"), sep = sep, index=False)
            OutputSheetsFormatting.unwantedFrame(origFrame, resultsFrame).to_csv(os.path.join(outPutDir,f"{currTime}/{nameForUnwantedFrame}.{format}"), sep = sep, index=False)




class OutputSheetsFormatting:
    @staticmethod
    def filterOnePlarformCuratableFrameArray(origDf, newDf):
        print("Preparing single array platform curatable list")
        columns = OutputSheetsFormatting._getFilterResultColumns(origDf,newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[~newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[newDf['Type'].str.contains("array")]
        return newDf

    @staticmethod
    def filterOnePlarformCuratableFrameRNASeq(origDf, newDf):
        print("Preparing single RNA seq platform curatable list")
        columns = OutputSheetsFormatting._getFilterResultColumns(origDf,newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[~newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[~newDf['Type'].str.contains("array")]
        return newDf
    
    @staticmethod
    def filterMultiArrayPlarformCuratableFrame(origDf, newDf):
        print("Preparing multiplatform curatable list")
        columns = OutputSheetsFormatting._getFilterResultColumns(origDf,newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf= newDf.loc[newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[newDf['Type'].str.contains("array")]
        return newDf
        
    @staticmethod
    def filterMultiRNASeqPlarformCuratableFrame(origDf, newDf):
        print("Preparing multiplatform curatable list")
        columns = OutputSheetsFormatting._getFilterResultColumns(origDf,newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[~newDf['Type'].str.contains("array")]
        return newDf 


    ## @TODO Alex's group by hitwords sheet
    @staticmethod
    def groupByHitWordsFrame(origDf, newDf):
        pass
        

    @staticmethod
    def nonCuratedPlatFormFrame(origDf, newDf):
        print("Preparing non-curated platform experiments list")
        columns = OutputSheetsFormatting._getFilterResultColumns(origDf,newDf)
        for column in columns:
            if column != "nonCuratedPlatofrms Filter Results":
                newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
            else:
                newDf = newDf.loc[newDf[column].str.startswith("(Failure)")]
        return newDf

    @staticmethod
    def unwantedFrame(origDf, newDf):
        print("Preparing a list of experiments that we cannot or do not want")
        columns = OutputSheetsFormatting._getFilterResultColumns(origDf,newDf)
        def searchFails(row):
            for column in columns:
                if column != "nonCuratedPlatofrms Filter Results":
                    if row[column].startswith("(Failure"):
                        return True
            return False
        newDf = newDf.loc[newDf.apply(searchFails, axis=1)]
        return newDf

    @staticmethod
    def _getFilterResultColumns(origDf, newDf):
        return newDf.columns.difference(origDf.columns).difference(["hitList"])