import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import joblib
import os
from pathlib import Path

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
st.sidebar.title("🧭 Navegação")
pagina = st.sidebar.radio(
    "Escolha uma seção:",
    options=["📊 Análise de Dados", "🧠 Predição de Obesidade"],
    index=1  # Inicia na página de predição (mais usada)
)

st.sidebar.markdown("---")
st.sidebar.caption("Desenvolvido para o Tech Challenge - Data Analytics (FIAP)")

# ------------------------------------------------------------
# FUNÇÕES DE CARREGAMENTO (com cache)
# ------------------------------------------------------------
@st.cache_data
def carregar_dataset():
    caminho_pasta = Path(r"C:\Users\fabio\Desktop\Código python\FIAP\FIAP_fase4\0_tech_challenge\Base de dados")
    caminho_arquivo = caminho_pasta / "Obesity.csv"
    if not caminho_arquivo.exists():
        st.error(f"Arquivo de dados não encontrado em: {caminho_arquivo}")
        return None
    return pd.read_csv(caminho_arquivo)

@st.cache_resource
def carregar_modelo():
    caminho_modelo = os.path.join(os.getcwd(), "modelo", "model_lgb.jlib")
    if not os.path.exists(caminho_modelo):
        st.error(f"Modelo não encontrado em: {caminho_modelo}")
        return None
    return joblib.load(caminho_modelo)

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

# Importa função de pré-processamento (se existir)
try:
    from analise_funcoes import df_base_obesidade_tratado
except ImportError:
    def df_base_obesidade_tratado(df):
        return df.copy()

# ------------------------------------------------------------
# PÁGINA 1: ANÁLISE DE DADOS (POWER BI)
# ------------------------------------------------------------
if pagina == "📊 Análise de Dados":
    st.title("📊 Análise de Dados - Obesidade")
    st.markdown(
        """
        Acompanhe abaixo o dashboard interativo com os principais insights sobre obesidade, 
        desenvolvido no Power BI.
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
                    options=['Fêmea', 'Macho'],
                    index=0,
                    horizontal=True
                )
                sexo_map = {'Fêmea': 'Female', 'Macho': 'Male'}
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
                st.caption(f"Altura selecionada: {altura:.2f}".replace('.', ',') + " m")
        
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
                
                col_m1, col_m2, col_m3 = st.columns(3)
                with col_m1:
                    st.metric("🥇 Mais provável", top_classes[0], delta=f"{top_probs[0]*100:.1f}%")
                with col_m2:
                    st.metric("🥈 Segunda", top_classes[1], delta=f"{top_probs[1]*100:.1f}%")
                with col_m3:
                    st.metric("🥉 Terceira", top_classes[2], delta=f"{top_probs[2]*100:.1f}%")
                
                # Gráfico compacto com as 5 principais
                prob_df = pd.DataFrame({
                    "Classe": [dict_obesidade.get(c, c) for c in classes],
                    "Probabilidade": probas
                }).sort_values("Probabilidade", ascending=False).head(5)
                
                st.markdown("##### 📊 Distribuição de probabilidades")
                st.bar_chart(prob_df.set_index("Classe")["Probabilidade"], height=250)
            
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
