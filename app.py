import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Configuração da página
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

# --- PERSISTÊNCIA DE DADOS ---

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

# --- INICIALIZAÇÃO DE VARIÁVEIS ---
st.session_state.servicos_data = carregar_servicos()

if "barbeiro_autenticado" not in st.session_state:
    st.session_state.barbeiro_autenticado = False

formas_pagamento = ["Pix", "Cartão de Crédito", "Cartão de Débito", "Dinheiro (Local)"]

# --- INTERFACE ---
st.title("✂️ Barbearia Estilo & Corte")
st.subheader("Tabela de Serviços e Agendamento Online")

tab1, tab2, tab3 = st.tabs(["💰 Tabela de Preços", "📅 Novo Agendamento", "🔒 Área do Barbeiro"])

# --- TABELA DE PREÇOS (PÚBLICA) ---
with tab1:
    st.markdown("### Preços e Serviços")
    st.dataframe(
        st.session_state.servicos_data.style.format({"Preço (R$)": "R$ {:.2f}"}),
        use_container_width=True,
        hide_index=True
    )

# --- FORMULÁRIO DE AGENDAMENTO (PÚBLICO) ---
with tab2:
    st.markdown("### Reserve seu Horário")
    chave_pix_atual = carregar_pix()
    
    with st.form(key="form_agendar"):
        nome = st.text_input("Seu Nome")
        telefone = st.text_input("Telefone / WhatsApp")
        servico_selecionado = st.selectbox("Selecione o Serviço", st.session_state.servicos_data["Serviço"])
        
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

# --- ÁREA DO BARBEIRO ---
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

        # 1. ALTERAR VALORES E DURAÇÃO DOS SERVIÇOS
        st.markdown("### 🏷️ Alterar Preços dos Serviços")
        servico_editar = st.selectbox(
            "Selecione o serviço para alterar o valor:",
            st.session_state.servicos_data["Serviço"],
            key="select_edit_servico"
        )
        
        dados_servico_atual = st.session_state.servicos_data[
            st.session_state.servicos_data["Serviço"] == servico_editar
        ].iloc[0]
        
        with st.form(key="form_editar_precos"):
            novo_preco = st.number_input(
                "Novo Preço (R$):",
                min_value=0.0,
                value=float(dados_servico_atual["Preço (R$)"]),
                step=5.0,
                format="%.2f"
            )
            nova_duracao = st.text_input(
                "Nova Duração:",
                value=str(dados_servico_atual["Duração"])
            )
            btn_salvar_preco = st.form_submit_button("Salvar Novo Valor")
            
            if btn_salvar_preco:
                idx = st.session_state.servicos_data[
                    st.session_state.servicos_data["Serviço"] == servico_editar
                ].index[0]
                
                st.session_state.servicos_data.at[idx, "Preço (R$)"] = novo_preco
                st.session_state.servicos_data.at[idx, "Duração"] = nova_duracao
                
                salvar_servicos(st.session_state.servicos_data)
                st.success(f"✅ Preço do serviço '{servico_editar}' alterado para R$ {novo_preco:.2f} com sucesso!")
                st.rerun()

        st.divider()

        # 2. ALTERAR CHAVE PIX
        st.markdown("### 🔑 Alterar Chave Pix")
        pix_atual = carregar_pix()
        with st.form(key="form_chave_pix"):
            nova_chave = st.text_input("Chave Pix Atual:", value=pix_atual)
            btn_salvar_pix = st.form_submit_button("Salvar Chave Pix")
            
            if btn_salvar_pix:
                salvar_pix(nova_chave)
                st.success("✅ Chave Pix atualizada com sucesso!")
                st.rerun()

        st.divider()

        # 3. LISTA DE AGENDAMENTOS
        st.markdown("### 📋 Agendamentos Confirmados")
        df_agendamentos = carregar_agendamentos()

        if not df_agendamentos.empty:
            st.dataframe(df_agendamentos, use_container_width=True, hide_index=True)
            total_faturado = df_agendamentos["Valor (R$)"].sum()
            st.metric(label="Faturamento Total Estimado", value=f"R$ {total_faturado:.2f}")
        else:
            st.info("Nenhum agendamento registrado até o momento.")

        st.divider()

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Atualizar Lista"):
                st.rerun()
                
        with col_btn2:
            if st.button("🗑️ Zerar Todos os Agendamentos"):
                zerar_agendamentos()
                st.warning("Todos os agendamentos foram apagados!")
                st.rerun()
