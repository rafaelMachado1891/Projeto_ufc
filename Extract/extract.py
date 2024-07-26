import requests
from bs4 import BeautifulSoup

def coletar_dados_div(soup, div_class, stats_texts):
    """
    Coleta dados de uma div específica com base na classe e textos das estatísticas.
    
    :param soup: Objeto BeautifulSoup da página web.
    :param div_class: Classe da div que contém as estatísticas.
    :param stats_texts: Dicionário onde as chaves são os textos que identificam as estatísticas e os valores são os nomes das variáveis para armazená-los.
    :return: Dicionário com os dados coletados.
    """
    div = soup.find('div', class_=div_class)
    dados = {key: None for key in stats_texts.values()}
    
    if div:
        stats = div.find_all('div', class_='athlete-stats__stat')
        for stat in stats:
            stat_value = stat.find('p', class_='athlete-stats__text athlete-stats__stat-numb').text.strip()
            stat_text = stat.find('p', class_='athlete-stats__text athlete-stats__stat-text').text.strip()
            for key, value in stats_texts.items():
                if key in stat_text:
                    dados[value] = stat_value
                    break
    
    return dados

url = "https://www.ufc.com.br/athlete/alex-pereira"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Dicionário com os textos das estatísticas e os nomes das variáveis
    stats_texts = {
        'Wins by Knockout': 'vitorias_por_nocaute',
        'First Round Finishes': 'vitorias_primeiro_round'
    }
    
    # Coletar dados das estatísticas
    estatisticas = coletar_dados_div(soup, 'stats-records-inner', stats_texts)

    data = []
    resultado = soup.find_all('div', class_="hero-profile")
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
            'Vitorias por Nocaute': estatisticas['vitorias_por_nocaute'],
            'Vitorias no Primeiro Round': estatisticas['vitorias_primeiro_round']
        })

    if data:
        print(data)
    else:
        print("Não foi possível extrair os dados")
else:
    print("Erro ao acessar a página:", response.status_code)