#!/usr/bin/env python3
"""Update Notion page for: Rate-distortion theory (overview)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81b0-8517-e0453e157a3f"
ICON = "🟠"  # Advanced
SLUG = "rate_distortion_theory"
EXPLAINER_URL = f"https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/{SLUG}_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Every time you compress an image, stream a video, or save an MP3, a trade-off is being made: smaller file size (fewer bits) means lower quality (more distortion). Rate-distortion theory, developed by Claude Shannon in 1959, answers the most fundamental question about this trade-off: "), rt("what is the minimum number of bits per sample you must spend to keep distortion below a specified threshold?", italic=True), rt(" This hard limit — the R-D curve — is a wall no codec can break through.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine summarising a novel. A one-word summary (\"adventure\") uses very few bits but loses almost everything — high distortion. A full copy is zero distortion but costs all the bits. Every intermediate-length summary corresponds to a point on the rate-distortion curve. Shannon proved no summariser, however brilliant, can operate below this curve.")),
    heading3("One-sentence summary"),
    para(rt("Rate-distortion theory gives the information-theoretic minimum bit rate needed to represent a source within an allowed reconstruction error, expressed as a convex, decreasing function R(D) of distortion D.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("The rate-distortion function "), eq(r"R(D) = \min_{p(\hat{x}|x):\,\mathbb{E}[d(X,\hat{X})]\leq D} I(X;\hat{X})"), rt(" is the theoretical compression floor. For a Gaussian source with MSE distortion: "), eq(r"R(D) = \tfrac{1}{2}\log_2(\sigma^2/D)")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Shannon's 1948 source coding theorem established the entropy "), eq(r"H(X)"), rt(" as the minimum lossless compression limit. But for continuous-valued sources like audio and images, lossless compression requires infinite bits (entropy of a continuous distribution is infinite in bits). Engineers knew that allowing small errors dramatically reduced the required storage — but had no principled way to quantify the trade-off. What IS the minimum rate for a given quality?")),
    heading3("The Breakthrough"),
    para(rt("Shannon (1959) in \"Coding Theorems for a Discrete Source with a Fidelity Criterion\" introduced the rate-distortion function "), eq(r"R(D)"), rt(" and proved that it is the tight lower bound: any code achieving average distortion "), eq(r"D"), rt(" must use at least "), eq(r"R(D)"), rt(" bits per source symbol, AND there exist codes achieving this bound (asymptotically in block length).")),
    heading3("Evolution Timeline"),
    bullet(rt("1948 — Shannon's source coding theorem (lossless)")),
    bullet(rt("1959 — Shannon introduces R-D theory (lossy); Kolmogorov independently formulates ε-entropy")),
    bullet(rt("1970s — Berger's book \"Rate Distortion Theory\" systematises the field")),
    bullet(rt("1990s–2000s — Practical wavelet codecs (JPEG2000), scalar quantization approaches R-D limits")),
    bullet(rt("2017 — β-VAE recast as R-D Lagrangian relaxation; Ballé et al. propose neural image codecs approaching R-D bounds")),
    bullet(rt("2020s — Diffusion models + learned perceptual distortion metrics open new R-D frontiers")),
    heading3("Before vs After"),
    table(3,
        table_row(["Dimension", "Before (1948 Source Coding)", "After (1959 Rate-Distortion)"]),
        table_row(["Objective", "Lossless recovery", "Bounded distortion recovery"]),
        table_row(["Applicable to", "Discrete sources with finite entropy", "Continuous sources, all distortion metrics"]),
        table_row(["Compression limit", "Entropy H(X) bits", "R(D) bits — a function of allowed error"]),
        table_row(["Practical relevance", "Text compression (Huffman, Arithmetic)", "Image (JPEG), audio (MP3), video (H.264)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ─────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Let "), eq(r"X"), rt(" be a random variable (the "), rt("source", italic=True), rt(") with distribution "), eq(r"p(x)"), rt(". A "), rt("lossy compressor", italic=True), rt(" maps "), eq(r"X"), rt(" to a "), rt("reconstruction", italic=True), rt(" "), eq(r"\hat{X}"), rt(" via a conditional distribution "), eq(r"p(\hat{x}|x)"), rt(". The "), rt("distortion measure", italic=True), rt(" "), eq(r"d(x, \hat{x}) \geq 0"), rt(" quantifies the error (MSE: "), eq(r"d = (x-\hat{x})^2"), rt("; Hamming: "), eq(r"d = \mathbf{1}[x \neq \hat{x}]"), rt(").")),
    heading3("The Rate-Distortion Function"),
    para(rt("The rate-distortion function is defined as:")),
    equation_block(r"R(D) = \min_{\substack{p(\hat{x}|x):\\ \mathbb{E}[d(X,\hat{X})] \leq D}} I(X;\hat{X})"),
    para(rt("where "), eq(r"I(X;\hat{X}) = \mathbb{E}\!\left[\log \frac{p(X,\hat{X})}{p(X)p(\hat{X})}\right]"), rt(" is the mutual information. The minimisation is over all conditional distributions (channels) that keep expected distortion below "), eq(r"D"), rt(".")),
    heading3("Key Properties"),
    bullet(rt("Non-increasing: "), rt("More distortion tolerance → never needs more bits", italic=True)),
    bullet(rt("Convex: "), rt("The R-D curve bends upward; halving distortion always costs increasingly more bits (diminishing returns on quality improvement)", italic=True)),
    bullet(rt("R(0) = H(X) "), rt("for discrete sources (lossless limit); "), eq(r"R(0) = \infty"), rt(" for continuous sources")),
    bullet(eq(r"R(D) = 0"), rt(" for "), eq(r"D \geq D_{\max} = \min_{\hat{x}} \mathbb{E}[d(X,\hat{x})]"), rt(" (trivial reconstruction)")),
    callout("🔑", rt("Core invariant: ", bold=True), rt("No compressor — classical or neural — can achieve average distortion "), eq(r"D"), rt(" at fewer than "), eq(r"R(D)"), rt(" bits per sample. This is a consequence of the data processing inequality and Fano's inequality.")),
    divider(),

    # ── Section 4: PhD-Level Deep Dive ────────────────────────────────────────
    heading2("🔬 Architecture & Internal Workings — PhD-Level Deep Dive"),
    heading3("Solving the Gaussian Case: Full Derivation"),
    para(rt("Source: "), eq(r"X \sim \mathcal{N}(0, \sigma^2)"), rt(". Distortion: MSE, "), eq(r"d(x,\hat{x}) = (x-\hat{x})^2"), rt(". We want to find "), eq(r"R(D) = \min_{p(\hat{x}|x)} I(X;\hat{X})"), rt(" s.t. "), eq(r"\mathbb{E}[(X-\hat{X})^2] \leq D"), rt(".")),
    heading3("Step 1: Lagrangian Relaxation"),
    para(rt("Convert the constrained problem to an unconstrained one via a Lagrange multiplier "), eq(r"s \geq 0"), rt(":")),
    equation_block(r"\min_{p(\hat{x}|x)} \left[ I(X;\hat{X}) + s \cdot \mathbb{E}[(X-\hat{X})^2] \right]"),
    para(rt("For each "), eq(r"s"), rt(", the optimal solution gives a point "), eq(r"(D^*(s), R^*(s))"), rt(" on the R-D curve. Sweeping "), eq(r"s \in [0, \infty)"), rt(" traces the entire curve.")),
    heading3("Step 2: Optimal Conditional Distribution"),
    para(rt("The first-order condition for the Lagrangian gives the "), rt("Blahut-Arimoto", italic=True), rt(" optimality condition: the optimal channel satisfies")),
    equation_block(r"p^*(\hat{x}|x) = \frac{p^*(\hat{x}) \exp(-s \cdot (x-\hat{x})^2)}{\int p^*(\hat{x}') \exp(-s \cdot (x-\hat{x}')^2) \, d\hat{x}'}"),
    para(rt("For the Gaussian source, one can verify that the optimal "), eq(r"p^*(\hat{x}|x)"), rt(" is Gaussian. Specifically, the optimal reconstruction channel is "), eq(r"\hat{X} = \alpha X + N"), rt(" where "), eq(r"N \sim \mathcal{N}(0, D)"), rt(" is independent noise and "), eq(r"\alpha = (\sigma^2 - D)/\sigma^2"), rt(".")),
    heading3("Step 3: Computing the Mutual Information"),
    para(rt("With optimal "), eq(r"p^*(\hat{x}|x)"), rt(", compute "), eq(r"I(X;\hat{X}) = h(\hat{X}) - h(\hat{X}|X)"), rt(":")),
    equation_block(r"h(X|\hat{X}) = \frac{1}{2}\log(2\pi e D) \quad (\text{Gaussian noise of variance } D)"),
    equation_block(r"h(X) = \frac{1}{2}\log(2\pi e \sigma^2) \quad (\text{Gaussian source})"),
    equation_block(r"I(X;\hat{X}) = h(X) - h(X|\hat{X}) = \frac{1}{2}\log_2\!\left(\frac{\sigma^2}{D}\right)"),
    para(rt("This uses the entropy power inequality: the Gaussian minimises "), eq(r"h(\hat{X}|X)"), rt(" for fixed "), eq(r"\mathbb{E}[(X-\hat{X})^2] = D"), rt(", ensuring the Gaussian channel is optimal.")),
    heading3("Step 4: The Result"),
    equation_block(r"R(D) = \max\!\left(0,\; \frac{1}{2}\log_2\!\left(\frac{\sigma^2}{D}\right)\right), \quad 0 \leq D \leq \sigma^2"),
    heading3("Numerical Trace (σ²=1)"),
    para(rt("Walking through key operating points:")),
    table(4,
        table_row(["Distortion D", "Lagrange s", "R(D) [bits]", "Practical meaning"]),
        table_row(["0.01", "50.0", "3.32", "Near-lossless (quantization noise 1%)"]),
        table_row(["0.10", "5.0", "1.66", "~2-bit quantization per sample"]),
        table_row(["0.25 = σ²/4", "2.0", "1.00", "Exactly 1 bit/sample"]),
        table_row(["0.50 = σ²/2", "1.0", "0.50", "Half a bit per sample"]),
        table_row(["1.00 = σ²", "0.0", "0.00", "Predict mean, no transmission"]),
    ),
    heading3("Vector Quantisation and Water-Filling"),
    para(rt("For a vector source "), eq(r"\mathbf{X} = (X_1, \ldots, X_n)"), rt(" with independent components of variances "), eq(r"\sigma_i^2"), rt(", the optimal allocation of distortion to each component follows the "), rt("reverse water-filling", italic=True), rt(" rule: given a total distortion budget "), eq(r"D"), rt(", set "), eq(r"D_i = \min(\theta, \sigma_i^2)"), rt(" where "), eq(r"\theta"), rt(" is the water level (Lagrange multiplier) chosen so "), eq(r"\sum_i D_i = D"), rt(". Components with "), eq(r"\sigma_i^2 < \theta"), rt(" are dropped entirely (allocated zero rate). The total rate is:")),
    equation_block(r"R(D) = \sum_{i:\sigma_i^2 > \theta} \frac{1}{2}\log_2\!\left(\frac{\sigma_i^2}{\theta}\right)"),
    callout("⚠️", rt("Design Decision: ", bold=True), rt("Why MSE and not perceptual quality? Shannon's theorem holds for ANY bounded distortion measure, including perceptual metrics (SSIM, LPIPS). The resulting R-D function changes, but the theorem — that R(D) is a hard lower bound — holds universally. Modern neural codecs optimise a perceptual R-D curve explicitly.")),
    divider(),

    # ── Section 5: The Math Behind It ─────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("The Shannon Lower Bound (Proof Sketch)"),
    para(rt("We prove "), eq(r"R \geq R(D)"), rt(" for any code achieving distortion "), eq(r"D"), rt(". Consider a code that maps "), eq(r"n"), rt(" source symbols to a binary codeword of length "), eq(r"nR"), rt(" bits. By Fano's inequality and the data processing inequality:")),
    equation_block(r"nR \geq H(\text{index}) \geq I(X^n; \hat{X}^n) \geq \sum_{i=1}^n I(X_i; \hat{X}_i) \geq n \cdot R(D)"),
    para(rt("where the last step uses Jensen's inequality and convexity of "), eq(r"R(D)"), rt(". Dividing by "), eq(r"n"), rt(" gives "), eq(r"R \geq R(D)"), rt(".")),
    heading3("Achievability (Shannon's Forward Theorem)"),
    para(rt("For any "), eq(r"R > R(D)"), rt(" and "), eq(r"\varepsilon > 0"), rt(", there exists a block code of length "), eq(r"n"), rt(" (for large enough "), eq(r"n"), rt(") that achieves distortion at most "), eq(r"D + \varepsilon"), rt(" with probability "), eq(r"1 - \varepsilon"), rt(". The proof uses random codebook generation and joint typicality: draw "), eq(r"2^{nR}"), rt(" reconstruction sequences i.i.d. from the optimal marginal "), eq(r"p^*(\hat{x})"), rt(", then find the jointly typical pair.")),
    heading3("The Blahut-Arimoto Algorithm"),
    para(rt("Since the R-D optimisation is a convex program, it can be solved iteratively. The Blahut-Arimoto algorithm alternates between:")),
    numbered(eq(r"p^{(t+1)}(\hat{x}|x) = \frac{p^{(t)}(\hat{x})\exp(-s\,d(x,\hat{x}))}{\sum_{\hat{x}'} p^{(t)}(\hat{x}')\exp(-s\,d(x,\hat{x}'))}"), rt(" (update channel)")),
    numbered(eq(r"p^{(t+1)}(\hat{x}) = \sum_x p(x)\, p^{(t+1)}(\hat{x}|x)"), rt(" (update marginal)")),
    para(rt("This converges to the global optimum since the objective is jointly convex in "), eq(r"(p(\hat{x}|x), p(\hat{x}))"), rt(".")),
    heading3("Connection to Channel Capacity"),
    para(rt("Rate-distortion is the dual of channel capacity. Channel capacity asks: given a fixed channel, what is the maximum information rate? R-D theory asks: given a fixed source and distortion budget, what is the minimum channel capacity needed? Formally, "), eq(r"C = \max_{p(x)} I(X;Y)"), rt(" vs "), eq(r"R(D) = \min_{p(\hat{x}|x)} I(X;\hat{X})"), rt(". Shannon proved both in 1948–1959, establishing the complete information-theoretic picture of communication.")),
    callout("⚠️", rt("Mathematical subtlety: ", bold=True), rt("The Gaussian case is special — the optimal channel is Gaussian (additive noise). For non-Gaussian sources, the optimal "), eq(r"p^*(\hat{x}|x)"), rt(" is not closed-form; you must run Blahut-Arimoto numerically. Also, the formula "), eq(r"R(D) = \tfrac{1}{2}\log_2(\sigma^2/D)"), rt(" is in bits (using "), eq(r"\log_2"), rt("). The natural-log version gives nats: "), eq(r"R(D) = \tfrac{1}{2}\ln(\sigma^2/D)")),
    divider(),

    # ── Section 6: Code Implementation ────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch: Gaussian R-D Curve"),
    code_block("python",
"""import numpy as np
import matplotlib.pyplot as plt

def rd_gaussian(sigma2: float, D_vals: np.ndarray) -> np.ndarray:
    \"\"\"Rate-distortion function for Gaussian source with MSE distortion.

    R(D) = max(0, 0.5 * log2(sigma^2 / D))  for D in [0, sigma^2]

    Args:
        sigma2: source variance
        D_vals: array of distortion values
    Returns:
        R(D) in bits/sample
    \"\"\"
    # Clip to avoid log(0); at D=0 the limit is infinity
    return np.maximum(0.0, 0.5 * np.log2(sigma2 / np.clip(D_vals, 1e-10, None)))


# Example: unit Gaussian source
sigma2 = 1.0
D = np.linspace(0.005, sigma2, 500)
R = rd_gaussian(sigma2, D)

# Verify key points
for d in [0.01, 0.10, 0.25, 0.50, 1.00]:
    r = rd_gaussian(sigma2, np.array([d]))[0]
    print(f"D={d:.2f}  R(D)={r:.4f} bits")
# D=0.01  R(D)=3.3219
# D=0.25  R(D)=1.0000  <- exactly 1 bit at D=sigma^2/4
# D=1.00  R(D)=0.0000  <- zero rate at max distortion

# Plot R-D curve
plt.figure(figsize=(7, 4))
plt.plot(D, R, 'purple', lw=2.5, label=r'$R(D) = \\frac{1}{2}\\log_2(\\sigma^2/D)$')
plt.fill_between(D, R, R.max(), alpha=0.1, color='green', label='Achievable region')
plt.xlabel('Distortion D'); plt.ylabel('Rate R(D) [bits/sample]')
plt.title('Rate-Distortion Curve: Gaussian Source (σ²=1)')
plt.legend(); plt.tight_layout(); plt.show()
"""),
    heading3("6b — Blahut-Arimoto Algorithm (Discrete Sources)"),
    code_block("python",
"""import numpy as np

def blahut_arimoto(px: np.ndarray, d_matrix: np.ndarray, s: float,
                    n_iter: int = 200, tol: float = 1e-8):
    \"\"\"Blahut-Arimoto algorithm for computing R(D).

    Args:
        px: source distribution, shape (n_x,)
        d_matrix: distortion matrix d[i,j] = d(x_i, x_hat_j), shape (n_x, n_x_hat)
        s: Lagrange multiplier (s >= 0); larger s = lower distortion
        n_iter: max iterations
        tol: convergence tolerance
    Returns:
        (R, D): rate in bits, expected distortion at optimal point
    \"\"\"
    n_x, n_xhat = d_matrix.shape

    # 1. Initialise reconstruction marginal uniformly
    q_xhat = np.ones(n_xhat) / n_xhat

    for _ in range(n_iter):
        q_xhat_prev = q_xhat.copy()

        # 2. Update conditional channel p(x_hat | x)
        # p(x_hat|x) ∝ q(x_hat) * exp(-s * d(x, x_hat))
        log_channel = np.log(q_xhat + 1e-300) - s * d_matrix  # (n_x, n_xhat)
        log_channel -= log_channel.max(axis=1, keepdims=True)   # numerical stability
        channel = np.exp(log_channel)
        channel /= channel.sum(axis=1, keepdims=True)           # normalise rows

        # 3. Update reconstruction marginal q(x_hat) = sum_x p(x) * p(x_hat|x)
        q_xhat = px @ channel  # (n_xhat,)

        if np.max(np.abs(q_xhat - q_xhat_prev)) < tol:
            break

    # 4. Compute I(X; X_hat) and E[d]
    # I = sum_{x, x_hat} p(x)*p(x_hat|x) * log(p(x_hat|x) / q(x_hat))
    joint = px[:, None] * channel  # (n_x, n_xhat)
    mask = joint > 0
    I = np.sum(joint[mask] * np.log2(channel[mask] / q_xhat[None, :][mask]))
    D_exp = np.sum(joint * d_matrix)

    return I, D_exp


# Example: Binary source with Hamming distortion
px = np.array([0.5, 0.5])          # fair coin
d = np.array([[0, 1], [1, 0]])     # Hamming distortion

# Trace R-D curve by sweeping s
s_vals = np.logspace(-2, 3, 100)
rd_curve = [blahut_arimoto(px, d, s) for s in s_vals]
R_vals, D_vals = zip(*rd_curve)

# At D=0.1: binary source R(D) = H(0.1) - H(D) = 0.531 bits
# (known closed-form: R(D) = 1 - H_b(D) for binary source)
print(f"R(D=0.1) ≈ {1 - (-0.1*np.log2(0.1) - 0.9*np.log2(0.9)):.4f} bits (closed form)")
# ⚠️ Gotcha: s controls the Lagrange multiplier, NOT distortion directly.
# Sweep s from 0 (zero rate) to ∞ (zero distortion) to trace the full curve.
"""),
    heading3("6c — β-VAE as R-D Optimisation"),
    code_block("python",
"""import torch, torch.nn as nn, torch.nn.functional as F

class BetaVAE(nn.Module):
    \"\"\"β-VAE whose ELBO minimises the rate-distortion Lagrangian.

    beta=1: standard VAE (balanced rate-distortion)
    beta>1: high compression, more distortion, better disentanglement
    beta<1: high fidelity, less disentangled
    \"\"\"
    def __init__(self, input_dim=784, latent_dim=16, beta=1.0):
        super().__init__()
        self.beta = beta
        self.encoder = nn.Sequential(nn.Linear(input_dim, 256), nn.ReLU())
        self.mu = nn.Linear(256, latent_dim)
        self.log_var = nn.Linear(256, latent_dim)
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 256), nn.ReLU(),
            nn.Linear(256, input_dim), nn.Sigmoid()
        )

    def encode(self, x):
        h = self.encoder(x)
        return self.mu(h), self.log_var(h)

    def reparameterise(self, mu, log_var):
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        return mu + eps * std

    def forward(self, x):
        mu, log_var = self.encode(x)
        z = self.reparameterise(mu, log_var)
        return self.decoder(z), mu, log_var

    def loss(self, x, x_hat, mu, log_var):
        # Distortion: binary cross-entropy reconstruction loss
        recon = F.binary_cross_entropy(x_hat, x, reduction='sum')
        # Rate: KL divergence = upper bound on I(X; Z)
        # = -0.5 * sum(1 + log_var - mu^2 - exp(log_var))
        rate = -0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp())
        # β scales rate penalty ↔ moves operating point on R-D curve
        # ⚠️ beta > 1 compresses the code → blurrier reconstructions
        return recon + self.beta * rate, recon.item(), rate.item()

# Usage
model = BetaVAE(beta=4.0)  # High compression → more disentangled
"""),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy): What is rate-distortion theory?"),
    para(rt("Shannon's theory of the minimum bit rate needed to represent a source within an allowed average distortion. The rate-distortion function "), eq(r"R(D)"), rt(" gives this minimum as a function of the tolerable distortion "), eq(r"D"), rt(". It is a hard lower bound — no codec can beat it.")),
    heading3("Q2 (Easy): What shape is the R-D curve and why?"),
    para(rt("It is convex and non-increasing. Non-increasing: allowing more distortion never requires more bits. Convex: improving distortion from "), eq(r"D"), rt(" to "), eq(r"D/2"), rt(" always costs more additional bits than the next halving (diminishing returns on quality).")),
    heading3("Q3 (Medium): Derive R(D) for a Gaussian source."),
    para(rt("The Gaussian source "), eq(r"X \sim \mathcal{N}(0, \sigma^2)"), rt(" with MSE distortion has "), eq(r"R(D) = \frac{1}{2}\log_2(\sigma^2/D)"), rt(" for "), eq(r"0 \leq D \leq \sigma^2"), rt(", zero otherwise. The proof uses: (1) the optimal channel is Gaussian (additive noise "), eq(r"N \sim \mathcal{N}(0,D)"), rt("), (2) "), eq(r"I(X;\hat{X}) = h(X) - h(X|\hat{X}) = \frac{1}{2}\log_2(\sigma^2/D)"), rt(". The Gaussian is optimal by the entropy power inequality: it maximises "), eq(r"h(X|\hat{X})"), rt(" for fixed distortion, minimising mutual information.")),
    heading3("Q4 (Medium): How does β-VAE relate to rate-distortion theory?"),
    para(rt("The β-VAE ELBO is "), eq(r"\mathcal{L} = \mathbb{E}[\log p(x|z)] - \beta\, KL(q(z|x)\|p(z))"), rt(". This is the Lagrangian relaxation of "), eq(r"\min_\theta \mathbb{E}[d(x,\hat{x})]"), rt(" s.t. "), eq(r"I(X;Z) \leq R"), rt(" with "), eq(r"\beta"), rt(" as the Lagrange multiplier. Minimising for different "), eq(r"\beta"), rt(" traces the rate-distortion curve. "), rt("Follow-up trap:", bold=True), rt(" Is the KL term exactly the rate? No — "), eq(r"KL(q(z|x)\|p(z)) = I(X;Z) + KL(q(z)\|p(z)) \geq I(X;Z)"), rt(". The VAE over-penalises rate unless the aggregate posterior matches the prior.")),
    heading3("Q5 (Hard): What is the reverse water-filling theorem?"),
    para(rt("For a vector Gaussian source "), eq(r"\mathbf{X} = (X_1, \ldots, X_n)"), rt(" with independent components of variances "), eq(r"\sigma_i^2"), rt(", the optimal distortion allocation under total budget "), eq(r"D"), rt(" is: "), eq(r"D_i = \min(\theta, \sigma_i^2)"), rt(", where the water level "), eq(r"\theta"), rt(" is chosen so "), eq(r"\sum_i D_i = D"), rt(". Components with "), eq(r"\sigma_i^2 < \theta"), rt(" are allocated "), eq(r"D_i = \sigma_i^2"), rt(" (zero bits — just predict the mean). The total rate is "), eq(r"R = \sum_{i:\sigma_i^2 > \theta} \frac{1}{2}\log_2(\sigma_i^2/\theta)"), rt(". This is called 'reverse' water-filling because we pour water into low-variance components.")),
    heading3("Q6 (Hard): How does neural image compression approach R-D limits?"),
    para(rt("Ballé et al. (2017) showed that a neural autoencoder with quantised latents can be trained end-to-end to minimise "), eq(r"R + \lambda D"), rt(" (the R-D Lagrangian). The rate is estimated via an entropy model on quantised latents; the distortion is MSE or perceptual loss. On Kodak benchmarks, modern neural codecs (e.g., Cheng2020, VCT) match or exceed HEVC Intra compression, coming within ~10-20% of the Gaussian R-D bound for natural images.")),
    heading3("Multi-Level Explanations"),
    para(rt("Explain to a PhD Researcher: ", bold=True), rt("The R-D function is the solution to a convex optimisation over the space of Markov kernels "), eq(r"p(\hat{x}|x)"), rt(". Its geometric properties — convexity, slope "), eq(r"dR/dD = s"), rt(" (negative Lagrange multiplier) — follow directly from the duality with the capacity-cost function. The Gaussian case achieves the bound because the Gaussian maximises differential entropy for fixed variance, making the additive noise channel optimal via the entropy power inequality.")),
    para(rt("Explain to a Research Scientist/Engineer: ", bold=True), rt("R(D) is the theoretical minimum bit rate for a given distortion level. For a Gaussian source, "), eq(r"R(D) = \frac{1}{2}\log_2(\sigma^2/D)"), rt(" bits/sample. In β-VAE, "), eq(r"\beta"), rt(" controls which point on the R-D curve you operate at — higher "), eq(r"\beta"), rt(" means more compression (lower rate, higher distortion). For neural codecs, this is literally the training objective: minimise "), eq(r"R + \lambda D"), rt(" end-to-end.")),
    heading3("Red Flags"),
    callout("🚩", rt("Wrong: ", bold=True), rt("'R(D) is the performance of JPEG.' — No. R(D) is the Shannon limit; JPEG operates above this curve. JPEG-2000 with entropy coding is closer but still not optimal. The gap between JPEG and R(D) represents 1-2x compression overhead on natural images.")),
    callout("🚩", rt("Wrong: ", bold=True), rt("'The KL term in VAE = I(X;Z).' — Only when the aggregate posterior "), eq(r"q(z) = \int q(z|x)p(x)dx"), rt(" matches the prior "), eq(r"p(z)"), rt(". In practice they differ, so KL > I(X;Z).")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    heading3("Rate-Distortion vs Alternatives"),
    table(5,
        table_row(["Method", "Rate guarantee", "Distortion type", "Practical gap", "Best for"]),
        table_row(["Shannon R-D bound", "Optimal (impossible to beat)", "Any bounded metric", "N/A — theoretical", "Benchmarking codecs"]),
        table_row(["JPEG / DCT coding", "~1.5-2x above R-D", "MSE (quantised DCT)", "~3-5 dB sub-optimal", "Legacy web images"]),
        table_row(["JPEG 2000 / Wavelet", "~1.2-1.5x above R-D", "MSE (wavelet subbands)", "~1-3 dB sub-optimal", "Medical/archival images"]),
        table_row(["BPG / HEVC Intra", "~1.1x above R-D", "MSE + VVC tools", "<1 dB sub-optimal", "Video keyframes"]),
        table_row(["Neural codec (Ballé)", "~1.05-1.15x above R-D", "MSE or perceptual", "Near-optimal", "State-of-the-art compression"]),
        table_row(["β-VAE (β=1)", "No hard guarantee", "Recon. + KL", "Not optimised for R-D", "Generative modelling"]),
    ),
    heading3("When to Use R-D Theory"),
    bullet(rt("Benchmarking: ", bold=True), rt("Evaluate how close your codec is to the Shannon limit.")),
    bullet(rt("Architecture choice: ", bold=True), rt("Use R(D) to set the target rate budget for a given quality constraint.")),
    bullet(rt("β-VAE design: ", bold=True), rt("Interpret "), eq(r"\beta"), rt(" as a Lagrange multiplier and choose it to operate at the desired point on the R-D curve.")),
    bullet(rt("Neural codec training: ", bold=True), rt("Directly optimise "), eq(r"R + \lambda D"), rt(" using differentiable entropy models.")),
    heading3("When NOT to Use"),
    bullet(rt("R-D theory assumes "), rt("ergodic sources", italic=True), rt(" — real images have spatial correlations that require more sophisticated source models.")),
    bullet(rt("MSE distortion correlates poorly with human perception. Use perceptual R-D (SSIM, LPIPS) for visual quality tasks.")),
    bullet(rt("For very short block lengths, the asymptotic guarantee degrades; use finite-length analysis instead.")),
    callout("🎯", rt("Decision guide: ", bold=True), rt("Want to know if your codec is efficient? Compute "), eq(r"R(D)"), rt(" for your source model and compare. Want to train a β-VAE for disentangled representations? Set "), eq(r"\beta"), rt(" ≈ 4–10. Want near-optimal image compression? Use a neural codec (Ballé et al.) trained with "), eq(r"R + \lambda D"), rt(".")),
    divider(),

    # ── Section 9: Explainer Embed ─────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ─────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Shannon entropy and mutual information (§4.1)")),
    bullet(rt("Source coding / lossless compression (§4.2)")),
    bullet(rt("KL divergence and information measures (§4.1)")),
    bullet(rt("Gaussian distribution and differential entropy")),
    heading3("What to Learn Next"),
    bullet(rt("Channel capacity (§4.2) — the dual problem")),
    bullet(rt("Information bottleneck principle — R-D with a relevance constraint")),
    bullet(rt("Vector quantisation (VQ-VAE) — discrete version of R-D compression")),
    bullet(rt("Neural image compression (Ballé et al.) — practical R-D optimisation")),
    heading3("Key Papers"),
    bullet(rt("Shannon (1959). \"Coding Theorems for a Discrete Source with a Fidelity Criterion.\" IRE National Convention Record. — Founding paper of R-D theory.")),
    bullet(rt("Berger (1971). Rate Distortion Theory. Prentice-Hall. — Comprehensive textbook treatment.")),
    bullet(rt("Higgins et al. (2017). \"β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework.\" ICLR. — β-VAE as R-D Lagrangian.")),
    bullet(rt("Alemi et al. (2018). \"Fixing a Broken ELBO.\" ICML. — Precise R-D interpretation of the VAE objective.")),
    bullet(rt("Ballé et al. (2017). \"End-to-end Optimized Image Compression.\" ICLR. — Neural codec approaching R-D limits.")),
    heading3("Best Resources"),
    bullet(rt("Cover & Thomas, Elements of Information Theory, Chapter 10 (Rate-Distortion Theory).")),
    bullet(rt("Blahut (1972). \"Computation of Channel Capacity and Rate-Distortion Functions.\" IEEE Trans. Info. Theory. — Original Blahut-Arimoto paper.")),
    bullet(rt("Lecture notes: David MacKay, Information Theory, Inference, and Learning Algorithms, Chapter 8.")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Entropy & Information Theory (§4.1), Source Coding Theorem (§4.2), KL Divergence (§4.1), VAE (Generative Models), β-VAE, Information Bottleneck, Neural Image Compression.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
