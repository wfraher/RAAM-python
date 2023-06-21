import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from yahooquery import *
from pull_data import *

# Load the data
ticker = Ticker("AMD")
data = close_prices(ticker, start_date=None, end_date=None, interval="1d")

# We will predict whether the stock price increased or decreased
data['Price_Up'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

# Drop the date column
data = data.drop(columns=['Date'])

# Split the data into features (X) and target (y)
y = data['Price_Up']
X = data.drop(columns=['Price_Up'])

# Normalize the feature data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model architecture
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(loss='binary_crossentropy', optimizer=Adam(), metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=50, batch_size=32)
