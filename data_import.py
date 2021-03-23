""" A partir dos arquivos originais gerar arquivos com rapida importação"""
    
import os.path
import pandas as pd

def data_import(path, forca_reload):
    """ Importação em caso de inexistência de arquivo de pickle gerado"""
    # os arquivos com os dados originais nao puderam ser disponibilizados, a pedido do cliente
    print("Chamada de data_import")
    file_to_write = path + "data\\interim\\horarios_raw.pck"
    if(not os.path.exists(file_to_write) or forca_reload):
        file_to_open = path + "data\\raw\\dados_horarios.xlsx"
        print("Abertura de dados horarios")
        db = pd.read_excel(file_to_open,sheet_name='Dados Horarios',skiprows =1)
        db.to_pickle(file_to_write)

    file_to_write = path + "data\\interim\\perda_carga.pck"
    if(not os.path.exists(file_to_write) or forca_reload):
        file_to_open = path + "data\\raw\\Medicoes_Gerais.xlsx"
        print("Abertura de perda de carga")
        db = pd.read_excel(file_to_open,sheet_name='Perda de Carga')
        db.to_pickle(file_to_write)
    print("Termino de data_import")

