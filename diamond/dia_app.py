import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

import numpy             as np
import warnings

from sklearn.preprocessing   import (
    LabelEncoder,
    StandardScaler,
    MinMaxScaler,
    RobustScaler,
    QuantileTransformer,
    PowerTransformer
)
from sklearn.model_selection import train_test_split
from sklearn.linear_model    import (
    LinearRegression,
    Ridge,
    Lasso
)
from sklearn.tree           import DecisionTreeRegressor
from sklearn.ensemble       import RandomForestRegressor
from sklearn.metrics        import (
    mean_squared_error,
    r2_score,
    mean_squared_log_error
)

from sklearn.pipeline       import Pipeline
warnings.filterwarnings("ignore")

import pickle
from sklearn.ensemble import RandomForestClassifier

#import zipfile module
from zipfile import ZipFile

#import zipfile
 
#with zipfile.ZipFile("geekpython.zip", mode="r") as arch:
#    myzip = arch.getinfo("geek.txt")

#myzip = None
with ZipFile('diamond/diamond_clf.zip', 'r') as f:
    myZip = f.getInfo("diamond_clf.pkl")


    penguins_raw = pd.read_csv("diamond/diamonds.csv")
    raw = pd.read_csv("diamond/diamonds.csv")
    
    st.dataframe(raw)
    penguins = penguins_raw.drop(columns=['price','Unnamed: 0'])
    df = pd.concat([penguins],axis=0)
    #df = penguins_raw
    #df.drop(["Unnamed: 0"], axis=1,inplace=True)
    st.dataframe(df)
    
    #st.dataframe(df)
    
    st.title('Diabetes Prediction')
    
    # Split Columns
    col1, col2 = st.columns(2)
    
    with col1 :
      carat = st.number_input('Enter the Carat value')
    
    with col2 :
      cut = st.selectbox('Enter the Cut value', ('Good','Ideal', 'Premium', 'Very Good', 'Fair'))
     
    with col1 :
      color = st.selectbox('Enter the Color value', ('E','I','J','H'))
    
    with col2 :
      clarity = st.selectbox('Enter the clarity',('SI2','SI1','VS2','VS1'))
    
    with col1 :
      table = st.number_input('Enter the table value')
    
    with col2 :
      x = st.number_input('Enter the X value')
    
    with col1 :
      y = st.number_input('Enter the Y value')
    
    with col2 :
      z = st.number_input('Enter the Z value')
    
    with col1 :
      depth = st.number_input('Enter the depth value')
    
    
    data = {'carat':carat,
            'cut':cut,
            'color':color,
            'clarity':clarity,
            'depth':depth,
            'table':table,
            'x':x,
            'y':y,
            'z':z}
    
    features = pd.DataFrame(data,index=[0])
    
    new_df = pd.concat([features,df],axis=0)
    
    
    
    
    object_cols = df.select_dtypes(include='object').columns.tolist()
    label_encoder = LabelEncoder()
    for col in object_cols:
        df[col] = label_encoder.fit_transform(df[col])
        new_df[col] = label_encoder.fit_transform(new_df[col])
    
    new_df = new_df[:1]
    st.dataframe(new_df)    
    
    
    
    st.title("Correlation Heatmap")
    
    plt.figure(figsize=(10, 7))
    sns.heatmap(df.corr(), annot=True, cmap="flare")
    plt.title("Correlation Heatmap", fontsize=16)
    st.pyplot(plt)
    
    model_diabetes = pickle.load(open("diamond/diamond_clf.pkl", 'rb'))
    # Prediction
    diabetes_diagnosis = ''
    
    if st.button('Diabetes Prediction Test'):
      diabetes_prediction = model_diabetes.predict(new_df)
      st.write(diabetes_prediction)



