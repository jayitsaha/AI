#!/usr/bin/env python3
"""Update Notion page for: Non-informative & weakly informative priors (Jeffreys prior)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8150-aa8e-ee58dea0b259"
ICON = "🟡"  # Intermediate
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/noninformative_jeffreys_priors_explainer.html"

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": EXPLAINER_URL},
}

blocks = [

    # ── Section 1: 30-Second Version ──────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("When you run a Bayesian analysis you must choose a prior — your beliefs about a parameter before seeing data. Sometimes you want the data to do all the talking, with almost no influence from the prior. The challenge: there is no obviously 'neutral' choice. A prior that looks flat and uninformative in one representation turns out to be strongly informative in another.")),
    heading3("Real-World Analogy"),
    para(rt("Suppose you measure coin fairness by the probability of heads "), eq(r"p"), rt(". Saying 'I believe all values of "), eq(r"p"), rt(" are equally likely' sounds neutral. But if you instead describe the coin by its log-odds "), eq(r"\phi = \log\!\left(\frac{p}{1-p}\right)"), rt(", that 'flat' prior on "), eq(r"p"), rt(" becomes a strongly peaked, non-flat distribution on "), eq(r"\phi"), rt(". Your 'no opinion' belief depends on what unit you measure in — like saying 'I'm equally likely to weigh anything between 0 and 100' in kilograms vs. pounds.")),
    heading3("One-Sentence Summary"),
    para(rt("The Jeffreys prior "), eq(r"\pi(\theta) \propto \sqrt{\mathcal{I}(\theta)}"), rt(" — proportional to the square root of the Fisher information — is the unique prior that assigns equal plausibility to statistically equivalent models regardless of which parameterization you choose.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("A flat prior is NOT uninformative — it is informative in every parameterization except one. Jeffreys prior is the only prior invariant to smooth reparameterization, and for a Bernoulli parameter it equals Beta(1/2, 1/2), not Beta(1, 1).")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Early Bayesian analysis (Laplace, 1812) used flat priors — "), eq(r"\pi(\theta) \propto 1"), rt(" — as a natural expression of ignorance. This worked well for location parameters but produced incoherent results elsewhere: for a Poisson rate "), eq(r"\lambda"), rt(", a flat prior on "), eq(r"\lambda"), rt(" is not flat on "), eq(r"\sqrt{\lambda}"), rt(" or "), eq(r"\log\lambda"), rt(". The inference changes depending on how you set up the problem.")),
    heading3("What Came Before"),
    para(rt("The principle of indifference (Laplace, Keynes) says: if there is no reason to prefer one hypothesis over another, assign equal probabilities. But equal in what sense? In the absence of a principled answer, different analysts reached contradictory conclusions from the same data.")),
    heading3("The Breakthrough"),
    para(rt("Harold Jeffreys (1946, 'An Invariant Form for the Prior Probability in Estimation Problems', Proc. R. Soc. London A, Vol. 186) showed that the prior "), eq(r"\pi(\theta) \propto \sqrt{\det \mathcal{I}(\theta)}"), rt(" — the square root of the determinant of the Fisher information matrix — is invariant under any smooth reparameterization. This resolves the indifference paradox by grounding 'uninformativity' in the geometry of the statistical model.")),
    heading3("Evolution Timeline"),
    para(rt("Laplace (1812): flat priors → Jeffreys (1946): invariant prior based on Fisher information → Bernardo (1979): reference priors as an extension to multivariate problems → Gelman et al. (2006–): weakly informative priors as practical default for applied Bayes → Stan / PyMC community (2010s): half-normal, half-Cauchy priors for hierarchical scales.")),
    table(
        4,
        table_row(["Dimension", "Flat Prior", "Jeffreys Prior", "Weakly Informative"]),
        table_row(["Definition", "π(θ) ∝ 1", "π(θ) ∝ √I(θ)", "E.g. Normal(0,1) or Beta(2,2)"]),
        table_row(["Reparameterization invariance", "No", "Yes", "No"]),
        table_row(["Proper (integrable)?", "Often no", "Often no", "Yes"]),
        table_row(["Posterior propriety guarantee", "No", "Requires checking", "Typically yes"]),
        table_row(["Effect on posterior", "Dominated by likelihood", "Mild regularization at extremes", "Gentle pull to plausible region"]),
        table_row(["Best use case", "Large n, conjugate convenience", "Principled default, publications", "Practical applied Bayes"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Let "), eq(r"p(x|\theta)"), rt(" be a parametric likelihood. The "), rt("Fisher information", bold=True), rt(" is:")),
    equation_block(r"\mathcal{I}(\theta) = \mathbb{E}_{X|\theta}\!\left[\left(\frac{\partial \log p(X|\theta)}{\partial \theta}\right)^{\!2}\right] = -\mathbb{E}_{X|\theta}\!\left[\frac{\partial^2 \log p(X|\theta)}{\partial \theta^2}\right]"),
    para(rt("It measures the curvature of the log-likelihood — how sharply the likelihood peaks at the true "), eq(r"\theta"), rt(". The Cramér–Rao bound says any unbiased estimator "), eq(r"\hat\theta"), rt(" satisfies "), eq(r"\operatorname{Var}(\hat\theta) \geq 1/[n\,\mathcal{I}(\theta)]"), rt(".")),
    para(rt("The "), rt("Jeffreys prior", bold=True), rt(" for a scalar parameter is:")),
    equation_block(r"\pi_J(\theta) \propto \sqrt{\mathcal{I}(\theta)}"),
    para(rt("For a vector parameter "), eq(r"\theta \in \mathbb{R}^d"), rt(", it generalizes to the volume element of the Fisher–Rao metric:")),
    equation_block(r"\pi_J(\theta) \propto \sqrt{\det \mathcal{I}(\theta)}"),
    para(rt("where "), eq(r"\mathcal{I}(\theta)"), rt(" is the "), eq(r"d \times d"), rt(" Fisher information matrix.")),
    callout("🔑", rt("Core Invariance Property: ", bold=True), rt("For any smooth bijection "), eq(r"\phi = g(\theta)"), rt(", the Jeffreys prior in "), eq(r"\theta"), rt(" and the Jeffreys prior derived directly for "), eq(r"\phi"), rt(" give the same posterior inference. This is because "), eq(r"\sqrt{\mathcal{I}_\phi(\phi)}\,d\phi = \sqrt{\mathcal{I}_\theta(\theta)}\,d\theta"), rt(" — it is the Riemannian volume element of the statistical manifold.")),
    heading3("Prerequisites"),
    bullet(rt("Bayes' theorem: "), eq(r"p(\theta|x) \propto p(x|\theta)\pi(\theta)")),
    bullet(rt("Likelihood function and log-likelihood")),
    bullet(rt("Score function and Fisher information")),
    bullet(rt("Change of variables / Jacobian for probability densities")),
    bullet(rt("Beta and Gamma distributions")),
    divider(),

    # ── Section 4: Architecture / Deep-Dive ───────────────────────────────────
    heading2("🔬 Architecture & Internal Workings — PhD Deep Dive"),
    heading3("Step-by-step: Deriving the Jeffreys prior for Bernoulli(p)"),
    para(rt("Step 1. Write the log-likelihood for a single observation "), eq(r"X \in \{0,1\}")),
    equation_block(r"\log p(X|p) = X\log p + (1-X)\log(1-p)"),
    para(rt("Step 2. Compute the score (derivative w.r.t. "), eq(r"p"), rt("):")),
    equation_block(r"s(X;p) = \frac{\partial \log p(X|p)}{\partial p} = \frac{X}{p} - \frac{1-X}{1-p}"),
    para(rt("Step 3. Fisher information = variance of the score:")),
    equation_block(r"\mathcal{I}(p) = \mathbb{E}[s^2] = \frac{\mathbb{E}[X]}{p^2} + \frac{1-\mathbb{E}[X]}{(1-p)^2} = \frac{p}{p^2} + \frac{1-p}{(1-p)^2} = \frac{1}{p(1-p)}"),
    para(rt("Step 4. Jeffreys prior:")),
    equation_block(r"\pi_J(p) \propto \sqrt{\mathcal{I}(p)} = \frac{1}{\sqrt{p(1-p)}} = p^{-1/2}(1-p)^{-1/2}"),
    para(rt("Step 5. Recognize this as the Beta density: "), eq(r"\pi_J(p) = \text{Beta}(1/2,\, 1/2)"), rt(". The normalizing constant is "), eq(r"B(1/2,1/2) = \Gamma(1/2)^2/\Gamma(1) = \pi"), rt(", so the density is "), eq(r"\pi_J(p) = [p(1-p)]^{-1/2}/\pi"), rt(".")),
    heading3("Numerical Trace"),
    para(rt("Evaluate "), eq(r"\pi_J"), rt(" at specific points:")),
    bullet(rt("At "), eq(r"p = 0.5"), rt(": "), eq(r"\pi_J(0.5) = (0.5)^{-0.5}(0.5)^{-0.5}/\pi = 2/\pi \approx 0.6366")),
    bullet(rt("At "), eq(r"p = 0.1"), rt(": "), eq(r"\pi_J(0.1) = (0.1)^{-0.5}(0.9)^{-0.5}/\pi = 1/(\pi\sqrt{0.09}) \approx 1.061")),
    bullet(rt("At "), eq(r"p = 0.01"), rt(": "), eq(r"\pi_J(0.01) \approx 1/(\\pi\sqrt{0.0099}) \approx 3.20"), rt(" — high mass, high information near 0")),
    para(rt("Note the "), rt("U-shape", bold=True), rt(": the prior is highest near "), eq(r"p=0"), rt(" and "), eq(r"p=1"), rt(" (where a single observation is most informative) and lowest at "), eq(r"p=0.5"), rt(" (maximum uncertainty per observation).")),
    heading3("Why flat ≠ invariant — a concrete failure"),
    para(rt("Consider the reparameterization "), eq(r"\phi = \arcsin(\sqrt{p}) \in [0, \pi/2]"), rt(". This is the "), rt("variance-stabilizing transform", bold=True), rt(" for the Bernoulli. The Jacobian is "), eq(r"dp/d\phi = \sin(2\phi)"), rt(".")),
    para(rt("Under this map, the flat prior "), eq(r"\pi(p) = 1"), rt(" becomes:")),
    equation_block(r"\pi_\phi^\text{flat}(\phi) = \pi_p^\text{flat}\!\left(\sin^2\!\phi\right)\cdot\left|\frac{dp}{d\phi}\right| = 1 \cdot |\sin(2\phi)|"),
    para(rt("This is "), rt("not", italic=True), rt(" uniform in "), eq(r"\phi"), rt(": it peaks at "), eq(r"\phi = \pi/4"), rt(" (corresponding to "), eq(r"p=0.5"), rt(") and vanishes at the endpoints.")),
    para(rt("The Jeffreys prior "), eq(r"\pi_J(p) = [p(1-p)]^{-1/2}/\pi"), rt(" becomes:")),
    equation_block(r"\pi_\phi^J(\phi) = \frac{1}{\pi\sqrt{\sin^2\!\phi\,\cos^2\!\phi}}\cdot|\sin(2\phi)| = \frac{|\sin(2\phi)|}{\pi\,|\sin\phi\cos\phi|} = \frac{2|\sin\phi\cos\phi|}{\pi\,|\sin\phi\cos\phi|} = \frac{2}{\pi}"),
    para(rt("Exactly uniform! Value "), eq(r"2/\pi \approx 0.637"), rt(" everywhere on "), eq(r"[0, \pi/2]"), rt(". This numerical agreement was verified by scipy computation.")),
    heading3("Jeffreys prior for other common likelihoods"),
    bullet(rt("Normal("), eq(r"\mu"), rt(", "), eq(r"\sigma^2"), rt(") with "), eq(r"\sigma"), rt(" known: "), eq(r"\mathcal{I}(\mu) = 1/\sigma^2"), rt(" (constant) "), rt("⟹"), rt(" Jeffreys is improper flat "), eq(r"\pi(\mu) \propto 1")),
    bullet(rt("Normal(0, "), eq(r"\sigma^2"), rt(") with "), eq(r"\mu"), rt(" known: "), eq(r"\mathcal{I}(\sigma) = 2/\sigma^2"), rt(" "), rt("⟹"), rt(" Jeffreys is "), eq(r"\pi(\sigma) \propto 1/\sigma"), rt(" (log-uniform, also called the Jeffreys scale prior)")),
    bullet(rt("Poisson("), eq(r"\lambda"), rt("): "), eq(r"\mathcal{I}(\lambda) = 1/\lambda"), rt(" "), rt("⟹"), rt(" Jeffreys is "), eq(r"\pi(\lambda) \propto 1/\sqrt{\lambda}")),
    bullet(rt("Exponential("), eq(r"\lambda"), rt("): "), eq(r"\mathcal{I}(\lambda) = 1/\lambda^2"), rt(" "), rt("⟹"), rt(" Jeffreys is "), eq(r"\pi(\lambda) \propto 1/\lambda")),
    callout("⚠️", rt("Design Decision: ", bold=True), rt("Why not just use Jeffreys everywhere? (1) Many Jeffreys priors are improper — they don't integrate to 1. Always verify the posterior is proper before using them. (2) For multivariate problems, the Jeffreys prior often does not perform well (Stein's paradox: it is not admissible in ≥3 dimensions). Reference priors (Bernardo 1979) are preferred for multivariate settings.")),
    divider(),

    # ── Section 5: Math ────────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Proof of reparameterization invariance"),
    para(rt("Let "), eq(r"\phi = g(\theta)"), rt(" with "), eq(r"g"), rt(" smooth and invertible. The Fisher information transforms as:")),
    equation_block(r"\mathcal{I}_\phi(\phi) = \mathcal{I}_\theta\!\left(g^{-1}(\phi)\right)\cdot\left(\frac{d\theta}{d\phi}\right)^{\!2}"),
    para(rt("The Jeffreys prior for "), eq(r"\phi"), rt(" derived directly:")),
    equation_block(r"\pi_J^\phi(\phi) \propto \sqrt{\mathcal{I}_\phi(\phi)} = \sqrt{\mathcal{I}_\theta(\theta)}\cdot\left|\frac{d\theta}{d\phi}\right|"),
    para(rt("The change-of-variables formula for the induced distribution on "), eq(r"\phi"), rt(" from "), eq(r"\pi_J^\theta(\theta) \propto \sqrt{\mathcal{I}_\theta(\theta)}"), rt(" gives:")),
    equation_block(r"\pi^\phi(\phi) = \pi_J^\theta\!\left(g^{-1}(\phi)\right)\cdot\left|\frac{d\theta}{d\phi}\right| \propto \sqrt{\mathcal{I}_\theta(\theta)}\cdot\left|\frac{d\theta}{d\phi}\right| = \pi_J^\phi(\phi)"),
    para(rt("These are identical. No other prior has this property.")),
    heading3("Bayesian update with Jeffreys prior for Bernoulli"),
    para(rt("Prior: "), eq(r"\pi_J(p) = \text{Beta}(1/2, 1/2)"), rt(". Observe "), eq(r"k"), rt(" successes in "), eq(r"n"), rt(" Bernoulli trials. Likelihood: "), eq(r"p(k|p) \propto p^k(1-p)^{n-k}"), rt(". Posterior:")),
    equation_block(r"p(p|k,n) \propto p^{k+1/2-1}(1-p)^{n-k+1/2-1} = \text{Beta}\!\left(k + \tfrac{1}{2},\; n-k+\tfrac{1}{2}\right)"),
    para(rt("Example: 7 heads in 10 flips:")),
    bullet(rt("Posterior: "), eq(r"\text{Beta}(7.5,\; 3.5)")),
    bullet(rt("Posterior mean: "), eq(r"7.5/11 \approx 0.6818")),
    bullet(rt("Posterior MAP: "), eq(r"(7.5-1)/(11-2) = 6.5/9 \approx 0.7222")),
    bullet(rt("95% credible interval: approximately "), eq(r"[0.394, 0.907]")),
    heading3("Jeffreys prior as the Fisher–Rao volume element"),
    para(rt("The Fisher information defines a "), rt("Riemannian metric", bold=True), rt(" on the statistical manifold: the inner product of two score vectors. The Jeffreys prior is the induced "), rt("volume form", bold=True), rt(" of this Riemannian manifold:")),
    equation_block(r"\pi_J(\theta) = \sqrt{\det \mathcal{I}(\theta)} = \text{Riemannian volume element}"),
    para(rt("This gives the Jeffreys prior a geometric interpretation: it assigns equal volume (equal 'information measure') to regions that are equally distinguishable by the likelihood.")),
    callout("⚠️", rt("Common Misconception: ", bold=True), rt("'Jeffreys prior encodes zero prior information.' Not quite. It encodes information about the statistical structure of the model — specifically, it places more prior mass where data is more informative about the parameter. It is invariant, but not zero-information. True zero-information would require knowing nothing about the observation model either.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy / SciPy)"),
    code_block("python", """import numpy as np
from scipy import stats
from scipy.special import beta as beta_fn

# ── Fisher information for common likelihoods ──
def fisher_bernoulli(p):
    \"\"\"I(p) = 1 / [p*(1-p)] for Bernoulli(p).\"\"\"
    return 1.0 / (p * (1.0 - p))

def fisher_poisson(lam):
    \"\"\"I(lambda) = 1/lambda for Poisson(lambda).\"\"\"
    return 1.0 / lam

def fisher_normal_mu(sigma):
    \"\"\"I(mu) = 1/sigma^2 for Normal(mu, sigma^2) with sigma known.\"\"\"
    return 1.0 / sigma**2

def fisher_normal_sigma(sigma):
    \"\"\"I(sigma) = 2/sigma^2 for Normal(0, sigma^2) with mu known.\"\"\"
    return 2.0 / sigma**2

# ── Jeffreys prior objects ──
jeffreys_bernoulli = stats.beta(0.5, 0.5)       # Beta(1/2, 1/2)

# ── Bayesian update: Bernoulli with Jeffreys prior ──
def bernoulli_posterior(k, n, prior_a=0.5, prior_b=0.5):
    \"\"\"Beta posterior for Bernoulli(p) given k successes in n trials.
    Default prior_a=0.5, prior_b=0.5 is the Jeffreys prior.
    Compare with flat: prior_a=prior_b=1 (Laplace).
    \"\"\"
    return stats.beta(prior_a + k, prior_b + (n - k))

# 7 heads in 10 flips
post_jeffreys = bernoulli_posterior(7, 10, 0.5, 0.5)
post_flat     = bernoulli_posterior(7, 10, 1.0, 1.0)

print(f\"Jeffreys posterior: Beta(7.5, 3.5)\")
print(f\"  Mean : {post_jeffreys.mean():.4f}\")  # 0.6818
print(f\"  MAP  : {(7.5-1)/(11-2):.4f}\")        # 0.7222
print(f\"  95%  : [{post_jeffreys.ppf(0.025):.4f}, {post_jeffreys.ppf(0.975):.4f}]\")

print(f\"Flat posterior  : Beta(8, 4)\")
print(f\"  Mean : {post_flat.mean():.4f}\")        # 0.6667
print(f\"  MAP  : {(8-1)/(12-2):.4f}\")            # 0.7000

# ── Reparameterization invariance verification ──
# phi = arcsin(sqrt(p)) transforms Jeffreys Beta(1/2,1/2) to Uniform(2/pi)
p_vals   = np.linspace(0.01, 0.99, 10_000)
phi_vals = np.arcsin(np.sqrt(p_vals))
jac      = np.sin(2 * phi_vals)            # |dp/dphi|
pi_phi   = jeffreys_bernoulli.pdf(p_vals) / jac  # change of variables
print(f\"pi_phi: mean={pi_phi.mean():.5f}, std={pi_phi.std():.7f}\")
print(f\"2/pi = {2/np.pi:.5f}\")            # Should match mean
"""),

    heading3("6b — Production Usage (PyMC)"),
    code_block("python", """import pymc as pm
import numpy as np
import arviz as az

data = np.array([1,1,0,1,1,0,1,0,1,1])  # 7 heads, 3 tails

with pm.Model() as model_jeffreys:
    # Jeffreys prior for a Bernoulli rate
    p = pm.Beta("p", alpha=0.5, beta=0.5)

    obs = pm.Bernoulli("obs", p=p, observed=data)
    trace = pm.sample(2000, tune=1000, target_accept=0.9,
                      return_inferencedata=True, progressbar=False)

print(az.summary(trace, var_names=["p"]))

# ── Weakly informative alternative (Gelman recommendation) ──
with pm.Model() as model_weakly:
    # Beta(2,2): gentle pull toward center
    p = pm.Beta("p", alpha=2, beta=2)

    obs = pm.Bernoulli("obs", p=p, observed=data)
    trace2 = pm.sample(2000, tune=1000, return_inferencedata=True, progressbar=False)

# ── Scale parameters: use half-normal instead of flat ──
# BAD:  sigma ~ Uniform(0, 100)   # mildly informative, slow mixing
# GOOD: sigma ~ HalfNormal(0, 1)  # weakly informative, well-behaved
with pm.Model() as scale_model:
    sigma = pm.HalfNormal("sigma", sigma=1.0)  # weakly informative
    mu    = pm.Normal("mu", mu=0, sigma=10)    # weakly informative for location
    obs   = pm.Normal("obs", mu=mu, sigma=sigma, observed=data)
"""),
    callout("⚠️", rt("Gotcha: ", bold=True), rt("Using "), rt("pm.Uniform('p', 0, 1)", code=True), rt(" for a Bernoulli parameter applies a flat prior, NOT a Jeffreys prior. Always be explicit: "), rt("pm.Beta('p', alpha=0.5, beta=0.5)", code=True), rt(" for Jeffreys.")),
    divider(),

    # ── Section 7: Interview ───────────────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),

    toggle([rt("Q1 (Easy): What is a non-informative prior?", bold=True)], [
        para(rt("A non-informative prior (also called a vague or diffuse prior) is designed to let the likelihood dominate the posterior — expressing minimal prior beliefs. Common choices include flat priors ("), eq(r"\pi(\theta) \propto 1"), rt(") and the Jeffreys prior ("), eq(r"\pi(\theta) \propto \sqrt{\mathcal{I}(\theta)}"), rt("). The Jeffreys prior is preferred because it is invariant to reparameterization, whereas a flat prior is non-informative only in the specific parameterization where it is defined.")),
    ]),

    toggle([rt("Q2 (Easy): What is the Jeffreys prior for a Bernoulli parameter?", bold=True)], [
        para(rt("Beta(1/2, 1/2). Derived as: Fisher information "), eq(r"\mathcal{I}(p) = 1/[p(1-p)]"), rt(". Jeffreys prior "), eq(r"\pi_J(p) \propto \sqrt{1/[p(1-p)]} = p^{-1/2}(1-p)^{-1/2}"), rt(", which is the Beta(1/2, 1/2) density. It is a U-shape: high near 0 and 1, low at 0.5. The posterior with "), eq(r"k"), rt(" successes in "), eq(r"n"), rt(" trials is Beta("), eq(r"k + 1/2"), rt(", "), eq(r"n - k + 1/2"), rt(").")),
    ]),

    toggle([rt("Q3 (Medium): Why is a flat prior not truly uninformative?", bold=True)], [
        para(rt("A flat prior "), eq(r"\pi(p) = 1"), rt(" on "), eq(r"p \in [0,1]"), rt(" is informative in every other parameterization. Transform to "), eq(r"\phi = \arcsin(\sqrt{p})"), rt("; the induced prior is "), eq(r"\pi(\phi) \propto |\sin(2\phi)|"), rt(", which is peaked at "), eq(r"\phi=\pi/4"), rt(" (corresponding to "), eq(r"p=0.5"), rt("), not flat. The prior 'believes' "), eq(r"p=0.5"), rt(" is more likely when expressed in "), eq(r"\phi"), rt(" coordinates. Which parameterization is 'natural' is arbitrary — hence no parameterization-dependent prior can be called truly uninformative.")),
    ]),

    toggle([rt("Q4 (Medium): Prove reparameterization invariance of the Jeffreys prior.", bold=True)], [
        para(rt("Let "), eq(r"\phi = g(\theta)"), rt(". Fisher information transforms as "), eq(r"\mathcal{I}_\phi(\phi) = \mathcal{I}_\theta(\theta)(d\theta/d\phi)^2"), rt(". The induced prior on "), eq(r"\phi"), rt(" from "), eq(r"\pi_J^\theta \propto \sqrt{\mathcal{I}_\theta}"), rt(" is: "), eq(r"\pi_J^\theta(\theta)|d\theta/d\phi| \propto \sqrt{\mathcal{I}_\theta(\theta)}|d\theta/d\phi| = \sqrt{\mathcal{I}_\theta(\theta)(d\theta/d\phi)^2} = \sqrt{\mathcal{I}_\phi(\phi)}"), rt(", which equals "), eq(r"\pi_J^\phi(\phi)"), rt(". QED.")),
    ]),

    toggle([rt("Q5 (Hard): When should you NOT use the Jeffreys prior?", bold=True)], [
        para(rt("(1) "), rt("Multivariate settings:", bold=True), rt(" In ≥3 dimensions the Jeffreys prior is inadmissible (James–Stein phenomenon). Bernardo's reference priors are preferred. (2) "), rt("Improper posteriors:", bold=True), rt(" Jeffreys priors are often improper; the posterior may also be improper. For example, the flat prior on "), eq(r"\mu \in \mathbb{R}"), rt(" combined with a finite normal sample yields a proper posterior, but the same is not always true. Always verify. (3) "), rt("Hierarchical models:", bold=True), rt(" Jeffreys priors on hierarchical variance components cause degenerate posteriors (Gelman 2006). Use half-normal or half-Cauchy instead.")),
    ]),

    toggle([rt("Q6 (Hard): Explain the Jeffreys prior from an information geometry perspective.", bold=True)], [
        para(rt("Explain to a PhD Researcher: ", bold=True), rt("The set of all probability distributions "), eq(r"\{p(x|\theta)\}"), rt(" forms a statistical manifold. The Fisher information matrix "), eq(r"\mathcal{I}(\theta)"), rt(" defines a Riemannian metric (the Fisher–Rao metric) on this manifold. The Jeffreys prior is the induced volume form "), eq(r"d\text{vol}(\theta) = \sqrt{\det\mathcal{I}(\theta)}\,d\theta"), rt(". Since the volume form of a Riemannian manifold is invariant under diffeomorphisms by construction, so is the Jeffreys prior. It assigns equal measure to regions of equal 'statistical volume' — regions that are equally distinguishable by observations.")),
    ]),

    toggle([rt("Q7 (Medium): What is a weakly informative prior and when do you use it?", bold=True)], [
        para(rt("A weakly informative prior is a proper prior that encodes only broad, plausible constraints — not strong domain knowledge. Examples: "), eq(r"\text{Normal}(0, 1)"), rt(" for standardized regression coefficients (they are rarely > ±2–3 SDs), "), eq(r"\text{HalfNormal}(0, 1)"), rt(" for scale parameters (positive, not astronomically large). They prevent the sampler from exploring pathological regions of parameter space (e.g., "), eq(r"\sigma = 1000"), rt(" for data in [0,1]) while being 'weak' enough to be overridden by moderate amounts of data. Preferred over Jeffreys for hierarchical models and when improper posteriors are a risk.")),
    ]),

    toggle([rt("Q8 (Hard): How does the choice of prior affect posterior concentration as n→∞?", bold=True)], [
        para(rt("By the Bernstein–von Mises theorem: under regularity conditions, for any fixed "), rt("proper", italic=True), rt(" prior with "), eq(r"\pi(\theta_0) > 0"), rt(" at the true parameter "), eq(r"\theta_0"), rt(", the posterior converges to "), eq(r"\mathcal{N}(\theta_0, [n\mathcal{I}(\theta_0)]^{-1})"), rt(" as "), eq(r"n \to \infty"), rt(" — the same Gaussian regardless of which prior was used. So asymptotically, all reasonable priors agree. The prior matters most in small-") , eq(r"n"), rt(" regimes, for high-dimensional "), eq(r"\theta"), rt(", or when the likelihood is weak or multimodal.")),
    ]),
    divider(),

    # ── Section 8: Comparison ──────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(
        5,
        table_row(["Prior", "Bernoulli form", "Invariant", "Proper", "Best for"]),
        table_row(["Flat / Uniform", "Beta(1,1)", "No", "Yes (on [0,1])", "Convenience; large n"]),
        table_row(["Jeffreys", "Beta(½,½)", "Yes", "No (on ℝ)", "Principled default; publication"]),
        table_row(["Weakly informative", "Beta(2,2) or Normal", "No", "Yes", "Hierarchical models; stability"]),
        table_row(["Haldane / improper", "Beta(0,0)", "No", "No", "Extreme non-informativity (rarely used)"]),
        table_row(["Conjugate (subjective)", "Beta(α,β) arbitrary", "No", "Yes", "Prior knowledge encoded; analytic posterior"]),
        table_row(["Reference prior", "Like Jeffreys; derived differently", "Yes", "Sometimes", "Multivariate problems; nuisance params"]),
    ),
    callout("🎯", rt("Decision Guide: ", bold=True), rt("Use "), rt("Jeffreys", bold=True), rt(" when you need a principled, invariant default for a single parameter and are willing to verify posterior propriety. Use "), rt("weakly informative (Half-Normal, Normal(0,1))", bold=True), rt(" for hierarchical scale parameters and when practical inference stability matters more than invariance. Use "), rt("conjugate priors", bold=True), rt(" when you have genuine prior knowledge or need analytic posteriors for speed.")),
    divider(),

    # ── Section 9: Explainer ───────────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ─────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Bayes' Theorem and the posterior formula")),
    bullet(rt("Conjugate priors and the Beta-Bernoulli model")),
    bullet(rt("Fisher information and the Cramér-Rao bound")),
    bullet(rt("Change of variables for probability densities (Jacobian)")),
    heading3("What to Learn Next"),
    bullet(rt("Bernardo's reference priors (extension of Jeffreys to multivariate and nuisance parameters)")),
    bullet(rt("Posterior predictive checks (prior sensitivity analysis)")),
    bullet(rt("Markov Chain Monte Carlo (MCMC) for posterior inference with non-conjugate priors")),
    bullet(rt("Bayesian model comparison (Bayes factors and marginal likelihoods)")),
    bullet(rt("Variational inference as an alternative to MCMC")),
    heading3("Key Papers"),
    bullet(rt("Jeffreys, H. (1946). 'An Invariant Form for the Prior Probability in Estimation Problems.' Proc. R. Soc. London A, 186, 453–461. — Original derivation of the invariant prior.")),
    bullet(rt("Bernardo, J.M. (1979). 'Reference Posterior Distributions for Bayesian Inference.' J. R. Stat. Soc. B, 41(2), 113–147. — Extends Jeffreys to reference priors for nuisance parameters.")),
    bullet(rt("Gelman, A. (2006). 'Prior distributions for variance parameters in hierarchical models.' Bayesian Analysis, 1(3), 515–534. — Why Jeffreys fails for hierarchical scales; half-Cauchy recommendation.")),
    bullet(rt("Simpson, D., et al. (2017). 'Penalising Model Component Complexity.' Statistical Science. — Modern weakly informative priors from a principled complexity-penalization perspective.")),
    heading3("Best Resources"),
    bullet(rt("Gelman et al., Bayesian Data Analysis (3rd ed.), Chapter 2-3: prior distributions and Jeffreys priors.")),
    bullet(rt("Bernardo & Smith, Bayesian Theory (2000), Chapter 5: objective Bayesian methods.")),
    bullet(rt("Stan Prior Choice Wiki: https://github.com/stan-dev/stan/wiki/Prior-Choice-Recommendations")),
    bullet(rt("Michael Betancourt's case study 'Towards a Principled Bayesian Workflow' (betanalpha.github.io)")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Bayes' Theorem · Conjugate Priors · Fisher Information & Cramér-Rao Bound · MCMC Sampling · Variational Inference · Bernardo Reference Priors · Posterior Predictive Checks")),
]

if __name__ == "__main__":
    update_page(PAGE_ID, ICON, PROPERTIES, blocks)
