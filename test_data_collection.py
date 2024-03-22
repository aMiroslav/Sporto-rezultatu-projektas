import pytest
import requests_mock
import pandas as pd
from data_collection import (KrepsinioKlubuRinkiklis, FutboloKlubuRinkiklis, GautiPuslapi)

# 1
@pytest.fixture
def fiktyvi_eurolygos_data():
    return [
        ['1', 'Real Madrid', '25', '20', '5', '10', '2', '85', '80', '5', '2', '4'],
        ['2', 'Barcelona', '25', '19', '6', '11', '1', '80', '75', '5', '2', '3'],
    ]

mock_html = """
<html>
<head><title>Sample Page</title></head>
<body>
<table class="stats_01">
  <tr><td>1</td><td>Real Madrid</td><td>25</td><td>20</td><td>5</td><td>10</td><td>2</td><td>85</td>
  <td>80</td><td>5</td><td>2</td><td>4</td></tr>
  <tr><td>2</td><td>Barcelona</td><td>25</td><td>19</td><td>6</td><td>11</td><td>1</td><td>80</td>
  <td>75</td><td>5</td><td>2</td><td>3</td></tr>
</table>
</body>
</html>"""

def test_krepsinio_klubu_rinkiklis(fiktyvi_eurolygos_data):
    test_url = 'https://www.basketnews.lt/lygos/25-eurolyga/lenteles.html'
    expected_response = [
        ['1', 'Real Madrid', '25', '20', '5', '10', '2', '85', '80', '5', '2', '4'],
        ['2', 'Barcelona', '25', '19', '6', '11', '1', '80', '75', '5', '2', '3'],
    ]
    with requests_mock.Mocker() as m:
        m.get(test_url, text=mock_html)
        result = KrepsinioKlubuRinkiklis().eurolygos_duomenu_rinkimas_bendras()
        assert result == expected_response

# 2
@pytest.fixture
def fiktyvi_alyga_data():
    return [
        ['2', 'Vilniaus „Žalgiris“ ', '4', '2', '2', '0', '2', '0', '+2', '8'],
        ['6', 'Marijampolės „Sūduva“', '4', '1', '2', '1', '4', '4', '0', '5'],
    ]

mock_html = """
<html>
<head><title>Sample Page</title></head>
<body>
<table class="table01">
  <tr><td>2</td><td>Vilniaus „Žalgiris“</td><td>4</td><td>2</td><td>2</td><td>0</td><td>2</td><td>0</td><td>+2</td><td>8</td></tr>
  <tr><td>6</td><td>Marijampolės „Sūduva“</td><td>4</td><td>1</td><td>2</td><td>1</td><td>4</td><td>4</td><td>0</td><td>5</td></tr>
</table>
</body>
</html>"""

def test_futbolo_klubu_rinkiklis(fiktyvi_alyga_data):
    test_url = 'https://alyga.lt/turnyrine-lentele/1'
    expected_response = [
        ['2', 'Vilniaus „Žalgiris“', '4', '2', '2', '0', '2', '0', '+2', '8'],
        ['6', 'Marijampolės „Sūduva“', '4', '1', '2', '1', '4', '4', '0', '5'],
    ]
    with requests_mock.Mocker() as m:
        m.get(test_url, text=mock_html)
        result = FutboloKlubuRinkiklis().futbolo_info()
        assert result == expected_response

# 3

mock_html = """
<html>
<head>
<title>Fiktyvus puslapis</title>
</head>
<body>
<h1>Fiktyvaus puslapio turinys</h1>
</body>
</html>"""


def test_gauti_puslapi():
    test_url = 'https://neratokiourl.lt'
    laukiamas_puslapio_turinys = 'Fiktyvaus puslapio turinys'

    with requests_mock.Mocker() as m:
        m.get(test_url, text=mock_html)
        soup = GautiPuslapi.gauti_is_url(test_url)
        turinys = soup.find('h1').text.strip() if soup else None
        assert turinys == laukiamas_puslapio_turinys

# 4
@pytest.fixture
def krepsinio_klubu_rinkiklis():
    return KrepsinioKlubuRinkiklis()

def test_sukurti_df_duomenys_gauti(krepsinio_klubu_rinkiklis):
    krepsinio_data = [
        ['1', 'Komanda 1', '10', '8', '2', '5', '1', '20', '18', '2', '1', '5', '80'],
        ['2', 'Komanda 2', '10', '7', '3', '4', '2', '22', '20', '2', '0', '4' '70']
    ]
    df = krepsinio_klubu_rinkiklis.sukurti_df(krepsinio_data)
    assert isinstance(df, pd.DataFrame)
    assert df.columns.tolist() == ['Pozicija', 'Komanda', 'Zaista', 'Laimeta', 'Pralaimeta',
                                    'Laimeta_namie', 'Pralaimeta_namie',
                                    'Vidut_tasku_per_rungtyne', 'Varzovu_vid_tasku',
                                    'vidutinis_skirtumas', 'Laimeta_is_eiles', 'Laimeta_%']


def test_sukurti_df_without_data(krepsinio_klubu_rinkiklis):
    df = krepsinio_klubu_rinkiklis.sukurti_df(None)
    assert df is None