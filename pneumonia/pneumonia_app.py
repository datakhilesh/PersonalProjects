import streamlit as st
import cv2
import numpy as np
from keras.preprocessing import image
from tensorflow import keras
from keras.applications.vgg16 import preprocess_input

# Load the trained model
model = keras.models.load_model('chest_xray.h5')

def classify_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_data = preprocess_input(img_array)
    result = model.predict(img_data)
    return result

def main():
    st.title("Pneumonia Detection App")
    st.write("Upload a chest X-ray image to check for pneumonia.")

    uploaded_file = st.file_uploader("Choose a chest X-ray image...", type="jpg")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

        # Save the uploaded image temporarily
        temp_img_path = "temp_image.jpg"
        with open(temp_img_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Make prediction
        result = classify_image(temp_img_path)
        st.write("Prediction Result:")
        if result[0][0] == 0:
            st.error("Person is Affected By PNEUMONIA")
        else:
            st.success("Result is Normal")

if __name__ == '__main__':
    main()
