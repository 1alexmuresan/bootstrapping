#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 16:50:56 2025

@author: alex
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# Download Apple stock data
ticker = "AAPL"
df = yf.download(ticker, start="2015-02-01", end="2025-02-01")

# Calculate arithmetic returns
df["Arithmetic Returns"] = df["Close"].pct_change()

# Drop NaN values
returns = df["Arithmetic Returns"].dropna()

# Define bootstrapping parameters
sample_size = 252  # 1 year of trading days
n_bootstrap = 5000  # Number of bootstrap samples
bootstrap_sds = []

# Bootstrapping process
for _ in range(n_bootstrap):
    bootstrap_sample = np.random.choice(returns, size=sample_size, replace=True)
    annualized_sd = np.std(bootstrap_sample, ddof=1) * np.sqrt(252)  # Annualize each SD
    bootstrap_sds.append(annualized_sd)  # Store annualized values

# Convert to numpy array for analysis
mean_bootstrap_sd = np.mean(bootstrap_sds)  

# Plot histogram of the bootstrapped annualized standard deviations
plt.figure(figsize=(10, 6))
plt.hist(bootstrap_sds, bins=50, density=True, alpha=0.6, color="blue", label="Bootstrap Annualized SD Distribution")

# Compute confidence interval
lower_bound = np.percentile(bootstrap_sds, 2.5)
upper_bound = np.percentile(bootstrap_sds, 97.5)
plt.axvline(lower_bound, color="red", linestyle="--", label="2.5% CI")
plt.axvline(upper_bound, color="red", linestyle="--", label="97.5% CI")

# Labels and title
plt.xlabel("Bootstrap Annualized Standard Deviation")
plt.ylabel("Density")
plt.title("Bootstrapped Distribution of Annualized Standard Deviations for AAPL (2015-2025)")
plt.legend()
plt.grid()

plt.show()

# Output results
print(f"Bootstrapped Mean Annualized Standard Deviation: {mean_bootstrap_sd:.4f}")
print(f"95% Confidence Interval: ({lower_bound:.4f}, {upper_bound:.4f})")



