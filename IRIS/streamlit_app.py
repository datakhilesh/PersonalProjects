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
load_clf = pickle.load(open("IRIS/iris_model.pkl", 'rb'))

try:
    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target

    # Load the model
    with open('IRIS/iris_model.pkl', 'rb') as model_file:
        clf = pickle.load(model_file)
        gg = [[2.0,3,4,2.4,3.6]]
        ff = clf.predict(gg)
        st.write(ff)

    st.write("Model loaded successfully")

except Exception as e:
    st.write("Error loading the model: {e}")
