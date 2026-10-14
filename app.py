import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="IIP | Institution Intelligence",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
:root { --navy:#14243A; --teal:#0F8B8D; --muted:#667085; }
.block-container { padding-top: 1.35rem; padding-bottom: 2.5rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #14243A; }
[data-testid="stSidebar"] * { color: #F7FAFC !important; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #14243A !important; }
h1, h2, h3 { color: #14243A; letter-spacing: -0.02em; }
div[data-testid="stMetric"] {
  background: #FFFFFF; border: 1px solid #E5EAF1; padding: 16px 18px;
  border-radius: 12px; box-shadow: 0 2px 8px rgba(20,36,58,.035);
}
div[data-testid="stMetricLabel"] { color: #667085; }
.iip-subtitle { color:#667085; margin-top:-10px; margin-bottom:18px; }
.iip-pill { display:inline-block; padding:4px 9px; border-radius:999px;
  background:#E8F5F4; color:#0F7779; font-size:12px; font-weight:600; }
.iip-note { background:#F4F7FB; border-left:4px solid #0F8B8D; padding:12px 14px; border-radius:7px; }
hr { border-color: #E5EAF1; }
</style>
""", unsafe_allow_html=True)

# ---------- Demonstration dataset ----------
INSTITUTIONS = {
    "ABC Institute of Technology": {
        "aishe": "DEMO-0001", "city": "Hyderabad", "state": "Telangana",
        "type": "Engineering college", "ownership": "Private / Trust",
        "established": 2004, "university": "XYZ University",
        "students": 3120, "capacity": 4800, "latest_admissions": 780,
        "placement": 72, "naac": "B++ (demo)", "nirf": "Not ranked in demo dataset",
        "risk": "Review", "faculty": 186, "land": 18.5, "builtup": 94000,
        "annual_fee_lakh": 2.8,
        "admissions": [
            {"year":"2021-22","intake":1080,"admissions":540,"reported":565},
            {"year":"2022-23","intake":1080,"admissions":610,"reported":620},
            {"year":"2023-24","intake":1080,"admissions":690,"reported":710},
            {"year":"2024-25","intake":1200,"admissions":760,"reported":800},
            {"year":"2025-26","intake":1200,"admissions":780,"reported":820},
        ],
        "placements": [
            {"year":"2021","eligible":300,"placed":165,"highest":12,"average":3.8,"median":3.4},
            {"year":"2022","eligible":320,"placed":190,"highest":14,"average":4.1,"median":3.6},
            {"year":"2023","eligible":350,"placed":220,"highest":15,"average":4.4,"median":3.9},
            {"year":"2024","eligible":380,"placed":260,"highest":16,"average":4.8,"median":4.2},
            {"year":"2025","eligible":400,"placed":292,"highest":18,"average":5.2,"median":4.6},
        ],
        "courses": [
            {"course":"Computer Science","intake":360,"admissions":295},
            {"course":"AI & Machine Learning","intake":240,"admissions":205},
            {"course":"Electronics","intake":240,"admissions":150},
            {"course":"Mechanical","intake":180,"admissions":75},
            {"course":"Civil","intake":180,"admissions":55},
        ],
    },
    "Northstar College of Management": {
        "aishe": "DEMO-0002", "city": "Warangal", "state": "Telangana",
        "type": "Management college", "ownership": "Private / Society",
        "established": 2012, "university": "Northstar State University",
        "students": 1480, "capacity": 2100, "latest_admissions": 310,
        "placement": 66, "naac": "Not verified", "nirf": "Unavailable",
        "risk": "Attention", "faculty": 74, "land": 7.2, "builtup": 36500,
        "annual_fee_lakh": 1.6,
        "admissions": [
            {"year":"2021-22","intake":500,"admissions":390,"reported":405},
            {"year":"2022-23","intake":500,"admissions":370,"reported":380},
            {"year":"2023-24","intake":500,"admissions":350,"reported":365},
            {"year":"2024-25","intake":500,"admissions":330,"reported":355},
            {"year":"2025-26","intake":500,"admissions":310,"reported":335},
        ],
        "placements": [
            {"year":"2021","eligible":210,"placed":150,"highest":8,"average":3.5,"median":3.1},
            {"year":"2022","eligible":220,"placed":155,"highest":9,"average":3.6,"median":3.2},
            {"year":"2023","eligible":225,"placed":153,"highest":10,"average":3.7,"median":3.3},
            {"year":"2024","eligible":230,"placed":150,"highest":11,"average":3.8,"median":3.4},
            {"year":"2025","eligible":240,"placed":158,"highest":12,"average":4.0,"median":3.5},
        ],
        "courses": [
            {"course":"MBA","intake":240,"admissions":155},
            {"course":"MCA","intake":120,"admissions":82},
            {"course":"Business Analytics","intake":80,"admissions":43},
            {"course":"Executive Management","intake":60,"admissions":30},
        ],
    },
    "Riverbend University": {
        "aishe": "DEMO-0003", "city": "Nizamabad", "state": "Telangana",
        "type": "University", "ownership": "Private",
        "established": 2010, "university": "Riverbend University",
        "students": 4200, "capacity": 6000, "latest_admissions": 960,
        "placement": 78, "naac": "A (demo)", "nirf": "Category data unavailable",
        "risk": "Review", "faculty": 245, "land": 42, "builtup": 155000,
        "annual_fee_lakh": 2.1,
        "admissions": [
            {"year":"2021-22","intake":1400,"admissions":780,"reported":800},
            {"year":"2022-23","intake":1400,"admissions":820,"reported":835},
            {"year":"2023-24","intake":1500,"admissions":900,"reported":925},
            {"year":"2024-25","intake":1500,"admissions":930,"reported":945},
            {"year":"2025-26","intake":1600,"admissions":960,"reported":980},
        ],
        "placements": [
            {"year":"2021","eligible":500,"placed":340,"highest":16,"average":4.6,"median":4.0},
            {"year":"2022","eligible":520,"placed":365,"highest":18,"average":4.9,"median":4.3},
            {"year":"2023","eligible":540,"placed":390,"highest":20,"average":5.1,"median":4.5},
            {"year":"2024","eligible":560,"placed":410,"highest":22,"average":5.4,"median":4.8},
            {"year":"2025","eligible":580,"placed":452,"highest":24,"average":5.8,"median":5.0},
        ],
        "courses": [
            {"course":"Engineering","intake":650,"admissions":420},
            {"course":"Management","intake":300,"admissions":220},
            {"course":"Sciences","intake":350,"admissions":180},
            {"course":"Pharmacy","intake":300,"admissions":140},
            {"course":"Arts & Humanities","intake":0,"admissions":0},
        ],
    },
}

PAGES = [
    "Executive Overview", "Admission Intelligence", "Placement Intelligence",
    "Rankings & Accreditation", "Promoter Due Diligence", "Campus Performance",
    "Commercial Intelligence", "Risk & Red Flags", "Sources & Verification"
]

def pct(n, d):
    return (n / d * 100) if d else 0

def money_lakh(value):
    return f"₹{value:,.1f}L"

def source_status(source):
    return {
        "Demonstration dataset": "Demonstration",
        "Institution website": "Self-reported",
        "University portal": "Requires validation",
        "Government dataset": "Requires validation",
        "Internal assessment": "Internal",
    }.get(source, "Unavailable")

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ◈ IIP")
    st.caption("INSTITUTION INTELLIGENCE")
    st.markdown("---")
    page = st.radio("WORKSPACE", PAGES, index=0, label_visibility="visible")
    st.markdown("---")
    st.caption("DEMO WORKSPACE")
    st.caption("All institution names and figures in this starter app are fictional demonstration data.")
    st.markdown("Version 0.1 • Prototype")

st.title("Institution Intelligence Platform")
st.markdown('<p class="iip-subtitle">One Search. One Profile. One Executive View.</p>', unsafe_allow_html=True)

# Search is available on all pages
col_search, col_hint = st.columns([2, 1])
with col_search:
    institution_name = st.selectbox(
        "Search institution",
        list(INSTITUTIONS.keys()),
        index=0,
        help="Search is currently connected to the included fictional demonstration dataset."
    )
with col_hint:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="iip-pill">DEMONSTRATION DATA</span>', unsafe_allow_html=True)

inst = INSTITUTIONS[institution_name]
admissions_df = pd.DataFrame(inst["admissions"])
placements_df = pd.DataFrame(inst["placements"])
courses_df = pd.DataFrame(inst["courses"])
admissions_df["utilisation"] = admissions_df.apply(lambda r: pct(r["admissions"], r["intake"]), axis=1)
placements_df["placement_rate"] = placements_df.apply(lambda r: pct(r["placed"], r["eligible"]), axis=1)
current_util = pct(inst["students"], inst["capacity"])
latest = admissions_df.iloc[-1]
avg_util = admissions_df["utilisation"].mean()
admission_growth = pct(latest["admissions"] - admissions_df.iloc[0]["admissions"], admissions_df.iloc[0]["admissions"])
admission_gap = int(latest["reported"] - latest["admissions"])
gap_pct = pct(admission_gap, latest["reported"]) if latest["reported"] else 0

def profile_header():
    st.subheader(inst["name"] if "name" in inst else institution_name)
    st.caption(f'{inst["type"]}  •  {inst["city"]}, {inst["state"]}  •  Established {inst["established"]}')
    st.write(f'**Ownership:** {inst["ownership"]}  ·  **Affiliated university:** {inst["university"]}  ·  **AISHE:** {inst["aishe"]}')
    st.info("Demonstration data only. These figures do not describe or verify a real institution.")

def chart_layout(fig, height=320):
    fig.update_layout(
        height=height, margin=dict(l=8, r=8, t=35, b=8),
        paper_bgcolor="white", plot_bgcolor="white",
        font=dict(family="Arial", color="#344054"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EEF2F6")
    st.plotly_chart(fig, use_container_width=True)

def show_sources():
    sources = pd.DataFrame([
        {"Metric":"Institution profile","Source":"Demonstration dataset","Checked":str(date.today()),"Status":"Demonstration","Evidence":"Fictional sample record"},
        {"Metric":"Admissions","Source":"Demonstration dataset","Checked":str(date.today()),"Status":"Demonstration","Evidence":"Fictional five-year values"},
        {"Metric":"Placement","Source":"Demonstration dataset","Checked":str(date.today()),"Status":"Demonstration","Evidence":"Fictional placement values"},
        {"Metric":"Accreditation","Source":"Demonstration dataset","Checked":str(date.today()),"Status":"Demonstration","Evidence":"Not an official verification"},
        {"Metric":"Commercial assumptions","Source":"Internal assessment","Checked":str(date.today()),"Status":"Illustrative","Evidence":"Scenario assumptions only"},
    ])
    st.dataframe(sources, use_container_width=True, hide_index=True)
    st.download_button("Download source register (CSV)", sources.to_csv(index=False).encode("utf-8"), file_name="iip_source_register_demo.csv", mime="text/csv")

# ---------- Pages ----------
if page == "Executive Overview":
    profile_header()
    st.markdown("### Executive snapshot")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Student capacity", f'{inst["capacity"]:,}')
    c2.metric("Current students", f'{inst["students"]:,}')
    c3.metric("Latest admissions", f'{inst["latest_admissions"]:,}')
    c4.metric("Capacity utilisation", f"{current_util:.1f}%")
    c5.metric("Placement rate", f'{inst["placement"]}%*')
    c6.metric("Overall risk", inst["risk"])
    st.caption("*Placement figure is illustrative and not independently verified.")
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown("### Five-year admission trend")
        fig = px.line(admissions_df, x="year", y="utilisation", markers=True, labels={"year":"Academic year","utilisation":"Utilisation (%)"})
        fig.update_traces(line_color="#0F8B8D", line_width=3, marker_size=8)
        chart_layout(fig)
    with right:
        st.markdown("### Regulatory overview")
        reg = pd.DataFrame([
            ["UGC recognition","Not verified"],["AICTE approval","Not verified"],
            ["NAAC",inst["naac"]],["University affiliation","Requires validation"],
            ["NBA accreditation","Unavailable"],["NIRF",inst["nirf"]],
        ], columns=["Area","Status"])
        st.dataframe(reg, use_container_width=True, hide_index=True)
    a,b,c = st.columns(3)
    with a:
        st.markdown("### Admission momentum")
        st.metric("5-year average utilisation", f"{avg_util:.1f}%")
        st.metric("Admissions change over period", f"{admission_growth:+.1f}%")
    with b:
        st.markdown("### Commercial snapshot")
        st.metric("Available capacity", f'{max(inst["capacity"]-inst["students"],0):,}')
        st.metric("Annual fee assumption", money_lakh(inst["annual_fee_lakh"]))
    with c:
        st.markdown("### Items to review")
        st.warning("Regulatory status requires source validation.")
        st.warning("Placement figures are illustrative.")
    st.markdown("### Executive assessment")
    st.markdown('<div class="iip-note">Prototype assessment: use the underlying records and verification status before making any partnership decision. No automated overall quality score is assigned.</div>', unsafe_allow_html=True)
    st.markdown("### Quick actions")
    q1,q2,q3 = st.columns(3)
    with q1:
        if st.button("Review admissions", use_container_width=True): st.session_state["jump_page"] = "Admission Intelligence"
    with q2:
        if st.button("Review risk register", use_container_width=True): st.session_state["jump_page"] = "Risk & Red Flags"
    with q3:
        if st.button("Review sources", use_container_width=True): st.session_state["jump_page"] = "Sources & Verification"
    if st.session_state.get("jump_page"):
        st.info(f'Use the sidebar to open: {st.session_state["jump_page"]}')

elif page == "Admission Intelligence":
    st.subheader("Admission Intelligence")
    st.caption("Five-year admission performance and intake utilisation.")
    f1,f2 = st.columns(2)
    with f1:
        selected_years = st.multiselect("Academic years", admissions_df["year"].tolist(), default=admissions_df["year"].tolist())
    with f2:
        metric_choice = st.selectbox("Trend metric", ["Utilisation (%)","Admissions","Approved intake"])
    view = admissions_df[admissions_df["year"].isin(selected_years)].copy()
    if metric_choice == "Utilisation (%)":
        fig = px.line(view, x="year", y="utilisation", markers=True, labels={"year":"Academic year","utilisation":"Utilisation (%)"})
    else:
        ycol = "admissions" if metric_choice == "Admissions" else "intake"
        fig = px.bar(view, x="year", y=ycol, labels={"year":"Academic year",ycol:metric_choice})
    chart_layout(fig)
    st.metric("5-year average utilisation", f'{avg_util:.1f}%')
    st.metric("Admissions change from first to latest year", f"{admission_growth:+.1f}%")
    show_gap = st.toggle("Show institution-reported vs demo-verified comparison", value=True)
    if show_gap:
        admissions_df["gap"] = admissions_df["reported"] - admissions_df["admissions"]
        admissions_df["gap_pct_of_reported"] = admissions_df.apply(lambda r: pct(r["gap"],r["reported"]) if r["reported"] else 0,axis=1)
        st.dataframe(admissions_df.rename(columns={"year":"Academic year","intake":"Approved intake (demo)","admissions":"University-registered admissions (demo)","reported":"Institution-reported admissions (demo)","utilisation":"Utilisation (%)","gap":"Difference","gap_pct_of_reported":"Difference (% of reported)"}).round(1), use_container_width=True, hide_index=True)
        st.caption("The 'university-registered' label above is a demonstration field only, not a real university verification.")
    st.markdown("### Course-wise intake")
    course_chart = px.bar(courses_df, x="course", y=["intake","admissions"], barmode="group", labels={"course":"Course","value":"Students","variable":"Measure"})
    chart_layout(course_chart, 360)
    st.dataframe(courses_df.rename(columns={"course":"Course","intake":"Approved intake (demo)","admissions":"Admissions (demo)"}), use_container_width=True, hide_index=True)
    st.download_button("Download admission table (CSV)", admissions_df.to_csv(index=False).encode("utf-8"), "iip_admissions_demo.csv", "text/csv")

elif page == "Placement Intelligence":
    st.subheader("Placement Intelligence")
    st.caption("Five-year outcomes, with all values marked as demonstration figures.")
    a,b,c = st.columns(3)
    latest_p = placements_df.iloc[-1]
    a.metric("Latest placement rate", f'{latest_p["placement_rate"]:.1f}%')
    b.metric("Students placed", f'{int(latest_p["placed"]):,}')
    c.metric("Average package", money_lakh(latest_p["average"]))
    chart = px.line(placements_df, x="year", y="placement_rate", markers=True, labels={"year":"Placement year","placement_rate":"Placement rate (%)"})
    chart.update_traces(line_color="#0F8B8D", line_width=3)
    chart_layout(chart)
    st.dataframe(placements_df.rename(columns={"year":"Year","eligible":"Eligible students (demo)","placed":"Students placed (demo)","placement_rate":"Placement rate (%)","highest":"Highest package (₹ lakh)","average":"Average package (₹ lakh)","median":"Median package (₹ lakh)"}).round(1), use_container_width=True, hide_index=True)
    st.markdown("### Employer intelligence")
    st.info("Recruiter-level records, repeat recruiters, sectors, internship companies and placement locations are not included in this starter dataset. Add sourced records before presenting these as findings.")
    st.download_button("Download placement table (CSV)", placements_df.to_csv(index=False).encode("utf-8"), "iip_placements_demo.csv", "text/csv")

elif page == "Rankings & Accreditation":
    st.subheader("Rankings & Accreditation")
    st.caption("Regulatory statuses below are placeholders for demonstrating the interface, not verified records.")
    data = pd.DataFrame([
        ["UGC recognition","Not verified","No official evidence connected"],
        ["AICTE approval","Not verified","Approval letter/source required"],
        ["NAAC",inst["naac"],"Verify grade, cycle and validity"],
        ["NBA accreditation","Unavailable","Programme-specific evidence required"],
        ["University affiliation","Requires validation","Affiliation order required"],
        ["NIRF",inst["nirf"],"Check relevant category and year"],
        ["Autonomous status","Unavailable","Official record required"],
    ], columns=["Area","Current status","Evidence / next step"])
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.markdown("### Five-year ranking timeline")
    timeline = pd.DataFrame({"Year":[2022,2023,2024,2025,2026],"Rank":["Unavailable"]*5})
    st.dataframe(timeline, use_container_width=True, hide_index=True)
    st.warning("Do not infer a rank, approval or accreditation from missing data. Add the official source URL and checked date for each claim.")

elif page == "Promoter Due Diligence":
    st.subheader("Promoter Due Diligence")
    st.caption("Use documented public records and preserve the legal status of each record.")
    st.info("No promoter or litigation data is populated in this demo. This does not mean that no records exist.")
    with st.form("promoter_record_form"):
        p1,p2 = st.columns(2)
        with p1:
            entity = st.text_input("Person / trust / society / company")
            record_type = st.selectbox("Record type", ["Promoter profile","Corporate association","Court case","Regulatory action","Insolvency record","Government notice","Other"])
            legal_status = st.selectbox("Record status", ["Not assessed","Complaint","FIR","Charge","Prosecution","Conviction","Acquittal","Civil dispute","Order / notice"])
        with p2:
            record_date = st.date_input("Record date", value=date.today())
            jurisdiction = st.text_input("Jurisdiction / authority")
            source_url = st.text_input("Source URL")
        summary = st.text_area("Evidence-based summary")
        submitted = st.form_submit_button("Add to temporary review list")
    if submitted:
        if not entity.strip() or not summary.strip():
            st.error("Enter an entity and a summary.")
        else:
            st.session_state.setdefault("promoter_records", []).append({
                "Entity":entity,"Record type":record_type,"Status":legal_status,
                "Date":str(record_date),"Jurisdiction":jurisdiction,
                "Source URL":source_url,"Summary":summary
            })
            st.success("Added to this browser session's temporary review list.")
    records = st.session_state.get("promoter_records", [])
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
        st.download_button("Export review list (CSV)", pd.DataFrame(records).to_csv(index=False).encode("utf-8"), "iip_promoter_review.csv", "text/csv")
    st.caption("This prototype does not perform legal-record searches or independently validate user-entered claims.")

elif page == "Campus Performance":
    st.subheader("Campus Performance")
    a,b,c,d = st.columns(4)
    a.metric("Student strength", f'{inst["students"]:,}')
    b.metric("Faculty strength", f'{inst["faculty"]:,}')
    b_ratio = inst["students"] / inst["faculty"] if inst["faculty"] else 0
    c.metric("Students per faculty", f"{b_ratio:.1f}")
    d.metric("Campus utilisation", f"{current_util:.1f}%")
    infra = pd.DataFrame([
        ["Land area",f'{inst["land"]} acres',"Requires source validation"],
        ["Built-up area",f'{inst["builtup"]:,} sq ft',"Requires source validation"],
        ["Classrooms","Unavailable","No source record"],
        ["Laboratories","Unavailable","No source record"],
        ["Library","Unavailable","No source record"],
        ["Hostel capacity / occupancy","Unavailable","No source record"],
        ["Sports and transport","Unavailable","No source record"],
    ], columns=["Parameter","Value","Status"])
    st.markdown("### Infrastructure overview")
    st.dataframe(infra, use_container_width=True, hide_index=True)
    st.markdown("### Academic indicators")
    academics = pd.DataFrame([
        ["Attendance","Unavailable"],["Pass percentage","Unavailable"],["Backlogs","Unavailable"],
        ["Dropout rate","Unavailable"],["Graduation rate","Unavailable"],["Student progression","Unavailable"],
    ], columns=["Indicator","Value"])
    st.dataframe(academics, use_container_width=True, hide_index=True)
    st.caption("Unavailable means the starter dataset does not contain this information; it is not a negative assessment.")

elif page == "Commercial Intelligence":
    st.subheader("Commercial Intelligence")
    st.caption("Explore hypothetical scenarios. Outputs are not actual revenue forecasts.")
    with st.container(border=True):
        st.markdown("### Partnership scenario calculator")
        x1,x2,x3 = st.columns(3)
        with x1:
            addressable = st.number_input("Eligible / addressable students", min_value=0, max_value=1000000, value=min(inst["students"],1000000), step=50)
        with x2:
            participation = st.slider("Assumed participation rate (%)", 0, 100, 20)
        with x3:
            revenue_per_student = st.number_input("Assumed gross revenue per participating student (₹)", min_value=0, max_value=10000000, value=15000, step=1000)
        participants = round(addressable * participation / 100)
        gross_potential = participants * revenue_per_student
        m1,m2,m3 = st.columns(3)
        m1.metric("Potential participants", f"{participants:,}")
        m2.metric("Illustrative gross potential", f"₹{gross_potential:,.0f}")
        m3.metric("Capacity headroom", f'{max(inst["capacity"]-inst["students"],0):,}')
        st.caption("Formula: eligible students × assumed participation rate × assumed gross revenue per participating student.")
    st.markdown("### Institution commercial snapshot")
    c1,c2,c3 = st.columns(3)
    c1.metric("Total students (demo)", f'{inst["students"]:,}')
    c2.metric("Latest admissions (demo)", f'{inst["latest_admissions"]:,}')
    c3.metric("Annual fee assumption", money_lakh(inst["annual_fee_lakh"]))
    st.warning("Fee collection, discounts, refunds, outstanding balances, and actual revenue are unavailable. Do not treat scenario outputs as confirmed revenue, profit, or a partnership recommendation.")
    scenario = pd.DataFrame([{
        "Institution":institution_name,"Eligible students":addressable,
        "Participation rate (%)":participation,"Assumed gross revenue per participant (₹)":revenue_per_student,
        "Potential participants":participants,"Illustrative gross potential (₹)":gross_potential
    }])
    st.download_button("Download scenario (CSV)", scenario.to_csv(index=False).encode("utf-8"), "iip_commercial_scenario.csv", "text/csv")

elif page == "Risk & Red Flags":
    st.subheader("Risk & Red Flags")
    st.caption("Illustrative review items only. A review flag is not proof of a violation.")
    risks = pd.DataFrame([
        ["Regulatory","Attention","Recognition / approval evidence not connected","Obtain current official records","Requires review"],
        ["Admissions","Attention","Reported and comparison figures differ in demo data","Reconcile academic year and definitions","Demonstration"],
        ["Placements","Attention","Placement values are not independently verified","Request placement report and supporting methodology","Requires review"],
        ["Infrastructure","Insufficient data","Infrastructure evidence is incomplete","Request current inventory and supporting records","Insufficient data"],
        ["Promoter / legal","Insufficient data","No public-record research is connected","Conduct documented review using reliable records","Insufficient data"],
    ], columns=["Category","Severity","Indicator","Recommended follow-up","Evidence status"])
    sev = st.multiselect("Severity", risks["Severity"].unique().tolist(), default=risks["Severity"].unique().tolist())
    filtered = risks[risks["Severity"].isin(sev)]
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.markdown("### Review principles")
    st.markdown("- Critical issues should be tied to authoritative evidence.\n- Missing information is not proof of non-compliance.\n- Allegations and legal outcomes must be distinguished.\n- Keep the underlying source and review date with every risk record.")
    st.download_button("Download risk register (CSV)", filtered.to_csv(index=False).encode("utf-8"), "iip_risk_register_demo.csv", "text/csv")

elif page == "Sources & Verification":
    st.subheader("Sources & Verification")
    st.caption("A metric is only as reliable as its source and the date and method of verification.")
    show_sources()
    st.markdown("### Add a source record")
    with st.form("source_form"):
        c1,c2 = st.columns(2)
        with c1:
            metric = st.text_input("Metric / claim")
            source_org = st.text_input("Source organization")
            source_kind = st.selectbox("Source type", ["Government data","University portal","Regulatory authority","Institution website","Published report","Internal assessment","Demonstration dataset"])
        with c2:
            check_date = st.date_input("Date checked", value=date.today(), key="source_check_date")
            status = st.selectbox("Verification status", ["Verified","Self-reported","Requires validation","Estimate","Unavailable","Demonstration"])
            url = st.text_input("Source URL")
        note = st.text_area("Evidence notes")
        save_source = st.form_submit_button("Add source to temporary register")
    if save_source:
        if not metric.strip() or not source_org.strip():
            st.error("Enter at least the metric and source organization.")
        else:
            st.session_state.setdefault("extra_sources", []).append({
                "Metric":metric,"Source organization":source_org,"Source type":source_kind,
                "Date checked":str(check_date),"Status":status,"Source URL":url,"Evidence notes":note
            })
            st.success("Added to this browser session's temporary source register.")
    extra = st.session_state.get("extra_sources", [])
    if extra:
        st.dataframe(pd.DataFrame(extra), use_container_width=True, hide_index=True)
        st.download_button("Export added sources (CSV)", pd.DataFrame(extra).to_csv(index=False).encode("utf-8"), "iip_added_sources.csv", "text/csv")

# ---------- Global report export ----------
st.markdown("---")
report = pd.DataFrame([{
    "Institution": institution_name,
    "Institution type": inst["type"],
    "Location": f'{inst["city"]}, {inst["state"]}',
    "Ownership": inst["ownership"],
    "Established": inst["established"],
    "Affiliated university": inst["university"],
    "AISHE code": inst["aishe"],
    "Student capacity (demo)": inst["capacity"],
    "Current students (demo)": inst["students"],
    "Capacity utilisation (%)": round(current_util,1),
    "Latest admissions (demo)": inst["latest_admissions"],
    "Placement rate (demo, unverified)": inst["placement"],
    "Risk state (illustrative)": inst["risk"],
    "Data note": "Fictional demonstration data. Not official or independently verified."
}])
st.download_button("Download executive snapshot (CSV)", report.to_csv(index=False).encode("utf-8"), file_name="iip_executive_snapshot_demo.csv", mime="text/csv")
st.caption("IIP prototype • Demonstration data only • Verify every institutional claim against its underlying source before decision-making.")
