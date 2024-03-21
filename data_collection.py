import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)


class KrepsinioKlubuRinkiklis:

    def eurolygos_duomenu_rinkimas_bendras(self):
        url = 'https://www.basketnews.lt/lygos/25-eurolyga/lenteles.html'
        krepsinio_data = []
        response = requests.get(url)
        if response.status_code == 200:
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
        else:
            print('Something went wrong cannot get a website data..')

    def info(self):
        return self.eurolygos_duomenu_rinkimas_bendras()

class KrepsinioZaidejuRinkiklis:

    def eurolygos_zaideju_statistika(self):
        url = ('https://www.basketnews.lt/lygos/25-eurolyga/statistika.html?fgroup=players&fseason=2023&fmonth=0&stage'
               '=0&fpos=pts&sort=total&games_type=all#google_vignette')
        eurolyga_zaideju_data = []
        response = requests.get(url)
        if response.status_code == 200:
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
        else:
            print('Something went wrong cannot get a website data..')

    def info(self):
        return self.eurolygos_zaideju_statistika()

class FutboloKlubuRinkiklis:

    def futbolo_info(self):
        url = 'https://alyga.lt/turnyrine-lentele/1'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/122.0.0.0 Safari/537.36 CCleaner/122.0.0.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            a_lygos_info = []
            table = soup.find('table', class_='table01')
            for row in table.find_all('tr'):
                row_data = []
                for cell in row.find_all('td'):
                    row_data.append(cell.text.strip())
                if row_data:
                    a_lygos_info.append(row_data)
            a_lygos_bendras_df = pd.DataFrame(a_lygos_info, columns=['Vieta', 'Komanda', 'Suzaista', 'Laimeta',
                                                                     'Lygiosios', 'Pralaimeta', 'Imusta', 'Praleista',
                                                                     'Ivarciu_santykis', 'Taskai'])
            return a_lygos_bendras_df

        else:
            print('Something went wrong cannot get a website data..')

    def info(self):
        return self.futbolo_info()

class FutboloZaidejuRinkiklis:
    def futbolo_zaideju_info(self):
        url = 'https://alyga.lt/turnyrine-lentele/1'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/122.0.0.0 Safari/537.36 CCleaner/122.0.0.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='table01')
            linkai = table.find_all('a')
            zaideju_info = []
            for link in linkai:
                komandos_pavadinimas = link.text.strip()
                komandos_linkas = link['href']
                response_komanda = requests.get(komandos_linkas)
                if response_komanda.status_code == 200:
                    soup_team = BeautifulSoup(response_komanda.text, 'html.parser')
                    zaideju_lentele = soup_team.find('table', class_='table01 tablesorter')
                    for row in zaideju_lentele.find_all('tr')[1:]:
                        zaideju_data = [komandos_pavadinimas]
                        for cell in row.find_all('td'):
                            zaideju_data.append(cell.text.strip())
                        if zaideju_data:
                            zaideju_info.append(zaideju_data)
                        else:
                            print('Nera informacijos apie zaidejus')
                else:
                    print('Negalima pasiekti zaideju puslapio')

            futbolo_zaideju_df = pd.DataFrame(zaideju_info, columns=['Komanda', 'Zaidejo_numeris','Zaidejas', 'Pozicija',
                                                            'Zaistos_rungtynes', 'Minutes', 'Ivarciai', 'Rez_perdavima',
                                                            'Geltonos_korteles', 'Raudonos_korteles'])
            return futbolo_zaideju_df

        else:
            print('Something went wrong cannot get a website data..')

    def info(self):
        return self.futbolo_zaideju_info()



class InformacijaApieSporta:
    def __init__(self, duomenys):
        self.duomenys = duomenys

    def gauti_info_apie_komandas(self, komandos_pavadinimas):
        komandos_info = self.duomenys[self.duomenys['Komanda'] == komandos_pavadinimas]
        if not komandos_info.empty:
            return komandos_info
        else:
            print(f'Komanda {komandos_pavadinimas} nerasta')

    def gauti_info_apie_zaideja(self, zaidejas):
        zaidejo_info = self.duomenys[self.duomenys['Zaidejas'] == zaidejas]
        if not zaidejo_info.empty:
            return zaidejo_info
        else:print(f'Zaidejas {zaidejas} nerasta')



# futbolo_rinkiklis = FutboloKlubuRinkiklis()
# a_lygos_bendras_df = futbolo_rinkiklis.futbolo_info()
# informacija_apie_sporta = InformacijaApieSporta(a_lygos_bendras_df)
# komandos_info = informacija_apie_sporta.gauti_info_apie_komandas('Marijampolės „Sūduva“')
# if komandos_info is not None:
#     print("Informacija apie komanda")
#     print(komandos_info)
#
# krepsinio_rinkiklis = KrepsinioKlubuRinkiklis()
# krepsinio_data = krepsinio_rinkiklis.eurolygos_duomenu_rinkimas_bendras()
# informacija_apie_sporta = InformacijaApieSporta(krepsinio_data)
# komandos_info = informacija_apie_sporta.gauti_info_apie_komandas('Madrido Real')
# if komandos_info is not None:
#     print("Informacija apie komanda")
#     print(komandos_info)
#
# krepsinio_zaideju_rinkiklis = KrepsinioZaidejuRinkiklis()
# zaidejo_data = krepsinio_zaideju_rinkiklis.eurolygos_zaideju_statistika()
# informacija_apie_zaideja = InformacijaApieSporta(zaidejo_data)
# zaidejo_info = informacija_apie_zaideja.gauti_info_apie_zaideja('Achille  Polonara')
# if zaidejo_info is not None:
#     print("Informacija apie zaideja:")
#     print(zaidejo_info)
#
# futbolo_zaideju_rinkiklis = FutboloZaidejuRinkiklis()
# zaidejo_data = futbolo_zaideju_rinkiklis.futbolo_zaideju_info()
# informacija_apie_zaideja = InformacijaApieSporta(zaidejo_data)
# zaidejo_info = informacija_apie_zaideja.gauti_info_apie_zaideja('Paulius Golubickas')
# if zaidejo_info is not None:
#     print("Informacija apie zaideja:")
#     print(zaidejo_info)


