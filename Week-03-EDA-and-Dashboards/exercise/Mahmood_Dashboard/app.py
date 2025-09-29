import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Population Dashboard", page_icon="📈", layout="wide")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        # Fallback to bundled sample data
        df_path = Path('data\sample_population.csv')
        df = pd.read_csv(df_path)
    # Basic cleanups
    df.columns = [c.strip() for c in df.columns]
    return df

st.title("📈 Population Dashboard")
st.write(
    "Upload your own CSV (with columns like `Country`, `Year`, `Population`) "
    "or explore the sample dataset to get started."
)

with st.sidebar:
    st.header("Controls")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    st.markdown("**Expected columns**: `Country`, `Year`, `Population`")
    st.caption("Tip: Keep column names simple; capitalization doesn’t matter.")

df = load_data(uploaded)

# Coerce dtypes
if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
if "Population" in df.columns:
    df["Population"] = pd.to_numeric(df["Population"], errors="coerce")

# Sidebar Filters (populate from data safely)
countries = sorted([c for c in df["Country"].dropna().unique().tolist()]) if "Country" in df.columns else []
year_min, year_max = (int(df["Year"].min()), int(df["Year"].max())) if "Year" in df.columns and df["Year"].notna().any() else (None, None)

with st.sidebar:
    sel_countries = st.multiselect("Select countries", countries, default=(countries[:5] if len(countries) >= 5 else countries))
    if year_min is not None:
        sel_years = st.slider("Year range", min_value=year_min, max_value=year_max, value=(year_min, year_max), step=1)
    else:
        sel_years = None

# Filter
mask = pd.Series([True] * len(df))
if sel_countries:
    mask &= df["Country"].isin(sel_countries)
if sel_years:
    y1, y2 = sel_years
    mask &= df["Year"].between(y1, y2)

fdf = df[mask].dropna(subset=["Population"])

# KPIs
col1, col2, col3 = st.columns(3)
if not fdf.empty:
    latest_year = int(fdf["Year"].max())
    latest_df = fdf[fdf["Year"] == latest_year]
    total_pop = latest_df["Population"].sum()
    n_countries = latest_df["Country"].nunique()
    avg_pop = latest_df["Population"].mean()

    col1.metric("Total Population (latest year)", f"{total_pop:,.0f}")
    col2.metric("Countries (latest year)", f"{n_countries}")
    col3.metric("Avg. Population (latest year)", f"{avg_pop:,.0f}")
else:
    col1.write("No data after filters; adjust selections.")

st.markdown("---")

# Line chart: population over time
if not fdf.empty and {"Year","Population","Country"}.issubset(fdf.columns):
    fig = px.line(fdf, x="Year", y="Population", color="Country", markers=True,
                  title="Population Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Bar chart: latest year comparison
if not fdf.empty and "Country" in fdf.columns:
    latest_year = int(fdf["Year"].max()) if "Year" in fdf.columns and fdf["Year"].notna().any() else None
    if latest_year is not None:
        latest_df = fdf[fdf["Year"] == latest_year].sort_values("Population", ascending=False)
        fig2 = px.bar(latest_df, x="Country", y="Population", title=f"Population by Country (Year {latest_year})")
        st.plotly_chart(fig2, use_container_width=True)

# Raw data
with st.expander("Preview Data"):
    st.dataframe(fdf.head(100), use_container_width=True)
