import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração inicial da página
st.set_page_config(
    page_title="Barbearia Estilo & Corte",
    page_icon="✂️",
    layout="centered"
)

# Título do App
st.title("✂️ Barbearia Estilo & Corte")
st.subheader("Tabela de Serviços e Agendamento Online")

# --- ESTADO DA SESSÃO (Memória do App) ---

# Tabela de Serviços e Preços
if "servicos_data" not in st.session_state:
    st.session_state.servicos_data = pd.DataFrame({
        "Serviço": ["Corte Masculino", "Barba Completa", "Combo (Corte + Barba)", "Pezinho / Acabamento", "Sobrancelha"],
        "Duração": ["30 min", "30 min", "50 min", "15 min", "15 min"],
        "Preço (R$)": [45.00, 35.00, 70.00, 20.00, 15.00]
    })

# Histórico de agendamentos
if "agendamentos" not in st.session_state:
    st.session_state.agendamentos = pd.DataFrame(
        columns=["Cliente", "Telefone", "Serviço", "Data", "Horário", "Forma de Pagamento", "Valor (R$)"]
    )

# Chave Pix inicial (pode ser alterada no painel)
if "chave_pix" not in st.session_state:
    st.session_state.chave_pix = "123.456.789-00"

formas_pagamento = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro (Local)"]

# Navegação por Abas
tab1, tab2, tab3 = st.tabs(["💰 Tabela de Preços", "📅 Novo Agendamento", "⚙️ Painel & Configurações"])

# --- ABA 1: TABELA DE PREÇOS ---
with tab1:
    st.markdown("### Preços e Serviços")
    st.dataframe(
        st.session_state.servicos_data.style.format({"Preço (R$)": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

# --- ABA 2: FORMULÁRIO DE AGENDAMENTO ---
with tab2:
    st.markdown("### Reserve seu Horário")
    
    with st.form(key="form_agendar"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("Telefone / WhatsApp")
        servico_selecionado = st.selectbox("Selecione o Serviço", st.session_state.servicos_data["Serviço"])
        
        # Preço do serviço escolhido
        preco_atual = float(st.session
