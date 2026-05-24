import pandas as pd

def compute_returns(prices):
    returns = prices.pct_change()
    return returns

def compute_volatility(returns, window = 30):
    volatility = returns.rolling(window).std()
    return volatility