import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import streamlit as st
import platform
import sys

print("Python Version:", sys.version)
print("Platform:", platform.platform())
# ... print other relevant information about your environment
# Collect user input for four numbers using sliders
number1 = st.sidebar.slider("Number 1", 0.0, 10.0, 5.0)
number2 = st.sidebar.slider("Number 2", 0.0, 10.0, 5.0)
number3 = st.sidebar.slider("Number 3", 0.0, 10.0, 5.0)
number4 = st.sidebar.slider("Number 4", 0.0, 10.0, 5.0)

# Organize user input into a nested list
nested_list = [[number1, number2, number3, number4]]
#load_clf = pickle.load(open("IRIS/iris_model.pkl", 'rb'))


import seaborn as sns
import matplotlib.pyplot as plt
#from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()
data = iris.data
target = iris.target
feature_names = iris.feature_names

# Streamlit UI
st.title("Iris Dataset Visualization")
st.sidebar.header("Visualization Settings")

# Checkbox for heatmap
show_heatmap = st.sidebar.checkbox("Show Heatmap")

# Checkbox for scatter plot
show_scatter_plot = st.sidebar.checkbox("Show Scatter Plot")

# Display selected visualizations
if show_heatmap:
    st.subheader("Correlation Heatmap")
    correlation_matrix = sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
    st.pyplot()

if show_scatter_plot:
    st.subheader("Scatter Plot")
    selected_feature = st.sidebar.selectbox("Select Feature for X-axis", feature_names)
    sns.scatterplot(x=data[:, feature_names.index(selected_feature)], y=target, hue=target)
    plt.xlabel(selected_feature)
    plt.ylabel("Target")
    st.pyplot()

try:
    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target

    # Load the model
    with open('IRIS/iris_mod.pkl', 'rb') as model_file:
        clf = pickle.load(model_file)
        gg = [[2.0,3.4,2.4,3.6]]
        ff = clf.predict(nested_list)
        if ff == 0:
            st.write('sucks')
        elif ff == 1:
            st.write('dumbass')
        else:
            st.write('lame')
        st.write(ff)
        

    st.write("Model loaded successfully")

except Exception as e:
    st.write("Error loading the model: {e}")
