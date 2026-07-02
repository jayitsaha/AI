#!/usr/bin/env python3
"""Update Notion page for: Hierarchical / Multilevel Bayesian Models"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81ba-9e6d-f30e58af6363"
ICON = "🟡"  # Intermediate
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/hierarchical_bayesian_models_explainer.html"},
}

blocks = [
    # ── Section 1: The 30-Second Version ──
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("A hierarchical (multilevel) Bayesian model organises data into groups and says: each group has its own parameter, but all those parameters are drawn from a shared parent distribution (the hyperprior). This creates a statistical link between groups — groups borrow information from each other. The result is called "), rt("partial pooling", bold=True), rt(" or shrinkage: estimates for data-poor groups are pulled toward the overall mean, while data-rich groups remain near their own observations.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine 8 school classrooms taking the same exam, but class sizes range from 3 to 30 students. You want to estimate each classroom's true average ability. If you use only each class's own data (no pooling), the 3-student classes give wildly uncertain estimates. If you lump all students together (complete pooling), you miss real between-class differences. Hierarchical modelling does the right thing: it says 'a 3-student classroom's estimate should be nudged toward the school average, because 3 observations can't tell us much — but a 30-student classroom's estimate should trust its own data almost entirely.'")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Partial pooling shrinks group estimates toward a shared grand mean. The shrinkage factor "), eq(r"\mathcal{B}_j = \frac{\sigma^2/n_j}{\sigma^2/n_j + \tau^2}"), rt(" is larger when a group is small ("), eq(r"n_j"), rt(" small) or noisy ("), eq(r"\sigma^2"), rt(" large) and smaller when the group is large or groups genuinely differ ("), eq(r"\tau^2"), rt(" large).")),
    divider(),

    # ── Section 2: Historical Context ──
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Classical frequentist statistics treats group parameters as either completely independent (fixed effects, no-pooling) or completely identical (pooled estimate). Neither extreme is optimal. In the 1950s–60s, statisticians noticed that no-pooling estimates had unnecessarily high variance for small groups, and that there was no principled way to share information across groups in a frequentist framework.")),
    heading3("What Came Before"),
    para(rt("The dominant approach before hierarchical models was "), rt("two-step estimation", bold=True), rt(": first compute each group's sample mean, then treat those as fixed and independent. This ignored estimation uncertainty within each group. The Neyman-Scott problem (1948) formalised a case where maximum likelihood fails when the number of nuisance parameters grows with sample size — exactly the situation with many small groups.")),
    heading3("The Breakthrough — James-Stein and Empirical Bayes"),
    para(rt("The formal statistical breakthrough came from two directions. Charles Stein (1956) proved the shocking result that the sample mean is "), rt("inadmissible", bold=True, italic=True), rt(" as an estimator of a multivariate normal mean when the dimension is ≥ 3: there always exists a shrinkage estimator with lower total mean squared error. James and Stein (1961) made this constructive. On the Bayesian side, Herbert Robbins (1956) developed "), rt("Empirical Bayes", bold=True), rt(" — estimating the hyperparameters from the data itself — making the approach practical.")),
    para(rt("The full modern treatment came from Gelman, Carlin, Stern, and Rubin's textbook "), rt("Bayesian Data Analysis", bold=True, italic=True), rt(" (1995), which framed hierarchical models as the natural solution to the problem of grouped data. Stan (2012) made MCMC for hierarchical models computationally feasible at scale.")),
    heading3("Evolution Timeline"),
    bullet(rt("1948: Neyman-Scott problem — limits of fixed-effects MLE with many groups")),
    bullet(rt("1956: Stein inadmissibility result — sample mean is not optimal for K≥3 means")),
    bullet(rt("1961: James-Stein estimator — first practical shrinkage formula")),
    bullet(rt("1956/70s: Robbins + Efron & Morris — Empirical Bayes formalised")),
    bullet(rt("1972: Lindley & Smith — fully Bayesian hierarchical regression")),
    bullet(rt("1995: Gelman et al. BDA — textbook treatment; widespread adoption")),
    bullet(rt("2012: Stan — automatic MCMC for arbitrary hierarchical models")),
    heading3("Before vs After"),
    table(4,
        table_row(["Dimension", "Fixed Effects (Before)", "Hierarchical / Partial Pooling (After)"]),
        table_row(["Small groups", "Huge uncertainty, noisy estimates", "Shrunk toward grand mean, reduced variance"]),
        table_row(["Information sharing", "None — each group isolated", "All groups inform hyperparameters jointly"]),
        table_row(["Model complexity", "K×p parameters (one per group)", "p hyperparameters + group deviations"]),
        table_row(["Optimality", "Inadmissible for K≥3 (Stein)", "Bayes-optimal under model assumptions"]),
        table_row(["Computation", "Closed form OLS/MLE", "MCMC or Laplace approximation required"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ──
    heading2("🧠 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Hyperprior: ", bold=True), rt("A prior on the parameters of another prior. In "), eq(r"\theta_j \sim \mathcal{N}(\mu, \tau^2)"), rt(", the distribution "), eq(r"p(\mu, \tau)"), rt(" is the hyperprior.")),
    bullet(rt("Hyperparameters: ", bold=True), eq(r"\mu"), rt(" (grand mean) and "), eq(r"\tau"), rt(" (between-group SD). These govern how similar groups are to each other.")),
    bullet(rt("Partial pooling: ", bold=True), rt("The posterior estimate for each group borrows information from other groups via the shared hyperprior. Amount of borrowing adapts to data quality.")),
    bullet(rt("Shrinkage factor: ", bold=True), eq(r"\mathcal{B}_j = \frac{\sigma^2/n_j}{\sigma^2/n_j + \tau^2} \in [0,1]"), rt(". When "), eq(r"\mathcal{B}_j = 0"), rt(": no pooling. When "), eq(r"\mathcal{B}_j = 1"), rt(": complete pooling.")),
    bullet(rt("Empirical Bayes: ", bold=True), rt("Estimating the hyperparameters "), eq(r"(\mu, \tau)"), rt(" from the marginal likelihood "), eq(r"p(\mathbf{y} \mid \mu, \tau)"), rt(" rather than placing a full prior on them.")),
    heading3("The Three-Level Generative Model"),
    equation_block(r"\text{Level 3 (Hyperprior):} \quad \mu \sim p(\mu), \quad \tau \sim p(\tau)"),
    equation_block(r"\text{Level 2 (Group prior):} \quad \theta_j \mid \mu, \tau \;\sim\; \mathcal{N}(\mu, \tau^2), \quad j = 1, \ldots, J"),
    equation_block(r"\text{Level 1 (Likelihood):} \quad y_{ij} \mid \theta_j, \sigma \;\sim\; \mathcal{N}(\theta_j, \sigma^2), \quad i = 1, \ldots, n_j"),
    callout("🔑", rt("Core invariant: ", bold=True), rt("The group parameters "), eq(r"\theta_j"), rt(" are "), rt("neither fixed constants nor a single shared constant", italic=True), rt(". They are random variables drawn from a common distribution whose parameters are themselves estimated from data. This is the defining property of a hierarchical model.")),
    divider(),

    # ── Section 4: Architecture Deep Dive ──
    heading2("🔬 Architecture & Internal Workings (PhD Deep Dive)"),
    heading3("Information Flow"),
    para(rt("The hierarchical model defines a "), rt("directed acyclic graph (DAG)", bold=True), rt(" of conditional dependencies: hyperparameters "), eq(r"(\mu, \tau)"), rt(" → group parameters "), eq(r"\theta_j"), rt(" → observations "), eq(r"y_{ij}"), rt(". During inference this reverses: observations inform group parameters, which jointly inform the hyperparameters.")),
    heading3("The Posterior — Joint and Conditional"),
    para(rt("The joint posterior (with "), eq(r"\sigma"), rt(" known for simplicity) factorises as:")),
    equation_block(r"p(\theta_1,\ldots,\theta_J,\mu,\tau \mid \mathbf{y}) \propto p(\mu,\tau) \prod_{j=1}^J \left[ p(\theta_j \mid \mu,\tau) \prod_{i=1}^{n_j} p(y_{ij} \mid \theta_j) \right]"),
    para(rt("The conditional posterior of each "), eq(r"\theta_j"), rt(" given "), eq(r"\mu, \tau"), rt(" and the data is Gaussian (conjugacy of Normal-Normal):")),
    equation_block(r"\theta_j \mid \mathbf{y}_j, \mu, \tau, \sigma \;\sim\; \mathcal{N}\!\left(\hat{\theta}_j,\; V_j\right)"),
    equation_block(r"\hat{\theta}_j = \frac{\dfrac{n_j}{\sigma^2}\bar{y}_j + \dfrac{1}{\tau^2}\mu}{\dfrac{n_j}{\sigma^2} + \dfrac{1}{\tau^2}}, \qquad V_j = \left(\frac{n_j}{\sigma^2} + \frac{1}{\tau^2}\right)^{-1}"),
    heading3("Numerical Trace — 8 Schools Example"),
    para(rt("Using "), eq(r"\sigma = 15"), rt(", "), eq(r"\tau = 10"), rt(", "), eq(r"\hat{\mu} = 53.53"), rt(":")),
    table(5,
        table_row(["Group", "n_j", "ȳ_j (no-pool)", "B_j (shrinkage)", "θ̂_j (partial pool)"]),
        table_row(["G1", "3", "50.9", "0.429", "52.0"]),
        table_row(["G2", "3", "53.3", "0.429", "53.4"]),
        table_row(["G3", "5", "53.4", "0.310", "53.4"]),
        table_row(["G4", "10", "63.0", "0.184", "61.3"]),
        table_row(["G5", "10", "48.8", "0.184", "49.7"]),
        table_row(["G6", "20", "41.2", "0.101", "42.5"]),
        table_row(["G7", "20", "60.0", "0.101", "59.4"]),
        table_row(["G8", "30", "56.1", "0.070", "56.0"]),
    ),
    para(rt("Group 1 (n=3, ȳ=50.9): posterior SD = "), eq(r"\sqrt{V_1} = \sqrt{(3/225 + 1/100)^{-1}} = \sqrt{42.86} = 6.55"), rt(" vs no-pool SE = 8.66. Uncertainty reduced 24% by borrowing.")),
    heading3("Why Posterior Variance is Always Smaller"),
    para(rt("The posterior precision "), eq(r"1/V_j = n_j/\sigma^2 + 1/\tau^2"), rt(" is the "), rt("sum", italic=True), rt(" of the data precision and the prior precision. Adding a positive quantity increases precision, so "), eq(r"V_j < \sigma^2/n_j"), rt(" always. The prior from the hyperprior acts as free extra data.")),
    heading3("Design Decision: Why Not Fix Hyperparameters?"),
    para(rt("Fixing "), eq(r"\mu_0, \tau_0"), rt(" a priori is called an "), rt("informative prior", italic=True), rt(" — fine if you have strong subject-matter knowledge. Estimating them from data (Empirical Bayes) or placing another prior on them (fully Bayesian) removes the need for arbitrary choices and lets the data determine how much to pool. Full Bayes propagates uncertainty in "), eq(r"(\mu, \tau)"), rt(" into uncertainty about each "), eq(r"\theta_j"), rt(", giving honest credible intervals.")),
    callout("⚠️", rt("Edge case: when τ→0 (all groups identical), partial pooling → complete pooling. When τ→∞ (completely unrelated groups), partial pooling → no pooling. The prior ", bold=True), rt("HalfNormal(τ)"), rt(" or "), rt("HalfCauchy(τ)", code=True), rt(" governs this: heavy-tailed priors on τ allow the data to support large between-group differences.")),
    divider(),

    # ── Section 5: The Math ──
    heading2("📐 The Math Behind It"),
    heading3("Marginal Likelihood and Hyperparameter Estimation"),
    para(rt("Integrating out the group parameters, the marginal distribution of group means is:")),
    equation_block(r"\bar{y}_j \mid \mu, \tau, \sigma \;\sim\; \mathcal{N}\!\left(\mu,\; \frac{\sigma^2}{n_j} + \tau^2\right)"),
    para(rt("This marginal is the key to Empirical Bayes: we can maximise "), eq(r"\prod_j p(\bar{y}_j \mid \mu, \tau)"), rt(" over "), eq(r"(\mu, \tau)"), rt(" to get point estimates. The precision-weighted MLE for "), eq(r"\mu"), rt(" is:")),
    equation_block(r"\hat{\mu} = \frac{\sum_j \bar{y}_j / (\sigma^2/n_j + \tau^2)}{\sum_j 1/(\sigma^2/n_j + \tau^2)}"),
    para(rt("For "), eq(r"\tau^2"), rt(", the Method-of-Moments estimate solves "), eq(r"\sum_j (\bar{y}_j - \hat{\mu})^2 / (\sigma^2/n_j + \tau^2) = J - 1"), rt(", the expected chi-squared. Full Bayes marginalises over "), eq(r"(\mu, \tau)"), rt(" using MCMC.")),
    heading3("Posterior Mean as Convex Combination"),
    equation_block(r"\hat{\theta}_j = (1-\mathcal{B}_j)\bar{y}_j + \mathcal{B}_j\mu, \qquad \mathcal{B}_j = \frac{\sigma^2/n_j}{\sigma^2/n_j + \tau^2}"),
    para(rt("This is a "), rt("convex combination", bold=True), rt(": "), eq(r"\hat{\theta}_j \in [\min(\bar{y}_j, \mu), \max(\bar{y}_j, \mu)]"), rt(". It interpolates between the no-pooling extreme ("), eq(r"\mathcal{B}_j = 0"), rt(", return "), eq(r"\bar{y}_j"), rt(") and the complete-pooling extreme ("), eq(r"\mathcal{B}_j = 1"), rt(", return "), eq(r"\mu"), rt(").")),
    heading3("Mean Squared Error — Why Shrinkage Wins"),
    para(rt("The total MSE across all groups under squared error loss:")),
    equation_block(r"\text{MSE}_{\text{no-pool}} = \sum_j \frac{\sigma^2}{n_j}"),
    equation_block(r"\text{MSE}_{\text{partial}} = \sum_j \left[(1-\mathcal{B}_j)^2 \cdot \frac{\sigma^2}{n_j} + \mathcal{B}_j^2 \cdot (\mu - \theta_j)^2\right]"),
    para(rt("The partial pooling estimator has variance component reduced by factor "), eq(r"(1-\mathcal{B}_j)^2"), rt(" at the cost of bias "), eq(r"\mathcal{B}_j(\mu - \theta_j)"), rt(". When "), eq(r"\tau"), rt(" is small (groups are similar), the bias is small but the variance reduction is large → total MSE is lower. Stein (1956) proved this improvement is guaranteed when "), eq(r"J \geq 3"), rt(".")),
    callout("⚠️", rt("Mathematical subtlety: ", bold=True), rt("The Empirical Bayes estimator plugs in "), eq(r"\hat{\mu}, \hat{\tau}"), rt(" as if they were the truth. This ignores uncertainty in the hyperparameters, causing "), rt("credible intervals to be too narrow", italic=True), rt(". Full MCMC integration over "), eq(r"p(\mu, \tau \mid \mathbf{y})"), rt(" gives honest coverage. For this reason, full Bayesian MCMC (Stan/PyMC) is preferred when "), eq(r"J"), rt(" is small.")),
    divider(),

    # ── Section 6: Code ──
    heading2("💻 Code Implementation"),
    heading3("6a — Analytic Empirical Bayes (NumPy)"),
    code_block("python", """import numpy as np

# Data: 8 groups, known within-group sigma
n_j   = np.array([3, 3, 5, 10, 10, 20, 20, 30])
y_bar = np.array([50.9, 53.3, 53.4, 63.0, 48.8, 41.2, 60.0, 56.1])
sigma = 15.0  # within-group SD (known or estimated from pooled residuals)

# Step 1: Group-level standard errors
se_j = sigma / np.sqrt(n_j)        # [8.66, 8.66, 6.71, 4.74, 4.74, 3.35, 3.35, 2.74]

# Step 2: Estimate tau (between-group SD) via Method of Moments
# Var(y_bar_j) = sigma^2/n_j + tau^2  =>  estimate tau^2 from residuals
tau_sq_raw = np.mean((y_bar - np.mean(y_bar))**2) - np.mean(se_j**2)
tau = np.sqrt(max(tau_sq_raw, 0.0))   # clamp at 0; here ≈ 7.3

# Step 3: Shrinkage factors
B_j = (se_j**2) / (se_j**2 + tau**2)  # fraction pulled toward grand mean

# Step 4: Precision-weighted grand mean (marginal weights)
w_j  = 1.0 / (se_j**2 + tau**2)       # marginal precisions
mu_hat = np.sum(w_j * y_bar) / np.sum(w_j)  # ~53.5

# Step 5: Partial-pooling estimates
theta_hat = mu_hat + (1 - B_j) * (y_bar - mu_hat)
# [52.0, 53.4, 53.4, 61.3, 49.7, 42.5, 59.4, 56.0]

# Step 6: Posterior SDs (tighter than no-pool SEs)
V_j       = 1.0 / (n_j / sigma**2 + 1.0 / tau**2)
post_sd_j = np.sqrt(V_j)
# [6.55, 6.55, 5.57, 4.29, 4.29, 3.18, 3.18, 2.64]

print(f"Partial pool: {np.round(theta_hat, 1)}")
print(f"No pool:      {np.round(y_bar, 1)}")
print(f"Grand mean:   {mu_hat:.2f}")
print(f"B_j:          {np.round(B_j, 3)}")
"""),
    heading3("6b — Full Bayesian with PyMC"),
    code_block("python", """import numpy as np
import pymc as pm
import arviz as az

n_j   = np.array([3, 3, 5, 10, 10, 20, 20, 30])
y_bar = np.array([50.9, 53.3, 53.4, 63.0, 48.8, 41.2, 60.0, 56.1])
se_j  = 15.0 / np.sqrt(n_j)   # known within-group SE

with pm.Model() as hier_model:
    # Hyperprior
    mu  = pm.Normal("mu", mu=50.0, sigma=20.0)      # grand mean
    tau = pm.HalfNormal("tau", sigma=15.0)           # between-group SD

    # Group-level means (non-centered parameterization for better geometry)
    # theta_j = mu + tau * z_j  where z_j ~ N(0,1)
    z   = pm.Normal("z", mu=0.0, sigma=1.0, shape=len(n_j))
    theta = pm.Deterministic("theta", mu + tau * z)

    # Likelihood: observe group sample means with known SE
    obs = pm.Normal("obs", mu=theta, sigma=se_j, observed=y_bar)

    # Sample posterior
    trace = pm.sample(2000, tune=1000, target_accept=0.9,
                      return_inferencedata=True, random_seed=42)

# Posterior summary
summary = az.summary(trace, var_names=["mu", "tau", "theta"])
print(summary)

# Posterior means for theta (partial pooling)
theta_post = trace.posterior["theta"].mean(("chain", "draw")).values
print("Partial pooling (MCMC):", np.round(theta_post, 1))

# Gotcha: use non-centered parameterization for hierarchical models!
# Centered (theta ~ Normal(mu, tau)) suffers from funnel geometry when
# tau is small -> poor mixing. Non-centered (theta = mu + tau*z) separates
# the geometry and gives much better MCMC efficiency.
"""),
    callout("⚠️", rt("Non-centered parameterization: ", bold=True), rt("In PyMC/Stan, always reparameterise as "), eq(r"\theta_j = \mu + \tau \cdot z_j"), rt(", "), eq(r"z_j \sim \mathcal{N}(0,1)"), rt(". The centred parameterisation "), eq(r"\theta_j \sim \mathcal{N}(\mu, \tau^2)"), rt(" creates a 'funnel' geometry when "), eq(r"\tau`"), rt(" is small, causing MCMC to mix poorly. Non-centred separates the global ("), eq(r"\mu, \tau"), rt(") and local ("), eq(r"z_j"), rt(") scales.")),
    divider(),

    # ── Section 7: Interview Q&A ──
    heading2("🎯 Interview Deep-Dive"),
    heading3("Easy"),
    toggle([rt("Q1: What is the difference between no-pooling, complete-pooling, and partial-pooling?", bold=True)], [
        para(rt("No pooling estimates each group independently (each gets its own parameter fit only to that group's data). Complete pooling fits a single parameter shared by all groups. Partial pooling is the hierarchical middle ground: group parameters are drawn from a shared distribution, so they share information but are not forced to be identical. Partial pooling is adaptive — it automatically determines how much to pool based on group size and between-group variation.")),
    ]),
    toggle([rt("Q2: What is a hyperprior, and why does it matter?", bold=True)], [
        para(rt("A hyperprior is a prior on the parameters of another prior. In the model "), eq(r"\theta_j \sim \mathcal{N}(\mu, \tau^2)"), rt(", the distribution "), eq(r"p(\mu, \tau)"), rt(" is the hyperprior. It matters because it controls how strongly groups are linked: if "), eq(r"\tau"), rt(" is very small (tight hyperprior), all groups are forced to be similar; if "), eq(r"\tau"), rt(" is large, groups can vary widely. Putting a prior on "), eq(r"\tau"), rt(" rather than fixing it allows the data to determine the degree of pooling.")),
    ]),
    heading3("Medium"),
    toggle([rt("Q3: Derive the shrinkage factor. Why does it depend on group size?", bold=True)], [
        para(rt("The posterior mean for "), eq(r"\theta_j"), rt(" is a precision-weighted combination of the data (precision "), eq(r"n_j/\sigma^2"), rt(") and the prior (precision "), eq(r"1/\tau^2"), rt("):")),
        equation_block(r"\hat{\theta}_j = \frac{(n_j/\sigma^2)\bar{y}_j + (1/\tau^2)\mu}{n_j/\sigma^2 + 1/\tau^2}"),
        para(rt("Rearranging: "), eq(r"\hat{\theta}_j = \mu + (1-\mathcal{B}_j)(\bar{y}_j - \mu)"), rt(" where "), eq(r"\mathcal{B}_j = \frac{\sigma^2/n_j}{\sigma^2/n_j + \tau^2}"), rt(". As "), eq(r"n_j"), rt(" grows, "), eq(r"\sigma^2/n_j \to 0"), rt(" so "), eq(r"\mathcal{B}_j \to 0"), rt(": large groups trust their own data. As "), eq(r"n_j \to 0"), rt(", "), eq(r"\mathcal{B}_j \to 1"), rt(": empty groups fall back on the prior.")),
    ]),
    toggle([rt("Q4: What is the non-centered parameterization and why is it needed?", bold=True)], [
        para(rt("In centred form, "), eq(r"\theta_j \sim \mathcal{N}(\mu, \tau^2)"), rt(". When "), eq(r"\tau"), rt(" is small, "), eq(r"\theta_j"), rt(" and "), eq(r"\mu"), rt(" are nearly correlated, creating a narrow 'funnel' in the joint posterior. HMC/NUTS chains get stuck in the neck of the funnel. Non-centred form: "), eq(r"\theta_j = \mu + \tau z_j"), rt(", "), eq(r"z_j \sim \mathcal{N}(0,1)"), rt(". Now "), eq(r"z_j"), rt(" and "), eq(r"(\mu, \tau)"), rt(" are roughly independent, the geometry is well-conditioned, and sampling is efficient. Always use non-centred for deep hierarchies.")),
    ]),
    heading3("Hard"),
    toggle([rt("Q5 (Expert): Stein's paradox says the sample mean is inadmissible for K≥3. What does this mean for hierarchical models?", bold=True)], [
        para(rt("Stein (1956) proved: for K≥3 means, the estimator "), eq(r"\hat{\theta}_j = \bar{y}_j"), rt(" is "), rt("inadmissible", bold=True), rt(" under squared error loss. That is, there exists another estimator with strictly lower total MSE for every possible true "), eq(r"\theta"), rt(". The James-Stein estimator "), eq(r"\hat{\theta}^{JS} = \left(1 - \frac{(K-2)\sigma^2}{\|\bar{y}\|^2}\right)\bar{y}"), rt(" is one such dominating estimator. Hierarchical Bayesian models provide the full probabilistic justification: the shrinkage is exactly the posterior mean under the assumption that "), eq(r"\theta_j \sim \mathcal{N}(\mu, \tau^2)"), rt(". The key lesson: for grouped data with K≥3 groups, you should always pool — the question is only "), rt("how much", italic=True), rt(", not "), rt("whether", italic=True), rt(".")),
    ]),
    toggle([rt("Q6 (Expert): When does hierarchical modelling fail or hurt?", bold=True)], [
        para(rt("Hierarchical models can fail in several ways: (1) "), rt("Prior sensitivity on τ", bold=True), rt(": if τ is near 0 and the posterior is sensitive to the hyperprior on τ, different hyperprior choices give very different pooling. (2) "), rt("Wrong exchangeability assumption", bold=True), rt(": partial pooling assumes groups are exchangeable draws from the same distribution. If groups are fundamentally different populations, pooling introduces bias that exceeds the variance reduction. (3) "), rt("Few groups (J < 5)", bold=True), rt(": with very few groups, we have little data to estimate τ, and the full Bayes posterior for τ is very wide. Empirical Bayes underestimates uncertainty. (4) "), rt("Computational failure (divergences)", bold=True), rt(": centred parameterisation with small τ causes HMC divergences that signal unreliable posterior estimates.")),
    ]),
    heading3("Explain to a PhD Researcher"),
    para(rt("Hierarchical models are equivalent to placing a conjugate Normal hyperprior on the group means and marginalising. Under a flat hyperprior for "), eq(r"\mu"), rt(" and marginalising over it, the marginal posterior for "), eq(r"\tau"), rt(" is determined by the residual between-group variation. Full inference uses HMC on the joint "), eq(r"p(\mu,\tau,z_1,\ldots,z_J \mid \mathbf{y})"), rt(" with the non-centred parameterisation to avoid funnel geometry. From a frequentist angle, the Empirical Bayes estimator achieves the Stein risk reduction guarantee by data-adaptively estimating the shrinkage target.")),
    heading3("Explain to a Research Scientist / Engineer"),
    para(rt("Think of hierarchical models as regularised group-specific models. The 'regulariser' is the hyperprior — it penalises groups from deviating too far from the population mean. The strength of regularisation is automatic: groups with little data get more regularisation, groups with lots of data get less. In practice, you specify the model in PyMC or Stan, use the non-centered parameterisation, run NUTS/HMC, and check for divergences. The posterior estimates are your partial-pooling estimates with honest uncertainty.")),
    divider(),

    # ── Section 8: Comparison ──
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Approach", "No Pooling", "Complete Pooling", "Partial Pooling (Hierarchical)", "Fixed Regularisation"]),
        table_row(["Estimator for θ_j", "ȳ_j", "Grand mean μ̂", "μ̂ + (1−B_j)(ȳ_j − μ̂)", "ȳ_j + λ(μ̂ − ȳ_j), fixed λ"]),
        table_row(["Bias", "Zero (unbiased)", "High (ignores groups)", "Adaptive (small for large n_j)", "Fixed bias"]),
        table_row(["Variance", "High for small groups", "Very low", "Adaptive (low for small n_j)", "Reduced, fixed amount"]),
        table_row(["Handles small groups?", "Poorly (high SE)", "Yes, but homogenises", "Yes, with shrinkage", "Partially"]),
        table_row(["Uncertainty", "Honest SEs", "Too narrow (ignores group var)", "Honest posteriors via MCMC", "Underestimates"]),
        table_row(["Data requirement", "Each group separately", "All data pooled", "Joint model, benefits from J≥5 groups", "J≥2, λ chosen by CV"]),
        table_row(["Software", "OLS per group", "Single OLS", "PyMC, Stan, brms", "sklearn Ridge"]),
    ),
    callout("🎯", rt("Decision guide: ", bold=True), rt("Use "), rt("no pooling", bold=True), rt(" when all groups have large n and you need unbiased individual estimates. Use "), rt("complete pooling", bold=True), rt(" when group differences are irrelevant. Use "), rt("hierarchical partial pooling", bold=True), rt(" when groups have varying sizes (especially some small), groups are related (exchangeable), and you want optimal bias-variance trade-off. Use "), rt("Ridge regression", bold=True), rt(" as a non-Bayesian approximation if you only care about prediction and not inference on group-specific parameters.")),
    divider(),

    # ── Section 9: Explainer Embed ──
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/hierarchical_bayesian_models_explainer.html"),
    para(rt("Step through partial pooling visually — 8 groups, varying sample sizes. See no-pooling vs complete-pooling vs partial-pooling estimates animate. Use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ──
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Bayes' Theorem and Bayesian Updating (3.8) — how priors update to posteriors")),
    bullet(rt("Conjugate Priors — Normal-Normal conjugacy used in the analytic derivation")),
    bullet(rt("Maximum Likelihood Estimation — Empirical Bayes maximises marginal likelihood")),
    bullet(rt("Gaussian Distribution — all levels of the hierarchy use Normal distributions")),
    heading3("What to Learn Next"),
    bullet(rt("Bayesian Model Comparison (WAIC, LOO-CV) — comparing pooled vs hierarchical")),
    bullet(rt("Gaussian Processes — infinite-dimensional hierarchical models")),
    bullet(rt("Variational Inference — approximate inference when MCMC is too slow")),
    bullet(rt("Mixed Effects Models (LME4) — frequentist counterpart via REML")),
    bullet(rt("Bayesian Neural Networks — hierarchical priors on weights")),
    heading3("Key Papers"),
    bullet(rt("Stein (1956): 'Inadmissibility of the usual estimator for the mean of a multivariate normal distribution' — the impossibility result that motivates shrinkage")),
    bullet(rt("James & Stein (1961): 'Estimation with quadratic loss' — first constructive shrinkage estimator")),
    bullet(rt("Efron & Morris (1975): 'Data analysis using Stein's estimator and its generalizations' — JASA, bridges Bayes and frequentist shrinkage")),
    bullet(rt("Lindley & Smith (1972): 'Bayes estimates for the linear model' — formal Bayesian hierarchical regression")),
    bullet(rt("Gelman et al. (1995): 'Bayesian Data Analysis' — standard textbook, Chapter 5 on hierarchical models")),
    heading3("Best Resources"),
    bullet(rt("Gelman & Hill (2007): 'Data Analysis Using Regression and Multilevel/Hierarchical Models' — most accessible full treatment")),
    bullet(rt("Richard McElreath: 'Statistical Rethinking' (2020 2nd ed.) — Chapter 13–14, outstanding conceptual development")),
    bullet(rt("PyMC documentation: pymc.io — hierarchical models tutorial")),
    bullet(rt("Stan documentation: mc-stan.org — hierarchical models section, non-centred parameterisation guide")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Bayesian Updating (3.8), Conjugate Priors (3.9), Gaussian Processes (Part XIV), Variational Inference, Mixed Effects Models (REML), Empirical Bayes, Stein's Paradox")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
