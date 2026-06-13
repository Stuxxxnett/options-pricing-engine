import numpy as np
from scipy.stats import norm


def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes price for a European option.

    Parameters
    ----------
    S     : float  - Current stock price
    K     : float  - Strike price
    T     : float  - Time to expiration in years
    r     : float  - Risk-free interest rate (annual, decimal)
    sigma : float  - Volatility of the underlying asset (annual, decimal)
    option_type : str - "call" or "put"

    Returns
    -------
    float : Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price


if __name__ == "__main__":
    # Sample parameters
    S = 100      # Stock price
    K = 100      # Strike price
    T = 1        # 1 year to expiry
    r = 0.05     # 5% risk-free rate
    sigma = 0.2  # 20% volatility

    call_price = black_scholes(S, K, T, r, sigma, "call")
    put_price  = black_scholes(S, K, T, r, sigma, "put")

    print(f"Call Price : ${call_price:.4f}")
    print(f"Put Price  : ${put_price:.4f}")

    # Verify put-call parity: C - P = S - K*e^(-rT)
    parity = call_price - put_price
    expected = S - K * np.exp(-r * T)
    print(f"\nPut-Call Parity Check")
    print(f"C - P        : {parity:.4f}")
    print(f"S - Ke^(-rT) : {expected:.4f}")
    print(f"Parity holds : {abs(parity - expected) < 1e-10}")