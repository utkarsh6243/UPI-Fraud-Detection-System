# UPI AI Shield - AI Powered UPI Fraud Detection System

An AI-powered UPI Fraud Detection System built using Machine Learning and Streamlit. The application predicts whether a UPI transaction is **Safe** or **Fraudulent** in real time while providing an interactive dashboard, analytics, secure authentication, and transaction history.
## Features

- Secure Login & User Authentication
- AI-Based Fraud Detection
- Fraud Probability Prediction
- Interactive Dashboard
- Analytics Dashboard with Visualizations
- Transaction History
- Search & Filter Transactions
- CSV Report Export
- Modern Enterprise UI
- SQLite Database Integration

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Plotly
- SQLite
- Joblib
- Streamlit Option Menu

## Project Structure

```
UPI-Fraud-Detection-System
│
├── assets/
├── components/
│   ├── analytics.py
│   ├── dashboard.py
│   ├── detect_fraud.py
│   └── __init__.py
│
├── data/
├── models/
│
├── app.py
├── auth.py
├── database.py
├── generate_dataset.py
├── train_model.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository
bash
git clone https://github.com/utkarsh6243/UPI-Fraud-Detection-System.git
```

### Open Project

```bash
cd UPI-Fraud-Detection-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## Application Modules

### Dashboard

- Live Transaction Overview
- Fraud Statistics
- Interactive Charts
- AI Monitoring

### Fraud Detection

- Predict Safe/Fraud Transaction
- Fraud Probability Score
- Instant AI Prediction

### Analytics

- Transaction Analysis
- Fraud Distribution
- Location Analysis
- Device Analysis
- Business Insights

### Transaction History

- View Previous Transactions
- Search by UPI ID
- Filter by Status
- Export CSV Reports

---

## Machine Learning

The fraud detection model is trained using supervised machine learning techniques to classify UPI transactions as either **Safe** or **Fraudulent** based on transaction attributes.

## Future Improvements

- Batch Fraud Prediction
- Explainable AI (SHAP)
- Email & SMS Alerts
- Cloud Deployment
- REST API Integration
- Multi-Factor Authentication
- Admin Panel
- Real-Time Monitoring
