# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 18:45:11 2022

https://queroficarrico.com/blog/utilidade-domestica-periodo-de-safras-de-frutas-verduras-e-pescados/
fonte: CEAGESP

@author: CKT
"""


import pandas as pd
import requests


# =============================================================================
# Scrape da tabela de alimentos da URL
# =============================================================================

## URL 
url = "https://queroficarrico.com/blog/utilidade-domestica-periodo-de-safras-de-frutas-verduras-e-pescados/"

## Cabeçalho de solicitação HTTP
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

## Solicitação das informações da URL
req = requests.get(url, headers=header)

## Scrape da URL solicitada
dfs = pd.read_html(req.text)[0]



# =============================================================================
# Processamento dos dados 
# =============================================================================

## Listas utilizadas para criar a tabela final - tabelaMesesAlimentos[meses, alimentos]
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
alimentos = ['Frutas', 'Legumes', 'Verduras', 'Pescados']

## Tabela final
tabelaMesesAlimentos = pd.DataFrame([],index=meses, columns=alimentos)

## Processamento dos dados
for i in range(0,len(meses)):
    for j in  range(0,len(alimentos)):
        for ii in dfs.index:
            for jj in dfs.columns:
                if meses[i].lower() in dfs.loc[ii, jj].lower() and alimentos[j].lower() in dfs.loc[ii, jj].lower():
                    textoSeparado = dfs.loc[ii, jj]
                    break
            
        textoSeparado = textoSeparado.replace(meses[i].upper(), '')
        
        if alimentos[j] != alimentos[-1]:
            textoSeparado = textoSeparado[textoSeparado.lower().find(alimentos[j].lower()):textoSeparado.lower().find(alimentos[j+1].lower())]
        else:
            textoSeparado = textoSeparado[textoSeparado.lower().find(alimentos[j].lower()):]
        
        tabelaMesesAlimentos.loc[meses[i],alimentos[j]] = textoSeparado.replace(alimentos[j].upper(), '').strip()
        
## Salva a tabela final ".CSV" (encoding para diferentes tipos de Sistemas Operacionais)
# tabelaMesesAlimentos.to_csv('tabela-safra-mensal-de-alimentos.csv',encoding='utf-8')
# tabelaMesesAlimentos.to_csv('tabela-safra-mensal-de-alimentos.csv',encoding='utf-8-sig')
tabelaMesesAlimentos.to_csv('tabela-safra-mensal-de-alimentos.csv',encoding='latin-1')