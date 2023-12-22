from altair.vegalite import Data
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
# Streamlit app
st.title('Energy Performance Model')


# Assuming you have an image file named 'default_image.png'
default_image_path = 'icon.png'

# Streamlit app
#st.title('Image Display App')



# Load the trained Decision Tree model using pickle
with open('best_decision_tree_model.pkl', 'rb') as file:
    best_tree_reg = pickle.load(file)

#insurance/insure.py
data = pd.read_csv('energy.csv')

show_data = st.sidebar.checkbox("Raw Data")
# Display selected visualizations
if show_data:

  with st.expander("Dataset Preview"):
    st.dataframe(data)

  with st.expander("Dataset Describe"):
    st.dataframe(data.describe())


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

# Function to predict 'Y1' and 'Y2' based on user input
def predict_energy_performance(x1, x2, x3, x4, x5, x6, x7, x8):
    # Create a DataFrame with user input
    user_input = pd.DataFrame({
        'X1': [x1],
        'X2': [x2],
        'X3': [x3],
        'X4': [x4],
        'X5': [x5],
        'X6': [x6],
        'X7': [x7],
        'X8': [x8]
    })

    # Predict 'Y1' and 'Y2'
    predictions = best_tree_reg.predict(user_input)

    return predictions[0, 0], predictions[0, 1]

# Streamlit app
#st.title('Energy Performance Prediction')
# Checkbox for prediction
predict_checkbox = st.sidebar.checkbox('Predict Energy Performance')

if predict_checkbox:
  # User input for feature values
  x1 = st.slider('Relative Compactness (X1)', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
  x2 = st.slider('Surface Area (X2)', min_value=500.0, max_value=1000.0, value=750.0, step=1.0)
  x3 = st.slider('Wall Area (X3)', min_value=300.0, max_value=400.0, value=350.0, step=1.0)
  x4 = st.slider('Roof Area (X4)', min_value=100.0, max_value=200.0, value=150.0, step=1.0)
  x5 = st.slider('Overall Height (X5)', min_value=3.0, max_value=10.0, value=6.0, step=0.1)
  x6 = st.selectbox('Orientation (X6)', [2, 3, 4, 5])
  x7 = st.slider('Glazing Area (X7)', min_value=0.0, max_value=1.0, value=0.5, step=0.01)
  x8 = st.slider('Glazing Area Distribution (X8)', min_value=0, max_value=5, value=3, step=1)

  # Predict 'Y1' and 'Y2'
  y1_pred, y2_pred = predict_energy_performance(x1, x2, x3, x4, x5, x6, x7, x8)

  # Display the predicted values
  st.subheader('Predicted Energy Performance:')
  st.write(f'Y1: {y1_pred:.2f}')
  st.write(f'Y2: {y2_pred:.2f}')


predict_visuals = st.sidebar.checkbox('Cool Correlation Visuals')

if predict_visuals:

    # Scatter plot for X1 vs y1
    fig, ax = plt.subplots()
    sns.scatterplot(x='X1', y='Y1', data=data, ax=ax)
    st.pyplot(fig)
    fig.savefig('scatter_x1_y1.png')

      # Scatter plot for X1 vs y2
    fig, ax = plt.subplots()
    sns.scatterplot(x='X1', y='Y2', data=data, ax=ax)
    st.pyplot(fig)
    fig.savefig('scatter_x1_y2.png')

      # Scatter plot for X5 vs y1
    fig, ax = plt.subplots()
    sns.scatterplot(x='X5', y='Y1', data=data, ax=ax)
    st.pyplot(fig)
    fig.savefig('scatter_x5_y1.png')

      # Scatter plot for X5 vs y2
    fig, ax = plt.subplots()
    sns.scatterplot(x='X5', y='Y2', data=data, ax=ax)
    st.pyplot(fig)
    fig.savefig('scatter_x5_y2.png')

      # Scatter plot for X8 vs y1
    fig, ax = plt.subplots()
    sns.scatterplot(x='X8', y='Y1', data=data, ax=ax)
    st.pyplot(fig)
    fig.savefig('scatter_x8_y1.png')

      # Scatter plot for X8 vs y2
    fig, ax = plt.subplots()
    sns.scatterplot(x='X8', y='Y2', data=data, ax=ax)
    st.pyplot(fig)
    fig.savefig('scatter_x8_y2.png')





# Check if no checkboxes are selected
if not predict_visuals and not predict_checkbox and not show_heatmap and not show_data:
    st.image(default_image_path, caption='Default Image')
    with st.expander("Dataset Description"):
      # Display information about the dataset
      st.header('About the Dataset')
      st.write("""
      The dataset was created by Angeliki Xifara (angxifara '@' gmail.com, Civil/Structural Engineer)
      and was processed by Athanasios Tsanas (tsanasthanasis '@' gmail.com, Oxford Centre for Industrial and Applied Mathematics, University of Oxford, UK).

      ### Data Set Information:

      We perform energy analysis using 12 different building shapes simulated in Ecotect.
      The buildings differ with respect to the glazing area, the glazing area distribution, and the orientation, amongst other parameters.
      We simulate various settings as functions of the afore-mentioned characteristics to obtain 768 building shapes.
      The dataset comprises 768 samples and 8 features, aiming to predict two real-valued responses.
      It can also be used as a multi-class classification problem if the response is rounded to the nearest integer.

      ### Attribute Information:

      The dataset contains eight attributes (or features, denoted by X1…X8) and two responses (or outcomes, denoted by y1 and y2).
      The aim is to use the eight features to predict each of the two responses.

      Specifically:
      - X1 Relative Compactness
      - X2 Surface Area
      - X3 Wall Area
      - X4 Roof Area
      - X5 Overall Height
      - X6 Orientation
      - X7 Glazing Area
      - X8 Glazing Area Distribution
      - y1 Heating Load
      - y2 Cooling Load
      """)
