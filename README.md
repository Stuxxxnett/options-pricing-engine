# Options Pricing Engine

A Python-based quantitative finance tool that prices European options using two independent methods — the closed-form Black-Scholes formula and Monte Carlo simulation — then compares them. Includes computation of all five major Greeks for risk analysis.

---

## Methods Implemented

### Black-Scholes Model
Closed-form analytical solution for European option pricing based on the assumption of log-normally distributed asset returns and constant volatility.

### Monte Carlo Simulation
Stochastic simulation of 100,000 terminal stock price paths using geometric Brownian motion. Produces a price estimate with standard error and 95% confidence interval.

### The Greeks
Analytical sensitivity measures derived from the Black-Scholes model:

| Greek | Measures |
|-------|----------|
| Delta | Price sensitivity to underlying asset price change |
| Gamma | Rate of change of Delta |
| Vega  | Price sensitivity to volatility change |
| Theta | Price decay per day |
| Rho   | Price sensitivity to interest rate change |

---

## Sample Results

Parameters used: S = 100, K = 100, T = 1 year, r = 5%, sigma = 20%

### Pricing Comparison

| Method        | Call Price | Put Price |
|---------------|------------|-----------|
| Black-Scholes | $10.4506   | $5.5735   |
| Monte Carlo   | $10.4205   | $5.6122   |
| Difference    | $0.0301    | $0.0387   |

Monte Carlo standard error: 0.04677 (call), 0.02752 (put)  
Monte Carlo 95% CI (call): ($10.3289, $10.5122)  
Put-Call Parity check: confirmed (error < 1e-10)

### Greeks at S = 100

| Greek | Call    | Put     |
|-------|---------|---------|
| Delta |  0.6368 | -0.3632 |
| Gamma |  0.0188 |  0.0188 |
| Vega  |  0.3752 |  0.3752 |
| Theta | -0.0176 | -0.0045 |
| Rho   |  0.5323 | -0.4189 |

---

## Project Structure

```
options-pricing-engine/
├── src/
│   ├── black_scholes.py   — Closed-form BS pricing
│   ├── monte_carlo.py     — Monte Carlo simulation engine
│   ├── greeks.py          — Greeks computation
│   └── analysis.py        — Visualization and comparison
├── outputs/               — Generated charts (gitignored)
├── tests/
└── README.md
```

---

## Visualizations

### Option Price vs Stock Price
Call and put prices plotted across a range of stock prices (S = 50 to 150), with strike price marked.

### Greeks vs Stock Price
Four-panel plot showing Delta, Gamma, Vega, and Theta for both call and put options across the same stock price range.

### Monte Carlo Convergence
Log-scale convergence plot showing Monte Carlo price approaching the Black-Scholes value as simulations increase from 100 to 100,000, with 95% confidence interval bands.

---

## Setup and Usage

Requirements: Python 3.10+

```bash
git clone https://github.com/YOUR_USERNAME/options-pricing-engine.git
cd options-pricing-engine
python -m venv venv
venv\Scripts\activate
pip install numpy scipy matplotlib plotly streamlit
```

Run individual modules:

```bash
cd src
python black_scholes.py    # BS pricing + parity check
python monte_carlo.py      # MC simulation + comparison
python greeks.py           # Greeks computation
python analysis.py         # Generate all charts
```

---

## Key Concepts

### Black-Scholes Formula

The price of a European call option is given by:

```
C = S * N(d1) - K * e^(-rT) * N(d2)

d1 = [ln(S/K) + (r + sigma^2/2) * T] / (sigma * sqrt(T))
d2 = d1 - sigma * sqrt(T)
```

### Geometric Brownian Motion (Monte Carlo)

Each simulated terminal stock price follows:

```
S_T = S * exp((r - sigma^2/2) * T + sigma * sqrt(T) * Z)
```

where Z ~ N(0,1)

---

## Resume Keywords

Stochastic modeling, Monte Carlo simulation, derivatives pricing, numerical methods, Black-Scholes model, options Greeks, risk analysis, quantitative finance, NumPy, SciPy, Python