#!/usr/bin/env python3
"""Update Notion page for: KL Divergence Loss (VAEs)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81d8-bdd5-e7e4acdbcba1"
ICON = "🟠"  # Advanced
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/AI/explainers/kl_divergence_loss_explainer.html"},
}

blocks = [
    # ── Section 1: The 30-Second Version ──
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("When a Variational Autoencoder (VAE) compresses an input into a latent code, it doesn't output a single point — it outputs a small probability cloud (a Gaussian distribution) of possible codes. The KL divergence loss is a penalty that keeps this cloud close to a fixed, simple reference cloud (a standard normal distribution), so the latent space stays organized and usable for generating new data.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine every student in a school is assigned a locker location described as \"somewhere near coordinates (x, y), give or take some fuzziness.\" If left unconstrained, students would claim distant, tiny, private corners of the building to avoid ever being confused with each other. The KL penalty is a rule that says: \"keep your locker's average location close to the building's center, and keep your fuzziness close to a standard amount.\" That way, if you pick a random spot near the center, you'll land on a real, sensible locker.")),
    para(rt("Summary: KL divergence loss regularizes a VAE's encoder output toward a fixed prior distribution (usually the standard normal), trading off against the reconstruction loss to keep the latent space smooth and generative.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("KL loss has a closed-form for Gaussians — ½(μ² + σ² − 1 − log σ²) — and it is zero exactly when the encoder gives up and ignores the input (posterior collapse), not when the model is \"doing great.\"")),
    divider(),

    # ── Section 2: Historical Context ──
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Plain autoencoders learn a deterministic mapping from input to a single latent point. The latent space they produce is not organized — it may have holes, disconnected clusters, and regions that decode to garbage. You cannot reliably sample a random point and get a realistic output. Autoencoders compress; they do not generate.")),
    heading3("What Came Before"),
    para(rt("Classical autoencoders (and denoising autoencoders) minimized only a reconstruction loss. Nothing constrained the geometry of the latent space, so the encoder was free to scatter codes arbitrarily — memorizing training points as isolated spikes rather than forming a continuous, sample-able manifold.")),
    heading3("The Breakthrough"),
    para(rt("Kingma & Welling (2013) reframed autoencoding as approximate Bayesian inference: the encoder becomes a variational approximation "), eq(r"q_\phi(z|x)"), rt(" to the true (intractable) posterior "), eq(r"p(z|x)"), rt(". Maximizing the Evidence Lower Bound (ELBO) naturally introduces a KL divergence term between "), eq(r"q_\phi(z|x)"), rt(" and a chosen prior "), eq(r"p(z)"), rt(" — for the first time giving a principled, differentiable reason to regularize the latent space.")),
    heading3("Key Paper(s)"),
    bullet(rt("Kingma & Welling, \"Auto-Encoding Variational Bayes\", ICLR 2014 — introduced the VAE, the reparameterization trick, and the closed-form Gaussian KL term.", italic=False)),
    bullet(rt("Rezende, Mohamed & Wierstra, \"Stochastic Backpropagation and Approximate Inference in Deep Generative Models\", ICML 2014 — independently derived the same reparameterized ELBO objective.")),
    bullet(rt("Higgins et al., \"β-VAE: Learning Basic Visual Concepts with a Constrained Variational Framework\", ICLR 2017 — introduced the β weight on the KL term for disentanglement.")),
    heading3("Evolution Timeline"),
    para(rt("Deterministic Autoencoders → Variational Autoencoders (KL-regularized ELBO) → β-VAE (weighted KL for disentanglement) → VQ-VAE / discrete latents (side-steps KL collapse) → Diffusion models (KL appears again, summed across many small denoising steps).")),
    table(3,
        table_row(["Dimension", "Autoencoder (Before)", "VAE (After)"]),
        table_row(["Latent structure", "Arbitrary, disconnected", "Continuous, organized around prior"]),
        table_row(["Can generate new samples?", "No — no sampling procedure", "Yes — sample z ~ N(0,I), decode"]),
        table_row(["Loss function", "Reconstruction only", "Reconstruction − KL(q(z|x)‖p(z))"]),
        table_row(["Interpolation in latent space", "Often produces garbage", "Smooth, semantically meaningful"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ──
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Let "), eq(r"x"), rt(" be an observed data point and "), eq(r"z \in \mathbb{R}^d"), rt(" a latent variable. The encoder (inference network) outputs a distribution "), eq(r"q_\phi(z|x) = \mathcal{N}(\mu_\phi(x), \operatorname{diag}(\sigma^2_\phi(x)))"), rt(". The prior is fixed: "), eq(r"p(z) = \mathcal{N}(0, I)"), rt(". The KL divergence loss is "), eq(r"D_{KL}(q_\phi(z|x)\,\|\,p(z))"), rt(", the expected log-ratio between the two densities.")),
    heading3("Building Blocks"),
    bullet(rt("Encoder network — maps "), eq(r"x"), rt(" to "), eq(r"(\mu, \log\sigma^2)")),
    bullet(rt("Reparameterization trick — "), eq(r"z = \mu + \sigma \odot \epsilon,\ \epsilon\sim\mathcal{N}(0,I)"), rt(" — makes sampling differentiable")),
    bullet(rt("Decoder network — maps sampled "), eq(r"z"), rt(" back to a reconstruction "), eq(r"\hat{x}")),
    bullet(rt("ELBO — the training objective combining reconstruction likelihood and the KL penalty")),
    heading3("Core Property / Invariant"),
    para(rt("The KL term is minimized (=0) uniquely at "), eq(r"\mu=0, \sigma^2=1"), rt(" — i.e., when the posterior exactly equals the prior. This is a convex, smooth function of "), eq(r"(\mu,\sigma^2)"), rt(" with a single global minimum, so gradient descent on it is well-behaved.")),
    callout("🔑", rt("Key Concept: ", bold=True), rt("The KL term is per-dimension additive for diagonal Gaussians — the total KL is the sum of d independent 1-D KL terms, one per latent dimension. This is exactly what makes it closed-form and cheap.")),
    heading3("Prerequisites Check"),
    para(rt("To understand this, you should know: probability distributions (Gaussian pdf), expectation, Kullback-Leibler divergence for two known distributions, basic variational inference / Bayes' rule, and the standard autoencoder architecture.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ──
    heading2("🏗️ Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("Where KL Sits in the VAE Pipeline"),
    para(rt("Forward pass: "), eq(r"x"), rt(" → encoder → "), eq(r"(\mu, \log\sigma^2)"), rt(" → reparameterized sample "), eq(r"z"), rt(" → decoder → "), eq(r"\hat{x}"), rt(". The KL term is computed directly from "), eq(r"(\mu, \log\sigma^2)"), rt(" — it never touches the sampled "), eq(r"z"), rt(" or the decoder at all. It is a pure function of the encoder's output statistics.")),
    heading3("Internal Mechanism Breakdown"),
    para(rt("WHAT: For each of the d latent dimensions, compute "), eq(r"\tfrac12(\mu_i^2 + \sigma_i^2 - 1 - \log\sigma_i^2)"), rt(" and sum. "), rt("HOW: Implemented as a single vectorized expression over the encoder's "), eq(r"\mu"), rt(" and "), eq(r"\log\sigma^2"), rt(" outputs — no sampling or Monte Carlo needed because the Gaussian-Gaussian KL integral is analytic. "), rt("WHY designed this way: using log-variance (not variance directly) as the network output avoids needing a positivity constraint on σ² and improves numerical stability of the log term.")),
    heading3("Numerical Trace"),
    para(rt("Encoder outputs "), eq(r"\mu = 1.2"), rt(", "), eq(r"\log\sigma^2 = \log(0.6) \approx -0.511"), rt(" for one latent dimension.")),
    numbered(rt("σ² = exp(−0.511) = 0.600")),
    numbered(rt("Term 1: 0.5 × μ² = 0.5 × 1.44 = 0.720")),
    numbered(rt("Term 2: 0.5 × σ² = 0.5 × 0.600 = 0.300")),
    numbered(rt("Term 3: −0.5 (constant)")),
    numbered(rt("Term 4: −0.5 × log(σ²) = −0.5 × (−0.511) = 0.255")),
    numbered(rt("Sum: 0.720 + 0.300 − 0.500 + 0.255 = 0.775 = D_KL for this dimension")),
    para(rt("If d = 20 latent dimensions all had this same value, total KL loss = 20 × 0.775 = 15.5 — this is the number added (after scaling by β) to the negative reconstruction log-likelihood.")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("Posterior collapse — decoder is powerful enough to ignore z; encoder drives μ→0, σ²→1 for all x, KL→0, latent code carries no information.")),
    bullet(rt("Numerical overflow — if the network outputs very large log-variance early in training, exp(logvar) can overflow; clamp log-variance to a sane range (e.g. [-10, 10]).")),
    bullet(rt("KL vanishing in sequence VAEs — strong autoregressive decoders (e.g., LSTM/Transformer text decoders) are especially prone to collapse; addressed via KL annealing, free bits, or weakening the decoder.")),
    callout("🎯", rt("Design Decision: ", bold=True), rt("Why sum over dimensions and average over the batch, not the reverse? Reconstruction loss is typically summed over all pixels/tokens of an example; to keep the two terms on a comparable per-example scale, KL is also summed over its d dimensions, then both are averaged over the batch.")),
    divider(),

    # ── Section 5: The Math ──
    heading2("📐 The Math Behind It"),
    heading3("Full Derivation"),
    para(rt("Start from the definition of KL divergence for continuous distributions:")),
    equation_block(r"D_{KL}(q\|p) = \int q(z)\log\frac{q(z)}{p(z)}\,dz = \mathbb{E}_{q}\big[\log q(z) - \log p(z)\big]"),
    para(rt("Substitute the univariate Gaussian log-densities "), eq(r"q(z)=\mathcal{N}(z;\mu,\sigma^2)"), rt(" and "), eq(r"p(z)=\mathcal{N}(z;0,1)"), rt(":")),
    equation_block(r"\log q(z) = -\tfrac12\log(2\pi\sigma^2) - \frac{(z-\mu)^2}{2\sigma^2}, \qquad \log p(z) = -\tfrac12\log(2\pi) - \frac{z^2}{2}"),
    para(rt("Subtract and take the expectation under q. Using the identities "), eq(r"\mathbb{E}_q[(z-\mu)^2]=\sigma^2"), rt(" and "), eq(r"\mathbb{E}_q[z^2]=\mu^2+\sigma^2"), rt(":")),
    equation_block(r"D_{KL} = \mathbb{E}_q\Big[-\tfrac12\log\sigma^2 - \frac{(z-\mu)^2}{2\sigma^2} + \tfrac12\log(1) + \frac{z^2}{2}\Big] = -\tfrac12\log\sigma^2 - \tfrac12 + \tfrac12(\mu^2+\sigma^2)"),
    para(rt("Rearranged into the standard closed form:")),
    equation_block(r"D_{KL}\big(\mathcal{N}(\mu,\sigma^2)\,\|\,\mathcal{N}(0,1)\big) = \frac12\big(\mu^2+\sigma^2-1-\log\sigma^2\big)"),
    para(rt("For a d-dimensional diagonal Gaussian posterior, sum over dimensions:")),
    equation_block(r"D_{KL}\big(q_\phi(z|x)\,\|\,\mathcal{N}(0,I)\big) = \frac12\sum_{i=1}^{d}\Big(\mu_i^2+\sigma_i^2-1-\log\sigma_i^2\Big)"),
    heading3("The Full ELBO Loss"),
    para(rt("The VAE is trained by maximizing the Evidence Lower Bound (equivalently, minimizing its negative):")),
    equation_block(r"\mathcal{L}(\theta,\phi;x) = \mathbb{E}_{q_\phi(z|x)}\big[\log p_\theta(x|z)\big] - \beta \cdot D_{KL}\big(q_\phi(z|x)\,\|\,p(z)\big)"),
    heading3("Gradient Computation"),
    para(rt("Because μ and log σ² are direct, deterministic outputs of the encoder, the KL term's gradients are exact — no sampling variance:")),
    equation_block(r"\frac{\partial D_{KL}}{\partial \mu_i} = \mu_i, \qquad \frac{\partial D_{KL}}{\partial \log\sigma_i^2} = \tfrac12(\sigma_i^2 - 1)"),
    para(rt("This contrasts with the reconstruction term, whose gradient requires the reparameterization trick "), eq(r"z=\mu+\sigma\odot\epsilon"), rt(" to be differentiable through the sampling step.")),
    heading3("Convergence / Guarantees"),
    para(rt("D_KL(q‖p) ≥ 0 always (Gibbs' inequality / Jensen's inequality applied to the concave log), with equality iff q = p almost everywhere. This guarantees the ELBO is truly a lower bound on log p(x), and the KL term alone has a unique, convex minimum at μ=0, σ²=1 per dimension.")),
    callout("⚠️", rt("Common Misconception: ", bold=True), rt("\"Minimizing KL loss to exactly zero is the training goal.\" False — KL=0 means posterior collapse (the encoder ignores x). A well-trained VAE has KL strictly positive and stable, reflecting genuine information flowing from x into z.")),
    divider(),

    # ── Section 6: Code Implementation ──
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", '''import numpy as np

def kl_divergence_gaussian(mu, logvar):
    """Closed-form KL(N(mu, sigma^2) || N(0, I)) per example.

    Args:
        mu: array (batch, d) of posterior means
        logvar: array (batch, d) of posterior log-variances
    Returns:
        array (batch,) of per-example KL divergence, summed over d dims
    """
    # sigma^2 = exp(logvar); avoids needing a positivity constraint on the
    # network output (log-variance can be any real number)
    sigma2 = np.exp(logvar)

    # Per-dimension term: 0.5 * (mu^2 + sigma^2 - 1 - log(sigma^2))
    kl_per_dim = 0.5 * (mu**2 + sigma2 - 1.0 - logvar)

    # Sum over latent dimensions -> one scalar KL per example
    return np.sum(kl_per_dim, axis=-1)


def reparameterize(mu, logvar, rng):
    """Differentiable sample z = mu + sigma * epsilon."""
    std = np.exp(0.5 * logvar)
    eps = rng.standard_normal(mu.shape)
    return mu + eps * std


# Example: batch of 3 examples, 4 latent dims
rng = np.random.default_rng(0)
mu = np.array([[0.1, -0.3, 1.2, 0.0],
               [2.0, 0.0, 0.0, -1.5],
               [0.0, 0.0, 0.0, 0.0]])
logvar = np.array([[-0.2, 0.1, -0.5, 0.0],
                    [0.5, 0.0, 0.0, 1.0],
                    [0.0, 0.0, 0.0, 0.0]])

kl = kl_divergence_gaussian(mu, logvar)
print("Per-example KL:", kl)   # third row (mu=0, logvar=0) -> KL = 0 (matches prior)
'''),
    heading3("6b — Production Usage (PyTorch)"),
    code_block("python", '''import torch
import torch.nn.functional as F

def vae_loss(x, x_recon, mu, logvar, beta=1.0):
    """Beta-VAE loss: reconstruction + beta * KL, averaged over batch.

    Key hyperparameters:
      beta: KL weight. beta=1 is the standard VAE (Kingma & Welling 2014).
            beta>1 trades reconstruction fidelity for disentanglement
            (Higgins et al. 2017). beta<1 favors sharper reconstructions.
    """
    # Reconstruction term: e.g. binary cross-entropy summed over pixels
    recon_loss = F.binary_cross_entropy(x_recon, x, reduction='sum') / x.size(0)

    # Closed-form KL, summed over latent dims, averaged over batch
    kl_loss = 0.5 * torch.sum(mu.pow(2) + logvar.exp() - 1 - logvar, dim=-1)
    kl_loss = kl_loss.mean()

    return recon_loss + beta * kl_loss, recon_loss, kl_loss


# ⚠️ Gotcha: KL annealing. Turning on the full KL weight from step 0 often
# causes posterior collapse before the decoder has learned to use z at all.
# Common fix: linearly ramp beta from 0 -> target value over the first
# N training steps ("KL warm-up" / "KL annealing").
def kl_annealing_weight(step, warmup_steps=10000, target_beta=1.0):
    return target_beta * min(1.0, step / warmup_steps)
'''),
    divider(),

    # ── Section 7: Interview Deep-Dive ──
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy): What does the KL term in a VAE loss do?"),
    para(rt("A: It regularizes the encoder's output distribution "), eq(r"q(z|x)"), rt(" to stay close to a fixed prior "), eq(r"p(z)=\mathcal{N}(0,I)"), rt(", keeping the latent space smooth, continuous, and sample-able so new data can be generated by sampling z from the prior.")),
    heading3("Q2 (Medium): Why does the Gaussian-Gaussian KL have a closed form, while the reconstruction term needs sampling?"),
    para(rt("A: Both q(z|x) and p(z) are Gaussian, and the KL integral between two Gaussians is analytically solvable (it reduces to simple moment expressions: mean, variance, log-variance). The reconstruction term, "), eq(r"\mathbb{E}_{q}[\log p_\theta(x|z)]"), rt(", involves an arbitrary decoder network inside the expectation, so it must be approximated via Monte Carlo sampling (usually a single sample per step) using the reparameterization trick.")),
    heading3("Q3 (Medium): What is posterior collapse, and why does it happen?"),
    para(rt("A: Posterior collapse is when q(z|x) → p(z) for every x (KL → 0), meaning z carries no information about x. It happens when the decoder is expressive enough to model x well without using z (e.g., strong autoregressive decoders), so the optimizer takes the \"free\" path of minimizing KL to zero rather than paying the KL cost to encode useful information.")),
    para(rt("⚠️ Follow-up trap: \"So we should just remove the KL term?\" A: No — removing it entirely turns the model into a plain autoencoder with no valid generative sampling procedure. The fix is to weaken this specific failure mode (KL annealing, free bits, weaker decoder) while keeping the term.", italic=True)),
    heading3("Q4 (Hard): Derive the closed-form KL between N(μ,σ²) and N(0,1)."),
    para(rt("A: [See full derivation above] — expand both log-densities, take expectation under q using "), eq(r"\mathbb{E}_q[(z-\mu)^2]=\sigma^2"), rt(" and "), eq(r"\mathbb{E}_q[z^2]=\mu^2+\sigma^2"), rt(", simplify to "), eq(r"\tfrac12(\mu^2+\sigma^2-1-\log\sigma^2)"), rt(".")),
    heading3("Q5 (Hard): What does β>1 do in a β-VAE, mathematically and practically?"),
    para(rt("A: It scales the KL penalty relative to reconstruction: "), eq(r"\mathcal{L}=\text{recon} - \beta D_{KL}"), rt(". Larger β forces the aggregate posterior closer to the isotropic prior for every input, which (empirically, via an information-bottleneck argument) encourages each latent dimension to encode an independent, interpretable factor of variation — at the cost of blurrier reconstructions since less total information can pass through the bottleneck.")),
    heading3("Multi-Level Explanations"),
    para(rt("To a PhD Researcher: ", bold=True), rt("The KL term arises from the ELBO decomposition "), eq(r"\log p(x) = \mathcal{L}(\theta,\phi;x) + D_{KL}(q_\phi(z|x)\|p(z|x))"), rt("; since the true posterior "), eq(r"p(z|x)"), rt(" is intractable, we instead bound log p(x) below and the KL(q‖p(z)) term in the ELBO acts as an amortized variational regularizer, connecting to rate-distortion theory (KL = \"rate\", reconstruction = \"distortion\").")),
    para(rt("To a Research Scientist/Engineer: ", bold=True), rt("It's one line of code — 0.5*(mu²+var−1−logvar).sum() — but it's the single most common source of training instability in VAEs. Watch KL and reconstruction loss separately in your logs; if KL crashes to ~0 early, you have posterior collapse and need annealing or free bits.")),
    heading3("System Design Angle"),
    para(rt("In production generative pipelines (e.g., VAE-based image compression, anomaly detection via reconstruction+KL score, or VAE priors feeding downstream diffusion/latent models), the KL loss weight β is a tunable knob exposed in config, and per-dimension KL values are often logged individually to detect dead latent dimensions (KL≈0 for that dim across the whole dataset).")),
    heading3("Red Flags"),
    bullet(rt("Saying KL should be driven to exactly zero as a training goal.")),
    bullet(rt("Confusing the KL term with the reconstruction loss's role — reconstruction is what needs the reparameterization trick, not KL.")),
    bullet(rt("Forgetting the closed form exists — proposing to estimate the KL term via sampling when both distributions are Gaussian.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ──
    heading2("⚖️ Comparison & Trade-offs"),
    table(4,
        table_row(["Dimension", "Standard VAE (β=1)", "β-VAE (β>1)", "VQ-VAE (discrete)"]),
        table_row(["KL weight", "1.0", "Tunable, typically 4–150", "N/A — no KL term (codebook + commitment loss instead)"]),
        table_row(["Latent space", "Continuous, mildly organized", "Continuous, strongly disentangled", "Discrete codebook, no collapse risk"]),
        table_row(["Reconstruction quality", "Good baseline", "Blurrier as β increases", "Sharp — avoids KL-induced blur"]),
        table_row(["Posterior collapse risk", "Moderate", "Higher (stronger pull to prior)", "Not applicable"]),
    ),
    heading3("When to Use"),
    bullet(rt("Standard KL loss (β=1): general-purpose generative modeling where you need a valid sampling procedure and don't need interpretable latent axes.")),
    bullet(rt("β-VAE (β>1): representation learning tasks that need disentangled, interpretable factors (e.g., separating pose from identity in faces).")),
    bullet(rt("KL annealing / free bits: any VAE with a powerful decoder (RNN/Transformer) prone to posterior collapse.")),
    heading3("When NOT to Use"),
    bullet(rt("If you don't need a generative/sampling capability at all — a plain autoencoder (no KL term) is simpler and gives sharper reconstructions.")),
    bullet(rt("If your decoder already struggles to reconstruct — adding heavy KL weight will worsen fidelity without a clear disentanglement benefit.")),
    heading3("Advantages"),
    bullet(rt("Closed-form, exact gradients — cheap to compute, no sampling noise in this term.")),
    bullet(rt("Provides a principled, tunable regularization knob (β) connecting directly to information-theoretic rate-distortion trade-offs.")),
    heading3("Disadvantages"),
    bullet(rt("Prone to posterior collapse with strong decoders.")),
    bullet(rt("Fixed isotropic Gaussian prior is a strong, sometimes unrealistic assumption about the true latent structure.")),
    callout("🎯", rt("Decision: ", bold=True), rt("Use standard KL (β=1) as your default VAE regularizer. Increase β only if you specifically need disentangled representations, and add KL annealing whenever you observe collapse (KL loss crashing near 0 early in training).")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ──
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/AI/explainers/kl_divergence_loss_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("KL Divergence (general definition and properties)")),
    bullet(rt("Variational Inference / Evidence Lower Bound (ELBO)")),
    bullet(rt("Reparameterization Trick")),
    bullet(rt("Gaussian distributions and maximum likelihood estimation")),
    heading3("What to Learn Next"),
    bullet(rt("β-VAE and disentangled representation learning")),
    bullet(rt("Posterior collapse mitigation (KL annealing, free bits, cyclical annealing)")),
    bullet(rt("VQ-VAE and discrete latent variable models")),
    bullet(rt("Diffusion models (KL terms reappear across many small denoising steps)")),
    heading3("Key Papers"),
    bullet(rt("Kingma & Welling (2014) — \"Auto-Encoding Variational Bayes\" — introduces the VAE and the closed-form Gaussian KL term.")),
    bullet(rt("Rezende, Mohamed & Wierstra (2014) — \"Stochastic Backpropagation and Approximate Inference in Deep Generative Models\" — parallel derivation of reparameterized variational inference.")),
    bullet(rt("Higgins et al. (2017) — \"β-VAE\" — weights the KL term to encourage disentanglement.")),
    bullet(rt("Bowman et al. (2016) — \"Generating Sentences from a Continuous Space\" — identifies and addresses posterior collapse via KL annealing in text VAEs.")),
    bullet(rt("Razavi et al. (2019) — \"Generating Diverse High-Fidelity Images with VQ-VAE-2\" — sidesteps KL collapse with discrete latents.")),
    heading3("Best Resources"),
    bullet(rt("Kingma & Welling, \"An Introduction to Variational Autoencoders\" (2019 tutorial monograph) — comprehensive, derivation-heavy treatment.")),
    bullet(rt("Stanford CS236 (Deep Generative Models) lecture notes on VAEs.")),
    bullet(rt("Lilian Weng's blog: \"From Autoencoder to Beta-VAE\" — clear derivations and diagrams.")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Variational Autoencoders, ELBO / Variational Inference, Reparameterization Trick, β-VAE, Posterior Collapse, Rate-Distortion Theory, Diffusion Models.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
