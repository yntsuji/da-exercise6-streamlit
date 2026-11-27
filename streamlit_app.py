import streamlit as st
import pandas as pd


# Chat-GPT vinkkasi tällaisen muodon, kun pandas ei ensin tunnistanut sarakkeita oikein
df = pd.read_csv(
    "https://pxweb2.stat.fi/PxWeb/sq/2f8e62ab-a65a-43d9-902d-0d235a9b65bf",
    sep=" ",
    quotechar='"'
)

st.markdown("# Hotel stats of Sodankylä and Inari")



st.dataframe(df)

# Kuukaudet nätimpään muotoon. Tekoäly muistutti syntaksista.
df["Month"] = pd.to_datetime(
        df["Month"],
        format="%YM%m",
        errors="coerce"
    )

# Muutin datan numeeriseksi, koska muuten numerot näkyivät diagrammissa väärin
df["Sodankylä Nights spent"] = pd.to_numeric(
    df["Sodankylä Nights spent"],
    errors="coerce"
)

# Pelkät vuoden 2025 kuukaudet
df_2025 = df[df["Month"].dt.year == 2025]

st.markdown("### Sodankylä hotel nights 2025 (no data for May)")


st.line_chart(
        df_2025,
        x="Month",
        y="Sodankylä Nights spent"
    )


