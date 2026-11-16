from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Gapminder World Explorer", page_icon="🌍", layout="wide")

@st.cache_data
def load_data():
    """Load the CSV once and cache it for fast interactions."""
    csv_path = Path(__file__).parent / "exp10_gapminder.csv"
    if not csv_path.exists():
        raise FileNotFoundError(
            "exp10_gapminder.csv was not found. Keep the CSV in the same folder as app.py."
        )
    data = pd.read_csv(csv_path)
    required = {"country", "continent", "year", "lifeExp", "pop", "gdpPercap"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"The dataset is missing required columns: {sorted(missing)}")
    data["year"] = data["year"].astype(int)
    return data


df = load_data()
continents = sorted(df["continent"].dropna().unique().tolist())
years = sorted(df["year"].dropna().unique().tolist())

st.title("🌍 Gapminder World Explorer")
st.caption("Explore how population, GDP per capita and life expectancy changed across countries from 1952 to 2007.")

# Sidebar controls
st.sidebar.header("Explore the dataset")
selected_continents = st.sidebar.multiselect(
    "Continent", options=continents, default=continents,
    help="Select one or more continents. Clear all to show an empty selection."
)
selected_year = st.sidebar.select_slider(
    "Year", options=years, value=years[-1],
    help="The selected year controls the KPIs, bubble chart, ranking and table."
)
country_search = st.sidebar.text_input("Search country", placeholder="e.g. India")

# Current-year rows for all components that use a year snapshot
snapshot = df[(df["year"] == selected_year) & (df["continent"].isin(selected_continents))].copy()
if country_search.strip():
    snapshot = snapshot[snapshot["country"].str.contains(country_search.strip(), case=False, na=False)]

# KPI cards
st.subheader(f"Key indicators — {selected_year}")
k1, k2, k3, k4 = st.columns(4)
if snapshot.empty:
    k1.metric("Countries", "0")
    k2.metric("Average life expectancy", "—")
    k3.metric("Total population", "—")
    k4.metric("Median GDP per capita", "—")
    st.info("No countries match the current filters. Select at least one continent or clear the country search.")
else:
    k1.metric("Countries", f"{snapshot['country'].nunique():,}")
    k2.metric("Average life expectancy", f"{snapshot['lifeExp'].mean():.1f} years")
    k3.metric("Total population", f"{snapshot['pop'].sum():,.0f}")
    k4.metric("Median GDP per capita", f"${snapshot['gdpPercap'].median():,.0f}")

# Bubble chart
st.subheader("GDP per capita vs life expectancy")
if not snapshot.empty:
    bubble = px.scatter(
        snapshot, x="gdpPercap", y="lifeExp", size="pop", color="continent",
        hover_name="country", size_max=55, log_x=True,
        labels={"gdpPercap": "GDP per capita (US$, log scale)",
                "lifeExp": "Life expectancy (years)", "pop": "Population"},
        title=f"Country comparison in {selected_year}"
    )
    bubble.update_layout(legend_title_text="Continent", margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(bubble, use_container_width=True)
else:
    st.caption("The bubble chart will appear when the current filters return rows.")

# Trend lines respond to the continent and search filters. The selected year is marked on the chart.
st.subheader("Country trends over time")
trend_pool = df[df["continent"].isin(selected_continents)].copy()
if country_search.strip():
    trend_pool = trend_pool[trend_pool["country"].str.contains(country_search.strip(), case=False, na=False)]
trend_options = sorted(trend_pool["country"].unique().tolist())
default_trends = [c for c in ["India", "China"] if c in trend_options]
trend_countries = st.multiselect(
    "Choose countries", options=trend_options, default=default_trends,
    help="The country list follows the selected continents and country search."
)
trend_metric = st.selectbox(
    "Metric", options=["lifeExp", "gdpPercap", "pop"],
    format_func=lambda x: {"lifeExp": "Life expectancy", "gdpPercap": "GDP per capita", "pop": "Population"}[x]
)
if trend_countries:
    trend_df = trend_pool[trend_pool["country"].isin(trend_countries)]
    trend_fig = px.line(
        trend_df, x="year", y=trend_metric, color="country", markers=True,
        labels={"year": "Year", "lifeExp": "Life expectancy (years)",
                "gdpPercap": "GDP per capita (US$)", "pop": "Population"},
        title="Historical trend (1952–2007)"
    )
    trend_fig.add_vline(x=selected_year, line_dash="dash", annotation_text=f"Selected year: {selected_year}")
    trend_fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(trend_fig, use_container_width=True)
else:
    st.info("Choose at least one country to display the trend line.")

# Top-N ranking for the selected year
st.subheader("Top countries ranking")
r1, r2 = st.columns([1, 3])
with r1:
    ranking_metric = st.selectbox(
        "Rank by", options=["pop", "lifeExp", "gdpPercap"],
        format_func=lambda x: {"pop": "Population", "lifeExp": "Life expectancy", "gdpPercap": "GDP per capita"}[x]
    )
    top_n = st.slider("Top N", min_value=3, max_value=20, value=10)
if not snapshot.empty:
    ranking = snapshot.nlargest(top_n, ranking_metric).sort_values(ranking_metric)
    ranking_fig = px.bar(
        ranking, x=ranking_metric, y="country", orientation="h", color="continent",
        labels={"country": "Country", "pop": "Population", "lifeExp": "Life expectancy (years)",
                "gdpPercap": "GDP per capita (US$)"},
        title=f"Top {min(top_n, len(ranking))} countries by {ranking_metric} in {selected_year}"
    )
    ranking_fig.update_layout(margin=dict(l=10, r=10, t=55, b=10))
    st.plotly_chart(ranking_fig, use_container_width=True)

# Filtered table and CSV download
st.subheader("Filtered data")
st.write(f"Rows shown: {len(snapshot):,}")
st.dataframe(snapshot.sort_values(["continent", "country"]), use_container_width=True, hide_index=True)
csv_bytes = snapshot.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download filtered rows as CSV", data=csv_bytes,
    file_name=f"gapminder_filtered_{selected_year}.csv", mime="text/csv",
    disabled=snapshot.empty
)

st.divider()
st.caption("Dataset: Gapminder World Development Dataset. Observations are recorded every five years from 1952 to 2007.")
