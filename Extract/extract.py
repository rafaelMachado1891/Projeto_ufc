import requests
from bs4 import BeautifulSoup

def extrair_estatiticas_por_minuto(soup, legenda):
    numbers = {}
    secao = soup.find_all('div', class_='stats-records--compare stats-records-inner')

    for iteracao in secao:
        div = iteracao.find('div')
        if div and legenda in div.text:
            

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

url = "https://www.ufc.com.br/athlete/alex-pereira"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Coletar dados dos golpes significativos
    golpes_significativos = extrair_estatisticas_por_titulo(soup, 'Precisão de striking')
    
    # Coletar dados de precisão de quedas
    precisao_quedas = extrair_estatisticas_por_titulo(soup, 'Precisão De Quedas')

    estatiticas_por_minuto = soup.find('div', 'stats-records--compare stats-records-inner').text.strip()
    print(estatiticas_por_minuto)
    
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

        data.append(atleta_data)

    if data:
        print(data)
    else:
        print("Não foi possível extrair os dados")
else:
    print("Erro ao acessar a página:", response.status_code)