import requests
from bs4 import BeautifulSoup

url = "https://www.ufc.com.br/athlete/alex-pereira"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar a div principal com a classe 'hero-profile'
    resultado = soup.find_all('div', class_="hero-profile")

    # Encontrar a div com a classe 'c-overlap__stats-wrap'
    precisao_strike = soup.find('div', class_='c-overlap__stats-wrap')

    golpes_conectados = None
    golpes_desferidos = None
    
    if precisao_strike:
        stats = precisao_strike.find_all('dl', class_='c-overlap__stats')
        for stat in stats:
            stat_text = stat.find('dt', class_='c-overlap__stats-text').text.strip()
            stat_value = stat.find('dd', class_='c-overlap__stats-value').text.strip()
            if 'Golpes Sig. Conectados' in stat_text:
                golpes_conectados = stat_value
            elif 'Golpes Sig. Desferidos' in stat_text:
                golpes_desferidos = stat_value

    data = []
    for result in resultado:
        categoria = result.find('p', class_="hero-profile__division-title").text.strip() if result.find('p', class_="hero-profile__division-title") else None
        atleta = result.find('h1', class_="hero-profile__name").text.strip() if result.find('h1', class_="hero-profile__name") else None
        record = result.find('p', class_="hero-profile__division-body").text.strip() if result.find('p', class_="hero-profile__division-body") else None
        ultima_luta = result.find('h3', class_="c-card-event--athlete-fight__headline").text.strip() if result.find('h3', class_="c-card-event--athlete-fight__headline") else None
        imagem = result.find('div', class_='hero-profile__image-wrap').find('img')
        imagem_src = imagem['src'] if imagem else None

        data.append({
            'Categoria': categoria,
            'Atleta': atleta,
            'Recorde': record,
            'Ultima_Luta': ultima_luta,
            'Foto': imagem_src,
            'Golpes Sig. Conectados': golpes_conectados,
            'Golpes Sig. Desferidos': golpes_desferidos
        })

    if data:
        print(data)
    else:
        print("Não foi possível extrair os dados")
else:
    print("Erro ao acessar a página:", response.status_code)