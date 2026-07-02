#!/usr/bin/env python3
"""Update Notion page for: Random Walks — Part I / Section 3 / Subsection 3.11"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8131-8a9a-c837c99f06a9"
ICON = "🟡"   # Intermediate
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/random_walks_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [

    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("A random walk is the path of an object that takes a sequence of steps, where each step direction is chosen at random. The simplest version: flip a coin — heads means step right (+1), tails means step left (−1). Your position after n steps is the running sum of all those coin flips.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine a drunk person leaving a bar. Each second they take one step, but they have no control over direction — 50% left, 50% right. After 100 seconds, where are they? On average, right at the door (expected position = 0). But the spread of possible locations grows as √100 = 10 — they could easily be 10–20 steps away. This diffusive spreading is the signature of a random walk.")),
    heading3("One-Sentence Summary"),
    para(rt("A random walk is the cumulative sum of i.i.d. zero-mean steps; its expected position is always zero but its spread grows as √n, and it underpins diffusion, Brownian motion, and SGD noise.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("After n steps of ±1, E[Sₙ] = 0 (no drift) but E[|Sₙ|] ≈ √(2n/π) ≈ 0.798√n. The walk spreads diffusively as √n — not linearly, not logarithmically.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("In the early 20th century, physicists needed to model pollen particles jiggling in water (Brownian motion, observed by Robert Brown in 1827). Mathematicians needed to understand the long-run behavior of gambling games. Biologists needed models for genetic drift. All these phenomena share the same mathematical skeleton.")),
    heading3("Key Papers & Milestones"),
    bullet(rt("Louis Bachelier (1900) — ", bold=True), rt("Théorie de la spéculation. First mathematical treatment of random walks applied to stock prices. Predated Einstein's work on Brownian motion by 5 years.")),
    bullet(rt("Albert Einstein (1905) — ", bold=True), rt("Über die von der molekularkinetischen Theorie der Wärme geforderte Bewegung. Derived the diffusion equation from random walk assumptions; predicted Avogadro's number.")),
    bullet(rt("Marian Smoluchowski (1906) — ", bold=True), rt("Independent derivation of Brownian motion, giving the diffusion coefficient in terms of microscopic quantities.")),
    bullet(rt("George Pólya (1921) — ", bold=True), rt("Über eine Aufgabe der Wahrscheinlichkeitsrechnung betreffend die Irrfahrt im Strassennetz. Proved the recurrence theorem: simple random walk is recurrent in 1D and 2D, transient in 3D+.")),
    bullet(rt("Norbert Wiener (1923) — ", bold=True), rt("Differential-space. Rigorously constructed Brownian motion (Wiener process) as the continuous limit of a random walk.")),
    heading3("Evolution Timeline"),
    numbered(rt("Gambling / coin-flip analysis (Bernoulli, Pascal, 17th c.) → discrete combinatorial tools")),
    numbered(rt("Bachelier 1900 → finance application, CLT connection")),
    numbered(rt("Einstein / Smoluchowski 1905–06 → physics, diffusion equation")),
    numbered(rt("Pólya 1921 → recurrence theorem, graph theory")),
    numbered(rt("Wiener 1923 → rigorous continuous-time process")),
    numbered(rt("Lévy 1940s → stable processes, heavy-tailed generalizations")),
    numbered(rt("Modern ML → SGD noise, MCMC, PageRank, graph neural networks")),
    heading3("Before vs. After"),
    table(3,
        table_row(["Dimension", "Before (ad-hoc models)", "After (Random Walk framework)"]),
        table_row(["Diffusion", "Empirical Fick's law", "Derived from first principles via √n scaling"]),
        table_row(["Finance", "No rigorous model", "Brownian motion / GBM (Bachelier → Black-Scholes)"]),
        table_row(["Long-run behavior", "Unknown", "Recurrence / transience classified by dimension"]),
        table_row(["CLT connection", "Separate theorem", "Scaling limit S_n/√n → N(0,1) made explicit"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🔑 Core Concepts & Theory"),
    heading3("Formal Definition"),
    para(rt("Let "), eq(r"X_1, X_2, \ldots"), rt(" be i.i.d. random variables with "), eq(r"\Pr(X_i = +1) = \Pr(X_i = -1) = \tfrac{1}{2}"), rt(". The simple symmetric random walk is:")),
    equation_block(r"S_0 = 0, \qquad S_n = \sum_{k=1}^n X_k"),
    para(rt("More generally, steps can have any distribution with finite mean and variance: "), eq(r"\mathbb{E}[X_k] = \mu"), rt(" (drift) and "), eq(r"\operatorname{Var}(X_k) = \sigma^2"), rt(". The simple symmetric case has "), eq(r"\mu = 0,\; \sigma^2 = 1"), rt(".")),
    heading3("Key Properties"),
    bullet(rt("Mean: ", bold=True), eq(r"\mathbb{E}[S_n] = n\mu = 0"), rt(" (symmetric case)")),
    bullet(rt("Variance: ", bold=True), eq(r"\operatorname{Var}(S_n) = n\sigma^2 = n"), rt(" — grows linearly")),
    bullet(rt("Second moment: ", bold=True), eq(r"\mathbb{E}[S_n^2] = n"), rt(" — confirms √n spread")),
    bullet(rt("Markov property: ", bold=True), rt("The future depends only on the current position, not the history")),
    bullet(rt("Martingale: ", bold=True), eq(r"\mathbb{E}[S_n \mid S_1,\ldots,S_{n-1}] = S_{n-1}"), rt(" — fair game property")),
    heading3("The √n Diffusive Envelope"),
    para(rt("The standard deviation of "), eq(r"S_n"), rt(" is "), eq(r"\sqrt{n}"), rt(", so most paths live within "), eq(r"\pm\sqrt{n}"), rt(" of zero. By the Central Limit Theorem:")),
    equation_block(r"\frac{S_n}{\sqrt{n}} \xrightarrow{d} \mathcal{N}(0,1) \quad \text{as } n \to \infty"),
    para(rt("Expected absolute displacement, derived from the CLT limit:")),
    equation_block(r"\mathbb{E}[|S_n|] \approx \sqrt{\frac{2n}{\pi}} \approx 0.7979\,\sqrt{n}"),
    callout("🔑", rt("Key Invariant: ", bold=True), rt("The diffusive scaling S_n = O(√n) is universal — it holds for any i.i.d. steps with finite variance, regardless of the step distribution. This is the content of the CLT applied to cumulative sums.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ────────────────────────────
    heading2("🏗️ Architecture & Internal Workings (PhD Deep-Dive)"),
    heading3("Step-by-Step Internal Mechanics"),
    para(rt("At each time step n, the random walk performs exactly one operation: sample "), eq(r"X_n \in \{-1, +1\}"), rt(" uniformly, then update the position:")),
    equation_block(r"S_n = S_{n-1} + X_n"),
    para(rt("This simple update rule has profound consequences. The key internal structure:")),
    numbered(rt("State: ", bold=True), rt("The full state is just the current position S_n — a single integer. The walk is memoryless (Markov property).")),
    numbered(rt("Transition: ", bold=True), rt("P(Sₙ = k+1 | Sₙ₋₁ = k) = P(Sₙ = k−1 | Sₙ₋₁ = k) = 1/2 — a symmetric random walk on ℤ.")),
    numbered(rt("Path count: ", bold=True), rt("After n steps, there are 2ⁿ equally likely paths. The number of paths reaching position k (where k and n have the same parity) is C(n, (n+k)/2).")),
    heading3("Numerical Trace (n=6 steps)"),
    para(rt("Suppose the coin flips are: +1, −1, +1, +1, −1, +1. The walk evolves as:")),
    table(4,
        table_row(["Step n", "Flip Xₙ", "Position Sₙ", "Running E[Sₙ²]=n"]),
        table_row(["0", "—", "0", "0"]),
        table_row(["1", "+1", "1", "1"]),
        table_row(["2", "−1", "0", "2"]),
        table_row(["3", "+1", "1", "3"]),
        table_row(["4", "+1", "2", "4"]),
        table_row(["5", "−1", "1", "5"]),
        table_row(["6", "+1", "2", "6"]),
    ),
    para(rt("Final position S₆ = 2. E[S₆] = 0. E[S₆²] = 6. √6 ≈ 2.45 — the position 2 is well within the ±√6 ≈ ±2.45 band.")),
    heading3("Reflection Principle"),
    para(rt("A central combinatorial tool: every path from (0,0) to (n, k) with k > 0 that touches 0 can be reflected at the first zero-crossing to produce a bijection with paths from (0,−2) to (n, k). This gives:")),
    equation_block(r"\Pr(S_n = k,\; S_1 > 0,\ldots,S_{n-1} > 0) = \frac{|k|}{n} \Pr(S_n = k)"),
    heading3("Pólya Recurrence — Internal Mechanism"),
    para(rt("In 1D, returning to 0 requires equal numbers of +1 and −1 steps. After 2n steps, the probability of being at 0 is:")),
    equation_block(r"\Pr(S_{2n} = 0) = \binom{2n}{n} \frac{1}{4^n} \sim \frac{1}{\sqrt{\pi n}} \quad \text{(Stirling)}"),
    para(rt("The expected number of returns to 0 is "), eq(r"\sum_{n=1}^\infty \Pr(S_{2n}=0)"), rt(", which diverges (harmonic-like series in 1D and 2D), proving recurrence. In 3D, the return probability "), eq(r"P_{2n}^{(3)}(0,0) \sim (4\pi n)^{-3/2}"), rt(" — a summable series — proving transience.")),
    heading3("Design Decision: Why ±1?"),
    callout("🔧", rt("Design Choice: ", bold=True), rt("The ±1 step is the simplest non-trivial symmetric choice. Any finite-variance symmetric distribution gives the same √n scaling (CLT universality). Heavy-tailed distributions (Cauchy, etc.) produce Lévy flights with anomalous scaling α ≠ 1/2 — faster or slower diffusion than √n.")),
    divider(),

    # ── Section 5: The Math ────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Deriving the Variance: Var(Sₙ) = n"),
    para(rt("Since the steps "), eq(r"X_k"), rt(" are independent and "), eq(r"\operatorname{Var}(X_k) = \mathbb{E}[X_k^2] - (\mathbb{E}[X_k])^2 = 1 - 0 = 1"), rt(":")),
    equation_block(r"\operatorname{Var}(S_n) = \operatorname{Var}\!\left(\sum_{k=1}^n X_k\right) = \sum_{k=1}^n \operatorname{Var}(X_k) = n"),
    heading3("Deriving E[|Sₙ|] ≈ √(2n/π)"),
    para(rt("By CLT, "), eq(r"S_n / \sqrt{n} \xrightarrow{d} Z \sim \mathcal{N}(0,1)"), rt(". For "), eq(r"Z \sim \mathcal{N}(0,1)"), rt(":")),
    equation_block(r"\mathbb{E}[|Z|] = \int_{-\infty}^{\infty} |z| \frac{e^{-z^2/2}}{\sqrt{2\pi}}\, dz = 2 \int_0^\infty z \frac{e^{-z^2/2}}{\sqrt{2\pi}}\, dz = \sqrt{\frac{2}{\pi}}"),
    para(rt("Because "), eq(r"|S_n| = \sqrt{n} \cdot |S_n/\sqrt{n}|"), rt(" and continuous mapping theorem:")),
    equation_block(r"\mathbb{E}[|S_n|] \approx \sqrt{n} \cdot \mathbb{E}[|Z|] = \sqrt{n} \cdot \sqrt{\frac{2}{\pi}} = \sqrt{\frac{2n}{\pi}}"),
    heading3("Law of the Iterated Logarithm (LIL)"),
    para(rt("A sharp characterization of the extreme paths:")),
    equation_block(r"\limsup_{n \to \infty} \frac{S_n}{\sqrt{2n \log \log n}} = 1 \quad \text{almost surely}"),
    para(rt("This tells us paths exceed "), eq(r"\sqrt{2n \log \log n}"), rt(" infinitely often but do not exceed "), eq(r"(1+\varepsilon)\sqrt{2n \log \log n}"), rt(" for any "), eq(r"\varepsilon > 0"), rt(".")),
    heading3("Ballot Problem"),
    para(rt("In an election with n total votes, candidate A receiving k votes (k > n/2): the probability that A is strictly ahead throughout the counting is:")),
    equation_block(r"\Pr(\text{A leads throughout}) = \frac{2k - n}{n} = \frac{k - (n-k)}{n}"),
    heading3("Continuous Limit: Brownian Motion"),
    para(rt("Take step size "), eq(r"\delta x = \sigma\sqrt{\delta t}"), rt(" and step time "), eq(r"\delta t = T/n"), rt(". As "), eq(r"n \to \infty"), rt(", the rescaled walk "), eq(r"B_t^{(n)} = \delta x \cdot S_{\lfloor t/\delta t \rfloor}"), rt(" converges to Brownian motion satisfying:")),
    equation_block(r"\frac{\partial p}{\partial t} = \frac{\sigma^2}{2} \frac{\partial^2 p}{\partial x^2}, \quad p(x,t) = \frac{1}{\sqrt{2\pi\sigma^2 t}} \exp\!\left(-\frac{x^2}{2\sigma^2 t}\right)"),
    callout("⚠️", rt("Common Pitfall: ", bold=True), rt("E[Sₙ] = 0 does NOT mean the walk stays near 0. Individual paths drift far — E[|Sₙ|] ≈ 0.798√n ≠ 0. The zero mean refers to the average over all possible paths, not the behavior of any particular path. Also: the walk returns to 0 in finite expected time in 1D (E[T₀] = ∞, but P(return) = 1).")),
    divider(),

    # ── Section 6: Code Implementation ────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("From Scratch — NumPy"),
    code_block("python", '''import numpy as np
import matplotlib.pyplot as plt

# ── Simple Symmetric Random Walk ──────────────────────────────────────────
np.random.seed(42)
N = 1000          # number of steps
n_paths = 5       # number of independent walkers

# Each row is one walk; cumsum gives running total
steps = np.random.choice([-1, 1], size=(n_paths, N))  # shape (5, 1000)
S = np.hstack([np.zeros((n_paths, 1)), np.cumsum(steps, axis=1)])  # shape (5, 1001)

# ── Key Statistics ─────────────────────────────────────────────────────────
n_vals = np.arange(N+1)
print(f"Var(S_N) = {np.var(S[:, -1]):.2f}  (expected: {N})")
print(f"E[|S_N|] = {np.mean(np.abs(S[:, -1])):.3f}  "
      f"(theory √(2N/π) = {np.sqrt(2*N/np.pi):.3f})")

# ── Monte Carlo Verification ───────────────────────────────────────────────
trials = 50000
final_positions = np.sum(np.random.choice([-1,1], size=(trials, N)), axis=1)
print(f"E[|S_N|] MC = {np.mean(np.abs(final_positions)):.3f}")

# ── The √n Envelope ─────────────────────────────────────────────────────────
envelope = np.sqrt(n_vals)                          # ±√n band
# What fraction of paths stay inside ±√n at each step?
inside = np.mean(np.abs(S) <= envelope[None, :], axis=0)
print(f"Fraction inside ±√n at n=N: {inside[-1]:.3f}")  # ~0.683 (1-sigma)

# ── Diffusion Limit: rescale to Brownian motion ────────────────────────────
t = np.linspace(0, 1, N+1)
B = S / np.sqrt(N)              # rescaled walk → B_t as N→∞

# ── Polya Recurrence: count zero returns in 1D ──────────────────────────────
def count_returns(path):
    """Count how many times a path returns to 0 after t=0."""
    return np.sum(path[1:] == 0)

returns_1d = [count_returns(S[i]) for i in range(n_paths)]
print(f"Zero returns per path (1D): {returns_1d}")
# In theory: number of returns ~ ∞ as N→∞ (recurrent)

# ── General Random Walk with drift ──────────────────────────────────────────
def random_walk(n, mu=0.0, sigma=1.0, n_paths=1, seed=None):
    """General random walk with Gaussian steps."""
    rng = np.random.default_rng(seed)
    steps = rng.normal(mu, sigma, size=(n_paths, n))
    return np.hstack([np.zeros((n_paths, 1)), np.cumsum(steps, axis=1)])

# With drift mu=0.1: walk grows as mu*n + sigma*√n
biased = random_walk(200, mu=0.1, sigma=1.0, n_paths=3, seed=0)
print(f"Biased walk final pos: {biased[:, -1]}  (expected: {0.1*200})")'''),

    heading3("Production Usage — scipy + statsmodels"),
    code_block("python", '''import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import adfuller  # ADF test for unit root

# ── Test if a time series is a random walk (unit root test) ────────────────
# Random walk is the null hypothesis of the ADF test
np.random.seed(0)
rw = np.cumsum(np.random.randn(500))          # synthetic random walk

result = adfuller(rw, autolag="AIC")
print(f"ADF statistic: {result[0]:.4f}")
print(f"p-value: {result[1]:.4f}")           # > 0.05 → fail to reject RW null
print(f"Conclusion: {'RW (unit root)' if result[1] > 0.05 else 'Stationary'}")

# ── Simulate Geometric Brownian Motion (stock price model) ──────────────────
def gbm(S0, mu, sigma, T, n, seed=None):
    """Geometric Brownian Motion: dS = mu*S*dt + sigma*S*dW"""
    rng = np.random.default_rng(seed)
    dt = T / n
    # Exact solution: S(t) = S0 * exp((mu - sigma²/2)*t + sigma*W_t)
    t = np.linspace(0, T, n+1)
    W = np.concatenate([[0], np.cumsum(rng.normal(0, np.sqrt(dt), n))])
    return S0 * np.exp((mu - 0.5*sigma**2)*t + sigma*W)

prices = gbm(S0=100, mu=0.05, sigma=0.2, T=1, n=252, seed=42)
print(f"GBM price after 1 year: {prices[-1]:.2f}  (expected: {100*np.exp(0.05):.2f})")

# ── MCMC Random Walk Sampler ─────────────────────────────────────────────────
def metropolis_random_walk(log_target, x0, step_size, n_iter):
    """Metropolis-Hastings with random walk proposal."""
    x = x0
    samples = [x]
    for _ in range(n_iter):
        proposal = x + np.random.normal(0, step_size)
        log_ratio = log_target(proposal) - log_target(x)
        if np.log(np.random.uniform()) < log_ratio:
            x = proposal                      # accept
        samples.append(x)
    return np.array(samples)

# Sample from N(3, 1)
log_N = lambda x: -0.5 * (x - 3)**2
samples = metropolis_random_walk(log_N, x0=0, step_size=0.5, n_iter=5000)
print(f"MCMC posterior mean: {np.mean(samples[500:]):.3f}  (true: 3.0)")
# ⚠️ step_size controls acceptance rate: too small → slow mixing (like small η in SGD)
#    too large → high rejection rate'''),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎯 Interview Deep-Dive"),
    heading3("Q1 (Easy): What is a random walk and what is E[Sₙ]?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("A random walk is a sequence S₀=0, Sₙ = X₁ + … + Xₙ where steps Xₖ are i.i.d. For the symmetric ±1 walk, E[Xₖ]=0 so by linearity E[Sₙ] = 0 for all n. The key follow-up is to distinguish E[Sₙ]=0 from E[|Sₙ|]=0 — the walk still spreads.")),
    ]),
    heading3("Q2 (Easy): What is Var(Sₙ)?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Var(Sₙ) = n for the simple ±1 walk. Since steps are independent, variances add: Var(Σ Xₖ) = Σ Var(Xₖ) = n·1 = n. So std(Sₙ) = √n.")),
    ]),
    heading3("Q3 (Medium): Why does E[|Sₙ|] grow as √n and not as n?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("By CLT, Sₙ/√n → N(0,1). So |Sₙ| ≈ √n·|Z| where Z~N(0,1). The key factor is that N(0,1) has a finite first absolute moment E[|Z|] = √(2/π) ≈ 0.798. Therefore E[|Sₙ|] ≈ 0.798√n. The growth is √n, not n, because the walk is unbiased — equal chances of going positive or negative cancel out the linear growth, leaving only the √n scaling from variance.")),
    ]),
    heading3("Q4 (Medium): State and explain Pólya's recurrence theorem"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Simple random walk is recurrent (returns to origin with probability 1) in 1D and 2D, and transient (escapes to infinity) in 3D and higher. The proof uses the Borel-Cantelli lemma: if the sum of return probabilities P(S₂ₙ=0) diverges, then the walk returns infinitely often (recurrence). P(S₂ₙ=0) ~ 1/√(πn) in 1D → harmonic series (diverges) → recurrent. In 3D, P(S₂ₙ=0) ~ (4πn)^{-3/2} → summable → transient.")),
        callout("⚠️", rt("Follow-up trap: ", bold=True), rt("'If recurrent in 2D, what's the expected return time?' Answer: The walk returns to 0 with probability 1, but the expected return time is infinite! This distinction (recurrent but null-recurrent) trips up many interviewees.")),
    ]),
    heading3("Q5 (Medium): How does a random walk relate to the CLT?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("The CLT IS the statement that Sₙ/√n → N(0,1). The random walk is literally the CLT's object of study — Sₙ is the sum of n i.i.d. variables, and the CLT describes the distribution of this sum after rescaling. The CLT → diffusive scaling (√n); the functional CLT (Donsker's theorem) shows the entire rescaled path Sₙ·t/√n converges to Brownian motion in C[0,1].")),
    ]),
    heading3("Q6 (Hard): Explain the connection between random walks and SGD noise"),
    toggle([rt("Answer", bold=True)], [
        para(rt("In SGD, the parameter update is θₜ = θₜ₋₁ − η∇̃f(θₜ₋₁), where ∇̃f = ∇f + ξₜ with ξₜ being mini-batch noise. Near a critical point where ∇f(θ*) ≈ 0, the trajectory in parameter space is approximately a random walk with step variance η²σ²/B (η=LR, σ²=gradient variance, B=batch size). The walk explores a region of size ~η·σ/√B around θ*. This random walk behavior in weight space: (1) provides implicit regularization by preferring wider minima, (2) helps escape sharp local minima, (3) explains why small batch size and large LR can generalize better (larger random-walk exploration).")),
        callout("⚠️", rt("Follow-up: ", bold=True), rt("'Is SGD truly a random walk?' Not exactly — the loss landscape is curved, so steps are not i.i.d. near a minimum (the Hessian creates a restoring force, making it an Ornstein-Uhlenbeck process rather than a free random walk). The random walk approximation holds only locally and transiently.")),
    ]),
    heading3("Q7 (Hard): Explain the Ballot Problem"),
    toggle([rt("Answer", bold=True)], [
        para(rt("In an election, candidate A gets a votes, candidate B gets b votes (a > b), for a+b = n total. What is the probability that A leads strictly throughout the counting? Answer: (a−b)/n = (2a−n)/n. Proof uses the reflection principle: paths where B ever leads can be bijected (via reflection at the first tie) with paths starting at 2, giving equal count. This is equivalent to asking: of all random walk paths from 0 to a−b > 0, what fraction stay strictly positive? The answer is (a−b)/n by the cycle lemma.")),
    ]),
    heading3("Explain to Two Levels"),
    callout("🎓", rt("PhD Researcher: ", bold=True), rt("A random walk on ℤ is a Markov chain with transition kernel P(x, x±1) = 1/2. Its generator acts as the discrete Laplacian, connecting to harmonic analysis. The CLT scaling Sₙ/√n → N(0,1) is a special case of Donsker's invariance principle in the Skorokhod space D[0,1]. Pólya's theorem follows from the comparison of the Green's function G(0,0) = Σₙ P(S₂ₙ=0): Green's function finite ↔ transient. The random walk is the discrete skeleton of Brownian motion, which is the unique continuous local martingale with quadratic variation ⟨B⟩ₜ = t.")),
    callout("🔬", rt("Research Scientist/Engineer: ", bold=True), rt("A random walk is a cumulative sum of i.i.d. zero-mean steps. Variance grows linearly, so std dev grows as √n. CLT gives the Gaussian distribution of the final position when rescaled. Key applications: (1) MCMC — Metropolis-Hastings uses a random walk proposal distribution; (2) SGD noise acts like a random walk in parameter space near minima; (3) financial models (GBM); (4) ADF/unit-root tests for time series stationarity. The 1D/2D recurrence vs 3D+ transience is a beautiful theoretical fact but rarely comes up in practice.")),
    heading3("System Design Angle"),
    para(rt("Random walks appear in: (1) A/B testing — test duration should scale as √n by CLT confidence intervals; (2) Recommendation systems — random walks on item graphs for PageRank-like scoring; (3) LLM training — SGD trajectory in billion-parameter space follows a random walk locally; (4) Anomaly detection — detecting when a process leaves its random-walk regime (CUSUM, SPRT).")),
    heading3("Red Flags (Wrong Answers)"),
    bullet(rt("Saying E[Sₙ] = 0 implies the walk stays near 0 — wrong, E[|Sₙ|] grows as √n")),
    bullet(rt("Confusing recurrence (return prob = 1) with null recurrence (E[return time] = ∞)")),
    bullet(rt("Claiming SGD is exactly a random walk — it's only approximately a RW near flat regions")),
    bullet(rt("Saying the walk 'always returns to 0' without specifying dimension")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    heading3("Random Walk Variants"),
    table(5,
        table_row(["Variant", "Step distribution", "Scaling", "Limit process", "Use case"]),
        table_row(["Simple RW (1D)", "±1 uniform", "√n", "Brownian motion", "Theory, pedagogy"]),
        table_row(["Gaussian RW", "N(0, σ²)", "σ√n", "Brownian motion (same!)", "SGD, finance"]),
        table_row(["Biased/Drifted RW", "±1 with p≠1/2", "μn + σ√n", "BM with drift", "Stock prices"]),
        table_row(["Lévy Flight", "Heavy-tailed, α<2", "n^{1/α}", "α-stable Lévy process", "Anomalous diffusion"]),
        table_row(["2D RW", "±1 in each dim", "√n per dim", "2D Brownian motion", "Recurrence demos"]),
        table_row(["SARW (self-avoiding)", "Excludes revisits", "n^ν (ν≈0.59 in 3D)", "No simple limit", "Polymer modeling"]),
        table_row(["Geometric BM", "Log-normal steps", "Exponential", "GBM", "Financial prices"]),
    ),
    heading3("When to Use"),
    bullet(rt("Simple RW: ", bold=True), rt("Understanding diffusion, CLT intuition, pedagogical purposes")),
    bullet(rt("Gaussian RW: ", bold=True), rt("SGD analysis, MCMC proposals, financial simulation")),
    bullet(rt("Biased RW: ", bold=True), rt("Modeling processes with drift (stock trends, biased coin)")),
    bullet(rt("Lévy Flight: ", bold=True), rt("Heavy-tailed phenomena (earthquake sizes, internet traffic)")),
    heading3("When NOT to Use"),
    bullet(rt("If observations are correlated (AR/MA structure) — use specialized time series models")),
    bullet(rt("If the distribution has infinite variance (α-stable) — CLT doesn't apply; use Lévy processes")),
    bullet(rt("For continuous-time processes — transition directly to Brownian motion / SDEs")),
    callout("🎯", rt("Decision: ", bold=True), rt("Use simple ±1 RW for theory and intuition. Use Gaussian RW for simulation. Use GBM for finance. Use Lévy flights for heavy tails. Add drift μ≠0 whenever the process has a systematic trend.")),
    divider(),

    # ── Section 9: Interactive Explainer Embed ─────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through random walk properties — paths, √n envelope, CLT scaling, Pólya recurrence, and SGD connections. Use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Probability basics: expectation, variance, independence")),
    bullet(rt("The Central Limit Theorem (3.8 in this vault)")),
    bullet(rt("Markov Chains (3.10 in this vault)")),
    bullet(rt("Law of Large Numbers (3.7 in this vault)")),
    heading3("What to Learn Next"),
    bullet(rt("Brownian Motion / Wiener Process — continuous-time limit of random walk")),
    bullet(rt("Martingales — the random walk is the canonical martingale")),
    bullet(rt("Itô Calculus — stochastic differential equations driven by Brownian motion")),
    bullet(rt("Markov Chain Monte Carlo (MCMC) — random walks for Bayesian inference")),
    bullet(rt("Stochastic Gradient Descent — random walk interpretation of optimization")),
    heading3("Key Papers"),
    bullet(rt("Bachelier (1900) — ", bold=True), rt("Théorie de la spéculation. First mathematical treatment of Brownian motion applied to markets.")),
    bullet(rt("Einstein (1905) — ", bold=True), rt("Über die von der molekularkinetischen Theorie der Wärme geforderte Bewegung. Random walk derivation of diffusion.")),
    bullet(rt("Pólya (1921) — ", bold=True), rt("Über eine Aufgabe der Wahrscheinlichkeitsrechnung betreffend die Irrfahrt im Strassennetz. The recurrence theorem.")),
    bullet(rt("Wiener (1923) — ", bold=True), rt("Differential-space. Rigorous construction of Brownian motion as limit of random walks.")),
    bullet(rt("Donsker (1951) — ", bold=True), rt("Invariance principle: rescaled random walk path → Brownian motion in C[0,1].")),
    heading3("Best Resources"),
    bullet(rt("Book: Durrett, Probability: Theory and Examples — Chapter 4 (Random Walks), rigorous")),
    bullet(rt("Book: Lawler & Limic, Random Walk: A Modern Introduction — comprehensive")),
    bullet(rt("Lecture: MIT OCW 18.650 Statistics for Applications — Sections 6–7")),
    bullet(rt("Blog: Terence Tao, 'The random walk' — beautiful geometric intuitions")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Markov Chains (3.10), Brownian Motion, Martingales, CLT (3.8), Itô Calculus, SGD & Optimization, MCMC, PageRank, Lévy Processes, Diffusion Models.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
