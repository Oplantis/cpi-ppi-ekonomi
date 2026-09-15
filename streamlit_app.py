
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="CPI-PPI-Ekonomi", page_icon="📈", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.4rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {background:#111827; border:1px solid #25324a; padding:14px; border-radius:12px;}
h1,h2,h3 {letter-spacing:-0.02em;}
.small {color:#94a3b8; font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

st.title("CPI-PPI-Ekonomi Dashboard")
st.caption("CPI • PPI • Shelter • Communication • Services • Rates • Energy • FX • Model tracking")

page = st.sidebar.radio("Monitor", [
    "Overview", "CPI", "PPI", "Shelter v0.4", "Communication",
    "Core Services", "Rates & Yield Curve", "Energy", "FX / BoJ", "Model Tracker"
])

# Placeholder history: clearly marked until official feeds/models are connected.
months = pd.date_range("2025-01-01", periods=21, freq="MS")
rng = np.random.default_rng(7)

def demo_series(base, vol=.03):
    return np.round(base + rng.normal(0, vol, len(months)).cumsum()/5, 3)

demo = pd.DataFrame({
    "Month": months,
    "CPI Headline MoM": demo_series(.25),
    "CPI Core MoM": demo_series(.27),
    "Shelter": demo_series(.32, .025),
    "Rent": demo_series(.30, .02),
    "OER": demo_series(.31, .02),
    "Communication": demo_series(-.05, .12),
    "PPI Headline MoM": demo_series(.20, .06),
}).set_index("Month")

if page == "Overview":
    st.warning("İlk sürüm: altyapı çalışıyor. Grafiklerdeki tarihsel değerler DEMO/PLACEHOLDER. Sonraki aşamada BLS/FRED ve kendi modellerimizin gerçek verileri bağlanacak.")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("CPI Nowcast", "—", "v0.3")
    c2.metric("Core CPI Nowcast", "—", "v0.3")
    c3.metric("Shelter Nowcast", "—", "v0.4")
    c4.metric("PPI Nowcast", "—", "model")
    st.subheader("Inflation monitor")
    st.line_chart(demo[["CPI Headline MoM","CPI Core MoM"]], height=300)
    a,b = st.columns(2)
    with a:
        st.subheader("Shelter components")
        st.line_chart(demo[["Shelter","Rent","OER"]], height=280)
    with b:
        st.subheader("PPI")
        st.line_chart(demo[["PPI Headline MoM"]], height=280)
    st.subheader("Monitor status")
    st.dataframe(pd.DataFrame([
        ["CPI v0.2","Benchmark","Planned"],
        ["CPI v0.3","Primary nowcast","Planned"],
        ["Shelter v0.4","Rent/OER/Lodging","Planned"],
        ["Communication","Carrier pricing overlay","Planned"],
        ["Core Services","ISM + wages overlay","Planned"],
        ["PPI","Headline/Core + pass-through","Planned"],
        ["Rates","2Y/10Y/20Y/30Y + mortgage","Planned"],
        ["Energy","Oil/gasoline transmission","Planned"],
        ["FX / BoJ","USDJPY + BoJ","Planned"],
    ], columns=["Monitor","Purpose","Live feed"]), use_container_width=True, hide_index=True)

elif page == "CPI":
    st.header("CPI Monitor")
    st.info("v0.2 benchmark + v0.3 primary model; consensus, actual and forecast error will be stored here.")
    st.line_chart(demo[["CPI Headline MoM","CPI Core MoM"]])

elif page == "PPI":
    st.header("PPI Monitor")
    st.line_chart(demo[["PPI Headline MoM"]])
    st.caption("Next: official BLS PPI series, core measures and CPI pass-through signals.")

elif page == "Shelter v0.4":
    st.header("Shelter v0.4")
    st.line_chart(demo[["Rent","OER","Shelter"]])
    st.markdown("**Planned inputs:** Rent • OER • Lodging away from home • PPI traveler accommodation • Zillow shelter signals • hotel ADR/RevPAR.")

elif page == "Communication":
    st.header("Communication / Wireless")
    st.line_chart(demo[["Communication"]])
    st.markdown("Carrier pricing events, wireless services and communication CPI will be tracked here.")

elif page == "Core Services":
    st.header("Core Services")
    st.markdown("ISM Services Prices • New Orders • Atlanta Wage Growth Tracker • controlled services overlay.")
    st.info("Live series connection is the next phase.")

elif page == "Rates & Yield Curve":
    st.header("Rates & Yield Curve")
    st.markdown("2Y • 10Y • 20Y • 30Y Treasury • 30Y mortgage • curve/stress indicators.")
    st.info("FRED/Treasury live connection is the next phase.")

elif page == "Energy":
    st.header("Energy")
    st.markdown("WTI/Brent • gasoline • energy CPI/PPI transmission • scenario analysis.")
    st.info("Live market/official data connection is the next phase.")

elif page == "FX / BoJ":
    st.header("FX / BoJ")
    st.markdown("USDJPY • DXY • BoJ policy • U.S. Treasury interaction.")
    st.info("Live data connection is the next phase.")

else:
    st.header("Model Tracker")
    st.dataframe(pd.DataFrame([
        ["CPI","v0.2","Benchmark"],
        ["CPI","v0.3","Primary"],
        ["Shelter","v0.4","Primary"],
        ["Communication","Carrier event overlay","Primary"],
    ], columns=["Model","Version","Role"]), use_container_width=True, hide_index=True)
    st.caption(f"Dashboard build: {datetime.now().strftime('%Y-%m-%d')}")
