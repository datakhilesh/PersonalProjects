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

#"C:\Users\Akhilesh Datar\Desktop\streamlit\sentiment\diamonds.csv"


df = pd.read_csv("C:/Users/Akhilesh Datar/Desktop/streamlit/sentiment/diamonds.csv")
st.write("shape: ", df.shape)
st.dataframe(df)

df.drop(["Unnamed: 0"], axis=1,inplace=True)
st.dataframe(df)

object_cols = df.select_dtypes(include='object').columns.tolist()
st.write("Categorical variables:")
st.write(object_cols)

st.title("Count Plots for Categorical Columns")

for c in object_cols:
    st.subheader(f"Count Plot of {c}")
    
    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    ax = sns.countplot(x=df[c], palette="Set3")
    
    # Add count annotations on top of the bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='baseline', fontsize=10, color='black', xytext=(0, 5),
                    textcoords='offset points')

    plt.title(f'Count Plot of {c}', fontsize=14)
    
    # Display the plot using Streamlit
    st.pyplot(plt)
    
    # Display value counts and separator
    st.write(df[c].value_counts())
    st.write("-" * 25)


label_encoder = LabelEncoder()
for col in object_cols:
    df[col] = label_encoder.fit_transform(df[col])



st.title("Correlation Heatmap")

plt.figure(figsize=(10, 7))
sns.heatmap(df.corr(), annot=True, cmap="flare")
plt.title("Correlation Heatmap", fontsize=16)

# Display the heatmap using Streamlit
st.pyplot(plt)

st.write(df)


X = df.drop("price", axis = "columns")
Y = df["price"]

st.write(X,Y)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.25, random_state=42)
st.title(X_train.shape)
st.title(X_test.shape)
st.title(Y_train.shape)
st.title(Y_test.shape)


regressors = [
    ("Linear Regression", LinearRegression()),
    ("Ridge Regression", Ridge()),
    ("Lasso Regression", Lasso()),
    ("Decision Tree Regression", DecisionTreeRegressor()),
    ("Random Forest Regression", RandomForestRegressor())
]

scalers = [
    ("Standard Scaler", StandardScaler()),
    ("MinMax Scaler", MinMaxScaler()),
    ("Robust Scaler", RobustScaler()),
    ("Quantile Transformer", QuantileTransformer()),
    ("Power Transformer", PowerTransformer())
]

results = []

for regressor_name, regressor in regressors:
    for scaler_name, scaler in scalers:
        pipeline = Pipeline([
            ('scaler', scaler),
            ('regressor', regressor)
        ])
        pipeline.fit(X_train, Y_train)
        Y_pred = pipeline.predict(X_test)
        r2     = r2_score(Y_test, Y_pred)
        mse = mean_squared_error(Y_test, Y_pred)
        rmse = np.sqrt(mse)
        results.append({
            'Regressor': regressor_name,
            'Scaler': scaler_name,
            'R2': r2,
            'MSE': mse,
            'RMSE': rmse
        })
        print(f"******** {regressor_name} + {scaler_name} ********")



results = pd.DataFrame(results)
st.dataframe(results)

best_r2_row         = results.loc[results['R2'].idxmax()]
best_result_mse     = results.loc[results['R2'] == best_r2_row['R2']].loc[results['MSE'].idxmin()]
best_result_rmse    = results.loc[results['R2'] == best_result_mse['R2']].loc[results['RMSE'].idxmin()]
st.write("\nBest Result:")
st.write
(best_result_rmse)


model  = Pipeline([('scaler',PowerTransformer()),('regressor',RandomForestRegressor())]).fit(X_train,Y_train)

# Saving the model
import pickle
pickle.dump(model, open('diamond_clf.pkl', 'wb'))