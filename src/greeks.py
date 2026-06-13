import numpy as np
from scipy.stats import norm


def compute_greeks(S, K, T, r, sigma, option_type="call"):
    """
    Compute the Black-Scholes Greeks for a European option.

    Parameters
    ----------
    S           : float - Current stock price
    K           : float - Strike price
    T           : float - Time to expiration in years
    r           : float - Risk-free interest rate (annual, decimal)
    sigma       : float - Volatility (annual, decimal)
    option_type : str   - "call" or "put"

    Returns
    -------
    dict with keys: delta, gamma, vega, theta, rho
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Gamma and Vega are identical for calls and puts
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega  = S * norm.pdf(d1) * np.sqrt(T) / 100  # per 1% move in volatility

    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
        rho   = K * T * np.exp(-r * T) * norm.cdf(d2) / 100

    elif option_type == "put":
        delta = norm.cdf(d1) - 1
        theta = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
        rho   = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100

    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return {
        "delta" : round(delta, 6),
        "gamma" : round(gamma, 6),
        "vega"  : round(vega,  6),
        "theta" : round(theta, 6),
        "rho"   : round(rho,   6)
    }


if __name__ == "__main__":
    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

    for option_type in ["call", "put"]:
        greeks = compute_greeks(S, K, T, r, sigma, option_type)

        print(f"\n--- {option_type.upper()} GREEKS ---")
        print(f"Delta : {greeks['delta']:>10}  (price change per $1 move in stock)")
        print(f"Gamma : {greeks['gamma']:>10}  (delta change per $1 move in stock)")
        print(f"Vega  : {greeks['vega']:>10}  (price change per 1% move in volatility)")
        print(f"Theta : {greeks['theta']:>10}  (price change per day)")
        print(f"Rho   : {greeks['rho']:>10}  (price change per 1% move in rate)")