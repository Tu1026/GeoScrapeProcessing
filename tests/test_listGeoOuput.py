"""This module is used to test if the output from listGEO is compatible
with the program
"""
import pytest
import pandas as pd
import subprocess
from datetime import datetime


@pytest.fixture(scope='session')
def list_GEO_output() -> pd.DataFrame:
    """This fixture generates output from ListGEO
    to be used in tests
    """
    today = datetime.now().strftime("%Y.%m.%d")
    subprocess.call('$GEMMACMD listGEOData -u $GemmaUsername -p $GEMMAPASSWORD'
                    ' -output testListGeo.txt '
                    f'-date {today}', shell=True)
    yield pd.read_csv('testListGeo.txt', sep=',')
    subprocess.call('rm testListGeo.txt')


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
        list_GEO_output['Superseries']
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
