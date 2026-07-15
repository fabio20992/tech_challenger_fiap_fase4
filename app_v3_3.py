import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import joblib
import requests
from io import BytesIO

# ------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ------------------------------------------------------------
st.set_page_config(
    page_title="PrevObesidade - Sistema de Apoio ao Diagnóstico",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------
# BARRA LATERAL - MENU DE NAVEGAÇÃO
# ------------------------------------------------------------
st.sidebar.title("⚕️ PrevObesidade")
pagina = st.sidebar.radio(
    "Escolha uma seção:",
    options=["🧠 Predição de Obesidade", "📊 Análise de Dados"],
    index=0  # Inicia na página de predição (mais usada)
)

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para o Tech Challenge - Data Analytics (FIAP)")

# ------------------------------------------------------------
# FUNÇÕES DE CARREGAMENTO (com cache)
# ------------------------------------------------------------

# Carregando o dataset do github - Melhoria: tentar criar um dicionário com as amostras dos registros necessáias para suprir a criação do df com a coluna 'MTRAS', começando com automovel
@st.cache_data
def carregar_dataset():
    # URL raw do seu arquivo no GitHub
    url = "https://raw.githubusercontent.com/fabio20992/tech_challenger_fiap_fase4/refs/heads/main/Base%20de%20dados/Obesity.csv"
    
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o dataset do GitHub: {e}")
        return None

@st.cache_resource
def carregar_modelo():
    # URL raw do seu modelo no GitHub
    url = "https://github.com/fabio20992/tech_challenger_fiap_fase4/raw/refs/heads/main/modelo/model_lgb.jlib"
    try:
        # Faz o download do conteúdo binário
        response = requests.get(url)
        response.raise_for_status()  # Levanta erro se a requisição falhar
        
        # Carrega o modelo a partir do conteúdo em memória
        modelo = joblib.load(BytesIO(response.content))
        return modelo
    except Exception as e:
        st.error(f"Erro ao carregar o modelo do GitHub: {e}")
        return None

# Carrega recursos (somente se necessário)
df_original = carregar_dataset() if pagina == "🧠 Predição de Obesidade" else None
modelo = carregar_modelo() if pagina == "🧠 Predição de Obesidade" else None

# Dicionário de tradução
dict_obesidade = {
    'Insufficient_Weight': 'Abaixo do peso',
    'Normal_Weight':      'Peso normal',
    'Overweight_Level_I': 'Sobrepeso I',
    'Overweight_Level_II':'Sobrepeso II',
    'Obesity_Type_I':     'Obesidade I',
    'Obesity_Type_II':    'Obesidade II',
    'Obesity_Type_III':   'Obesidade III'
}

ordem_categorias= [
    'Abaixo do peso',
    'Peso normal',
    'Sobrepeso I',
    'Sobrepeso II',
    'Obesidade I',
    'Obesidade II',
    'Obesidade III'
]

# ------------------------------------------------------------
# PÁGINA 1: ANÁLISE DE DADOS (POWER BI)
# ------------------------------------------------------------
if pagina == "📊 Análise de Dados":
    st.title("📊 Análise de Dados - Obesidade")
    st.markdown(
        """
        Acompanhe abaixo o dashboard com os principais insights sobre a base de treinamento do modelo de 
        machine learn para categorização de casos de obesidade, desenvolvido no Power BI.
        """
    )
    
    # INSIRA AQUI O SEU LINK DE EMBED DO POWER BI
    POWER_BI_EMBED_URL = "https://app.powerbi.com/view?r=eyJrIjoiMGY2ODQ0YjQtYTdmMi00NWI5LTg2ZmUtMGU5ODY3MDgyY2FhIiwidCI6IjM2ZTIxY2JiLWI1YzUtNGQzOC1iYWQ0LTZhMjlmOWQ4ZTZhYiJ9"
    
    # Exibe o dashboard usando iframe
    components.html(
        f"""
        <iframe 
            src="{POWER_BI_EMBED_URL}" 
            width="100%" 
            height="700" 
            frameborder="0" 
            allowFullScreen="true"
            style="border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        </iframe>
        """,
        height=720,
        width=1200
    )

# ------------------------------------------------------------
# PÁGINA 2: PREDIÇÃO DE OBESIDADE
# ------------------------------------------------------------
else:  # "🧠 Predição de Obesidade"
    st.title("⚕️ PrevObesidade")
    st.markdown(
        """
        **Sistema preditivo para auxiliar médicos no diagnóstico de obesidade**  
        Preencha os dados abaixo e obtenha uma classificação do nível de obesidade.
        """
    )
    
    # ------------------------------------------------------------
    # FORMULÁRIO DE ENTRADA
    # ------------------------------------------------------------
    with st.form(key="form_predicao", clear_on_submit=False):
        st.header("📋 Dados do Paciente")
        
        with st.expander("Dados Demográficos", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                sexo = st.radio(
                    "Sexo biológico",
                    options=['Feminino', 'Masculino'],
                    index=0,
                    horizontal=True
                )
                sexo_map = {'Feminino': 'Female', 'Masculino': 'Male'}
                sexo_cod = sexo_map[sexo]
            
            with col2:
                idade = st.slider(
                    "Idade (anos)",
                    min_value=18,
                    max_value=100,
                    value=30,
                    step=1
                )
            
            with col3:
                altura = st.slider(
                    "Altura (m)",
                    min_value=0.8,
                    max_value=2.2,
                    value=1.70,
                    step=0.01,
                    format="%.2f"
                )
                # st.caption(f"Altura selecionada: {altura:.2f}".replace('.', ',') + " m")
        
        with st.expander("Medidas e Histórico", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                peso = st.slider(
                    "Peso (kg)",
                    min_value=20,
                    max_value=200,
                    value=70,
                    step=1
                )
            with col2:
                historico = st.radio(
                    "Histórico familiar de obesidade",
                    options=['Não', 'Sim'],
                    index=0,
                    horizontal=True
                )
                historico_map = {'Sim': 'yes', 'Não': 'no'}
                historico_cod = historico_map[historico]
            with col3:
                fumante = st.radio(
                    "Fumante",
                    options=['Não', 'Sim'],
                    index=0,
                    horizontal=True
                )
                fumante_map = {'Sim': 'yes', 'Não': 'no'}
                fumante_cod = fumante_map[fumante]
        
        with st.expander("Hábitos Alimentares", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                favc = st.radio(
                    "Consome alimentos muito calóricos frequentemente?",
                    options=['Não', 'Sim'],
                    index=0,
                    horizontal=True
                )
                favc_map = {'Sim': 'yes', 'Não': 'no'}
                favc_cod = favc_map[favc]
            
            with col2:
                fcvc = st.selectbox(
                    "Frequência de consumo de vegetais nas refeições",
                    options=['raramente', 'às vezes', 'sempre'],
                    index=1
                )
                fcvc_map = {'raramente': 1, 'às vezes': 2, 'sempre': 3}
                fcvc_cod = fcvc_map[fcvc]
            
            with col3:
                ncp = st.selectbox(
                    "Número de refeições principais por dia",
                    options=['uma refeição', 'duas', 'três', 'quatro ou mais'],
                    index=2
                )
                ncp_map = {'uma refeição': 1, 'duas': 2, 'três': 3, 'quatro ou mais': 4}
                ncp_cod = ncp_map[ncp]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                caec = st.selectbox(
                    "Faz lanches entre as refeições?",
                    options=['não consome', 'às vezes', 'frequentemente', 'sempre'],
                    index=1
                )
                caec_map = {
                    'não consome': 'no',
                    'às vezes': 'Sometimes',
                    'frequentemente': 'Frequently',
                    'sempre': 'Always'
                }
                caec_cod = caec_map[caec]
            
            with col2:
                ch2o = st.selectbox(
                    "Consumo diário de água",
                    options=['< 1 L/dia', '1–2 L/dia', '> 2 L/dia'],
                    index=1
                )
                ch2o_map = {'< 1 L/dia': 1, '1–2 L/dia': 2, '> 2 L/dia': 3}
                ch2o_cod = ch2o_map[ch2o]
            
            with col3:
                scc = st.radio(
                    "Monitora a ingestão calórica diária?",
                    options=['Não', 'Sim'],
                    index=0,
                    horizontal=True
                )
                scc_map = {'Sim': 'yes', 'Não': 'no'}
                scc_cod = scc_map[scc]
        
        with st.expander("Estilo de Vida", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                faf = st.selectbox(
                    "Frequência semanal de atividade física",
                    options=['nenhuma', '~1–2×/sem', '~3–4×/sem', '5×/sem ou mais'],
                    index=1
                )
                faf_map = {
                    'nenhuma': 0,
                    '~1–2×/sem': 1,
                    '~3–4×/sem': 2,
                    '5×/sem ou mais': 3
                }
                faf_cod = faf_map[faf]
            
            with col2:
                tue = st.selectbox(
                    "Tempo diário com dispositivos eletrônicos",
                    options=['~0–2 h/dia', '~3–5 h/dia', '> 5 h/dia'],
                    index=1
                )
                tue_map = {'~0–2 h/dia': 0, '~3–5 h/dia': 1, '> 5 h/dia': 2}
                tue_cod = tue_map[tue]
            
            with col3:
                calc = st.selectbox(
                    "Frequência de consumo de álcool",
                    options=['não bebe', 'às vezes', 'frequentemente', 'sempre'],
                    index=0
                )
                calc_map = {
                    'não bebe': 'no',
                    'às vezes': 'Sometimes',
                    'frequentemente': 'Frequently',
                    'sempre': 'Always'
                }
                calc_cod = calc_map[calc]
        
        with st.expander("Transporte", expanded=True):
            mtrans = st.selectbox(
                "Meio de transporte habitual",
                options=['carro', 'moto', 'bicicleta', 'transporte público', 'a pé'],
                index=0
            )
            mtrans_map = {
                'carro': 'Automobile',
                'moto': 'Motorbike',
                'bicicleta': 'Bike',
                'transporte público': 'Public_Transportation',
                'a pé': 'Walking'
            }
            mtrans_cod = mtrans_map[mtrans]
        
        submitted = st.form_submit_button("🔍 Realizar Predição", use_container_width=True)
    
    # ------------------------------------------------------------
    # PROCESSAMENTO E PREDIÇÃO (executado APÓS o submit)
    # ------------------------------------------------------------
    if submitted:
        if df_original is None or modelo is None:
            st.error("Não foi possível carregar os dados ou o modelo. Verifique os arquivos.")
        else:
            # 1. Monta o registro
            novo_registro = [
                sexo_cod, idade, altura, peso,
                historico_cod, favc_cod, fcvc_cod, ncp_cod,
                caec_cod, fumante_cod, ch2o_cod, scc_cod,
                faf_cod, tue_cod, calc_cod, mtrans_cod, 0
            ]
            
            cols = df_original.columns.tolist()
            novo_df = pd.DataFrame([novo_registro], columns=cols)
            df_completo = pd.concat([df_original, novo_df], ignore_index=True)
            
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

            df_tratado = df_base_obesidade_tratado(df_completo)
            paciente_tratado = df_tratado.tail(1).reset_index(drop=True)
            cols_to_drop = [col for col in paciente_tratado.columns if col in ['Obesity', 'IMC']]
            paciente_tratado = paciente_tratado.drop(columns=cols_to_drop, errors='ignore')
            
            with st.spinner("Classificando..."):
                predicao_raw = modelo.predict(paciente_tratado)[0]
                predicao_traduzida = dict_obesidade.get(predicao_raw, "Categoria desconhecida")
            
            # ============================================================
            # PAINEL DE RESULTADOS – LIMPO E COM VÍRGULA DECIMAL
            # ============================================================
            st.success("✅ Predição concluída")
            
            # Card principal
            st.markdown(
                f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem 1rem;
                    border-radius: 16px;
                    text-align: center;
                    color: white;
                    margin: 1rem 0;
                    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
                ">
                    <p style="font-size: 1.2rem; opacity: 0.9; margin: 0;">Classificação prevista</p>
                    <h1 style="font-size: 3rem; font-weight: 700; margin: 0.2rem 0; letter-spacing: 1px;">
                        {predicao_traduzida}
                    </h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Métricas das 3 principais probabilidades
            if hasattr(modelo, "predict_proba"):
                probas = modelo.predict_proba(paciente_tratado)[0]
                classes = modelo.classes_
                top_indices = probas.argsort()[-3:][::-1]
                top_probs = probas[top_indices]
                top_classes = [dict_obesidade.get(classes[i], classes[i]) for i in top_indices]
                
            # Resumo dos dados do paciente (com vírgula decimal)
            with st.expander("📋 Dados do paciente (resumo)", expanded=False):
                imc = peso / (altura ** 2)
                resumo = {
                    "Sexo": sexo,
                    "Idade": idade,
                    "Altura": f"{altura:.2f}".replace('.', ',') + " m",
                    "Peso": f"{peso:.0f} kg",
                    "IMC": f"{imc:.1f}".replace('.', ',')
                }
                cols_resumo = st.columns(len(resumo))
                for i, (label, value) in enumerate(resumo.items()):
                    with cols_resumo[i]:
                        st.metric(label, value)
                
                # Demais dados em duas colunas
                with st.container():
                    st.caption("Outros fatores informados")
                    outros = {
                        "Histórico familiar": historico,
                        "Consumo calórico freq.": favc,
                        "Vegetais": fcvc,
                        "Refeições": ncp,
                        "Lanches": caec,
                        "Fumante": fumante,
                        "Água": ch2o,
                        "Monitora calorias": scc,
                        "Atividade física": faf,
                        "Uso eletrônicos": tue,
                        "Álcool": calc,
                        "Transporte": mtrans
                    }
                    cols2 = st.columns(2)
                    for i, (k, v) in enumerate(outros.items()):
                        with cols2[i % 2]:
                            st.caption(f"**{k}:** {v}")


            # Resumo dos dados do paciente (com vírgula decimal)            
            with st.expander("📋 Distribuição dos resultados do modelo", expanded=False):

                import altair as alt

                if hasattr(modelo, "predict_proba"):
                    probas = modelo.predict_proba(paciente_tratado)[0]
                    classes = modelo.classes_

                    # Mapeia probabilidades para português
                    probs_dict = {dict_obesidade.get(cls, cls): prob * 100 for cls, prob in zip(classes, probas)}

                    # DataFrame na ordem fixa
                    df = pd.DataFrame({
                        'Categoria': ordem_categorias,
                        'Probabilidade (%)': [probs_dict.get(cat, 0) for cat in ordem_categorias]
                    })

                    # Gráfico de barras verticais
                    barras = alt.Chart(df).mark_bar(
                        size=45,
                        color='#2c7fb8',
                        cornerRadiusTopLeft=4,
                        cornerRadiusTopRight=4
                    ).encode(
                        x=alt.X('Categoria',
                                sort=ordem_categorias,
                                title=None,
                                axis=alt.Axis(
                                    labelAngle=-15,
                                    labelFontSize=11
                                )
                        ),
                        y=alt.Y('Probabilidade (%)',
                                scale=alt.Scale(domain=[0, 100]),
                                title='Probabilidade (%)',
                                axis=alt.Axis(
                                    grid=False,          # Remove TODAS as grades automáticas
                                    values=[0, 50, 100], # Apenas os rótulos 0, 50 e 100
                                    titleFontSize=12,
                                    labelFontSize=11
                                )
                        )
                    ).properties(height=360)

                    # Linhas manuais em 0 e 100 (as "réguas" mínima e máxima)
                    linha_0 = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='#d3d3d3', strokeDash=[4, 4]).encode(y='y')
                    linha_100 = alt.Chart(pd.DataFrame({'y': [100]})).mark_rule(color='#d3d3d3', strokeDash=[4, 4]).encode(y='y')

                    # Rótulos dos valores percentuais (em cima de cada barra)
                    rotulos = barras.mark_text(
                        align='center',
                        baseline='bottom',
                        dy=-6,
                        fontSize=12,
                        fontWeight='bold',
                        color='#d3d3d3'        # mesma cor do texto das categorias
                    ).encode(
                        text=alt.Text('Probabilidade (%)', format='.1f')
                    )

                    # Combina tudo: barras + regras + rótulos
                    grafico = (barras + linha_0 + linha_100 + rotulos)

                    st.altair_chart(grafico, use_container_width=True)

