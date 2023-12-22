import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing 
label_encoder = preprocessing.LabelEncoder() 
import numpy as np


# Title and Introduction
st.title("Factors Influencing Health Insurance Prices")
st.write("Many factors that affect how much you pay for health insurance are not within your control. Nonetheless, it's good to have an understanding of what they are.")

# Factors List
st.subheader("Factors Affecting Health Insurance Premiums")
factors_list = [
    "Age: Age of the primary beneficiary",
    "Sex: Gender of the insurance contractor (Female/Male)",
    "BMI: Body Mass Index, an objective index of body weight (kg / m^2)",
    "Children: Number of children covered by health insurance / Number of dependents",
    "Smoker: Smoking status",
    "Region: The beneficiary's residential area in the US (Northeast, Southeast, Southwest, Northwest)"]


# Display the factors list
for factor in factors_list:
    st.write(f"- {factor}")

# Conclusion
st.write("Understanding these factors can help you gain insights into how health insurance premiums are calculated.")

#insurance/insure.py
data = pd.read_csv('insurance/insurance.csv')

with st.expander("Dataset Preview"):
  st.dataframe(data)

with st.expander("Dataset Describe"):
  st.dataframe(data.describe())


# Checkbox for visualizations
show_visualizations = st.sidebar.checkbox("Show Visualizations")

if show_visualizations:
    st.subheader("Visualizations")

    # Barplot 1
    st.subheader("Barplot 1: Charges by Region and Children")
    fig1, ax1 = plt.subplots()
    sns.barplot(x='region', y='charges', hue='children', data=data, palette='cool', ax=ax1)
    st.pyplot(fig1)

    # Histogram
    st.subheader("Histogram: Charges Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(data=data, x='charges', kde=True, ax=ax2)
    st.pyplot(fig2)

    # Barplot 2
    st.subheader("Barplot 2: Charges by Region and Sex")
    fig3, ax3 = plt.subplots()
    sns.barplot(x='region', y='charges', hue='sex', data=data, palette='cool', ax=ax3)
    st.pyplot(fig3)


data['region']= label_encoder.fit_transform(data['region'])
data['sex']= label_encoder.fit_transform(data['sex'])
data['smoker']= label_encoder.fit_transform(data['smoker'])

# Checkbox for heatmap
show_heatmap = st.sidebar.checkbox("Show Heatmap")
# Display selected visualizations
if show_heatmap:
    st.subheader("Correlation Heatmap")
    
    # Calculate the correlation matrix
    correlation_matrix = data.corr()

    # Create a heatmap using seaborn
    heatmap_fig, ax = plt.subplots()
    sns.heatmap(correlation_matrix, annot=True, cmap="rocket", ax=ax)
    st.pyplot(heatmap_fig)


# Checkbox for predictions
show_predictions = st.sidebar.checkbox("Show Predictions")

# Display selected visualizations
if show_predictions:
  st.subheader("Predictions")
  age = st.slider("Enter age:", min_value=18, max_value=100, value=25)
  sex = st.radio("Select sex:", ['Female', 'Male'])
  bmi = st.number_input("Enter BMI:", min_value=10.0, max_value=50.0, value=25.0)
  children = st.slider("Enter number of children:", min_value=0, max_value=10, value=0)
  smoker = st.radio("Select smoker status:", ['Non-smoker', 'Smoker'])
  region = st.selectbox("Select region:", ['Southwest', 'Southeast', 'Northwest', 'Northeast'])

  # Convert user input to numerical values
  sex = 0 if sex == 'Female' else 1
  smoker = 0 if smoker == 'Non-smoker' else 1
  region_mapping = {'Southwest': 1, 'Southeast': 2, 'Northeast': 3, 'Northwest': 4}
  region = region_mapping[region]


# Make predictions on user input
  try:
      with open('insurance/your_model.pkl', 'rb') as model_file:
          loaded_model = pickle.load(model_file)
          st.write("Model Loaded")  # Display a message if the model is loaded successfully
          
          # Create a DataFrame from the user input
          user_input = pd.DataFrame({'age': [age], 'sex': [sex], 'bmi': [bmi], 'children': [children], 'smoker': [smoker], 'region': [region]})
          st.dataframe(user_input)
          
          # Make predictions using the loaded model
          predictions = loaded_model.predict(user_input)
          st.write(predictions)
  except Exception as e:
      st.error(f"Error loading the model: {e}")
      loaded_model = None  # Set loaded_model to None if there's an error loading the model

  # The rest of your Streamlit app can continue here
