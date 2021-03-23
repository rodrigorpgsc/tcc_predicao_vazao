""" Módulo para realizar transformação nos dados visando permitir a geração de dados finais que sejam uteis para a análise"""

import os.path
import pandas as pd
import numpy as np
import constants as co
from scipy import interpolate

def data_transformation_horario(path, forca_recalc):
    """ Chama as funcoes de preparacao dos dados horarios"""
    file_to_open = path + "data\\interim\\horarios_raw.pck"
    file_to_open_2 = path + "data\\interim\\perda_carga.pck"
    file_to_open_3 = path + "data\\interim\\diarios_raw.pck"
    file_to_write = path + "data\\interim\\horarios_transformed.pck"
    print("Inicio da data transformation horario")
    if forca_recalc or not os.path.exists(file_to_write):
        gera_enriquecimento_horario(file_to_open, file_to_open_2, file_to_open_3, file_to_write)
    print("Termino da data transformation horario")


def insere_separador_cabecalho(df):
    colunas = df.columns.tolist()
    new_col = colunas.copy()
    for a in range(len(colunas)):
        for i, c in enumerate(colunas[a]):
            if c.isdigit():
                # posicao do digito eh i
                new_col[a] = colunas[a][0:i]+'_'+colunas[a][i:]
                break


    df.columns = new_col
    return df
def calculo_rendimento(df):
    geracao = []
    q_turb = []

    # Obtem coluna de geração de cada unidade
    # Obtem coluna de vazão turbinada de cada máquina

    for i in range(co.num_unit):
        if i+1 <= 9:
            geracao.append(df['GE_0{}'.format(i+1)])
            q_turb.append(df['VT_0{}'.format(i+1)])
        else:
            geracao.append(df['GE_{}'.format(i+1)])
            q_turb.append(df['VT_{}'.format(i+1)])

    # Obtem coluna de queda vruta de cada ilha
    h_bruta = []
    for i in range(co.num_ilha):
        h_bruta.append(df['QB_{}H'.format(i+1)])

    #obtem o rendimento de cada maquina (caso a maq esteja desligada rend=0)
    rend = []
    for i in range(co.num_unit):
        if i <= 7:
            a = 0
        elif (i>=8) and (i<=19):
            a = 1
        elif (i>=20) and (i<=31):
            a = 2
        elif (i>=32) and (i<=43):
            a = 3
        else:
            print('alguma coisa ta errada na contagem')

# Calculo de nerdimentos das unidades ( 1 a 44)
        rend_temp = []
        for t in range(len(geracao[i])):
            if (geracao[i][t] >= 20): # and (h_bruta[t] >= 20):
                rend_eq = geracao[i][t] / (co.G * ((q_turb[i][t] * h_bruta[a][t]) - (co.ko * q_turb[i][t]**3)))
                rend_temp.append(rend_eq)
            else:
                rend_temp.append(0)
        rend.append(rend_temp)

    # Acrescenta uma coluna de rendimento para cada máquina (RND##)

    for i in range (co.num_unit):
        if i+1 <= 9:
            df['RND_0{}'.format(i+1)] = rend[i]
        else:
            df['RND_{}'.format(i+1)] = rend[i]

    return df
def agrupamento_ilha_geracao(df,tags_ug):
    for tag in tags_ug:
        aux=concatena_str_dic(co.ILHA_GERACAO, tag)
        
        for ilha in co.ILHA_GERACAO.keys():
            new_col = tag+ 'TOT'+ilha
            # cria coluna com a soma da tag de turbinas da mesma ilha ex: VTGG1TOT
            df.insert(0, new_col, df.filter(items=aux[ilha], axis=1).sum(axis=1))
    return df

def filtragem(df):
    """ Operação de juncao de valores individuais, para formar o todo"""
    # filtros para separar os cabecalho
    NMcha=df.filter(regex="NM")
    NJcha=df.filter(regex="NJ")
    
    df['NM_TOT'] = NMcha.median(axis=1)
    df['NJ_TOT'] = NJcha.median(axis=1)
    df['HGROSS'] = df['NM_TOT'] - df['NJ_TOT']
    return df

def estado_constante_durante_umahora(df, colunas, prefixo):
    for col in colunas:
        id_unidade = col[2:]
        df[prefixo+id_unidade] = (df[col] == 60).astype(int)
    return df

def selecao_colunas_unidade(df, prefixo):
    # seleciona as colunas em funcao de alguma caracteristica adicional da turbina
#    return [col for col in df if col.startswith(prefixo) and len(col)==4 and col[2].isdigit() and ((co.df_usina.loc[co.df_usina['Nome']== 'UG'+col[2:4]])['Qtd_pas']=='5').bool()]
    # filtragem sem levar em consideracao caracteriticas da turbina
    return [col for col in df if col.startswith(prefixo) and len(col)==4 and col[2].isdigit()]

def totalizadores(df):
    """ Operação de soma de valores individuais, para formar o todo"""
    # filtros para calcular os valores totais
    VTcha = selecao_colunas_unidade(df, 'VT')
    GEcha = selecao_colunas_unidade(df, 'GE')
#    aa = [col for col in VTcha if ((co.df_usina.loc[co.df_usina['Nome']== 'UG'+col[2:4]])['Qtd_pas']=='5').bool() & True]
    
    df['VT_TOT'] = df[VTcha].sum(axis=1)
    df['GE_TOT'] = df[GEcha].sum(axis=1)

    # calculo da qtd de ugs em disponibilidade(dco)
    TRcha = selecao_colunas_unidade(df, 'TR')
    prefixo = "UGRESERVA"
    df = estado_constante_durante_umahora(df, TRcha, prefixo)
    UG_REScha = [col for col in df if col.startswith(prefixo)]
    df[prefixo+'TOT'] = df[UG_REScha].sum(axis=1)

    # calculo da qtd de ugs gerando
    TGcha = selecao_colunas_unidade(df, 'TG')
    prefixo = "UGGERANDO"
    df = estado_constante_durante_umahora(df, TGcha, prefixo)
    UG_REScha = [col for col in df if col.startswith(prefixo)]
    df[prefixo+'TOT'] = df[UG_REScha].sum(axis=1)

    for ident in TRcha:
        id = ident[2:4]
        df['UGDISPONIVEL'+id] = df['UGRESERVA'+id]|df['UGGERANDO'+id]

    TDcha = [col for col in df if col.startswith('UGDISPONIVEL')]
    df['UGDISPONIVEL_TOT'] = df[TDcha].sum(axis=1)

    return df

def edita_colunas_tempo(df):
    data_arr=pd.date_range('01-01-2017', periods=len(df), freq='H')

    # seta DATA como DataFrame’s index.
    # adiciona campo temporal, subtituindo os campos data e hora separados
    df['DATA_HORA']=data_arr
    df = df.set_index('DATA_HORA')

   
    # calculo de colunas de tempo
    df['YEAR'] = df.index.year
    df['MONTH'] = df.index.month
    df['WEEKDAY'] = df.index.dayofweek

        # gera Nm do ibama

    return df

   
def concatena_str_dic(topologia_ilha, tag):
    chaves=topologia_ilha.keys()
    tags_ilha={}
    for chave in chaves:
        tags_ilha[chave]=[tag+str(s).zfill(2) for s in topologia_ilha[chave] ]
    return tags_ilha

def insere_perda_carga(df, pc):
    """ Insere perda de cara em metros e constante de perda """
    # Arquivos de dados
    df1 = pc
    df2 = df

    df_merge = df1.join(df2, how='inner', rsuffix='_dir')
    # Dicionário de saída
    for maq in range(0, 50):
        perda_grade = list(df_merge['UG{:02d}'.format(maq+1)])
        temp_lig = df_merge['TG_{:02d}'.format(maq+1)]
        uni_turb = df_merge['VT_{:02d}'.format(maq+1)]

        aux1 = []
        aux2 = []

        for (i, val) in enumerate(temp_lig):
            if (val == 60) and (not np.isnan(perda_grade[i])):
                q_turb = uni_turb[i]
                aux1.append(perda_grade[i])
                aux2.append(perda_grade[i]/(q_turb**2))
            else:
                aux1.append(np.nan)
                aux2.append(np.nan)

        # Colunas extras
        df_merge['PHG{}'.format(maq+1)] = aux1
        df_merge['K_GR{}'.format(maq+1)] = aux2
    return df_merge

def insere_setpoint_ilha(df):
    """ Insere o Setpoint de potencia global pra cada ilha """
    # Arquivos de dados
    df1 = df

    # Gera potencia 500kV
    pot_ilha = []
    for maq in range(0, 44):
        gerando = list(df1['UGGERANDO_{:02d}'.format(maq+1)])
        pot_ug = list(df1['GE_{:02d}'.format(maq+1)])
        pot_correct = np.multiply(gerando, pot_ug)
        pot_ilha.append(pot_correct)

    df['GE_500KV'] = list(np.sum(pot_ilha, axis=0))

    # Gera potencia 230kV
    pot_ilha = []
    for maq in range(44, 50):
        gerando = list(df1['UGGERANDO_{:02d}'.format(maq+1)])
        pot_ug = list(df1['GE_{:02d}'.format(maq+1)])
        pot_correct = np.multiply(gerando, pot_ug)
        pot_ilha.append(pot_correct)

    df['GE_230KV'] = list(np.sum(pot_ilha, axis=0))

    return df

def afluencia_interpol(df1, df2):
    """ função que interpola afluencia diária """
    aflu_h = df2['VAMH']

    size = len(aflu_h)

    aflu_d = list(df1['VAMD'][0: int(size/24)])

    # Define pontos originais
    xk = []
    for (i, val) in enumerate(aflu_d):
        xk.append(i*24)

    # Define novos pontos para linearização
    eixo_x = range(size - 24)

    intermed = interpolate.interp1d(xk, aflu_d, kind='cubic')

    aflu_spline = list(intermed(eixo_x)) + [aflu_d[-1]]*24

    df2['VAMH_SPLINE'] = aflu_spline

    return df2

def previsao_afluencia(df1):
    """ função quedefine a afluencia interpolada média """
    aflu_h = df1['VAMH_SPLINE']

    size = len(aflu_h)

    dias = int(size/24)
    # Loop principal
    prev_aflu = []
    for i in range(dias):
        conj = aflu_h[i*24 : (i+1)*24]

        mean = np.mean(conj)
        for j in range(0, 24):
            prev_aflu.append(mean)
    
    df1['PREV_AFLU'] = prev_aflu

    return df1

def gera_dataset_long_turbinas(file_to_write):
    # le a base de dados
    df = pd.read_pickle(file_to_write)
    # cria campos de discordancia em relacao ao proposto por SAE
    df['erro_pe'] = df['otimsppe_']-df['pe_']
    df['erro_52'] = df['otimr52_']-df['r52_']

    # aplica a medicao no conjunto de turbinas 
    
def gera_enriquecimento_horario(file_to_open, file_to_open_2, file_to_open_3, file_to_write):

    # le a base de dados
    df = pd.read_pickle(file_to_open)

    # le dados de perda na carga
    pc = pd.read_pickle(file_to_open_2)

    # le a base de dados diarios
    df_d = pd.read_pickle(file_to_open_3)
    
    # cria o indice, cria o data e hora e outros campos temporais
    df = edita_colunas_tempo(df)
    pc = edita_colunas_tempo(pc)

    # tags para serem agrupados para sumario por ilha de geracao
    tags_ug = ['VT','VV','GE']
    df = agrupamento_ilha_geracao(df, tags_ug)
    
    # calculo de valores totais da usina, todas as maquinas
    df = totalizadores(df)

    # calculo de valores totais da usina, todas as maquinas
    df = filtragem(df)

    # insere separador _ antes de numeros (requerido para operacoes de long->wide e wide->long)
    df = insere_separador_cabecalho(df)
    
    # calculo de rendimento
   # df = calculo_rendimento(df)

    # insere perda na grade em metro e constante de perda
    df = insere_perda_carga(df, pc)

    # insere afluencia diaria interpolada
    df = afluencia_interpol(df_d, df)

    # insere setpoint de potencia pra HVDC e acre/rondonia
    df = insere_setpoint_ilha(df)

    # insere previsão de afluencia diária
    df = previsao_afluencia(df)

    # salva dataset já pré-editado
    df.to_pickle(file_to_write)

    

