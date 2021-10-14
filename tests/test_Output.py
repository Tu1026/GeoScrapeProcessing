"""
This module makes sure that the output of the filters captures
all of the GSEs and nothing is left out
[Action]: Change the docs/input/test.csv file if the format has changed
"""
import subprocess
import pytest


@pytest.fixture
def runGEOProcessing():
    """Running GEOScrape command to generate test output from docs/input/test.csv
    """
    subprocess.call("cd ..")
    subprocess.call("source ")