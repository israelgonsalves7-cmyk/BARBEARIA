import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração inicial da página
st.set_page_config(
    page_title="Barbearia Estilo & Corte",
    page_icon="✂️",
    layout="centered"
)

ARQUIVO_CSV = "agendamentos.csv"
ARQUIVO_PIX = "chave_pix.txt"
SENHA_BARBEIRO = "1234"  # 👈 Altere para sua senha!

# --- FUNÇÕES DE PERSISTÊNCIA DE DADOS ---

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
        with open(ARQUIVO_PIX, "r") as f:
            return f.read().strip()
    return "Cole sua chave Pix aqui"

def salvar_pix(nova_chave):
    with open(ARQUIVO_PIX, "w") as f:
        f.write(nova_chave)

# --- INICIALIZAÇÃO DE ESTADOS ---

if "servicos_data" not in st.session_state:
    st.session_state.servicos_data = pd.DataFrame({
        "Serviço": ["Corte Masculino", "Barba Completa", "Combo (Corte + Barba)", "Pezinho / Acabamento", "Sobrancelha"],
        "Duração": ["30 min", "30 min", "50 min", "15 min", "15 min"],
        "Preço (R$)": [45.00, 35.00, 70.00, 20.00, 15.00]
    })

if "barbeiro_autenticado" not in st.session_state:
    st.session_state.barbeiro_autenticado = False

formas_pagamento = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro (Local)"]

# Interface Principal
st.title("✂️ Barbearia Estilo & Corte")
st.subheader("Tabela de Serviços e Agendamento Online")

tab1, tab2, tab3 = st.tabs(["💰 Tabela de Preços", "📅 Novo Agendamento", "🔒 Área do Barbeiro"])

# --- ABA 1: TABELA DE PREÇOS (PÚBLICA) ---
with tab1:
    st.markdown("### Preços e Serviços")
    st.dataframe(
        st.session_state.servicos_data.style.format({"Preço (R$)": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

# --- ABA 2: FORMULÁRIO DE AGENDAMENTO (PÚBLICA) ---
with tab2:
    st.markdown("### Reserve seu Horário")
    chave_pix_atual = carregar_pix()
    
    with st.form(key="form_agendar"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("Telefone / WhatsApp")
        servico_selecionado = st.selectbox("Selecione o Serviço", st.session_state.servicos_data["Serviço"])
        
        preco_atual = float(st.session_state.servicos_data.loc[
            st.session_state.servicos_data["Serviço"] == servico_selecionado, "
