import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t
import datetime as dt
import time

from yahooquery import Ticker

past_data_days = 120
trading_days = 15
target_price = 2.2
ticker_symbol = "GOSS"

df = 5

end_date = dt.datetime.today()
start_date = end_date - dt.timedelta(days=past_data_days)


def get_spot_price(ticker_symbol, start=start_date, end=end_date):
    ticker = Ticker(ticker_symbol)
    prices = ticker.history(period=f"{past_data_days}d")['close']  # last 60 days
    return prices.iloc[-1]

current_spot_price = get_spot_price(ticker_symbol, start_date, end_date).item()
entry = current_spot_price

def realized_volatility(ticker_symbol, start=start_date, end=end_date):
    ticker = Ticker(ticker_symbol)
    prices = ticker.history(period=f"{past_data_days}d")['close']
    returns = np.log(prices / prices.shift(1)).dropna()
    sigma = returns.std()
    return sigma.item(), returns

sigma_daily, returns = realized_volatility(ticker_symbol, start_date, end_date)

sigma_t = sigma_daily * np.sqrt(trading_days)

mu_daily = returns.mean().item()
if trading_days <= 100:
    mu_t = 0
else:
    mu_t = mu_daily * past_data_days

log_return_target = np.log(target_price / current_spot_price)
z = float(log_return_target - mu_t) / sigma_t

k = 0.5
stop_price = entry * np.exp(-k * sigma_t)

print(f'Z score is: {z}')
print("-" * 40)
print(f"daily volatility:, {sigma_daily}")
print("-" * 40)
print(f"{trading_days} days sigma:, {sigma_t}")
print("-" * 40)
print(f"Current spot price {current_spot_price}")
print(f"current target price {target_price}")

N_STEPS = trading_days
N_PATHS = 50000
dt_sim = 1 / 252
mu = 0
sigma = sigma_daily * np.sqrt(252)

flat_hits = 0
target_hits = 0
stop_hits = 0


for _ in range(N_PATHS):
    price = entry

    for _ in range(N_STEPS):
        Z = t.rvs(df)
        Z = Z / np.sqrt(df / (df - 2))

        price *= np.exp(
            (mu - 0.5 * sigma ** 2) * dt_sim
            + sigma * np.sqrt(dt_sim) * Z
        )

        if price >= target_price:
            target_hits += 1
            break
        elif price <= stop_price:
            stop_hits += 1
            break
    else:
        flat_hits += 1

gain = target_price - entry
loss = entry - stop_price

P_win = target_hits / N_PATHS
P_loss = stop_hits / N_PATHS
P_flat = 1 - P_win - P_loss

R = gain / loss
EV = P_win * gain - P_loss * loss

print(f"Ev is {EV}")
Kelly = P_win - (P_loss / R)
print(f"Kelly is {Kelly * 100}")
print(f" Fractional kelly is {(Kelly * 100) * 1/4}")
print("-" * 40)
print(f"win percentage: {P_win * 100}")
print(f"loss percentage: {P_loss * 100}")
print(f"neither win or loss percentage: {P_flat * 100}")

Labels = ["Win (target)", "Loss (Stop)", "Flat"]
Probs = [P_win, P_loss, P_flat]

plt.bar(Labels, Probs)
plt.ylabel("Probability")
plt.title("First touch probabilities")
plt.ylim([0, 1])
plt.show()
time.sleep(2)
