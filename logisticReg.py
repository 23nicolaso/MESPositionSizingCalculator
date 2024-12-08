import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# Read the CSV file
df = pd.read_csv('newerBeautifulMESData.csv')

# Convert Date and Time columns to datetime
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%m/%d/%Y %I:%M:%S %p')

# Create hour of day column
df['hour'] = df['datetime'].dt.hour

# Calculate price changes for different holding periods (in minutes)
holding_periods = list(range(1, 121, 1))  # Creates list from 1 to 120 in steps of 1 minute

# Pre-allocate columns to avoid fragmentation
price_change_cols = [f'price_change_{period}m' for period in holding_periods]
future_close_cols = [f'future_close_{period}m' for period in holding_periods]

# Create empty DataFrame with all needed columns
new_cols = pd.DataFrame(index=df.index, columns=price_change_cols + future_close_cols)
df = pd.concat([df, new_cols], axis=1)

# Initialize a dictionary to store results for each hour
hourly_results = {}

# Initialize the scaler and linear regression model
scaler = StandardScaler()
lr = LinearRegression()

# Iterate through each hour of the day
for hour in range(24):
    # Filter the DataFrame for the current hour
    df_hour = df[df['hour'] == hour].copy()  # Use .copy() to avoid SettingWithCopyWarning
    
    # Skip if there is no data for this hour
    if df_hour.empty:
        continue

    # Remove outliers using IQR
    Q1 = df_hour['close'].quantile(0.25)
    Q3 = df_hour['close'].quantile(0.75)
    IQR = Q3 - Q1
    df_hour = df_hour[(df_hour['close'] >= Q1 - 1.5 * IQR) & (df_hour['close'] <= Q3 + 1.5 * IQR)]

    # Recalculate results for the current hour
    results = []
    for period in holding_periods:
        df_hour.loc[:, f'future_close_{period}m'] = df_hour.groupby('Date')['close'].shift(-period)
        df_hour.loc[:, f'price_change_{period}m'] = abs(df_hour[f'future_close_{period}m'] - df_hour['close']) * 4
        
        overall_stats = df_hour[f'price_change_{period}m'].agg(['mean', 'std', 'count']).round(2)
        results.append({
            'period_minutes': period,
            'overall_stats': overall_stats
        })

    # Extract periods and means for log transformation and linear regression
    periods = np.array([r['period_minutes'] for r in results]).reshape(-1, 1)
    means = np.array([r['overall_stats']['mean'] for r in results])

    # Remove NaN values from periods and means
    valid_indices = ~np.isnan(means)
    periods = periods[valid_indices]
    means = means[valid_indices]

    # Apply log transformation
    log_periods = np.log(periods)
    log_means = np.log(means)

    # Scale the features
    X_scaled = scaler.fit_transform(log_periods)

    # Fit linear regression on log-transformed data
    lr.fit(X_scaled, log_means)

    # Prepare data for prediction
    X_pred_scaled = scaler.transform(log_periods)
    y_pred_log = lr.predict(X_pred_scaled)
    y_pred = np.exp(y_pred_log)

    # Store results for the current hour
    hourly_results[hour] = {
        'periods': periods,
        'means': means,
        'y_pred': y_pred,
        'slope': lr.coef_[0] * scaler.scale_[0],
        'intercept': lr.intercept_ + lr.coef_[0] * (-scaler.mean_[0])
    }

    # Create visualization for the current hour
    # plt.figure(figsize=(12, 8))
    # plt.scatter(periods, means, color='blue', label='Actual Data Points')
    # plt.plot(periods, y_pred, color='red', label='Log-Linear Regression Fit')
    # plt.title(f'Overall Mean Price Movement by Holding Period with Log-Linear Regression (Hour {hour})')
    # plt.xlabel('Holding Period (minutes)')
    # plt.ylabel('Mean Price Movement (ticks)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # Print regression equation for the current hour
    # print(f"\nLog-Linear Regression Equation for Hour {hour}:")
    # print(f"ln(y) = {hourly_results[hour]['slope']:.4f} * ln(x) + {hourly_results[hour]['intercept']:.4f}")
    # print("Where:")
    # print("y = Mean Price Movement (ticks)")
    # print("x = Holding Period (minutes)")

    # Print transformed equation for the current hour
    # print(f"\nTransformed Equation for Hour {hour}:")
    print(f"hour: {hour}, y = e^({hourly_results[hour]['intercept']:.4f}) * x^({hourly_results[hour]['slope']:.4f}) \\n\\")
    # print(f"time: {hour}, y = {np.exp(hourly_results[hour]['intercept']):.4f} * x^({hourly_results[hour]['slope']:.4f})")

# Print regression equation
slope = lr.coef_[0] * scaler.scale_[0]  # Adjust slope for scaling
intercept = lr.intercept_ + slope * (-scaler.mean_[0])  # Adjust intercept for scaling
# print("\nLog-Linear Regression Equation:")
# print(f"ln(y) = {slope:.4f} * ln(x) + {intercept:.4f}")
# print("Where:")
# print("y = Mean Price Movement (ticks)")
# print("x = Holding Period (minutes)")

# Print transformed equation
# print("\nTransformed Equation:")
# print(f"y = e^({intercept:.4f}) * x^({slope:.4f})")
# print(f"y = {np.exp(intercept):.4f} * x^({slope:.4f})")

# Print actual values for specific holding periods
# target_periods = [1, 5, 15]
# print("\nActual Values:")
# for period in target_periods:
#     period_idx = periods.flatten().tolist().index(period)
#     print(f"{period} minute holding period: {means[period_idx]:.2f} ticks")
