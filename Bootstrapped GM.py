"""
Bootstrapped Geometric Means with Graph of Distribution and Confidence Intervals
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import gmean  # Import built-in geometric mean function

ticker = "DUOL"  # Replace with your desired stock ticker
start_date = "2015-02-01"
end_date = "2025-02-01"

# Download data
df = yf.download(ticker, start=start_date, end=end_date)

# Compute Daily Geometric Returns
df["Geometric Returns"] = 1 + df["Close"].pct_change()  # Convert to return factor (1 + r)
df = df.dropna()  # Remove NaN values

# Compute Historical Annualized Geometric Mean Using gmean (Daily Returns)
daily_geometric_mean = gmean(df["Geometric Returns"]) - 1  # Convert back to return
annualized_geometric_mean = (1 + daily_geometric_mean) ** 252 - 1  # Annualize (252 trading days in a year)

# Bootstrapping Parameters
sample_size = 252  # 1 year of trading days
n_bootstrap = 5000  # Number of bootstrap samples
bootstrap_means = []

# Bootstrapping Process
for _ in range(n_bootstrap):
    bootstrap_sample = np.random.choice(df["Geometric Returns"], size=sample_size, replace=True)
    annualized_geom_mean = (gmean(bootstrap_sample) ** 252) - 1  # Annualizing the bootstrapped geometric mean
    bootstrap_means.append(annualized_geom_mean)

# Compute Bootstrapped Statistics
mean_bootstrap_geommean = np.mean(bootstrap_means)
lower_bound = np.percentile(bootstrap_means, 2.5)
upper_bound = np.percentile(bootstrap_means, 97.5)

# Plot Histogram of Annualized Bootstrapped Geometric Means
plt.figure(figsize=(10, 6))
plt.hist(bootstrap_means, bins=50, density=True, alpha=0.6, color="green", label="Bootstrap Annualized Geometric Mean Distribution")

# Confidence Interval Lines
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
print(f"Bootstrapped Mean Annualized Geometric Return: {mean_bootstrap_geommean:.4f}")
print(f"95% Confidence Interval: ({lower_bound:.4f}, {upper_bound:.4f})")








