import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SalarySense – SaaS Salary Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# GLOBAL CSS – SaaS THEME
# =========================

# Apply dark mode styles if enabled
dark_mode_css = ""
if st.session_state.get('dark_mode', False):
    dark_mode_css = """
    /* Dark mode overrides */
    .stApp {
        background: linear-gradient(135deg, #0f172a, #1e293b, #334155) !important;
    }
    .saas-brand-title, .section-title {
        color: #f1f5f9 !important;
    }
    .saas-brand-subtitle, .section-subtitle {
        color: #94a3b8 !important;
    }
    .saas-info-card {
        background: rgba(30, 41, 59, 0.85) !important;
        border: 1px solid rgba(71, 85, 105, 0.55) !important;
    }
    .saas-info-card h3 {
        color: #f1f5f9 !important;
    }
    .saas-info-card p {
        color: #cbd5e1 !important;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.82) !important;
        border: 1px solid rgba(71, 85, 105, 0.7) !important;
    }
    .glass-card h3 {
        color: #f1f5f9 !important;
    }
    .glass-card p {
        color: #cbd5e1 !important;
    }
    .result-card {
        background: rgba(30, 41, 59, 0.96) !important;
        border: 1px solid rgba(71, 85, 105, 0.7) !important;
    }
    .result-title {
        color: #f1f5f9 !important;
    }
    /* About section text */
    .stMarkdown p, .stMarkdown li {
        color: #f1f5f9 !important;
    }
    h3 {
        color: #f1f5f9 !important;
    }
    """

st.markdown(
    """
<style>
/* Global animated background */
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f8f9ff, #ffffff);
    background-size: 400% 400%;
    animation: gradientShift 18s ease infinite;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Top navbar */
.saas-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 4px 2px 4px;
}
.saas-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}
.saas-logo {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    background: radial-gradient(circle at 0% 0%, #ff8a3c, #7b5cff);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-weight: 800;
    font-size: 20px;
}
.saas-brand-title {
    font-size: 20px;
    font-weight: 800;
    color: #111827;
}
.saas-brand-subtitle {
    font-size: 12px;
    color: #6b7280;
}
.saas-pill {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 999px;
    background: #ecf0ff;
    color: #4f46e5;
    font-weight: 600;
}
.saas-top-right {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #6b7280;
}
.saas-avatar {
    width: 28px;
    height: 28px;
    border-radius: 999px;
    background: linear-gradient(135deg, #4f46e5, #ec4899);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #f9fafb;
    font-weight: 700;
    font-size: 13px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #1f2937);
    color: #f9fafb !important;
}
.sidebar-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 4px;
}
.sidebar-caption {
    font-size: 11px;
    color: #d1d5db;
    margin-bottom: 16px;
}
.sidebar-footer {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 24px;
}

/* Sidebar radio buttons */
.st-emotion-cache-16txtl3, .st-emotion-cache-10trblm {
    color: #e5e7eb !important;
}

/* KPI cards */
.kpi-row {
    margin-top: 8px;
}
.kpi-card {
    background: rgba(255,255,255,0.90);
    border-radius: 18px;
    padding: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 10px 26px rgba(15,23,42,0.06);
}
.kpi-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: .16em;
    color: #9ca3af;
}
.kpi-value {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
}
.kpi-sub {
    font-size: 12px;
    color: #6b7280;
}

/* Glass / info cards */
.card-wrapper {
    display: flex;
    gap: 22px;
    margin-top: 24px;
}
.glass-card {
    flex: 1;
    background: rgba(255,255,255,0.82);
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.7);
    backdrop-filter: blur(14px) saturate(180%);
    -webkit-backdrop-filter: blur(14px) saturate(180%);
    box-shadow: 0 10px 30px rgba(15,23,42,0.12);
    transition: all 0.25s ease-out;
}
.glass-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 18px 44px rgba(15,23,42,0.22);
    border-color: rgba(129,140,248,0.9);
}
.glass-card h3 {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 4px;
    color: #111827;
}
.glass-card p {
    margin: 3px 0;
    font-size: 0.95rem;
    color: #4b5563;
}

/* Tabs */
.stTabs [role="tab"] {
    background: rgba(255,255,255,0.95);
    color: #6b7280 !important;
    padding: 8px 18px;
    border-radius: 999px;
    border: 1px solid #e5e7eb;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: #111827 !important;
    color: #f9fafb !important;
    border-color: #111827 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #ec4899);
    color: #ffffff !important;
    padding: 8px 18px;
    border-radius: 999px;
    border: none;
    font-weight: 600;
    width: 100%;
    box-shadow: 0 8px 22px rgba(129,140,248,0.5);
}
.stButton > button:hover {
    transform: translateY(-1px) scale(1.02);
    transition: 0.15s ease-in-out;
}

/* Result card */
.result-card {
    background: rgba(255,255,255,0.96);
    border-radius: 22px;
    padding: 24px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 14px 36px rgba(15,23,42,0.16);
}
.result-title {
    font-size: 20px;
    font-weight: 800;
    color: #111827;
}
.result-pill-good {
    display: inline-flex;
    padding: 4px 10px;
    border-radius: 999px;
    background: #ecfdf5;
    color: #15803d;
    font-size: 12px;
    font-weight: 600;
    margin-top: 6px;
}
.result-pill-risk {
    display: inline-flex;
    padding: 4px 10px;
    border-radius: 999px;
    background: #fef2f2;
    color: #b91c1c;
    font-size: 12px;
    font-weight: 600;
    margin-top: 6px;
}
.result-sub {
    font-size: 13px;
    color: #6b7280;
    margin-top: 8px;
}

/* Section titles */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #111827;
}
.section-subtitle {
    font-size: 13px;
    color: #6b7280;
}

/* Footer */
.footer-note {
    text-align: right;
    font-size: 11px;
    color: #9ca3af;
    margin-top: 26px;
    padding-bottom: 8px;
}

/* Main SaaS card */
.saas-info-card {
    flex: 1;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.55);
    backdrop-filter: blur(12px) saturate(160%);
    box-shadow: 0 6px 22px rgba(0,0,0,0.08);
    transition: all .28s cubic-bezier(0.22, 1, 0.36, 1);
    transform-style: preserve-3d;
}

/* Hover: 3D lift + glow + shadow */
.saas-info-card:hover {
    transform: translateY(-10px) scale(1.03) rotateX(3deg) rotateY(-3deg);
    border: 1px solid rgba(138, 92, 255, 0.65);
    box-shadow: 
        0 18px 42px rgba(0,0,0,0.18),
        0 0 16px rgba(138, 92, 255, 0.35);
}

/* Text styling */
.saas-info-card h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 6px;
}

.saas-info-card p {
    margin: 3px 0;
    font-size: 0.95rem;
    color: #4b5563;
}

/* Responsive */
@media(max-width: 900px) {
    .card-wrapper {
        flex-direction: column;
    }
}

""" + dark_mode_css + """

</style>
""",
    unsafe_allow_html=True,
)

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    try:
        return joblib.load("best_salary_model_pipeline.pkl")
    except FileNotFoundError:
        st.error("❌ Model file not found. Make sure 'best_salary_model_pipeline.pkl' is in this folder.")
        return None


model = load_model()

# =========================
# SIDEBAR – NAVIGATION
# =========================
with st.sidebar:
    st.markdown('<div class="sidebar-title">SalarySense</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-caption">AI-powered salary band intelligence for HR, analytics, and experiments.</div>',
        unsafe_allow_html=True,
    )

    # Dark/Light mode toggle
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    if st.button("🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "👤 Single Prediction", "📂 Batch Prediction", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-footer">Logged in as <b>Waleed</b><br/>Streamlit SaaS Template · v1.0</div>',
        unsafe_allow_html=True,
    )

# =========================
# TOP NAVBAR
# =========================
st.markdown(
    """
<div class="saas-topbar">
    <div class="saas-brand">
        <div class="saas-logo">S</div>
        <div>
            <div class="saas-brand-title">SalarySense</div>
            <div class="saas-brand-subtitle">SaaS Salary Prediction & Insights</div>
        </div>
        <div class="saas-pill">ML · Binary Classifier</div>
    </div>
    <div class="saas-top-right">
        <span>Plan: <b>Developer</b></span>
        <div class="saas-avatar">W</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")  # small spacing

# ==========================================================
# PAGE: DASHBOARD
# ==========================================================
if page == "🏠 Dashboard":
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="saas-info-card">
            <h3>🧠 Model Type</h3>
            <p><strong>Classification</strong></p>
            <p>Predicts salary > / ≤ $50K</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="saas-info-card">
            <h3>📊 Features Used</h3>
            <p><strong>5 Features</strong></p>
            <p>Age · Hours · Edu · Role · Experience*</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="saas-info-card">
            <h3>💼 Primary Use Case</h3>
            <p><strong>HR Analytics</strong></p>
            <p>What-if simulation & band analysis</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-title">Model Overview</div>
        <div class="section-subtitle">
            Get a quick understanding of how this classifier behaves and how it can be integrated into HR or analytics workflows.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card-wrapper">
            <div class="glass-card">
                <h3>🧠 Model Behavior</h3>
                <p><strong>Binary classification</strong> model trained on income labels.</p>
                <p>Returns salary bands as <strong>> $50K</strong> or <strong>≤ $50K</strong> with probability scores.</p>
            </div>
            <div class="glass-card">
                <h3>📥 Input Space</h3>
                <p>Designed for <strong>structured tabular data</strong>.</p>
                <p>Ideal for HR datasets with employee demographics, working hours, and role attributes.</p>
            </div>
            <div class="glass-card">
                <h3>💼 Integration Ideas</h3>
                <p>Use in <strong>salary benchmarking tools</strong>, internal HR dashboards, or analytics playgrounds.</p>
                <p>Great for education, demos, and experimentation.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # simple static example chart (placeholder)
    demo_df = pd.DataFrame(
        {
            "Band": ["> $50K", "<= $50K"],
            "Count": [42, 58],
        }
    )
    fig = px.bar(
        demo_df,
        x="Band",
        y="Count",
        text="Count",
        title="Sample Salary Band Distribution (Demo)",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), template="simple_white")
    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# PAGE: SINGLE PREDICTION
# ==========================================================
elif page == "👤 Single Prediction":
    st.markdown(
        """
        <div class="section-title">Single Prediction</div>
        <div class="section-subtitle">
            Provide a single employee profile to predict their salary band and inspect confidence.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        with st.form("single_form"):
            age = st.number_input("Age", 18, 90, 30)
            hours_per_week = st.number_input("Hours per Week", 1, 99, 40)

            education = st.selectbox(
                "Education Level",
                [
                    "Bachelors",
                    "Masters",
                    "Doctorate",
                    "Some-college",
                    "HS-grad",
                    "Prof-school",
                    "Assoc-acdm",
                    "Assoc-voc",
                    "11th",
                ],
            )

            occupation = st.selectbox(
                "Occupation",
                [
                    "Prof-specialty",
                    "Exec-managerial",
                    "Sales",
                    "Craft-repair",
                    "Adm-clerical",
                    "Tech-support",
                    "Machine-op-inspct",
                    "Other-service",
                    "Transport-moving",
                ],
            )

            submitted = st.form_submit_button("🚀 Predict This Profile")

    with col_right:
        if submitted and model:
            experience = max(0, age - 18)
            input_df = pd.DataFrame(
                {
                    "age": [age],
                    "education": [education],
                    "occupation": [occupation],
                    "hours-per-week": [hours_per_week],
                    "experience": [experience],
                }
            )
            try:
                pred = model.predict(input_df)[0]
                proba = model.predict_proba(input_df)[0]
                band = "> $50K" if pred == 1 else "≤ $50K"
                conf = float(max(proba))

                pill_class = "result-pill-good" if pred == 1 else "result-pill-risk"
                pill_text = "Higher income band" if pred == 1 else "Lower income band"

                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-title">Predicted Salary Band: {band}</div>
                        <div class="{pill_class}">{pill_text}</div>
                        <div class="result-sub">
                            Model confidence: <b>{conf:.2%}</b><br/>
                            Features used: age, education, occupation, hours per week, engineered experience.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Confidence bar chart
                prob_df = pd.DataFrame(
                    {"Band": ["> $50K", "≤ $50K"], "Probability": proba}
                )
                fig2 = px.bar(
                    prob_df,
                    x="Band",
                    y="Probability",
                    range_y=[0, 1],
                    text="Probability",
                    title="Confidence Breakdown",
                )
                fig2.update_traces(
                    texttemplate="%{text:.2%}",
                    textposition="outside",
                    marker=dict(
                        color=["#16a34a" if b == "> $50K" else "#dc2626" for b in prob_df["Band"]],
                    ),
                )
                fig2.update_layout(
                    margin=dict(l=10, r=10, t=40, b=10), template="simple_white", yaxis_title=""
                )
                st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.info("Fill the form on the left and click **Predict This Profile** to see results here.")

# ==========================================================
# PAGE: BATCH PREDICTION
# ==========================================================
elif page == "📂 Batch Prediction":
    st.markdown(
        """
        <div class="section-title">Batch Prediction</div>
        <div class="section-subtitle">
            Upload a CSV with multiple employee records and generate salary band predictions with distribution analytics.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    uploaded = st.file_uploader(
        "Upload CSV with columns: age, education, occupation, hours-per-week",
        type="csv",
    )

    if uploaded is not None and model:
        try:
            df = pd.read_csv(uploaded)
            required_cols = {"age", "education", "occupation", "hours-per-week"}

            if not required_cols.issubset(df.columns):
                st.error(f"CSV must contain columns: {', '.join(required_cols)}")
            else:
                df_pred = df[list(required_cols)].copy()
                df_pred["experience"] = (df_pred["age"] - 18).clip(lower=0)
                preds = model.predict(df_pred)
                df["Predicted Salary Band"] = ["> $50K" if p == 1 else "≤ $50K" for p in preds]

                st.success("✅ Batch predictions generated successfully.")

                col_a, col_b = st.columns([1.1, 1])

                with col_a:
                    counts = df["Predicted Salary Band"].value_counts()
                    pie = px.pie(
                        names=counts.index,
                        values=counts.values,
                        title="Predicted Salary Band Distribution",
                        color=counts.index,
                        color_discrete_map={"> $50K": "#16a34a", "≤ $50K": "#dc2626"},
                    )
                    pie.update_traces(textinfo="percent+label")
                    st.plotly_chart(pie, use_container_width=True)

                with col_b:
                    st.write("**Preview (first 20 rows)**")
                    st.dataframe(df.head(20))

                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download Full Prediction CSV",
                    csv_bytes,
                    "salary_predictions.csv",
                    mime="text/csv",
                )

        except Exception as e:
            st.error(f"Error reading or processing CSV: {e}")
    elif uploaded is None:
        st.info("📂 Upload a CSV file to run batch predictions.")

# ==========================================================
# PAGE: ABOUT / CREDITS
# ==========================================================
elif page == "ℹ️ About":
    st.markdown(
        """
        <div class="section-title">About SalarySense</div>
        <div class="section-subtitle">
            A demo SaaS-style salary prediction platform built with Streamlit, scikit-learn, and a tabular income classifier.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 👨💻 Developer")
    st.write("**Name:** Waleedul Haque")
    st.write("**Role:** B.Tech CSE · AI & Full Stack Enthusiast")
    st.write("**GitHub:** [@waleedul3](https://github.com/waleedul3)")
    st.write("**Use Case:** Portfolio project · Internship/placement showcase · AI demo")

    st.markdown("### 🧠 Tech Stack")
    st.write("- **Frontend & UI:** Streamlit (custom SaaS-style CSS)")
    st.write("- **Model:** scikit-learn pipeline loaded via `joblib`")
    st.write("- **Data Handling:** pandas")
    st.write("- **Visualization:** Plotly (interactive charts)")

    st.markdown("### 🚀 Ideas to Extend")
    st.write("- Add authentication (just UI) for HR vs Admin roles")
    st.write("- Add explainability (feature importance, SHAP plots)")
    st.write("- Integrate with a database to log predictions")
    st.write("- Deploy as a true SaaS-style tool with user accounts")

# FOOTER
st.markdown(
    """
    <div class="footer-note">
        SalarySense · Built with ❤️ by <strong>Waleedul Haque</strong> · Powered by Streamlit & scikit-learn
    </div>
    """,
    unsafe_allow_html=True,
)