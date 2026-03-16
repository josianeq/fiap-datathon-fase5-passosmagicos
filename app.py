import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Datathon - Passos Mágicos",
    layout="wide"
)

# --------------------------------------------------
# LOGOS
# --------------------------------------------------

col1, col2, col3 = st.columns([3,2,3])

with col2:
    st.image("logos.png", width=300)

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("Datathon - Passos Mágicos")

st.markdown(
"""
Dashboard de análise exploratória dos dados educacionais
dos estudantes da **Passos Mágicos**.
"""
)

# --------------------------------------------------
# CARREGAR BASE
# --------------------------------------------------

df = pd.read_excel(
    "BASE DE DADOS PEDE 2024 - DATATHON.xlsx",
    sheet_name="PEDE2024"
)

df.columns = df.columns.str.strip()

# --------------------------------------------------
# PADRONIZAR NOMES DAS PEDRAS
# --------------------------------------------------

if "Pedra 2024" in df.columns:

    df["Pedra 2024"] = (
        df["Pedra 2024"]
        .astype(str)
        .str.strip()
        .str.title()
        .replace({
            "Agata":"Ágata",
            "Ágata":"Ágata",
            "Topazio":"Topázio",
            "Topázio":"Topázio"
        })
    )

# --------------------------------------------------
# TRATAR FASE
# --------------------------------------------------

df["Fase"] = df["Fase"].astype(str)
df["Fase"] = df["Fase"].str.replace("Alfa","0",case=False)
df["Fase"] = df["Fase"].str.extract(r'(\d+)')
df["Fase"] = pd.to_numeric(df["Fase"],errors="coerce")

df = df[df["Fase"].between(0,7)]

# --------------------------------------------------
# FILTRO
# --------------------------------------------------

st.sidebar.title("Filtros")

fases = sorted(df["Fase"].dropna().unique())

fase_selecionada = st.sidebar.selectbox(
    "Selecione uma fase",
    ["Todas"] + list(fases)
)

if fase_selecionada == "Todas":
    df_filtro = df
else:
    df_filtro = df[df["Fase"] == fase_selecionada]

st.sidebar.metric("Alunos na seleção",len(df_filtro))

# --------------------------------------------------
# MÉTRICAS PRINCIPAIS
# --------------------------------------------------

col1,col2,col3 = st.columns(3)

col1.metric("Total de alunos",len(df_filtro))

if "IEG" in df_filtro.columns:
    col2.metric("Média IEG",round(df_filtro["IEG"].mean(),2))

if "IDA" in df_filtro.columns:
    col3.metric("Média IDA",round(df_filtro["IDA"].mean(),2))

st.divider()

# --------------------------------------------------
# ABAS
# --------------------------------------------------

aba1, aba2, aba3, aba4 = st.tabs([
    "Análise dos Dados",
    "Relação entre Indicadores",
    "Insights",
    "Exploração do INDE"
])

# ==================================================
# ABA 1
# ==================================================

with aba1:

    st.subheader("Visualização da Base")

    st.dataframe(df_filtro)

    col1,col2 = st.columns(2)

    if "IEG" in df_filtro.columns:

        with col1:

            st.subheader("Distribuição do IEG")

            fig,ax = plt.subplots(figsize=(3,2))

            sns.histplot(df_filtro["IEG"].dropna(),bins=20,ax=ax)

            ax.set_ylabel("Alunos", fontsize=8)

            plt.tight_layout()

            st.pyplot(fig)

    if "IDA" in df_filtro.columns:

        with col2:

            st.subheader("Distribuição do IDA")

            fig,ax = plt.subplots(figsize=(3,2))

            sns.histplot(df_filtro["IDA"].dropna(),bins=20,ax=ax)

            ax.set_ylabel("Alunos", fontsize=8)

            plt.tight_layout()

            st.pyplot(fig)

    st.divider()

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("Distribuição de Alunos por Fase")

        fase_counts = df_filtro.groupby("Fase").size()

        fig,ax = plt.subplots(figsize=(3,2))

        bars = ax.bar(fase_counts.index,fase_counts.values)

        ax.set_ylabel("Alunos",fontsize=8)

        ax.tick_params(labelsize=8)

        ax.set_ylim(0,max(fase_counts.values)*1.15)

        for bar in bars:

            y = bar.get_height()

            ax.text(
                bar.get_x()+bar.get_width()/2,
                y*0.9,
                int(y),
                ha="center",
                va="top",
                fontsize=8,
                color="white",
                fontweight="bold"
            )

        plt.tight_layout()

        st.pyplot(fig)

    with col2:

        if "Pedra 2024" in df_filtro.columns:

            st.subheader("Distribuição das Pedras")

            ordem_pedras = [
                "Quartzo",
                "Ágata",
                "Ametista",
                "Topázio"
            ]

            pedra_counts = (
                df_filtro["Pedra 2024"]
                .value_counts()
                .reindex(ordem_pedras, fill_value=0)
            )

            fig,ax = plt.subplots(figsize=(3,2))

            bars = ax.bar(
                pedra_counts.index,
                pedra_counts.values
            )

            ax.tick_params(axis='x',labelsize=8)

            ax.set_ylim(0,max(pedra_counts.values)*1.15)

            for bar in bars:

                y = bar.get_height()

                ax.text(
                    bar.get_x()+bar.get_width()/2,
                    y*0.9,
                    int(y),
                    ha="center",
                    va="top",
                    fontsize=8,
                    color="white",
                    fontweight="bold"
                )

            plt.xticks(rotation=20)

            plt.tight_layout()

            st.pyplot(fig)

# ==================================================
# ABA 2
# ==================================================

with aba2:

    col1,col2 = st.columns(2)

    if "IEG" in df_filtro.columns and "IDA" in df_filtro.columns:

        with col1:

            st.subheader("Relação entre IEG e IDA")

            fig,ax = plt.subplots(figsize=(3,2))

            sns.scatterplot(
                data=df_filtro,
                x="IEG",
                y="IDA",
                ax=ax
            )

            ax.tick_params(labelsize=8)

            plt.tight_layout()

            st.pyplot(fig)

    indicadores = []

    for col in ["IEG","IDA"]:
        if col in df_filtro.columns:
            indicadores.append(col)

    if len(indicadores) >= 2:

        with col2:

            st.subheader("Correlação entre Indicadores")

            corr = df_filtro[indicadores].corr()

            fig,ax = plt.subplots(figsize=(3,2))

            sns.heatmap(
                corr,
                annot=True,
                cmap="Blues",
                ax=ax
            )

            ax.tick_params(labelsize=8)

            plt.tight_layout()

            st.pyplot(fig)

# ==================================================
# ABA 3
# ==================================================

with aba3:

    if "INDE 2024" in df_filtro.columns:

        st.subheader("Distribuição de Risco Educacional")

        df_risco = df_filtro.copy()

        df_risco["nivel_risco"] = pd.cut(
            df_risco["INDE 2024"],
            bins=[0,6,8,10],
            labels=[
                "Risco educacional",
                "Atenção",
                "Bom desempenho"
            ]
        )

        risco = (
            df_risco["nivel_risco"]
            .value_counts()
            .reindex([
                "Risco educacional",
                "Atenção",
                "Bom desempenho"
            ])
        )

        fig, ax = plt.subplots(figsize=(3,2))

        bars = ax.bar(risco.index, risco.values)

        ax.set_ylim(0, max(risco.values) * 1.3)

        ax.set_ylabel("Alunos", fontsize=8)

        ax.tick_params(axis='y', labelsize=8)
        ax.tick_params(axis='x', labelsize=7)

        plt.xticks(rotation=10)

        for bar in bars:

            y = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width()/2,
                y*0.92,
                int(y),
                ha="center",
                va="top",
                fontsize=8,
                color="white",
                fontweight="bold"
            )

        plt.tight_layout()

        st.pyplot(fig, width=500)

    # INSIGHTS

    st.subheader("Principais Insights")

    st.markdown(
    """
    • A maior parte dos estudantes encontra-se na faixa **Atenção**, indicando que muitos alunos estão em nível intermediário de desempenho educacional.

    • Existe uma **relação positiva entre engajamento escolar (IEG) e desempenho acadêmico (IDA)**, sugerindo que estudantes mais engajados tendem a apresentar melhor desempenho.

    • A análise da distribuição do **INDE 2024** mostra que apenas uma parcela menor dos estudantes está em situação de **risco educacional**, enquanto a maioria apresenta desempenho intermediário ou adequado.
""")

# ==================================================
# ABA 4
# ==================================================

with aba4:

    st.subheader("Exploração do Indicador INDE")

    st.write("""
Explore como diferentes valores do **INDE**
podem indicar níveis diferentes de risco educacional.
""")

    st.markdown("### Simulação de risco educacional")

    inde_valor = st.slider(
        "Selecione um valor de INDE",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.1
    )

    st.write("INDE selecionado:", round(inde_valor,2))

    if inde_valor < 6:

        st.error("Classificação: Risco educacional")

        st.info("""
Recomendação pedagógica:

• acompanhamento pedagógico mais próximo  
• reforço escolar  
• diagnóstico de dificuldades
""")

    elif inde_valor < 8:

        st.warning("Classificação: Atenção")

        st.info("""
Recomendação pedagógica:

• monitoramento contínuo  
• incentivo ao engajamento  
• acompanhamento preventivo
""")

    else:

        st.success("Classificação: Bom desempenho")

        st.info("""
Recomendação pedagógica:

• estímulo à autonomia acadêmica  
• atividades de aprofundamento  
• manutenção das boas práticas
""")

    st.subheader("Interpretação")

    st.write("""
Valores menores no INDE podem indicar necessidade de maior acompanhamento pedagógico,
enquanto valores mais altos indicam melhor desenvolvimento educacional.
""")