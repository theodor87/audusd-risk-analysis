import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

# 1. Load historical data from CSV and ensure datetime index
df = pd.read_csv("audusd_historical.csv", header=[0, 1], index_col=0)
df.index = pd.to_datetime(df.index)

# 2. Extract Close prices for AUD/USD
prices = df["Close"]["AUDUSD=X"]

# 3. Calculate Drawdown metrics
rolling_max = prices.cummax()
drawdown = ((prices - rolling_max) / rolling_max) * 100

max_dd = drawdown.min()
max_dd_date = drawdown.idxmin()
avg_dd = drawdown.mean()

# Print professional summary to console
print("----------------------------------------")
print("AUD/USD DRAWDOWN & RISK ANALYSIS (Past 1 Year)")
print(f"Maximum Drawdown (Max DD): {max_dd:.2f}%")
print(f"Date of Max Drawdown: {str(max_dd_date)[:10]}")
print(f"Average Drawdown: {avg_dd:.2f}%")
print("----------------------------------------")

# 4. Generate professional charts for LinkedIn / Portfolio
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Top subplot: Price Action & Peak Tracking
ax1.plot(
    prices.index, prices, label="AUD/USD Close Price", color="#2b5c8f", linewidth=1.5
)
ax1.plot(
    rolling_max.index,
    rolling_max,
    label="Running Maximum (Peak)",
    color="#2ca02c",
    linestyle="--",
    alpha=0.8,
)
ax1.set_title(
    "AUD/USD Price Action & Peak Highs (1-Year)", fontsize=14, fontweight="bold"
)
ax1.set_ylabel("Price", fontsize=12)
ax1.legend(loc="lower left")
ax1.grid(True, linestyle=":", alpha=0.6)

# Bottom subplot: Drawdown percentage
ax2.fill_between(drawdown.index, drawdown, 0, color="#d62728", alpha=0.3)
ax2.plot(
    drawdown.index, drawdown, label="Drawdown (%)", color="#d62728", linewidth=1
)
ax2.set_title(
    f"Asset Drawdown & Correction Curve (Max DD: {max_dd:.2f}%)",
    fontsize=14,
    fontweight="bold",
)
ax2.set_ylabel("Drawdown (%)", fontsize=12)
ax2.set_xlabel("Date", fontsize=12)
ax2.legend(loc="lower left")
ax2.grid(True, linestyle=":", alpha=0.6)

# FIX: Format X-axis dates cleanly by month so they don't overlap
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
fig.autofmt_xdate(rotation=45)

# Layout adjustment and saving
plt.tight_layout()
output_image = "audusd_drawdown_analysis.png"
plt.savefig(output_image, dpi=300)
print(f"\nProfessional chart successfully saved as '{output_image}'!")

# Display the plot window
plt.show()