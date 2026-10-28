
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Stock Trend Analysis",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stMetric"] {
        background-color: #151f32;
        border: 1px solid #26354d;
        padding: 20px;
        border-radius: 12px;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc;
    }
    h1, h2, h3 {
        color: #f8fafc;
    }
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }
</style>
""", unsafe_allow_html=True)

st.title("📈 Stock Trend Analysis Tool")

st.caption(
    "Analyze historical stock prices, price movements "
    "and technical indicators."
)

st.divider()

st.sidebar.title("⚙️ Dashboard Settings")

symbol = st.sidebar.text_input(
    "Stock Symbol",
    value="TCS.NS"
).strip().upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
    index=3
)

st.sidebar.info(
    "Examples: TCS.NS, RELIANCE.NS, INFY.NS, AAPL, MSFT"
)

analyze = st.sidebar.button(
    "🔍 Analyze Stock",
    use_container_width=True
)

if analyze:

    if not symbol:
        st.error("Please enter a stock symbol.")
        st.stop()

    with st.spinner("Fetching stock market data..."):
        try:
            data = yf.download(
                symbol,
                period=period,
                interval="1d",
                auto_adjust=True,
                progress=False
            )
        except Exception as error:
            st.error(f"Unable to download data: {error}")
            st.stop()

    if data.empty:
        st.error(
            "No stock data found. Please check the symbol "
            "or try again later."
        )
        st.stop()

    close_prices = data["Close"]

    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]

    close_prices = pd.to_numeric(
        close_prices,
        errors="coerce"
    ).dropna()

    if close_prices.empty:
        st.error("No valid closing prices are available.")
        st.stop()

    analysis = pd.DataFrame(index=close_prices.index)

    analysis["Close"] = close_prices
    analysis["MA20"] = close_prices.rolling(20).mean()
    analysis["MA50"] = close_prices.rolling(50).mean()
    analysis["Daily Return"] = close_prices.pct_change() * 100

    delta = close_prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    average_gain = gain.ewm(
        alpha=1 / 14,
        min_periods=14,
        adjust=False
    ).mean()

    average_loss = loss.ewm(
        alpha=1 / 14,
        min_periods=14,
        adjust=False
    ).mean()

    rs = average_gain / average_loss

    analysis["RSI"] = 100 - (100 / (1 + rs))

    ma20_latest = analysis["MA20"].iloc[-1]
    ma50_latest = analysis["MA50"].iloc[-1]

    if pd.isna(ma20_latest) or pd.isna(ma50_latest):
        signal = "Not Enough Data"
    elif ma20_latest > ma50_latest:
        signal = "BUY"
    elif ma20_latest < ma50_latest:
        signal = "SELL"
    else:
        signal = "HOLD"

    latest = close_prices.iloc[-1]

    previous = (
        close_prices.iloc[-2]
        if len(close_prices) > 1
        else latest
    )

    change = latest - previous

    change_pct = (
        (change / previous) * 100
        if previous != 0
        else 0
    )

    highest = close_prices.max()
    lowest = close_prices.min()

    if latest > previous:
        trend = "📈 Upward"
    elif latest < previous:
        trend = "📉 Downward"
    else:
        trend = "➡️ No Change"

    st.subheader(f"📊 Market Overview: {symbol}")
    st.subheader("🤖 Technical Signal")

    if signal == "BUY":
        st.success("🟢 BUY — MA20 is above MA50")
    elif signal == "SELL":
        st.error("🔴 SELL — MA20 is below MA50")
    elif signal == "HOLD":
        st.warning("🟡 HOLD — Both moving averages are equal")
    else:
        st.info("Not enough historical data to generate a signal")

    st.caption(
        f"Period: {period} | Latest available observation: "
        f"{close_prices.index[-1].strftime('%d %b %Y')}"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Latest Price",
        f"₹{latest:,.2f}",
        f"{change:+,.2f} ({change_pct:+.2f}%)"
    )

    c2.metric("Highest Price", f"₹{highest:,.2f}")
    c3.metric("Lowest Price", f"₹{lowest:,.2f}")
    c4.metric("Latest Daily Trend", trend)

    st.divider()

    st.subheader("📈 Stock Price Movement")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=analysis.index,
            y=analysis["Close"],
            name="Closing Price",
            mode="lines",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#111827",
        height=430,
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode="x unified",
        legend=dict(orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📉 Moving Average Analysis")

    ma_fig = go.Figure()

    ma_fig.add_trace(
        go.Scatter(
            x=analysis.index,
            y=analysis["Close"],
            name="Closing Price",
            mode="lines"
        )
    )

    ma_fig.add_trace(
        go.Scatter(
            x=analysis.index,
            y=analysis["MA20"],
            name="MA20",
            mode="lines"
        )
    )

    ma_fig.add_trace(
        go.Scatter(
            x=analysis.index,
            y=analysis["MA50"],
            name="MA50",
            mode="lines"
        )
    )

    ma_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#111827",
        height=430,
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        hovermode="x unified",
        legend=dict(orientation="h")
    )

    st.plotly_chart(ma_fig, use_container_width=True)

    st.subheader("📊 Relative Strength Index (RSI)")

    latest_rsi = analysis["RSI"].iloc[-1]

    if pd.isna(latest_rsi):
        st.info("Not enough data to calculate RSI.")
    else:
        rsi_col1, rsi_col2 = st.columns(2)

        rsi_col1.metric("Latest RSI", f"{latest_rsi:.2f}")

        if latest_rsi > 70:
            rsi_col2.metric("RSI Status", "Overbought")
        elif latest_rsi < 30:
            rsi_col2.metric("RSI Status", "Oversold")
        else:
            rsi_col2.metric("RSI Status", "Neutral Range")

        rsi_fig = go.Figure()

        rsi_fig.add_trace(
            go.Scatter(
                x=analysis.index,
                y=analysis["RSI"],
                name="RSI",
                mode="lines"
            )
        )

        rsi_fig.add_hline(y=70, line_dash="dash")
        rsi_fig.add_hline(y=30, line_dash="dash")

        rsi_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#111827",
            height=350,
            xaxis_title="Date",
            yaxis_title="RSI",
            yaxis_range=[0, 100],
            showlegend=False
        )

        st.plotly_chart(rsi_fig, use_container_width=True)

    st.subheader("📊 Daily Returns")

    returns = analysis["Daily Return"].dropna()

    if not returns.empty:
        return_fig = go.Figure()

        return_fig.add_trace(
            go.Bar(
                x=returns.index,
                y=returns,
                name="Daily Return"
            )
        )

        return_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#111827",
            height=300,
            xaxis_title="Date",
            yaxis_title="Return (%)",
            showlegend=False
        )

        st.plotly_chart(return_fig, use_container_width=True)

    st.subheader("🔮 Stock Price Prediction")

    prediction_data = analysis[["Close"]].dropna().copy()

    if len(prediction_data) >= 30:

        prediction_data["Day"] = range(len(prediction_data))

        X = prediction_data[["Day"]]
        y = prediction_data["Close"]

        split_index = int(len(prediction_data) * 0.8)

        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]

        y_train = y.iloc[:split_index]
        y_test = y.iloc[split_index:]

        accuracy_model = LinearRegression()
        accuracy_model.fit(X_train, y_train)

        test_predictions = accuracy_model.predict(X_test)

        mae = float(abs(y_test - test_predictions).mean())

        nonzero_actual = y_test != 0

        if nonzero_actual.any():
            mape = float(
                (
                    abs(
                        (
                            y_test[nonzero_actual]
                            - test_predictions[nonzero_actual.to_numpy()]
                        )
                        / y_test[nonzero_actual]
                    ).mean()
                    * 100
                )
            )
        else:
            mape = float("nan")

        st.subheader("🎯 Prediction Accuracy")

        acc1, acc2 = st.columns(2)

        acc1.metric("Mean Absolute Error (MAE)", f"₹{mae:.2f}")

        if pd.notna(mape):
            acc2.metric(
                "Mean Absolute Percentage Error (MAPE)",
                f"{mape:.2f}%"
            )
        else:
            acc2.metric("Mean Absolute Percentage Error (MAPE)", "N/A")

        st.caption(
            "Metrics show performance on historical test data. "
            "They do not guarantee future prediction accuracy."
        )

        prediction_data["Day"] = range(len(prediction_data))

        X_all = prediction_data[["Day"]]
        y_all = prediction_data["Close"]

        final_model = LinearRegression()
        final_model.fit(X_all, y_all)

        future_days = pd.DataFrame({
            "Day": range(
                len(prediction_data),
                len(prediction_data) + 7
            )
        })

        predicted_prices = final_model.predict(future_days[["Day"]])

        future_dates = pd.bdate_range(
            start=prediction_data.index[-1] + pd.Timedelta(days=1),
            periods=7
        )

        prediction_df = pd.DataFrame({
            "Date": future_dates,
            "Predicted Price": predicted_prices
        })

        st.info(
            "These are simple Linear Regression estimates based on "
            "historical prices, not guaranteed future prices."
        )

        prediction_fig = go.Figure()

        prediction_fig.add_trace(
            go.Scatter(
                x=prediction_data.index,
                y=prediction_data["Close"],
                mode="lines",
                name="Historical Price"
            )
        )

        prediction_fig.add_trace(
            go.Scatter(
                x=prediction_df["Date"],
                y=prediction_df["Predicted Price"],
                mode="lines+markers",
                name="Predicted Price",
                line=dict(dash="dash")
            )
        )

        prediction_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#111827",
            height=400,
            xaxis_title="Date",
            yaxis_title="Stock Price (₹)",
            hovermode="x unified"
        )

        st.plotly_chart(prediction_fig, use_container_width=True)

        st.subheader("📋 Predicted Prices")

        st.dataframe(
            prediction_df.style.format({
                "Predicted Price": "₹{:.2f}"
            }),
            use_container_width=True
        )

    else:
        st.info(
            "Prediction aur accuracy calculate karne ke liye "
            "kam se kam 30 historical price records chahiye. "
            "Sidebar mein 3mo, 6mo ya 1y select karke try karein."
        )

    with st.expander("📋 View Historical Stock Data"):
        st.dataframe(
            data.sort_index(ascending=False),
            use_container_width=True
        )

    csv_data = data.to_csv().encode("utf-8")

    st.download_button(
        label="⬇️ Download Historical Data (CSV)",
        data=csv_data,
        file_name=f"{symbol}_stock_data.csv",
        mime="text/csv"
    )

    st.success("Stock analysis completed successfully!")

    st.caption(
        "This dashboard analyzes historical market data and does not "
        "guarantee future price movements or returns."
    )

else:
    st.info(
        "👈 Enter a stock symbol in the sidebar and click "
        "'Analyze Stock' to view the dashboard."
    )

    st.markdown("""
    ### 🚀 Dashboard Features

    - Historical stock price visualization
    - Latest price and daily price change
    - Highest and lowest recorded closing prices
    - 20-day and 50-day moving averages
    - RSI indicator
    - Daily percentage returns
    - Linear Regression price estimates
    - Historical prediction error metrics
    - Downloadable historical data
    """)

