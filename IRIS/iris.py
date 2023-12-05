import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Streamlit app title
st.title('Iris Dataset Visualization')

# Load Iris dataset from CSV URL
iris_url = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
iris = pd.read_csv(iris_url)

# Display a preview of the dataset
st.subheader('Dataset Preview')
st.dataframe(iris.head())

# Visualization options
st.subheader('Visualization Options')

# Select features for scatter plot
feature_x = st.selectbox('Select X-axis feature:', iris.columns[:-1])
feature_y = st.selectbox('Select Y-axis feature:', iris.columns[:-1])

# Scatter plot based on user-selected features
fig, ax = plt.subplots()
for species, color in zip(iris['species'].unique(), ['red', 'green', 'blue']):
    species_data = iris[iris['species'] == species]
    ax.scatter(species_data[feature_x], species_data[feature_y], label=species, color=color)

ax.set_title(f'{feature_x} vs {feature_y}')
ax.set_xlabel(feature_x)
ax.set_ylabel(feature_y)
ax.legend()
st.pyplot(fig)
