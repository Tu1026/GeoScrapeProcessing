"""This module is used to test if the output from listGEO is compatible
with the program
"""
import pytest
import pandas as pd
import subprocess
from datetime import datetime
import os
from pathlib import Path
import time


curdir = Path(__file__).parent


@pytest.fixture(scope='module')
def list_GEO_output() -> pd.DataFrame:
    """This fixture generates output from ListGEO
    to be used in tests
    """
    os.chdir(curdir)
    today = datetime.now().strftime("%Y.%m.%d")
    ps = subprocess.Popen([os.environ['GEMMACMD'], 'listGEOData', '-u',
                           os.environ['GemmaUsername'], '-p',
                           os.environ['GEMMAPASSWORD'], '-output',
                           'testListGeo.txt', '-date', today])
    time.sleep(10)
    yield pd.read_csv('testListGeo.txt', sep="\t")
    ps.wait()
    os.remove('testListGeo.txt')


def test_hitWordsFilter_compat(list_GEO_output):
    try:
        list_GEO_output['Title']
        list_GEO_output['Summary']
        list_GEO_output['MeSH']
        list_GEO_output['SampleTerms']
    except KeyError:
        pytest.fail('Failed because needed column not here')
    except Exception as e:
        pytest.fail(f'Failed because generic {e} invesitgate why')


def test_nonCuratedPlatFilter_compat(list_GEO_output):
    try:
        list_GEO_output['AllPlatformsInGemma']
    except KeyError:
        pytest.fail('Failed because needed column not here')
    except Exception as e:
        pytest.fail(f'Failed because generic {e} invesitgate why')


def test_rnaTypeFilter_compat(list_GEO_output):
    try:
        list_GEO_output['Title']
        list_GEO_output['Summary']
        list_GEO_output['MeSH']
        list_GEO_output['SampleTerms']
    except KeyError:
        pytest.fail('Failed because needed column not here')
    except Exception as e:
        pytest.fail(f'Failed because generic {e} invesitgate why')


def test_sampleSizeFiltercompat(list_GEO_output):
    try:
        list_GEO_output['NumSamples']
    except KeyError:
        pytest.fail('Failed because needed column not here')
    except Exception as e:
        pytest.fail(f'Failed because generic {e} invesitgate why')


def test_superSeriesFilter_compat(list_GEO_output):
    try:
        list_GEO_output['SuperSeries']
    except KeyError:
        pytest.fail('Failed because needed column not here')
    except Exception as e:
        pytest.fail(f'Failed because generic {e} invesitgate why')


def test_writerColumn_compat(list_GEO_output):
    try:
        list_GEO_output['Platforms']
        list_GEO_output['Type']
    except KeyError:
        pytest.fail('Failed because needed column not here')
    except Exception as e:
        pytest.fail(f'Failed because generic {e} invesitgate why')