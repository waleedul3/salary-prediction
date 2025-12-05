# 💼 SalarySense - AI-Powered Salary Prediction Platform

A modern SaaS-style web application for predicting employee salary bands using machine learning. Built with Streamlit and featuring a professional dark/light mode interface.
<img width="1913" height="972" alt="image" src="https://github.com/user-attachments/assets/dd0ab0a6-465f-48a5-94f2-5062f8ebba4b" />
<img width="1912" height="968" alt="image" src="https://github.com/user-attachments/assets/101dc3a5-e29f-44b6-bcca-21c2b7003426" />
<img width="1910" height="978" alt="image" src="https://github.com/user-attachments/assets/1514042f-d139-47d6-8621-f527abc2aa2f" />
<img width="1910" height="976" alt="image" src="https://github.com/user-attachments/assets/6bf09ede-ca1b-4e76-97aa-b02b3e325d4b" />
<img width="1913" height="893" alt="image" src="https://github.com/user-attachments/assets/327b25f3-0575-4d2a-b237-c0fb36c98605" />
<img width="1882" height="894" alt="image" src="https://github.com/user-attachments/assets/fa06a08f-ce84-4c11-91b1-712a691230d3" />







## ✨ Features

- **🧠 ML-Powered Predictions**: Binary classification model predicting salary > / ≤ $50K
- **👤 Single Prediction**: Individual employee salary band prediction
- **📂 Batch Processing**: CSV upload for bulk predictions with analytics
- **🌙 Dark/Light Mode**: Toggle between themes with smooth transitions
- **📊 Interactive Charts**: Plotly visualizations for confidence breakdown
- **🎨 Modern UI**: SaaS-style interface with 3D hover effects and glassmorphism
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Required packages (see requirements.txt)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd employee-salary-prediction
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app3.py
```

4. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
employee-salary-prediction/
├── app3.py                           # Main Streamlit application
├── best_salary_model_pipeline.pkl    # Trained ML model
├── requirements.txt                  # Python dependencies
└── README.md                        # Project documentation
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python
- **ML Framework**: scikit-learn
- **Data Processing**: pandas, numpy
- **Visualization**: Plotly
- **Model Persistence**: joblib

## 📊 Model Details

- **Type**: Binary Classification
- **Features**: Age, Education, Occupation, Hours per Week, Experience (engineered)
- **Output**: Salary band prediction (> $50K or ≤ $50K) with confidence scores
- **Use Case**: HR analytics, salary benchmarking, what-if analysis

## 🎯 Usage

### Dashboard
- Overview of model capabilities
- Interactive KPI cards with 3D hover effects
- Sample data visualization

### Single Prediction
1. Enter employee details in the form
2. Click "Predict This Profile"
3. View salary band prediction with confidence breakdown

### Batch Prediction
1. Upload CSV with columns: `age`, `education`, `occupation`, `hours-per-week`
2. Download results with predictions
3. View distribution analytics

### Theme Toggle
- Click the 🌙/☀️ button in sidebar to switch themes
- Automatic UI adaptation for dark/light modes

## 📋 CSV Format for Batch Predictions

Your CSV should contain these columns:
- `age`: Employee age (18-90)
- `education`: Education level (Bachelors, Masters, etc.)
- `occupation`: Job role (Prof-specialty, Exec-managerial, etc.)
- `hours-per-week`: Working hours per week (1-99)

## 🚀 Deployment

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy with one click

### Local Production
```bash
streamlit run app3.py --server.port 8501 --server.address 0.0.0.0
```

## 👨‍💻 Developer

**Waleedul Haque**
- B.Tech CSE Student
- AI & Full Stack Enthusiast
- GitHub: [@waleedul3](https://github.com/waleedul3)

## 🎨 UI Features

- **Glassmorphism Effects**: Translucent cards with backdrop blur
- **3D Hover Animations**: Cards lift and tilt on hover
- **Gradient Backgrounds**: Animated color transitions
- **Professional Typography**: System fonts with proper hierarchy
- **Responsive Layout**: Adapts to different screen sizes

## 🔧 Customization

### Adding New Features
- Modify `app3.py` for new functionality
- Update CSS in the `<style>` block for UI changes
- Add new pages by extending the sidebar navigation

### Model Updates
- Replace `best_salary_model_pipeline.pkl` with your trained model
- Ensure model accepts the same feature format
- Update feature descriptions in the UI

## 📈 Future Enhancements

- [ ] User authentication system
- [ ] Model explainability (SHAP, feature importance)
- [ ] Database integration for prediction logging
- [ ] API endpoints for external integration
- [ ] Advanced analytics dashboard
- [ ] Multi-model comparison

## 📄 License

This project is created for educational and portfolio purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**SalarySense · Built with ❤️ by Waleedul Haque · Powered by Streamlit & scikit-learn**
