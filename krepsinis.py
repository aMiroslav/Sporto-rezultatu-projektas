import pandas as pd
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 500)
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('eurolyga.csv')

top_5_komandos = df.groupby('Komanda')['Laimeta'].mean().sort_values(ascending=False).head(5)
# print(top_5_komandos)

top_5_silpniausios_komandos = df.groupby('Komanda')['Pralaimeta'].mean().sort_values(ascending=False).head(5)
# print(top_5_silpniausios_komandos)

plt.figure(figsize=(14,7))
top_5_komandos.plot(kind='bar', color='red')
plt.title('Top 5 komandos Eurolygoje', fontsize=20)
plt.xlabel('Komanda', fontsize=14)
plt.ylabel('Laimetos rungtynes', fontsize=14)
plt.xticks(rotation=1)
plt.grid(True)
# plt.show()

plt.figure(figsize=(14,7))
top_5_silpniausios_komandos.plot(kind='bar', color='blue')
plt.title('Silpniausios komandos Eurolygoje', fontsize=20)
plt.xlabel('Komanda', fontsize=14)
plt.ylabel('Pralaimetos rungtynes', fontsize=14)
plt.xticks(rotation=1)
plt.grid(True)
plt.show()

