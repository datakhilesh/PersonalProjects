
import streamlit as st
import pickle
import numpy as np

# Load the model from the .pkl file
with open("iris_model.pkl", "rb") as model_file:
    loaded_model = pickle.load(model_file)

# Streamlit UI
st.title("Iris Flower Prediction App")
st.sidebar.header("Input Features")

# Collect user input features
user_input = []
for i in range(4):
    feature_value = st.sidebar.slider(f"Feature {i+1}", 0.0, 7.0, 3.0)
    user_input.append(feature_value)

# Convert user input to numpy array
input_array = np.array(user_input).reshape(1, -1)

# Make predictions using the loaded model
prediction = loaded_model.predict(input_array)
prediction_proba = loaded_model.predict_proba(input_array)

# Display results
st.subheader("Prediction:")
st.write(f"The model predicts: {prediction[0]}")

st.subheader("Prediction Probabilities:")
for i, class_label in enumerate(loaded_model.classes_):
    st.write(f"{class_label}: {prediction_proba[0][i]:.4f}")
