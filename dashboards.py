# OBJETIVOS DO DASHBOARD -> VISÃO MENSAL
    # - Faturamento por unidade
    # - Tipo de produto mais vendido, contribuição por filial
    # - Desempenho das formas de pagamento
    # - Avaliações médias das filiais

# FUNCIONAMENTO DO DASHBOARD – PASSOS GERAIS:
# 1. Importa bibliotecas para dados, interface e gráficos
# 2. Lê e prepara os dados (conversão, ordenação, coluna mês)
# 3. Adiciona filtro de mês na barra lateral
# 4. Filtra os dados conforme o mês escolhido
# 5. Organiza o layout da interface em colunas
# 6. Cria gráficos interativos com base nos dados filtrados

import streamlit as st
import pandas as pd
import plotly.express as px 

# 1. Configuração do layout da página
st.set_page_config(layout='wide')

# 2. Leitura e preparação dos dados
df = pd.read_csv('supermarket_sales.csv', sep=";", decimal=",")  # Lê os dados do CSV
df["Date"] = pd.to_datetime(df["Date"])                          # Converte a coluna de data
df = df.sort_values("Date")                                      # Ordena os dados por data
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month).zfill(2))  # Cria coluna "Month"

# 3. Adiciona seletor de mês na barra lateral
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# 4. Filtra os dados com base no mês selecionado
df_filtered = df[df["Month"] == month]

# 5. Layout da interface com colunas
col1, col2 = st.columns(2)               # Primeira linha com 2 colunas
col3, col4, col5 = st.columns(3)         # Segunda linha com 3 colunas

# 6. Geração de gráficos

# Gráfico 1: Faturamento por dia (por filial)
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico 2: Faturamento por tipo de produto
# Agrupa os dados por tipo de produto, soma o faturamento total de cada grupo,
# ordena do menor para o maior faturamento e reinicia o índice.
# Isso é feito para gerar um gráfico limpo e organizado do total vendido por categoria.
prod_total = df_filtered.groupby("Product line")[["Total"]].sum().sort_values("Total", ascending=True).reset_index() 

fig_prod = px.bar(prod_total, x="Total", y="Product line", title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

# Gráfico 3: Faturamento por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico 4: Faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Gráfico 5: Avaliação média por filial
rating_avg = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(rating_avg, x="City", y="Rating", title="Avaliação média por filial", color="City")
col5.plotly_chart(fig_rating, use_container_width=True)