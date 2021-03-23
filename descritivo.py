# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 18:37:31 2020

@author: rodrigo.gosmann
"""
import matplotlib.pyplot as plt
from matplotlib import pyplot
import numpy as np
from scipy import stats
from pandas import DataFrame
import seaborn as sns
import pandas as pd


def grafico_dados_raw(dados_s_out,arq):
    df = pd.DataFrame(dados_s_out[['HGROSS_1H','PHG2','K_GR2','GE_02','NJ_1H','VT_02','mes']])
    pyplot.figure(figsize=(25, 25))
    sns_plot  = sns.pairplot(df,hue='mes')
    sns_plot.savefig(arq)
