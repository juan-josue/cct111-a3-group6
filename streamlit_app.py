"""
CCT 111 - A3
"""
# ---- IMPORT LIBS & LOAD DATASET----
import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('./Toronto Island Ferry Ticket Counts.csv')

# Convert the Timestamp column to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Using the Timestamp create new Year, Month, and Hour Columns
df["Year"] = df["Timestamp"].dt.year
df["Month"] = df["Timestamp"].dt.month
df["Hour"] = df["Timestamp"].dt.hour


# ---- INTRO SECTION ----
st.title("Toronto Island Ferry Fleet Replacement Justification ⛴️ 🌊")

st.image("./fleet-image.png", caption="Toronto Island New Ferry")

st.markdown(
    """ 
    The City of Toronto has allocated funding for constructing and delivering two :rainbow[fully electric ferries],
    with funding for additional vessels subject to approval. We are determining whether ticket sales and
    redemption trends over the past decade justify replacing the Toronto Island ferry fleet.
    """
)

st.divider()

# ---- INTRODUCING THE DATA ----
st.subheader("📊 The Data at a Glance")
st.markdown(
    """
    This dataset provides near real-time information on Toronto Island ferry ticket sales and ticket redemptions.
    This Data set is maintained by Toronto's Department of Parks, Forest, and Recreation.
    
    This will help us understand the demand trends and make data based decisions on fleet replacement.
    """
)

df[["Timestamp", "Year", "Sales Count", "Redemption Count"]]

st.divider()


# ---- SALES AND REDEMPTION BY YEAR LINE CHART ----
st.subheader("📈 Sales and Redemption Trends Over the Years")
st.markdown(
    """
    The line chart below shows the annual trends in ticket sales and redemptions. 
    - We can see that ticket sales a decade ago exceeded ticket redemption meaning that not every purchased
    ticket was redeemed.
    - Over the last decade we can observe that ticket redemption matches ticket sales implying
    that nearly all tickets sold are being used implying a ridership volume.
    - Another notable observation is that in 2020 sales and redemption dropped due to the COVID-19 pandemic,
    however in 2022 the counts returned to pre-pandemic levels.
    """
)

# Group by Year and sum Sales and Redemptions
yearly_data = df.groupby("Year")[["Sales Count", "Redemption Count"]].sum().reset_index()

# Display line chart with a title
st.line_chart(yearly_data.set_index("Year"))

st.divider()


# ---- SEASON TRENDS LINE CHART WITH YEAR SELECTION ----
st.subheader("📅 Seasonal Trends in Redemptions")
st.markdown(
    """
    This chart shows seasonal redemption trends for a selected year. We can see the ticket redemption peaks and lows,
    helping us understand seasonal variations in demand.
    """
)

# Convert available years into a range for the slider
min_year = int(df["Year"].min())  # Earliest year in dataset
max_year = int(df["Year"].max())  # Latest year in dataset

# Define a dictionary to map month numbers to names
month_map = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# Use a slider instead of a dropdown
selected_year = st.slider("Select a Year", min_year, max_year, 2016)

# Filter data for selected year
filtered_df = df[df["Year"] == selected_year]

# Group by Month and sum Redemptions
monthly_data = filtered_df.groupby("Month")[["Redemption Count"]].sum().reset_index()

# Convert Month numbers to names using the dict
monthly_data["Month"] = monthly_data["Month"].map(month_map)

# Ensure the months are in the correct order
month_order = list(month_map.values())  # ["Jan", "Feb", ..., "Dec"]
monthly_data["Month"] = pd.Categorical(monthly_data["Month"], categories=month_order, ordered=True)

# Sort by the newly defined order
monthly_data = monthly_data.sort_values("Month")

# Display the monthly data in a line chart
st.line_chart(monthly_data.set_index("Month"))

st.divider()

# ---- PEAK HOURS ----
st.subheader("🕒 Peak Hourly Redemptions")
st.markdown(
    """
    The bar chart below shows the peak hours for ferry ticket redemptions throughout the day. 
    - High redemption numbers during peak hours point to the need for more frequent ferry service or
     additional vessels to minimize wait times and improve passenger experience.
    """
)

hourly_data = df.groupby("Hour")[["Redemption Count"]].sum().reset_index()
st.bar_chart(hourly_data.set_index("Hour"))
