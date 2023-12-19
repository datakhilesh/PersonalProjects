import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

# Set the start date and today's date
START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

# Streamlit app title
st.title('Stock Price Prediction App')

# Stock selection dropdown
stocks = {'GOOGL': 'GOOGL', 'AAPL': 'AAPL', 'AMZN': 'AMZN'}
selected_stock = st.selectbox('Select stock for prediction', list(stocks.keys()))

# Number of years for prediction
n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

# Function to load stock data
@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

# Load stock data
data_load_state = st.text('Loading data...')
data = load_data(stocks[selected_stock])
data_load_state.text('Loading data... done!')

# Display raw data
st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="Stock Open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Stock Close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

# Display raw data plot
plot_raw_data()

# Predict forecast with Prophet
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

# Show and plot forecast
st.subheader('Forecast data')
st.write(forecast.tail())

st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
