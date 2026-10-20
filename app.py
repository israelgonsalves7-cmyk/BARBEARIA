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
SENHA_BARBEIRO = "1234"  # 👈 Mude para a senha que desejar!

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
        with open(ARQUIVO_PIX, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Cole sua chave Pix aqui"

def salvar_pix(nova_chave):
    with open(ARQUIVO_PIX, "w", encoding="utf-8") as f:
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

# Título do App
st.title("✂️ Barbearia Estilo & Corte")
st.subheader("Tabela de Serviços e Agendamento Online")

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
    chave_pix_atual = carregar_pix()
    
    with st.form(key="form_agendar"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("Telefone / WhatsApp")
        servico_selecionado = st.selectbox("Selecione o Serviço", st.session_state.servicos_data["Serviço"])
        
        # Obter preço do serviço selecionado
        filtro_servico = st.session_state.servicos_data["Serviço"] == servico_selecionado
        preco_atual = float(st.session_state.servicos_data.loc[filtro_servico, "Preço (R$)"].values[0])
        
        data_agendamento = st.date_input("Data do Agendamento", min_value=datetime.today())
        horarios = [f"{h:02d}:00" for h in range(9, 19)]
        horario_selecionado = st.selectbox("Horário", horarios)
        
        forma_pagamento_selecionada = st.selectbox("Forma de Pagamento", formas_pagamento)
        
        st.info(f"💵 **Valor do Serviço:** R$ {preco_atual:.2f}")
        
        if forma_pagamento_selecionada == "Pix":
            st.warning(f"🔑 **Chave Pix para Pagamento:** `{chave_pix_atual}`")
        
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
                salvar_agendamento(novo_registro)
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
                st.rerun()
            else:
                st.error("Senha incorreta!")
    else:
        col_title, col_logout = st.columns([3, 1])
        with col_title:
            st.success("🔓 Modo Barbeiro Ativo")
        with col_logout:
            if st.button("🚪 Sair"):
                st.session_state.barbeiro_autenticado = False
                st.rerun()

        st.divider()

        # 1. Alterar Chave Pix (Exclusivo da Área Logada do Barbeiro)
        st.markdown("### 🔑 Alterar Chave Pix para Recebimento")
        pix_atual = carregar_pix()
        with st.form(key="form_chave_pix"):
            nova_chave = st.text_input("Chave Pix (CPF, CNPJ, Celular, E-mail ou Aleatória):", value=pix_atual)
            btn_salvar_pix = st.form_submit_button("Salvar Nova Chave Pix")
            
            if btn_salvar_pix:
                salvar_pix(nova_chave)
                st.success("✅ Chave Pix salva e atualizada com sucesso para todos os clientes!")
                st.rerun()

        st.divider()

        # 2. Painel de Agendamentos do Barbeiro
        st.markdown("### 📋 Painel de Agendamentos Registrados")
        df_agendamentos = carregar_agendamentos()

        if not df_agendamentos.empty:
            st.dataframe(df_agendamentos, use_container_width=True, hide_index=True)
            total_faturado = df_agendamentos["Valor (R$)"].sum()
            st.metric(label="Faturamento Total Estimado", value=f"R$ {total_faturado:.2f}")
        else:
            st.info("Nenhum agendamento registrado no momento.")

        st.divider()

        # Botões de Ação
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Atualizar Lista"):
                st.rerun()
                
        with col_btn2:
            if st.button("🗑️ Zerar Todos os Agendamentos"):
                zerar_agendamentos()
                st.warning("Todos os agendamentos foram apagados!")
                st.rerun()
