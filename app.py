import streamlit as st

# Tenta instalar as bibliotecas automaticamente caso o Streamlit ignore o requirements.txt
try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
    import os
    os.system('pip install pandas matplotlib openpyxl')
    import pandas as pd
    import matplotlib.pyplot as plt

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
        st.markdown("Este gráfico cruza a **Qualidade das Chances (xG por 90')** contra os **Gols Reais (por 90')**.")

        if 'Remates/90' in df.columns and 'Golos esperados/90' in df.columns:
            fig, ax = plt.subplots(figsize=(10, 6), facecolor='#F5F2E7')
            ax.set_facecolor('#F5F2E7')

            for i, row in df.iterrows():
                is_brusque = row.get('Equipa') == 'Brusque' or row.get('Equipe') == 'Brusque'
                cor = '#008000' if is_brusque else '#999999'
                tamanho = 300 if is_brusque else 80
                borda = '#FFD700' if is_brusque else 'none'
                
                x = row.get('Golos esperados/90', 0)
                y = row.get('Golos/90', 0)
                
                ax.scatter(x, y, s=tamanho, color=cor, edgecolors=borda, linewidth=2, alpha=0.8)
                
                if is_brusque and y > 0.1:
                    ax.text(x, y + 0.02, str(row.get('Jogador', '')), fontsize=9, fontweight='bold', ha='center')

            ax.axvline(df['Golos esperados/90'].mean(), color='gray', linestyle='--', alpha=0.4)
            ax.axhline(df['Gols/90'].mean(), color='gray', linestyle='--', alpha=0.4)

            ax.set_title("Matriz de Letalidade Ofensiva", fontsize=14, fontweight='bold', family='serif')
            ax.set_xlabel("Gols Esperados por 90' (xG/90)", fontsize=10)
            ax.set_ylabel("Gols Reais por 90'", fontsize=10)
            
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            st.pyplot(fig)
        else:
            st.error("As colunas 'Remates/90' ou 'Golos esperados/90' não foram encontradas no arquivo.")
else:
    st.info("👈 Por favor, faça o upload do arquivo XLSX ou CSV no painel lateral para iniciar a plataforma.")
