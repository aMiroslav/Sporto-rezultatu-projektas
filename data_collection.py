import requests
from bs4 import BeautifulSoup
import pandas as pd
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)


class GautiPuslapi:
    def __init__(self, url):
        self.url = url

    def gauti_is_url(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print(f"Nepavyko gauti duomenu is {self.url}. Gautas 'status code': {response.status_code}")
            return None


class KrepsinioKlubuRinkiklis:
    def __init__(self):
        self.url = 'https://www.basketnews.lt/lygos/25-eurolyga/lenteles.html'
        self.gauti_puslapi = GautiPuslapi(self.url)

    def eurolygos_duomenu_rinkimas_bendras(self):
        soup = self.gauti_puslapi.gauti_is_url()
        if soup:
            krepsinio_data = []
            try:
                table = soup.find('table', class_='stats_01')
                if table:
                    for row in table.find_all('tr'):
                        row_data = []
                        for cell in row.find_all('td'):
                            row_data.append(cell.text.strip())
                        if row_data:
                            krepsinio_data.append(row_data)
                    return krepsinio_data
                else:
                    print("Lenteles nera.")
                    return None
            except AttributeError as e:
                print(f"Soupas nieko negrazino {e}")
                return None
        else:
            print("Nepavyko gauti duomenų iš puslapio.")
            return None

    def sukurti_df(self, krepsinio_data):
        if krepsinio_data:
            eurolyga_df = pd.DataFrame(krepsinio_data,
                                       columns=['Pozicija', 'Komanda', 'Zaista', 'Laimeta', 'Pralaimeta',
                                                'Laimeta_namie', 'Pralaimeta_namie',
                                                'Vidut_tasku_per_rungtyne', 'Varzovu_vid_tasku',
                                                'vidutinis_skirtumas', 'Laimeta_is_eiles', 'L5', 'Laimeta_%'])
            eurolyga_df = eurolyga_df.drop('L5', axis=1)
            return eurolyga_df
        else:
            print('Nera duomenu df sukurimui')
            return None

    def info(self):
        return self.eurolygos_duomenu_rinkimas_bendras()

class KrepsinioZaidejuRinkiklis:
    def __init__(self):
        self.url = (
            'https://www.basketnews.lt/lygos/25-eurolyga/statistika.html?fgroup=players&fseason=2023&fmonth=0&stage'
            '=0&fpos=pts&sort=total&games_type=all#google_vignette')
        self.gauti_puslapi = GautiPuslapi(self.url)

    def eurolygos_zaideju_statistika(self):
        # url = ('https://www.basketnews.lt/lygos/25-eurolyga/statistika.html?fgroup=players&fseason=2023&fmonth=0&stage'
        #        '=0&fpos=pts&sort=total&games_type=all#google_vignette')
        puslapio_duomenys = self.gauti_puslapi.gauti_is_url()
        if puslapio_duomenys:
            eurolyga_zaideju_data = []
            try:
                table = puslapio_duomenys.find('table', class_='list02')
                for row in table.find_all('tr'):
                    row_data = []
                    for cell in row.find_all('td'):
                        row_data.append(cell.text.strip())
                    if row_data:
                        eurolyga_zaideju_data.append(row_data)
                return eurolyga_zaideju_data
            except AttributeError as e:
                print(f"Lenteles rasti nepavyko {e}")
        else:
            print("Nepavyko gauti duomenų iš puslapio.")

    def sukurti_df(self, eurolyga_zaideju_data):
        if eurolyga_zaideju_data:
            eurolygos_zaidejai_df = pd.DataFrame(eurolyga_zaideju_data,
                                       columns=['Pozicija', 'Zaidejas', 'Taskai', 'Komanda', 'Rungtynes', 'Taskai_min',
                                                'Taskai_max'])
            eurolygos_zaidejai_df = eurolygos_zaidejai_df.drop(0)
            return eurolygos_zaidejai_df
        else:
            print('Nera duomenu df sukurimui')
            return None

    def info(self):
        return self.eurolygos_zaideju_statistika()

class FutboloKlubuRinkiklis:
    def __init__(self):
        self.url = 'https://alyga.lt/turnyrine-lentele/1'
        self.gauti_puslapi = GautiPuslapi(self.url)

    def futbolo_info(self):
        puslapio_duomenys = self.gauti_puslapi.gauti_is_url()
        if puslapio_duomenys:
            a_lygos_info = []
            try:
                table = puslapio_duomenys.find('table', class_='table01')
                for row in table.find_all('tr'):
                    row_data = []
                    for cell in row.find_all('td'):
                        row_data.append(cell.text.strip())
                    if row_data:
                        a_lygos_info.append(row_data)
                return a_lygos_info
            except AttributeError as e:
                print(f"Lenteles rasti nepavyko {e}")
        else:
            print("Nepavyko gauti duomenų iš puslapio.")

    def sukurti_df(self, a_lygos_info):
        if a_lygos_info:
            a_lygos_bendras_df = pd.DataFrame(a_lygos_info,
                                       columns=['Vieta', 'Komanda', 'Suzaista', 'Laimeta',
                                                'Lygiosios', 'Pralaimeta', 'Imusta', 'Praleista',
                                                'Ivarciu_santykis', 'Taskai'])
            return a_lygos_bendras_df
        else:
            print('Nera duomenu df sukurimui')
            return None

    def info(self):
        return self.futbolo_info()


class FutboloZaidejuRinkiklis:
    def __init__(self):
        self.url = 'https://alyga.lt/turnyrine-lentele/1'
        self.gauti_puslapi = GautiPuslapi(self.url)

    def futbolo_zaideju_info(self):
        puslapio_duomenys = self.gauti_puslapi.gauti_is_url()
        if puslapio_duomenys:
            zaideju_info = []
            try:
                table = puslapio_duomenys.find('table', class_='table01')
                linkai = table.find_all('a')
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
                return zaideju_info
            except AttributeError as e:
                print(f"Lenteles rasti nepavyko {e}")
        else:
            print("Nepavyko gauti duomenų iš puslapio.")

    def sukurti_df(self, zaideju_info):
        if zaideju_info:
            futbolo_zaideju_df = pd.DataFrame(zaideju_info,
                                       columns=['Komanda', 'Zaidejo_numeris','Zaidejas', 'Pozicija',
                                                'Zaistos_rungtynes', 'Minutes', 'Ivarciai', 'Rez_perdavima',
                                                'Geltonos_korteles', 'Raudonos_korteles'])
            return futbolo_zaideju_df
        else:
            print('Nera duomenu df sukurimui')
            return None

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

# krepsinio_rinkiklis = KrepsinioKlubuRinkiklis()
# krepsinio_data = krepsinio_rinkiklis.eurolygos_duomenu_rinkimas_bendras()
# if krepsinio_data:
#     df = krepsinio_rinkiklis.sukurti_df(krepsinio_data)
#     print(df)
# else:
#     print('Nera duomenu df sukurimui')

# krepsinio_zaideju_rinkiklis = KrepsinioZaidejuRinkiklis()
# eurolyga_zaideju_data = krepsinio_zaideju_rinkiklis.eurolygos_zaideju_statistika()
# if eurolyga_zaideju_data:
#     df = krepsinio_zaideju_rinkiklis.sukurti_df(eurolyga_zaideju_data)
#     print(df)
# else:
#     print('Nera duomenu df sukurimui')

# a_lygos_rinkiklis = FutboloKlubuRinkiklis()
# a_lygos_data = a_lygos_rinkiklis.futbolo_info()
# if a_lygos_data:
#     df = a_lygos_rinkiklis.sukurti_df(a_lygos_data)
#     print(df)
# else:
#     print('Nera duomenu df sukurimui')

# a_lygos_zaideju_rinkiklis = FutboloZaidejuRinkiklis()
# a_lygos_zaideju_data = a_lygos_zaideju_rinkiklis.futbolo_zaideju_info()
# if a_lygos_zaideju_data:
#     df = a_lygos_zaideju_rinkiklis.sukurti_df(a_lygos_zaideju_data)
#     print(df)
# else:
#     print('Nera duomenu df sukurimui')

class SportoInformacijosSistema:
    def __init__(self):
        self.krepsinio_rinkiklis = KrepsinioKlubuRinkiklis()
        self.krepsinio_zaideju_rinkiklis = KrepsinioZaidejuRinkiklis()
        self.futbolo_rinkiklis = FutboloKlubuRinkiklis()
        self.futbolo_zaideju_rinkiklis = FutboloZaidejuRinkiklis()

    def gauti_info_apie_krepsinio_komanda(self):
        krepsinio_data = self.krepsinio_rinkiklis.eurolygos_duomenu_rinkimas_bendras()
        if krepsinio_data:
            komandos_pavadinimas = input("Iveskite ieskomos komandos pavadinima: ")
            found = False
            for row in krepsinio_data:
                if komandos_pavadinimas in row:
                    print("Informacija apie komanda:")
                    print(row)
                    found = True
                    break
            if not found:
                print("Komanda nerasta.")
        else:
            print("Nera informacijos apie komandas.")

    def gauti_info_apie_krepsinio_zaideja(self):
        zaidejo_data = self.krepsinio_zaideju_rinkiklis.eurolygos_zaideju_statistika()
        if zaidejo_data:
            zaidejas = input("Iveskite ieskoma zaideja: ")
            zaidejas = zaidejas.replace(" ", "  ")
            found = False
            for row in zaidejo_data:
                if zaidejas in row:
                    print("Informacija apie zaideja:")
                    print(row)
                    found = True
                    break
            if not found:
                print("Zaidejas nerastas.")
        else:
            print("Nera informacijos apie zaidejus.")

    def gauti_info_apie_futbolo_kluba(self):
        a_lygos_info = self.futbolo_rinkiklis.futbolo_info()
        if a_lygos_info:
            komandos_pavadinimas = input("Iveskite ieskomos komandos pavadinima: ")
            found = False
            for row in a_lygos_info:
                if komandos_pavadinimas in row:
                    print("Informacija apie komanda:")
                    print(row)
                    found = True
                    break
            if not found:
                print("Komanda nerasta.")
        else:
            print("Nera informacijos apie komandas.")

    def gauti_info_apie_futbolo_zaideja(self):
        futbolo_zaideju_rinkiklis = FutboloZaidejuRinkiklis()
        futbolo_zaidejo_data = futbolo_zaideju_rinkiklis.futbolo_zaideju_info()
        if futbolo_zaidejo_data:
            zaidejas = input("Iveskite ieskoma zaideja: ")
            found = False
            for row in futbolo_zaidejo_data:
                if zaidejas in row:
                    print("Informacija apie zaideja:")
                    print(row)
                    found = True
                    break
            if not found:
                print("Zaidejas nerastas.")
        else:
            print("Nera informacijos apie zaidejus.")

    def main(self):
        print(f"Seiki atvyke i krepsinio ir futbolo statistikos sistema!\nPasirinkite jus dominanti veiksma:"
              f"\n1. Informacija apie pasirinkta Eurolygos kluba\n"
              f"2. Informacija apie pasirinkta Eurolygos zaideja\n"
              f"3. Informacija apie pasirinkta A lygos futbolo kluba\n"
              f"4. Informacija apie pasirinkta A lygos futbolo zaideja\n"
              f"5. Baigti darba ")


        pasirinkimas = input("Iveskite savo pasirinkima (1-5): ")

        if pasirinkimas == '1':
            self.gauti_info_apie_krepsinio_komanda()
        elif pasirinkimas == '2':
            self.gauti_info_apie_krepsinio_zaideja()
        elif pasirinkimas == '3':
            self.gauti_info_apie_futbolo_kluba()
        elif pasirinkimas == '4':
            self.gauti_info_apie_futbolo_zaideja()
        elif pasirinkimas =='5':
            print("Sistema isjungiama")
            return
        else:
            print("Neteisingas pasirinkimas, prasome ivesti skaiciu (1-5).")
            self.main()

if __name__ == "__main__":
    sporto_sistema = SportoInformacijosSistema()
    sporto_sistema.main()
