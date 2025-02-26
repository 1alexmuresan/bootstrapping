"""
Bootstrapped Arithmetic Means with Graph of Distribution and Confidence Intervals
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

# Compute Historical Annualized Arithmetic Mean
annualized_arithmetic_mean = np.mean(returns) * 252

# Bootstrapping Parameters
sample_size = 252  # Replace with your desired sample size (in days). 1 year of trading is approx. 252 days
n_bootstrap = 5000 # Number of bootstrap samples
bootstrap_means = []

# Bootstrapping Process
for _ in range(n_bootstrap):
    bootstrap_sample = np.random.choice(returns, size=sample_size, replace=True)
    annualized_arithmeans = np.mean(bootstrap_sample) * 252
    bootstrap_means.append(annualized_arithmeans)
mean_bootstrap_arithmean = np.mean(bootstrap_means)  

# Plot Histogram of Annualized Bootstrapped Arithmetic Means
plt.figure(figsize=(10, 6))
plt.hist(bootstrap_means, bins=50, density=True, alpha=0.6, color="blue", label="Bootstrap Annualized Aithmetic Mean Distribution")

# Compute Confidence Intervals
lower_bound = np.percentile(bootstrap_means, 2.5)
upper_bound = np.percentile(bootstrap_means, 97.5)
plt.axvline(lower_bound, color="red", linestyle="--", label="2.5% CI")
plt.axvline(upper_bound, color="red", linestyle="--", label="97.5% CI")

# Plot Titles and Labels
plt.xlabel("Bootstrap Annualized Arithmetic Mean Return")
plt.ylabel("Density")
plt.title("Bootstrapped Distribution of Annualized Arithmetic Mean Returns")
plt.legend()
plt.grid()

plt.show()
print(f"Historical  Arithmetic Mean: {annualized_arithmetic_mean:.4f}")
print(f"Bootstrapped Mean Semi-Annualized Arithmetic Return: {mean_bootstrap_arithmean:.4f}")
print(f"95% Confidence Interval: ({lower_bound:.4f}, {upper_bound:.4f})")


