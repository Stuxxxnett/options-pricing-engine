import numpy as np
from scipy.stats import norm
from black_scholes import black_scholes


def vega(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes vega (sensitivity of price to volatility).

    Parameters
    ----------
    S     : float - Current stock price
    K     : float - Strike price
    T     : float - Time to expiration in years
    r     : float - Risk-free interest rate (annual, decimal)
    sigma : float - Volatility of the underlying asset (annual, decimal)

    Returns
    -------
    float : Vega (price change per 1.00 change in sigma)
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return S * norm.pdf(d1) * np.sqrt(T)


def implied_volatility(market_price, S, K, T, r, option_type="call",
                        tol=1e-6, max_iter=100):
    """
    Solve for the implied volatility that recovers a given market price,
    using Newton-Raphson with a bisection fallback for robustness.

    Parameters
    ----------
    market_price : float - Observed market price of the option
    S            : float - Current stock price
    K            : float - Strike price
    T            : float - Time to expiration in years
    r            : float - Risk-free interest rate (annual, decimal)
    option_type  : str   - "call" or "put"
    tol          : float - Convergence tolerance on price error
    max_iter     : int   - Maximum iterations for each method

    Returns
    -------
    float : Implied volatility (annual, decimal)
    """
    sigma = 0.3  # initial guess

    # Newton-Raphson
    for _ in range(max_iter):
        price = black_scholes(S, K, T, r, sigma, option_type)
        diff = price - market_price

        if abs(diff) < tol:
            return sigma

        v = vega(S, K, T, r, sigma)
        if v < 1e-8:
            break  # vega too small, switch to bisection

        sigma -= diff / v
        if sigma <= 0:
            break  # Newton-Raphson stepped into invalid territory

    # Bisection fallback (robust, guaranteed to converge if bracket is valid)
    low, high = 1e-4, 5.0
    for _ in range(max_iter):
        mid = (low + high) / 2
        price = black_scholes(S, K, T, r, mid, option_type)
        diff = price - market_price

        if abs(diff) < tol:
            return mid
        if diff > 0:
            high = mid
        else:
            low = mid

    return mid  # best estimate after max_iter if exact tolerance not hit


if __name__ == "__main__":
    # Sample parameters
    S = 100      # Stock price
    K = 100      # Strike price
    T = 1        # 1 year to expiry
    r = 0.05     # 5% risk-free rate
    true_sigma = 0.2  # 20% volatility used to generate the "market" price

    market_call_price = black_scholes(S, K, T, r, true_sigma, "call")
    market_put_price = black_scholes(S, K, T, r, true_sigma, "put")

    recovered_call_iv = implied_volatility(market_call_price, S, K, T, r, "call")
    recovered_put_iv = implied_volatility(market_put_price, S, K, T, r, "put")

    print(f"True Volatility        : {true_sigma:.4f}")
    print(f"Recovered IV (Call)    : {recovered_call_iv:.4f}")
    print(f"Recovered IV (Put)     : {recovered_put_iv:.4f}")
    print(f"Call IV Error          : {abs(recovered_call_iv - true_sigma):.2e}")
    print(f"Put IV Error           : {abs(recovered_put_iv - true_sigma):.2e}")