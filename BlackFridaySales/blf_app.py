import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

#import os
#print(os.getcwd())

# Load the data
train = pd.read_csv('c:/Users/Akhilesh Datar/Desktop/blackFriday/train.csv')
test = pd.read_csv('c:/Users/Akhilesh Datar/Desktop/blackFriday/test.csv')

def prepare(*args):
    for df in args:
        # Dropping columns with more than 50% null values
        thresh = len(df) * 0.5
        df.dropna(thresh=thresh, axis=1, inplace=True)
        
        # Filling nulls with the mean for 'Product_Category_2'
        df['Product_Category_2'] = df['Product_Category_2'].fillna(df['Product_Category_2'].mean())
        
        # Making 'Marital_Status' column into bool
        df['Marital_Status'] = df['Marital_Status'].astype('bool')

prepare(train, test)

# Sample data for training
df = train.sample(n=100000)
true_test = test.sample(n=10000)

# Features
features = ['Gender', 'Age', 'Occupation', 'City_Category',
            'Stay_In_Current_City_Years', 'Marital_Status',
            'Product_Category_1', 'Product_Category_2']

X = pd.get_dummies(train[features])
y = train.Purchase

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

# Train a Random Forest model
rf2 = RandomForestRegressor(random_state=1)
rf2.fit(X_train, y_train)

# Make predictions on the test set
y_pred = rf2.predict(X_test)

# Evaluate the model
def rf_score(test, prediction):
    mse = metrics.mean_squared_error(test, prediction)
    rmse = metrics.mean_squared_error(test, prediction, squared=False)
    mae = metrics.mean_absolute_error(test, prediction)
    medae = metrics.median_absolute_error(test, prediction)
    mape = metrics.mean_absolute_percentage_error(test, prediction)

    st.write(f"Mean Squared Error (MSE): {mse}")
    st.write(f"Root Mean Squared Error (RMSE): {rmse}")
    st.write(f"Mean Absolute Error (MAE): {mae}")
    st.write(f"Median Absolute Error (MEDAE): {medae}")
    st.write(f"Mean Absolute Percentage Error: {mape}")
    st.write(f'Test variance: {np.var(y_test)}')

rf_score(y_test, y_pred)

# Train the model on the entire dataset
rf2.fit(X, y)

# Make predictions on the test dataset
test_df_pred = rf2.predict(pd.get_dummies(test[features]))
test_df_pred = pd.DataFrame({'Purchase': test_df_pred})

# Concatenate the predictions with the original test dataset
final_df = pd.concat([test, test_df_pred], axis=1)

# Display the first 4 rows of the final DataFrame
st.write(final_df.head(4))
