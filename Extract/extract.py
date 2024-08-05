# extract.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
from funcoes import obter_links, obter_resposta, coletar_informacoes_principais

# URL principal
url_principal = 'https://www.ufc.com.br/athletes'

# Função principal para coletar informações dos lutadores
def coletar_informacoes_dos_lutadores(url):
    links = obter_links(url)
    todas_informacoes = []

    for link in links:
        response = obter_resposta(link)
        if response:
            soup = BeautifulSoup(response.text, 'html.parser')
            informacoes = coletar_informacoes_principais(soup)
            todas_informacoes.extend(informacoes)

    return todas_informacoes

# Coletar informações dos lutadores
informacoes_lutadores = coletar_informacoes_dos_lutadores(url_principal)

# Salvar os dados em um arquivo Parquet
df = pd.DataFrame(informacoes_lutadores)
df.to_parquet('../data/dados.parquet', index=False)
