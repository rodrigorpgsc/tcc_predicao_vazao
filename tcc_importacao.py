# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from matplotlib import pyplot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import descritivo as ivp
import seaborn as sns


# # trecho de codigo contendo toda a base de dados transformada
# dados_raw = pd.read_pickle("data\\interim\\horarios_transformed.pck")
# # selecao das colunas de interesse
# col_input=list(['K_GR2', 'NM_1H','NJ_1H','PHG2','GE_02', 'VT_02'])
# dados = dados_raw[col_input]
# dados.to_pickle("data\\interim\\horarios_transformed_redz.pck")

# trecho de codigo contendo a base permitida de compartilhamento
dados = pd.read_pickle("data\\interim\\horarios_transformed_redz.pck")

dados['HGROSS_1H']=dados['NM_1H']-dados['NJ_1H']
dados['mes']=dados_raw.index.month


# informacao de periodicidades
dados=dados.asfreq(freq='H')

#######################################
########### Descritivo
#######################################
ivp.grafico_dados_raw(dados,"dados_raw.png")
# revelou outliers, entao vamos remover os outliers e toda a linha

dados['PHG2'][dados['PHG2']>1.2]=np.nan
# remover os registros de ge abaixo de 1M

# contagem de valores duplicados
(dados.duplicated()).value_counts()

# contagem de nans
conta_nans=dados.isna().sum()


#######################################
###### filtragem (preenchimento de NAs)
# tratamento de todos os NAs nas colunas selecionadas
dados = dados.interpolate()

ivp.grafico_dados_raw(dados,"dados_outlier.png")

#vazao em funcao da epoca do ano
pyplot.figure(figsize=(16, 9))
sns.boxplot(y=dados['VT_02'], x= dados['mes'])
plt.savefig('boxplot_mes_vazao.png')

