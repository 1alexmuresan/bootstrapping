"""
Bootstrapped Geometric Means with Graph of Distribution and Confidence Intervals
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

ticker = "AAPL" # Replace with your desired stock ticker
start_date = "2015-02-01" # Replace with your desired start date
end_date = "2025-02-01"  # Replace with your desired end date

df = yf.download(ticker, start=start_date, end=end_date)
df["Arithmetic Returns"] = df["Close"].pct_change()
df = df.dropna()

# Convert Arithmetic Returns to Log Returns
df["Log Returns"] = np.log(1 + df["Arithmetic Returns"])

# Compute Historical Annualized Geometric Mean Using gmean (Daily Returns)
daily_geometric_mean_log = np.mean(df["Log Returns"])  # Mean of log returns is approximately the geometric mean
annualized_geometric_mean_log = daily_geometric_mean_log * 252  # Annualize log return
annualized_geometric_mean = np.exp(annualized_geometric_mean_log) - 1  # Convert back to normal return

# Bootstrapping Parameters
sample_size = 252  # 1 year of trading days
n_bootstrap = 5000  # Number of bootstrap samples
bootstrap_means = []

# Bootstrapping Process
for _ in range(n_bootstrap):
    bootstrap_sample = np.random.choice(df["Log Returns"], size=sample_size, replace=True)
    annualized_geom_mean_log = np.mean(bootstrap_sample) * 252 # Annualize log return
    annualized_geom_mean = np.exp(annualized_geom_mean_log) - 1 #Convert back to normal return
    bootstrap_means.append(annualized_geom_mean)

# Bias Correction
bias = np.mean(bootstrap_means) - annualized_geometric_mean
corrected_bootstrap_means = [x - bias for x in bootstrap_means]
corrected_mean_bootstrap_geommean = np.mean(corrected_bootstrap_means)


# Plot Histogram of Annualized Bootstrapped Geometric Means
plt.figure(figsize=(10, 6))
plt.hist(corrected_bootstrap_means, bins=50, density=True, alpha=0.6, color="green", label="Bootstrap Annualized Geometric Mean Distribution")

# Compute Confidence Intervals
lower_bound = np.percentile(corrected_bootstrap_means, 2.5)
upper_bound = np.percentile(corrected_bootstrap_means, 97.5)
plt.axvline(lower_bound, color="red", linestyle="--", label="2.5% CI")
plt.axvline(upper_bound, color="red", linestyle="--", label="97.5% CI")

# Plot Titles and Labels
plt.xlabel("Bootstrap Annualized Geometric Mean Return")
plt.ylabel("Density")
plt.title("Bootstrapped Distribution of Annualized Geometric Mean Returns (Daily Data)")
plt.legend()
plt.grid()

plt.show()

# Print Results
print(f"Historical Geometric Mean (Daily): {annualized_geometric_mean:.4f}")
print(f"Bootstrapped Mean Annualized Geometric Return: {corrected_mean_bootstrap_geommean:.4f}")
print(f"95% Confidence Interval: ({lower_bound:.4f}, {upper_bound:.4f})")








