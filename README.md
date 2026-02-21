MONTE CARLO FIRST TOUCH PROBABILITY SIMULATOR 

This project estimates the probability that a stock reaches a target price or stop-loss within a fixed time horizon using Monte Carlo simulation.

The goal is not to price options it’s to evaluate trade risk, probability of outcomes, and position sizing logic before entering a trade.



What This Does

The script pulls historical price data, estimates realized volatility from log returns, simulates thousands of future price paths using Student-t shocks to allow for fat tails, and tracks which level is hit first: target, stop, or neither.

From those simulations it calculates win probability, loss probability, expected value (EV), risk/reward ratio, and Kelly fraction sizing.



Modeling Approach

Future prices are simulated using a Geometric Brownian Motion framework:

S(t+1) = S(t) * exp((μ − ½σ²)Δt + σ√Δt Z)

Z follows a Student-t distribution to account for heavier tails than a normal distribution.  
σ is estimated from historical realized volatility.  
μ is set conservatively.  
Δt = 1/252 for daily steps.

The simulation runs thousands of paths and records the first level touched.



Why This Exists

Before taking a trade, it’s useful to quantify:

What is the probability the target gets hit first?  
What is the probability the stop gets hit first?  
Is the expected value positive?  
What fraction of capital is justified?

This tool provides a structured way to answer those questions probabilistically instead of relying on intuition.



Key Parameters

Historical lookback window (chosen number of your choice, default 120)  
Simulation horizon in trading days  
Number of simulated paths (chosen number of your liking preferably > 250,000 for time sake but still works)  
Target and stop levels  
Student-t degrees of freedom (fat-tail control)



Limitations

The model assumes constant volatility over the forecast window.  
It does not model volatility clustering or regime shifts.  
Transaction costs and slippage are ignored.  
It is not a standalone trading system.

This is a probabilistic risk model, not a prediction engine.





For research purposes only

