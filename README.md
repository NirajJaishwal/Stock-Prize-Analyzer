# 📊 Stock Prize Analyzer

The **Stock Prize Analyzer** is a web-based application built with Flask and integrated with data science libraries like `yfinance`, `plotly`, and `pandas`. It allows users to search and visualize stock market data interactively. Perfect for investors, students, or anyone interested in analyzing historical stock prices. It uses the model trained using Deep Learning algorithm LSTM to process the sequential and time series data effectively.

---

## 🔥 Features

- 📈 Visualizes historical stock data using interactive Plotly graphs.
- 🔍 Allows input of stock ticker symbols (e.g., `AAPL`, `GOOGL`, `TSLA`).
- 📆 Supports date filtering to customize your analysis period.
- 🧠 Built-in integration with machine learning-ready libraries.
- 🌐 Deployed online using **Render** for easy access.

---

## 🚀 Live Demo

[Click here to try it out](https://stock-prize-analyzer-1.onrender.com/)

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, Bootstrap
- **Data Handling**: yFinance, Pandas, numpy
- **Machine Learning Model**: LSTM
- **Visualization**: Plotly Express
- **Deployment**: Render
- **Version Control**: Git + GitHub

---

## 📦 Installation

### 🧱 Prerequisites

- Python 3.8+
- Git

### 🧪 Local Setup

```bash
# Clone the repository
git clone https://github.com/NirajJaishwal/Stock-Prize-Analyzer.git
cd stock-prize-analyzer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
