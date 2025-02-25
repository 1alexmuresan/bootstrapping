"""
Correlation Matrix of Assets
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import pandas as pd

tickers = ["COP", "DVN", "AAPL", "MSFT", "IEF", "LQD"] # Replace with your desired stock ticker
start_date = "2015-02-01" # Replace with your desired start date
end_date = "2025-02-01" # Replace with your desired end date

data = yf.download(tickers, start=start_date, end=end_date)["Close"]
returns = data.pct_change().dropna()

# Compute the Correlation Matrix
correlation_matrix = returns.corr()
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)

# Plot the Correlation Matrix as a Heatmap (Lower Triangle Only)
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar=True, vmin=-1, vmax=1, mask=mask)
plt.title("Lower Triangle of Correlation Matrix for Stock Returns")
plt.tight_layout()
plt.show()

print(correlation_matrix)
