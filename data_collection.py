import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)


class SportoDuomenuRinkiklis:
    def __init__(self):
        pass

    def eurolygos_duomenu_rinkimas_bendras(self):
        url = 'https://www.basketnews.lt/lygos/25-eurolyga/lenteles.html'
        krepsinio_data = []
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='stats_01')
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):
                row_data.append(cell.text.strip())
            if row_data:
                krepsinio_data.append(row_data)
        eurolyga_df = pd.DataFrame(krepsinio_data, columns=['Pozicija', 'Komanda', 'Zaista', 'Laimeta', 'Pralaimeta',
                                                           'Laimeta_namie', 'Pralaimeta_namie',
                                                           'Vidut_tasku_per_rungtyne', 'Varzovu_vid_tasku',
                                                           'vidutinis_skirtumas', 'Laimeta_is_eiles', 'L5','Laimeta_%'])
        eurolyga_df = eurolyga_df.drop('L5', axis=1)
        return eurolyga_df


    def eurolygos_zaideju_statistika(self):
        url = ('https://www.basketnews.lt/lygos/25-eurolyga/statistika.html?fgroup=players&fseason=2023&fmonth=0&stage'
               '=0&fpos=pts&sort=total&games_type=all#google_vignette')
        eurolyga_zaideju_data = []
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='list02')
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):
                row_data.append(cell.text.strip())
            if row_data:
                eurolyga_zaideju_data.append(row_data)
        eurolygos_zaidejai_df = pd.DataFrame(eurolyga_zaideju_data, columns=['Pozicija', 'Zaidejas', 'Taskai', 'Komanda', 'Rungtynes', 'Taskai_min', 'Taskai_max'])
        eurolygos_zaidejai_df = eurolygos_zaidejai_df.drop(0)

        return eurolygos_zaidejai_df




rinkiklis = SportoDuomenuRinkiklis()
rinkiklis.eurolygos_duomenu_rinkimas_bendras()
# rinkiklis.eurolygos_zaideju_statistika()
