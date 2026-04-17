# 📊 Poll Results Visualizer

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-FF4B4B.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458.svg)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557c.svg)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Transform survey and poll data into actionable insights with interactive visualizations and automated reporting.

## 🎯 Overview

**Poll Results Visualizer** is a comprehensive data analysis and visualization tool that converts raw poll/survey responses into meaningful insights. It automates the entire data pipeline from data generation to visualization, making it perfect for understanding public opinion, customer feedback, and survey results.

## ✨ Features

### 📊 Data Processing
- ✅ Synthetic poll data generation (500+ realistic responses)
- ✅ Automatic data cleaning and preprocessing
- ✅ Missing value handling & duplicate removal
- ✅ Text standardization & feature engineering

### 📈 Analysis Capabilities
- ✅ Vote share/percentage calculation
- ✅ Demographic analysis (region, age, gender, occupation)
- ✅ Satisfaction scoring & trend analysis
- ✅ Temporal pattern detection
- ✅ Correlation analysis

### 🎨 Visualizations
- ✅ Bar charts for categorical data
- ✅ Pie charts for percentage distribution
- ✅ Stacked bar charts for demographic comparisons
- ✅ Histograms for satisfaction ratings
- ✅ Line charts for temporal trends
- ✅ Word clouds for text feedback
- ✅ Interactive Plotly dashboard

### 📋 Output Formats
- ✅ High-resolution PNG images
- ✅ Interactive HTML dashboard
- ✅ CSV exports of cleaned data
- ✅ Text insights report
- ✅ Summary statistics

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| **Language** | Python 3.11+ |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly, WordCloud |
| **Web Dashboard** | Streamlit |
| **Analysis** | Scikit-learn |
| **Environment** | VS Code / Jupyter |

## 📁 Project Structure
Poll-Results-Visualizer/
│
├── data/
│ ├── poll_data.csv # Raw synthetic data
│ └── cleaned_poll_data.csv # Processed data
│
├── src/
│ ├── init.py
│ ├── data_generator.py # Synthetic data generation
│ ├── data_cleaner.py # Data preprocessing
│ ├── analysis.py # Statistical analysis
│ ├── visualizations.py # Chart generation
│ └── insights.py # Insight generation
│
├── outputs/
│ ├── bar_chart_.png # Visualization charts
│ ├── pie_chart_.png
│ ├── satisfaction_histogram.png
│ ├── wordcloud.png
│ ├── interactive_dashboard.html
│ ├── insights_report.txt
│ └── summary_statistics.csv
│
├── images/ # Screenshots for documentation
│
├── app.py # Streamlit dashboard
├── main.py # Complete pipeline runner
├── requirements.txt # Python dependencies
├── .gitignore # Git ignore file
└── README.md # Project documentation