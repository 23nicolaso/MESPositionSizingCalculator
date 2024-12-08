import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('beautifulMESData.csv')

# Convert Date and Time columns to datetime
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%Y %I:%M:%S %p')

# Create hour of day column
df['hour'] = df['datetime'].dt.hour

# Calculate price changes for different holding periods (in minutes)
holding_periods = [1, 5, 10, 15, 30, 60, 120]

results = []
for period in holding_periods:
    # Forward shift the close price by the period
    df[f'future_close_{period}m'] = df.groupby(df['Date'])['close'].shift(-period)
    
    # Calculate absolute price change in ticks (0.25 point = 1 tick)
    df[f'price_change_{period}m'] = abs(df[f'future_close_{period}m'] - df['close']) * 4  # multiply by 4 to convert to ticks
    
    # Group by hour and calculate mean price change
    hourly_stats = df.groupby('hour')[f'price_change_{period}m'].agg(['mean', 'std', 'count']).round(2)
    
    # Calculate overall stats
    overall_stats = df[f'price_change_{period}m'].agg(['mean', 'std', 'count']).round(2)
    
    results.append({
        'period_minutes': period,
        'hourly_stats': hourly_stats,
        'overall_stats': overall_stats
    })

# Create visualizations
plt.style.use('seaborn')
fig, axes = plt.subplots(2, 1, figsize=(15, 12))

# Plot 1: Mean price movement by hour for each period
ax1 = axes[0]
for result in results:
    period = result['period_minutes']
    hourly_means = result['hourly_stats']['mean']
    ax1.plot(hourly_means.index, hourly_means.values, label=f'{period}m', marker='o')

ax1.set_title('Mean Price Movement by Hour of Day')
ax1.set_xlabel('Hour of Day')
ax1.set_ylabel('Mean Price Movement (ticks)')
ax1.legend(title='Holding Period')
ax1.grid(True)

# Plot 2: Overall mean price movement by holding period
ax2 = axes[1]
periods = [r['period_minutes'] for r in results]
means = [r['overall_stats']['mean'] for r in results]
ax2.bar(periods, means)
ax2.set_title('Overall Mean Price Movement by Holding Period')
ax2.set_xlabel('Holding Period (minutes)')
ax2.set_ylabel('Mean Price Movement (ticks)')
ax2.grid(True)

plt.tight_layout()
plt.show()

# Print numerical results
print("\nPrice Movement Statistics (in ticks):\n")
for result in results:
    period = result['period_minutes']
    print(f"\n{period} Minute Holding Period:")
    print("-" * 50)
    print("\nOverall Statistics:")
    print(f"Mean: {result['overall_stats']['mean']:.2f} ticks")
    print(f"Std Dev: {result['overall_stats']['std']:.2f} ticks")
    print(f"Sample Size: {result['overall_stats']['count']}")
    
    print("\nStatistics by Hour:")
    print(result['hourly_stats'])
    print("\n")
