import numpy as np
import pandas as pd
import yfinance as yf
from keras.models import load_model
import streamlit as st
import matplotlib.pyplot as plt

st.header("Stock Market Predictor")
model = load_model(r"keras_model_Nepse.h5")
# Sidebar
st.sidebar.header('Select Stock Symbol To Predict ')

# Pre-defined datasets
dataset_options = {
  "NEPSE":pd.read_csv("nepse.csv"),
  "ADBL": pd.read_csv("ADBL_2000-01-01_2021-12-31.csv"),
  "HDL": pd.read_csv("HDL_2000-01-01_2021-12-31.csv"),
  "DDBL":pd.read_csv("DDBL_price_history.csv")
}

# User selects dataset
selected_dataset = st.sidebar.selectbox("Select Symbol", options=list(dataset_options.keys()))

# Selected dataset
data = dataset_options[selected_dataset]
#data = data1[: :-1]
data = data.iloc[::-1].reset_index(drop=True)

# Check if the column "close price" exists in the DataFrame (case-insensitive)
if any(col.lower() == "close" for col in data.columns):
    # Rename the column "close price" to "Close" (case-insensitive)
    data.rename(columns=lambda x: "Close" if x.lower() == "close" else x, inplace=True)

#data1= pd.read_csv("ADBL_2000-01-01_2021-12-31.csv")
#data = data1[::-1]


st.subheader('Stock Data')
reversed_data = data[::-1]
st.write(reversed_data)

data_train = pd.DataFrame(data.Close[0: int(len(data)*0.80)])
data_test = pd.DataFrame(data.Close[int(len(data)*0.80): len(data)])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

pas_100_days = data_train.tail(100)
data_test = pd.concat([pas_100_days, data_test], ignore_index=True)
data_test_scale = scaler.fit_transform(data_test)

st.subheader('Price vs MA50')
ma_50_days = data.Close.rolling(50).mean()
fig1 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r')
plt.plot(data.Close, 'g')
plt.show()
st.pyplot(fig1)

st.subheader('Price vs MA50 vs MA100')
ma_100_days = data.Close.rolling(100).mean()
fig2 = plt.figure(figsize=(8,6))
plt.plot(ma_50_days, 'r')
plt.plot(ma_100_days, 'b')
plt.plot(data.Close, 'g')
plt.show()
st.pyplot(fig2)

st.subheader('Price vs MA100 vs MA200')
ma_200_days = data.Close.rolling(200).mean()
fig3 = plt.figure(figsize=(8,6))
plt.plot(ma_100_days, 'r')
plt.plot(ma_200_days, 'b')
plt.plot(data.Close, 'g')
plt.show()
st.pyplot(fig3)

x = []
y = []

for i in range(60, data_test_scale.shape[0]):
    x.append(data_test_scale[i-60:i])
    y.append(data_test_scale[i,0])

x,y = np.array(x), np.array(y)

predict = model.predict(x)

scale = 1/scaler.scale_

predict = predict * scale
y = y * scale

st.subheader('Original Price vs Predicted Price')
fig4 = plt.figure(figsize=(8,6))
plt.plot(predict, 'r', label='Original Price')
plt.plot(y, 'g', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()
st.pyplot(fig4)


#Predictions


new_df = data.filter(['Close'])

last_60_days = new_df[-60:].values   # Taking value of last 60 days
last_60_days_scaled = scaler.transform(last_60_days)

X_test = []
X_test.append(last_60_days_scaled)

X_test = np.array(X_test)  # Convert to np array
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))  # Reshape to 3D for LSTM model

st.subheader('Predicted Price for Next Day:')
tomorrow = model.predict(X_test)
tomorrow_price = scaler.inverse_transform(tomorrow)
st.write(tomorrow_price)

# Predict prices for the next 7 days
pred_prices = []
for i in range(7):
    pred_scale_price = model.predict(X_test)  # Predicting the price for next day
    pred_price = scaler.inverse_transform(pred_scale_price)  # Inversing the scaled value to actual value
    pred_prices.append(pred_price[0][0])  # Append the predicted price to the list
    # Shift the data by one day and append the newly predicted price
    X_test = np.append(X_test[:, 1:, :], pred_scale_price.reshape((1, 1, 1)), axis=1)

# Display the predicted prices for the next 30 days
st.subheader('Predicted Prices for the Next 7 Days:')
for day, price in enumerate(pred_prices, start=1):
    st.write(f"Day {day}: {price}")
