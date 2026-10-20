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

# Base de dados de preços
servicos_data = {
    "Serviço": ["Corte Masculino", "Barba Completa", "Combo (Corte + Barba)", "Pezinho / Acabamento", "Sobrancelha"],
    "Duração": ["30 min", "30 min", "50 min", "15 min", "15 min"],
    "Preço (R$)": [45.00, 35.00, 70.00, 20.00, 15.00]
}

df_servicos = pd.DataFrame(servicos_data)

# Estado da sessão para armazenar agendamentos
if "agendamentos" not in st.session_state:
    st.session_state.agendamentos = pd.DataFrame(
        columns=["Cliente", "Telefone", "Serviço", "Data", "Horário"]
    )

# Navegação por Abas
tab1, tab2, tab3 = st.tabs(["💰 Tabela de Preços", "📅 Novo Agendamento", "📋 Painel (Barbeiro)"])

# --- ABA 1: TABELA DE PREÇOS ---
with tab1:
    st.markdown("### Preços e Serviços")
    st.dataframe(
        df_servicos.style.format({"Preço (R$)": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

# --- ABA 2: FORMULÁRIO DE AGENDAMENTO ---
with tab2:
    st.markdown("### Reserve seu Horário")
    
    with st.form(key="form_agendar"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("Telefone / WhatsApp")
        servico_selecionado = st.selectbox("Selecione o Serviço", df_servicos["Serviço"])
        data_agendamento = st.date_input("Data do Agendamento", min_value=datetime.today())
        
        horarios = [f"{h:02d}:00" for h in range(9, 19)]
        horario_selecionado = st.selectbox("Horário", horarios)
        
        btn_confirmar = st.form_submit_button("Confirmar Agendamento")
        
        if btn_confirmar:
            if not nome or not telefone:
                st.error("Por favor, preencha seu nome e telefone.")
            else:
                novo_registro = {
                    "Cliente": nome,
                    "Telefone": telefone,
                    "Serviço": servico_selecionado,
                    "Data": data_agendamento.strftime("%d/%m/%Y"),
                    "Horário": horario_selecionado
                }
                st.session_state.agendamentos = pd.concat(
                    [st.session_state.agendamentos, pd.DataFrame([novo_registro])],
                    ignore_index=True
                )
                st.success(f"✅ Agendamento confirmado para {nome} em {data_agendamento.strftime('%d/%m/%Y')} às {horario_selecionado}!")

# --- ABA 3: PAINEL DE CONTROLE ---
with tab3:
    st.markdown("### Agendamentos Confirmados")
    
    if st.session_state.agendamentos.empty:
        st.info("Nenhum agendamento registrado até o momento.")
    else:
        st.dataframe(st.session_state.agendamentos, use_container_width=True, hide_index=True)
        
        if st.button("Limpar Todos os Registros"):
            st.session_state.agendamentos = pd.DataFrame(
                columns=["Cliente", "Telefone", "Serviço", "Data", "Horário"]
            )
            st.rerun()
