import streamlit as st
import json
import os
from datetime import datetime
from collections import defaultdict

ARQUIVO_DADOS = "cortes.json"

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r") as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w") as f:
        json.dump(dados, f, indent=4)

def adicionar_corte(nome, valor):
    data = datetime.now().strftime("%Y-%m-%d")
    novo = {"cliente": nome, "valor": valor, "data": data}
    dados.append(novo)
    salvar_dados(dados)

def relatorio_por_data(data):
    return [c for c in dados if c["data"] == data]

def excluir_corte(cliente, valor, data):
    global dados
    dados = [c for c in dados if not (c["cliente"] == cliente and c["valor"] == valor and c["data"] == data)]
    salvar_dados(dados)
    st.success(f"Corte de {cliente} (R$ {valor:.2f}) em {data} excluído.")
    st.rerun()

def gerar_relatorio_mensal():
    meses = defaultdict(float)
    for corte in dados:
        data_obj = datetime.strptime(corte["data"], "%Y-%m-%d")
        chave = data_obj.strftime("%m/%Y")
        meses[chave] += corte["valor"]
    return dict(sorted(meses.items()))

def filtrar_por_cliente(nome):
    return [c for c in dados if nome.lower() in c["cliente"].lower()]

# --- Streamlit App ---
st.set_page_config(page_title="Barbearia", layout="centered")
st.markdown("<h1 style='text-align: center;'>✂️ Barbearia</h1>", unsafe_allow_html=True)

dados = carregar_dados()

st.markdown("## 📌 Registrar Corte")
with st.form("form_corte"):
    nome = st.text_input("Nome do cliente")
    valor = st.number_input("Valor do corte (R$)", min_value=0.0, step=0.5)
    enviar = st.form_submit_button("💾 Registrar")

    if enviar:
        if nome and valor > 0:
            adicionar_corte(nome, valor)
            st.success(f"✅ Corte registrado: {nome} - R$ {valor:.2f}")
            st.rerun()
        else:
            st.warning("⚠️ Preencha todos os campos corretamente.")

st.markdown("---")

# RELATÓRIO DO DIA
st.markdown("## 📅 Relatório de Hoje")
hoje = datetime.now().strftime("%Y-%m-%d")
cortes_hoje = relatorio_por_data(hoje)

if cortes_hoje:
    total = 0
    for corte in cortes_hoje:
        st.markdown(f"**{corte['cliente']}** - R$ {corte['valor']:.2f} ({corte['data']})")
        if st.button(f"🗑️ Excluir {corte['cliente']} {corte['valor']}", key=f"{corte['cliente']}_{corte['valor']}_{corte['data']}"):
            excluir_corte(corte["cliente"], corte["valor"], corte["data"])
        st.markdown("---")
        total += corte["valor"]
    st.markdown(f"### 💵 Total do dia: R$ {total:.2f}")
else:
    st.info("Nenhum corte registrado hoje.")

# CONSULTA POR DATA
st.markdown("## 🔎 Ver Faturamento por Data")
data_consulta = st.date_input("Selecione a data")
data_str = data_consulta.strftime("%Y-%m-%d")
relatorio_data = relatorio_por_data(data_str)

if relatorio_data:
    total_dia = 0
    for c in relatorio_data:
        st.write(f"- {c['cliente']} - R$ {c['valor']:.2f}")
        total_dia += c["valor"]
    st.markdown(f"**Total em {data_str}: R$ {total_dia:.2f}**")
else:
    st.info("Nenhum corte nesse dia.")

# RELATÓRIO MENSAL
st.markdown("## 📊 Relatório Mensal")
rel_mensal = gerar_relatorio_mensal()
if rel_mensal:
    for mes, total in rel_mensal.items():
        st.write(f"• {mes}: R$ {total:.2f}")
else:
    st.info("Sem dados mensais ainda.")

# FILTRO POR CLIENTE
st.markdown("## 🔍 Buscar Cliente")
busca = st.text_input("Digite o nome")

if busca:
    resultados = filtrar_por_cliente(busca)
    if resultados:
        for r in resultados:
            st.markdown(f"- {r['data']}: **{r['cliente']}** - R$ {r['valor']:.2f}")
    else:
        st.warning("Nenhum resultado encontrado.")

