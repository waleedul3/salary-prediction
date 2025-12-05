import streamlit as st
import joblib
import pandas as pd
import io
import plotly.express as px  # Import Plotly

# --- Page Configuration ---
st.set_page_config(
    page_title="Employee Salary Predictor",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme-Aware CSS ---
st.markdown("""
<style>
    :root {--primary-color: #007bff; --background-color: #f0f2f6; --card-background-color: #ffffff; --text-color: #212529; --border-color: #e6e6e6; --gradient-start: #007bff; --gradient-end: #00c6ff;}
    body.theme-dark {--primary-color: #00aaff; --background-color: #0e1117; --card-background-color: #161b22; --text-color: #fafafa; --border-color: #30363d; --gradient-start: #00aaff; --gradient-end: #007bff;}
    .stApp {background-color: var(--background-color);}
    .main .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    .metric-card {background-color: var(--card-background-color); border: 1px solid var(--border-color); padding: 1.5rem; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.04);}
    .metric-card h3 {color: var(--primary-color); font-size: 1.2rem; margin-bottom: 0.5rem;}
    .metric-card p {color: var(--text-color); font-size: 2.2rem; font-weight: 600;}
    .stProgress > div > div > div > div {background-image: linear-gradient(to right, var(--gradient-start), var(--gradient-end));}
</style>
""", unsafe_allow_html=True)


# --- Model Loading ---
@st.cache_resource
def load_model():
    """Loads the trained model pipeline from disk."""
    try:
        return joblib.load('best_salary_model_pipeline.pkl')
    except FileNotFoundError:
        st.error("❌ Model file not found. Ensure 'best_salary_model_pipeline.pkl' is present.")
        return None
model = load_model()

# --- Sidebar ---
with st.sidebar:
   
    st.header("👤 Single Record Input")
    with st.form("single_prediction_form"):
        age = st.number_input("Age", 18, 90, 30)
        hours_per_week = st.number_input("Hours/Week", 1, 99, 40)
        education = st.selectbox("🎓 Education Level", ['Bachelors', 'Masters', 'Doctorate', 'Some-college', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc', '11th'])
        occupation = st.selectbox("🧑‍💻 Occupation", ['Prof-specialty', 'Exec-managerial', 'Sales', 'Craft-repair', 'Adm-clerical', 'Tech-support', 'Machine-op-inspct', 'Other-service', 'Transport-moving'])
        submit_button_single = st.form_submit_button("🚀 Predict Single Record", use_container_width=True)

# --- Main Page ---
st.title("👨‍💼 Employee Salary Predictor")
st.markdown("Choose between predicting a single record or uploading a CSV for batch predictions.")
tab1, tab2 = st.tabs(["👤 Single Prediction", "📂 Batch Prediction"])

# --- Tab 1: Single Prediction ---
with tab1:
    st.header("Single Record Prediction")
    if submit_button_single and model:
        experience = max(0, age - 18)
        input_data = pd.DataFrame({'age': [age], 'education': [education], 'occupation': [occupation], 'hours-per-week': [hours_per_week], 'experience': [experience]})
        try:
            prediction = model.predict(input_data)[0]
            prediction_proba = model.predict_proba(input_data)[0]
            if prediction == 1:
                result_text = "> $50K"
                st.balloons()
            else:
                result_text = "<= $50K"

            st.subheader("📈 Prediction Analysis")
            col1, col2 = st.columns([0.6, 0.4]) # Adjust column widths
            with col1:
                st.markdown(f'<div class="metric-card"><h3>Predicted Salary</h3><p>{result_text}</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-card" style="margin-top: 20px;"><h3>Confidence</h3><p>{max(prediction_proba):.2%}</p></div>', unsafe_allow_html=True)
            
            with col2:
                # ⭐ NEW: Pie chart for confidence scores
                prob_df = pd.DataFrame({'Category': ['> $50K', '<= $50K'], 'Probability': prediction_proba})
                fig = px.pie(prob_df, values='Probability', names='Category', title='Prediction Probability',
                             color_discrete_sequence=px.colors.sequential.Blues_r)
                fig.update_layout(showlegend=False)
                fig.update_traces(textinfo='percent+label', textfont_size=14)
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Enter details in the sidebar and click 'Predict' to see the result here.", icon="👋")

# --- Tab 2: Batch Prediction ---
with tab2:
    st.header("Batch Salary Prediction")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="CSV should contain: 'age', 'education', 'occupation', 'hours-per-week'")
    if uploaded_file is not None and model:
        df_upload = pd.read_csv(uploaded_file)
        required_cols = {'age', 'education', 'occupation', 'hours-per-week'}
        if not required_cols.issubset(df_upload.columns):
            st.error(f"Error: CSV must contain the following columns: {list(required_cols)}")
        else:
            with st.spinner('Generating predictions...'):
                df_predict = df_upload[list(required_cols)].copy()
                df_predict['experience'] = (df_predict['age'] - 18).clip(lower=0)
                predictions = model.predict(df_predict)
                df_upload['Predicted Salary'] = ['> $50K' if p == 1 else '<= $50K' for p in predictions]
            
            st.success("✅ Predictions Generated Successfully!")
            
            # ⭐ NEW: Display a plot and the dataframe side-by-side
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Prediction Distribution")
                prediction_counts = df_upload['Predicted Salary'].value_counts()
                fig = px.pie(values=prediction_counts.values, names=prediction_counts.index, title="Distribution of Predicted Salaries")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("Prediction Results")
                st.dataframe(df_upload)

            csv_data = df_upload.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results as CSV", csv_data, 'predicted_salaries.csv', 'text/csv', use_container_width=True, type="primary")