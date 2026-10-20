import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuração inicial da página com layout largo/centralizado
st.set_page_config(
    page_title="Barbearia Estilo & Corte",
    page_icon="✂️",
    layout="centered"
)

# --- CSS CUSTOMIZADO (DESIGN BARBEARIA RETRÔ / MODERNA) ---
st.markdown("""
<style>
    /* Fundo da Página */
    .stApp {
        background-color: #121212;
        color: #f5f5f5;
    }

    /* Ocultar menus padrões do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header/Banner da Barbearia */
    .barber-header {
        background: linear-gradient(135deg, #1f1c18 0%, #000000 100%);
        padding: 30px 20px;
        border-radius: 12px;
        border-bottom: 3px solid #d4af37;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.2);
    }
    
    .barber-title {
        color: #d4af37 !important;
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 2.3em;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 5px;
        text-transform: uppercase;
    }
    
    .barber-subtitle {
        color: #cccccc !important;
        font-size: 1.1em;
        font-style: italic;
    }

    /* Estilização das Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #1e1e1e;
        padding: 8px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 8px;
        color: #aaaaaa;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        background-color: #d4af37 !important;
        color: #000000 !important;
    }

    /* Botões */
    .stButton>button {
        background-color: #d4af37;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        background-color: #f3cf55;
        color: #000000;
        box-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5);
    }

    /* Entradas de Texto e Form */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input {
        background-color: #242424 !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
    }

    /* Cards Informativos */
    .stAlert {
        border-radius: 8px;
    }
    
    /* Métricas no Painel do Barbeiro */
    [data-testid="stMetricValue"] {
        color: #d4af37 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

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
    df_vazio.to_csv(ARQUIVO_
