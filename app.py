import streamlit as pd
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO EDITORIAL (BEGE SAF)
st.set_page_config(page_title="SAF Intelligence - Série C", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #F5F2E7;
        color: #222222;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #111111;
    }
    </style>
""", unsafe_allow_html=True)

# 2. DICIONÁRIO DE TRADUÇÃO DE POSIÇÕES
posicoes_map = {
    'CB': 'Zagueiro', 'LCB': 'Zagueiro', 'RCB': 'Zagueiro',
    'LB': 'Lateral Esquerdo', 'LWB': 'Lateral Esquerdo',
    'RB': 'Lateral Direito', 'RWB': 'Lateral Direito',
    'DMF': 'Volante', 'LDMF': 'Volante', 'RDMF': 'Volante',
    'LCMF': 'Meia Central', 'RCMF': 'Meia Central',
    'AMF': 'Meia Atacante', 'LAMF': 'Meia Atacante', 'RAMF': 'Meia Atacante',
    'LW': 'Ponta Esquerda', 'LWF': 'Ponta Esquerda',
    'RW': 'Ponta Direita', 'RWF': 'Ponta Direita',
    'CF': 'Centroavante', 'ST': 'Centroavante', 'GK': 'Goleiro'
}

# 3. CABEÇALHO DA PLATAFORMA
st.title("🛡️ SAF Intelligence: Série C 2026")
st.markdown("### Painel de Desempenho Tático e Estatístico — Brusque FC")

# 4. UPLOAD DE DADOS
st.sidebar.header("📁 Painel de Controle")
uploaded_file = st.sidebar.file_uploader("Suba a planilha de dados (.xlsx ou .csv)", type=['xlsx', 'csv'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    if 'Posição' in df.columns:
        df['Posição_PT'] = df['Posição'].map(posicoes_map).fillna('Outro')
    
    if 'Jogador' in df.columns:
        df.loc[df['Jogador'] == 'João Pedro', 'Posição_PT'] = 'Meia Atacante'

    st.sidebar.markdown("---")
    pilar_selecionado = st.sidebar.radio(
        "Selecione o Pilar de Análise:",
        [
            "Pilar 1: Ataque (Letalidade)",
            "Pilar 2: Meio-Campo (Em desenvolvimento)",
            "Pilar 3: Defesa (Em desenvolvimento)",
            "Pilar 4: Goleiros (Em desenvolvimento)"
        ]
    )

    if pilar_selecionado == "Pilar 1: Ataque (Letalidade)":
        st.header("Pilar 1: Eficiência e Tomada de Decisão (Ataque)")
        st.markdown("Este gráfico interativo cruza a **Qualidade das Chances (xG por 90')** contra os **Gols Reais (por 90')**.")

        if 'Remates/90' in df.columns and 'Golos esperados/90' in df.columns:
            # Criar coluna para destacar o Brusque
            df['Destaque'] = df['Equipa'].apply(lambda x: 'Brusque SAF' if x == 'Brusque' else 'Outros Clubes')

            # Gráfico interativo com Plotly (Não precisa de bibliotecas extras)
            fig = px.scatter(
                df, 
                x='Golos esperados/90', 
                y='Golos/90',
                color='Destaque',
                color_discrete_map={'Brusque SAF': '#008000', 'Outros Clubes': '#999999'},
                hover_name='Jogador',
                text='Jogador',
                title="Matriz de Letalidade Ofensiva"
            )

            fig.update_traces(textposition='top center', marker=dict(size=12))
            fig.update_layout(
                plot_bgcolor='#F5F2E7',
                paper_bgcolor='#F5F2E7',
                font=dict(family='serif', color='#222222'),
                title_font=dict(size=18, family='serif')
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("As colunas 'Remates/90' ou 'Golos esperados/90' não foram encontradas no arquivo.")
else:
    st.info("👈 Por favor, faça o upload do arquivo XLSX ou CSV no painel lateral para iniciar a plataforma.")
