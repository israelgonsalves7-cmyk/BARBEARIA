import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# Configuração inicial da página
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

def zer
