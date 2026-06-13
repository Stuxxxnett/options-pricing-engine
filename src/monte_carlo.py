import numpy as np


def monte_carlo_option_price(S, K, T, r, sigma, option_type="call", n_simulations=100_000, seed=42):
    """
    Price a European option using Monte Carlo simulation.

    Parameters
    ----------
    S             : float - Current stock price
    K             : float - Strike price
    T             : float - Time to expiration in years
    r             : float - Risk-free interest rate (annual, decimal)
    sigma         : float - Volatility (annual, decimal)
    option_type   : str   - "call" or "put"
    n_simulations : int   - Number of simulated paths
    seed          : int   - Random seed for reproducibility

    Returns
    -------
    dict with keys: price, std_error, confidence_interval
    """
    rng = np.random.default_rng(seed)

    # Simulate terminal stock prices
    Z = rng.standard_normal(n_simulations)
    S_T = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    # Calculate payoffs
    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
    elif option_type == "put":
        payoffs = np.maximum(K - S_T, 0)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    # Discount payoffs to present value
    discounted_payoffs = np.exp(-r * T) * payoffs

    price      = np.mean(discounted_payoffs)
    std_error  = np.std(discounted_payoffs) / np.sqrt(n_simulations)
    ci_lower   = price - 1.96 * std_error
    ci_upper   = price + 1.96 * std_error

    return {
        "price"               : round(price, 4),
        "std_error"           : round(std_error, 6),
        "confidence_interval" : (round(ci_lower, 4), round(ci_upper, 4))
    }


if __name__ == "__main__":
    from black_scholes import black_scholes

    S, K, T, r, sigma = 100, 100, 1, 0.05, 0.2

    for option_type in ["call", "put"]:
        bs_price = black_scholes(S, K, T, r, sigma, option_type)
        mc       = monte_carlo_option_price(S, K, T, r, sigma, option_type)

        print(f"\n--- {option_type.upper()} OPTION ---")
        print(f"Black-Scholes Price : ${bs_price:.4f}")
        print(f"Monte Carlo Price   : ${mc['price']:.4f}")
        print(f"Std Error           : {mc['std_error']}")
        print(f"95% CI              : {mc['confidence_interval']}")
        print(f"Difference          : ${abs(bs_price - mc['price']):.4f}")