# 📈 Stock Trend Analysis Tool

An interactive stock market analysis dashboard built using Python and Streamlit. This project helps users explore historical stock prices, visualize market trends, analyze technical indicators, and estimate future stock prices using Machine Learning.

## 🚀 Project Overview

The Stock Trend Analysis Tool provides a simple and interactive interface for analyzing historical stock market data. Users can explore price movements, understand technical indicators, compare moving averages, and view estimated prices for the next seven business days.

The project combines data analysis, visualization, and basic machine learning in one dashboard.

## ✨ Features

* **Historical Stock Data:** Retrieve and analyze historical stock prices.
* **Interactive Dashboard:** Explore stock market information through a Streamlit interface.
* **Stock Price Visualization:** View historical price movements using interactive charts.
* **Moving Average Analysis:** Analyze 20-day and 50-day moving averages (MA20 and MA50).
* **RSI Indicator:** Examine the Relative Strength Index to understand recent price momentum.
* **Daily Returns Analysis:** Visualize daily percentage changes in stock prices.
* **Stock Trend Indicators:** Display simple BUY, SELL, or HOLD signals based on moving-average comparisons.
* **Price Estimation:** Use Linear Regression to estimate prices for the next seven business days.
* **Model Evaluation:** Evaluate historical test predictions using Mean Absolute Error (MAE) and Mean Absolute Percentage Error (MAPE).
* **Historical Data Table:** View stock data in tabular format.
* **CSV Download:** Download historical stock data for further analysis.

## 🛠️ Technologies Used

| Technology   | Purpose                                 |
| ------------ | --------------------------------------- |
| Python       | Main programming language               |
| Streamlit    | Interactive web dashboard               |
| Pandas       | Data handling and analysis              |
| NumPy        | Numerical calculations                  |
| Plotly       | Interactive charts and visualizations   |
| yfinance     | Retrieving historical stock market data |
| Scikit-learn | Linear Regression and model evaluation  |

## 📂 Project Structure

```text
stock-trend-analysis-tool/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

Follow these steps to run the project on your local computer.

### 1. Clone the Repository

```bash
git clone https://github.com/sachin9367/stock-trend-analysis-tool.git
```

### 2. Open the Project Folder

```bash
cd stock-trend-analysis-tool
```

### 3. Create a Virtual Environment

**Windows:**

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows Command Prompt:**

```bash
venv\Scripts\activate
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the Application

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the dashboard.

## 📊 How to Use

1. Run the application.
2. Select a stock symbol from the available input options.
3. Choose the historical time period you want to analyze.
4. Review the latest, highest, and lowest stock prices.
5. Explore the price chart and technical indicators.
6. Review the price estimates and model evaluation metrics.
7. View or download the historical stock data as a CSV file.

**Note:** Stock symbols must be supported by the data provider. For Indian stocks, symbols such as `TCS.NS`, `RELIANCE.NS`, and `INFY.NS` may be used if supported by the application.

## 🤖 Machine Learning Approach

The project uses **Linear Regression** to estimate future stock prices based on historical price data.

Model evaluation uses historical test data and the following metrics:

* **MAE (Mean Absolute Error):** Measures the average absolute difference between actual and predicted prices.
* **MAPE (Mean Absolute Percentage Error):** Measures prediction error as a percentage, where actual values are nonzero.

These metrics describe performance on the selected historical test data. They do not guarantee the accuracy of future predictions.

## 🎯 Learning Outcomes

This project provides practical experience with:

* Python programming
* Data cleaning and analysis
* Exploratory data visualization
* Technical indicators and moving averages
* Basic machine learning
* Model evaluation
* Building interactive dashboards
* Managing Python dependencies
* Git and GitHub

## ⚠️ Limitations and Disclaimer

* Stock price estimates are based on historical data and a basic Linear Regression model.
* Actual market prices can differ significantly from estimated prices.
* BUY, SELL, and HOLD indicators are based on simple moving-average comparisons and are not personalized investment recommendations.
* Historical performance does not guarantee future results.
* This project is intended for educational and analytical purposes only. It should not be used as the sole basis for investment decisions.

## 👨‍💻 Author

**Sachin Kumar Thakur**

* GitHub: [@sachin9367](https://github.com/sachin9367)
* Project Repository: [Stock Trend Analysis Tool](https://github.com/sachin9367/stock-trend-analysis-tool)

---

⭐ If you find this project useful for learning, consider giving the repository a star.
