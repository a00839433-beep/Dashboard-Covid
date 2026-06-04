import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import StrMethodFormatter

st.title("COVID Mortality Dashboard")

covid_data = pd.read_csv("Death by Age Data.csv")

covid_data = covid_data.dropna( subset=["Country", "Wb_income", "Agegroup", "Deaths"] )

covid_data["Date"] = pd.to_datetime( covid_data["Year"].astype(str) + "-" + covid_data["Month"].astype(str) + "-01")

min_date = covid_data["Date"].min()
max_date = covid_data["Date"].max()

covid_data["Deaths"] = pd.to_numeric( covid_data["Deaths"], errors="coerce")

covid_data = covid_data.dropna(subset=["Deaths"])

countries = sorted(covid_data["Country"].unique())

selected_countries = st.sidebar.multiselect("Select countries", countries, default=countries[:5])

date_range = st.sidebar.date_input("Select period", value=(min_date, max_date),min_value=min_date,max_value=max_date)

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

filtered_data = covid_data[
    (covid_data["Date"] >= start_date) &
    (covid_data["Date"] <= end_date)
]

if len(selected_countries) > 0:
    filtered_data = filtered_data[
        filtered_data["Country"].isin(selected_countries)
    ]

st.subheader("Deaths by age group")

deaths_by_age = filtered_data.groupby("Agegroup")["Deaths"].sum().reset_index()

deaths_by_age = deaths_by_age.sort_values("Deaths")

highest_deaths = deaths_by_age["Deaths"].max()

max_age = deaths_by_age[deaths_by_age["Deaths"] == highest_deaths]["Agegroup"].iloc[0]

colors = []

for age in deaths_by_age["Agegroup"]:
    if age == max_age:
        colors.append("red")
    else:
        colors.append("gray")

fig1, ax1 = plt.subplots()

ax1.barh( deaths_by_age["Agegroup"], deaths_by_age["Deaths"], color=colors)

ax1.set_xlabel("Deaths")
ax1.set_ylabel("Age Group")
ax1.set_title("Deaths by Age Group")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax1.spines["bottom"].set_visible(False)

st.pyplot(fig1)

st.subheader("Deaths by country and age group")

country_age_data = filtered_data.groupby(
    ["Country", "Agegroup"]
)["Deaths"].sum().reset_index()

chart_data = country_age_data.pivot( index="Country", columns="Agegroup", values="Deaths")

chart_data = chart_data.fillna(0)

chart_data = chart_data.head(10)

fig2, ax2 = plt.subplots()

chart_data.plot(kind="bar",stacked=True,ax=ax2)

ax2.set_xlabel("Country")
ax2.set_ylabel("Deaths")
ax2.set_title("Deaths by Country and Age Group")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

plt.xticks(rotation=0)

st.pyplot(fig2)

st.subheader("Deaths by income level")

income_level_data = filtered_data.groupby("Wb_income")["Deaths"].sum().reset_index()

fig3, ax3 = plt.subplots()

ax3.bar(income_level_data["Wb_income"], income_level_data["Deaths"])

ax3.set_xlabel("Income Level")
ax3.set_ylabel("Deaths")
ax3.set_title("Deaths by Income Level")
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["left"].set_visible(False)
ax3.spines["bottom"].set_visible(False)
ax3.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}'))

plt.xticks(rotation=0)

st.pyplot(fig3)