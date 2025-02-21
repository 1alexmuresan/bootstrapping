#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 12:22:04 2025

@author: alex
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

tickers = ["MRNA", "BNTX", "AAPL", "MSFT", "IEF", "LQD"]
start_date = "2015-02-01"
end_date = "2025-02-01"

results = {}

for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)
    df["Arithmetic Returns"] = df["Close"].pct_change()
    returns = df["Arithmetic Returns"].dropna()
    
    # Note: 252 days = approx. 1 year of trading days
    annualized_arithmetic_mean = np.mean(returns) * 252
    
    # Bootstrapping for arithmetic mean
    sample_size = 252 
    n_bootstrap = 5000
    bootstrap_means = [np.mean(np.random.choice(returns, size=sample_size, replace=True)) * 252 for _ in range(n_bootstrap)]
    
    # Bootstrapping for geometric mean
    bootstrap_geometric_means = []
    for _ in range(n_bootstrap):
        bootstrap_sample = np.random.choice(returns, size=sample_size, replace=True)
        geometric_mean = np.exp(np.mean(np.log(1 + bootstrap_sample))) - 1
        bootstrap_geometric_means.append(geometric_mean)
        
    annualized_bootstrap_geometric_means = np.array(bootstrap_geometric_means) * 252
    
    # Bootstrapping for standard deviation
    bootstrap_sds = []
    for _ in range(n_bootstrap):
        bootstrap_sample = np.random.choice(returns, size=sample_size, replace=True)
        bootstrap_sds.append(np.std(bootstrap_sample, ddof=1) * np.sqrt(252))

    # Sharpe Ratio = (Arithmetic Mean Returns - 1/2 * (Std Dev)^2) / Std Dev
    mean_returns = annualized_arithmetic_mean
    std_dev = np.mean(bootstrap_sds)
    sharpe_ratio = (mean_returns - 0.5 * std_dev**2) / std_dev
    
    results[ticker] = [
        annualized_arithmetic_mean,
        np.mean(bootstrap_means),
        np.mean(annualized_bootstrap_geometric_means),
        np.mean(bootstrap_sds),
        sharpe_ratio
    ]

stats_df = pd.DataFrame(results, index=["Ann. AM", "Boot AM", 
                                         "Boot GM", "Boot SD", "Sharpe Ratio"]).T

fig, ax = plt.subplots(figsize=(8, 4))
ax.axis("tight")
ax.axis("off")
table = ax.table(cellText=stats_df.round(6).values,
                 colLabels=stats_df.columns,
                 rowLabels=stats_df.index,
                 cellLoc="center", loc="center")

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

plt.title("Bootstrapped Annualized Returns (Arithmetic, Geometric, SD, and Sharpe Ratio)")
plt.show()

# Print the DataFrame
print(stats_df.round(4))





