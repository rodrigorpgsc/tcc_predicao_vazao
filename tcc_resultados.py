# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 22:28:09 2021

@author: rodrigo.gosmann
"""

import matplotlib.pyplot as plt
import seaborn as sns



plt.figure(figsize=(20,10)) #plotting
amostras_zoom=500
plt.plot(dataY_plot[qtd_amo_treino:qtd_amo_treino+amostras_zoom], label='Actuall Data') #actual plot
plt.plot(data_predict[qtd_amo_treino:qtd_amo_treino+amostras_zoom], label='Neural Net Data') #predicted plot
plt.plot(y_pred_forest[qtd_amo_treino:qtd_amo_treino+amostras_zoom], label='Forest Data') #predicted plot
plt.title('Time-Series Prediction')
plt.legend()
plt.savefig('zoom_ts.png')


plt.clf()
plt.figure(figsize=(10,6)) #plotting
sns.histplot(residuos[qtd_amo_treino:],kde=True)
plt.xlim(-30, 130)
plt.title('Histograma dos residuos')
plt.savefig('hist_residuos.png')


np.percentile(residuos['forest'],[2.5,97.5])

np.percentile(residuos['neural_net'],[2.5,97.5])
