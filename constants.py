import pandas as pd
""" Declaracao de constantes do programa"""

ILHA_GERACAO={
    'GG1':list(range(1,9)),
    'GG2':list(range(9,21)),
    'GG3':list(range(21,33)),
    'GG4':list(range(33,45)),
    'GG5':list(range(45,51)),
    }

df_usina = pd.DataFrame([
    ['UG01','GG1','5'],
    ['UG02','GG1','5'],
    ['UG03','GG1','5'],
    ['UG04','GG1','5'],
    ['UG05','GG1','5'],
    ['UG06','GG1','5'],
    ['UG07','GG1','5'],
    ['UG08','GG1','5'],

    ['UG09','GG2','5'],
    ['UG10','GG2','5'],
    ['UG11','GG2','5'],
    ['UG12','GG2','5'],
    ['UG13','GG2','4'],
    ['UG14','GG2','4'],
    ['UG15','GG2','4'],
    ['UG16','GG2','4'],
    ['UG17','GG2','4'],
    ['UG18','GG2','4'],
    ['UG19','GG2','4'],
    ['UG20','GG2','4'],

    ['UG21','GG3','5'],
    ['UG22','GG3','5'],
    ['UG23','GG3','4'],
    ['UG24','GG3','4'],
    ['UG25','GG3','4'],
    ['UG26','GG3','4'],
    ['UG27','GG3','4'],
    ['UG28','GG3','4'],
    ['UG29','GG3','4'],
    ['UG30','GG3','4'],
    ['UG31','GG3','5'],
    ['UG32','GG3','5'],

    ['UG33','GG4','5'],
    ['UG34','GG4','5'],
    ['UG35','GG4','5'],
    ['UG36','GG4','5'],
    ['UG37','GG4','4'],
    ['UG38','GG4','4'],
    ['UG39','GG4','4'],
    ['UG40','GG4','4'],
    ['UG41','GG4','4'],
    ['UG42','GG4','4'],
    ['UG43','GG4','4'],
    ['UG44','GG4','4'],

    ['UG45','GG5','5'],
    ['UG46','GG5','5'],
    ['UG47','GG5','5'],
    ['UG48','GG5','5'],
    ['UG49','GG5','5'],
    ['UG50','GG5','5'],
    ],columns = ['Nome','GG','Qtd_pas'])


COLS_LEGS_DIARIA ={
    'NR24':'Nível do reservatório', # NR24 NR24	#0.00	m	Nível do reservatório às 24 horas
    'VO24':'Volume total do reservatório', # VO24 VO24	#,##0.000	hm³	Volume total do reservatório às 24 horas
    'PV24':'Percentual de volume útil às 24 horas', # PV24 PV24	#0.00	%	Percentual de volume útil às 24 horas
    'GERD':'Geração diária', # GERD GERD	#,##0	MWh	Geração diária
    'VAMD':'Vazão afluente', # VAMD VAMD	#0	m³/s	Vazão afluente média diária
    'VDMD':'Vazão defluente', # VDMD VDMD	#0	m³/s	Vazão defluente média diária
    'PROD':'Produtividade', # PROD PROD	#,##0.000	MWh/(m³/s)	Produtividade média diária
    'VTMD':'Vazão turbinada', # VTMD VTMD	#0	m³/s	Vazão turbinada média diária
    'VVMD':'Vazão vertida',# VVMD VVMD	#0	m³/s	Vazão vertida média diária
    'VTVD':'Vazão turbinada em vazio',# VTVD VTVD	#0	m³/s	Vazão turbinada em vazio média diária
    'VOED':'Vazão outras estruturas (escada de peixes + ET)',# VOED VOED	#0	m³/s	Vazão outras estruturas (escada de peixes)
    'VPMD':'Vazão VTP-Vert.Principal',# VPMD VPMD	#0	m³/s	Vazão VTP média diária
    'VCMD':'Vazão VCP-Vert.Complementar',# VCMD VCMD	#0	m³/s	Vazão VTC média diária
    'VETMD':'Vazão ET-Extravasador de troncos',# VETMD VETMD	#0	m³/s	Vazão ET média diária
    'VGG1MD':'Vazão turbinada da GG1',# VGG1MD VGG1MD	#0	m³/s	Vazão turbinada da casa de força GG1 média diária
    'VGG2MD':'Vazão turbinada da GG2',# VGG2MD VGG2MD	#0	m³/s	Vazão turbinada da casa de força GG2 média diária
    'VGG3MD':'Vazão turbinada da GG3',# VGG3MD VGG3MD	#0	m³/s	Vazão turbinada da casa de força GG3 média diária
    'VGG4MD':'Vazão turbinada da GG4',# VGG4MD VGG4MD	#0	m³/s	Vazão turbinada da casa de força GG4 média diária
    # variaveis derivadas das originais
    'YEAR':'Ano',# 	string, ano do registro
    'MONTH':'Mês',# 	string, mes do registro
    'WEEKDAY':'Dia da semana',# 	int, dia da semana do registro
    'VSTP':'Vazão de escada de peixes',# 	m³/s, vazão de escada de peixes
    'NM_IBAMA':'Meta de reservatório segundo IBAMA ',# 	m	Meta de reservatorio segundo IBAMA, em função da vazao afluente
    }

# usina e totais
COLS_LEGS_HORARIA_TOT ={
    # variaveis da usina, não possuem id pois são unicos
    'NREH':'Nível do reservatório horário',
    'VTTH':'Volume total do reservatório horário',
    'PVUH':'Percentual de volume útil horário',
    'GERH':'Geração horária',
    'VAMH':'Vazão afluente média horária',
    'VDMH':'Vazão defluente média horária',
    'VTMH':'Vazão turbinada média horária',
    'VVMH':'Vazão vertida média horária',
    'VTVH':'Vazão turbinada em vazio média horária',
    'VOEH':'Vazão outras estruturas',
    'VPMH':'Vazão vertida média horária no VTP',
    'VCMH':'Vazão vertida média horária no VTC',
    'VSTP':'Vazão escada de peixes',
    'VCET':'Vazão horária da comporta do ET',
    'ACET':'Abertura horária da comporta do ET',
    'FLAG_STP':'Estado do STP',
    'FLAG_SADHI_MANUAL':'Entrada manual dos níveis da usina para envio ao ONS via SADHI',
    'NAMONTSADHI':'Nível montante horário para envio ao SADHI',
    'NAJUSSADHI':'Nível jusante horário para envio ao SADHI',
    'QBSADHI':'Queba bruta horária para envio ao SADHI',
    # variaveis geradas
    'YEAR':'Ano',# 	string, ano do registro
    'MONTH':'Mês',# 	string, mes do registro
    'WEEKDAY':'Dia da semana',# 	int, dia da semana do registro
    'DATA_HORA':'Data e hora juntos',
    'VT_TOT':'Vazao turbinada total horaria',
    'GE_TOT':'Geracao horario total horaria',
    'GE_500KV':'Geracao horario total da linha HVDC',
    'GE_230KV':'Geracao horario total da linha Acre/Rondonia',
    'NM_TOT':'Nível montante da usina (mediana das GGs)',
    'NJ_TOT':'Nível jusante da usina (mediana das GGs)',
    'HGROSS':'Queda bruta da usina ',
    'UG_RESERVA_TOT':'Quantidade de geradores em DCO', #int, qtd de ugs disponivel mas não utilizadas
    'UG_GERANDO_TOT':'Quantidade de geradores em funcionamento', #int, qtd de máquinas em operação e com 52 fechado
    'UG_DISPONIVEL_TOT':'Quantidade de geradores disponiveis', #int, disponivel seja gerando ou em dco
    'VAMH_SPLINE':'Vazão afluente diária interpolada (m³/s)'
}

# turbinas
COLS_LEGS_HORARIA_UG ={
    # variaveis originais
    'TG':'Tempo gerando da unidade UG##',
    'TV':'Tempo em vazio da unidade UG##',
    'TR':'Tempo em reserva da unidade UG##',
    'TP':'Tempo parado da unidade UG##',
    'GE':'Geração horária da unidade UG##',
    'VT':'Vazão turbinada da unidade UG##',
    'VV':'Vazão turbinada em vazio da unidade UG##',

    # variaveis geradas
    'UGRESERVA':'Gerador em DCO',  #int, ug disponivel mas não utilizadas
    'UGGERANDO':'Gerador em funcionamento',  #int, qtd de máquinas em operação e com 52 fechado
    'UGDISPONIVEL':'Gerador disponivel',  #int, disponivel seja gerando ou em dco
    'PHG':'Perda de carga na grade em metros',  #float, Perda de carga na grade em metros
    'K_GR':'Constante de perda na grade'  #float, Constante de perda na grade
}

####### Casas de força
COLS_LEGS_HORARIA_GG ={
    # variaveis originais

    'NMH':'Nível de montante horário da casa de força GG#',
    'NJH':'Nível de jusante horário da casa de força GG#',
    'QBH':'Queda bruta horária da casa de força GG#',
    'VGGMH':'Vazão turbinada média horária na casa de força GG#',
}

####### Vertedouros
COLS_LEGS_HORARIA_VERT ={

    ####### Comportas principais
    'AC':'Abertura horária da comporta ## do VTP',
    'VC':'Vazão horária da comporta ## do VTP',
}

ko = 9.2039e-7      # Constante de perda de carga
G = 1.042926e-2     #Constante relativa a gravidade e densidade d'agua
num_unit = 44       #Número de unidades
num_ilha = 4        #Número de ilhas

#####################################
##### Dataset long

####### LONG_TURBINAS
COLS_LEGS_LONG_TURBINAS ={
    # originais
    'data_hora':'Data e hora do registro',
    'ug':'identificador da turbina', # tipo int
    'pe_':'potencia ativa medida', # tipo float
    'r52_':'estado do r52 medido', # tipo int
    'hloss_':'perda na grade medida', # tipo float
    'qtur_':'vazao turbina medida ', # tipo float
    'otim52_':'estado do 52 otimo proposto', # tipo int
    'otimsppe_':'setpoint otimo proposto', # tipo float
    'bench52_':'estado do 52 benchmark proposto', # tipo int
    'benchsppe_':'setpoint benchmark proposto', # tipo float
    # derivados
    'erro_pe':'setpoint benchmark proposto', # tipo float
    'erro_52':'setpoint benchmark proposto', # tipo float
    
}



