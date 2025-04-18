import streamlit as st
import pandas as pd
import psycopg2

# === DB CONFIG ===
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ml_data"
DB_USER = "user"
DB_PASSWORD = "password"

# === Connect to PostgreSQL ===
@st.cache_data
def load_data():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    df = pd.read_sql("SELECT * FROM ml_ready_data", conn)
    conn.close()
    return df

# === Streamlit App ===
st.set_page_config(page_title="ML Dashboard", layout="wide")
st.title(" ML Data Dashboard")

data = load_data()

# Preview sample data
st.write("### Sample of ML-Ready Data")
st.dataframe(data.head())

# Show total transaction value (if column exists)
if 'Value' in data.columns:
    st.write("### Total Transaction Value")
    st.metric("Total ", f"{data['Value'].sum():,.0f}")
else:
    st.warning(" 'Value' column not found — skipping total metric.")

# Top domains
if 'Domain' in data.columns:
    st.write("### Top Domains")
    top_domains = data['Domain'].value_counts().head(5)
    st.bar_chart(top_domains)
else:
    st.warning(" 'Domain' column not found — skipping domain chart.")

# Transaction count by location
if 'Location' in data.columns and 'Transaction_count' in data.columns:
    st.write("### Transaction Count by Location")
    top_locations = (
        data.groupby('Location')['Transaction_count']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_locations)
else:
    st.warning(" 'Location' or 'Transaction_count' column not found — skipping location chart.")
