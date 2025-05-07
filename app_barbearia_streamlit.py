# app_barbearia_streamlit.py
import streamlit as st
import json
import os
from datetime import datetime

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

def relatorio_do_dia(data=None):
    if not data:
        data = datetime.now().strftime("%Y-%m-%d")
    lista = [c for c in dados if c["data"] == data]
    return lista

# --- App Streamlit ---
st.set_page_config(page_title="Barbearia - Cortes", layout="centered")
st.title("✂️ Barbearia - Registro de Cortes")

dados = carregar_dados()

with st.form("form_corte"):
    nome = st.text_input("Nome do cliente")
    valor = st.number_input("Valor do corte (R$)", min_value=0.0, step=0.5)
    enviar = st.form_submit_button("Registrar Corte")

    if enviar:
        if nome and valor > 0:
            adicionar_corte(nome, valor)
            st.success(f"Corte registrado: {nome} - R$ {valor:.2f}")
            st.rerun()
        else:
            st.warning("Preencha todos os campos corretamente.")

st.subheader("📅 Relatório do Dia")
hoje = datetime.now().strftime("%Y-%m-%d")
cortes_hoje = relatorio_do_dia(hoje)

if cortes_hoje:
    total = 0
    for c in cortes_hoje:
        st.write(f"• {c['cliente']} - R$ {c['valor']:.2f}")
        total += c["valor"]
    st.markdown(f"**Total do dia:** R$ {total:.2f}")
else:
    st.info("Nenhum corte registrado hoje.")
