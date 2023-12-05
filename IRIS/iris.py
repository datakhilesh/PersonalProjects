pip install --upgrade --force-reinstall seaborn
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Iris dataset
iris = sns.load_dataset('iris')

# Streamlit app title
st.title('Iris Dataset Visualization')

# Select features for plotting
feature_x = st.selectbox('Select X-axis feature:', iris.columns[:-1])
feature_y = st.selectbox('Select Y-axis feature:', iris.columns[:-1])

# Scatter plot based on user-selected features
fig, ax = plt.subplots()
sns.scatterplot(data=iris, x=feature_x, y=feature_y, hue='species', ax=ax)
ax.set_title(f'{feature_x} vs {feature_y}')
st.pyplot(fig)
