import itertools
import pandas as pd
from datetime import datetime
import os
from config import ConfigVariables
import swifter
from apps.readAndWriter.reader import Reader


class Writer:

    @staticmethod
    def writeGEOScrapeToCsvs(resultsFrame, origFrame):
        outPutDir = ConfigVariables.OUTPUTDIR
        gService = ConfigVariables.GOOGLESERVICE
        sep = ConfigVariables.SEP
        print(f"Outputing the file in your selected location at {outPutDir}")

        currTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        nameForAllFrame = "Processed_GeoSrape_mainFrame"

        nameForOnePlarformCuratableFrameArray = "(1.Ready for loading Arrays) Processed_GeoSrape_mainFrame"

        nameForOnePlarformCuratableFrameRNA = "(2.Ready for loading RNA-seq) Processed_GeoSrape_mainFrame"

        nameForMultiPlarformCuratableFrameArray = "(3. Check if you need to split platforms Arrays) Processed_GeoSrape_mainFrame"

        nameForMultiPlarformCuratableFrameRNA = "(4. Check if you need to split platforms RNA-seq) Processed_GeoSrape_mainFrame"

        nameForDoubleCheckFrame = "(5. Double check these experiments, check the 'action' status for more info) Double_Check_Frame"

        nameForHitList = "(Experiments grouped by hitWords)"

        nameForUnwantedFrame = "(Discarded Experiments) Processed_GeoSrape_mainFrame"

        if gService:
            # [gService.createNewWorkSheetFromDf( for methodToWriteToGoogle in
            # dir(OutputSheetsFormatting) if not
            # methodToWriteToGoogle.startswith("__")]
            gService.createNewWorkSheetFromDf(
                nameForOnePlarformCuratableFrameArray,
                OutputSheetsFormatting.filterOnePlarformCuratableFrameArray(
                    origFrame,
                    resultsFrame))
            gService.createNewWorkSheetFromDf(
                nameForOnePlarformCuratableFrameRNA,
                OutputSheetsFormatting.filterOnePlarformCuratableFrameRNASeq(
                    origFrame,
                    resultsFrame))
            gService.createNewWorkSheetFromDf(
                nameForMultiPlarformCuratableFrameArray,
                OutputSheetsFormatting.filterMultiArrayPlarformCuratableFrame(
                    origFrame,
                    resultsFrame))
            gService.createNewWorkSheetFromDf(
                nameForMultiPlarformCuratableFrameRNA,
                OutputSheetsFormatting.filterMultiRNASeqPlarformCuratableFrame(
                    origFrame,
                    resultsFrame))
            gService.createNewWorkSheetFromDf(
                nameForDoubleCheckFrame,
                OutputSheetsFormatting.doubleCheckFrame(
                    origFrame,
                    resultsFrame))
            if not ConfigVariables.NOHITTERM:
                gService.createNewWorkSheetFromDf(
                    nameForHitList,
                    OutputSheetsFormatting.groupByHitWordsFrame(
                        origFrame, resultsFrame))
            gService.createNewWorkSheetFromDf(nameForAllFrame, resultsFrame)
            gService.createNewWorkSheetFromDf(
                nameForUnwantedFrame,
                OutputSheetsFormatting.unwantedFrame(
                    origFrame,
                    resultsFrame))

        elif not gService:
            if sep == "\t":
                format = "tsv"
            else:
                format = "csv"
            # Write main frame
            os.mkdir(os.path.join(outPutDir, currTime))
            OutputSheetsFormatting.filterOnePlarformCuratableFrameArray(
                origFrame,
                resultsFrame).to_csv(
                os.path.join(
                    outPutDir,
                    f"{currTime}/"
                    f"{nameForOnePlarformCuratableFrameArray}.{format}"),
                sep=sep,
                index=False)
            OutputSheetsFormatting.filterOnePlarformCuratableFrameRNASeq(
                origFrame,
                resultsFrame).to_csv(
                os.path.join(
                    outPutDir,
                    f"{currTime}/"
                    f"{nameForOnePlarformCuratableFrameRNA}.{format}"),
                sep=sep,
                index=False)
            OutputSheetsFormatting.filterMultiArrayPlarformCuratableFrame(
                origFrame,
                resultsFrame).to_csv(
                os.path.join(
                    outPutDir,
                    f"{currTime}/"
                    f"{nameForMultiPlarformCuratableFrameArray}.{format}"),
                sep=sep,
                index=False)
            OutputSheetsFormatting.filterMultiRNASeqPlarformCuratableFrame(
                origFrame,
                resultsFrame).to_csv(
                os.path.join(
                    outPutDir,
                    f"{currTime}/"
                    f"{nameForMultiPlarformCuratableFrameRNA}.{format}"),
                sep=sep,
                index=False)
            OutputSheetsFormatting.doubleCheckFrame(
                origFrame,
                resultsFrame).to_csv(
                os.path.join(
                    outPutDir,
                    f"{currTime}/{nameForDoubleCheckFrame}.{format}"),
                sep=sep,
                index=False)
            if not ConfigVariables.NOHITTERM:
                OutputSheetsFormatting.groupByHitWordsFrame(
                    origFrame,
                    resultsFrame).to_csv(
                    os.path.join(
                        outPutDir,
                        f"{currTime}/{nameForHitList}.{format}"),
                    sep=sep,
                    index=False)
            resultsFrame.to_csv(
                os.path.join(
                    outPutDir,
                    f"{currTime}/{nameForAllFrame}.{format}"),
                sep=sep,
                index=False)
            OutputSheetsFormatting.unwantedFrame(
                origFrame,
                resultsFrame).to_csv(
                os.path.join(
                    outPutDir,
                    f"{currTime}/{nameForUnwantedFrame}.{format}"),
                sep=sep,
                index=False)


class OutputSheetsFormatting:
    @staticmethod
    def filterOnePlarformCuratableFrameArray(origDf, newDf):
        print("Preparing single array platform curatable list")
        columns = OutputSheetsFormatting.__getFilterResultColumns(
            origDf, newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[~newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[newDf['Type'].str.contains("array")]
        return newDf

    @staticmethod
    def filterOnePlarformCuratableFrameRNASeq(origDf, newDf):
        print("Preparing single RNA seq platform curatable list")
        columns = OutputSheetsFormatting.__getFilterResultColumns(
            origDf, newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[~newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[~newDf['Type'].str.contains("array")]
        return newDf

    @staticmethod
    def filterMultiArrayPlarformCuratableFrame(origDf, newDf):
        print("Preparing multiplatform array curatable list")
        columns = OutputSheetsFormatting.__getFilterResultColumns(
            origDf, newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[newDf['Type'].str.contains("array")]
        return newDf

    @staticmethod
    def filterMultiRNASeqPlarformCuratableFrame(origDf, newDf):
        print("Preparing multiplatform RNA-seq curatable list")
        columns = OutputSheetsFormatting.__getFilterResultColumns(
            origDf, newDf)
        for column in columns:
            newDf = newDf.loc[newDf[column].str.startswith("(Success)")]
        newDf = newDf.loc[newDf['Platforms'].str.contains(";")]
        newDf = newDf.loc[~newDf['Type'].str.contains("array")]
        return newDf

    @staticmethod
    def groupByHitWordsFrame(_, newDf):
        print("Preparing the list that Alex "
              "wants (group experiments by hit words)")
        hitWordsDict = {}

        for hitFile in ConfigVariables.HITTERMSFILES:
            for word in Reader.read_terms(hitFile):
                hitWordsDict[word] = []
        for combTerm in Reader.read_combination_of_terms(ConfigVariables.HITTERMSFILES):
            hitWordsDict[combTerm] = []

        for row in newDf.itertuples():
            if row.hitList:
                for hit in row.hitList:
                    hitWordsDict[hit].append(row.Acc)
                # Check if a valid combination exists
                combinationKeys = ["+".join(keys) for keys in itertools.combinations(row.hitList, 2)]
                for combKey in combinationKeys:
                    if combKey in hitWordsDict:
                        hitWordsDict[combKey].append(row.Acc)
                        
        for key, val in hitWordsDict.items():
            hitWordsDict[key] = ";".join(val)
        return pd.DataFrame.from_dict(
            hitWordsDict, orient="index").reset_index()

    @staticmethod
    def doubleCheckFrame(origDf, newDf):
        print("Preparing a list that needs to be double checked for RNA"
              " type and platform curatability")
        columns = OutputSheetsFormatting.__getFilterResultColumns(
            origDf, newDf)
        doubleCheckColumns = {"RNA Filter Results":
                              "Check if the RNA type is what we don't support ",
                              "nonCuratedPlatforms Filter Results":
                              ("Check if the platform can be curated in GEMMA "
                               "Usually all Illumina are fine but "
                               "Ion Torrent or AB ARE not")}
        # Everything needs so succeed except RNA and platform filters
        for column in columns:
            if column in doubleCheckColumns.keys():
                pass
            else:
                newDf = newDf.loc[newDf[column].str.startswith("(Success)")]

        def getActionForProblem(row):
            result = []
            for column, action in doubleCheckColumns.items():
                if "(Failure)" in row[column]:
                    if column == "RNA Filter Results":
                        action = action + row[column].split(":")[1]
                    result.append(action)
            return ";".join(result)

        newDf['Action'] = newDf.swifter.allow_dask_on_strings(
            enable=True).apply(getActionForProblem, axis=1)
        newDf = newDf.loc[~(pd.isna(newDf['Action']) | (newDf['Action'] == ""))]

        return newDf

    @staticmethod
    def unwantedFrame(origDf, newDf):
        print("Preparing a list of experiments that we cannot or do not want")
        columns = OutputSheetsFormatting.__getFilterResultColumns(
            origDf, newDf)

        def searchFails(row):
            for column in columns:
                if (column == "nonCuratedPlatforms Filter Results"
                        or column == "RNA Filter Results"):
                    continue
                else:
                    if row[column].startswith("(Failure)"):
                        return True
            return False
        newDf = newDf.loc[newDf.apply(searchFails, axis=1)]
        return newDf

    @staticmethod
    def __getFilterResultColumns(origDf, newDf):
        return newDf.columns.difference(origDf.columns).difference(["hitList"])
