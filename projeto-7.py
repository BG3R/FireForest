import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

#Colunas utilizadas

#estado : Para identificar o número de ocorrências por estado.
#bioma : Para categorizar os incêndios por biomas.
#frp : Para analisar a distribuição do poder radiativo do fogo.
#numero_dias_sem_chuva e risco_fogo : Para correlacionar dias sem chuva com o risco de fogo.
#data_pas : Para analisar a sazonalidade dos incêndios ao longo dos meses.

#Gráficos gerados

#Barras para contagem por estado e bioma.
#Histogramas para distribuição do FRP.
#Gráficos dispersos para relação entre dias sem chuva e risco de fogo.
#Barras empilhadas para ocorrências por mês e bioma.


# Carregar os dados do arquivo CSV
file_path = 'focos_br_todos-sats_2024.csv'
data = pd.read_csv(file_path)

# Converter a coluna de datas para o formato datetime
data['data_pas'] = pd.to_datetime(data['data_pas'])
data['mes'] = data['data_pas'].dt.month  # Extrair o mês da data

# Função para gerar gráficos
def plot_and_save(title, xlabel, ylabel, data, kind='bar', filename=None):
    data.plot(kind=kind, figsize=(10, 6), legend=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
    plt.show()

# Número de ocorrências de incêndios por estado
ocorrencias_por_estado = data['estado'].value_counts()
plot_and_save(
    title='Número de Ocorrências de Incêndios por Estado',
    xlabel='Estado',
    ylabel='Número de Ocorrências',
    data=ocorrencias_por_estado,
    filename='ocorrencias_por_estado.png'
)


# Contar o número de ocorrências por estado
ocorrencias_por_estado = data['estado'].value_counts()

# Estados com mais e menos ocorrências (top 17 e bottom 10)
top_17_estados = ocorrencias_por_estado.head(17)
bottom_10_estados = ocorrencias_por_estado.tail(10)

# Imprimir os estados com mais ocorrências no console
print("Top 17 estados com mais ocorrências:")
print(top_17_estados)

# Imprimir os estados com menos ocorrências no console
print("\nTop 10 estados com menos ocorrências:")
print(bottom_10_estados)

# Gráfico dos estados com mais ocorrências
plt.figure(figsize=(14, 7))
top_17_estados.plot(kind='bar', color='blue')
plt.title('Top 17 Estados com Mais Ocorrências de Incêndios')
plt.xlabel('Estado')
plt.ylabel('Número de Ocorrências')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_17_estados_mais_ocorrencias.png')
plt.show()

# Gráfico dos estados com menos ocorrências
plt.figure(figsize=(12, 6))
bottom_10_estados.plot(kind='bar', color='red')
plt.title('Top 10 Estados com Menos Ocorrências de Incêndios')
plt.xlabel('Estado')
plt.ylabel('Número de Ocorrências')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_10_estados_menos_ocorrencias.png')
plt.show()

# Encontrar o estado com mais e menos ocorrências
estado_mais_ocorrencias = ocorrencias_por_estado.idxmax()
estado_menos_ocorrencias = ocorrencias_por_estado.idxmin()

print(f"\nEstado com mais ocorrências: {estado_mais_ocorrencias} ({ocorrencias_por_estado.max()})")
print(f"Estado com menos ocorrências: {estado_menos_ocorrencias} ({ocorrencias_por_estado.min()})")


# Número de ocorrências de incêndios por bioma
ocorrencias_por_bioma = data['bioma'].value_counts()
plot_and_save(
    title='Número de Ocorrências de Incêndios por Bioma',
    xlabel='Bioma',
    ylabel='Número de Ocorrências',
    data=ocorrencias_por_bioma,
    filename='ocorrencias_por_bioma.png'
)

# Número de ocorrências por mês e bioma
ocorrencias_mes_bioma = data.groupby(['mes', 'bioma']).size().unstack()
ocorrencias_mes_bioma.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Número de Ocorrências por Mês e Bioma')
plt.xlabel('Mês')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('ocorrencias_mes_bioma.png')
plt.show()

# Distribuição do poder radiativo do fogo (FRP)
sns.histplot(data['frp'], kde=True, bins=30)
plt.title('Distribuição do Poder Radiativo do Fogo (FRP)')
plt.xlabel('FRP')
plt.ylabel('Frequência')
plt.tight_layout()
plt.savefig('distribuicao_frp.png')
plt.show()

# Relação entre número de dias sem chuva e risco de fogo
sns.scatterplot(x=data['numero_dias_sem_chuva'], y=data['risco_fogo'])
plt.title('Relação entre Dias sem Chuva e Risco de Fogo')
plt.xlabel('Dias sem Chuva')
plt.ylabel('Risco de Fogo')
plt.tight_layout()
plt.savefig('relacao_dias_sem_chuva_risco_fogo.png')
plt.show()

# Ocorrências ao longo dos meses
ocorrencias_mensais = data.groupby('mes').size()
plot_and_save(
    title='Ocorrências de Incêndios ao Longo dos Meses',
    xlabel='Mês',
    ylabel='Número de Ocorrências',
    data=ocorrencias_mensais,
    filename='ocorrencias_mensais.png'
)

# Distribuição do número de dias sem chuva
dias_sem_chuva = data['numero_dias_sem_chuva'].value_counts().sort_index()
plot_and_save(
    title='Distribuição do Número de Dias sem Chuva',
    xlabel='Dias sem Chuva',
    ylabel='Frequência',
    data=dias_sem_chuva,
    filename='dias_sem_chuva.png'
)

# Carregar os dados do arquivo CSV
file_path = 'focos_br_todos-sats_2024.csv'  # Substitua pelo caminho correto do arquivo
data = pd.read_csv(file_path)

# Carregar o GeoJSON do Brasil (disponível publicamente ou use outro arquivo apropriado)
geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

# Ajustar os dados para contagem de ocorrências por estado
ocorrencias_por_estado = data['estado'].value_counts().reset_index()
ocorrencias_por_estado.columns = ['estado', 'ocorrencias']

# Criar um dicionário para normalizar os nomes dos estados (caso necessário)
estado_nome_map = {
    "ACRE": "Acre",
    "ALAGOAS": "Alagoas",
    "AMAZONAS": "Amazonas",
    "BAHIA": "Bahia",
    "CEARÁ": "Ceará",
    "DISTRITO FEDERAL": "Distrito Federal",
    "ESPÍRITO SANTO": "Espírito Santo",
    "GOIÁS": "Goiás",
    "MARANHÃO": "Maranhão",
    "MATO GROSSO": "Mato Grosso",
    "MATO GROSSO DO SUL": "Mato Grosso do Sul",
    "MINAS GERAIS": "Minas Gerais",
    "PARÁ": "Pará",
    "PARAÍBA": "Paraíba",
    "PARANÁ": "Paraná",
    "PERNAMBUCO": "Pernambuco",
    "PIAUÍ": "Piauí",
    "RIO DE JANEIRO": "Rio de Janeiro",
    "RIO GRANDE DO NORTE": "Rio Grande do Norte",
    "RIO GRANDE DO SUL": "Rio Grande do Sul",
    "RONDÔNIA": "Rondônia",
    "RORAIMA": "Roraima",
    "SANTA CATARINA": "Santa Catarina",
    "SÃO PAULO": "São Paulo",
    "SERGIPE": "Sergipe",
    "TOCANTINS": "Tocantins"
}

# Normalizar os nomes dos estados no DataFrame
ocorrencias_por_estado['estado'] = ocorrencias_por_estado['estado'].map(estado_nome_map)

# 1º Gráfico: Ocorrências de incêndios por estado
fig1 = px.choropleth(
    ocorrencias_por_estado,
    geojson=geojson_url,
    locations='estado',
    featureidkey='properties.name',
    color='ocorrencias',
    color_continuous_scale="Reds",
    title="Ocorrências de Incêndios por Estado no Brasil"
)
fig1.update_geos(fitbounds="locations", visible=False)
fig1.show()

# 2º Gráfico: Mapeamento de áreas de risco (baseado no risco_fogo médio por estado)
risco_fogo_por_estado = data.groupby('estado')['risco_fogo'].mean().reset_index()
risco_fogo_por_estado.columns = ['estado', 'risco_fogo']
risco_fogo_por_estado['estado'] = risco_fogo_por_estado['estado'].map(estado_nome_map)

fig2 = px.choropleth(
    risco_fogo_por_estado,
    geojson=geojson_url,
    locations='estado',
    featureidkey='properties.name',
    color='risco_fogo',
    color_continuous_scale="Oranges",
    title="Mapeamento de Áreas de Risco de Incêndio no Brasil"
)
fig2.update_geos(fitbounds="locations", visible=False)
fig2.show()


print("Análise concluída! Os gráficos foram gerados e salvos.")