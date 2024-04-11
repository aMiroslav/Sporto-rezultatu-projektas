import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
import seaborn  as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score, \
    roc_curve, auc
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder

df =pd.read_csv('Cempionu lyga.csv')

df['Win_perc'] = (df['W'] / df['MP']) * 100
df['Collecting_point_perc'] = (df['Pts'] / (3 *df['MP'])) * 100

    # BENDRAS SITUACIJOS ATVAIZDAVIMAS
print('Čempionų lygos turnyrinė lentelė vaizdžiai')
fig = px.treemap(df, path=['Country', 'Squad'], values='Collecting_point_perc')
fig.update_traces(textfont=dict(size=26))
fig.show()

    # ANALIZUOJAME SANTYKI TARP PRALEISTU IVARCIU IR LYGIOSIOMIS PASIBAIGUSIU RUNGTYNIU
plt.scatter(df['D'], df['GA'], s=df['MP'])
plt.title('Santykis tarp praleistų įvarčių ir lygiųjų')
plt.xlabel('Lygiosios')
plt.ylabel('Pelnyti įvarčiai')
plt.show()


    # ANALIZUOJAME SANTYKI TARP PElNYTU IVARCIU IR PRALAIMETU RUNGTYNIU
categories = pd.cut(df['MP'], bins=3, labels=['6', '8', '9'])
colors = {'6': 'blue', '8': 'green', '9': 'red'}


for category in categories.unique():
    plt.scatter(df.loc[categories == category, 'L'], df.loc[categories == category, 'GF'],
                color=colors[category], label=category, alpha=0.5)
plt.title('Santykis tarp pelnytų įvarčių ir pralaimėtų rungtynių')
plt.xlabel('Pralaimėta rungtynių')
plt.ylabel('Pelnyta įvarcių')
plt.legend(title='Rungtynių sužaista')
plt.show()

    # Filter teams for the second visualization
df_filtered = df[(df['MP'] >= 5)]

fig = px.scatter(df, x='MP', y='W', size='MP', color='Country',
                 hover_name='Squad', hover_data=['Win_perc', 'Collecting_point_perc'],
                 opacity=0.5, size_max=40)
fig.update_layout(title='Komandų klasifikacija pagal šalis',
                  xaxis_title='Žaista rungtynių',
                  yaxis_title='Laimėta rungtynių',
                  legend_title='Šalis')
fig.show()

    # Linijine regresija
X = df[['GF', 'Pts']]
y = df['W']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse_linear = mean_squared_error(y_test, y_pred)
r2_score_linear = r2_score(y_test, y_pred)
print(f"MSE vertė: {mse_linear}")
print(f"R2 vertė: {r2_score_linear}")

plt.scatter(y_test, y_pred, color='blue')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
plt.xlabel('Tikrosios vertės')
plt.ylabel('Prognozuotos vertės')
plt.title('Linijinės regresijos modelis: Pelnyti įvarčiai ir Taškai vs. Pergalės')
plt.show()



    # Prognozuojame patekima i ketvirtfinali
X = df[['W', 'D', 'L', 'GF', 'GA', 'GD', 'xG', 'xGA']]
y = df['k']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

param_grid = {
    'n_estimators': [20, 50, 100, 200],
    'max_depth': [None, 5, 10, 15],
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42), param_grid=param_grid, cv=4, scoring='accuracy')
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
print("Geriausi parametrai", best_params)

best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)

    # Skaiciuojame modelio tikslumo rodiklius
accuracy_best = accuracy_score(y_test, y_pred_best)
precision_best = precision_score(y_test, y_pred_best, average='macro')
recall_best = recall_score(y_test, y_pred_best, average='macro')
f1_best = f1_score(y_test, y_pred_best, average='macro')
print('Geriausiais "accuracy score":', accuracy_best)
print('Geriausias "precision score":', precision_best)
print('Geriausias "recall score":', recall_best)
print('Geriausias "f1 score":', f1_best)

    # Kryzmines patikros vizualizacija
results = grid_search.cv_results_
score = results['mean_test_score'].reshape(len(param_grid['max_depth']), len(param_grid['n_estimators']))

plt.figure(figsize=(10, 6))
sns.heatmap(score, annot=True, fmt='.3f', xticklabels=param_grid['n_estimators'],
            yticklabels=param_grid['max_depth'], cmap='viridis', cbar=True)
plt.xlabel('Parametras: n_estimators')
plt.ylabel('Parametras: max_depth')
plt.title('Kryžminės patikros vizualizacija')
plt.show()

    # Vizualizuojame rodikliu svarba, prognozuojant patekima i ketvirtfinali
feature_importances = pd.DataFrame(best_model.feature_importances_, index=X_train.columns,
                                   columns=['Importance']).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(14,6))
sns.barplot(x=feature_importances.Importance, y=feature_importances.index, hue=feature_importances.index,
            palette='viridis', legend=False)
plt.title('Rodiklių svarba naudojant "RandomForestClassifier"')
plt.xlabel('Rodiklių svarba')
plt.ylabel('Rodikliai')
plt.show()

    # Naudojame ROC, AUC
y_scores_qf = best_model.predict_proba(X_test)[:, 1]
le = LabelEncoder()
y_test_encoded = le.fit_transform(y_test)

y_test_bin = (y_test_encoded == le.transform(['R16'])[0]).astype(int)

fpr, tpr, thresholds = roc_curve(y_test_bin, y_scores_qf)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC kreivė pagal spėjimą ar komanda pateks į Top-16"')
plt.legend(loc='lower right')
plt.show()


