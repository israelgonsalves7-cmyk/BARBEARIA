import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Barbearia Estilo & Corte",
    page_icon="✂️",
    layout="centered"
)

ARQUIVO_CSV = "agendamentos.csv"
ARQUIVO_PIX = "chave_pix.txt"
ARQUIVO_SERVICOS = "servicos.json"
SENHA_BARBEIRO = "1234"

SERVICOS_PADRAO = [
    {"Serviço": "Corte Masculino", "Duração": "30 min", "Preço (R$)": 45.00},
    {"Serviço": "Barba Completa", "Duração": "30 min", "Preço (R$)": 35.00},
    {"Serviço": "Combo (Corte + Barba)", "Duração": "50 min", "Preço (R$)": 70.00},
    {"Serviço": "Pezinho / Acabamento", "Duração": "15 min", "Preço (R$)": 20.00},
    {"Serviço": "Sobrancelha", "Duração": "15 min", "Preço (R$)": 15.00}
]

def carregar_servicos():
    if os.path.exists(ARQUIVO_SERVICOS):
        try:
            with open(ARQUIVO_SERVICOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                return pd.DataFrame(dados)
        except Exception:
            pass
    return pd.DataFrame(SERVICOS_PADRAO)

def salvar_servicos(df_servicos):
    with open(ARQUIVO_SERVICOS, "w", encoding="utf-8") as f:
        json.dump(df_servicos.to_dict(orient="records"), f, ensure_ascii=False, indent=4)

def carregar_agendamentos():
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV)
    return pd.DataFrame(
        columns=["Cliente", "Telefone", "Serviço", "Data", "Horário", "Forma de Pagamento", "Valor (R$)"]
    )

def salvar_agendamento(novo_registro):
    df = carregar_agendamentos()
    df_novo = pd.DataFrame([novo_registro])
    df_atualizado = pd.concat([df, df_novo], ignore_index=True)
    df_atualizado.to_csv(ARQUIVO_CSV, index=False)

def zerar_agendamentos():
    df_vazio = pd.DataFrame(
        columns=["Cliente", "Telefone", "Serviço", "Data", "Horário", "Forma de Pagamento", "Valor (R$)"]
    )
    df_vazio.to_csv(ARQUIVO_CSV, index=False)

def carregar_pix():
    if os.path.exists(ARQUIVO_PIX):
        with open(ARQUIVO_PIX, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Cole sua chave Pix aqui"

def salvar_pix(nova_chave):
    with open(ARQUIVO_PIX, "w", encoding="utf-8") as f:
        f.write(nova_chave)

st.session_state.servicos_data = carregar_servicos()

if "barbeiro_autenticado" not in st.session_state:
    st.session_state.barbeiro_autenticado = False

formas_pagamento = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro (Local)"]

st.title("✂️ Barbearia Estilo & Corte")
st.subheader("Tabela de Serviços e Agendamento Online")

tab1, tab2, tab3 = st.tabs(["💰 Tabela de Preços", "📅 Novo Agendamento", "🔒 Área do Barbeiro"])

with tab1:
    st.markdown("### Preços e Serviços")
    st.dataframe(
        st.session_state.servicos_data.style.format({"Preço (R$)": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.markdown("### Reserve seu Horário")
    chave_pix_atual = carregar_pix()
    
    with st.form(key="form_agendar"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("Telefone / WhatsApp")
        servico_selecionado = st.selectbox("Selecione o Serviço", st.session_state.servicos_data["Serviço"])
        
        filtro_servico = st.session_state.servicos_data["Serviço"] == servico_selecionado
