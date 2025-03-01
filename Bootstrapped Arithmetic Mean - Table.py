"""
Bootstrapped Arithmetic Means with Table
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

tickers = ["DUOL", "DVN", "AAPL", "MSFT", "IEF", "LQD"] # Replace with your desired stock tickers
start_date = "2024-02-01" # Replace with your desired start date
end_date = "2025-02-01" # Replace with your desired end date

results = {}

for ticker in tickers:
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
        annualized_arithmeans = np.mean(bootstrap_sample) * 252 # Annualizing each mean
        bootstrap_means.append(annualized_arithmeans)
    mean_bootstrap_arithmean = np.mean(bootstrap_means)
    results[ticker] = [annualized_arithmetic_mean, mean_bootstrap_arithmean]

stats_df = pd.DataFrame(results, index=["Historical Arithmetic Mean", "Bootstrapped Arithmetic Mean"]).T

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
plt.title("Bootstrapped Annualized Arithmetic Means")
plt.tight_layout()

plt.show()
print(stats_df.round(6))
