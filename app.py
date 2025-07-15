import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="payGaze", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("transactions.csv")

@st.cache_data
def load_geojson():
    with open("india_states.geojson", "r") as f:
        return json.load(f)

df = load_data()
geojson = load_geojson()

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Overview",
    "📊 Transactions",
    "🗺️ Map",
    "📈 State Comparison"
])


if page == "🏠 Overview":
    st.title("📊 PayGaze: UPI Data Analytics Platform")
    st.write("A powerful interactive dashboard to explore UPI transaction trends across India.")

    st.metric("Total Transactions", df["Count"].sum())
    st.metric("Total Amount", f"₹ {int(df['Amount'].sum()):,}")

elif page == "📊 Transactions":
    st.title("💰 Transaction Analysis")
    year = st.selectbox("Select Year", sorted(df["Year"].unique()))
    quarter = st.selectbox("Select Quarter", sorted(df["Quarter"].unique()))
    trans_type = st.selectbox("Transaction Type", df["Transaction_type"].unique())

    filtered = df[(df["Year"] == year) & (df["Quarter"] == quarter) & (df["Transaction_type"] == trans_type)]

    fig = px.bar(filtered, x="State", y="Amount", color="State",
                 title=f"{trans_type} Transactions in Q{quarter}, {year}")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🗺️ Map":
    st.title("🗺️ Statewise Transaction Analysis (Choropleth)")

    # User selections
    year = st.selectbox("Select Year (Map)", sorted(df["Year"].unique()), key="map_year")
    quarter = st.selectbox("Select Quarter (Map)", sorted(df["Quarter"].unique()), key="map_quarter")
    metric = st.radio("Select Metric to Visualize", ["Amount", "Count"], horizontal=True)

    # Filter + group data
    map_df = df[(df["Year"] == year) & (df["Quarter"] == quarter)]
    map_df = map_df.groupby("State")[[metric]].sum().reset_index()

    # Fix state name mismatches
    state_mapping = {
        "Andaman And Nicobar Islands": "Andaman & Nicobar Islands",
        "Dadara And Nagar Havelli And Daman And Diu": "Dadra & Nagar Haveli & Daman & Diu",
        "Jammu And Kashmir": "Jammu & Kashmir",
        "Nct Of Delhi": "Delhi",
        "Telengana": "Telangana"
    }
    map_df["State"] = map_df["State"].replace(state_mapping)
    map_df["State"] = map_df["State"].str.strip().str.lower()

    for feature in geojson["features"]:
        feature["properties"]["NAME_1"] = feature["properties"]["NAME_1"].strip().lower()

    # Plot the map
    fig = px.choropleth(
        map_df,
        geojson=geojson,
        featureidkey="properties.NAME_1",
        locations="State",
        color=metric,
        color_continuous_scale="Reds",
        title=f"{metric} across States - Q{quarter}, {year}",
        scope="asia",
        hover_data=["State", metric]
    )
    fig.update_geos(
        fitbounds="locations",
        visible=True,
        projection_type="mercator"
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "📈 State Comparison":
    st.title("📈 Multi-State UPI Trend (Amount & Count)")
    
    st.markdown("---")
    st.subheader("📈 Compare States Over Time (Amount & Count)")

    selected_states = st.multiselect(
        "Select States to Compare",
        options=sorted(df["State"].unique()),
        default=["Maharashtra", "Karnataka"]
    )

    if selected_states:
        comparison_df = df[df["State"].isin(selected_states)]
        comparison_df = comparison_df.groupby(["State", "Year", "Quarter"])[["Amount", "Count"]].sum().reset_index()
        comparison_df["Period"] = comparison_df["Year"].astype(str) + " Q" + comparison_df["Quarter"].astype(str)

        fig_multi = px.line(
            comparison_df,
            x="Period",
            y="Amount",
            color="State",
            line_dash_sequence=["solid"],
            markers=True,
            title="💰 Amount Trend by State"
        )
        fig_multi.update_layout(xaxis_title="Period", yaxis_title="Amount (INR)")
        st.plotly_chart(fig_multi, use_container_width=True)

        fig_count = px.line(
            comparison_df,
            x="Period",
            y="Count",
            color="State",
            line_dash="State",
            markers=True,
            title="🔢 Transaction Count Trend by State"
        )
        fig_count.update_layout(xaxis_title="Period", yaxis_title="Number of Transactions")
        st.plotly_chart(fig_count, use_container_width=True)

        # Download Option (PNG)
        st.markdown("### 📥 Download Chart as Image")

selected_download_fig = st.radio("Which graph to download?", ["Amount Trend", "Count Trend"])
if selected_download_fig == "Amount Trend":
    fig_to_export = fig_multi
else:
    fig_to_export = fig_count

import plotly.io as pio
import io

try:
    img_bytes = pio.to_image(fig_to_export, format="png", engine="kaleido")
    st.download_button(
        label="📷 Download PNG",
        data=img_bytes,
        file_name=f"{selected_download_fig.replace(' ', '_')}.png",
        mime="image/png"
    )
except Exception as e:
    st.error("❌ Image export failed. You can still right-click the chart above and choose 'Save as image'.")
    st.exception(e)
