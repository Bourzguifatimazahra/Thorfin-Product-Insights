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

if 'price' in df.columns and df['price'].notna().any():
    pmin = float(np.nanmin(df['price']))
    pmax = float(np.nanmax(df['price']))
    price_range = st.sidebar.slider("Prix", min_value=round(pmin,2), max_value=round(pmax,2), value=(round(pmin,2), round(pmax,2)))
    df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

if 'rating' in df.columns and df['rating'].notna().any():
    rmin = int(np.nanmin(df['rating']))
    rmax = int(np.nanmax(df['rating']))
    rating_range = st.sidebar.slider("Note", min_value=rmin, max_value=rmax, value=(rmin, rmax))
    df = df[(df['rating'] >= rating_range[0]) & (df['rating'] <= rating_range[1])]

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
