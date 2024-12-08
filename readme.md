# MES Position Size Calculator

For all people struggling to figure out how to size their position for MES, this project is for you! 
This project analyzes historical MES (Micro E-mini S&P 500 Futures) intraday (1 min timeframe) price action to determine optimal position sizing based on historical volatility. The final output is a PineScript indicator (indicator publically available on my tradingview profile: https://www.tradingview.com/u/spiritualhealer117/) that will recommend position size in MES contracts based on your desired holding period, and your desired profit target. 

It uses a series of log-transformed linear regressions to model how price changes scale with different holding periods across hours of the day.

## Overview

The system consists of three main Python scripts that:

1. Analyze historical price data, and visualize the Mean Price Movement by Holding Period and by Hour of Day (`generalStatsGraph.py`)
2. Perform log-linear regression modeling on holding period vs price movement, with a different fit for each hour of the day (`logisticReg.py`)
3. Convert the regression coefficients to PineScript switch statements (`processToPinescript.py`)

The final output is a series of coefficients that are used in my PineScript indicator to provide position size recommendations based on:
- Time of day
- Intended holding period
- Historical volatility patterns

## How It Works

1. `generalStatsGraph.py`:
   - Loads historical MES price data
   - Calculates absolute price changes over different holding periods
   - Generates visualizations of price movement patterns by hour
   - Outputs statistical summaries

2. `logisticReg.py`:
   - Performs log transformation on price movement data
   - Fits linear regression models for each hour of the day
   - Models the relationship: ln(price_change) = β₁ln(holding_period) + β₀
   - Outputs coefficients in the form: price_change = e^β₀ * holding_period^β₁

3. `processToPinescript.py`:
   - Converts regression coefficients into PineScript switch statements
   - Generates code that can be used in TradingView

4. Pinescript Indicator:
   - Copy the results from `processToPinescript.py` and paste them into the switch statements of my Pinescript indicator
   - The indicator will then recommend position size based on the desired holding period and profit target

## Usage

1. Run the Python scripts in order:
   ```bash
   python generalStatsGraph.py
   python logisticReg.py
   python processToPinescript.py
   ```

2. Copy the generated PineScript code into TradingView

3. The indicator will provide position size recommendations based on:
   - Current hour of day
   - Your intended holding period
   - Expected price movement calculated from the regression model

## Notes and Disclaimers

- All price movements are measured in ticks (0.25 points = 1 tick for MES)
- The model assumes log-normal distribution of price movements
- Position sizing should be adjusted based on your risk tolerance
- Past performance does not guarantee future results
- This is by no means a trading system, nor an endorsement of trading MES
- Outputs of this model are not financial advice, but rather an educational tool