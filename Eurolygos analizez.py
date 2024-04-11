import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, silhouette_score, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler

        # Naudojame RandomForestRegressor norėdami nuspėti laimėtų rungtynių kiekį
df = pd.read_csv('eurolyga.csv')

features = df[['Vidut_tasku_per_rungtyne','vidutinis_skirtumas', 'Varzovu_vid_tasku', 'Laimeta_%']]

X = features
y = df['Laimeta']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)

param_grid = {
    'n_estimators': [10, 20, 30, 40, 50, 60, 70, 80, 90],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid=param_grid, cv=5,
                           scoring='neg_mean_squared_error', n_jobs=-1)

grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
best_params = grid_search.best_params_

y_pred_best = best_model.predict(X_test)
mse_best = mean_squared_error(y_test, y_pred_best)
r2 = r2_score(y_test, y_pred_best)
print(f'Geriausia "Mean Squared Error" vertė: {mse_best:.2f}')
print(f'Geriausi modelio parametrai: {best_params}')
print(f'Geriausia "R2 Score" vertė: {r2:.2f}')

    # Vizualizuojame duomenys naudodami geriausius parametrus iš kryžminės patikros
regressor = RandomForestRegressor(random_state=42, n_estimators=80, max_depth=None, min_samples_split=2)
regressor.fit(X_train, y_train)

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_best, color='blue')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel('Tikras laimetų rungtynių skaičius')
plt.ylabel('Suprognuozuotas laimėtų rungtynių skaičius')
plt.title('Suprognuozuotų laimėjimų vs. Tikrų laimėjimų santykis')
plt.show()

    # Apskaičiuojame ir vizualizuojame rodiklių svarbą prognozei
feature_importances = regressor.feature_importances_
feature_importance_df = pd.DataFrame({'Rodiklis': X.columns, 'Svarba': feature_importances})
feature_importance_df = feature_importance_df.sort_values(by='Svarba', ascending=False)
print(feature_importance_df)

plt.figure(figsize=(18, 6))
plt.barh(feature_importance_df['Rodiklis'], feature_importance_df['Svarba'], color='skyblue', height=0.5)
plt.xlabel('Svarba')
plt.ylabel('Rodiklis')
plt.title('Rodiklių įtaka Laimėtoms rungtynėms')
plt.gca().invert_yaxis()
plt.show()

    # Vizualizuojame koreliaciją tarp vidutiniškai per rungtynes pelnomų taškų ir laimėjimų
plt.scatter(df['Laimeta'], df['Vidut_tasku_per_rungtyne'], c='red', alpha=0.3,)
plt.title('Koreliacija tarp laimėjimų ir vidutiniškai perlnomų per rungtynes taškų')
plt.xlabel('Laimėta')
plt.ylabel('Vidutiniškai taškų per rungtynes')
plt.show()

       # Prognozuojame pelnytų taškų skaičių naudodami Linijinės regresijos modelį

X = df[['Zaista', 'Pralaimeta', 'Laimeta_namie', 'Pralaimeta_namie', 'Varzovu_vid_tasku', 'vidutinis_skirtumas',
        'Laimeta_is_eiles', 'Laimeta_%']]
y = df['Vidut_tasku_per_rungtyne']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse_linear = mean_squared_error(y_test, y_pred)
rmse_linear = np.sqrt(mse_linear)
r2_score_linear = r2_score(y_test, y_pred)
print(f"Mean Squared Error: {mse_linear}")
print(f"Root Mean Squared Error: {rmse_linear}")
print(f"R2 Score: {r2_score_linear}")

    # Vizualizuojame prognozę
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, color='blue')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--')
plt.xlabel('Pelnyti taškai')
plt.ylabel('Suprognuozuotas pelnytų taųkų skaičius')
plt.title(f'Pelnyti vs suprognozuoti taškai. MSE: {mse_linear:.4f}')
plt.show()

        # Naudojame K-means klasterizajios metodą duomenų analizei

X = df[['Zaista', 'Laimeta', 'Pralaimeta', 'Laimeta_namie', 'Pralaimeta_namie', 'Varzovu_vid_tasku', 'vidutinis_skirtumas',
        'Laimeta_is_eiles', 'Laimeta_%']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit_transform(scaled_features)

df['Cluster_Labels'] = kmeans.labels_
silh_score = silhouette_score(scaled_features, kmeans.labels_)
print(f'"Silhouette" rodiklio vertė: {silh_score}')

plt.figure(figsize=(10,6))
plt.scatter(scaled_features[:, 1], scaled_features[:, 2], c=kmeans.labels_, cmap='viridis', s=50, edgecolor='k')
plt.title(f'Eurolygos statistikos klasterizavimas su K-Means, Silhouette score: {silh_score:.4f}')
plt.xlabel('Žaista rungtynių')
plt.ylabel("Laimėta namie rungtynių")
plt.colorbar(label='Cluster ID')
plt.show()

