import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURAÇÃO DA PÁGINA (ESTILO BEGE SAF / PORTAL DO SPORT)
st.set_page_config(page_title="SAF Graph Engine - Série C", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #F5F2E7;
        color: #222222;
        font-family: 'Georgia', serif;
    }
    h1, h2, h3 {
        color: #111111;
    }
    .stButton>button {
        background-color: #008000;
        color: white;
        font-weight: bold;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ SAF Graph Engine: Criador de Gráficos Táticos")
st.markdown("Gerador automatizado de gráficos de desempenho para a Diretoria e Comissão Técnica.")

# 2. ESCOLHER O TIPO DE GRÁFICO
tipo_grafico = st.sidebar.selectbox(
    "Escolha o Gráfico para Gerar:",
    [
        "Pilar 1: Letalidade de Ataque (Volume x Qualidade)",
        "Pilar 3: Exposição Defensiva (Remates Sofridos)",
        "Pilar 4: Eficiência de Goleiros"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** Insira os dados abaixo ou faça upload da sua planilha para atualizar o gráfico instantaneamente.")

# 3. ENTRADA DE DADOS SIMULADA / OU UPLOAD
uploaded_file = st.sidebar.file_uploader("Ou envie sua planilha XLSX/CSV", type=['xlsx', 'csv'])

if uploaded_file is not None:
    if uploaded_file.name.endswith('csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
else:
    # Dados padrão baseados no seu relatório da Série C caso não suba nada ainda
    data_padrao = {
        'Time': ['Brusque', 'Guarani', 'Maringá', 'Paysandu', 'Botafogo PB', 'Ferroviária', 'Amazonas', 'Santa Cruz', 'Caxias', 'Ituano'],
        'Remates_Jogo': [11.13, 15.32, 14.58, 14.39, 11.84, 12.44, 10.43, 10.37, 11.95, 12.69],
        'xG_Remate': [0.10, 0.10, 0.09, 0.09, 0.10, 0.09, 0.10, 0.09, 0.09, 0.09],
        'Remates_Sofridos': [14.52, 10.38, 10.12, 11.40, 12.75, 11.54, 11.10, 12.59, 10.88, 11.83]
    }
    df = pd.DataFrame(data_padrao)

# 4. GERAÇÃO DO GRÁFICO ESCOLHIDO
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#F5F2E7')
ax.set_facecolor('#F5F2E7')

if tipo_grafico == "Pilar 1: Letalidade de Ataque (Volume x Qualidade)":
    st.subheader("📊 Gráfico: Volume de Chutes vs Qualidade (xG por Chute)")
    
    x = df['Remates_Jogo']
    y = df['xG_Remate']
    times = df['Time']

    # Linhas de média (Quadrantes)
    ax.axvline(x.mean(), color='#999999', linestyle='--', alpha=0.6)
    ax.axhline(y.mean(), color='#999999', linestyle='--', alpha=0.6)

    # Plotar pontos
    for i in range(len(times)):
        is_brusque = times[i] == 'Brusque'
        cor = '#008000' if is_brusque else '#888888'
        tamanho = 400 if is_brusque else 150
        borda = '#FFD700' if is_brusque else 'none'
        
        ax.scatter(x[i], y[i], s=tamanho, color=cor, edgecolors=borda, linewidth=2, zorder=3)
        
        # Nomear apenas o Brusque ou todos se preferir
        if is_brusque:
            ax.text(x[i], y[i] + 0.003, times[i], fontsize=11, fontweight='bold', color='#008000', ha='center')
        else:
            ax.text(x[i], y[i] + 0.002, times[i], fontsize=8, color='#555555', ha='center', alpha=0.7)

    ax.set_xlabel("Finalizações por Jogo (Volume)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Qualidade Média (xG por Finalização)", fontsize=11, fontweight='bold')
    ax.set_title("Série C 2026: Quem mais finaliza x Quem melhor finaliza", fontsize=14, fontweight='bold', pad=15)

elif tipo_grafico == "Pilar 3: Exposição Defensiva (Remates Sofridos)":
    st.subheader("📊 Gráfico: Análise de Carga Defensiva")
    
    x = df['Time']
    y = df['Remates_Sofridos']
    
    # Cores (Brusque em destaque)
    cores = ['#008000' if t == 'Brusque' else '#888888' for t in x]
    
    ax.bar(x, y, color=cores, width=0.6)
    ax.axhline(y.mean(), color='red', linestyle='--', label='Média da Competição')
    
    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Remates Sofridos por Jogo", fontsize=11, fontweight='bold')
    ax.set_title("Série C 2026: Carga Defensiva (Quem mais cede finalizações)", fontsize=14, fontweight='bold', pad=15)
    ax.legend()

# Limpeza visual estilo editorial
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()

# Exibir na tela do site
st.pyplot(fig)

st.markdown("---")
st.download_button(
    label="📥 Baixar Gráfico em Imagem (PNG)",
    data=fig.savefig("grafico_saf.png", format="png", facecolor='#F5F2E7', bbox_inches='tight'),
    file_name="grafico_desempenho_brusque.png",
    mime="image/png"
)
