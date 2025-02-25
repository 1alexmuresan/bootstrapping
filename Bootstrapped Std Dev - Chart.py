"""
Bootstrapping with Consistent Sampling & Post-Loop Annualization
"""
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

tickers = ["COP", "DVN", "AAPL", "MSFT", "IEF", "LQD"]
start_date = "2015-02-01"
end_date = "2025-02-01"

results = {}

for ticker in tickers:
    df = yf.download(ticker, start=start_date, end=end_date)
    df["Arithmetic Returns"] = df["Close"].pct_change()
    returns = df["Arithmetic Returns"].dropna()

    # Bootstrapping parameters
    sample_size = 252  # 1 year of trading days
    n_bootstrap = 5000
    bootstrap_sds = []
    
    for _ in range(n_bootstrap):        
        bootstrap_sample = np.random.choice(returns, size=sample_size, replace=True)
        annualized_sd = np.std(bootstrap_sample, ddof=1) * np.sqrt(252)  # Annualizing each standard deviation
        bootstrap_sds.append(annualized_sd)
    mean_bootstrap_sd = np.mean(bootstrap_sds)  

    results[ticker] = [mean_bootstrap_sd]

# Convert results to DataFrame
stats_df = pd.DataFrame(results, index=["Boot SD"]).T

# Display table
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

plt.title("Bootstrapped Annualized Standard Deviations")
plt.tight_layout()
plt.show()

# Print the DataFrame
print(stats_df.round(6))
