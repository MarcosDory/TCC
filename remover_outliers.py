# -*- coding: utf-8 -*-
"""Remover_outliers

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fJhHiZwmaKDhqkz7b7IhlvvvVqshme7f

**REMOVER OUTLIERS VIA Z_SCORE OU MÉTODO INTER QUARTIL:**

Marcos Alexandre Leoni de Goes
9817870

24/11/2023

O script possui as seguintes finalidades:



*   Abrir planilhas meteorológicas fornecidas pelo site do INMET em escala diária;

*   Apresentar ao usuário graficos para avaliação de assimetria junto com o valor de z-score;
*   Questionar ao usuário se determinada variável é simetrica ou não;


*   Através da resposta fornecida, aplicar método IQR ou z-score para remover outliers;




*   Apresntar um resumo dos dados para cada planilha com os limites superiores e inferiores, total de dados, total de outliers removidos;
"""

# Importando bibliotecas:
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
from datetime import datetime
import scipy.stats as stats
import time

#Salvando os nomes dos diretórios de cada arquivo em uma variável:

path = r'/content/drive/Shareddrives/PUB_Meteorologia/Dados_diarios_com_radiacao'
files=os.listdir(path)
files_xlsx = [path + "/"+ f for f in files if f[-3:] == 'csv']

# Ajustando as datas da planilha para colunas separadas de dia, mês e ano:

 def configurando_data(df):
  df['Data Medicao'] = df['Data Medicao'].apply(pd.to_datetime)
  df['ANO'] = df['Data Medicao'].dt.year
  df['MES'] = df['Data Medicao'].dt.month
  df['DIA'] = df['Data Medicao'].dt.day
  df.loc[df.MES == 1,'MES']='Jan'
  df.loc[df.MES == 2,'MES']='Fev'
  df.loc[df.MES == 3,'MES']='Mar'
  df.loc[df.MES == 4,'MES']='Abr'
  df.loc[df.MES == 5,'MES']='Mai'
  df.loc[df.MES == 6,'MES']='Jun'
  df.loc[df.MES == 7,'MES']='Jul'
  df.loc[df.MES == 8,'MES']='Ago'
  df.loc[df.MES == 9,'MES']='Set'
  df.loc[df.MES == 10,'MES']='Out'
  df.loc[df.MES == 11,'MES']='Nov'
  df.loc[df.MES == 12,'MES']='Dez'

"""A função abaixo denominada "removendo_outliers", irá aplicar o método z-score ou IQR para remoção de valores:

Ela usará como critério a resposta do input entregue ao usuário se a variável apresenta distribuição normal ou não:
"""

def removendo_outliers(df):

  if lista[1] == "nao":

    Q1 = np.quantile(df["TMax(°C)"],.25)
    Q3 = np.quantile(df["TMax(°C)"],.75)
    IIQ = Q3 - Q1
    Lim_inf_iqr_temperatura = Q1 - 1.5*IIQ
    Lim_sup_iqr_temperatura = Q3 + 1.5*IIQ
    df = df.loc[df['TMax(°C)'] > Lim_inf_iqr_temperatura]
    df = df.loc[df['TMax(°C)'] < Lim_sup_iqr_temperatura]

  else:

    med=sum(df["TMax(°C)"])/len(df["TMax(°C)"])
    std=np.std(df["TMax(°C)"])
    zscore_temperatura_sup=med+3*std
    zscore_temperatura_inf=med-3*std
    df = df.loc[df['TMax(°C)'] < zscore_temperatura_sup]
    df = df.loc[df['TMax(°C)'] > zscore_temperatura_inf]

  if lista[2] == "nao":

    Q1 = np.quantile(df["TMin(°C)"],.25)
    Q3 = np.quantile(df["TMin(°C)"],.75)
    IIQ = Q3 - Q1
    Lim_inf_iqr_temperatura_min = Q1 - 1.5*IIQ
    Lim_sup_iqr_temperatura_min = Q3 + 1.5*IIQ
    df = df.loc[df['TMin(°C)'] < Lim_sup_iqr_temperatura_min]
    df = df.loc[df['TMin(°C)'] > Lim_inf_iqr_temperatura_min]

  else:

    med=sum(df["TMin(°C)"])/len(df["TMin(°C)"])
    std=np.std(df["TMin(°C)"])
    zscore_temperatura_sup=med+3*std
    zscore_temperatura_inf=med-3*std
    df = df.loc[df['TMin(°C)'] < zscore_temperatura_sup]
    df = df.loc[df['TMin(°C)'] > zscore_temperatura_inf]

  if lista[3] == "nao":

    Q1 = np.quantile(df['UR(%)'],.25)
    Q3 = np.quantile(df['UR(%)'],.75)
    IIQ = Q3 - Q1
    Lim_inf_iqr_ur = Q1 - 1.5*IIQ
    Lim_sup_iqr_ur = Q3 + 1.5*IIQ
    df = df.loc[df['UR(%)'] < Lim_sup_iqr_ur]
    df = df.loc[df['UR(%)'] > Lim_inf_iqr_ur]

  else:

    med=sum(df['UR(%)'])/len(df['UR(%)'])
    std=np.std(df['UR(%)'])
    zscore_ur_sup=med+3*std
    zscore_ur_inf=med-3*std
    df = df.loc[df['UR(%)'] < zscore_ur_sup]
    df = df.loc[df['UR(%)'] > zscore_ur_inf]

  if lista[4] == "nao":

    Q1 = np.quantile(df['U2(m/s)'],.25)
    Q3 = np.quantile(df['U2(m/s)'],.75)
    IIQ = Q3 - Q1
    Lim_inf_iqr_vento = Q1 - 1.5*IIQ
    Lim_sup_iqr_vento = Q3 + 1.5*IIQ
    df = df.loc[df['U2(m/s)'] < Lim_sup_iqr_vento]
    df = df.loc[df['U2(m/s)'] > Lim_inf_iqr_vento]


  else:

    med=sum(df['U2(m/s)'])/len(df['U2(m/s)'])
    std=np.std(df['U2(m/s)'])
    zscore_vento_sup=med+3*std
    zscore_vento_inf=med-3*std
    df = df.loc[df['U2(m/s)'] < zscore_vento_sup]
    df = df.loc[df['U2(m/s)'] > zscore_vento_inf]

  if lista[5] == "nao":

    Q1 = np.quantile(df["RAD(MJ/m²)"],.25)
    Q3 = np.quantile(df["RAD(MJ/m²)"],.75)
    IIQ = Q3 - Q1
    Lim_inf_iqr_rad = Q1 - 1.5*IIQ
    Lim_sup_iqr_rad = Q3 + 1.5*IIQ
    df = df.loc[df["RAD(MJ/m²)"] < Lim_sup_iqr_rad]
    df = df.loc[df["RAD(MJ/m²)"] > Lim_inf_iqr_rad]

  else:

    med=sum(df['RAD(MJ/m²)'])/len(df['RAD(MJ/m²)'])
    std=np.std(df['RAD(MJ/m²)'])
    zscore_radiacao_sup=med+3*std
    zscore_radiacao_inf=med-3*std
    df = df.loc[df['RAD(MJ/m²)'] < zscore_radiacao_sup]
    df = df.loc[df['RAD(MJ/m²)'] > zscore_radiacao_inf]

  time.sleep(4)
  df.to_csv("sem_outliers_" + files[contador] , index=False)

o21 205-ok

# Calculando ETo via PENMAN-Monteith:

def calculo_eto_horario(df):

  df["Coef G"]=df["Rn(MJ/m²)"]*0.1
  df["es"]=(7.5*df["Tar"])/(df["Tar"] + 273.3)
  df["es"]=0.6108*10**(df["es"])
  df["ea"]=(df["es"]*df['UR(%)'])/100
  df["Coef Y"]=0.063
  df["Coef S"]=(4098*df["es"])
  df["Coef S"]=df["Coef S"]/((df["Tar"]+273.3)*(df["Tar"]+273.3))
  df["ETP P-Mont"]=(0.408*(df["Coef S"])*((df["Rn(MJ/m²)"])-(df["Coef G"])))+((900*df["Coef Y"]*df['U2(m/s)']*(df["es"]-df["ea"]))/(df["Tar"]+273.3))
  df["ETP P-Mont"]=df["ETP P-Mont"]/(df["Coef S"] + df["Coef Y"]*(1+0.34*(df['U2(m/s)'])))

def graficos(df):
 contar=1
 coluna=df.columns.tolist()

 while contar < 7:
  plt.figure(figsize=(12,4))

  k=coluna[contar]
  plt.subplot(1,3,1)
  plt.hist(df[k],bins=30)
  plt.title('Histograma')

  plt.subplot(1,3,2)
  stats.probplot(df[k],
  dist='norm',plot=plt)
  plt.ylabel('quantiles')

  plt.subplot(1,3,3)
  sns.boxplot(y=df[k])
  plt.title(f'Boxplot  - {k}')
  plt.subplots_adjust(left=0.5,
                    bottom=0.5,
                    right=1.9,
                    top=0.9,
                    wspace=1.4,
                    hspace=1.4)
  plt.show()

  contar=contar+1

def salvando(df):
  df.to_csv("sem_outliers_" + files[contador] , index="False")

contador=0
lista=["nao","nao","nao","nao","nao","nao"]

# Verifique se os separadores de decimais estão corretos:

while contador < 1 :
  df=pd.read_csv(files_xlsx[contador],sep=",",decimal = '.', dtype = {"UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)":np.float64,'PRECIPITACAO TOTAL, DIARIO (AUT)(mm)':np.float64,"TEMPERATURA MAXIMA, DIARIA (AUT)(°C)": np.float64,"TEMPERATURA MINIMA, DIARIA (AUT)(°C)":np.float64,"UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)": np.float64,"VENTO, VELOCIDADE MEDIA DIARIA (AUT)(m/s)": np.float64})
  print(f"{contador+1}° Planilha : ")


  #df=df.drop("Unnamed: 0", axis=1)
  df=df.dropna()
  df=df.rename(columns={"PRECIPITACAO TOTAL, DIARIO (AUT)(mm)":'Prec(mm)',"TEMPERATURA MINIMA, DIARIA (AUT)(°C)":'TMin(°C)',"TEMPERATURA MAXIMA, DIARIA (AUT)(°C)":'TMax(°C)',"UMIDADE RELATIVA DO AR, MEDIA DIARIA (AUT)(%)":'UR(%)',"VENTO, VELOCIDADE MEDIA DIARIA (AUT)(m/s)":'U2(m/s)',"RADIACAO GLOBAL(Mj/m²)":'RAD(MJ/m²)'})
  df=df.drop("Unnamed: 0",axis=1)

  graficos(df)

  df=df[df["ANO"]>2008]
  df=df.drop(["ANO","MES","DIA"],axis=1)

  print(df.skew())

  #k1=input("A distribuição é simétrica para chuva? ")
  #k2=input("A distribuição é simétrica para temperatura maxima? ")
  #k3=input("A distribuição é simétrica para temperatura minima? ")
  #k4=input("A distribuição é simétrica para umidade? ")
  #k5=input("A distribuição é simétrica para vento? ")
  #k6=input("A distribuição é simétrica para radiacao? ")

  #lista.append(k1)
  #lista.append(k2)
  #lista.append(k3)
  #lista.append(k4)
  #lista.append(k5)
  #lista.append(k6)


  removendo_outliers(df)
  configurando_data(df)

  df=df.drop(["ANO","MES","DIA"],axis=1)

  salvando(df)
  contador=contador+1

  print(lista)

df=df.loc[df["RAD(MJ/m²)"] < 20]

df=df.to_csv("TESTE.csv")

df