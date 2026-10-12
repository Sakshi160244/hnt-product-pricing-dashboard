
import os
import base64
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# HNT Product Pricing Dashboard
st.set_page_config(
    page_title="HNT | Product Pricing Dashboard",
    page_icon="🥨",
    layout="wide",
    initial_sidebar_state="expanded",
)

BG = "#241D19"
PANEL = "#302621"
PANEL_2 = "#1D1713"
GOLD = "#D9A441"
GOLD_LIGHT = "#F2C66D"
CREAM = "#FFF4E6"
MUTED = "#BDB0A4"
BORDER = "#6B5541"
GREEN = "#6BB36A"

# Background image
_bg_path = Path(__file__).parent / "assets" / "hnt_background.png"

if _bg_path.exists():
    _bg_b64 = base64.b64encode(_bg_path.read_bytes()).decode("ascii")
    BACKGROUND_DATA_URI = f"data:image/png;base64,{_bg_b64}"
else:
    BACKGROUND_DATA_URI = ""

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background:
          linear-gradient(rgba(36,29,25,.82), rgba(29,23,19,.88)),
          url("{BACKGROUND_DATA_URI}") center / cover fixed no-repeat,
          radial-gradient(ellipse at top left, #39281b 0%, {BG} 38%, #17110e 100%);
        color: {CREAM};
    }}

    [data-testid="stHeader"] {{ background: rgba(0,0,0,0); }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #17110e 0%, {PANEL} 100%);
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] * {{ color: {CREAM}; }}
    h1, h2, h3 {{ color: {CREAM} !important; }}
    p, label, .stMarkdown {{ color: {CREAM}; }}

    [data-testid="stMetric"] {{
        background: linear-gradient(135deg, {PANEL} 0%, {PANEL_2} 100%);
        border: 1px solid {GOLD};
        padding: 18px 20px;
        border-radius: 13px;
        box-shadow: 0 5px 18px rgba(0,0,0,.18);
    }}

    [data-testid="stMetricLabel"] {{
        color: {GOLD} !important;
        font-weight: 600;
    }}

    [data-testid="stMetricValue"] {{ color: {CREAM} !important; }}
    [data-testid="stMetricDelta"] {{ color: {GREEN} !important; }}

    div[data-testid="stDataFrame"], div[data-testid="stTable"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
        overflow: hidden;
    }}

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {{
        background-color: {PANEL} !important;
        color: {CREAM} !important;
        border-color: {BORDER} !important;
    }}

    input, textarea {{ color: {CREAM} !important; }}

    .section-title {{
        color: {GOLD};
        font-size: 1.05rem;
        font-weight: 700;
        padding-bottom: .45rem;
        border-bottom: 1px solid {BORDER};
        margin: .4rem 0 .8rem 0;
    }}

    .brand {{
        padding: 12px 0 18px 0;
        border-bottom: 1px solid {BORDER};
        margin-bottom: 18px;
    }}

    .brand-mark {{
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: 2px;
        color: {GOLD};
        line-height: 1.0;
    }}

    .brand-sub {{ color: {MUTED}; font-size: .8rem; margin-top: 5px; }}
    .hero-kicker {{ color: {GOLD}; text-transform: uppercase; letter-spacing: 2px; font-size: .75rem; font-weight: 700; }}
    .hero-title {{ color: {CREAM}; font-size: 2rem; font-weight: 700; margin: 0; }}
    .hero-sub {{ color: {MUTED}; margin-top: 2px; margin-bottom: 18px; }}

    .stButton > button {{
        background: linear-gradient(135deg, {GOLD_LIGHT}, {GOLD});
        color: #241D19;
        border: 1px solid {GOLD};
        border-radius: 8px;
        font-weight: 700;
        min-height: 2.5rem;
    }}

    .stButton > button:hover {{
        background: #E7B858;
        color: #241D19;
        border-color: #E7B858;
    }}

    a {{ color: {GOLD_LIGHT} !important; }}
    [data-testid="stTabs"] button {{ color: {CREAM}; }}

    [data-testid="stTabs"] button[aria-selected="true"] {{
        color: {GOLD} !important;
        border-bottom-color: {GOLD} !important;
    }}

    hr {{ border-color: {BORDER}; }}
    .small-note {{ color: {MUTED}; font-size: .82rem; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Map common source column names to expected names."""
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    aliases = {
        "image_url": "Image_URL",
        "image url": "Image_URL",
        "product_name": "Product_Name",
        "product name": "Product_Name",
        "product": "Product_Name",
        "category": "Category",
        "original_price": "Original_Price",
        "original price": "Original_Price",
        "original (₹)": "Original_Price",
        "price": "Price",
        "current (₹)": "Price",
        "discount_percent": "Discount_Percent",
        "discount percent": "Discount_Percent",
        "discount": "Discount_Percent",
        "product_url": "Product_URL",
        "product url": "Product_URL",
        "view": "Product_URL",
    }

    rename = {}
    for c in df.columns:
        key = c.strip().lower()
        if key in aliases:
            rename[c] = aliases[key]

    return df.rename(columns=rename)


def demo_data() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "Image_URL": "",
            "Product_Name": "Hindustan Next Taste Tutti Frutti Cookies",
            "Category": "Cookies & Biscuits",
            "Original_Price": 79,
            "Price": 69,
            "Discount_Percent": 12.7,
            "Product_URL": "",
        },
        {
            "Image_URL": "",
            "Product_Name": "Bombay Mixture Namkeen - HNT",
            "Category": "Namkeen",
            "Original_Price": 149,
            "Price": 109,
            "Discount_Percent": 26.8,
            "Product_URL": "",
        },
        {
            "Image_URL": "",
            "Product_Name": "Crispy Traditional Dal Sev Namkeen",
            "Category": "Namkeen",
            "Original_Price": 129,
            "Price": 109,
            "Discount_Percent": 15.5,
            "Product_URL": "",
        },
        {
            "Image_URL": "",
            "Product_Name": "HNT Ajwain Fan",
            "Category": "Fan",
            "Original_Price": 89,
            "Price": 69,
            "Discount_Percent": 22.5,
            "Product_URL": "",
        },
        {
            "Image_URL": "",
            "Product_Name": "HNT Desi Ghee Atta Biscuits",
            "Category": "Cookies & Biscuits",
            "Original_Price": 139,
            "Price": 119,
            "Discount_Percent": 14.4,
            "Product_URL": "",
        },
        {
            "Image_URL": "",
            "Product_Name": "HNT Family Snack Combo Pack",
            "Category": "Namkeen",
            "Original_Price": 197,
            "Price": 179,
            "Discount_Percent": 9.1,
            "Product_URL": "",
        },
        {
            "Image_URL": "",
            "Product_Name": "HNT Dal Biji Namkeen",
            "Category": "Namkeen",
            "Original_Price": 129,
            "Price": 109,
            "Discount_Percent": 15.5,
            "Product_URL": "",
        },
        {
            "Image_URL": "",
            "Product_Name": "HNT Classic Dry Fruit Cookies",
            "Category": "Cookies & Biscuits",
            "Original_Price": 99,
            "Price": 79,
            "Discount_Percent": 20.2,
            "Product_URL": "",
        },
    ])


def load_data() -> tuple[pd.DataFrame, str]:
    uploaded = st.sidebar.file_uploader(
        "Upload product data (Excel/CSV)",
        type=["xlsx", "xls", "csv"],
        help="Required: Product_Name, Category, Original_Price, Price. "
             "Image_URL, Discount_Percent and Product_URL are optional.",
    )

    if uploaded is not None:
        try:
            if uploaded.name.lower().endswith(".csv"):
                return normalize_columns(pd.read_csv(uploaded)), f"Uploaded: {uploaded.name}"

            return normalize_columns(pd.read_excel(uploaded)), f"Uploaded: {uploaded.name}"

        except Exception as exc:
            st.sidebar.error(f"Could not read file: {exc}")

    for candidate in (
        "products.xlsx",
        "products.csv",
        "Shop_Products.xlsx",
        "Shop_Products.csv",
    ):
        if Path(candidate).exists():
            try:
                if candidate.lower().endswith(".csv"):
                    return normalize_columns(pd.read_csv(candidate)), f"Loaded local file: {candidate}"

                return normalize_columns(pd.read_excel(candidate)), f"Loaded local file: {candidate}"

            except Exception:
                pass

    return demo_data(), "Demo data (upload your real product file to replace it)"


def ensure_schema(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)

    defaults = {
        "Image_URL": "",
        "Product_Name": "Unnamed product",
        "Category": "Uncategorized",
        "Original_Price": 0,
        "Price": 0,
        "Discount_Percent": None,
        "Product_URL": "",
    }

    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default

    for col in ["Original_Price", "Price", "Discount_Percent"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r"[^0-9.\-]", "", regex=True),
            errors="coerce",
        )

    calculated = (
        (df["Original_Price"] - df["Price"])
        / df["Original_Price"].replace(0, pd.NA) * 100
    )

    df["Discount_Percent"] = (
        df["Discount_Percent"].fillna(calculated).fillna(0)
    )
    df["Product_Name"] = df["Product_Name"].fillna("Unnamed product").astype(str)
    df["Category"] = df["Category"].fillna("Uncategorized").astype(str)
    df["Image_URL"] = df["Image_URL"].fillna("").astype(str)
    df["Product_URL"] = df["Product_URL"].fillna("").astype(str)

    return df


def money(v):
    try:
        return f"₹{float(v):,.2f}" if pd.notna(v) else "—"
    except Exception:
        return "—"


def chart_theme(fig, height=320):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=CREAM, family="DM Sans"),
        margin=dict(l=10, r=10, t=35, b=10),
        legend=dict(font=dict(color=CREAM)),
    )
    fig.update_xaxes(gridcolor="#45362B", zerolinecolor=BORDER, linecolor=BORDER)
    fig.update_yaxes(gridcolor="#45362B", zerolinecolor=BORDER, linecolor=BORDER)
    return fig


st.sidebar.markdown(
    f"""
    <div class="brand">
      <div class="brand-mark">✦ HNT</div>
      <div style="color:{GOLD};font-size:.75rem;font-style:italic;">
        Tasty Products • Better Living
      </div>
      <div class="brand-sub">Hindustan Next Taste</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Choose page",
    ["Overview", "Pricing & Discounts", "Product Explorer"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")

raw, data_source = load_data()
df = ensure_schema(raw)
st.sidebar.caption(data_source)

if df.empty:
    st.warning("No product rows found. Upload your product Excel/CSV file in the sidebar.")
    st.stop()

categories = sorted(df["Category"].dropna().astype(str).unique().tolist())

min_price = float(df["Price"].min()) if df["Price"].notna().any() else 0.0
max_price = float(df["Price"].max()) if df["Price"].notna().any() else 1000.0

if min_price == max_price:
    max_price = min_price + 1

if st.sidebar.button("↺ Reset Filters", use_container_width=True):
    st.session_state["category_filter"] = categories.copy()
    st.session_state["price_filter"] = (min_price, max_price)
    st.session_state["search_filter"] = ""
    st.rerun()

with st.sidebar.expander("Filters", expanded=True):
    selected_categories = st.multiselect(
        "Category",
        categories,
        default=categories,
        key="category_filter",
    )

    price_range = st.slider(
        "Price Range (₹)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        key="price_filter",
    )

    search_term = st.text_input(
        "Search Products",
        placeholder="Search product name...",
        key="search_filter",
    )

filtered = df[
    df["Category"].isin(selected_categories)
    & df["Price"].between(
        price_range[0], price_range[1], inclusive="both"
    )
    & df["Product_Name"].str.contains(
        search_term, case=False, na=False
    )
].copy()

st.markdown(
    f"""
    <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
      <div>
        <div class="hero-kicker">HNT • Product Intelligence</div>
        <div class="hero-title">HINDUSTAN NEXT TASTE</div>
        <div class="hero-sub">Product Pricing Dashboard</div>
      </div>
      <div style="color:{GOLD};font-family:Georgia,serif;font-style:italic;font-size:1.25rem;text-align:right;">
        Good Food<br/>Good Mood
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")


def render_metrics(data):
    c1, c2, c3, c4 = st.columns(4)

    total_products = len(data)
    total_categories = data["Category"].nunique() if not data.empty else 0
    avg_price = data["Price"].mean() if not data.empty else 0
    avg_discount = data["Discount_Percent"].mean() if not data.empty else 0

    c1.metric("Total Products", f"{total_products:,}")
    c2.metric("Total Categories", f"{total_categories:,}")
    c3.metric("Average Price", money(avg_price))
    c4.metric("Average Discount", f"{avg_discount:.1f}%")


def product_table(data, limit=None):
    view = data.copy()

    if limit:
        view = view.head(limit)

    display = pd.DataFrame({
        "Image": view["Image_URL"],
        "Product": view["Product_Name"],
        "Category": view["Category"],
        "Original (₹)": view["Original_Price"].map(money),
        "Current (₹)": view["Price"].map(money),
        "Discount": view["Discount_Percent"].map(lambda x: f"{x:.1f}%"),
        "View": view["Product_URL"],
    })

    column_config = {
        "Image": st.column_config.ImageColumn(
            "Image", help="Product photo", width="small"
        ),
        "Product": st.column_config.TextColumn("Product", width="large"),
        "Category": st.column_config.TextColumn("Category", width="medium"),
        "Original (₹)": st.column_config.TextColumn("Original (₹)", width="small"),
        "Current (₹)": st.column_config.TextColumn("Current (₹)", width="small"),
        "Discount": st.column_config.TextColumn("Discount", width="small"),
        "View": st.column_config.LinkColumn(
            "View", display_text="↗ Open", width="small"
        ),
    }

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config=column_config,
        height=430,
    )


if page == "Overview":
    render_metrics(filtered)

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown(
            '<div class="section-title">Top Products by Price</div>',
            unsafe_allow_html=True,
        )

        if filtered.empty:
            st.info("No products match the selected filters.")
        else:
            top = (
                filtered.nlargest(min(5, len(filtered)), "Price")
                .sort_values("Price")
            )

            fig = px.bar(
                top,
                x="Price",
                y="Product_Name",
                orientation="h",
                text="Price",
                labels={
                    "Price": "Current Price (₹)",
                    "Product_Name": "Product",
                },
            )

            fig.update_traces(
                marker_color=GOLD,
                texttemplate="₹%{x:,.0f}",
                textposition="outside",
            )

            st.plotly_chart(
                chart_theme(fig, 350),
                use_container_width=True,
            )

    with right:
        st.markdown(
            '<div class="section-title">Products by Category</div>',
            unsafe_allow_html=True,
        )

        if filtered.empty:
            st.info("No products match the selected filters.")
        else:
            cats = (
                filtered.groupby("Category", as_index=False)
                .size()
                .rename(columns={"size": "Products"})
            )

            fig = px.pie(
                cats,
                names="Category",
                values="Products",
                hole=0.58,
                color_discrete_sequence=[
                    GOLD, "#E87522", "#C84B4B",
                    "#9B4F96", "#4A90D9", "#A7B66A",
                ],
            )

            fig.update_traces(
                textposition="outside",
                textinfo="percent",
            )

            st.plotly_chart(
                chart_theme(fig, 350),
                use_container_width=True,
            )

    st.markdown(
        '<div class="section-title">Featured Products</div>',
        unsafe_allow_html=True,
    )

    product_table(filtered, limit=5)


elif page == "Pricing & Discounts":
    render_metrics(filtered)

    left, right = st.columns(2)

    with left:
        st.markdown(
            '<div class="section-title">Original vs Current Price</div>',
            unsafe_allow_html=True,
        )

        if filtered.empty:
            st.info("No products match the selected filters.")
        else:
            comp = (
                filtered.nlargest(min(10, len(filtered)), "Original_Price")
                .sort_values("Original_Price")
            )

            fig = px.bar(
                comp,
                x="Product_Name",
                y=["Original_Price", "Price"],
                barmode="group",
                labels={
                    "value": "Price (₹)",
                    "Product_Name": "Product",
                    "variable": "Price Type",
                },
                color_discrete_sequence=[GOLD, "#E87522"],
            )

            fig.update_layout(xaxis_tickangle=-30)

            st.plotly_chart(
                chart_theme(fig, 390),
                use_container_width=True,
            )

    with right:
        st.markdown(
            '<div class="section-title">Discount by Product</div>',
            unsafe_allow_html=True,
        )

        if filtered.empty:
            st.info("No products match the selected filters.")
        else:
            comp = (
                filtered.nlargest(min(10, len(filtered)), "Discount_Percent")
                .sort_values("Discount_Percent")
            )

            fig = px.bar(
                comp,
                x="Discount_Percent",
                y="Product_Name",
                orientation="h",
                labels={
                    "Discount_Percent": "Discount (%)",
                    "Product_Name": "Product",
                },
            )

            fig.update_traces(
                marker_color=GOLD,
                texttemplate="%{x:.1f}%",
                textposition="outside",
            )

            st.plotly_chart(
                chart_theme(fig, 390),
                use_container_width=True,
            )

    st.markdown(
        '<div class="section-title">Pricing & Discount Details</div>',
        unsafe_allow_html=True,
    )

    product_table(filtered)


else:  # Product Explorer
    render_metrics(filtered)

    st.markdown(
        '<div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;flex-wrap:wrap;">'
        '<div class="section-title" style="flex:1;border:0;margin-bottom:0;">Explore Products</div>'
        '<span class="small-note">Search, category and price filters are in the sidebar</span></div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.warning(
            "No products found. Try clearing the search or widening the price range."
        )
    else:
        product_table(filtered)


st.markdown("---")

st.markdown(
    f"""
    <div style="display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;color:{MUTED};font-size:.85rem;padding:.25rem 0 1rem;">
      <span>✦ Quality Ingredients</span>
      <span style="color:{GOLD}">|</span>
      <span>☆ Authentic Taste</span>
      <span style="color:{GOLD}">|</span>
      <span>♟ Trusted by Millions</span>
    </div>
    """,
    unsafe_allow_html=True,
)
