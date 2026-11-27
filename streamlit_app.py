import streamlit as st
import pandas as pd

df = pd.read_csv("https://pxweb2.stat.fi/PxWeb/sq/2f8e62ab-a65a-43d9-902d-0d235a9b65bf")


st.dataframe(df)