import streamlit as st
import pandas as pd

# Ladataan Sodankylän data
@st.cache_data
def load_data():
    return pd.read_csv(
        "https://pxweb2.stat.fi/PxWeb/sq/2f8e62ab-a65a-43d9-902d-0d235a9b65bf",
        sep=" ",
        quotechar='"'
    )
# Chat-GPT vinkkasi yllä olevan muodon, kun pandas ei ensin tunnistanut sarakkeita oikein
# Ilmeisesti olin ladannut Sodankylän datan vahingossa space separated

df = load_data()

# Ladataan Inarin data
@st.cache_data
def load_inari_data():
    return pd.read_csv(
        "https://pxweb2.stat.fi/PxWeb/sq/00ecd13f-33d8-4fb2-baea-1d251cef6697",
        sep=",",
        quotechar='"'
    )

inari_df = load_inari_data()


st.markdown("# Hotel stats of Sodankylä and Inari 2021-2025")



# Kuukaudet nätimpään muotoon. Tekoäly muistutti syntaksista.
df["Month"] = pd.to_datetime(
        df["Month"],
        format="%YM%m",
        errors="coerce"
    )

# Rajataan data pakottamalla vuosille 2021-2025, koska useasta yrityksestä huolimatta dataan tuli ladatessa 
# mukaan kuukausia ennen ja jälkeen haluttujen vuosien. Syy jäi mysteeriksi.
df = df[df["Month"].dt.year.between(2021, 2025)]


st.markdown("### Sodankylä hotel nights 2021-2025")

st.dataframe(df)



# Muutin datan numeeriseksi, koska muuten numerot näkyivät diagrammissa väärin
df["Sodankylä Nights spent"] = pd.to_numeric(
    df["Sodankylä Nights spent"],
    errors="coerce"
)

# Pelkät vuoden 2025 kuukaudet
df_2025 = df[df["Month"].dt.year == 2025]

st.markdown("### Sodankylä hotel nights 2025 by month (no data for May)")


st.line_chart(
        df_2025,
        x="Month",
        y="Sodankylä Nights spent"
    )


# Vuosittaiset yöpymismäärät
yearly_totals = (
    df.groupby(df["Month"].dt.year)["Sodankylä Nights spent"]
    .sum(min_count=1)
    .reset_index()
)

yearly_totals.columns = ["Year", "Nights spent"]

st.markdown("### Yearly hotel nights in Sodankylä")

st.bar_chart(
    yearly_totals,
    x="Year",
    y="Nights spent"
)



# Kotimaiset vs. ulkomaiset yöpymiset

st.markdown("### Domestic vs Foreign hotel nights")

# Sarakkeet taas numeerisiksi
df["Sodankylä Domestic nights"] = pd.to_numeric(
    df["Sodankylä Domestic nights"],
    errors="coerce"
)

df["Sodankylä Foreign nights"] = pd.to_numeric(
    df["Sodankylä Foreign nights"],
    errors="coerce"
)

# Teen varmuuden vuoksi oman taulukkonsa
display_df = df[[
    "Month",
    "Sodankylä Domestic nights",
    "Sodankylä Foreign nights"
]]

display_df["Month"] = display_df["Month"].dt.strftime("%Y-%m")

st.dataframe(display_df)


# Viivakaavio
st.line_chart(
    df,
    x="Month",
    y=[
        "Sodankylä Domestic nights",
        "Sodankylä Foreign nights"
    ]
)



# Sodankylä vs. Inari

st.markdown("### Hotel nights: Sodankylä vs Inari 2021-2025")

# Inarin kuukaudet päivämääriksi
inari_df["Month"] = pd.to_datetime(
    inari_df["Month"],
    format="%YM%m",
    errors="coerce"
)

# Rajaan myös Inarin datan halutuille vuosille
inari_df = inari_df[inari_df["Month"].dt.year.between(2021, 2025)]


# Inarin yöpymiset numeroiksi
inari_df["Inari Nights spent"] = pd.to_numeric(
    inari_df["Inari Nights spent"],
    errors="coerce"
)

# Yhdistetään molempien kuntien tiedot kuukauden perusteella
comparison = pd.merge(
    df[["Month", "Sodankylä Nights spent"]],
    inari_df[["Month", "Inari Nights spent"]],
    on="Month",
    how="inner"
)

# Otetaan mukaan vuodet 2021-2025
comparison = comparison[
    comparison["Month"].dt.year.between(2021, 2025)
]

# Piirretään molemmat samaan diagrammiin
st.line_chart(
    comparison,
    x="Month",
    y=[
        "Sodankylä Nights spent",
        "Inari Nights spent"
    ]
)


# Download-nappi Sodankylä vs. Inari -vertailudatalle

@st.cache_data
def convert_for_download(data):
    return data.to_csv().encode("utf-8")

csv = convert_for_download(comparison)

st.download_button(
    label="Download Sodankylä vs. Inari CSV",
    data=csv,
    file_name="sodankyla_vs_inari.csv",
    mime="text/csv",
    icon=":material/download:",
)

# Lataa vähän hassun näköistä dataa (ylimääräisen indeksin, ja toisen luvuista desimaalilla), mutta koska
# teknisesti toimii eikä anna virheellistä dataa, en ryhdy muotoa enää siivoamaan