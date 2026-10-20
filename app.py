import streamlit as st
import pandas as pd

# --- 1. INICIALIZAÇÃO DA TABELA DE PREÇOS NA SESSÃO ---
# Garantimos que a tabela fique salva na memória (st.session_state)
if "servicos_data" not in st.session_state:
    st.session_state.servicos_data = pd.DataFrame({
        "Serviço": ["Corte Masculino", "Barba Completa", "Combo (Corte + Barba)", "Pezinho / Acabamento", "Sobrancelha"],
        "Duração": ["30 min", "30 min", "50 min", "15 min", "15 min"],
        "Preço (R$)": [45.00, 35.00, 70.00, 20.00, 15.00]
    })

# --- 2. FORMULÁRIO PARA ALTERAR OS PREÇOS ---
st.subheader("✏️ Alterar Preço dos Serviços")

with st.form(key="form_alterar_preco"):
    # Seleção do serviço a ser alterado
    servico_alterar = st.selectbox(
        "Selecione o serviço:",
        st.session_state.servicos_data["Serviço"]
    )
    
    # Busca o preço atual do serviço selecionado
    preco_atual_selecionado = float(
        st.session_state.servicos_data.loc[
            st.session_state.servicos_data["Serviço"] == servico_alterar, "Preço (R$)"
        ].values[0]
    )
    
    # Campo para inserir o novo valor
    novo_preco = st.number_input(
        "Novo Preço (R$)",
        min_value=0.0,
        value=preco_atual_selecionado,
        step=5.0,
        format="%.2f"
    )
    
    # Botão de confirmação
    btn_atualizar_preco = st.form_submit_button("Atualizar Preço")
    
    if btn_atualizar_preco:
        # Atualiza a linha do serviço com o novo valor
        st.session_state.servicos_data.loc[
            st.session_state.servicos_data["Serviço"] == servico_alterar, "Preço (R$)"
        ] = novo_preco
        
        st.success(f" O preço do serviço **{servico_alterar}** foi alterado
