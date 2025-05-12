
# %%
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, train_test_split
from scipy.stats import randint

import matplotlib.pyplot as plt
from IPython.display import Image

# %%
exprData = pd.read_csv('data/UCEC_EXPRS_Normalized_filtered.csv')

exprData = exprData.drop('Unnamed: 0', axis=1)

print(exprData.head())

# %%
clin = pd.read_csv('data/UCEC_Clinical_522.csv')
print(clin.head())
for c in clin.columns:
    print(c)

# %%
X = exprData
y = clin['Cluster_3']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# %%
rf = RandomForestClassifier()
rf.fit(X_train, y_train)

# %%
y_pred = rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)

ConfusionMatrixDisplay(confusion_matrix=cm).plot()


# %%
### Ajuste de  hiperparametros
param_dist = {'n_estimators': randint(20,100),
              'max_depth': randint(1,20)}

print(param_dist['n_estimators'].rvs())

# Busca aleatória para testar os parâmetros
rand_search = RandomizedSearchCV(rf, 
                                 param_distributions = param_dist, 
                                 n_iter=5, 
                                 cv=5)


# Treina o modelo
rand_search.fit(X_train, y_train)

# Variável para o melhor modelo
best_rf = rand_search.best_estimator_

# Melhores hiperparametros
print('Best hyperparameters:',  rand_search.best_params_)


# %%
### Para Grid Search - muito demorado para rodar !!!!! Melhor não rodar ###

# param_dist = {'n_estimators': [i for i in range(20,100)],
#               'max_depth': [i for i in range(1,20)]}

# gsearch = GridSearchCV(rf, param_grid=param_dist)

# # Treina o modelo
# gsearch.fit(X_train, y_train)

# # Variável para o melhor modelo
# best_rf = gsearch.best_estimator_

# # Melhores hiperparametros
# print('Best hyperparameters:',  gsearch.best_params_)


# %%
# Predição do melhor modelo
y_pred = best_rf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print(classification_report(y_test, y_pred))

# Matriz de confusão
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(confusion_matrix=cm).plot()
# plt.show()
# %%
