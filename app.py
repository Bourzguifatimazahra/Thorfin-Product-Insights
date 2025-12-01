 
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF
from openai import AzureOpenAI
from wordcloud import WordCloud, STOPWORDS
import io, os, tempfile, base64, textwrap
from datetime import datetime
from dotenv import load_dotenv
 
load_dotenv()  # charge le fichier .env
API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = "https://bourz-mihhzl50-eastus2.cognitiveservices.azure.com/"
DEPLOYMENT_NAME = "gpt-5-chat"
API_VERSION = "2024-12-01-preview"

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)
# --------------------------
# Streamlit setup & header
# --------------------------
st.set_page_config(page_title="Thorfin Product Insights - Pro", layout="wide", initial_sidebar_state="expanded")
st.markdown(
    """
    <div style='background: linear-gradient(90deg,#0f172a,#0b8453); padding:18px; border-radius:12px;'>
      <h1 style='color:white; text-align:center; margin:0;'>Thorfin Product Insights — Pro Dashboard</h1>
      <p style='color:#d1fae5; text-align:center; margin:0.1rem 0 0 0;'>Exploration, KPI, visualisations & rapports (HTML + PDF)</p>
    </div>
    """, unsafe_allow_html=True
)
st.write("")

# --------------------------
# Sidebar: upload + filters
# --------------------------
st.sidebar.header("1) Dataset & filtres")
uploaded_file = st.sidebar.file_uploader("Uploader dataset (CSV / Excel / JSON)", type=["csv", "xlsx", "xls", "json"])

@st.cache_data
def load_data(file):
    if file is None:
        return None
    try:
        if file.name.lower().endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.lower().endswith((".xls", ".xlsx")):
            df = pd.read_excel(file)
        elif file.name.lower().endswith(".json"):
            df = pd.read_json(file)
        else:
            return None
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return None
    # normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df = load_data(uploaded_file)

# helper: safe column check
def has_cols(dataframe, cols):
    return all(c in dataframe.columns for c in cols)

# --------------------------
# If no data -> show instructions
# --------------------------
if df is None:
    st.info("Uploader un dataset (CSV / Excel / JSON) dans la sidebar pour commencer. "
            "Le dataset attendu contient des colonnes comme : client_id, product, product_description, price, rating, review_text, review_language, purchase_date.")
    st.stop()

# --------------------------
# Data normalisation & basic cleaning
# --------------------------
# try to coerce types if exist
if 'price' in df.columns:
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
if 'rating' in df.columns:
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
if 'purchase_date' in df.columns:
    df['purchase_date'] = pd.to_datetime(df['purchase_date'], errors='coerce')

st.success(f"Jeu de données chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes.")

# --------------------------
# Sidebar filters (interactive)
# --------------------------
st.sidebar.subheader("Filtres interactifs")

# Date filter
if 'purchase_date' in df.columns and df['purchase_date'].notna().any():
    min_date = df['purchase_date'].min().date()
    max_date = df['purchase_date'].max().date()
    date_range = st.sidebar.date_input("Date d'achat", [min_date, max_date])
    try:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        df = df[(df['purchase_date'] >= start_date) & (df['purchase_date'] <= end_date)]
    except Exception:
        pass

# Price filter
if 'price' in df.columns and df['price'].notna().any():
    pmin = float(np.nanmin(df['price']))
    pmax = float(np.nanmax(df['price']))
    price_range = st.sidebar.slider("Prix", min_value=round(pmin,2), max_value=round(pmax,2), value=(round(pmin,2), round(pmax,2)))
    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

# Rating filter
if 'rating' in df.columns and df['rating'].notna().any():
    rmin = int(np.nanmin(df['rating']))
    rmax = int(np.nanmax(df['rating']))
    rating_range = st.sidebar.slider("Note", min_value=rmin, max_value=rmax, value=(rmin, rmax))
    df = df[(df['rating'] >= rating_range[0]) & (df['rating'] <= rating_range[1])]

# Product search filter
if 'product' in df.columns:
    product_search = st.sidebar.text_input("Rechercher produit (nom partiel)")
    if product_search:
        df = df[df['product'].str.contains(product_search, case=False, na=False)]

# --------------------------
# KPIs
# --------------------------
st.header("Indicateurs clés (KPIs)")
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

num_reviews = int(df.shape[0])
avg_rating = float(df['rating'].mean()) if 'rating' in df.columns and df['rating'].notna().any() else np.nan
avg_price = float(df['price'].mean()) if 'price' in df.columns and df['price'].notna().any() else np.nan
top_product = None
if 'product' in df.columns and 'rating' in df.columns:
    grouped = df.groupby('product')['rating'].mean().dropna()
    if not grouped.empty:
        top_product = grouped.idxmax()

kpi_col1.metric("Nombre de reviews", f"{num_reviews}")
kpi_col2.metric("Note moyenne", f"{avg_rating:.2f}" if not np.isnan(avg_rating) else "N/A")
kpi_col3.metric("Prix moyen", f"${avg_price:.2f}" if not np.isnan(avg_price) else "N/A")
kpi_col4.metric("Produit le mieux noté", top_product if top_product else "N/A")

st.markdown("---")

# --------------------------
# Visualisations (Plotly & Seaborn)
# --------------------------
st.header("Visualisations avancées")

# Prepare numeric_df for heatmap/pairplot
numeric_df = df.select_dtypes(include=[np.number])

# 1) Plotly histogram (price)
if 'price' in df.columns and df['price'].notna().any():
    fig_price = px.histogram(df, x='price', nbins=25, title="Distribution des prix", labels={'price':'Prix'})
    st.plotly_chart(fig_price, use_container_width=True)

# 2) Boxplot / Violin plot of ratings by product (Plotly)
if has_cols(df, ['product','rating']):
    fig_box = px.box(df, x='product', y='rating', title="Boxplot : note par produit")
    st.plotly_chart(fig_box, use_container_width=True)

    fig_violin = px.violin(df, x='product', y='rating', box=True, points='all', title="Violin : note par produit")
    st.plotly_chart(fig_violin, use_container_width=True)

# 3) Scatter Price vs Rating (Plotly)
if has_cols(df, ['price','rating']):
    fig_scatter = px.scatter(df, x='price', y='rating', color='product' if 'product' in df.columns else None,
                             title="Scatter : Prix vs Note", hover_data=['product'] if 'product' in df.columns else None)
    st.plotly_chart(fig_scatter, use_container_width=True)

# 4) Pie / Donut chart of product distribution (Plotly)
if 'product' in df.columns:
    pc = df['product'].value_counts().reset_index()
    pc.columns = ['product_name', 'count']
    if not pc.empty:
        fig_pie = px.pie(pc, values='count', names='product_name', title="Répartition des produits")
        st.plotly_chart(fig_pie, use_container_width=True)

        # Donut (percent + labels)
        fig_donut = px.pie(pc, values='count', names='product_name', hole=0.45,
                           title="Donut : Répartition des produits")
        st.plotly_chart(fig_donut, use_container_width=True)

# 5) Pareto chart (bar + cumulative line) top products by count
if 'product' in df.columns:
    pareto = df['product'].value_counts().reset_index()
    pareto.columns = ['product', 'count']
    pareto['cumulative'] = pareto['count'].cumsum() / pareto['count'].sum()
    fig_pareto = px.bar(pareto.head(20), x='product', y='count', title="Pareto : top produits (count)")
    fig_pareto.add_scatter(x=pareto.head(20)['product'], y=pareto.head(20)['cumulative'], yaxis="y2", mode='lines+markers', name='Cumulé')
    fig_pareto.update_layout(
        yaxis=dict(title='Count'),
        yaxis2=dict(title='Cumulative %', overlaying='y', side='right', tickformat='.0%'),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

# 6) Pairplot & heatmap using seaborn for numeric columns (if enough numeric cols)
if numeric_df.shape[1] >= 2:
    with st.expander("Pairplot & Heatmap (seaborn)"):
        # Pairplot: may be slow for big datasets - sample if large
        sample_df = numeric_df.sample(n=min(200, numeric_df.shape[0]), random_state=42)
        pair_fig = sns.pairplot(sample_df)
        st.pyplot(pair_fig)

        # Heatmap
        fig_h, ax_h = plt.subplots(figsize=(6, 5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax_h)
        st.pyplot(fig_h)

# 7) WordCloud from review_text
if 'review_text' in df.columns:
    st.subheader("WordCloud des reviews (Top 2000 caractères)")
    text = " ".join(df['review_text'].dropna().astype(str).tolist())
    if text.strip() == "":
        st.write("Aucun texte de review disponible.")
    else:
        stopwords = set(STOPWORDS)
        wc = WordCloud(width=900, height=400, background_color='white', stopwords=stopwords, collocations=False)
        wc.generate(text[:2000])
        fig_wc, ax_wc = plt.subplots(figsize=(12,4))
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis('off')
        st.pyplot(fig_wc)

st.markdown("---")

# --------------------------
# Product insights panel
# --------------------------
st.header("Exploration produit")
prod_col1, prod_col2 = st.columns([3,1])
with prod_col1:
    selected_product = st.selectbox("Sélectionner un produit", df['product'].unique())
    product_df = df[df['product'] == selected_product]

    st.markdown(f"**{selected_product}** — {product_df.shape[0]} reviews")
    if 'rating' in product_df.columns:
        st.write(f"- Note moyenne : **{product_df['rating'].mean():.2f}**")
    if 'price' in product_df.columns:
        st.write(f"- Prix moyen : **${product_df['price'].mean():.2f}**")

    st.subheader("Extraits de reviews")
    sample_reviews = product_df['review_text'].dropna().astype(str).tolist()[:20]
    if sample_reviews:
        st.text_area("Reviews (éditable)", value="\n\n".join(sample_reviews), height=220)
    else:
        st.write("Aucun review disponible pour ce produit.")

with prod_col2:
    # small charts for selected product
    if 'rating' in product_df.columns:
        fig_r, ax_r = plt.subplots()
        sns.histplot(product_df['rating'].dropna(), bins=5, ax=ax_r)
        ax_r.set_title("Distribution des notes")
        st.pyplot(fig_r)
    if 'price' in product_df.columns:
        fig_p, ax_p = plt.subplots()
        sns.boxplot(x=product_df['price'].dropna(), ax=ax_p)
        ax_p.set_title("Distribution prix (boxplot)")
        st.pyplot(fig_p)

# --------------------------
# AI Summary button (Azure GPT-5)
# --------------------------
st.markdown("---")
st.header("AI : Résumé automatique des reviews")
ai_col1, ai_col2 = st.columns([3,1])
with ai_col1:
    ai_prompt_extra = st.text_area("Contrainte / ton pour le résumé (ex: court, points principaux, suggestions produit)", value="Résumé concis en 4 points : points positifs, axes d'amélioration, tendances, suggestions.")
    if st.button("Générer résumé AI pour le produit sélectionné"):
        reviews_to_send = "\n".join(product_df['review_text'].dropna().astype(str).tolist()[:30])
        if not reviews_to_send.strip():
            st.warning("Pas assez de texte dans les reviews pour générer un résumé.")
        else:
            system_msg = "You are a concise product insights assistant that summarizes customer reviews, extracts main pros/cons, and gives suggestions."
            user_msg = f"{ai_prompt_extra}\n\nReviews:\n{reviews_to_send}"
            try:
                response = client.chat.completions.create(
                    messages=[
                        {"role":"system", "content": system_msg},
                        {"role":"user", "content": user_msg}
                    ],
                    model=DEPLOYMENT_NAME,
                    max_tokens=700,
                    temperature=0.2
                )
                ai_summary = response.choices[0].message.content
                st.subheader("Résumé AI")
                st.write(ai_summary)
            except Exception as e:
                st.error(f"Erreur Azure OpenAI : {e}")

with ai_col2:
    st.info("Astuce : réduis la taille des reviews à 30 premiers pour limiter les tokens.")

# --------------------------
# Export: HTML & PDF
# --------------------------
st.markdown("---")
st.header("Rapports : Export HTML & PDF")

def fig_to_base64_matplotlib(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def save_plotly_png(fig):
    """Render a Plotly figure as PNG bytes (requires kaleido installed in environment)."""
    try:
        img_bytes = fig.to_image(format="png")
        return img_bytes
    except Exception:
        return None

# HTML export
if st.button("Générer rapport HTML pour le produit sélectionné"):
    # prepare images encoded in base64
    imgs = {}
    # matplotlib small plots
    # rating hist
    if 'rating' in product_df.columns and not product_df['rating'].dropna().empty:
        fig_h, ax_h = plt.subplots()
        sns.histplot(product_df['rating'], bins=5, ax=ax_h)
        ax_h.set_title("Distribution des notes")
        imgs['hist_rating'] = fig_to_base64_matplotlib(fig_h)
        plt.close(fig_h)
    # price box
    if 'price' in product_df.columns and not product_df['price'].dropna().empty:
        fig_b, ax_b = plt.subplots()
        sns.boxplot(x=product_df['price'].dropna(), ax=ax_b)
        ax_b.set_title("Distribution des prix")
        imgs['box_price'] = fig_to_base64_matplotlib(fig_b)
        plt.close(fig_b)
    # wordcloud
    if 'review_text' in product_df.columns:
        text = " ".join(product_df['review_text'].dropna().astype(str).tolist())
        if text.strip():
            wc = WordCloud(width=800, height=300, background_color='white', stopwords=set(STOPWORDS)).generate(text[:2000])
            fig_wc, ax_wc = plt.subplots(figsize=(10,3))
            ax_wc.imshow(wc); ax_wc.axis('off')
            imgs['wordcloud'] = fig_to_base64_matplotlib(fig_wc)
            plt.close(fig_wc)
    # KPIs & summary text
    html_summary_text = ai_summary if 'ai_summary' in locals() else (ai_summary if 'ai_summary' in globals() else "")

    # build HTML
    html = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Thorfin Report - {selected_product}</title>
<style>
body{{font-family:Arial, Helvetica, sans-serif; background:#f5f7fa; color:#111; padding:18px}}
.header{{background:linear-gradient(90deg,#0b8453,#0f172a); color:white; padding:16px; border-radius:8px; text-align:center}}
.container{{max-width:1100px; margin:18px auto}}
.card{{background:white; padding:14px; border-radius:8px; box-shadow:0 6px 14px rgba(0,0,0,0.06); margin-bottom:14px}}
.kpi{{display:flex; gap:18px; flex-wrap:wrap}}
.kpi .item{{flex:1; min-width:160px; padding:12px; border-radius:6px; background:#f8fafc; text-align:center}}
img{{max-width:100%; height:auto; display:block; margin:8px auto}}
pre{{background:#f3f4f6; padding:12px; border-radius:6px; overflow:auto}}
</style>
</head>
<body>
<div class="container">
<div class="header"><h1>Thorfin Product Insights — {selected_product}</h1></div>

<div class="card">
  <h2>KPIs</h2>
  <div class="kpi">
    <div class="item"><strong>Nombre de reviews</strong><div>{product_df.shape[0]}</div></div>
    <div class="item"><strong>Note moyenne</strong><div>{product_df['rating'].mean() if 'rating' in product_df.columns else 'N/A'}</div></div>
    <div class="item"><strong>Prix moyen</strong><div>${product_df['price'].mean() if 'price' in product_df.columns else 'N/A'}</div></div>
  </div>
</div>
"""

    # add images
    if 'hist_rating' in imgs:
        html += f"""
        <div class="card"><h2>Distribution des notes</h2>
        <img src="data:image/png;base64,{imgs['hist_rating']}"></div>
        """
    if 'box_price' in imgs:
        html += f"""
        <div class="card"><h2>Distribution des prix</h2>
        <img src="data:image/png;base64,{imgs['box_price']}"></div>
        """
    if 'wordcloud' in imgs:
        html += f"""
        <div class="card"><h2>WordCloud (reviews)</h2>
        <img src="data:image/png;base64,{imgs['wordcloud']}"></div>
        """

    html += f"""
    <div class="card"><h2>Résumé AI</h2><pre>{html_summary_text}</pre></div>
    <div class="card"><h2>Extraits de reviews</h2><pre>{textwrap.fill(' '.join(sample_reviews), width=120)}</pre></div>
    <div style="text-align:center; font-size:12px; color:#666; margin-top:12px">Généré le {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
    </div></body></html>
    """

    # save html file
    html_filename = f"{selected_product}_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.html"
    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html)
    with open(html_filename, "rb") as f:
        st.success(f"Rapport HTML généré : {html_filename}")
        st.download_button("Télécharger HTML", f, file_name=html_filename)

# PDF export
if st.button("Générer PDF pro (avec graphiques)"):
    tmp_files = []
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Thorfin Product Insights - {selected_product}", 0, 1, 'C')
        pdf.ln(4)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, f"Nombre de reviews: {product_df.shape[0]}", 0, 1)
        if 'rating' in product_df.columns:
            pdf.cell(0, 8, f"Note moyenne: {product_df['rating'].mean():.2f}", 0, 1)
        if 'price' in product_df.columns:
            pdf.cell(0, 8, f"Prix moyen: ${product_df['price'].mean():.2f}", 0, 1)
        pdf.ln(4)

        # plots -> temp files
        if 'rating' in product_df.columns and not product_df['rating'].dropna().empty:
            fig_tmp, ax_tmp = plt.subplots()
            sns.histplot(product_df['rating'], bins=5, ax=ax_tmp)
            ax_tmp.set_title("Distribution des notes")
            t = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig_tmp.savefig(t.name, bbox_inches='tight')
            plt.close(fig_tmp)
            tmp_files.append(t.name)
            pdf.image(t.name, x=10, w=pdf.w - 20)

        if 'price' in product_df.columns and not product_df['price'].dropna().empty:
            fig_tmp2, ax_tmp2 = plt.subplots()
            sns.boxplot(x=product_df['price'].dropna(), ax=ax_tmp2)
            ax_tmp2.set_title("Boxplot prix")
            t2 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            fig_tmp2.savefig(t2.name, bbox_inches='tight')
            plt.close(fig_tmp2)
            tmp_files.append(t2.name)
            pdf.add_page()
            pdf.image(t2.name, x=10, w=pdf.w - 20)

        # AI summary
        if 'ai_summary' in locals() and ai_summary:
            pdf.add_page()
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Résumé AI", 0, 1)
            pdf.set_font("Arial", "", 10)
            # split into chunks for multi_cell
            for line in ai_summary.split("\n"):
                pdf.multi_cell(0, 6, line)

        # Save PDF
        pdf_filename = f"{selected_product}_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(pdf_filename)

        # cleanup tmp files AFTER output (avoids Windows file lock issues)
        for tmp in tmp_files:
            try:
                os.unlink(tmp)
            except Exception:
                pass

        with open(pdf_filename, "rb") as f:
            st.success(f"PDF généré : {pdf_filename}")
            st.download_button("Télécharger PDF", f, file_name=pdf_filename)

    except Exception as e:
        st.error(f"Erreur génération PDF : {e}")
        # attempt cleanup
        for tmp in tmp_files:
            try:
                os.unlink(tmp)
            except Exception:
                pass

st.markdown("---")
st.caption("Dashboard généré localement. Pour déployer en production, configure une instance Azure/GCP/AWS et sécurise la clé Azure OpenAI.")
