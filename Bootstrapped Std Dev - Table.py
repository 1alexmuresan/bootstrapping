"""
Bootstrapped Standard Deviations with Table
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
    returns = df["Arithmetic Returns"].dropna()

    # Compute Historical Annualized Std Dev
    annualized_std_dev = np.std(returns) * np.sqrt(252)

    # Bootstrapping Parameters
    sample_size = 252  # 1 year of trading days
    n_bootstrap = 5000  # Number of bootstrap samples
    bootstrap_sds = []

    # Bootstrapping Process
    for _ in range(n_bootstrap):        
        bootstrap_sample = np.random.choice(returns, size=sample_size, replace=True)
        annualized_sd = np.std(bootstrap_sample, ddof=1) * np.sqrt(252)  # Annualizing each standard deviation
        bootstrap_sds.append(annualized_sd)
    mean_bootstrap_sd = np.mean(bootstrap_sds)  
    
    # Bias Correction
    bias = mean_bootstrap_sd - annualized_std_dev
    corrected_bootstrap_sds = [x - bias for x in bootstrap_sds]
    corrected_mean_bootstrap_sd = np.mean(corrected_bootstrap_sds)
    
    results[ticker] = [annualized_std_dev, corrected_mean_bootstrap_sd]

stats_df = pd.DataFrame(results, index=["Historical Std Dev", "Bootstrapped Std Dev"]).T

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
plt.title("Bootstrapped Annualized Standard Deviations")
plt.tight_layout()

plt.show()
print(stats_df.round(6))

plt.show()
print(stats_df.round(6))
