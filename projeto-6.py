# @title **4 - Importando Bibliotecas**

import numpy as np
import pandas as pd
import plotly.express as px
from IPython.display import Image
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from folium.features import DivIcon
from folium.plugins import HeatMapWithTime
import plotly.subplots as sp
import matplotlib.image as mpimg
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from folium import plugins
import scipy.stats as stats
import matplotlib.image as mpimg
import warnings
warnings.filterwarnings('ignore')


# @title **5 - Carregando e Verificando a Base de dados**

Base_Dados = pd.read_csv('Incendios.csv', sep = ';')
Base_Dados.head()

# @title **6 - Tamanho da Base**

Base_Dados.shape

# @title **7 - Informações da Base**

Base_Dados.info()

# @title **8 - Valores Unicos**

Base_Dados.nunique()

# @title **9 - Valores Nulos**
Base_Dados.isnull().sum()

# @title **10 - Verificando total de colunas**

Base_Dados.columns

# @title **11 - Gerando Grafico De Campos Nulos**


plt.figure( figsize=(15,6) )
plt.title('Analisando Campos Nulos')
sns.heatmap( Base_Dados.isnull(), cbar=False );


print("Como podemos ver o grafico acima indica que não temos nenhum valor faltante na nossa base de dados\n")

# @title **12 - Relação Anos e Incêndios**

years = list(Base_Dados.year.unique())

quantincendios = []

def convert_to_Int(number):

  if str(number)[-2] == '.':

    return int(str(number)[:-2])

  if str(number)[1] == '.' or str(number)[2] == '.':

    return int(str(number).replace('.',''))

Base_Dados["number"] = Base_Dados.apply(lambda row: convert_to_Int(row["number"]), axis=1)

for i in years:
    total_incendios = Base_Dados.loc[Base_Dados['year'] == i].number.sum()
    quantincendios.append(total_incendios)

fire_year_dict = {'year': years, 'number': quantincendios}

analise = pd.DataFrame(fire_year_dict)

analise.head(12)

# @title **13 - Total de incêndios no Brasil por ano**

fig = go.Figure()


fig.add_trace(go.Scatter(
    x=analise['year'],
    y=analise['number'],
    mode='lines+markers',
    marker=dict(color='#16171B'),
    line=dict(width=2),
    opacity=0.85,
    name="Incêndios por ano"
))


max_year = 2020
max_value = analise['number'][analise['year'] == max_year].values[0]

fig.add_annotation(
    x=max_year,
    y=max_value,
    text=f"Ano com mais incêndios:",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40
)

min_value = analise['number'].min()
min_year = analise['year'][analise['number'] == min_value].values[0]

fig.add_annotation(
    x=min_year,
    y=min_value,
    text=f"Ano com menos incêndios",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=40
)

fig.update_layout(
    title='Total de Incêndios No Brasil Por Ano (2012 - 2023)',
    xaxis_title='Ano',
    yaxis_title='Número Total de Incêndios',
    title_x=0.5,
    width=1000,
    height=500
)

print ("Relação entre os anos e o número total de incêndios no Brasil de 2012 a 2023,destacando o ano com mais e menos incêndios.\n")
fig.show()

# @title **14 - Total de incêndios no Brasil por mêses**

analise_02 = Base_Dados.groupby(by=['year', 'month']).sum().reset_index()
ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
ordem_df = pd.DataFrame({'month': ordem_meses})

ordem_meses = ordem_df.merge(Base_Dados.groupby('month')['number'].sum().reset_index(), on='month', how='left').fillna(0)

ordem_meses = ordem_meses.sort_values(by='number', ascending=False)

fig = px.bar(ordem_meses, x='month', y='number', color='number', color_continuous_scale='RdYlGn_r')

fig.update_yaxes(showgrid=False)
fig.update_xaxes(showgrid=False)

mes_max_incendios = ordem_meses.iloc[0]['month']
mes_max_valor = ordem_meses.iloc[0]['number']

mes_min_incendios = ordem_meses.iloc[-1]['month']
mes_min_valor = ordem_meses.iloc[-1]['number']

fig.add_annotation(
    x=mes_max_incendios,
    y=mes_max_valor,
    text=f"Mês com mais incêndios: {mes_max_incendios} ({mes_max_valor} incêndios)",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    bgcolor="lightyellow"
)

fig.add_annotation(
    x=mes_min_incendios,
    y=mes_min_valor,
    text=f"Mês com menos incêndios: {mes_min_incendios} ({mes_min_valor} incêndios)",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    bgcolor="lightblue"
)

fig.update_layout(
    title='Total de Incêndios no Brasil por Mês (2012 - 2023)',
    xaxis_title='Meses',
    yaxis_title='Incêndios',
    plot_bgcolor='white',
    title_x=0.5,
    margin=dict(r=150)
)

print("Relação entre os meses e o número total de incêndios no Brasil de 2012 a 2023,destacando o mês com mais e menos incêndios.\n")
fig.show()

# @title **15 - Total de incêndios no Brasil por estados**
analise_03 = Base_Dados.groupby(by=['state', 'year']).sum().reset_index()

states = Base_Dados['state'].unique()

states_fire_data = []
for state in states:
    total_incendios = analise_03.loc[analise_03['state'] == state].number.sum()
    states_fire_data.append(total_incendios)

states_fires = {
    "Estados": states,
    "Incêncios": states_fire_data
}

fig = px.bar(
    states_fires,
    x='Estados',
    y='Incêncios',
    color='Estados',
    color_discrete_sequence=px.colors.qualitative.Set3,
)

fig.update_xaxes(categoryorder='total descending')

fig.update_yaxes(showgrid=False)
fig.update_xaxes(showgrid=False)

estado_max_incendios = states_fires['Estados'][states_fire_data.index(max(states_fire_data))]
max_valor = max(states_fire_data)

estado_min_incendios = states_fires['Estados'][states_fire_data.index(min(states_fire_data))]
min_valor = min(states_fire_data)

fig.add_annotation(
    x=estado_max_incendios,
    y=max_valor,
    text=f"Maior número de incêndios: {estado_max_incendios} ({max_valor} incêndios)",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    bgcolor="lightyellow"
)

fig.add_annotation(
    x=estado_min_incendios,
    y=min_valor,
    text=f"Menor número de incêndios: {estado_min_incendios} ({min_valor} incêndios)",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40,
    bgcolor="lightblue"
)

fig.update_layout(
    title='Estados Com Maior Número De Incêndios No Brasil  (2012 - 2022)',
    xaxis_title='Estado',
    yaxis_title='Incêndios',
    plot_bgcolor='white',
    title_x=0.5,
    margin=dict(r=150)
)
print("O total de incêndios por estado no Brasil de 2012 a 2022, destacando os estados com o maior e menor número de incêndios\n")

fig.show()

# @title **16 - Top 3 Estados com mais incêndios por ano**

years = list(Base_Dados['year'].unique())
if 2023 not in years:
    years.append(2023)

top_3_states = []
top_3_fire = []
top_3_rank = {}

max_values = list(states_fires['Incêncios'])


for i in range(0, 3):
    maxValue = max(max_values)
    idx = max_values.index(maxValue)
    max_values[idx] = 0
    top_3_states.append(states_fires['Estados'][idx])


for state in top_3_states:
    fire_per_year = []
    for year in years:

        fire_per_month = Base_Dados.loc[(Base_Dados.state == state) & (Base_Dados.year == year)].number
        fire_year = 0

        for current_fire in fire_per_month:
            fire_year += current_fire
        fire_per_year.append(fire_year)
    top_3_fire.append(fire_per_year)


lista_transformada = list(zip(*top_3_fire))
lista_final = [list(tupla) for tupla in lista_transformada]

top_3_rank["State"] = top_3_states


for i in range(len(years)):
    top_3_rank[str(years[i])] = lista_final[i]


df_top_3_rank = pd.DataFrame(top_3_rank)


df_top_3_rank = df_top_3_rank.melt(id_vars=['State'], var_name='Year', value_name='Fire')


fig = px.line(df_top_3_rank, x='Year', y='Fire', color='State',
              title='Top 3 Estados Com Incêndios Por Ano (2012 - 2023)',
              labels={'Year': 'Ano', 'Fire': 'Número de Incêndios', 'State': 'Estado'})


fig.update_layout(title_x=0.5)

print(" Os tres estados que sofrem o maior numero de queimadas por ano\n")
fig.show()

# @title **17 - Top 10 Estados com mais incêndios por ano**

years = list(Base_Dados['year'].unique())
if 2023 not in years:
    years.append(2023)

top_10_states = []
top_10_fire = []


top_10_rank = {}


max_values = list(states_fires['Incêncios'])


for i in range(0, 10):
    maxValue = max(max_values)
    idx = max_values.index(maxValue)
    max_values[idx] = 0
    top_10_states.append(states_fires['Estados'][idx])


for state in top_10_states:
    fire_per_year = []
    for year in years:

        fire_per_month = Base_Dados.loc[(Base_Dados.state == state) & (Base_Dados.year == year)].number
        fire_year = 0

        for current_fire in fire_per_month:
            fire_year += current_fire
        fire_per_year.append(fire_year)
    top_10_fire.append(fire_per_year)


lista_transformada = list(zip(*top_10_fire))


lista_final = [list(tupla) for tupla in lista_transformada]


top_10_rank["State"] = top_10_states


for i in range(len(years)):
    top_10_rank[str(years[i])] = lista_final[i]


df_top_10_rank = pd.DataFrame(top_10_rank)


df_top_10_rank = df_top_10_rank.melt(id_vars=['State'], var_name='Year', value_name='Fire')


fig = px.line(df_top_10_rank, x='Year', y='Fire', color='State',
              title='Top 10 Estados Com Incêndios Por Ano  (2012 - 2023)',
              labels={'Year': 'Ano', 'Fire': 'Número de Incêndios', 'State': 'Estado'})


fig.update_layout(title_x=0.5)

print("Os dez primeiros estados que mais sofrem com o numero de queimadas por ano\n")
fig.show()

# @title **18 - Total de incêndios por mes no estado do Pará**

dados_para = Base_Dados[Base_Dados['state'] == 'Pará']

analise_para = dados_para.groupby('month')['number'].sum().reset_index()

ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

ordem_df = pd.DataFrame({'month': ordem_meses})

analise_para = ordem_df.merge(analise_para, on='month', how='left').fillna(0)

analise_para = analise_para.sort_values(by='number', ascending=False)

fig = px.bar(analise_para, x='number', y='month', color='number', color_continuous_scale='RdYlGn_r', orientation='h')

fig.update_traces(texttemplate='%{x}', textposition='outside')

fig.update_yaxes(showgrid=False)

fig.update_xaxes(showgrid=False)

fig.update_layout(
    title='Total De Incêndios No Estado Do Pará Por Mês (2012 - 2022)',
    yaxis_title='Mês',
    xaxis_title='Incêndios',
    plot_bgcolor='white',
    title_x=0.5
)

print("Meses em que o estado do Pará é mais afetado pelas queimadas , destacando o segundo semetre do ano sendo o pior\n")

fig.show()

# @title **19 - Total de incêndios por mes no estado do Mato Grosso**

dados_matogrosso = Base_Dados[Base_Dados['state'] == 'Mato Grosso']

analise_matogrosso = dados_matogrosso.groupby('month')['number'].sum().reset_index()

ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

ordem_df = pd.DataFrame({'month': ordem_meses})

analise_matogrosso = ordem_df.merge(analise_matogrosso, on='month', how='left').fillna(0)

analise_matogrosso = analise_matogrosso.sort_values(by='number', ascending=False)

fig = px.bar(analise_matogrosso, x='number', y='month', color='number', color_continuous_scale='RdYlGn_r', orientation='h')

fig.update_traces(texttemplate='%{x}', textposition='outside')

fig.update_yaxes(showgrid=False)

fig.update_xaxes(showgrid=False)

fig.update_layout(
    title='Total De Incêndios No Estado Do Mato Grosso Por Mês (2012 - 2022)',
    yaxis_title='Mês',
    xaxis_title='Incêndios',
    plot_bgcolor='white',
    title_x=0.5
)

print("Meses em que o estado do Mato Grosso é mais afetado pelas queimadas , destacando o segundo semetre do ano sendo o pior seguindo o mesmo padrão que o do Pará\n")
fig.show()

# @title **20 - Total de incêndios por mes no estado do Maranhão**

dados_maranhao = Base_Dados[Base_Dados['state'] == 'Maranhão']

analise_maranhao = dados_maranhao.groupby('month')['number'].sum().reset_index()

ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

ordem_df = pd.DataFrame({'month': ordem_meses})

analise_maranhao = ordem_df.merge(analise_maranhao, on='month', how='left').fillna(0)

analise_maranhao = analise_maranhao.sort_values(by='number', ascending=False)

fig = px.bar(analise_maranhao, x='number', y='month', color='number', color_continuous_scale='RdYlGn_r', orientation='h')

fig.update_traces(texttemplate='%{x}', textposition='outside')


fig.update_yaxes(showgrid=False)

fig.update_xaxes(showgrid=False)

fig.update_layout(
    title='Total De Incêndios No Estado Do Maranhão Por Mês (2012 - 2022)',
    yaxis_title='Mês',
    xaxis_title='Incêndios',
    plot_bgcolor='white',
    title_x=0.5
)

print("Meses em que o estado do Maranhão é mais afetado pelas queimadas , destacando o segundo semetre do ano sendo o pior seguindo o mesmo padrão que o do Pará e o Mato Grosso\n")
fig.show()

# @title **21 - Adicionando Latitude e Longitude de cada Estado**

all_states_fire_data = []


for state in states:

    total_fires = analise_03.loc[analise_03['state'] == state].number.sum()
    all_states_fire_data.append(total_fires)

Lat = [-8.77, -9.62, 1.41, -3.47, -13.29, -5.20, -15.83, -19.19, -15.98, -5.42, -12.64, -20.51, -18.10, -3.79, -7.28, -24.89, -8.38, -6.60, -5.81, -30.17, -22.25, -10.83, 1.99, -27.45, -10.57, -22.19, -10.25]
Log = [-70.55, -36.82, -51.77, -65.10, -41.71, -39.53, -47.86, -40.34, -49.86, -45.44, -55.42, -54.54, -44.38, -52.48, -36.72, -51.55, -37.86, -42.28, -36.59, -53.50, -42.66, -63.34, -61.33, -50.95, -37.45, -48.79, -48.26]

Dicionario = {
    'Estado': states,
    'Latitude': Lat,
    'Longitude': Log,
    'Incêndios': all_states_fire_data
}

coordenadas = pd.DataFrame(Dicionario)

coordenadas.head()

# @title **22 - Mapa de Calor com cada Estado e o numero total de incendios**

m = folium.Map(location=[-15.7886, -47.9292], zoom_start=4)

radius = 20


heat_data = list(zip(coordenadas['Latitude'], coordenadas['Longitude'], coordenadas['Incêndios']))
folium.plugins.HeatMap(heat_data, radius=radius).add_to(m)

for _, row in coordenadas.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        icon=None,
        popup=f"{row['Estado']} - Total de Incêndios: {row['Incêndios']}"
    ).add_to(m)
m

# @title **23 - Média de Incendios por estado,ano e mes**

mean_by_state = Base_Dados.groupby('state')['number'].mean()

mean_by_month = Base_Dados.groupby('month')['number'].mean()

mean_by_year = Base_Dados.groupby('year')['number'].mean()

print("Média de incêndios por estado:\n")
for state, mean in mean_by_state.items():
    print(f"{state:<20}: {mean:.2f}")

print("\nMédia de incêndios por mês:\n")
for month, mean in mean_by_month.items():
    print(f"{month:<12}: {mean:.2f}")

print("\nMédia de incêndios por ano:\n")
for year, mean in mean_by_year.items():
    print(f"{year:<5}: {mean:.2f}")

    

# @title **25 - Mediana de Incendios por estado,ano e mes**

median_by_state = Base_Dados.groupby('state')['number'].median()


median_by_month = Base_Dados.groupby('month')['number'].median()


median_by_year = Base_Dados.groupby('year')['number'].median()


print("Mediana de incêndios por estado:\n")
for state, median in median_by_state.items():
    print(f"{state:<20}: {median:.2f}")

print("\nMediana de incêndios por mês:\n")
for month, median in median_by_month.items():
    print(f"{month:<12}: {median:.2f}")

print("\nMediana de incêndios por ano:\n")
for year, median in median_by_year.items():
    print(f"{year:<5}: {median:.2f}")

# @title **26 - Moda de Incendios por estado,ano e mes**

mode_by_state = Base_Dados.groupby('state')['number'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)

mode_by_month = Base_Dados.groupby('month')['number'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)

mode_by_year = Base_Dados.groupby('year')['number'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)

print("Moda de incêndios por estado:\n")
for state, mode in mode_by_state.items():
    print(f"{state:<20}: {mode:.2f}")

print("\nModa de incêndios por mês:\n")
for month, mode in mode_by_month.items():
    print(f"{month:<12}: {mode:.2f}")

print("\nModa de incêndios por ano:\n")
for year, mode in mode_by_year.items():
    print(f"{year:<5}: {mode:.2f}")




# @title **27 - Desvio Padrão por estado,ano e mes**

std_by_state = Base_Dados.groupby('state')['number'].std()

std_by_month = Base_Dados.groupby('month')['number'].std()

std_by_year = Base_Dados.groupby('year')['number'].std()

print("Desvio padrão de incêndios por estado:\n")
for state, std in std_by_state.items():
    print(f"{state:<20}: {std:.2f}")

print("\nDesvio padrão de incêndios por mês:\n")
for month, std in std_by_month.items():
    print(f"{month:<12}: {std:.2f}")

print("\nDesvio padrão de incêndios por ano:\n")
for year, std in std_by_year.items():
    print(f"{year:<5}: {std:.2f}")


# @title **28 - Quartis por estado,ano e mes**

quantiles_by_state = Base_Dados.groupby('state')['number'].quantile([0.25, 0.5, 0.75]).unstack()

quantiles_by_month = Base_Dados.groupby('month')['number'].quantile([0.25, 0.5, 0.75]).unstack()

quantiles_by_year = Base_Dados.groupby('year')['number'].quantile([0.25, 0.5, 0.75]).unstack()

print("Quartis de incêndios por estado (25%, 50%, 75%):\n")
for state, quantiles in quantiles_by_state.iterrows():
    print(f"{state:<20}: {quantiles[0.25]:.2f}, {quantiles[0.50]:.2f}, {quantiles[0.75]:.2f}")

print("\nQuartis de incêndios por mês (25%, 50%, 75%):\n")
for month, quantiles in quantiles_by_month.iterrows():
    print(f"{month:<12}: {quantiles[0.25]:.2f}, {quantiles[0.50]:.2f}, {quantiles[0.75]:.2f}")

print("\nQuartis de incêndios por ano (25%, 50%, 75%):\n")
for year, quantiles in quantiles_by_year.iterrows():
    print(f"{year:<5}: {quantiles[0.25]:.2f}, {quantiles[0.50]:.2f}, {quantiles[0.75]:.2f}")



# @title **29 - Correlação entre mes e numero de incendios**

month_mapping = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5, 'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10, 'Novembro': 11, 'Dezembro': 12}
Base_Dados['month_code'] = Base_Dados['month'].map(month_mapping)


month_correlation_matrix = Base_Dados[['month_code', 'number']].corr()


plt.figure(figsize=(6, 4))
sns.heatmap(month_correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)


plt.title('Mapa de Calor da Correlação Entre Mês e Número de Incêndios')
print ("A correlação entre o mês e o número de incêndios é de 0.1346, o que indica uma correlação positiva fraca. Isso sugere que há uma leve tendência de mais incêndios em certos meses\n")
plt.show()


month_correlation_matrix



# @title **30 - Teste ANOVA por mes,estado e ano**

grouped_state = [group["number"].values for name, group in Base_Dados.groupby("state")]

anova_state_result = stats.f_oneway(*grouped_state)

print(f"ANOVA para o fator 'Estado':\nF-statística: {anova_state_result.statistic:.2f}, p-valor: {anova_state_result.pvalue:.2e}")

grouped_month = [group["number"].values for name, group in Base_Dados.groupby("month")]

anova_month_result = stats.f_oneway(*grouped_month)

print(f"\nANOVA para o fator 'Mês':\nF-statística: {anova_month_result.statistic:.2f}, p-valor: {anova_month_result.pvalue:.2e}")

grouped_year = [group["number"].values for name, group in Base_Dados.groupby("year")]

anova_year_result = stats.f_oneway(*grouped_year)

print(f"\nANOVA para o fator 'Ano':\nF-statística: {anova_year_result.statistic:.2f}, "
      f"p-valor: {anova_year_result.pvalue:.2e}\n")

# Interpretações
print("Isso significa que o estado onde o incêndio ocorre tem um efeito significativo sobre a quantidade de incêndios.")
print("Isso sugere que o mês em que os incêndios ocorrem tem um efeito relevante na quantidade de incêndios. Certos meses provavelmente têm mais incêndios do que outros.")
print("Isso significa que, com base nesses dados, o ano em si não parece ter um efeito significativo na quantidade de incêndios. As variações no número de incêndios de ano para ano não são estatisticamente significativas.")

# @title **31 - Verificando Outliers por Mes**
month_order = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']


fig = px.box(Base_Dados, x='month', y='number', category_orders={"month": month_order},
             title='Verificando Outliers por Mês',
             labels={'month': 'Mês', 'number': 'Número de Incêndios'})


print("Todos os valores presentes realmente fazem parte da base de dados então não removi nenhum valor considerado Outliers\n")
fig.show()


# @title **32 - Verificando Outliers por Ano**
fig = px.box(Base_Dados, x='year', y='number',
             title='Verificando Outliers por Ano',
             labels={'year': 'Ano', 'number': 'Número de Incêndios'})

print("Todos os valores presentes realmente fazem parte da base de dados então não removi nenhum valor considerado Outliers\n")
fig.show()


# @title **33 - Verificando Outliers por Estado**

fig = px.box(Base_Dados, x='state', y='number',
             title='Verificando Outliers por Estado',
             labels={'state': 'Estado', 'number': 'Número de Incêndios'})

print("Todos os valores presentes realmente fazem parte da base de dados então não removi nenhum valor considerado Outliers\n")
fig.show()


# @title **33 - Meses com alto numero de incendios por Estado**
critical_months_by_state = Base_Dados.groupby(['state', 'month'])['number'].sum().reset_index()


critical_months_by_state = critical_months_by_state.sort_values(by=['state', 'number'], ascending=False).groupby('state').head(1)


fig = px.bar(critical_months_by_state,
             x='state',
             y='number',
             color='month',
             title='Meses Críticos para Incêndios por Estado',
             labels={'number': 'Número de Incêndios', 'state': 'Estado', 'month': 'Mês'},
             hover_data=['number'])

print("Podemos observar que o mes de Setembro aparece em 15 estados diferentes mostrando um padrão bem claro")
fig.show()

# @title **34 - Porcentagem de incendios por estado**
total_fires_by_state = Base_Dados.groupby('state')['number'].sum().reset_index()


total_fires = total_fires_by_state['number'].sum()
total_fires_by_state['percentage'] = (total_fires_by_state['number'] / total_fires) * 100


total_fires_by_state = total_fires_by_state.sort_values(by='number', ascending=False)


fig_bar = px.bar(total_fires_by_state,
                 x='state',
                 y='number',
                 title='Distribuição de Incêndios por Estado',
                 labels={'number': 'Número de Incêndios', 'state': 'Estado'},
                 hover_data=['percentage'],
                 text='percentage')


fig_bar.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

print("Juntando os estados do Pará,Mato Grosso e Maranhão , eles totalizam um total de 45% das queimadas em territorio\n")
fig_bar.show()

# @title **35 - Porcentagem de incendios de um ano para outro**

fires_per_year = Base_Dados.groupby('year')['number'].sum().reset_index()


fires_per_year['percentage_change'] = fires_per_year['number'].pct_change() * 100


fires_per_year['percentage_change'].fillna(0, inplace=True)


fig = px.bar(fires_per_year,
             x='year',
             y='percentage_change',
             title='Evolução Anual de Incêndios em Percentual',
             labels={'percentage_change': 'Variação Percentual (%)', 'year': 'Ano'},
             text='percentage_change')


fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

print("Evolução anual de incendios em porcentagem de um ano para outro , destacando o ano de 2018 para 2019 uma crescente de 48% no numero total de incendios\n")
fig.show()

