#!/usr/bin/env python3
"""Update Notion page for: Bayesian Model Comparison — Bayes Factors, BIC"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8172-bf3f-d26ee3e12e40"
ICON = "🟠"  # Advanced depth
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/bayesian_model_comparison_explainer.html"

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: The 30-Second Version ─────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Bayesian model comparison answers the question: given two competing statistical models, which one is better supported by the observed data? Instead of comparing models only at their best-fit parameters (as classical hypothesis testing does), Bayesian comparison integrates the likelihood over all parameter values—giving each model credit for predictions it makes under any plausible parameter setting.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine two weather forecasters. Forecaster A uses only temperature to predict rain; Forecaster B uses temperature, humidity, wind, and cloud cover. If Forecaster A's simpler model is nearly as accurate, we should trust A more—Forecaster B may have just gotten lucky by tuning four dials. Bayesian model comparison does exactly this accounting: it rewards a model for its average predictive success over all plausible parameter values, automatically discounting complexity.")),
    heading3("One-Sentence Summary"),
    para(rt("The Bayes factor is the ratio of models' marginal likelihoods, and it enforces Occam's razor automatically by penalising models that spread probability mass over large, poorly-supported parameter spaces.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("BF₁₂ = p(D|M₁)/p(D|M₂). The marginal likelihood integrates the likelihood over the prior — complex models lose because they spread probability thinner. BIC ≈ −2 ln L̂ + k ln n is the cheap large-n approximation.")),
    divider(),

    # ── Section 2: Historical Context ────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Classical frequentist hypothesis testing (p-values, likelihood-ratio tests) compares models via their fit at the maximum-likelihood estimate, with a penalty only for degrees of freedom (AIC) or with asymptotic chi-squared calibration. These approaches do not encode prior knowledge, cannot express evidence in favour of the null, and give no principled way to compare non-nested models.")),
    heading3("What Came Before"),
    para(rt("The Neyman–Pearson framework (1933) formalised hypothesis testing but framed it as a decision problem with no posterior model probability. AIC (Akaike 1973) added the penalty "), eq(r"2k"), rt(" to balance fit and parsimony, but was motivated by prediction rather than hypothesis testing.")),
    heading3("The Breakthrough"),
    para(rt("Harold Jeffreys (1935, 1961) laid the foundation of Bayesian hypothesis testing in his "), rt("Theory of Probability", italic=True), rt(". He defined the Bayes factor and constructed the Jeffreys evidence scale. Schwarz (1978) derived BIC as a large-sample approximation to minus twice the log marginal likelihood from a Laplace expansion. Kass & Raftery (1995, JASA) provided a unified treatment and the calibrated evidence scale now universally cited.")),
    heading3("Evolution Timeline"),
    para(rt("Jeffreys (1935) → Bayesian hypothesis test, Bayes factor concept; Schwarz (1978) → BIC derivation; Kass–Raftery (1995) → calibration scale & review; Raftery (1999) → BIC for sociological models; Vehtari–Gelman (2012+) → WAIC, PSIS-LOO as Bayes factor alternatives.")),
    heading3("Key Papers"),
    bullet(rt("Jeffreys, H. (1961). "), rt("Theory of Probability", italic=True), rt(" (3rd ed.). Oxford. — Foundational Bayesian testing framework.")),
    bullet(rt("Schwarz, G. (1978). Estimating the dimension of a model. "), rt("Annals of Statistics, 6(2)", italic=True), rt(", 461–464. — BIC derivation from Laplace approximation.")),
    bullet(rt("Kass, R.E., & Raftery, A.E. (1995). Bayes factors. "), rt("JASA, 90(430)", italic=True), rt(", 773–795. — Comprehensive review with calibration scale.")),
    bullet(rt("Vehtari, A., Gelman, A., & Gabry, J. (2017). Practical Bayesian model evaluation using LOO-CV and WAIC. "), rt("Statistics and Computing, 27", italic=True), rt(", 1413–1432.")),
    heading3("Before vs After"),
    table(4,
        table_row(["Dimension", "Frequentist (LRT / AIC)", "Bayesian (BF / BIC)"]),
        table_row(["Compares at", "Best-fit parameters", "Average over prior"]),
        table_row(["Complexity penalty", "Fixed: 2k (AIC) or χ² df", "Automatic Occam factor"]),
        table_row(["Evidence for null", "Only reject / fail to reject", "BF can support null"]),
        table_row(["Prior required", "No", "Yes (BIC uses implicit flat prior)"]),
        table_row(["Non-nested models", "Problematic", "Natural"])),
    divider(),

    # ── Section 3: Core Concepts ──────────────────────────────────────────────
    heading2("🔑 Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Let "), eq(r"\mathcal{M} = \{M_1, \ldots, M_K\}"), rt(" be a discrete set of models. Each model "), eq(r"M_i"), rt(" specifies (a) a likelihood "), eq(r"p(D \mid \theta_i, M_i)"), rt(" and (b) a prior "), eq(r"p(\theta_i \mid M_i)"), rt(" over its parameter space "), eq(r"\Theta_i"), rt(".")),
    heading3("Model Evidence (Marginal Likelihood)"),
    para(rt("The marginal likelihood of model "), eq(r"M_i"), rt(" is:")),
    equation_block(r"p(D \mid M_i) = \int_{\Theta_i} p(D \mid \theta_i, M_i)\, p(\theta_i \mid M_i)\, d\theta_i"),
    para(rt("This is the probability of the data averaged over all parameter values weighted by the prior—the key quantity for model comparison.")),
    heading3("Bayes Factor"),
    equation_block(r"\mathrm{BF}_{12} = \frac{p(D \mid M_1)}{p(D \mid M_2)}"),
    para(rt("Combined with prior model odds, it gives the posterior odds:")),
    equation_block(r"\frac{P(M_1 \mid D)}{P(M_2 \mid D)} = \mathrm{BF}_{12} \cdot \frac{P(M_1)}{P(M_2)}"),
    heading3("BIC"),
    equation_block(r"\mathrm{BIC} \triangleq -2\ln\hat{L} + k\ln n"),
    para(rt("where "), eq(r"\hat{L} = p(D \mid \hat{\theta}, M)"), rt(" is the maximised likelihood, "), eq(r"k"), rt(" the number of free parameters, and "), eq(r"n"), rt(" sample size. Lower BIC is preferred.")),
    heading3("Kass–Raftery Evidence Scale"),
    table(3,
        table_row(["2 ln BF₁₂", "BF₁₂", "Evidence for M1"]),
        table_row(["0 – 2",    "1 – 3.2",  "Barely worth mentioning"]),
        table_row(["2 – 6",    "3.2 – 20", "Positive"]),
        table_row(["6 – 10",   "20 – 150", "Strong"]),
        table_row(["> 10",     "> 150",    "Very strong"])),
    callout("🔑", rt("Core Invariant: ", bold=True), rt("The Bayes factor is the unique Bayesian measure of evidence that satisfies transitivity: BF₁₃ = BF₁₂ · BF₂₃. No re-calibration is needed when adding new models.")),
    heading3("Prerequisites"),
    bullet(rt("Conditional probability and Bayes' theorem")),
    bullet(rt("Maximum likelihood estimation (MLE)")),
    bullet(rt("Conjugate priors and Gaussian distributions")),
    bullet(rt("Basic integration and multivariate calculus")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ───────────────────────────
    heading2("🏗️ Architecture & Internal Workings — PhD-Level Deep Dive"),
    heading3("The Occam Factor — Why Integration Penalises Complexity"),
    para(rt("Write the log marginal likelihood as:")),
    equation_block(r"\ln p(D \mid M) = \underbrace{\ln p(D \mid \hat{\theta}, M)}_{\text{goodness of fit}} + \underbrace{\ln \frac{p(\hat{\theta} \mid M) \cdot (2\pi)^{k/2}}{|\mathcal{H}|^{1/2}}}_{\text{Occam factor (negative)}}"),
    para(rt("The Occam factor (derived from the Laplace approximation) is always negative. It measures how much of the prior probability volume the data actually constrain: if the posterior collapses tightly around "), eq(r"\hat{\theta}"), rt(", the model is 'just right'; if the posterior barely moves from the prior, the model is too complex.")),
    heading3("Laplace Approximation in Detail"),
    para(rt("Expand "), eq(r"\ln p(D \mid \theta, M)"), rt(" to second order around "), eq(r"\hat{\theta}"), rt(":")),
    equation_block(r"\ln p(D \mid \theta, M) \approx \ln\hat{L} - \frac{1}{2}(\theta - \hat{\theta})^\top \mathcal{H} (\theta - \hat{\theta})"),
    para(rt("where "), eq(r"\mathcal{H}_{ij} = -\frac{\partial^2 \ln p(D \mid \theta)}{\partial \theta_i \partial \theta_j}\bigg|_{\hat{\theta}}"), rt(" is the observed Fisher information matrix. Integrating a Gaussian over "), eq(r"\mathbb{R}^k"), rt(" gives:")),
    equation_block(r"\ln p(D \mid M) \approx \ln\hat{L} + \frac{k}{2}\ln(2\pi) - \frac{1}{2}\ln\det\mathcal{H}"),
    para(rt("For "), eq(r"n"), rt(" iid observations, "), eq(r"\det\mathcal{H} \approx n^k \det\mathcal{I}(\hat{\theta})"), rt(" where "), eq(r"\mathcal{I}"), rt(" is the Fisher information per observation. Dropping "), eq(r"O(1)"), rt(" terms relative to the dominant "), eq(r"(k/2)\ln n"), rt(" term yields BIC.")),
    heading3("Numerical Trace — n=20, Linear vs Quadratic"),
    para(rt("True model: "), eq(r"y_i = 1 + 2x_i + \varepsilon_i"), rt(", "), eq(r"\varepsilon_i \sim \mathcal{N}(0, 0.25)")),
    code_block("python", """import numpy as np
np.random.seed(42); n=20; x=np.linspace(0,1,n)
y = 1 + 2*x + 0.5*np.random.randn(n)

# M1: linear (k=2), M2: quadratic (k=3)
X1 = np.column_stack([np.ones(n), x])
X2 = np.column_stack([np.ones(n), x, x**2])
b1 = np.linalg.lstsq(X1,y,rcond=None)[0]
b2 = np.linalg.lstsq(X2,y,rcond=None)[0]
r1, r2 = y-X1@b1, y-X2@b2
s1, s2 = r1@r1/n, r2@r2/n

logL1 = -n/2*np.log(2*np.pi*s1) - n/2   # -8.464
logL2 = -n/2*np.log(2*np.pi*s2) - n/2   # -8.409
bic1  = -2*logL1 + 2*np.log(n)          # 22.92
bic2  = -2*logL2 + 3*np.log(n)          # 25.81

lnBF  = (bic2 - bic1) / 2               # 1.443
BF    = np.exp(lnBF)                    # 4.23  positive evidence for M1
print(f"BF_12={BF:.2f}, ΔBIC={bic2-bic1:.2f}")"""),
    heading3("Design Decisions — Why not just use the LRT?"),
    callout("⚙️", rt("Design Decision: ", bold=True), rt("The likelihood-ratio test (LRT) compares -2(logL_restricted - logL_full) to a chi-squared distribution. It only works for nested models, has no natural calibration for non-nested comparison, and cannot produce evidence in favour of the null. The Bayes factor solves all three limitations at the cost of requiring a prior specification.")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("Lindley's paradox: As n→∞ with a fixed significance level, BF can support H₀ even when the p-value rejects it. The paradox dissolves when both frameworks use consistent sample-size asymptotics.")),
    bullet(rt("Improper priors: BF is undefined when either model has an improper prior (normalising constant is infinite). Use proper priors or the Intrinsic Bayes Factor (Berger & Pericchi 1996) instead.")),
    bullet(rt("BIC for small n: The Laplace approximation assumes n >> k. For small n, use the exact marginal likelihood or AICc = AIC + 2k(k+1)/(n-k-1).")),
    bullet(rt("Model averaging: If BF is ambiguous (1/3 < BF < 3), consider Bayesian Model Averaging (BMA) rather than hard selection.")),
    divider(),

    # ── Section 5: The Math ───────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("1. Posterior Model Probabilities"),
    para(rt("Treating model index "), eq(r"i"), rt(" as a parameter, Bayes' theorem at the model level gives:")),
    equation_block(r"P(M_i \mid D) = \frac{p(D \mid M_i)\, P(M_i)}{\displaystyle\sum_{j=1}^K p(D \mid M_j)\, P(M_j)}"),
    para(rt("With uniform model priors "), eq(r"P(M_i) = 1/K"), rt(", posterior model probabilities are proportional to the model evidences.")),
    heading3("2. Closed-Form Evidence — Gaussian with Gaussian Prior"),
    para(rt("Suppose "), eq(r"y_i \mid \mu \overset{iid}{\sim} \mathcal{N}(\mu, \sigma^2)"), rt(" with "), eq(r"\sigma^2"), rt(" known, and prior "), eq(r"\mu \sim \mathcal{N}(\mu_0, \tau^2)"), rt(". The marginal likelihood is:")),
    equation_block(r"\ln p(y \mid M) = -\frac{n}{2}\ln(2\pi\sigma^2) - \frac{1}{2\sigma^2}\sum_{i=1}^n(y_i - \bar{y})^2 - \frac{n(\bar{y}-\mu_0)^2}{2(\sigma^2 + n\tau^2)} - \frac{1}{2}\ln\!\left(1 + \frac{n\tau^2}{\sigma^2}\right)"),
    para(rt("The last term, "), eq(r"-\frac{1}{2}\ln(1 + n\tau^2/\sigma^2)"), rt(", is the Occam factor: it grows negatively as "), eq(r"\tau^2"), rt(" (prior spread) increases, penalising vague models.")),
    heading3("3. Laplace Approximation"),
    para(rt("Expand "), eq(r"\ln p(D \mid \theta, M)"), rt(" around "), eq(r"\hat{\theta}"), rt(":")),
    equation_block(r"\ln p(D \mid M) \approx \ln p(D \mid \hat{\theta}, M) + \frac{k}{2}\ln(2\pi) - \frac{1}{2}\ln\det\mathcal{H}(\hat{\theta})"),
    para(rt("where "), eq(r"\mathcal{H} = -\nabla^2_\theta \ln p(D \mid \theta)\big|_{\hat\theta}"), rt(". For iid data, "), eq(r"\mathcal{H} \approx n\, \mathcal{I}(\hat\theta)"), rt(" where "), eq(r"\mathcal{I}"), rt(" is the single-observation Fisher information, so "), eq(r"\det\mathcal{H} \approx n^k \det\mathcal{I}(\hat\theta)"), rt(" and:")),
    equation_block(r"\ln p(D \mid M) \approx \ln\hat{L} - \frac{k}{2}\ln n + \frac{k}{2}\ln(2\pi) - \frac{1}{2}\ln\det\mathcal{I}(\hat\theta)"),
    heading3("4. BIC Derivation"),
    para(rt("Drop the "), eq(r"O(1)"), rt(" terms (bounded in "), eq(r"k"), rt(") relative to the "), eq(r"(k/2)\ln n"), rt(" term, and multiply by "), eq(r"-2"), rt(":")),
    equation_block(r"\mathrm{BIC} = -2\ln\hat{L} + k\ln n \approx -2\ln p(D \mid M) + k\ln(2\pi)"),
    para(rt("Since "), eq(r"k\ln(2\pi)"), rt(" is the same for models of equal complexity, comparing BIC values between models of different "), eq(r"k"), rt(" is only exactly equivalent to comparing log Bayes factors when we account for this constant. For practical purposes:")),
    equation_block(r"\ln\mathrm{BF}_{12} \approx \frac{\mathrm{BIC}_2 - \mathrm{BIC}_1}{2}"),
    heading3("5. AIC vs BIC: Consistency and Efficiency"),
    para(rt("AIC = "), eq(r"-2\ln\hat{L} + 2k"), rt(". The penalty "), eq(r"2k"), rt(" is derived from minimising Kullback–Leibler divergence to the true predictive distribution (Akaike 1973). BIC's penalty "), eq(r"k\ln n"), rt(" grows with "), eq(r"n"), rt(", making BIC consistent (selects the true model as "), eq(r"n \to \infty"), rt(" if it is in the candidate set), whereas AIC is not consistent but is efficient (minimises prediction error in terms of KL divergence).")),
    callout("⚠️", rt("Mathematical Warning: ", bold=True), rt("The BIC ↔ Bayes factor connection requires (a) proper priors, (b) MLE is a good approximation to the posterior mode, and (c) the posterior is approximately Gaussian (large n). When these fail — e.g., mixture models with non-identifiability, or models with discrete parameters — BIC can give misleading results. Use exact MCMC-based marginal likelihoods (bridge sampling, thermodynamic integration) instead.")),
    divider(),

    # ── Section 6: Code Implementation ───────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """import numpy as np

def log_marginal_likelihood_laplace(X, y):
    \"\"\"Laplace approximation to log p(y|M) for linear Gaussian model.

    Args:
        X: design matrix (n, k)
        y: response vector (n,)
    Returns:
        (log_evidence, BIC)
    \"\"\"
    n, k = X.shape

    # Step 1: Compute MLE via normal equations
    beta_hat = np.linalg.lstsq(X, y, rcond=None)[0]

    # Step 2: Residual sum of squares
    residuals = y - X @ beta_hat
    rss = residuals @ residuals

    # Step 3: MLE for sigma^2 (plug-in)
    sigma2_hat = rss / n

    # Step 4: Maximised log-likelihood
    logL_hat = -n/2 * np.log(2 * np.pi * sigma2_hat) - n/2

    # Step 5: Laplace log-evidence (leading Schwarz term)
    # ln p(y|M) ≈ ln L_hat - (k/2)*ln(n) + O(1)
    log_evidence = logL_hat - (k/2) * np.log(n)

    # Step 6: BIC = -2*logL_hat + k*ln(n)
    bic = -2 * logL_hat + k * np.log(n)

    return log_evidence, bic


def bayes_factor_12(log_ev1, log_ev2):
    \"\"\"Bayes Factor BF_12 = exp(log_ev1 - log_ev2).\"\"\"
    ln_bf = log_ev1 - log_ev2
    # Clip to avoid overflow; BF > e^20 ≈ 5×10^8 is conclusive anyway
    return np.exp(np.clip(ln_bf, -20, 20)), ln_bf


# --- Example ---
np.random.seed(42)
n = 50
x = np.linspace(0, 1, n)
y = 1.5 + 3.0 * x + np.random.randn(n) * 0.4   # true: linear

X1 = np.column_stack([np.ones(n), x])             # M1: linear (k=2)
X2 = np.column_stack([np.ones(n), x, x**2])       # M2: quadratic (k=3)

lnE1, bic1 = log_marginal_likelihood_laplace(X1, y)
lnE2, bic2 = log_marginal_likelihood_laplace(X2, y)
BF12, ln_bf = bayes_factor_12(lnE1, lnE2)

print(f"ln Evidence: M1={lnE1:.3f}, M2={lnE2:.3f}")
print(f"BIC: M1={bic1:.2f}, M2={bic2:.2f}, ΔBIC={bic2-bic1:.2f}")
print(f"BF_12={BF12:.3f} (ln BF={ln_bf:.3f})")
# Kass-Raftery calibration
if abs(ln_bf) < np.log(3.2): verdict = "Inconclusive"
elif abs(ln_bf) < np.log(20): verdict = "Positive"
elif abs(ln_bf) < np.log(150): verdict = "Strong"
else: verdict = "Very Strong"
print(f"Evidence: {verdict} in favour of M{'1' if BF12 > 1 else '2'}")"""),
    heading3("6b — Production Usage (sklearn, ArviZ)"),
    code_block("python", """from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np

def sklearn_bic(X, y):
    \"\"\"BIC via sklearn (note: sklearn uses -2*logL + k*ln(n) convention,
    i.e. the standard formula but accessible via the GaussianMixture API
    or computed manually here).\"\"\"
    model = LinearRegression().fit(X, y)
    n, k = X.shape
    y_pred = model.predict(X)
    rss = np.sum((y - y_pred)**2)
    sigma2 = rss / n
    logL = -n/2 * np.log(2*np.pi*sigma2) - n/2
    bic = -2 * logL + k * np.log(n)
    return bic, logL

# Polynomial features
x = np.linspace(0, 1, 50).reshape(-1, 1)
y = 1.5 + 3.0*x.ravel() + np.random.randn(50)*0.4

results = {}
for degree in range(1, 6):
    Xp = PolynomialFeatures(degree).fit_transform(x)
    bic, logL = sklearn_bic(Xp, y)
    results[degree] = {'BIC': bic, 'k': degree+1}
    print(f"Degree {degree}: k={degree+1}, BIC={bic:.2f}")

best = min(results, key=lambda d: results[d]['BIC'])
print(f"Best model: degree {best}")

# ⚠️ Gotcha: GaussianMixture().bic(X) uses a different normalisation!
# Always compute BIC manually for linear regression comparisons.

# --- ArviZ WAIC (preferred for Bayesian MCMC comparisons) ---
# import arviz as az
# comparison = az.compare({'M1': idata1, 'M2': idata2}, ic='waic')
# print(comparison)  # ranks by elpd_waic, higher = better
# ⚠️ Gotcha: elpd is higher-is-better; BIC is lower-is-better.
#   az.compare provides 'weight' column for model averaging."""),
    callout("⚠️", rt("Gotcha: ", bold=True), rt("Never compare models fit on different data splits. The marginal likelihood must be evaluated on the EXACT same observations. Also, BIC is scale-invariant to the response variable, but misspecifying the likelihood family (e.g. using Gaussian BIC when data is Poisson) invalidates the comparison entirely.")),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is a Bayes factor and how does it differ from a p-value?", bold=True)], [
        para(rt("A Bayes factor "), eq(r"\mathrm{BF}_{12} = p(D \mid M_1)/p(D \mid M_2)"), rt(" is the ratio of marginal likelihoods — it quantifies how much more (or less) likely the data are under M1 than M2. A p-value is "), rt("P(data at least as extreme | H₀ is true)", italic=True), rt(", which is a probability under a single hypothesis, not a ratio of evidences. Key differences: (a) BF can provide evidence in favour of H₀; p-values cannot. (b) BF has a calibrated scale (Kass–Raftery); p < 0.05 is arbitrary. (c) BF requires specifying a prior; p-values do not.")),
    ]),
    toggle([rt("Q2 (Easy): What is BIC and when should you use it instead of AIC?", bold=True)], [
        para(eq(r"\mathrm{BIC} = -2\ln\hat{L} + k\ln n")),
        para(rt("Use BIC when: (a) you want consistency — BIC selects the true model as n→∞ (if it's in the candidate set), which AIC does not. (b) n is large relative to k, making the Laplace approximation valid. Use AIC when: (a) you care about predictive accuracy on new data (AIC is asymptotically equivalent to LOO-CV). (b) n is small (AIC penalises complexity less aggressively). Rule of thumb: BIC for hypothesis testing / model identification; AIC for forecasting / prediction.")),
    ]),
    toggle([rt("Q3 (Medium): Derive why BIC ≈ -2 ln p(D|M) for large n.", bold=True)], [
        para(rt("Start with the Laplace approximation to the marginal likelihood. Expand "), eq(r"\ln p(D \mid \theta, M)"), rt(" around "), eq(r"\hat\theta"), rt(" (the MLE):")),
        para(eq(r"\ln p(D \mid M) \approx \ln\hat{L} + \frac{k}{2}\ln(2\pi) - \frac{1}{2}\ln\det\mathcal{H}")),
        para(rt("For n iid obs, "), eq(r"\mathcal{H} \approx n\mathcal{I}(\hat\theta)"), rt(", so "), eq(r"\ln\det\mathcal{H} \approx k\ln n + \ln\det\mathcal{I}(\hat\theta)"), rt(". Dropping bounded O(1) terms relative to "), eq(r"(k/2)\ln n"), rt(":")),
        para(eq(r"\ln p(D \mid M) \approx \ln\hat{L} - \frac{k}{2}\ln n")),
        para(rt("Multiplying by -2: "), eq(r"\mathrm{BIC} = -2\ln\hat{L} + k\ln n \approx -2\ln p(D \mid M)")),
        para(rt("⚠️ Follow-up trap: 'Is this exact?' — No. The approximation drops "), eq(r"O(k)"), rt(" terms (specifically "), eq(r"k\ln(2\pi) + \ln\det\mathcal{I}(\hat\theta)"), rt("). For model comparison within the same model class, these constants partially cancel.")),
    ]),
    toggle([rt("Q4 (Medium): What is Lindley's paradox?", bold=True)], [
        para(rt("Lindley's paradox (1957): For a point null H₀: θ = θ₀ against a diffuse alternative H₁: θ ∼ Uniform or broad Gaussian, as n → ∞ with the sample mean fixed at the boundary of the rejection region (z = 1.96), the frequentist test rejects H₀ (p = 0.05) but the Bayes factor increasingly favours H₀. The resolution: the frequentist and Bayesian procedures ask different questions. Frequentists ask 'Is the data unlikely under H₀?' Bayesians ask 'Is H₀ more plausible than H₁ after seeing data?' With a very diffuse prior, the data are also unlikely under H₁ — so the Bayes factor can legitimately support H₀ even when p < 0.05.")),
    ]),
    toggle([rt("Q5 (Hard): How does the Occam factor emerge from the Laplace approximation, and why does it penalise complexity?", bold=True)], [
        para(rt("Write the log evidence as goodness-of-fit plus Occam factor:")),
        para(eq(r"\ln p(D \mid M) = \ln p(D \mid \hat\theta, M) + \underbrace{\ln \frac{p(\hat\theta \mid M)}{|\mathcal{H}/(2\pi)|^{1/2}}}_{\text{Occam factor} \leq 0}")),
        para(rt("The Occam factor equals "), eq(r"\ln p(\hat\theta \mid M) - \frac{1}{2}\ln\det(\mathcal{H}/2\pi)"), rt(". The first term is the prior density at the MLE; the second is the (negative) log-volume of the posterior. For a complex model with "), eq(r"\tau^2"), rt(" large (diffuse prior), "), eq(r"p(\hat\theta)"), rt(" is small — the MLE lives in a low-probability region of the prior. For a simple model with a tighter prior that concentrates near the true parameter, "), eq(r"p(\hat\theta)"), rt(" is high. This is the automatic razor: models that spread probability mass over most of parameter space get penalised because their prior places little mass exactly where the data falls.")),
        para(rt("⚠️ Follow-up: 'Can you make the Occam factor disappear?' — Yes, by making the prior sharply peaked at "), eq(r"\hat\theta"), rt(" (a 'spiked' prior). But then the prior encodes the same information as the data, defeating the purpose of model comparison.")),
    ]),
    toggle([rt("Q6 (Hard): When would you use bridge sampling instead of BIC?", bold=True)], [
        para(rt("Bridge sampling (Meng & Wong 1996, Gronau et al. 2017) computes the exact log marginal likelihood from MCMC samples of the posterior. It is preferred over BIC when: (a) the model is non-Gaussian / non-linear (Laplace approximation fails), (b) the posterior has multiple modes, (c) parameters include discrete variables (BIC is undefined), (d) n is small relative to k. Bridge sampling converges to the truth with enough MCMC samples; BIC is only asymptotically valid. The tradeoff: bridge sampling requires fitting both the prior and posterior with MCMC, and can be numerically unstable if the prior and posterior have poor overlap — requiring careful tempered proposal construction.")),
    ]),
    heading3("Multi-level Explanations"),
    heading3("For a PhD Researcher"),
    para(rt("BF₁₂ is the ratio of predictive priors: "), eq(r"p(D \mid M_1)/p(D \mid M_2)"), rt(". It equals the posterior odds divided by prior odds under equal model priors. The Laplace approximation to "), eq(r"\ln p(D \mid M)"), rt(" establishes the connection to BIC via the observed Fisher information. The key assumption is that the posterior concentrates around a unique mode (Bernstein–von Mises theorem), which fails for non-identified likelihoods, latent variable models with many local modes, and heavy-tailed posteriors. For exact computation, use importance sampling (harmonic mean — notoriously unstable), bridge sampling (Meng–Wong), or thermodynamic integration. Bayesian model averaging (BMA) is often more robust than hard selection: "), eq(r"p(y^* \mid D) = \sum_i p(y^* \mid D, M_i) P(M_i \mid D)"), rt(".")),
    heading3("For a Research Scientist / ML Engineer"),
    para(rt("In practice: (1) Fit each model. (2) Compute BIC = -2*logL + k*ln(n). (3) Pick the model with lowest BIC. (4) If ΔBIC < 2, the models are statistically indistinguishable and you may prefer the simpler one or average them. In Bayesian ML (Stan/PyMC), use az.compare() with ic='loo' — it computes PSIS-LOO-CV, which is more reliable than BIC for complex hierarchical models. For neural networks, BIC is impractical (k ≈ millions) — use held-out likelihood or BIC on the effective number of parameters (EIC/TIC).")),
    heading3("Red Flags in Interviews"),
    bullet(rt("'I compare models by their train loss' — No penalty for complexity; always picks the biggest model.")),
    bullet(rt("'I use p-values to choose between nested models' — p-values cannot express evidence for the null; BIC or BF preferred for model selection.")),
    bullet(rt("'BIC is always better than AIC' — BIC is consistent but not efficient; wrong for prediction tasks.")),
    bullet(rt("'Bayes factors work with improper priors' — They don't; the normalising constant is infinite and the ratio is undefined.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ───────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    heading3("Model Selection Criteria Compared"),
    table(6,
        table_row(["Criterion", "Formula", "Consistent?", "Efficient?", "Prior needed?", "Use case"]),
        table_row(["BIC",  "-2lnL̂ + k ln n",        "Yes", "No",  "Implicit flat", "Model identification, large n"]),
        table_row(["AIC",  "-2lnL̂ + 2k",             "No",  "Yes", "No",           "Prediction, small n"]),
        table_row(["AICc", "-2lnL̂ + 2k·n/(n-k-1)",  "No",  "Yes", "No",           "AIC for small n"]),
        table_row(["DIC",  "D(θ̄) + 2p_D",            "No",  "No",  "Full posterior","Hierarchical MCMC models"]),
        table_row(["WAIC", "-2Σ ln p̄(yᵢ) + 2pW",    "Yes*","Yes", "Full posterior","LOO-CV proxy, Stan/PyMC"]),
        table_row(["BF",   "p(D|M₁)/p(D|M₂)",        "Yes", "Yes", "Full prior",   "Rigorous hypothesis comparison"])),
    heading3("When to Use Bayes Factors"),
    bullet(rt("You have principled priors from domain knowledge or previous studies.")),
    bullet(rt("You need to quantify evidence for the null hypothesis.")),
    bullet(rt("You are comparing non-nested models where LRT is inapplicable.")),
    bullet(rt("You want a coherent sequential updating procedure (BF is consistent with sequential Bayes updating).")),
    heading3("When NOT to Use"),
    bullet(rt("Improper priors: BF is undefined (infinite normalising constant corrupts the ratio).")),
    bullet(rt("Very small n with vague priors: Lindley's paradox distorts results.")),
    bullet(rt("Neural networks with millions of parameters: Laplace approximation is computationally infeasible.")),
    bullet(rt("When predictive accuracy is the primary goal: use LOO-CV or WAIC instead.")),
    callout("🎯", rt("Decision: ", bold=True), rt("Use BIC when n is large, priors are hard to specify, and consistency matters. Use exact BF (bridge sampling) when n is small and you have strong priors. Use LOO-CV / WAIC for prediction-oriented Bayesian model selection in Stan or PyMC.")),
    divider(),

    # ── Section 9: Explainer Embed ────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Bayesian inference fundamentals (Bayes' theorem, posterior updates)")),
    bullet(rt("Conjugate priors catalog")),
    bullet(rt("Maximum likelihood estimation")),
    bullet(rt("Gaussian distribution and multivariate normal")),
    heading3("What to Learn Next"),
    bullet(rt("Bayesian Model Averaging (BMA)")),
    bullet(rt("Reversible-jump MCMC (model selection within MCMC)")),
    bullet(rt("Variational Bayes and ELBO as evidence lower bound")),
    bullet(rt("WAIC and PSIS-LOO-CV (modern alternatives to BIC)")),
    bullet(rt("Marginal likelihood estimation via bridge sampling")),
    heading3("Key Papers"),
    bullet(rt("Jeffreys, H. (1961). Theory of Probability (3rd ed.). Oxford. — The founding text.")),
    bullet(rt("Schwarz, G. (1978). Estimating the dimension of a model. Annals of Statistics 6(2): 461–464.")),
    bullet(rt("Kass, R.E., Raftery, A.E. (1995). Bayes factors. JASA 90(430): 773–795. — Essential reference.")),
    bullet(rt("Vehtari, A., Gelman, A., Gabry, J. (2017). Practical Bayesian model evaluation using LOO and WAIC. Statistics and Computing 27: 1413–1432.")),
    bullet(rt("Gronau, Q.F. et al. (2017). A tutorial on bridge sampling. Journal of Mathematical Psychology.")),
    heading3("Best Resources"),
    bullet(rt("Gelman, A. et al. Bayesian Data Analysis (3rd ed.), Ch. 7 — Model checking and comparison.")),
    bullet(rt("MacKay, D.J.C. Information Theory, Inference, and Learning Algorithms, Ch. 28 — Model Comparison.")),
    bullet(rt("McElreath, R. Statistical Rethinking (2nd ed.), Ch. 7 — Ulysses' Compass (AIC, WAIC, LOO).")),
    bullet(rt("ArviZ documentation — az.compare() for practical Bayesian model selection.")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Conjugate Priors, Maximum Likelihood Estimation, Hypothesis Testing, Bayesian Model Averaging, WAIC & LOO-CV, Variational Inference (ELBO), MCMC methods, Information Theory (KL Divergence)")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
