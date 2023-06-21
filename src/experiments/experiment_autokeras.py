# Import required libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.preprocessing import LabelEncoder
import autokeras as ak

# Load the iris dataset
iris = load_iris()
x, y = iris.data, iris.target

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Initialize the structured data classifier
clf = ak.StructuredDataClassifier(max_trials=10) # try 10 different models

# Fit the classifier
clf.fit(x_train, y_train, epochs=10)

# Evaluate the classifier
print('Accuracy: ', clf.evaluate(x_test, y_test))
