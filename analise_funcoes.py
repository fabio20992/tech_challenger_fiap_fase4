
import pandas as pd
import numpy as np

def cria_coluna_imc(df):            # Criação de novos atributos - IMC (Índice de massa corporal) - Peso / (altura²)
    df['IMC'] = df['Weight'] / (df['Height'] ** 2)
    return df

# Tratamento de variáveis categóricas (Encoding)
def trata_binarios(df):         
    # Variáveis Binárias (Sim/Não ou Gênero) - female = 0 / male = 1
    binary_cols = ['Gender', 'family_history', 'FAVC', 'SMOKE', 'SCC']
    for col in binary_cols:
        if df[col].dtype == 'object':
            df[col] = df[col].astype('category').cat.codes
    return df

def trata_variaveis_ordinais(df):
    # Variáveis Ordinais (Intensidade de hábitos)    # no = 0, sometimes = 1, frequently = 2, always = 3
    # Usando mapeamento com letras minúsculas/maiúsculas flexíveis
    df['CAEC'] = df['CAEC'].str.lower().map({'no': 0, 'sometimes': 1, 'frequently': 2, 'always': 3})
    df['CALC'] = df['CALC'].str.lower().map({'no': 0, 'sometimes': 1, 'frequently': 2, 'always': 3})
    return df

def trata_var_nominais_transporte(df):    # Variáveis Nominais (Meio de Transporte) -> Criando colunas dummies (0 ou 1)
    df = pd.get_dummies(df, columns=['MTRANS'], drop_first=True, dtype=int)
    return df

def df_base_obesidade_tratado(df):      #Pode ser necessárioeliminar a criação do IMC
    df = cria_coluna_imc(df)                # Criação de novos atributos - IMC (Índice de massa corporal) - Peso / (altura²)
    # Tratamento de variáveis categóricas (Encoding)
    df = trata_binarios(df)                 # Variáveis Binárias (Sim/Não ou Gênero) - female = 0 / male = 1
    df = trata_variaveis_ordinais(df)       # Usando mapeamento com letras minúsculas/maiúsculas flexíveis
    df =  trata_var_nominais_transporte(df)   # Variáveis Nominais (Meio de Transporte) -> Criando colunas dummies (0 ou 1)

    return df




