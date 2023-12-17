# app.py
import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Function for forecasting using Holt-Winters method
def forecast(data, forecast_period=10):
    model = ExponentialSmoothing(data, seasonal='add', seasonal_periods=12)
    fitted_model = model.fit()
    forecast_values = fitted_model.forecast(steps=forecast_period)
    return forecast_values

# Streamlit app
def main():
    st.title("Time Series Forecasting App")

    # CSV URL input
    csv_url = st.text_input("Enter the CSV URL:", "https://raw.githubusercontent.com/datasets/covid-19/main/data/time-series-19-covid-combined.csv")

    if csv_url:
        try:
            # Load data from CSV URL
            data = pd.read_csv(csv_url)
            st.subheader("Data Loaded from CSV URL:")
            st.write(data.head())

            # Visualization
            st.subheader("Time Series Visualization:")
            st.line_chart(data.set_index('Date'))

            # Forecasting
            st.subheader("Time Series Forecasting:")
            forecast_period = st.number_input("Enter the number of periods to forecast:", min_value=1, value=10)

            if st.button("Generate Forecast"):
                st.info("Forecasting in progress...")
                try:
                    # Extract time series data
                    time_series_data = data.set_index('Date').iloc[:, 0]

                    # Perform forecasting
                    forecast_values = forecast(time_series_data, forecast_period)

                    # Display forecast
                    st.line_chart(pd.Series(forecast_values, index=pd.date_range(start=time_series_data.index[-1], periods=forecast_period + 1)[1:]))
                    st.success("Forecast generated successfully!")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        except Exception as e:
            st.error(f"Error loading data from CSV URL: {e}")

if __name__ == "__main__":
    main()
