import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

import platform
import sys

print("Python Version:", sys.version)
print("Platform:", platform.platform())
# ... print other relevant information about your environment


try:
    # Load the Iris dataset
    iris = load_iris()
    X, y = iris.data, iris.target

    # Load the model
    with open('IRIS/iris_model.pkl', 'rb') as model_file:
        clf = pickle.load(model_file)

    print("Model loaded successfully")

except Exception as e:
    print(f"Error loading the model: {e}")
