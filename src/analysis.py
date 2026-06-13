import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from black_scholes import black_scholes
from greeks import compute_greeks

def plot_price_vs_spot(K=100, T=1, r=0.05, sigma=0.2):
    S_range = np.linspace(50, 150, 300)

    call_prices = [black_scholes(S, K, T, r, sigma, "call") for S in S_range]
    put_prices  = [black_scholes(S, K, T, r, sigma, "put")  for S in S_range]

    plt.figure(figsize=(10, 5))
    plt.plot(S_range, call_prices, label="Call Price", color="steelblue", linewidth=2)
    plt.plot(S_range, put_prices,  label="Put Price",  color="tomato",    linewidth=2)
    plt.axvline(K, color="gray", linestyle="--", label=f"Strike K={K}")
    plt.title("Option Price vs Stock Price")
    plt.xlabel("Stock Price (S)")
    plt.ylabel("Option Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("../outputs/price_vs_spot.png", dpi=150)
    plt.show()
    print("Saved: price_vs_spot.png")


def plot_greeks_vs_spot(K=100, T=1, r=0.05, sigma=0.2):
    S_range = np.linspace(50, 150, 300)

    greeks_call = [compute_greeks(S, K, T, r, sigma, "call") for S in S_range]
    greeks_put  = [compute_greeks(S, K, T, r, sigma, "put")  for S in S_range]

    greek_names = ["delta", "gamma", "vega", "theta"]
    colors      = ["steelblue", "tomato"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    for i, greek in enumerate(greek_names):
        call_vals = [g[greek] for g in greeks_call]
        put_vals  = [g[greek] for g in greeks_put]

        axes[i].plot(S_range, call_vals, label="Call", color="steelblue", linewidth=2)
        axes[i].plot(S_range, put_vals,  label="Put",  color="tomato",    linewidth=2)
        axes[i].axvline(K, color="gray", linestyle="--", alpha=0.6)
        axes[i].set_title(f"{greek.capitalize()} vs Stock Price")
        axes[i].set_xlabel("Stock Price (S)")
        axes[i].set_ylabel(greek.capitalize())
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)

    plt.suptitle("Option Greeks vs Stock Price", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("../outputs/greeks_vs_spot.png", dpi=150)
    plt.show()
    print("Saved: greeks_vs_spot.png")


def plot_mc_convergence(S=100, K=100, T=1, r=0.05, sigma=0.2):
    from monte_carlo import monte_carlo_option_price
    from black_scholes import black_scholes

    bs_price   = black_scholes(S, K, T, r, sigma, "call")
    sim_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]
    mc_prices  = []
    ci_lowers  = []
    ci_uppers  = []

    for n in sim_counts:
        mc = monte_carlo_option_price(S, K, T, r, sigma, "call", n_simulations=n)
        mc_prices.append(mc["price"])
        ci_lowers.append(mc["confidence_interval"][0])
        ci_uppers.append(mc["confidence_interval"][1])

    plt.figure(figsize=(10, 5))
    plt.semilogx(sim_counts, mc_prices,  color="steelblue", linewidth=2, marker="o", label="MC Price")
    plt.semilogx(sim_counts, ci_lowers,  color="steelblue", linewidth=1, linestyle="--", alpha=0.5)
    plt.semilogx(sim_counts, ci_uppers,  color="steelblue", linewidth=1, linestyle="--", alpha=0.5, label="95% CI")
    plt.fill_between(sim_counts, ci_lowers, ci_uppers, alpha=0.1, color="steelblue")
    plt.axhline(bs_price, color="tomato", linewidth=2, linestyle="-", label=f"BS Price ${bs_price:.4f}")
    plt.title("Monte Carlo Convergence to Black-Scholes Price")
    plt.xlabel("Number of Simulations (log scale)")
    plt.ylabel("Call Option Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("../outputs/mc_convergence.png", dpi=150)
    plt.show()
    print("Saved: mc_convergence.png")


if __name__ == "__main__":
    plot_price_vs_spot()
    plot_greeks_vs_spot()
    plot_mc_convergence()
    print("\nAll plots generated successfully.")