"""
Bootstrapped Stanadard Deviation with Graph of Distribution and Confidence Intervals
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

ticker = "AAPL" # Replace with your desired stock ticker
start_date = "2015-02-01" # Replace with your desired start date
end_date = "2025-02-01"  # Replace with your desired end date

df = yf.download(ticker, start=start_date, end=end_date)
df["Arithmetic Returns"] = df["Close"].pct_change()
returns = df["Arithmetic Returns"].dropna()

# Bootstrapping Parameters
sample_size = 252  # Replace with your desired sample size (in days). 1 year of trading is approx. 252 days
n_bootstrap = 5000  # Number of bootstrap samples
bootstrap_sds = []

# Bootstrapping Process
for _ in range(n_bootstrap):
    bootstrap_sample = np.random.choice(returns, size=sample_size, replace=True)
    annualized_sd = np.std(bootstrap_sample, ddof=1) * np.sqrt(252)  # Annualizing each standard deviation
    bootstrap_sds.append(annualized_sd)
mean_bootstrap_sd = np.mean(bootstrap_sds)  

# Plot Histogram of Annualized Bootstrapped Standard Deviations
plt.figure(figsize=(10, 6))
plt.hist(bootstrap_sds, bins=50, density=True, alpha=0.6, color="blue", label="Bootstrap Annualized Sttd Dev Distribution")

# Compute Confidence Intervals
lower_bound = np.percentile(bootstrap_sds, 2.5)
upper_bound = np.percentile(bootstrap_sds, 97.5)
plt.axvline(lower_bound, color="red", linestyle="--", label="2.5% CI")
plt.axvline(upper_bound, color="red", linestyle="--", label="97.5% CI")

# Plot Titles and Labels
plt.xlabel("Bootstrap Annualized Standard Deviation")
plt.ylabel("Density")
plt.title("Bootstrapped Distribution of Annualized Standard Deviations")
plt.legend()
plt.grid()

plt.show()
print(f"Bootstrapped Mean Annualized Standard Deviation: {mean_bootstrap_sd:.4f}")
print(f"95% Confidence Interval: ({lower_bound:.4f}, {upper_bound:.4f})")



