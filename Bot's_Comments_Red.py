from google.colab import files
files.upload()

import pandas as pd
import numpy as np
from collections import Counter
import re

df_total = pd.read_csv('Delmazo_twitter.csv')                                            #Archivo CSV que vaya a ingresar dentro del programa
df_total= df_total.drop(df_total[df_total['twitter_type'] != 'Tweet'].index)             #Elimina una columna de acuerdo con el tipo de dato
df_total = df_total.fillna('')
#df_total['']=df_total[''].str.replace('[#,&,:,-,\,/,_,=,+,*,,,...,$,<,>,[,],]','')   
df_total['created_at']= pd.to_datetime(df_total['created_at'])
df_total=df_total.drop(columns=['timeset','emoji_html_decimal','emoji_utf8','emoji_alias','description','friends_count','followers_count','real_name','location','place_type','place_fullname','place_name','quoted_status_permalink','profile_image','lang','possibly_sensitive','place_country','twitter_type'])

def contador(palabras_totales,longitud):                                                 #Iterador que cuenta las palabras más repetidas dentro de una columna, evitando que se repitan y colocando la cantidad de palabras que quieras en un DF
  x=Counter(' '.join(df_total["Label"]).split()).most_common(palabras_totales)           #Este es el extractor de palabras en una columna
  df_toC = pd.DataFrame(x)
  df_toC.rename(columns={0:'Termino',1:'Frecuencia'}, inplace=True)
  df_toC['Termino']=df_toC['Termino'].str.replace('[#,&,:,-,\,/,_,=,+,*,,,...,$]','')    #Cambia al caracter especial por un espacio vacio en una columna en especifico del DF, permitiendo que se haga una tabla con las palabras repetidas pero sin alterarse ninguno de sus caracteres
  df_toC=df_toC.drop(df_toC[df_toC['Termino'].str.len() < longitud].index)               #Filtra las palabras deacuerdo con su longitud (numero de caracteres)
  df_toC.reset_index(drop=True, inplace=True)
  df_toC['Repeated'] = df_toC.duplicated(['Termino'], keep=False)

  df_repetido=df_toC['Frecuencia'].groupby(df_toC['Termino']).sum()                      #Suma los terminos iguales en el DF, para eso se transforman sus caracteres especiales
  df_repetido=pd.DataFrame(df_repetido).reset_index()               
  df_repetido = df_repetido.sort_values(by=['Frecuencia'], ascending= False)
  df_repetido.reset_index(inplace=True)
  df_repetido=df_repetido.drop(columns=['index'])
  return df_repetido

def Xbots (no_elements):                                                                 #Esta funcion usa las palabras generadas por el contador para generar una lista de palabras
  ls=list(row for row in df_repetido['Termino'])
  ls=ls[:no_elements]
  print(type(ls))
  return ls

def ACSM (DataFrame,no_palabras):                                                        #Esta funcion usa la funcion Xbots para definir cuales seran las palabras utilizadas para reducir los comentarios de los bots en el DF, el cual se usa a si mismo una y otra vez para filtra aun mas la busqueda 
  for z in Xbots(no_palabras):                                                           #Usa la variable z para iterar la lista generada en Xbots
    DataFrame['Find'] = DataFrame['Label'].str.find(z)                                   #Encuentra las palabras en el DF
    DataFrame = DataFrame.sort_values(by=['Find'])
    DataFrame.drop(DataFrame[DataFrame['Find'] >= 0].index, inplace=True)                #Find genera numeros enteros mayores a 0, por lo cual eliminara los resultados de los bots porque son parecidos
    DataFrame=DataFrame.drop(columns=['Find'])
  return DataFrame

contador(100,4)                                                                          #No es un analisis 100% automatico, pero si resta muchos comentarios de bots innecesarios en el analisis de datos de acuerdo al entendimiento del usuario
df_total = ACSM(df_total,35)
df_total

