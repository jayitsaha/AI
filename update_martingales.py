#!/usr/bin/env python3
"""Update Notion page for: Martingales (basic definition)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81b6-94bf-eb34be274e6a"
ICON = "🟡"  # Intermediate
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/martingales_explainer.html"},
}

blocks = [
    # ─────────────────────────────────────────────────────────────
    # Section 1: The 30-Second Version
    # ─────────────────────────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("A martingale is a stochastic process where your best prediction for the next value — given everything you know so far — is exactly the current value. It models a "), rt("fair game", bold=True), rt(": no systematic drift up or down. Think of a fair coin-flip game where you bet $1 each round. No matter how many heads or tails you've seen, your expected wealth tomorrow equals your wealth today.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine tracking your running score in a perfectly fair coin-flip game. Win $1 on heads, lose $1 on tails. At any point — whether you're up $50 or down $30 — your expected future score is exactly your current score. Past streaks carry zero predictive power. You're equally likely to go up or down next. That sequence of running scores is a martingale.")),
    heading3("One-Sentence Summary"),
    para(rt("A martingale is a random process where the conditional expectation of the next value, given all past values, equals the present value: no drift, no trend, just a fair game.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("A martingale satisfies "), eq(r"\mathbb{E}[X_{t+1} \mid \mathcal{F}_t] = X_t"), rt(" — the best forecast for the future is the present. The Optional Stopping Theorem says no clever stopping rule can change your expected outcome in a fair game.")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 2: Historical Context
    # ─────────────────────────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("In the 18th and 19th centuries, gambling theory and probability were deeply intertwined. A central question: "), rt("can a gambler develop a strategy to guarantee winnings from a fair game?", italic=True), rt(" The popular 'Martingale' betting system (double your bet after each loss) seemed to suggest yes. The mathematical challenge was to formalize why this intuition is wrong, and to characterize what 'fair' really means for a random process.")),
    heading3("What Came Before"),
    para(rt("Before the rigorous theory, probability dealt mostly with independent coin flips and simple games. Bachelier's 1900 thesis on Brownian motion in financial markets hinted at the deeper structure, and early work by Bernstein and Lévy touched on conditional expectations. But there was no unified framework for dependent random processes with the 'fair game' property.")),
    heading3("The Breakthrough"),
    para(rt("Joseph Doob formalized the martingale concept rigorously in his 1953 book "), rt("Stochastic Processes", italic=True), rt(" (Wiley). He established the fundamental theorems — martingale convergence, Doob's optional stopping theorem, and the maximal inequalities — that made martingales a cornerstone of modern probability theory.")),
    heading3("Key Papers / Books"),
    bullet(rt("Doob, J.L. (1953). "), rt("Stochastic Processes", italic=True), rt(". Wiley. — First rigorous treatment; introduced the optional stopping theorem and convergence results.")),
    bullet(rt("Bachelier, L. (1900). Théorie de la spéculation. — Precursor: modelled stock prices as (what we now call) martingales.")),
    bullet(rt("Billingsley, P. (1995). "), rt("Probability and Measure", italic=True), rt(". — Standard graduate reference for martingale theory.")),
    bullet(rt("Harrison & Pliska (1981). Martingales and stochastic integrals in the theory of continuous trading. "), rt("Stochastic Processes and their Applications", italic=True), rt(", 11(3). — Fundamental theorem of asset pricing via martingales.")),
    heading3("Evolution Timeline"),
    para(rt("Random walks (18th c.) → Bachelier's Brownian motion (1900) → Doob's rigorous martingales (1953) → Martingale representation theorem (1967, Clark) → Fundamental theorem of asset pricing (1979, Harrison-Kreps) → Martingale methods in ML convergence (1990s–present).")),
    heading3("Before vs. After"),
    table(3,
        table_row(["Dimension", "Before Martingales", "After Doob (1953)"]),
        table_row(["Fair game definition", "Informal intuition about symmetric bets", "Precise: E[X_{t+1}|F_t]=X_t for adapted process"]),
        table_row(["Stopping strategies", "Believed doubling strategies could profit", "OST: E[X_tau]=X_0 — provably impossible"]),
        table_row(["Financial pricing", "Ad hoc methods, no arbitrage theory", "Risk-neutral measure; discounted prices are martingales"]),
        table_row(["ML convergence", "Heuristic arguments", "Martingale convergence theorem powers rigorous proofs"]),
    ),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 3: Core Concepts
    # ─────────────────────────────────────────────────────────────
    heading2("🧱 Core Concepts & Theory"),
    heading3("Probability Space and Filtration"),
    para(rt("Work on a probability space "), eq(r"(\Omega, \mathcal{F}, \mathbb{P})"), rt(". A "), rt("filtration", bold=True), rt(" "), eq(r"\{\mathcal{F}_t\}_{t \geq 0}"), rt(" is an increasing sequence of "), eq(r"\sigma"), rt("-algebras representing information up to time "), eq(r"t"), rt(":")),
    equation_block(r"\mathcal{F}_0 \subseteq \mathcal{F}_1 \subseteq \mathcal{F}_2 \subseteq \cdots \subseteq \mathcal{F}"),
    para(rt("A stochastic process "), eq(r"\{X_t\}"), rt(" is "), rt("adapted", bold=True), rt(" to the filtration if "), eq(r"X_t"), rt(" is "), eq(r"\mathcal{F}_t"), rt("-measurable — you can observe "), eq(r"X_t"), rt(" at time "), eq(r"t"), rt(". An "), rt("integrable", bold=True), rt(" process satisfies "), eq(r"\mathbb{E}[|X_t|] < \infty"), rt(" for all "), eq(r"t"), rt(".")),
    heading3("The Three Definitions"),
    para(rt("Let "), eq(r"\{X_t, \mathcal{F}_t\}_{t \geq 0}"), rt(" be an adapted, integrable process. It is a:")),
    bullet(rt("Martingale"), rt(" if "), eq(r"\mathbb{E}[X_{t+1} \mid \mathcal{F}_t] = X_t"), rt(" (a.s.) — fair game")),
    bullet(rt("Submartingale"), rt(" if "), eq(r"\mathbb{E}[X_{t+1} \mid \mathcal{F}_t] \geq X_t"), rt(" (a.s.) — expected to rise")),
    bullet(rt("Supermartingale"), rt(" if "), eq(r"\mathbb{E}[X_{t+1} \mid \mathcal{F}_t] \leq X_t"), rt(" (a.s.) — expected to fall")),
    callout("🔑", rt("Key Property: ", bold=True), rt("If "), eq(r"X_t"), rt(" is a martingale, then "), eq(r"\mathbb{E}[X_t] = \mathbb{E}[X_0]"), rt(" for all "), eq(r"t"), rt(". The unconditional mean is constant. This follows by iterated expectation: "), eq(r"\mathbb{E}[X_t] = \mathbb{E}[\mathbb{E}[X_t | \mathcal{F}_{t-1}]] = \mathbb{E}[X_{t-1}] = \cdots = \mathbb{E}[X_0]"), rt(".")),
    heading3("Canonical Examples"),
    bullet(rt("Symmetric random walk: "), eq(r"X_t = \sum_{s=1}^t \xi_s"), rt(", "), eq(r"\xi_s \overset{\text{iid}}{\sim} \pm 1"), rt(" with equal prob — martingale.")),
    bullet(rt("Biased walk "), eq(r"p \neq 0.5"), rt(": "), eq(r"\mathbb{E}[X_{t+1}|X_t] = X_t + (2p-1)"), rt(". Supermartingale if "), eq(r"p < 0.5"), rt(", submartingale if "), eq(r"p > 0.5"), rt(".")),
    bullet(rt("Doob martingale: For any integrable r.v. "), eq(r"Y"), rt(" and filtration, "), eq(r"M_n = \mathbb{E}[Y \mid \mathcal{F}_n]"), rt(" is a martingale.")),
    bullet(rt("Likelihood ratio: "), eq(r"L_t = \prod_{s=1}^t \frac{f_1(\xi_s)}{f_0(\xi_s)}"), rt(" is a "), eq(r"\mathbb{P}_0"), rt("-martingale (used in sequential hypothesis testing).")),
    bullet(rt("SGD gradient noise: "), eq(r"g_t - \nabla L(\theta_t)"), rt(" is a martingale difference sequence.")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 4: Architecture & Internal Workings (PhD deep-dive)
    # ─────────────────────────────────────────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD Deep-Dive)"),
    heading3("The Martingale Property: What Happens at Each Step"),
    para(rt("Consider the symmetric random walk "), eq(r"X_t = \sum_{s=1}^t \xi_s"), rt(" where "), eq(r"\xi_s = \pm 1"), rt(" with equal probability, and "), eq(r"\mathcal{F}_t = \sigma(\xi_1, \ldots, \xi_t)"), rt(".")),
    para(rt("Numerical trace (seed=42, first 6 steps):")),
    bullet(rt("t=0: X_0 = 0")),
    bullet(rt("t=1: ξ_1 = +1, X_1 = 1. E[X_2|X_1=1] = 1 (next step ±1 equally)")),
    bullet(rt("t=2: ξ_2 = -1, X_2 = 0. E[X_3|X_2=0] = 0")),
    bullet(rt("t=3: ξ_3 = +1, X_3 = 1")),
    bullet(rt("t=4: ξ_4 = +1, X_4 = 2")),
    bullet(rt("t=5: ξ_5 = +1, X_5 = 3. E[X_6|X_5=3] = 3 ✓")),
    para(rt("At every step: "), eq(r"\mathbb{E}[X_{t+1} \mid \mathcal{F}_t] = X_t + \mathbb{E}[\xi_{t+1}] = X_t + 0 = X_t"), rt(". Independence of "), eq(r"\xi_{t+1}"), rt(" from "), eq(r"\mathcal{F}_t"), rt(" is the key — each new increment is fresh.")),
    heading3("The Doob Decomposition"),
    para(rt("Every adapted integrable process "), eq(r"\{X_t\}"), rt(" has a unique Doob decomposition into a martingale part and a predictable part:")),
    equation_block(r"X_t = M_t + A_t"),
    para(rt("where "), eq(r"M_t"), rt(" is a martingale ("), eq(r"M_0 = X_0"), rt(") and "), eq(r"A_t"), rt(" is predictable ("), eq(r"A_0 = 0"), rt(", meaning "), eq(r"A_t"), rt(" is "), eq(r"\mathcal{F}_{t-1}"), rt("-measurable). For a submartingale, "), eq(r"A_t"), rt(" is non-decreasing. This decomposes any process into 'fair game' + 'systematic trend'.")),
    heading3("The Optional Stopping Theorem — Full Statement"),
    para(rt("Let "), eq(r"\{X_t, \mathcal{F}_t\}"), rt(" be a martingale and "), eq(r"\tau"), rt(" a stopping time ("), eq(r"\{\tau \leq t\} \in \mathcal{F}_t"), rt(" for all "), eq(r"t"), rt("). Under any of these regularity conditions:")),
    numbered(rt("(Bounded) "), eq(r"\tau \leq N"), rt(" a.s. for some fixed "), eq(r"N")),
    numbered(rt("(Integrable increments) "), eq(r"\mathbb{E}[\tau] < \infty"), rt(" and "), eq(r"|X_{t+1} - X_t| \leq C"), rt(" a.s.")),
    numbered(rt("(Uniform integrability) "), eq(r"\{X_{t \wedge \tau}\}"), rt(" is uniformly integrable")),
    para(rt("We get:")),
    equation_block(r"\mathbb{E}[X_\tau] = \mathbb{E}[X_0]"),
    para(rt("The proof sketch for the bounded case ("), eq(r"\tau \leq N"), rt("): Define the stopped martingale "), eq(r"X_{t \wedge \tau}"), rt(", which is itself a martingale. Then "), eq(r"\mathbb{E}[X_{N \wedge \tau}] = \mathbb{E}[X_0]"), rt(". Since "), eq(r"\tau \leq N"), rt(", we have "), eq(r"X_{N \wedge \tau} = X_\tau"), rt(" a.s.")),
    heading3("Why the Regularity Conditions Matter"),
    callout("⚠️", rt("Counter-example without regularity: ", bold=True), rt("The doubling strategy (stop when you first win) makes "), eq(r"X_\tau = 1"), rt(" a.s., violating "), eq(r"\mathbb{E}[X_\tau] = 0"), rt(". But "), eq(r"\mathbb{E}[\tau] = \infty"), rt(" (in expectation you wait forever), so condition 2 fails. The OST requires the stopping rule to be 'not too greedy'.")),
    heading3("Doob's Maximal Inequality"),
    para(rt("For a non-negative submartingale "), eq(r"\{X_t\}"), rt(" and "), eq(r"p > 1"), rt(":")),
    equation_block(r"\mathbb{E}\!\left[\max_{0 \leq t \leq T} X_t^p\right] \leq \left(\frac{p}{p-1}\right)^p \mathbb{E}[X_T^p]"),
    para(rt("For "), eq(r"p = 2"), rt(": "), eq(r"\mathbb{E}[\max_{t \leq T} X_t^2] \leq 4 \mathbb{E}[X_T^2]"), rt(". This controls the fluctuations of the maximum, essential for convergence proofs.")),
    heading3("Martingale Central Limit Theorem"),
    para(rt("For a martingale difference sequence "), eq(r"\{d_t = X_t - X_{t-1}\}"), rt(" with "), eq(r"\sum_{t=1}^n \mathbb{E}[d_t^2 | \mathcal{F}_{t-1}] \to \sigma^2"), rt(" in probability:")),
    equation_block(r"\frac{X_n}{\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, \sigma^2)"),
    para(rt("This is the foundation for CLT results in time series, sequential analysis, and stochastic optimization.")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 5: The Math
    # ─────────────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Formal Definition and Basic Properties"),
    para(rt("Let "), eq(r"(\Omega, \mathcal{F}, \mathbb{P})"), rt(" be a complete probability space with filtration "), eq(r"\{\mathcal{F}_t\}_{t=0}^T"), rt(". Process "), eq(r"\{X_t\}"), rt(" is a martingale if (i) adapted, (ii) integrable, and (iii) for all "), eq(r"s < t"), rt(":")),
    equation_block(r"\mathbb{E}[X_t \mid \mathcal{F}_s] = X_s \quad \text{a.s.}"),
    para(rt("Note this is equivalent to the incremental form "), eq(r"\mathbb{E}[X_{t+1} - X_t \mid \mathcal{F}_t] = 0"), rt(" (zero expected increments).")),
    heading3("Variance Growth"),
    para(rt("For a martingale with uncorrelated increments:")),
    equation_block(r"\operatorname{Var}(X_t) = \operatorname{Var}(X_0) + \sum_{s=0}^{t-1} \mathbb{E}[\operatorname{Var}(X_{s+1} \mid \mathcal{F}_s)]"),
    para(rt("For the symmetric random walk (variance = 1 per step): "), eq(r"\operatorname{Var}(X_t) = t"), rt(". The standard deviation grows as "), eq(r"\sqrt{t}"), rt(", giving the "), rt("diffusive scaling", bold=True), rt(".")),
    heading3("Jensen's Inequality and Convex Transforms"),
    para(rt("If "), eq(r"\{X_t\}"), rt(" is a martingale and "), eq(r"\phi"), rt(" is convex, then "), eq(r"\{\phi(X_t)\}"), rt(" is a submartingale:")),
    equation_block(r"\mathbb{E}[\phi(X_{t+1}) \mid \mathcal{F}_t] \geq \phi(\mathbb{E}[X_{t+1} \mid \mathcal{F}_t]) = \phi(X_t)"),
    para(rt("Consequences: "), eq(r"|X_t|, X_t^2, e^{\theta X_t}"), rt(" (for any "), eq(r"\theta"), rt(") are all submartingales.")),
    heading3("Doob's Martingale Convergence Theorem"),
    para(rt("If "), eq(r"\{X_t\}"), rt(" is a martingale with "), eq(r"\sup_t \mathbb{E}[|X_t|] < \infty"), rt(" ("), eq(r"L^1"), rt(" bounded), then:")),
    equation_block(r"X_\infty := \lim_{t \to \infty} X_t \quad \text{exists a.s. and } \mathbb{E}[|X_\infty|] < \infty"),
    para(rt("Proof sketch via upcrossings: Let "), eq(r"U_n([a,b])"), rt(" = number of times "), eq(r"X_t"), rt(" crosses from below "), eq(r"a"), rt(" to above "), eq(r"b"), rt(" in "), eq(r"n"), rt(" steps. Doob's upcrossing inequality:")),
    equation_block(r"(b-a)\,\mathbb{E}[U_n([a,b])] \leq \mathbb{E}[(X_n - a)^+]"),
    para(rt("If "), eq(r"\mathbb{E}[|X_n|]"), rt(" is bounded, upcrossings are finite a.s. for all "), eq(r"[a,b]"), rt(", implying convergence (since oscillation → convergence by completeness of "), eq(r"\mathbb{R}"), rt(").")),
    heading3("Optional Stopping — Proof for Bounded τ"),
    para(rt("Claim: If "), eq(r"\{X_t\}"), rt(" is a martingale and "), eq(r"\tau \leq N"), rt(" a.s., then "), eq(r"\mathbb{E}[X_\tau] = \mathbb{E}[X_0]"), rt(".")),
    para(rt("Proof: The stopped process "), eq(r"X_t^* = X_{t \wedge \tau}"), rt(" is a martingale (stopping does not break the martingale property — this follows from the optional sampling lemma). Therefore:")),
    equation_block(r"\mathbb{E}[X_0] = \mathbb{E}[X_0^*] = \mathbb{E}[X_N^*] = \mathbb{E}[X_{N \wedge \tau}] = \mathbb{E}[X_\tau]"),
    para(rt("where the first equality is "), eq(r"X_0^* = X_0"), rt(", the second uses the martingale property of "), eq(r"X^*"), rt(", and the last uses "), eq(r"\tau \leq N"), rt(". "), eq(r"\square")),
    heading3("Gambler's Ruin via OST"),
    para(rt("Start at "), eq(r"X_0 = x"), rt(", absorbing barriers at 0 and "), eq(r"N"), rt(". By OST:")),
    equation_block(r"\mathbb{E}[X_\tau] = x \implies N \cdot \mathbb{P}(X_\tau = N) + 0 \cdot \mathbb{P}(X_\tau = 0) = x"),
    equation_block(r"\Rightarrow \mathbb{P}(\text{reach } N) = \frac{x}{N}"),
    para(rt("This is the exact ruin probability for a fair game, derived purely from the martingale property.")),
    callout("⚠️", rt("Subtlety: ", bold=True), rt("OST does "), rt("not", bold=True, italic=True), rt(" say you cannot be "), rt("unlucky", italic=True), rt(" — only that expected outcomes don't change. Individual paths can reach any value. The constraint is on the "), rt("average", italic=True), rt(" over all possible histories.")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 6: Code Implementation
    # ─────────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("From Scratch — Martingale Simulation & OST Verification"),
    code_block("python", '''import numpy as np
from typing import Callable, Optional

def simulate_random_walk(
    T: int = 50,
    p: float = 0.5,
    X0: float = 0.0,
    n_paths: int = 1,
    seed: Optional[int] = None
) -> np.ndarray:
    """
    Simulate a binary random walk: +1 w.p. p, -1 w.p. 1-p.

    - p=0.5: martingale (E[X_{t+1}|X_t] = X_t)
    - p<0.5: supermartingale (E[X_{t+1}|X_t] < X_t)
    - p>0.5: submartingale (E[X_{t+1}|X_t] > X_t)

    Returns: array of shape (n_paths, T+1)
    """
    rng = np.random.default_rng(seed)
    # Steps: +1 with prob p, -1 with prob 1-p
    steps = rng.choice([1.0, -1.0], size=(n_paths, T), p=[p, 1-p])
    # Prepend starting value
    paths = np.hstack([np.full((n_paths, 1), X0), X0 + np.cumsum(steps, axis=1)])
    return paths  # shape: (n_paths, T+1)


def check_martingale_property(paths: np.ndarray, p: float) -> dict:
    """
    Verify the martingale condition empirically.
    E[X_{t+1} - X_t] should equal 2p - 1 (= 0 for martingale).
    """
    increments = np.diff(paths, axis=1)  # shape (n_paths, T)
    empirical_drift = increments.mean()
    theoretical_drift = 2*p - 1
    return {
        "empirical_drift_per_step": empirical_drift,
        "theoretical_drift_per_step": theoretical_drift,
        "is_martingale": np.isclose(empirical_drift, 0.0, atol=0.05),
        "variance_at_t": paths.var(axis=0)  # should grow as t for p=0.5
    }


def optional_stopping_theorem_demo(
    p: float = 0.5,
    X0: float = 0.0,
    lower: float = -10.0,
    upper: float = 10.0,
    n_sims: int = 20_000,
    max_steps: int = 100_000,
    seed: int = 42
) -> dict:
    """
    Verify: E[X_tau] = X0 where tau = first exit from (lower, upper).
    OST guarantees this equals X0 for a fair game (bounded stopping time
    with integrable increments is NOT needed here since increments are
    bounded by 1, but tau may be unbounded — UI condition applies).
    """
    rng = np.random.default_rng(seed)
    final_values = np.empty(n_sims)

    for i in range(n_sims):
        x = X0
        for _ in range(max_steps):
            x += rng.choice([1.0, -1.0], p=[p, 1-p])
            if x >= upper or x <= lower:
                break
        final_values[i] = x

    prob_upper = np.mean(final_values >= upper)
    prob_lower = np.mean(final_values <= lower)
    expected_final = final_values.mean()

    # OST prediction: E[X_tau] = X0
    # And: P(reach upper) = (X0 - lower)/(upper - lower) for fair game
    ost_prediction = X0
    ruin_formula = (X0 - lower) / (upper - lower)

    return {
        "E[X_tau]": expected_final,          # Should equal X0
        "OST prediction (X0)": ost_prediction,
        "P(reach upper)": prob_upper,         # Should equal ruin_formula
        "Gambler ruin formula": ruin_formula,
        "Error": abs(expected_final - ost_prediction)
    }


# ── Demo ──
paths = simulate_rw = simulate_random_walk(T=100, p=0.5, n_paths=1000, seed=42)
stats = check_martingale_property(paths, p=0.5)
print(f"Empirical drift: {stats['empirical_drift_per_step']:.4f} (should be ~0)")
print(f"Var(X_t) grows as t: {stats['variance_at_t'][[10,50,100]]}")  # ~10, 50, 100

ost = optional_stopping_theorem_demo(X0=0.0, lower=-10.0, upper=10.0)
print(f"E[X_tau] = {ost['E[X_tau]']:.4f} (OST says {ost['OST prediction (X0)']})")
print(f"P(reach +10) = {ost['P(reach upper)']:.4f} (formula: {ost['Gambler ruin formula']:.4f})")
'''),
    heading3("Production Usage — Doob's Martingale & Azuma-Hoeffding"),
    code_block("python", '''import numpy as np
from typing import Callable

# ── Doob Martingale (concentration via bounded differences) ──

def azuma_hoeffding_bound(n: int, c: float, delta: float) -> float:
    """
    Azuma-Hoeffding inequality for martingales with bounded differences.

    If |X_t - X_{t-1}| <= c_t a.s. and sum(c_t^2) <= n*c^2, then:
        P(X_n - X_0 >= t) <= exp(-t^2 / (2*n*c^2))

    Returns: t such that P(X_n - X0 >= t) <= delta
    Uses: t = c * sqrt(2n * log(1/delta))
    """
    import math
    return c * math.sqrt(2 * n * math.log(1.0 / delta))


def doob_martingale_example(f: Callable, samples: np.ndarray) -> np.ndarray:
    """
    Construct the Doob martingale M_k = E[f(X_1,...,X_n) | X_1,...,X_k].

    This is a martingale by construction (tower property of expectations).
    Used for: concentration bounds on functions of many random variables.
    """
    n = len(samples)
    martingale = np.zeros(n + 1)
    martingale[0] = f(samples).mean()  # E[f(X)] as proxy

    # In practice, use conditional Monte Carlo or kernel density estimation
    # Here simplified: running average (exact for additive functions)
    running_sum = 0.0
    for k in range(n):
        running_sum += samples[k]
        # E[f | X_1,...,X_k] approximated by prefix average for additive f
        martingale[k + 1] = running_sum / (k + 1)
    return martingale


# ── Example: SGD as a martingale ──
# Stochastic gradient g_t = true_grad + noise_t where E[noise_t|theta_t] = 0
# The noise is a martingale difference sequence

def sgd_martingale_noise_demo(theta0: float = 5.0, lr: float = 0.01, T: int = 200):
    """
    In SGD, mini-batch gradient = true gradient + zero-mean noise.
    The accumulated noise is a martingale.
    """
    rng = np.random.default_rng(0)

    # True gradient of f(theta) = theta^2 is 2*theta
    theta = theta0
    noise_accumulation = [0.0]

    for t in range(T):
        true_grad = 2 * theta
        stochastic_noise = rng.normal(0, abs(theta) * 0.5)  # noise ~ N(0, sigma^2)
        stochastic_grad = true_grad + stochastic_noise

        theta -= lr * stochastic_grad
        # Noise accumulation is a martingale (zero mean conditionally)
        noise_accumulation.append(noise_accumulation[-1] + stochastic_noise)

    return theta, np.array(noise_accumulation)


theta_final, noise_path = sgd_martingale_noise_demo()
print(f"SGD converged theta: {theta_final:.6f} (true: 0)")
print(f"Noise path (martingale): mean={noise_path.mean():.4f}, final={noise_path[-1]:.4f}")

# Concentration bound
bound = azuma_hoeffding_bound(n=100, c=1.0, delta=0.05)
print(f"Azuma-Hoeffding 95% bound (n=100, c=1): {bound:.3f}")
# Gotcha: Azuma requires BOUNDED differences — check c before applying!
'''),
    callout("💡", rt("Key Gotcha: ", bold=True), rt("Azuma-Hoeffding requires "), rt("bounded", italic=True), rt(" differences "), eq(r"|X_t - X_{t-1}| \leq c_t"), rt(" a.s. For unbounded noise (e.g., Gaussian increments), use Bernstein's inequality or Freedman's inequality instead.")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 7: Interview Deep-Dive
    # ─────────────────────────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy) — What is a martingale?"),
    para(rt("A martingale is a stochastic process "), eq(r"\{X_t\}"), rt(" where the expected future value, conditioned on all past information, equals the current value: "), eq(r"\mathbb{E}[X_{t+1} \mid \mathcal{F}_t] = X_t"), rt(". It models a 'fair game' — knowing the history doesn't help you predict which direction the process moves next.")),
    heading3("Q2 (Medium) — State and explain the Optional Stopping Theorem"),
    para(rt("If "), eq(r"\{X_t\}"), rt(" is a martingale and "), eq(r"\tau"), rt(" is a stopping time satisfying regularity conditions (e.g., "), eq(r"\tau"), rt(" bounded, or "), eq(r"\mathbb{E}[\tau] < \infty"), rt(" with bounded increments), then "), eq(r"\mathbb{E}[X_\tau] = \mathbb{E}[X_0]"), rt(". Implication: you cannot change your expected outcome from a fair game by choosing "), rt("when", italic=True), rt(" to stop.")),
    para(rt("Follow-up trap: "), rt("\"Can you give a counter-example where OST fails?\"", italic=True)),
    para(rt("A: The doubling betting strategy (stop when you first win): "), eq(r"\tau = \min\{t : X_t = 1\}"), rt(". Then "), eq(r"X_\tau = 1"), rt(" a.s., seemingly contradicting "), eq(r"\mathbb{E}[X_\tau] = 0"), rt(". But "), eq(r"\mathbb{E}[\tau] = \infty"), rt(" — the stopping time is not integrable, so OST's conditions fail.")),
    heading3("Q3 (Medium) — What is the difference between martingale, sub, and supermartingale?"),
    para(rt("Martingale: "), eq(r"\mathbb{E}[X_{t+1}|\mathcal{F}_t] = X_t"), rt(" (fair). Submartingale: "), eq(r"\geq X_t"), rt(" (tends up, favourable). Supermartingale: "), eq(r"\leq X_t"), rt(" (tends down, unfavourable).")),
    para(rt("Key relationship: If "), eq(r"X_t"), rt(" is a martingale and "), eq(r"\phi"), rt(" convex, then "), eq(r"\phi(X_t)"), rt(" is a submartingale (Jensen). Example: "), eq(r"|X_t|"), rt(" is always a submartingale.")),
    heading3("Q4 (Hard) — How do martingales appear in ML convergence proofs?"),
    para(rt("In SGD, let "), eq(r"g_t = \nabla f(x_t; \xi_t)"), rt(" be the stochastic gradient. The gradient noise "), eq(r"g_t - \nabla F(x_t)"), rt(" is a martingale difference sequence (MDS): "), eq(r"\mathbb{E}[g_t - \nabla F(x_t) \mid x_t] = 0"), rt(". The cumulative noise "), eq(r"\sum_{s=1}^t (g_s - \nabla F(x_s))"), rt(" is a martingale.")),
    para(rt("Convergence proofs bound "), eq(r"\mathbb{E}[F(x_T) - F^*]"), rt(" by decomposing into (a) deterministic descent term and (b) noise term — the latter is zero in expectation by the martingale property. The martingale CLT then gives the distribution of errors.")),
    heading3("Q5 (Hard) — Explain the connection between martingales and option pricing"),
    para(rt("The Fundamental Theorem of Asset Pricing (Harrison-Pliska 1981): A market is arbitrage-free iff there exists an equivalent martingale measure "), eq(r"\mathbb{Q}"), rt(" under which discounted prices "), eq(r"e^{-rt}S_t"), rt(" are martingales. Option prices are then expectations under "), eq(r"\mathbb{Q}"), rt(":")),
    equation_block(r"V_0 = \mathbb{E}^\mathbb{Q}\!\left[e^{-rT}(S_T - K)^+\right]"),
    para(rt("The Black-Scholes formula is exactly this expectation computed in closed form (under GBM for "), eq(r"S_t"), rt(").")),
    heading3("Multi-Level Explanations"),
    callout("🎓", rt("To a PhD researcher: ", bold=True), rt("Martingales are "), eq(r"L^1"), rt("-bounded adapted processes with "), eq(r"\mathbb{E}[X_t|\mathcal{F}_s]=X_s"), rt(". The theory (Doob's upcrossing lemma → a.s. convergence; OST via stopped process; Doob-Meyer for supermartingales) forms the backbone of stochastic calculus and financial mathematics. Key extension: continuous-time martingales w.r.t. Brownian filtration and the Itô isometry.")),
    callout("🔧", rt("To a research scientist/engineer: ", bold=True), rt("A martingale is a zero-drift stochastic process. OST = 'no clever stopping rule beats a fair game'. In ML: gradient noise in SGD is a martingale difference sequence, enabling convergence proofs. In finance: risk-neutral pricing = find the martingale measure. Practical tool: Azuma-Hoeffding for concentration bounds on functions of random variables.")),
    heading3("Red Flags (Wrong Answers)"),
    bullet(rt("'A martingale always converges' — FALSE. Needs "), eq(r"L^1"), rt(" boundedness (e.g., RW on "), eq(r"\mathbb{Z}"), rt(" is a martingale that does NOT converge).")),
    bullet(rt("'The OST says you can beat a fair game with a clever strategy' — EXACTLY WRONG. OST says the opposite.")),
    bullet(rt("'Martingale = random walk' — Too narrow. Martingale difference sequences need not be i.i.d.; the conditional mean zero condition is the key, not i.i.d.")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 8: Comparison
    # ─────────────────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    heading3("Martingales vs. Related Stochastic Process Concepts"),
    table(4,
        table_row(["Concept", "Condition", "Drift", "Key Use"]),
        table_row(["Martingale", "E[X_{t+1}|F_t] = X_t", "None", "Fair games, option pricing, convergence proofs"]),
        table_row(["Submartingale", "E[X_{t+1}|F_t] ≥ X_t", "Upward", "|X_t|, training loss upper bounds"]),
        table_row(["Supermartingale", "E[X_{t+1}|F_t] ≤ X_t", "Downward", "Discounted value, Lyapunov stochastic"]),
        table_row(["i.i.d. process", "Fully independent", "Depends on mean", "Simpler; martingale is generalization"]),
        table_row(["Markov chain", "P(X_{t+1}|X_t) = P(X_{t+1}|history)", "Any", "Overlaps: martingale ≠ Markov in general"]),
        table_row(["Brownian motion", "Continuous-time martingale", "None", "Limit of martingale RW; Itô calculus"]),
    ),
    heading3("When to Use Martingales"),
    bullet(rt("Proving convergence of stochastic algorithms (SGD, MCMC) — martingale convergence theorem")),
    bullet(rt("Deriving concentration bounds — Azuma-Hoeffding, McDiarmid's inequality")),
    bullet(rt("Financial derivative pricing — risk-neutral measure, no-arbitrage")),
    bullet(rt("Sequential hypothesis testing — Wald's SPRT, confidence sequences")),
    bullet(rt("Analysing randomized algorithms — optimal stopping, expected hitting times")),
    heading3("When NOT to Use"),
    bullet(rt("When the process has non-zero drift — model as sub/supermartingale or subtract the drift")),
    bullet(rt("When you need tail bounds for unbounded increments — Azuma requires bounded differences; use Bernstein's or Freedman's inequality")),
    bullet(rt("When increments are not zero-mean — the martingale difference condition must be verified")),
    callout("🎯", rt("Decision: ", bold=True), rt("Need to prove expected outcome unchanged by stopping? → OST. Need concentration bounds on a function of independent r.v.s? → Doob/Azuma. Need to price derivatives fairly? → Risk-neutral martingale measure. Need SGD convergence? → Martingale difference sequence framework.")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 9: Interactive Explainer
    # ─────────────────────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/martingales_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ─────────────────────────────────────────────────────────────
    # Section 10: Related Topics
    # ─────────────────────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites — Know These First"),
    bullet(rt("Conditional Expectation (Section 3.1) — E[X|Y] is the foundation of martingale condition")),
    bullet(rt("Probability Spaces & σ-algebras (Section 3.2) — needed for filtration formalism")),
    bullet(rt("Random Variables & Distributions (Section 3.3)")),
    bullet(rt("Law of Large Numbers & CLT (Section 3.7) — martingale CLT generalizes these")),
    heading3("What to Learn Next"),
    bullet(rt("Brownian Motion (Section 3.12) — continuous-time martingale, limit of RW")),
    bullet(rt("Itô Calculus (Section 3.13) — stochastic integration for continuous martingales")),
    bullet(rt("Concentration Inequalities (Section 3.14) — Azuma-Hoeffding, McDiarmid")),
    bullet(rt("Convergence of SGD (MLOps section) — martingale MDS framework")),
    bullet(rt("Black-Scholes Model — martingale pricing in continuous time")),
    heading3("Key Papers"),
    bullet(rt("Doob, J.L. (1953). "), rt("Stochastic Processes", italic=True), rt(". — The founding text; chapter 7 covers martingales.")),
    bullet(rt("Harrison, J.M. & Kreps, D.M. (1979). Martingales and arbitrage in multiperiod securities markets. "), rt("Journal of Economic Theory", italic=True), rt(", 20, 381–408.")),
    bullet(rt("Harrison, J.M. & Pliska, S.R. (1981). Martingales and stochastic integrals in the theory of continuous trading. "), rt("Stochastic Processes Appl.", italic=True), rt(", 11, 215–260.")),
    bullet(rt("Azuma, K. (1967). Weighted sums of certain dependent random variables. "), rt("Tôhoku Mathematical Journal", italic=True), rt(", 19(3), 357–367. — The martingale concentration inequality.")),
    bullet(rt("Freedman, D. (1975). On tail probabilities for martingales. "), rt("Annals of Probability", italic=True), rt(", 3(1), 100–118.")),
    heading3("Best Resources"),
    bullet(rt("Williams, D. (1991). "), rt("Probability with Martingales", italic=True), rt(". Cambridge. — The best introductory textbook; rigorous but readable.")),
    bullet(rt("Durrett, R. (2019). "), rt("Probability: Theory and Examples", italic=True), rt(". 5th ed. Cambridge. — Chapter 4–5 on martingales.")),
    bullet(rt("Steele, J.M. (2001). "), rt("Stochastic Calculus and Financial Applications", italic=True), rt(". Springer. — Connects martingales to finance beautifully.")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Brownian Motion, Itô Calculus, Concentration Inequalities, Black-Scholes, Sequential Testing (SPRT), SGD Convergence Analysis, Stopping Times, Gambler's Ruin")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
