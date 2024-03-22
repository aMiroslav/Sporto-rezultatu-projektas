import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)


# df = pd.read_csv('a_lygos_info.csv')
df = pd.read_csv('futbolo_zaideju_info.csv')

# daugiausiai_tasku_surinkus_komanda = df.groupby('Komanda')['Taskai'].mean().sort_values(ascending=False)
# # print(daugiausiai_tasku_surinkus_komanda)
#
# daugiausiai_ivarciu_imuse_komanda = df.groupby('Komanda')['Imusta'].mean().sort_values(ascending=False)
# # print(daugiausiai_ivarciu_imuse_komanda)
#
# komanda_daugiausiai_laimejusi_varzybu = df.groupby('Komanda')['Laimeta'].mean().sort_values(ascending=False)
# # print(komanda_daugiausiai_laimejusi_varzybu)
#
# geriausiai_pasirodzius_komanda = df.loc[(df['Laimeta'].idxmax()) & (df['Taskai'].idxmax())]
# # print(geriausiai_pasirodzius_komanda)
#
#
# df_rusiavimas = df.sort_values(by=['Komanda', 'Taskai', 'Laimeta', 'Ivarciu_santykis', 'Praleista'], ascending=[False, False, False, False, True])
# top_5_komandos = df_rusiavimas.head(5)
#
# top_5_komandos_a = df.groupby('Komanda')['Imusta'].mean().sort_values(ascending=False).head(5)
# print(top_5_komandos)


# print(top_5_komandos)

# #FUTBOLAS
top_komandos = df.groupby('Komanda')['Ivarciai'].max().sort_values(ascending=False)
# print(top_komandos)

top_zaidejas = df.groupby(['Zaidejas', 'Komanda'])['Ivarciai'].max().sort_values(ascending=False).head(5)
# print(top_zaidejas)

daugiausiai_ivarciu_imuses_zaidejas = df.groupby('Zaidejas')['Ivarciai'].max().sort_values(ascending=False).head(1)
# print(daugiausiai_ivarciu_imuses_zaidejas)

daugiausiai_zaides_zaidejas = df.groupby('Zaidejas')['Minutes'].max().sort_values(ascending=False).head(1)
# print(daugiausiai_zaides_zaidejas)

daugiausiai_zaidus_komanda = df.groupby('Komanda')['Minutes'].mean().sort_values(ascending=False)
# print(daugiausiai_zaidus_komanda)

maziausiai_nuobaudu_gavus_komanda = df.groupby('Komanda')['Geltonos_korteles'].sum().sort_values(ascending=True).head(1)
# print(maziausiai_nuobaudu_gavus_komanda)

daugiausiai_nuobaudu_gavusios_komandos = df.groupby('Komanda')['Geltonos_korteles'].sum().sort_values(ascending=False)
# print(daugiausiai_nuobaudu_gavusius_komandos)

# plt.figure(figsize=(14,7))
# top_5_komandos_a.plot(kind='bar', color='green')
# plt.title('Top 5 Komandos A lygoje', fontsize=20)
# plt.xlabel('Komanda', fontsize=12)
# plt.ylabel('Ivarciai', fontsize=12)
# plt.xticks(rotation=1)
# plt.grid(True)
# # plt.show()

plt.figure(figsize=(25,10))
daugiausiai_nuobaudu_gavusios_komandos.plot(kind='bar', color='red')
plt.title('Geltonu korteliu rinkejai', fontsize=40)
plt.xlabel('Komanda', fontsize=20)
plt.ylabel('Geltonos korteles', fontsize=20)
plt.xticks(rotation=1)
plt.grid(True)
plt.show()





