import joblib
import pandas as pd
from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# Load the trained model pipeline
# This pipeline includes preprocessing (scaling, one-hot encoding) and the classifier.
try:
    model = joblib.load('best_salary_model_pipeline.pkl')
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Model file not found. Make sure 'best_salary_model_pipeline.pkl' is in the correct directory.")
    model = None

# Define the route for the home page, which will display the form
# In your app.py, update the home() function like this:

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_data = None # Initialize as None
    if request.method == 'POST' and model:
        try:
            # --- Get form data ---
            age = int(request.form['age'])
            hours_per_week = int(request.form['hours-per-week'])
            education = request.form['education']
            occupation = request.form['occupation']
            experience = max(0, age - 18)

            # --- Create DataFrame for prediction ---
            input_df = pd.DataFrame({
                'age': [age], 'education': [education], 'occupation': [occupation],
                'hours-per-week': [hours_per_week], 'experience': [experience]
            })

            # --- Make prediction ---
            prediction = model.predict(input_df)[0]
            prediction_proba = model.predict_proba(input_df)[0]

            # --- Structure the results ---
            if prediction == 1:
                result_text = "> $50K"
                confidence = prediction_proba[1]
            else:
                result_text = "<= $50K"
                confidence = prediction_proba[0]

            prediction_data = {
                'result': result_text,
                'confidence': round(confidence * 100, 2)
            }

        except Exception as e:
            prediction_data = {'error': f"An error occurred: {e}"}

    # Render the template, passing the prediction data dictionary
    return render_template('index.html', prediction=prediction_data)

# Run the Flask app
if __name__ == '__main__':
    # Using host='0.0.0.0' makes the app accessible on your local network
    app.run(host='0.0.0.0', port=5000, debug=True)