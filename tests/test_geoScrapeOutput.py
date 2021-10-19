"""
This module makes sure that the output of the filters captures
all of the GSEs and nothing is left out
[Action]: Change the docs/input/test.csv file if the format has changed
"""
import os
import subprocess
import pytest
import re
import pandas as pd
from pathlib import Path
import shutil


curdir = Path(__file__).parent


@pytest.fixture(scope="module")
def runGEOProcessing():
    """Running GEOScrape command to generate test output from docs/input/test.csv
    """
    os.chdir(curdir.parent)
    subprocess.run(["python", "src/cli.py", "geoScrape", "-f",
                    "tests/docs/input/test.tsv", "-o",
                    "tests/docs/output"])
    os.chdir(curdir)
    subprocess.run(["ls", "docs/output"])
    yield
    for root, dirs, files in os.walk('tests/docs/output'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


@pytest.fixture(scope="module")
def getRelevantFiles(runGEOProcessing):
    os.chdir(curdir)
    testOutPutLocation = "docs/output"
    needCheckFiles = []
    for (dirpath, dirnames, filenames) in os.walk(testOutPutLocation):
        for file in filenames:
            # Get only GSEs from all the processed frames / disregard frame
            if re.match("^\(\\d", file) or re.match("^\(Dis", file):
                needCheckFiles.append(file)
        if re.search("\\d+$", dirpath):
            testOutPutLocation = dirpath
    return [os.path.join(testOutPutLocation, file) for file in needCheckFiles]


def test_no_GSE_left_out(getRelevantFiles):
    """This makes sure that no GSEs are left out and they are all captured
    """
    mainSet = set(pd.read_csv("docs/input/test.tsv", sep="\t").iloc[:, 0])
    for processedFile in getRelevantFiles:
        mainSet = mainSet.difference(set(pd.read_csv(processedFile,
                                         sep="\t").iloc[:, 0]))
    # Make sure all the GSEs are in the original is in all processed frame
    assert not mainSet


def test_no_extra_GSE(getRelevantFiles):
    """This makes sure that a single GSE does not appear twice in a frame
    """
    iniSet = set()
    for processedFile in getRelevantFiles:
        tempSet = set(pd.read_csv(processedFile, sep="\t").iloc[:, 0])
        if iniSet.isdisjoint(tempSet):
            iniSet |= tempSet
        else:
            pytest.fail("Some GSEs exist in more than one output sheet!"
                        "Double check what is going on."
                        f"failed at {processedFile}")


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """Cleanup a testing directory once we are finished."""
    for root, dirs, files in os.walk('tests/docs/output'):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

