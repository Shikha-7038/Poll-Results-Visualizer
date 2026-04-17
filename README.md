# 📊 Poll Results Visualizer

[![Python](https://img.shields.io/badge/Python-3.15-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

The **Poll Results Visualizer** is a comprehensive data analysis and visualization tool that transforms raw poll/survey data into actionable insights. It automates the entire data pipeline from data generation to visualization, making it perfect for understanding public opinion, customer feedback, and survey results.

## 🔍 Problem Statement

Organizations collect thousands of poll responses but struggle to:
- Extract meaningful insights from raw data
- Visualize results in an engaging way
- Make data-driven decisions quickly
- Share results with stakeholders effectively

## 💡 Solution

This project provides an end-to-end solution that:
- Generates realistic synthetic poll data (or imports real data)
- Cleans and preprocesses responses automatically
- Performs comprehensive statistical analysis
- Creates professional visualizations (bar charts, pie charts, stacked charts, word clouds)
- Generates actionable insights and recommendations
- Deploys an interactive dashboard for real-time exploration

## ✨ Features

### Data Processing
- ✅ Synthetic poll data generation (500+ responses)
- ✅ Automatic data cleaning and preprocessing
- ✅ Missing value handling
- ✅ Duplicate removal
- ✅ Text standardization
- ✅ Feature engineering

### Analysis Capabilities
- ✅ Vote share/percentage calculation
- ✅ Demographic analysis (region, age, gender, occupation)
- ✅ Satisfaction scoring
- ✅ Temporal trend analysis
- ✅ Correlation analysis
- ✅ Comparative insights

### Visualizations
- ✅ Bar charts for categorical data
- ✅ Pie charts for percentage distribution
- ✅ Stacked bar charts for demographic comparisons
- ✅ Histograms for satisfaction ratings
- ✅ Line charts for temporal trends
- ✅ Word clouds for text feedback
- ✅ Boxplots for distribution analysis
- ✅ Interactive Plotly dashboard

### Output Formats
- ✅ Static PNG images (high resolution)
- ✅ Interactive HTML dashboard
- ✅ CSV exports of cleaned data
- ✅ Text insights report
- ✅ Summary statistics

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Language | Python 3.15 |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly, WordCloud |
| Web Dashboard | Streamlit |
| Analysis | Scikit-learn |
| Environment | VS Code / Jupyter |

## 📁 Project Structure
Poll-Results-Visualizer/
│
├── data/                       # Generated and cleaned data
│   ├── poll_data.csv          # Raw synthetic data
│   └── cleaned_poll_data.csv  # Processed data
│
├── src/                        # Source code modules
│   ├── data_generator.py      # Synthetic data generation
│   ├── data_cleaner.py        # Data preprocessing
│   ├── analysis.py            # Statistical analysis
│   ├── visualizations.py      # Chart generation
│   └── insights.py            # Insight generation
│
├── outputs/                    # Generated outputs
│   ├── *.png                  # Visualization charts
│   ├── interactive_dashboard.html
│   ├── insights_report.txt
│   └── summary_statistics.csv
│
├── images/                     # Screenshots for documentation
├── app.py                      # Streamlit dashboard
├── main.py                     # Complete pipeline runner
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

🚀 Installation
Prerequisites
Python 3.11 or higher

pip package manager

Git (optional, for cloning)