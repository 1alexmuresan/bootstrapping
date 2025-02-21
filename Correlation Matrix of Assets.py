"""
Correlation Matrix of Assets
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
import pandas as pd

# Define tickers and date range
tickers = ["MRNA", "BNTX", "AAPL", "MSFT", "IEF", "LQD"]
start_date = "2015-02-01"
end_date = "2025-02-01"

# Download stock data
data = yf.download(tickers, start=start_date, end=end_date)["Close"]

# Calculate daily returns for each stock
returns = data.pct_change().dropna()

# Compute the correlation matrix
correlation_matrix = returns.corr()

# Mask the upper triangle of the matrix, but keep the diagonal (1s)
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)

# Plot the correlation matrix as a heatmap (lower triangle only)
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", cbar=True, vmin=-1, vmax=1, mask=mask)
plt.title("Lower Triangle of Correlation Matrix for Stock Returns")
plt.tight_layout()
plt.show()

# Print the correlation matrix
print(correlation_matrix)




