
import numpy as np

def calculate_sharpe_ratio(daily_returns, risk_free_rate = 0):
    # Calculate average daily return
    avg_daily_return = np.mean(daily_returns)

    # Calculate daily standard deviation
    daily_std_dev = np.std(daily_returns, ddof=1)

    # Annualize the figures
    annualized_return = (1 + avg_daily_return) ** 252 - 1
    annualized_std_dev = daily_std_dev * np.sqrt(252)

    # Convert annual risk-free rate to daily
    daily_risk_free = (1 + risk_free_rate) ** (1/252) - 1
    annualized_risk_free = (1 + daily_risk_free) ** 252 - 1

    # Calculate Sharpe ratio
    sharpe_ratio = (annualized_return - annualized_risk_free) / annualized_std_dev

    return sharpe_ratio

def calculate_max_drawdown(equity_values):
    # Calculate the running maximum
    running_max = np.maximum.accumulate(equity_values)

    # Calculate drawdowns
    drawdowns = (equity_values - running_max) / running_max

    # Find the maximum drawdown
    max_drawdown = np.min(drawdowns)
    return max_drawdown
