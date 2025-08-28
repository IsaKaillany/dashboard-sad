import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

np.random.seed(42)

# Datas
datas = pd.date_range("2025-08-01", "2025-08-25", freq="D")

# Clientes
clientes = ["Paulo", "Diego", "Daniel", "Carlos", "Aroldo", "Bruno"]

# Formas de pagamento
pagamentos = ["Cartão Crédito", "Cartão Débito", "Dinheiro", "Pix"]

# Criando DataFrame
dados = []
for data in datas:
    for cliente in clientes:
        producao = np.random.randint(15, 200)   # produção diária
        preco_unitario = np.random.randint(1, 3)
        faturamento = producao * preco_unitario
        pagamento = np.random.choice(pagamentos)
        cliente_frequente = np.random.choice(["Sim", "Não"])
        dados.append([data, cliente, producao, preco_unitario, faturamento, pagamento, cliente_frequente])

df = pd.DataFrame(dados, columns=["Data", "Clientes", "Produção", "Preço Unitário", "Faturamento", "Pagamento", "Cliente Frequente"])

# -----------------------------
# SIDEBAR - FILTROS
# -----------------------------
st.sidebar.header("Filtros")

# Período
periodo = st.sidebar.date_input("Período", [df["Data"].min(), df["Data"].max()])
df = df[(df["Data"] >= pd.to_datetime(periodo[0])) & (df["Data"] <= pd.to_datetime(periodo[1]))]

# Clientes
clientes_filtro = st.sidebar.multiselect("Clientes", df["Clientes"].unique(), default=df["Clientes"].unique())
df = df[df["Clientes"].isin(clientes_filtro)]

# Forma de pagamento
pag_filtro = st.sidebar.multiselect("Forma de Pagamento", df["Pagamento"].unique(), default=df["Pagamento"].unique())
df = df[df["Pagamento"].isin(pag_filtro)]

# Cliente frequente
cliente_filtro = st.sidebar.selectbox("Cliente Frequente?", ["Todos", "Sim", "Não"])
if cliente_filtro != "Todos":
    df = df[df["Cliente Frequente"] == cliente_filtro]

# -----------------------------
# MÉTRICAS PRINCIPAIS
# -----------------------------
total_producao = df["Produção"].sum()
total_faturamento = df["Faturamento"].sum()
ticket_medio = df["Faturamento"].sum() / df["Produção"].sum() if df["Produção"].sum() > 0 else 0
clientes_unicos = df["Clientes"].nunique()

st.title("Bonelaria - Dashboard de Produção e Faturamento")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Produção Total", total_producao)
col2.metric("Faturamento (R$)", f"{total_faturamento:,.2f}")
col3.metric("Ticket Médio (R$)", f"{ticket_medio:,.2f}")
col4.metric("Clientes", clientes_unicos)

# -----------------------------
# GRÁFICOS
# -----------------------------
st.subheader("Evolução do Faturamento")
faturamento_tempo = df.groupby("Data")["Faturamento"].sum().reset_index()
fig1 = px.line(faturamento_tempo, x="Data", y="Faturamento", title="Faturamento ao longo do tempo")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Produção por Dia")
producao_tempo = df.groupby("Data")["Produção"].sum().reset_index()
fig1 = px.line(producao_tempo, x="Data", y="Produção", title="Produção ao longo do tempo")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Produção por Cliente")
producao_cliente = df.groupby("Clientes")["Produção"].sum().reset_index().sort_values("Produção", ascending=False)
fig2 = px.bar(producao_cliente, x="Clientes", y="Produção", title="Produção por Cliente", text_auto=True)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Faturamento por Forma de Pagamento")
faturamento_pag = df.groupby("Pagamento")["Faturamento"].sum().reset_index()
fig3 = px.pie(faturamento_pag, names="Pagamento", values="Faturamento", title="Distribuição por Forma de Pagamento")
st.plotly_chart(fig3, use_container_width=True)
