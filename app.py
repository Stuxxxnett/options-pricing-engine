import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from black_scholes import black_scholes
from monte_carlo import monte_carlo_option_price
from greeks import compute_greeks

# Page config
st.set_page_config(
    page_title="Options Pricing Engine",
    page_icon="chart_with_upward_trend",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #0f1117; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        h1 { color: #ffffff; font-weight: 700; }
        h2, h3 { color: #e0e0e0; }
        .stMetric {
            background-color: #1e2130;
            border: 1px solid #2e3250;
            border-radius: 10px;
            padding: 1rem;
        }
        .stMetric label { color: #a0a0b0 !important; font-size: 0.85rem !important; }
        .stMetric div { color: #ffffff !important; font-size: 1.4rem !important; }
        .info-box {
            background-color: #1e2130;
            border-left: 4px solid #4a90d9;
            border-radius: 6px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            color: #c8ccd8;
            font-size: 0.92rem;
            line-height: 1.6;
        }
        .section-divider {
            border: none;
            border-top: 1px solid #2e3250;
            margin: 2rem 0;
        }
        .greek-card {
            background-color: #1e2130;
            border: 1px solid #2e3250;
            border-radius: 10px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.5rem;
            color: #c8ccd8;
            font-size: 0.88rem;
        }
        .tag {
            display: inline-block;
            background-color: #2e3250;
            color: #a0b0ff;
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 0.78rem;
            margin-right: 4px;
        }
    </style>
""", unsafe_allow_html=True)


# Header
st.markdown("# Options Pricing Engine")
st.markdown("""
<div class="info-box">
    A quantitative finance tool for pricing European options using two independent methods:
    the closed-form <b>Black-Scholes formula</b> and <b>Monte Carlo simulation</b>.
    Adjust the parameters in the sidebar and explore how option prices and risk sensitivities
    respond to changing market conditions.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<span class="tag">Black-Scholes</span>
<span class="tag">Monte Carlo</span>
<span class="tag">Greeks</span>
<span class="tag">Stochastic Modeling</span>
<span class="tag">Derivatives Pricing</span>
""", unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown("## Parameters")
    st.markdown("Adjust these values to see how the option price and Greeks respond.")

    st.markdown("---")
    st.markdown("**Underlying Asset**")
    S = st.number_input("Current Stock Price (S)", min_value=1.0, max_value=10000.0, value=100.0, step=1.0)
    K = st.number_input("Strike Price (K)", min_value=1.0, max_value=10000.0, value=100.0, step=1.0)

    st.markdown("**Contract Details**")
    T = st.slider("Time to Expiry (years)", min_value=0.01, max_value=5.0, value=1.0, step=0.01)
    option_type = st.radio("Option Type", ["Call", "Put"], horizontal=True)

    st.markdown("**Market Conditions**")
    sigma = st.slider("Volatility — sigma (%)", min_value=1, max_value=100, value=20, step=1) / 100
    r = st.slider("Risk-Free Rate (%)", min_value=0, max_value=20, value=5, step=1) / 100

    st.markdown("**Monte Carlo Settings**")
    n_simulations = st.select_slider(
        "Number of Simulations",
        options=[1000, 5000, 10000, 50000, 100000],
        value=100000
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.78rem; color:#6a6a8a; line-height:1.5'>
    S — spot price of the underlying asset<br>
    K — price at which option can be exercised<br>
    T — time remaining until expiration<br>
    sigma — annualized volatility of the asset<br>
    r — annualized risk-free interest rate
    </div>
    """, unsafe_allow_html=True)


option_type_lower = option_type.lower()

# Compute
bs_price = black_scholes(S, K, T, r, sigma, option_type_lower)
mc       = monte_carlo_option_price(S, K, T, r, sigma, option_type_lower, n_simulations)
greeks   = compute_greeks(S, K, T, r, sigma, option_type_lower)

difference = abs(bs_price - mc["price"])


# Pricing Results
st.markdown("## Pricing Results")
st.markdown("""
<div class="info-box">
    Black-Scholes gives an exact analytical price derived from a closed-form equation.
    Monte Carlo independently estimates the same price by simulating thousands of random
    future stock paths. Agreement between both methods validates the result.
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Black-Scholes Price", f"${bs_price:.4f}")
col2.metric("Monte Carlo Price",   f"${mc['price']:.4f}")
col3.metric("Difference",          f"${difference:.4f}")
col4.metric("MC Std Error",        f"{mc['std_error']:.5f}")

ci = mc["confidence_interval"]
st.markdown(f"""
<div class="info-box" style="margin-top:1rem">
    <b>95% Confidence Interval</b> &nbsp;|&nbsp;
    Lower: <b>${ci[0]:.4f}</b> &nbsp;&mdash;&nbsp; Upper: <b>${ci[1]:.4f}</b> &nbsp;|&nbsp;
    The Black-Scholes price falls <b>{'inside' if ci[0] <= bs_price <= ci[1] else 'outside'}</b> this interval.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)


# Greeks
st.markdown("## The Greeks")
st.markdown("""
<div class="info-box">
    Greeks measure the sensitivity of the option price to changes in market variables.
    They are essential for hedging and risk management on trading desks.
</div>
""", unsafe_allow_html=True)

gcol1, gcol2, gcol3, gcol4, gcol5 = st.columns(5)

gcol1.metric(
    "Delta",
    f"{greeks['delta']:.4f}",
    help="Price change per $1 move in the stock"
)
gcol2.metric(
    "Gamma",
    f"{greeks['gamma']:.4f}",
    help="Rate of change of Delta per $1 move in stock"
)
gcol3.metric(
    "Vega",
    f"{greeks['vega']:.4f}",
    help="Price change per 1% move in volatility"
)
gcol4.metric(
    "Theta",
    f"{greeks['theta']:.4f}",
    help="Price decay per calendar day"
)
gcol5.metric(
    "Rho",
    f"{greeks['rho']:.4f}",
    help="Price change per 1% move in interest rate"
)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)


# Charts
st.markdown("## Sensitivity Analysis")
st.markdown("""
<div class="info-box">
    These charts show how the option price and Greeks evolve as the stock price moves
    from well below the strike to well above it. The dashed vertical line marks the
    current stock price you selected.
</div>
""", unsafe_allow_html=True)

S_range = np.linspace(max(1, S * 0.5), S * 1.5, 300)

call_prices   = [black_scholes(s, K, T, r, sigma, "call") for s in S_range]
put_prices    = [black_scholes(s, K, T, r, sigma, "put")  for s in S_range]
greeks_call   = [compute_greeks(s, K, T, r, sigma, "call") for s in S_range]
greeks_put    = [compute_greeks(s, K, T, r, sigma, "put")  for s in S_range]

tab1, tab2, tab3 = st.tabs(["Option Prices", "Greeks", "Monte Carlo Convergence"])

with tab1:
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#1e2130")
    ax.plot(S_range, call_prices, color="#4a90d9", linewidth=2, label="Call Price")
    ax.plot(S_range, put_prices,  color="#e05c5c", linewidth=2, label="Put Price")
    ax.axvline(S, color="#ffffff", linestyle="--", alpha=0.4, label=f"Current S = {S}")
    ax.axvline(K, color="#f0a500", linestyle=":",  alpha=0.6, label=f"Strike K = {K}")
    ax.set_title("Option Price vs Stock Price", color="#e0e0e0", pad=12)
    ax.set_xlabel("Stock Price (S)", color="#a0a0b0")
    ax.set_ylabel("Option Price ($)", color="#a0a0b0")
    ax.tick_params(colors="#a0a0b0")
    ax.legend(facecolor="#1e2130", labelcolor="#e0e0e0", framealpha=0.8)
    ax.grid(True, alpha=0.15, color="#ffffff")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2e3250")
    st.pyplot(fig)
    plt.close()

with tab2:
    greek_keys   = ["delta", "gamma", "vega", "theta"]
    greek_labels = ["Delta", "Gamma", "Vega", "Theta"]

    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    fig.patch.set_facecolor("#0f1117")
    axes = axes.flatten()

    for i, (key, label) in enumerate(zip(greek_keys, greek_labels)):
        ax = axes[i]
        ax.set_facecolor("#1e2130")
        ax.plot(S_range, [g[key] for g in greeks_call], color="#4a90d9", linewidth=2, label="Call")
        ax.plot(S_range, [g[key] for g in greeks_put],  color="#e05c5c", linewidth=2, label="Put")
        ax.axvline(S, color="#ffffff", linestyle="--", alpha=0.4)
        ax.axvline(K, color="#f0a500", linestyle=":",  alpha=0.5)
        ax.set_title(f"{label} vs Stock Price", color="#e0e0e0", pad=8)
        ax.set_xlabel("Stock Price (S)", color="#a0a0b0", fontsize=9)
        ax.set_ylabel(label, color="#a0a0b0", fontsize=9)
        ax.tick_params(colors="#a0a0b0")
        ax.legend(facecolor="#1e2130", labelcolor="#e0e0e0", framealpha=0.8, fontsize=8)
        ax.grid(True, alpha=0.15, color="#ffffff")
        for spine in ax.spines.values():
            spine.set_edgecolor("#2e3250")

    plt.suptitle("Option Greeks vs Stock Price", color="#e0e0e0", fontsize=13, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with tab3:
    sim_counts = [100, 500, 1000, 5000, 10000, 50000, 100000]
    mc_prices, ci_lowers, ci_uppers = [], [], []

    with st.spinner("Running simulations..."):
        for n in sim_counts:
            mc_n = monte_carlo_option_price(S, K, T, r, sigma, option_type_lower, n_simulations=n)
            mc_prices.append(mc_n["price"])
            ci_lowers.append(mc_n["confidence_interval"][0])
            ci_uppers.append(mc_n["confidence_interval"][1])

    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#1e2130")
    ax.semilogx(sim_counts, mc_prices, color="#4a90d9", linewidth=2, marker="o", label="MC Price")
    ax.semilogx(sim_counts, ci_lowers, color="#4a90d9", linewidth=1, linestyle="--", alpha=0.4)
    ax.semilogx(sim_counts, ci_uppers, color="#4a90d9", linewidth=1, linestyle="--", alpha=0.4, label="95% CI")
    ax.fill_between(sim_counts, ci_lowers, ci_uppers, alpha=0.1, color="#4a90d9")
    ax.axhline(bs_price, color="#e05c5c", linewidth=2, linestyle="-", label=f"BS Price ${bs_price:.4f}")
    ax.set_title("Monte Carlo Convergence to Black-Scholes", color="#e0e0e0", pad=12)
    ax.set_xlabel("Number of Simulations (log scale)", color="#a0a0b0")
    ax.set_ylabel(f"{option_type} Price ($)", color="#a0a0b0")
    ax.tick_params(colors="#a0a0b0")
    ax.legend(facecolor="#1e2130", labelcolor="#e0e0e0", framealpha=0.8)
    ax.grid(True, alpha=0.15, color="#ffffff")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2e3250")
    st.pyplot(fig)
    plt.close()

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)


# About
st.markdown("## About This Project")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    <div class="info-box">
        <b>Black-Scholes Model</b><br><br>
        Derived in 1973 by Fischer Black and Myron Scholes, this formula gives the
        theoretical price of a European option assuming log-normally distributed returns,
        constant volatility, and no arbitrage.<br><br>
        <code>C = S·N(d1) - K·e^(-rT)·N(d2)</code><br>
        <code>d1 = [ln(S/K) + (r + s²/2)T] / (s·√T)</code><br>
        <code>d2 = d1 - s·√T</code>
    </div>
    """, unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="info-box">
        <b>Monte Carlo Simulation</b><br><br>
        Instead of a formula, Monte Carlo simulates thousands of possible future stock
        prices using geometric Brownian motion, computes the option payoff for each path,
        and averages them. As simulations increase, the estimate converges to the
        Black-Scholes price.<br><br>
        <code>S_T = S · exp((r - s²/2)T + s·√T·Z)</code><br>
        <code>Z ~ N(0, 1)</code>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; color:#4a4a6a; font-size:0.8rem; margin-top:2rem'>
    Built with Python — NumPy, SciPy, Matplotlib, Streamlit
</div>
""", unsafe_allow_html=True)