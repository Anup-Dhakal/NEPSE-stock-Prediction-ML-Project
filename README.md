# NEPSE Stock Price Prediction 📈

**Predicting NEPSE stock closing prices using LSTM networks.**

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python) ![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow) ![MIT License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Project Overview

This project uses **LSTM (Long Short-Term Memory)** networks to forecast **closing prices** of stocks listed on the **Nepal Stock Exchange (NEPSE)**. It helps investors understand trends and make informed decisions.

## 📊 Features

* Predict future closing prices of NEPSE stocks.
* Visualize predicted vs actual prices.
* Easy to extend for multiple stocks or additional indicators.

## 📂 Dataset

The dataset includes historical stock prices with columns:

* Date
* Open, High, Low, Close prices
* Volume

> Data can be sourced from NEPSE official website or other financial datasets.

## ⚡ Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/NEPSE-stock-Prediction-ML-Project.git
cd NEPSE-stock-Prediction-ML-Project
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run training:

```bash
python train_lstm.py
```

4. View predicted vs actual closing price plots.

## 🧠 Model

* **Type:** LSTM
* **Input:** Historical closing prices
* **Output:** Next closing price
* **Loss:** MSE
* **Optimizer:** Adam

## 📈 Results

* Predicts closing prices with visual comparison to actual prices.
* Evaluation metrics include RMSE and MAPE.

## 🔧 Folder Structure

```
NEPSE-stock-Prediction-ML-Project/
│
├─ data/               # NEPSE stock CSV files
├─ notebooks/          # Jupyter notebooks (EDA & training)
├─ models/             # Saved models
├─ train_lstm.py       # Training script
├─ requirements.txt    # Dependencies
├─ README.md           # Project documentation
```

## 🚀 Future Improvements

* Add technical indicators like SMA, EMA, RSI.
* Multi-step ahead forecasting.
* Integrate sentiment analysis from news.
* Deploy as web app/API for real-time predictions.

## 📄 License

This project is open-source under the **MIT License**.
