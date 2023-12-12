# Import necessary libraries
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge,Lasso  # Add Ridge
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.dummy import DummyRegressor

# Main function to handle data upload or selection
def main():
    st.title("Streamlit EDA and ML Web App ")
    st.subheader("By Akhilesh Datar")

    # User input for data selection or upload
    data_option = st.sidebar.radio("Select Data Source:", ("Upload Data", "Select Sample Dataset"))

    # Handle data based on user choice
    if data_option == "Upload Data":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            # Load user-uploaded data
            df = pd.read_csv(uploaded_file)
            st.success("Data uploaded successfully!")
        else:
            st.info("Please upload a CSV file.")
            return
    else:
        # Load sample dataset from Seaborn
        selected_dataset = st.sidebar.selectbox("Select Sample Dataset:", ("tips", "titanic"))
        df = sns.load_dataset(selected_dataset)
        st.success(f"Loaded sample dataset: {selected_dataset}")

    # Display original data preview
    st.subheader("Original Data Preview")
    st.write(df.head())

    # Separate columns into categorical and numerical variables
    categorical_columns = df.select_dtypes(include=['category', 'object']).columns
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns

    # Ask the user for encoding method
    encoding_method = st.radio("Select Encoding Method:", ("Label Encoder", "One-Hot Encoder"))

    # Encode categorical variables based on the selected method
    if encoding_method == "Label Encoder":
        label_encoder = LabelEncoder()
        for col in categorical_columns:
            df[col] = label_encoder.fit_transform(df[col])
    elif encoding_method == "One-Hot Encoder":
        df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

    # Display encoded data preview
    st.subheader("Encoded Data Preview")
    st.write(df.head())

    # Display correlation matrix heatmap for numerical columns after encoding
    st.subheader("Correlation Matrix After Encoding")
    encoded_corr_matrix = df[numerical_columns].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(encoded_corr_matrix, annot=True, cmap='coolwarm', linewidths=.5, ax=ax)
    st.pyplot(fig)

    # Ask user if they want to perform EDA
    perform_eda = st.checkbox("Perform Exploratory Data Analysis (EDA)")

    # EDA section
    if perform_eda:
        st.header("Exploratory Data Analysis (EDA)")
        # Display summary statistics
        st.subheader("Summary Statistics")
        st.write(df.describe())

    # Machine Learning Section
    ml_option = st.sidebar.checkbox("Machine Learning Tasks")
    if ml_option:
        st.header("Machine Learning Tasks")

        # Ask the user to select X (features) and y (target) columns
        selected_features = st.multiselect("Select X (Features) Columns:", df.columns)
        selected_target = st.selectbox("Select y (Target) Column:", df.columns)

        # Ask the user to choose between classification and regression
        task_type = st.radio("Select Task Type:", ("Classification", "Regression"))

        if task_type == "Classification":
            st.subheader("Classification Task")

            # Ask the user to select classification models
            selected_models = st.multiselect("Select Classification Models:", ["Logistic Regression", "Decision Tree", "Random Forest"])

            # Ask the user for the ratio of train-test split
            test_size = st.slider("Select Test Size Ratio:", min_value=0.1, max_value=0.5, step=0.05, value=0.2)

            # Split the data into X (features) and y (target)
            X = df[selected_features]
            y = df[selected_target]

            # Encode the target variable for classification
            label_encoder = LabelEncoder()
            y = label_encoder.fit_transform(y)

            # Split the data into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

            # Classification models dictionary
            classification_models = {
                "Logistic Regression": LogisticRegression(),
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier()
            }

            best_model_name = ""
            best_model_score = -float('inf')

            # Run classification models and select the best one
            for model_name, model in classification_models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # Calculate accuracy (you can choose a different metric)
                score = accuracy_score(y_test, y_pred)

                # Update best model
                if score > best_model_score:
                    best_model_name = model_name
                    best_model_score = score

            st.subheader("Best Classification Model:")
            st.write(f"Model: {best_model_name}")
            st.write(f"Best Score: {best_model_score}")

        elif task_type == "Regression":
            st.subheader("Regression Task")

            # Ask the user to select regression models
            selected_models = st.multiselect("Select Regression Models:", ["Linear Regression", "Ridge", "Lasso", "Random Forest"])

            # Ask the user for the ratio of train-test split
            test_size = st.slider("Select Test Size Ratio:", min_value=0.1, max_value=0.5, step=0.05, value=0.2)

            # Split the data into X (features) and y (target)
            X = df[selected_features]
            y = df[selected_target]

            # Split the data into train and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

            # Regression models dictionary
            regression_models = {
                "Linear Regression": LinearRegression(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "Random Forest": RandomForestRegressor()
            }

            best_model_name = ""
            best_model_mse = float('inf')
            best_model_r2 = -float('inf')

            worst_model_name = ""
            worst_model_mse = -float('inf')
            worst_model_r2 = float('inf')

            # Run regression models and select the best one
            for model_name, model in regression_models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)

                # Update best model
                if mse < best_model_mse and r2 > best_model_r2:
                    best_model_name = model_name
                    best_model_mse = mse
                    best_model_r2 = r2

                # Update worst model
                if mse > worst_model_mse and r2 < worst_model_r2:
                    worst_model_name = model_name
                    worst_model_mse = mse
                    worst_model_r2 = r2

            st.subheader("Best Regression Model:")
            st.write(f"Model: {best_model_name}")
            st.write(f"Mean Squared Error (MSE): {best_model_mse}")
            st.write(f"R-squared (R2): {best_model_r2}")

            st.subheader("Worst Regression Model:")
            st.write(f"Model: {worst_model_name}")
            st.write(f"Mean Squared Error (MSE): {worst_model_mse}")
            st.write(f"R-squared (R2): {worst_model_r2}")

# Run the application
if __name__ == "__main__":
    main()
