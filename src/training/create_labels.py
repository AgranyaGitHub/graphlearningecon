import pandas as pd

def create_disruption_labels(volatility, threshold = 0.04):
    labels = (volatility > threshold).astype(int)
    return labels