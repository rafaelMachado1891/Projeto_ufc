import requests
from bs4 import BeautifulSoup

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
    
    # Extrair dados de golpes significativos por posição
    stat_3bar_divs = soup.find_all('div', class_='c-stat-3bar__legend')
    for stat_div in stat_3bar_divs:
        groups = stat_div.find_all('div', class_='c-stat-3bar__group')
        for group in groups:
            label = group.find('div', class_='c-stat-3bar__label').text.strip()
            value = group.find('div', class_='c-stat-3bar__value').text.strip()
            if label in stat_labels.values():
                estatisticas[list(stat_labels.keys())[list(stat_labels.values()).index(label)]] = value

    return estatisticas

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

url = "https://www.ufc.com.br/athlete/alexandre-pantoja"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Coletar dados específicos
    dados_especificos = extrair_dados_especificos(soup)

    # Coletar dados dos golpes significativos
    golpes_significativos = extrair_estatisticas_por_titulo(soup, 'Precisão de striking')
    
    # Coletar dados de precisão de quedas
    precisao_quedas = extrair_estatisticas_por_titulo(soup, 'Precisão De Quedas')

    # Coletar dados de golpes por área
    golpes_por_area = extrair_golpes_por_area(soup)

    atletas = 'https://www.ufc.com.br/athletes'
    lista = requests.get(atletas)
    soup_atletas = BeautifulSoup(lista.text, 'html.parser')
    secoes = soup_atletas.find_all('section', class_='l-listing--stacked--full-width')

# Inicialize uma lista para armazenar os links
links_lutadores = []

for secao in secoes:
    # Encontre todos os elementos <span> com as classes corretas
    lutadores = secao.find_all('span', class_='ath-n__name ath-lf-fl')
    for lutador in lutadores:
        # Dentro de cada <span>, encontre o elemento <a> e obtenha o atributo href
        link_element = lutador.find('a')
        if link_element:
            link = link_element.get('href')
            if link:
                full_link = f"https://www.ufc.com.br{link}"
                links_lutadores.append(full_link)

                print(links_lutadores)
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

        # Adicionar estatísticas ao dicionário do atleta
        atleta_data.update(golpes_significativos)
        atleta_data.update(precisao_quedas)
        atleta_data.update(dados_especificos)
        atleta_data.update(golpes_por_area)

        data.append(atleta_data)

    if data:
        print(data)
    else:
        print("Não foi possível extrair os dados")
else:
    print("Erro ao acessar a página:", response.status_code)

