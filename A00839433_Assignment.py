import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

df = pd.read_csv("Death by Age Data.csv")
df = df.drop(columns=['Country_code', 'Who_region'])
df = df.dropna()

st.title("Dashboard for the analysis of Covid's impact on different countries")

countries_selected = st.multiselect("Select countries:", sorted(df["Country"].unique()))
num_countries = max(len(countries_selected),1)
filtered_df = df[df["Country"].isin(countries_selected)]


fig, ax = plt.subplots(figsize=(8, num_countries * 0.5))
ax.barh(df["Country"], df["Deaths"])

st.pyplot(fig)