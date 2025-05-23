import requests
from bs4 import BeautifulSoup
import pandas as pd

# Função para obter a resposta da URL
def obter_resposta(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar a página: {response.status_code}")
        return None
    return response

# Função para obter links dos lutadores
def obter_links(url):
    response = obter_resposta(url)
    if not response:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    secoes = soup.find_all('section', class_='l-listing--stacked--full-width')
    links_lutadores = []

    for secao in secoes:
        lutadores = secao.find_all('span', class_='ath-n__name ath-lf-fl')
        for lutador in lutadores:
            link_element = lutador.find('a')
            if link_element:
                link = link_element.get('href')
                if link:
                    full_link = f"https://www.ufc.com.br{link}"
                    links_lutadores.append(full_link)
    return links_lutadores

# Função para extrair estatísticas por título
def extrair_estatisticas_por_titulo(soup, titulo):
    estatisticas = {}
    sections = soup.find_all('div', class_='c-overlap__inner')

    for section in sections:
        h2 = section.find('h2')
        if h2 and titulo in h2.text:
            stats_wrap = section.find('div', class_='c-overlap__stats-wrap')
            stats = stats_wrap.find_all('dl', class_='c-overlap__stats')
            for stat in stats:
                stat_text = stat.find('dt', class_='c-overlap__stats-text').text.strip()
                stat_value = stat.find('dd', class_='c-overlap__stats-value').text.strip()
                estatisticas[stat_text] = stat_value
            break
    return estatisticas

# Função para extrair dados específicos
def extrair_dados_especificos(soup):
    estatisticas = {
        'Golpes Sig. Conectados por Minuto': None,
        'Golpes Sig. Absorvidos por Minuto': None,
        'Média de Quedas por 15 Min': None,
        'Média de Finalizações por 15 Min': None,
        'Defesa de Golpes Sig.': None,
        'Defesa de Quedas': None,
        'Média de Knockdowns': None,
        'Tempo médio de luta': None,
        'Golpes Sig. Em pé': None,
        'Golpes Sig. Clinche': None,
        'Golpes Sig. Solo': None,
        'KO/TKO': None,
        'DEC': None,
        'FIN ': None
    }

    stat_labels = {
        'Golpes Sig. Conectados por Minuto': 'Golpes Sig. Conectados',
        'Golpes Sig. Absorvidos por Minuto': 'Golpes Sig. Absorvidos',
        'Média de Quedas por 15 Min': 'Média de quedas',
        'Média de Finalizações por 15 Min': 'Média de finalizações',
        'Defesa de Golpes Sig.': 'Defesa de Golpes Sig.',
        'Defesa de Quedas': 'Defesa De Quedas',
        'Média de Knockdowns': 'Média de Knockdowns',
        'Tempo médio de luta': 'Tempo médio de luta',
        'Golpes Sig. Em pé': 'Em pé',
        'Golpes Sig. Clinche': 'Clinche',
        'Golpes Sig. Solo': 'Solo',
        'KO/TKO': 'KO/TKO',
        'DEC': 'DEC',
        'FIN ': 'FIN'
    }

    stat_compare_divs = soup.find_all('div', class_='c-stat-compare--no-bar')

    for stat_div in stat_compare_divs:
        groups = stat_div.find_all('div', class_='c-stat-compare__group')
        for group in groups:
            label = group.find('div', class_='c-stat-compare__label').text.strip()
            number = group.find('div', class_='c-stat-compare__number').text.strip()
            if label in stat_labels.values():
                estatisticas[list(stat_labels.keys())[list(stat_labels.values()).index(label)]] = number

    stat_3bar_divs = soup.find_all('div', class_='c-stat-3bar__legend')
    for stat_div in stat_3bar_divs:
        groups = stat_div.find_all('div', class_='c-stat-3bar__group')
        for group in groups:
            label = group.find('div', class_='c-stat-3bar__label').text.strip()
            value = group.find('div', class_='c-stat-3bar__value').text.strip()
            if label in stat_labels.values():
                estatisticas[list(stat_labels.keys())[list(stat_labels.values()).index(label)]] = value

    return estatisticas

# Função para extrair golpes por área
def extrair_golpes_por_area(soup):
    areas = {
        'Cabeça': None,
        'Corpo': None,
        'Pernas': None
    }

    stat_body_diagram = soup.find('div', class_='c-stat-body__diagram')
    if stat_body_diagram:
        head = stat_body_diagram.find('g', id='e-stat-body_x5F__x5F_head-txt')
        if head:
            areas['Cabeça'] = head.find('text', id='e-stat-body_x5F__x5F_head_value').text.strip()

        body = stat_body_diagram.find('g', id='e-stat-body_x5F__x5F_body-txt')
        if body:
            areas['Corpo'] = body.find('text', id='e-stat-body_x5F__x5F_body_value').text.strip()

        leg = stat_body_diagram.find('g', id='e-stat-body_x5F__x5F_leg-txt')
        if leg:
            areas['Pernas'] = leg.find('text', id='e-stat-body_x5F__x5F_leg_value').text.strip()

    return areas

# Função para coletar informações principais
def coletar_informacoes_principais(soup):
    dados_especificos = extrair_dados_especificos(soup)
    golpes_significativos = extrair_estatisticas_por_titulo(soup, 'Precisão de striking')
    precisao_quedas = extrair_estatisticas_por_titulo(soup, 'Precisão De Quedas')
    golpes_por_area = extrair_golpes_por_area(soup)

    data = []

    resultado = soup.find_all('div', class_="hero-profile")
    for result in resultado:
        categoria = result.find('p', class_="hero-profile__division-title").text.strip() if result.find('p', class_="hero-profile__division-title") else None
        atleta = result.find('h1', class_="hero-profile__name").text.strip() if result.find('h1', class_="hero-profile__name") else None
        record = result.find('p', class_="hero-profile__division-body").text.strip() if result.find('p', class_="hero-profile__division-body") else None
        ultima_luta = result.find('h3', class_="c-card-event--athlete-fight__headline").text.strip() if result.find('h3', class_="c-card-event--athlete-fight__headline") else None
        imagem = result.find('div', class_='hero-profile__image-wrap').find('img')
        imagem_src = imagem['src'] if imagem else None

        atleta_data = {
            'Categoria': categoria,
            'Atleta': atleta,
            'Recorde': record,
            'Ultima_Luta': ultima_luta,
            'Foto': imagem_src
        }

        atleta_data.update(golpes_significativos)
        atleta_data.update(precisao_quedas)
        atleta_data.update(dados_especificos)
        atleta_data.update(golpes_por_area)

        data.append(atleta_data)

    return data

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

# URL principal
url_principal = 'https://www.ufc.com.br/athletes'

# Coletar informações dos lutadores
informacoes_lutadores = coletar_informacoes_dos_lutadores(url_principal)

df = pd.DataFrame(informacoes_lutadores)
print(df)
df.to_parquet('../data/dados.parquet', index=False)
