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

# --- SENHA DE ACESSO DO BARBEIRO ---
SENHA_BARBEIRO = "1234"  # 👈 Altere para a senha que desejar!

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

# Chave Pix
if "chave_pix" not in st.session_state:
    st.session_state.chave_pix = "Cole sua chave Pix aqui"

# Controle de Autenticação do Barbeiro
if "barbeiro_autenticado" not in st.session_state:
    st.session_state.barbeiro_autenticado = False

formas_pagamento = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro (Local)"]

# Navegação por Abas
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
    
    with st.form(key="form_agendar"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("Telefone / WhatsApp")
        servico_selecionado = st.selectbox("Selecione o Serviço", st.session_state.servicos_data["Serviço"])
        
        # Preço do serviço escolhido
        preco_atual = float(st.session_state.servicos_data.loc[
            st.session_state.servicos_data["Serviço"] == servico_selecionado, "Preço (R$)"
        ].values[0])
        
        data_agendamento = st.date_input("Data do Agendamento", min_value=datetime.today())
        horarios = [f"{h:02d}:00" for h in range(9, 19)]
        horario_selecionado = st.selectbox("Horário", horarios)
        
        forma_pagamento_selecionada = st.selectbox("Forma de Pagamento", formas_pagamento)
        
        st.info(f"💵 **Valor do Serviço:** R$ {preco_atual:.2f}")
        
        # Exibe a Chave Pix se a opção Pix for selecionada
        if forma_pagamento_selecionada == "Pix":
            st.warning(f"🔑 **Chave Pix para Pagamento:** `{st.session_state.chave_pix}`")
        
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
                    "Horário": horario_selecionado,
                    "Forma de Pagamento": forma_pagamento_selecionada,
                    "Valor (R$)": preco_atual
                }
                st.session_state.agendamentos = pd.concat(
                    [st.session_state.agendamentos, pd.DataFrame([novo_registro])],
                    ignore_index=True
                )
                st.success(f"✅ Agendamento confirmado para {nome} em {data_agendamento.strftime('%d/%m/%Y')} às {horario_selecionado}!")

# --- ABA 3: ÁREA EXCLUSIVA DO BARBEIRO (RESTRITA POR SENHA) ---
with tab3:
    if not st.session_state.barbeiro_autenticado:
        st.markdown("### 🔐 Acesso Restrito ao Barbeiro")
        senha_input = st.text_input("Digite a senha de acesso:", type="password", key="input_senha_barbeiro")
        
        if st.button("Entrar no Painel"):
            if senha_input == SENHA_BARBEIRO:
                st.session_state.barbeiro_autenticado = True
                st.success("Acesso liberado!")
