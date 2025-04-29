import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
df = pd.read_csv('dashboard-fires-month-03-03-2025-11_16_31.csv', delimiter=';')

# Converter a coluna 'date' para datetime
df['date'] = pd.to_datetime(df['date'], format='%Y/%m')

# Agrupar por 'date' e 'class' e somar os focos
df_grouped = df.groupby(['date', 'class'])['focuses'].sum().reset_index()

# Gráfico de Colunas
plt.figure(figsize=(12, 6))
for class_name in df_grouped['class'].unique():
    plt.bar(df_grouped[df_grouped['class'] == class_name]['date'], 
            df_grouped[df_grouped['class'] == class_name]['focuses'], 
            label=class_name)
plt.xlabel('Data')
plt.ylabel('Número de Focos')
plt.title('Número de Focos por Classe ao Longo do Tempo')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('column_chart.png')
plt.show()

# Gráfico de Linha
plt.figure(figsize=(12, 6))
for class_name in df_grouped['class'].unique():
    plt.plot(df_grouped[df_grouped['class'] == class_name]['date'], 
             df_grouped[df_grouped['class'] == class_name]['focuses'], 
             marker='o', label=class_name)
plt.xlabel('Data')
plt.ylabel('Número de Focos')
plt.title('Número de Focos por Classe ao Longo do Tempo')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('line_chart.png')
plt.show()

# Gráfico de Pizza para o mês mais recente
latest_month = df['date'].max()
df_latest_month = df[df['date'] == latest_month].groupby('class')['focuses'].sum().reset_index()

plt.figure(figsize=(8, 8))
plt.pie(df_latest_month['focuses'], labels=df_latest_month['class'], autopct='%1.1f%%', startangle=140)
plt.title(f'Distribuição de Focos por Classe para {latest_month.strftime("%Y-%m")}')
plt.tight_layout()
plt.savefig('pie_chart.png')
plt.show()