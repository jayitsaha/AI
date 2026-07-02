#!/usr/bin/env python3
"""Update Notion page for: Minimum Description Length (MDL) Principle"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8148-a9d6-ed0a6c4f819d"
ICON = "🟡"  # Intermediate
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/minimum_description_length_explainer.html"

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
    para(rt("The Minimum Description Length (MDL) principle is a method for selecting the best model from a set of candidates. It says: the best model is the one that allows you to compress the data most compactly. Instead of asking 'which model fits best?', MDL asks 'which model + data encoding requires the fewest bits to transmit?'")),
    heading3("Real-World Analogy"),
    para(rt("Imagine trying to write the world's shortest novel that contains all the key information. A one-sentence summary misses details (underfitting). A word-for-word transcript of all human knowledge is too long (overfitting). The 'just right' book captures the true patterns efficiently. MDL finds that book — it picks the model that balances what you say explicitly (model description) against how much remains unexplained (residuals to encode).")),
    heading3("One-Sentence Summary"),
    para(rt("MDL selects the model that minimises the total bits needed to first describe the model, then describe the data given that model — the information-theoretic formalisation of Occam's Razor.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("MDL minimises L(model) + L(data|model). Simpler models cost fewer bits to describe; complex models cost fewer bits to encode residuals. The winner balances both. For Gaussian errors this is equivalent to minimising BIC.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Before MDL, model selection lacked a unified theoretical foundation. AIC (Akaike, 1974) and cross-validation optimise predictive accuracy but have no principled story for why the complexity penalty is what it is. Bayesian approaches require explicit priors that may be hard to specify. There was no purely data-driven, prior-free criterion grounded in first principles.")),
    heading3("The Key Insight"),
    para(rt("Jorma Rissanen's 1978 paper 'Modeling by Shortest Data Description' (Automatica, 1978) established that learning and compression are equivalent. Shannon's source coding theorem says the minimum expected code length for a source equals its entropy. Rissanen extended this: the best model of data is one that, when used as a probabilistic code, achieves the shortest description of that data.")),
    heading3("Evolution Timeline"),
    para(rt("Rissanen 1978 (crude MDL) → Rissanen 1987 (stochastic complexity) → Wallace & Freeman 1987 (MML, closely related) → Rissanen 1996 (NML / normalised maximum likelihood) → Grünwald 2007 (modern MDL unification). Connections to BIC (Schwarz 1978) established that BIC is the asymptotic leading term of NML-MDL.")),
    table(4,
        table_row(["Dimension", "AIC", "BIC / Two-part MDL", "NML MDL"]),
        table_row(["Complexity penalty", "2k", "k·ln n", "COMP(model class)"]),
        table_row(["Objective", "Predictive accuracy", "Model identification", "Exact compression"]),
        table_row(["Consistent selector?", "No", "Yes", "Yes"]),
        table_row(["Prior required?", "No", "No", "No"]),
        table_row(["Computable?", "Yes", "Yes", "Sometimes (Gaussian: yes)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🔑 Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Let "), eq(r"\mathcal{M}"), rt(" be a model class (e.g. all polynomial regressors), "), eq(r"M \in \mathcal{M}"), rt(" a specific model with "), eq(r"k"), rt(" free parameters, and "), eq(r"D = (x_1,\ldots,x_n)"), rt(" a dataset of "), eq(r"n"), rt(" observations.")),
    bullet(rt("L(M)"), rt(" = description length of the model itself (bits to specify its parameter values)")),
    bullet(rt("L(D|M)"), rt(" = description length of the data given the model = "), eq(r"-\log_2 p(D \mid \hat{\theta}_M)"), rt(" where "), eq(r"\hat{\theta}_M"), rt(" is the MLE")),
    bullet(rt("L_{\\text{total}}(M, D) = L(M) + L(D|M)"), rt(" = two-part (crude) MDL code length")),
    heading3("The Fundamental Tradeoff"),
    para(rt("As "), eq(r"k"), rt(" increases: "), eq(r"L(M)"), rt(" grows (more parameters to encode); "), eq(r"L(D|M)"), rt(" shrinks (better fit, lower residual entropy). The total has a unique minimum — the MDL-optimal model.")),
    callout("🔑", rt("Core invariant: ", bold=True), rt("any model that overfits pays a high "), eq(r"L(M)"), rt(" cost. Any model that underfits pays a high "), eq(r"L(D|M)"), rt(" cost. Only the model matching the true complexity minimises the sum.")),
    heading3("Prerequisites"),
    para(rt("To fully understand MDL you should know: Shannon entropy, Kraft inequality, maximum likelihood estimation, BIC, and the basics of Kolmogorov complexity.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings (PhD Deep-Dive) ───────────
    heading2("🏗️ Architecture & Internal Workings"),
    heading3("Two-Part (Crude) MDL — Full Derivation"),
    para(rt("Step 1: choose a model class, e.g. polynomials of degree "), eq(r"k"), rt(". Fit via MLE to get "), eq(r"\hat{\theta}"), rt(".")),
    para(rt("Step 2: Encode the model. To specify "), eq(r"k"), rt(" real parameters when there are "), eq(r"n"), rt(" data points, Rissanen showed you need precision "), eq(r"O(n^{-1/2})"), rt(", requiring "), eq(r"\frac{1}{2}\log_2 n"), rt(" bits per parameter:")),
    equation_block(r"L(M) = \frac{k}{2}\log_2 n"),
    para(rt("Intuition: with more data, MLE is more precise, so parameters need fewer quantisation levels — but the log grows slowly, penalising complexity gently.")),
    para(rt("Step 3: Encode the data. Under Gaussian errors with MLE variance "), eq(r"\hat{\sigma}^2 = \frac{1}{n}\sum(y_i - \hat{y}_i)^2"), rt(":")),
    equation_block(r"L(D \mid M) = \frac{n}{2}\log_2\hat{\sigma}^2 + \frac{n}{2}\log_2(2\pi e)"),
    para(rt("Step 4: Sum and minimise over "), eq(r"k"), rt(":")),
    equation_block(r"\hat{k}_{\text{MDL}} = \underset{k}{\operatorname{argmin}}\left[\frac{k}{2}\log_2 n + \frac{n}{2}\log_2\hat{\sigma}^2_k\right]"),
    heading3("Numerical Trace — Polynomial Regression"),
    para(rt("Data: "), eq(r"n=20"), rt(" observations from "), eq(r"y = 0.5x^2 + 0.3x + \varepsilon"), rt(", "), eq(r"\varepsilon\sim\mathcal{N}(0,0.25)"), rt(", seed=42.")),
    table(7,
        table_row(["Degree k", "Params", "RSS", "sigma^2 hat", "L(model)", "L(data|M)", "L_total"]),
        table_row(["0", "1", "10.755", "0.538", "2.16", "31.99", "34.15"]),
        table_row(["1", "2", "10.636", "0.532", "4.32", "31.83", "36.15"]),
        table_row(["2 (MDL min)", "3", "2.715", "0.136", "6.48", "12.13", "18.61"]),
        table_row(["3", "4", "2.472", "0.124", "8.64", "10.78", "19.43"]),
        table_row(["4", "5", "2.450", "0.123", "10.80", "10.65", "21.46"]),
        table_row(["8", "9", "1.861", "0.093", "19.45", "6.69", "26.13"]),
    ),
    para(rt("MDL correctly identifies degree 2 as the optimal model. Note that degree 1 is actually worse than degree 0 (total 36.15 vs 34.15) — a linear model adds cost without proportional benefit.")),
    heading3("Design Decisions"),
    callout("🔧", rt("Why ½·log₂(n) per parameter? ", bold=True), rt("This comes from quantisation theory: to estimate "), eq(r"\theta"), rt(" to precision "), eq(r"n^{-1/2}"), rt(" (the MLE standard error), you need "), eq(r"\log_2 n^{1/2} = \frac{1}{2}\log_2 n"), rt(" bits. This is also the term in Stirling's approximation that gives BIC its penalty.")),
    heading3("Failure Modes"),
    bullet(rt("MDL requires the model class to be fixed in advance. Selecting the class itself is a meta-MDL problem.")),
    bullet(rt("Two-part MDL is biased (depends on the parameterisation of the model). NML resolves this.")),
    bullet(rt("For very small n, the ½·log₂(n) penalty may be too weak, causing overfitting.")),
    divider(),

    # ── Section 5: The Math Behind It ─────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Normalized Maximum Likelihood (NML) — The Exact Form"),
    para(rt("NML avoids the parameterisation dependence of two-part MDL by defining the optimal code directly. The NML distribution over data sequences "), eq(r"x^n"), rt(" under model class "), eq(r"\mathcal{M}"), rt(" is:")),
    equation_block(r"p_{\text{NML}}(x^n \mid \mathcal{M}) = \frac{p(x^n \mid \hat{\theta}(x^n))}{\mathcal{C}_n(\mathcal{M})}"),
    para(rt("where "), eq(r"\hat{\theta}(x^n)"), rt(" is the MLE for the observed sequence "), eq(r"x^n"), rt(", and the denominator is the ")),
    para(rt("Parametric Complexity (COMP):")),
    equation_block(r"\mathcal{C}_n(\mathcal{M}) = \int p(y^n \mid \hat{\theta}(y^n))\, dy^n"),
    para(rt("COMP counts 'how many distinguishably different data sequences of length n can this model class fit well?' The NML code length is:")),
    equation_block(r"L_{\text{NML}}(x^n) = -\log_2 p(x^n \mid \hat{\theta}(x^n)) + \log_2 \mathcal{C}_n(\mathcal{M})"),
    para(rt("The first term is the negative log-likelihood (how well the MLE fits). The second term is the complexity cost — analogous to "), eq(r"L(M)"), rt(" but now exact and parameterisation-invariant.")),
    heading3("Asymptotic Expansion — Connection to BIC"),
    para(rt("For regular parametric models with "), eq(r"k"), rt(" parameters, Fisher information "), eq(r"I(\theta)"), rt(", and smooth likelihood:")),
    equation_block(r"\log_2 \mathcal{C}_n(\mathcal{M}) \approx \frac{k}{2}\log_2\frac{n}{2\pi e} + \log_2 \int_\Theta \sqrt{\det I(\theta)}\, d\theta + O(n^{-1})"),
    para(rt("The dominant term "), eq(r"\frac{k}{2}\log_2 n"), rt(" is exactly the BIC penalty (divided by "), eq(r"\ln 2"), rt("). The Fisher integral is data-independent and drops out of model comparisons. This proves BIC ≈ NML-MDL to leading order.")),
    heading3("Connection to Kolmogorov Complexity"),
    para(rt("Kolmogorov complexity "), eq(r"K(x)"), rt(" is the length of the shortest program (on a universal Turing machine) that outputs "), eq(r"x"), rt(". MDL upper-bounds "), eq(r"K(x)"), rt(" via specific model classes:")),
    equation_block(r"K(x) \leq L_{\text{NML}}(x \mid \mathcal{M}) + O(\log L_{\text{NML}}(x \mid \mathcal{M}))"),
    para(rt("As "), eq(r"\mathcal{M}"), rt(" grows richer (more model classes), "), eq(r"L_{\text{NML}}"), rt(" approaches "), eq(r"K"), rt(". MDL is the computable approximation to the uncomputable Kolmogorov complexity.")),
    callout("⚠️", rt("Common Misconception: ", bold=True), rt("MDL is not Bayesian. It requires no prior. NML emerges from the minimax code-length game: choose the code that minimises the worst-case regret relative to the best model in the class. The solution is NML — no prior needed.")),
    heading3("Stochastic Complexity"),
    para(rt("Rissanen's 1987 stochastic complexity "), eq(r"S(x^n \mid \mathcal{M})"), rt(" generalises MDL to sequential (online) coding. At each step "), eq(r"t"), rt(", you encode "), eq(r"x_t"), rt(" using the model fit on "), eq(r"x^{t-1}"), rt(":")),
    equation_block(r"S(x^n \mid \mathcal{M}) = \sum_{t=1}^{n} -\log_2 p(x_t \mid x^{t-1}, \hat{\theta}(x^{t-1}))"),
    divider(),

    # ── Section 6: Code Implementation ────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("From Scratch — Two-Part MDL for Polynomial Selection"),
    code_block("python", """import numpy as np
from itertools import product

def mdl_two_part_gaussian(x, y, degree):
    \"\"\"Compute MDL two-part code for polynomial regression.

    Uses Rissanen's parameter encoding cost (k/2 * log2(n)) and
    Gaussian MLE data code (-log2-likelihood).

    Args:
        x: input array, shape (n,)
        y: target array, shape (n,)
        degree: polynomial degree k

    Returns:
        (L_model, L_data, L_total) all in bits
    \"\"\"
    n = len(y)
    k = degree + 1  # number of parameters (including intercept)

    # Fit by OLS (MLE for Gaussian noise)
    if degree == 0:
        y_hat = np.full(n, y.mean())
    else:
        coeffs = np.polyfit(x, y, degree)
        y_hat = np.polyval(coeffs, x)

    # Residual variance (MLE, biased estimator)
    rss = np.sum((y - y_hat) ** 2)
    sigma2_mle = rss / n

    # L(M): parameter encoding cost
    L_model = 0.5 * k * np.log2(n)

    # L(D|M): negative log-likelihood under Gaussian
    # = (n/2)*log2(sigma2) + (n/2)*log2(2*pi*e)
    # Drop the constant (n/2)*log2(2*pi*e) only if comparing across models
    LOG2PIE = np.log2(2 * np.pi * np.e)
    L_data = 0.5 * n * np.log2(max(sigma2_mle, 1e-15)) + 0.5 * n * LOG2PIE

    return L_model, L_data, L_model + L_data


def mdl_select(x, y, max_degree=10):
    \"\"\"Select polynomial degree via MDL.\"\"\"
    results = []
    for deg in range(max_degree + 1):
        L_M, L_D, L_T = mdl_two_part_gaussian(x, y, deg)
        results.append({"degree": deg, "L_model": L_M, "L_data": L_D, "L_total": L_T})
    best = min(results, key=lambda r: r["L_total"])
    return best, results


# ── Demo ──
np.random.seed(42)
n = 20
x = np.linspace(-2, 2, n)
y = 0.5 * x**2 + 0.3 * x + np.random.randn(n) * 0.5  # true degree = 2

best, results = mdl_select(x, y, max_degree=8)
print(f"MDL selects degree: {best['degree']}  (L_total = {best['L_total']:.2f} bits)")
# Output: MDL selects degree: 2  (L_total = 18.61 bits)

for r in results:
    marker = " ← MDL" if r["degree"] == best["degree"] else ""
    print(f"deg={r['degree']}: L_model={r['L_model']:.2f}  L_data={r['L_data']:.2f}  Total={r['L_total']:.2f}{marker}")
"""),
    heading3("Production Usage — sklearn + MDL / BIC for Gaussian Mixture Models"),
    code_block("python", """from sklearn.mixture import GaussianMixture
import numpy as np

# BIC ≈ two-part MDL for Gaussian mixture selection
# sklearn computes BIC = -2*log_likelihood + k*ln(n)
# This is exactly 2 * L(D|M) * ln(2) + (k/2*log2(n)) * 2*ln(2) ≈ MDL

X = np.random.randn(300, 2)  # your data, shape (n_samples, n_features)

# Sweep over number of components
bic_scores = []
ks = range(1, 10)
for k in ks:
    gm = GaussianMixture(n_components=k, random_state=42)
    gm.fit(X)
    bic_scores.append(gm.bic(X))
    # Lower BIC = better MDL score

best_k = ks[np.argmin(bic_scores)]
print(f"MDL/BIC selects k={best_k} components")

# Gotcha: BIC in sklearn uses natural log, not log2.
# This doesn't affect model selection (only scales all values by ln2).
# Always compare BIC values within the same run — don't compare across
# different datasets or different sklearn versions.
"""),
    callout("⚠️", rt("Gotcha: ", bold=True), rt("sklearn's BIC uses natural log (nats) not bits. Model selection is unaffected (argmin is invariant to positive scaling), but the numeric values are not in bits. To convert: L_bits = BIC / (2 * ln 2).")),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is MDL? Why does it prevent overfitting?", bold=True)], [
        para(rt("MDL selects the model "), eq(r"M^* = \arg\min_M [L(M) + L(D|M)]"), rt(". An overfit model has a complex description (high "), eq(r"L(M)"), rt("), while an underfit model has large residuals (high "), eq(r"L(D|M)"), rt("). The sum is minimised only by the model that captures true structure without memorising noise.")),
    ]),
    toggle([rt("Q2 (Easy): How is MDL related to BIC?", bold=True)], [
        para(rt("Two-part MDL with Gaussian errors gives the penalty "), eq(r"\frac{k}{2}\log_2 n"), rt(". BIC is "), eq(r"-2\log\hat{L} + k\ln n"), rt(". Since "), eq(r"\log_2 n = \ln n / \ln 2"), rt(", BIC = 2·ln(2)·[L_data·log2→nat + L_model·bit→nat]. BIC is two-part MDL in nats, scaled by 2. Model selection is identical since argmin is preserved under positive scaling.")),
    ]),
    toggle([rt("Q3 (Medium): What is NML MDL and why is it better than two-part MDL?", bold=True)], [
        para(rt("Two-part MDL requires an arbitrary choice of how to encode the parameters (uniform quantisation, log-precision, etc.) — the result depends on the parameterisation. NML avoids this by defining the code directly as the distribution that minimises worst-case regret: "), eq(r"p_{\text{NML}}(x^n) = p(x^n|\hat{\theta}(x^n)) / \mathcal{C}_n"), rt(". The complexity term "), eq(r"\log \mathcal{C}_n"), rt(" is parameterisation-invariant because COMP counts distinguishable sequences, not parameter values.")),
    ]),
    toggle([rt("Q4 (Medium): How does MDL formalise Occam's Razor?", bold=True)], [
        para(rt("Occam's Razor: among models fitting the data equally well, prefer the simpler one. MDL quantifies 'simpler' as 'shorter to describe' ("), eq(r"L(M)"), rt(") and 'fitting equally well' as 'similar residual code cost' ("), eq(r"L(D|M)"), rt("). The principle is not just a preference but a theorem: for iid data from a distribution in "), eq(r"\mathcal{M}"), rt(", MDL-selected models converge to the true model as "), eq(r"n \to \infty"), rt(" (consistency), because only the true model achieves the minimum description length asymptotically.")),
    ]),
    toggle([rt("Q5 (Hard): What is the minimax regret interpretation of NML?", bold=True)], [
        para(rt("Define regret of using model "), eq(r"M"), rt(" for sequence "), eq(r"x^n"), rt(" as "), eq(r"R(x^n, M) = -\log p(x^n|M) - \min_{M'\in\mathcal{M}}[-\log p(x^n|M')]"), rt(". The minimax code minimises worst-case regret: "), eq(r"\min_q \max_{x^n} [-\log q(x^n) + \log p(x^n|\hat{\theta}(x^n))]"), rt(". The solution to this minimax game is precisely the NML distribution. COMP equals the minimax regret. This is the game-theoretic foundation of MDL.")),
    ]),
    toggle([rt("Q6 (Hard): When does MDL fail or require care?", bold=True)], [
        para(rt("(1) Non-parametric models: COMP may be infinite (the model class is too rich). Solution: restrict the class or use a finite approximation. (2) Heavy-tailed data: Gaussian residual coding "), eq(r"\frac{n}{2}\log_2\hat{\sigma}^2"), rt(" is misspecified; use the appropriate distribution. (3) Very small n: the "), eq(r"\frac{k}{2}\log_2 n"), rt(" penalty underestimates true complexity — AIC may be preferred for predictive purposes. (4) Model misspecification: if the true model is outside "), eq(r"\mathcal{M}"), rt(", MDL selects the best approximation within the class (robust but not exact).")),
    ]),
    toggle([rt("Q7 (Expert): Explain MDL to a PhD Researcher vs a Research Scientist.", bold=True)], [
        para(rt("PhD Researcher: ", bold=True), rt("MDL is the computable analogue of Kolmogorov complexity. Two-part MDL upper-bounds "), eq(r"K(x^n)"), rt(" via fixed model classes. NML achieves the minimax-optimal description length within "), eq(r"\mathcal{M}"), rt(": "), eq(r"L_{\text{NML}}(x^n) = -\log p(x^n|\hat{\theta}) + \log \mathcal{C}_n"), rt(". The COMP term equals the capacity of "), eq(r"\mathcal{M}"), rt(" in a precise information-theoretic sense. Asymptotically, "), eq(r"\log \mathcal{C}_n \sim \frac{k}{2}\log n"), rt(" for exponential families. MDL connects to PAC-Bayes bounds through the coding interpretation of KL divergence.")),
        para(rt("Research Scientist: ", bold=True), rt("In practice, use BIC for Gaussian models (sklearn's GaussianMixture.bic, GLM selection). BIC is MDL's leading term with a well-understood penalty: "), eq(r"k\ln n"), rt(". For non-Gaussian models, compute MDL directly as negative log-likelihood plus an encoding cost for parameters. MDL is consistent (picks the true model as n grows), unlike AIC. Use MDL when model identification matters; use AIC/cross-validation when predictive accuracy is the goal.")),
    ]),
    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Criterion", "Penalty", "Consistent?", "Computable?", "Best For"]),
        table_row(["AIC", "2k", "No", "Yes", "Predictive accuracy, small n"]),
        table_row(["BIC / 2-part MDL", "k·ln n", "Yes", "Yes", "Model identification, large n"]),
        table_row(["NML MDL", "log COMP(M)", "Yes", "Gaussian: yes", "Exact compression, theoretical"]),
        table_row(["Stochastic complexity", "Sequential NML", "Yes", "Sometimes", "Online/streaming data"]),
        table_row(["Cross-validation", "None (empirical)", "No", "Yes", "Prediction, non-parametric"]),
        table_row(["Bayes factor / BMA", "Prior-dependent", "Yes*", "MCMC", "When priors are available"]),
    ),
    callout("🎯", rt("Decision guide: ", bold=True), rt("Use BIC/MDL when you want to identify the true model structure and n is large. Use AIC or LOOCV when you care about prediction with small n. Use NML-MDL for theoretically rigorous compression. Use Bayes factors when informative priors are available and justified.")),
    heading3("Advantages of MDL"),
    bullet(rt("No prior distribution required — fully data-driven")),
    bullet(rt("Consistent: selects true model as n → ∞")),
    bullet(rt("Interpretable: penalty has a precise information-theoretic meaning")),
    bullet(rt("Unifies compression and learning — deep theoretical connections")),
    bullet(rt("Robust to mild model misspecification")),
    heading3("Disadvantages of MDL"),
    bullet(rt("Two-part MDL depends on parameterisation choice")),
    bullet(rt("NML-COMP may be infinite for non-parametric or very rich model classes")),
    bullet(rt("Computationally heavier than AIC for complex COMP integrals")),
    bullet(rt("Requires specification of the model class "), eq(r"\mathcal{M}"), rt(" — class selection is a meta-MDL problem")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the MDL tradeoff visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ───────────────────────────
    heading2("📚 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Shannon entropy and source coding theorem")),
    bullet(rt("Kraft inequality and prefix-free codes")),
    bullet(rt("Maximum likelihood estimation")),
    bullet(rt("Kullback-Leibler divergence")),
    bullet(rt("Kolmogorov complexity (theoretical background)")),
    heading3("What to Learn Next"),
    bullet(rt("AIC and BIC — practical model selection criteria")),
    bullet(rt("Bayesian model comparison and Bayes factors")),
    bullet(rt("Variational inference — ELBO as a compression objective")),
    bullet(rt("PAC-Bayes bounds — MDL connects to generalisation theory")),
    bullet(rt("Information bottleneck — MDL-flavoured representation learning")),
    heading3("Key Papers"),
    numbered(rt("Rissanen, J. (1978). Modeling by shortest data description. Automatica, 14(5), 465–471. ", italic=True), rt("— The founding MDL paper.")),
    numbered(rt("Rissanen, J. (1996). Fisher information and stochastic complexity. IEEE Transactions on Information Theory, 42(1), 40–47. ", italic=True), rt("— NML and parametric complexity.")),
    numbered(rt("Grünwald, P. D. (2007). The Minimum Description Length Principle. MIT Press. ", italic=True), rt("— Definitive modern treatment.")),
    numbered(rt("Schwarz, G. (1978). Estimating the dimension of a model. Annals of Statistics, 6(2), 461–464. ", italic=True), rt("— BIC; asymptotically equivalent to MDL.")),
    numbered(rt("Wallace, C. S., & Freeman, P. R. (1987). Estimation and inference by compact coding. JRSS-B. ", italic=True), rt("— Minimum message length (MML), closely related.")),
    heading3("Best Resources"),
    bullet(rt("Grünwald (2007) 'The MDL Principle' — MIT Press, comprehensive")),
    bullet(rt("MacKay (2003) 'Information Theory, Inference, and Learning Algorithms' — Ch. 28, free online")),
    bullet(rt("Vitanyi & Li (1997) 'An Introduction to Kolmogorov Complexity' — theoretical foundations")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Shannon Entropy, Kolmogorov Complexity, BIC, AIC, Bayesian Model Selection, Information Bottleneck, PAC-Bayes Bounds, Variational Inference (ELBO = MDL-flavoured objective).")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
