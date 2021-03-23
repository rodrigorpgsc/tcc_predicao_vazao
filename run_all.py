""" Projeto para analise de dados. Tem como objetivo gerar figuras automaticamente a partir da execução do script"""
import data_import as di
import data_preparation as dp
import os.path


# Forca recalculo a partir dos dados brutos
forca_import_excel = False
forca_recalc_horario = False

# selecao de path em funcao do usuario que executa o script (RPG ou AIP)
path =""
######################################
# Transformação para pickle

# transformacao de dados de excel para pickle, para auxiliar leitura de dados posteriores
di.data_import(path, forca_import_excel)

######################################
# Adição de colunas para enriquecimento do dataset

dp.data_transformation_horario(path, forca_recalc_horario)

