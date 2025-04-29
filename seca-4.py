import pandas as pd
import plotly.express as px

# Carregar os dados do arquivo Excel
file_path = "IIS_Brasil_2024_01.xlsx"
df = pd.read_excel(file_path, sheet_name="IIS")

# Definir categorias de seca
seca_classes = {
    6: "Excepcional",
    5: "Extrema",
    4: "Severa",
    3: "Moderada",
    2: "Fraca",
    1: "Normal"
}

# Filtrar os dados mais recentes (última coluna IIS6_0124)
ultima_coluna = "IIS6_0124"
df['Classificação'] = df[ultima_coluna].map(seca_classes)

# Contar o número de cidades por UF e por classe de seca
contagem_seca = df.groupby(['UF', 'Classificação']).size().reset_index(name='Número de Cidades')

# Pivotar os dados para facilitar a visualização
contagem_pivot = contagem_seca.pivot(index='UF', columns='Classificação', values='Número de Cidades').fillna(0)

# Calcular a classe predominante em cada UF
contagem_pivot['Classe Predominante'] = contagem_pivot.idxmax(axis=1)

# Criar o mapa interativo usando Plotly com tons terrosos
mapa_brasil = px.choropleth(
    contagem_pivot.reset_index(),
    geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
    locations='UF',
    featureidkey="properties.sigla",
    color='Classe Predominante',
    title="Mapa das Secas no Brasil por UF",
    labels={'Classe Predominante': 'Seca'},
    color_discrete_map={
        "Excepcional": "#8B4513",  # Marrom escuro
        "Extrema": "#A0522D",      # Sienna
        "Severa": "#D2691E",       # Chocolate
        "Moderada": "#CD853F",     # Peru
        "Fraca": "#DEB887",        # Bege claro
        "Normal": "#F5DEB3"        # Trigo
    }
)

mapa_brasil.update_geos(fitbounds="locations", visible=False)
mapa_brasil.show()
