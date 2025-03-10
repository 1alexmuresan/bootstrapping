"""
Bootstrapped Geometric Means with Table
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

tickers = ["COP", "DVN", "AAPL", "MSFT", "IEF", "LQD"]  # Replace with your desired stock tickers
start_date = "2015-02-01" # Replace with your desired start date
end_date = "2025-02-01"  # Replace with your desired end date

results = {}

for ticker in tickers:
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
    sample_size = 252  # Replace with your desired sample size (in days). 1 year of trading is approx. 252 days
    n_bootstrap = 5000 # Number of bootstrap samples
    bootstrap_means = []

    # Bootstrapping Process
    for _ in range(n_bootstrap):
        bootstrap_sample = np.random.choice(df["Log Returns"], size=sample_size, replace=True)
        annualized_geom_mean_log = np.mean(bootstrap_sample) * 252 # Annualize log return
        annualized_geom_mean = np.exp(annualized_geom_mean_log) - 1 #Convert back to normal return
        bootstrap_means.append(annualized_geom_mean)
    mean_bootstrap_geomean = np.mean(bootstrap_means)

    # Bias Correction
    bias = mean_bootstrap_geomean - annualized_geometric_mean
    corrected_bootstrap_means = [x - bias for x in bootstrap_means]
    corrected_mean_bootstrap_geommean = np.mean(corrected_bootstrap_means)
    
    results[ticker] = [annualized_geometric_mean, corrected_mean_bootstrap_geommean]

stats_df = pd.DataFrame(results, index=["Historical Geometric Mean", "Bootstrapped Geometric Mean"]).T

# Create Table
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
plt.title("Bootstrapped Geometric Arithmetic Means")
plt.tight_layout()

plt.show()
print(stats_df.round(6))
