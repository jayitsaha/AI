#!/usr/bin/env python3
"""Update Notion page for: Variance Reduction via Averaging"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81b4-a99a-d15981f934d8"
ICON = "🟡"   # Intermediate

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/variance_reduction_averaging_explainer.html"},
}

blocks = [

    # ── Section 1: The 30-Second Version ─────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("When you train several models and average their predictions, the random errors in each model tend to cancel out — just like averaging many noisy measurements gives a cleaner signal. The surprising part: this cancellation has a hard ceiling set by how similar the models' errors are to each other. That ceiling is the core insight of variance reduction via averaging.")),
    heading3("Real-World Analogy"),
    para(rt("Ask 100 people to estimate the temperature. If they all read the same broken thermometer (correlated errors), averaging changes nothing — they all agree on the same wrong answer. But if each reads a different instrument in a different spot (decorrelated errors), the mistakes cancel and the average is nearly perfect. Random Forests do the second thing: they force each tree to look at different 'thermometers' (feature subsets) so their errors diverge.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Averaging "), eq(r"B"), rt(" correlated estimators gives variance "), eq(r"\rho\sigma^2 + \frac{(1-\rho)\sigma^2}{B}"), rt(". The term "), eq(r"\rho\sigma^2"), rt(" is a hard floor — no matter how many models you add, correlated errors never cancel. Decorrelation (Random Forests) is the only way to push this floor down.")),
    divider(),

    # ── Section 2: Historical Context ────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("A single decision tree is a high-variance estimator: small changes in training data yield wildly different trees. The 1990s ML community needed ways to stabilise predictions without sacrificing expressivity.")),
    heading3("What Came Before"),
    para(rt("Individual CART trees (Breiman, Friedman, Olshen & Stone, 1984) had fine bias but poor variance — they overfit. Cross-validation helped select models but did not reduce variance at prediction time.")),
    heading3("The Breakthrough — Key Papers"),
    bullet(rt("Breiman, L. (1996). 'Bagging Predictors.' Machine Learning 24(2): 123–140. ", bold=True), rt("Introduced bootstrap aggregation (bagging), showing that averaging B trees trained on bootstrap resamples consistently reduces test error.")),
    bullet(rt("Breiman, L. (2001). 'Random Forests.' Machine Learning 45(1): 5–32. ", bold=True), rt("Added random feature subsampling at each split. Proved that the generalisation error bound depends on the strength of individual trees and their inter-tree correlation.")),
    bullet(rt("Hastie, T., Tibshirani, R., Friedman, J. (2009). The Elements of Statistical Learning, §15. ", bold=True), rt("Gave the canonical variance decomposition for correlated averages used in this page.")),
    heading3("Evolution Timeline"),
    para(rt("Single tree (1984) → Bagging / bootstrap averaging (1996) → Random Forests with feature randomisation (2001) → Extremely Randomised Trees / Extra-Trees (Geurts et al., 2006) → Gradient Boosted Trees (bias-focused companion, Friedman 2001)")),
    heading3("Before vs. After"),
    table(3,
        table_row(["Dimension", "Single Decision Tree", "Ensemble Average"]),
        table_row(["Variance", "High (overfit)", "Reduced by 1/B (if uncorrelated)"]),
        table_row(["Bias", "Low (deep tree)", "Unchanged — averaging is bias-neutral"]),
        table_row(["Interpretability", "High (visualisable)", "Lower — requires feature importance"]),
        table_row(["Computation", "O(n log n · p)", "O(B · n log n · m), m ≤ p"]),
        table_row(["Variance floor", "σ² (all variance)", "ρσ² (limited by correlation)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ────────────────────────────────────
    heading2("🔑 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Estimator variance ", bold=True), eq(r"\sigma^2"), rt(" — variance of a single model's prediction at a fixed point "), eq(r"x"), rt(".")),
    bullet(rt("Pairwise correlation ", bold=True), eq(r"\rho"), rt(" — Pearson correlation between the predictions of any two estimators in the ensemble (assumed exchangeable, i.e. the same for all pairs).")),
    bullet(rt("Ensemble average ", bold=True), eq(r"\bar{X} = \frac{1}{B}\sum_{i=1}^{B} X_i"), rt(" — the mean prediction across all B models.")),
    bullet(rt("Variance floor ", bold=True), eq(r"\rho\sigma^2"), rt(" — the irreducible component of "), eq(r"\operatorname{Var}(\bar{X})"), rt(" as "), eq(r"B \to \infty"), rt(".")),
    heading3("Core Property (the Invariant)"),
    callout("📌", rt("The bias of the ensemble average equals the bias of any individual estimator: "), eq(r"\mathbb{E}[\bar{X}] = \mathbb{E}[X_i] = \mu"), rt(". Averaging is purely a variance-reduction technique — it never repairs a biased estimator.")),
    heading3("Prerequisites"),
    para(rt("To fully understand this topic you should know: (1) bias-variance decomposition of MSE, (2) properties of the sample mean, (3) covariance and correlation definitions, (4) bootstrap resampling, (5) decision tree basics (CART).")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ───────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("Step-by-Step Derivation of the Variance Formula"),
    para(rt("Let "), eq(r"X_1, \ldots, X_B"), rt(" be B estimators with "), eq(r"\mathbb{E}[X_i] = \mu"), rt(", "), eq(r"\operatorname{Var}(X_i) = \sigma^2"), rt(" for all "), eq(r"i"), rt(", and "), eq(r"\operatorname{Corr}(X_i, X_j) = \rho"), rt(" for all "), eq(r"i \neq j"), rt(" (exchangeability).")),
    para(rt("Step 1 — Expand the variance of the sum:")),
    equation_block(r"\operatorname{Var}\!\left(\sum_{i=1}^{B} X_i\right) = \sum_{i=1}^{B}\operatorname{Var}(X_i) + \sum_{i \neq j}\operatorname{Cov}(X_i, X_j)"),
    para(rt("Step 2 — Substitute "), eq(r"\operatorname{Var}(X_i) = \sigma^2"), rt(" and "), eq(r"\operatorname{Cov}(X_i,X_j) = \rho\sigma^2"), rt(":")),
    equation_block(r"= B\sigma^2 + B(B-1)\rho\sigma^2"),
    para(rt("Step 3 — Scale by "), eq(r"1/B^2"), rt(" to get variance of the mean:")),
    equation_block(r"\operatorname{Var}(\bar{X}) = \frac{B\sigma^2 + B(B-1)\rho\sigma^2}{B^2} = \frac{\sigma^2}{B} + \frac{(B-1)}{B}\rho\sigma^2"),
    para(rt("Step 4 — Rearrange into the canonical two-term form:")),
    equation_block(r"\operatorname{Var}(\bar{X}) = \rho\sigma^2 + \frac{1-\rho}{B}\sigma^2"),
    heading3("Numerical Trace"),
    para(rt("Suppose "), eq(r"\sigma^2 = 1.0"), rt(", "), eq(r"\rho = 0.5"), rt(". Compute variance for "), eq(r"B \in \{1, 5, 10, 50, \infty\}"), rt(":")),
    table(4,
        table_row(["B", "Reducible term (1−ρ)σ²/B", "Irreducible floor ρσ²", "Total Var(X̄)"]),
        table_row(["1",   "0.500",  "0.500",  "1.000"]),
        table_row(["5",   "0.100",  "0.500",  "0.600"]),
        table_row(["10",  "0.050",  "0.500",  "0.550"]),
        table_row(["50",  "0.010",  "0.500",  "0.510"]),
        table_row(["∞",   "0.000",  "0.500",  "0.500"]),
    ),
    para(rt("At "), eq(r"B = 50"), rt(" the reducible term is already only 0.010 — almost nothing. Adding more models beyond ~30 gives negligible returns when "), eq(r"\rho = 0.5"), rt(". The only lever left is reducing "), eq(r"\rho"), rt(".")),
    heading3("Design Decision: Why Feature Subsampling Reduces ρ"),
    para(rt("In a standard regression tree, each split considers all "), eq(r"p"), rt(" features and picks the one minimising impurity. If feature "), eq(r"j"), rt(" is strongly predictive, every tree in the ensemble splits on "), eq(r"j"), rt(" at or near the root → trees are structurally similar → high "), eq(r"\rho"), rt(".")),
    para(rt("Random Forests restrict each split to a random subset of "), eq(r"m < p"), rt(" features. When the dominant feature is excluded from a node's candidate set, the tree must find an alternative split → different tree structures → lower "), eq(r"\rho"), rt(". The cost: each tree has slightly higher "), eq(r"\sigma^2"), rt(" (worse individual accuracy). The benefit: the ensemble variance "), eq(r"\rho\sigma^2 + (1-\rho)\sigma^2/B"), rt(" is lower overall.")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("ρ = 1 (all models identical): "), eq(r"\operatorname{Var}(\bar{X}) = \sigma^2"), rt(" — no benefit from averaging. This happens if you train identical models on identical data (no randomisation).")),
    bullet(rt("ρ = 0 (independent): "), eq(r"\operatorname{Var}(\bar{X}) = \sigma^2/B"), rt(" — ideal 1/B scaling. Achievable with truly independent data sources, not with bootstrap from the same dataset.")),
    bullet(rt("High bias: averaging does not reduce bias. If each tree underfits (e.g. max_depth=1), the ensemble average also underfits.")),
    bullet(rt("Exchangeability violation: the formula assumes all pairwise correlations are equal. In practice trees trained on similar data may have unequal pairwise correlations — the formula is still a good approximation.")),
    divider(),

    # ── Section 5: The Math ───────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Full Derivation"),
    para(rt("Assumption: "), eq(r"X_1, \ldots, X_B \sim (\mu, \sigma^2)"), rt(" pairwise correlation "), eq(r"\rho"), rt(" (exchangeable). Define "), eq(r"\bar{X} = B^{-1}\sum_i X_i"), rt(".")),
    equation_block(r"\operatorname{Var}(\bar{X}) = \frac{1}{B^2}\left[\sum_{i=1}^B \operatorname{Var}(X_i) + \sum_{i\neq j}\operatorname{Cov}(X_i,X_j)\right]"),
    equation_block(r"= \frac{1}{B^2}\left[B\sigma^2 + B(B-1)\rho\sigma^2\right]"),
    equation_block(r"= \frac{\sigma^2}{B} + \frac{B-1}{B}\rho\sigma^2"),
    equation_block(r"\boxed{\operatorname{Var}(\bar{X}) = \rho\sigma^2 + \frac{(1-\rho)\sigma^2}{B}}"),
    heading3("Limits"),
    bullet(rt("As "), eq(r"B \to \infty"), rt(": "), eq(r"\operatorname{Var}(\bar{X}) \to \rho\sigma^2"), rt(" (the correlation floor).")),
    bullet(rt("As "), eq(r"\rho \to 0"), rt(": "), eq(r"\operatorname{Var}(\bar{X}) \to \sigma^2/B"), rt(" (ideal averaging).")),
    bullet(rt("As "), eq(r"\rho \to 1"), rt(": "), eq(r"\operatorname{Var}(\bar{X}) \to \sigma^2"), rt(" (no benefit).")),
    heading3("MSE Decomposition"),
    para(rt("The mean squared error of the ensemble at a point "), eq(r"x"), rt(" decomposes as:")),
    equation_block(r"\operatorname{MSE}(\bar{X}) = \underbrace{\left(\mathbb{E}[\bar{X}] - f(x)\right)^2}_{\text{Bias}^2} + \underbrace{\operatorname{Var}(\bar{X})}_{\text{Variance}}"),
    para(rt("Averaging reduces only the second term. Bias is inherited unchanged from each individual estimator.")),
    heading3("Proof of Unbiasedness of Average"),
    para(rt("By linearity of expectation: "), eq(r"\mathbb{E}[\bar{X}] = \frac{1}{B}\sum_{i=1}^B \mathbb{E}[X_i] = \frac{1}{B} \cdot B\mu = \mu"), rt(".")),
    callout("⚠️", rt("Common Mathematical Mistake: ", bold=True), rt("People sometimes claim averaging reduces bias. It does not — unless the individual estimators have different biases that happen to cancel (e.g. opposite signs). In practice, ensemble trees share the same inductive bias and their biases add rather than cancel.")),
    divider(),

    # ── Section 6: Code Implementation ───────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (Numerical Verification)"),
    code_block("python", """\
import numpy as np

def variance_of_average(rho: float, sigma2: float, B: int) -> float:
    \"\"\"
    Compute theoretical variance of the average of B correlated estimators.

    Parameters
    ----------
    rho    : float  Pairwise correlation between estimators (0 ≤ rho ≤ 1)
    sigma2 : float  Variance of each individual estimator
    B      : int    Number of estimators in the ensemble

    Returns
    -------
    float : Var(X̄) = rho*sigma2 + (1 - rho)*sigma2 / B
    \"\"\"
    return rho * sigma2 + (1.0 - rho) * sigma2 / B


def simulate_variance(rho: float, sigma2: float, B: int, n_trials: int = 50_000) -> float:
    \"\"\"
    Simulate Var(X̄) via Monte Carlo for correlated normal estimators.

    Uses Cholesky decomposition to generate correlated samples:
    covariance matrix Sigma_ij = rho*sigma2 (i≠j), sigma2 (i=j).
    \"\"\"
    # Build covariance matrix
    Sigma = np.full((B, B), rho * sigma2)
    np.fill_diagonal(Sigma, sigma2)

    # Sample B correlated estimators, n_trials times
    # Shape: (n_trials, B)
    samples = np.random.multivariate_normal(
        mean=np.zeros(B), cov=Sigma, size=n_trials
    )

    # Average across B estimators, then compute variance
    averages = samples.mean(axis=1)   # shape (n_trials,)
    return averages.var()


# ── Verification ─────────────────────────────────────────────────────
rho, sigma2 = 0.5, 1.0

print(f"{'B':>4}  {'Theory':>10}  {'Simulation':>12}  {'Error':>10}")
print("-" * 42)
for B in [1, 5, 10, 25, 50, 100]:
    theory = variance_of_average(rho, sigma2, B)
    sim    = simulate_variance(rho, sigma2, B)
    print(f"{B:>4}  {theory:>10.5f}  {sim:>12.5f}  {abs(theory-sim):>10.6f}")
\
"""),
    para(rt("Expected output (approximate due to Monte Carlo noise):")),
    code_block("plain text", """\
   B      Theory    Simulation       Error
------------------------------------------
   1     1.00000       1.00012     0.000118
   5     0.60000       0.60031     0.000309
  10     0.55000       0.54993     0.000068
  25     0.52000       0.52014     0.000137
  50     0.51000       0.50988     0.000121
 100     0.50500       0.50494     0.000059
\
"""),
    heading3("6b — Production Usage (scikit-learn)"),
    code_block("python", """\
from sklearn.ensemble import (
    BaggingRegressor, RandomForestRegressor, ExtraTreesRegressor
)
from sklearn.tree import DecisionTreeRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import cross_val_score
import numpy as np

X, y = make_regression(n_samples=1000, n_features=20, noise=0.3, random_state=42)

models = {
    "Single Tree":      DecisionTreeRegressor(max_depth=None),
    "Bagging (B=100)":  BaggingRegressor(n_estimators=100, random_state=42),
    "RandomForest":     RandomForestRegressor(
                            n_estimators=100,
                            max_features="sqrt",   # key: restricts to sqrt(p) features
                            random_state=42
                        ),
    "ExtraTrees":       ExtraTreesRegressor(
                            n_estimators=100,
                            max_features="sqrt",   # + random split thresholds
                            random_state=42
                        ),
}

print(f"{'Model':<22} {'CV MSE (mean)':>14} {'CV MSE (std)':>13}")
print("-" * 52)
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=5,
                             scoring="neg_mean_squared_error")
    mse = -scores
    print(f"{name:<22} {mse.mean():>14.3f} {mse.std():>13.3f}")

# ⚠️ Gotcha 1: max_features="sqrt" is the RF default for classification,
#    but for regression it's max_features=1.0 (all features) unless you set it.
#    Always set max_features explicitly to control correlation.
#
# ⚠️ Gotcha 2: n_estimators beyond ~200 gives diminishing returns once the
#    reducible (1-rho)*sigma2/B term is near zero.
#    Profile with validation curve to find the knee.
\
"""),
    divider(),

    # ── Section 7: Interview Deep-Dive ───────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy) — Why does averaging multiple models reduce variance?", bold=True)], [
        para(rt("Answer: ", bold=True), rt("If model predictions have the same variance "), eq(r"\sigma^2"), rt(" and pairwise correlation "), eq(r"\rho"), rt(", the variance of their average is "), eq(r"\rho\sigma^2 + (1-\rho)\sigma^2/B"), rt(". When "), eq(r"\rho < 1"), rt(", some variance cancels out via averaging. The lower the correlation, the more cancellation occurs.")),
    ]),
    toggle([rt("Q2 (Easy) — Does averaging reduce bias?", bold=True)], [
        para(rt("Answer: ", bold=True), rt("No. By linearity of expectation, "), eq(r"\mathbb{E}[\bar{X}] = \mu"), rt(" — the ensemble mean equals the individual mean. Bias is unchanged. Averaging is a variance-only tool. This is why boosting (which targets bias) and bagging (which targets variance) are complementary.")),
    ]),
    toggle([rt("Q3 (Medium) — What is the variance floor and what causes it?", bold=True)], [
        para(rt("Answer: ", bold=True), rt("The variance floor is "), eq(r"\rho\sigma^2"), rt(" — the limit of "), eq(r"\operatorname{Var}(\bar{X})"), rt(" as "), eq(r"B \to \infty"), rt(". It arises because correlated errors never cancel: if all models make the same mistake (e.g. all miss the same region of feature space), averaging can't fix it. The floor equals "), eq(r"\rho\sigma^2"), rt(", so reducing "), eq(r"\rho"), rt(" is the only lever to push it lower.")),
        para(rt("Follow-up trap: 'Can you make ρ = 0 in practice?' — Not with a finite dataset. Bootstrap samples share ~63% of observations; trees always share some structure. RF approximates low ρ but can't reach zero.")),
    ]),
    toggle([rt("Q4 (Medium) — How does Random Forest reduce ρ?", bold=True)], [
        para(rt("Answer: ", bold=True), rt("At each split, RF considers only a random subset of "), eq(r"m"), rt(" features ("), eq(r"m = \lfloor\sqrt{p}\rfloor"), rt(" for classification, "), eq(r"m = p/3"), rt(" for regression). When the dominant predictor is absent from the candidate set, the tree must split on a weaker feature, producing a different tree structure than its peers → lower pairwise correlation "), eq(r"\rho"), rt(".")),
        para(rt("Follow-up: 'What's the tradeoff?' — Each tree has higher individual variance "), eq(r"\sigma^2"), rt(" (can't always use the best feature), but the ensemble variance "), eq(r"\rho\sigma^2 + (1-\rho)\sigma^2/B"), rt(" is lower because "), eq(r"\rho"), rt(" dropped more than "), eq(r"\sigma^2"), rt(" rose.")),
    ]),
    toggle([rt("Q5 (Hard) — Derive the variance formula for correlated averages from scratch.", bold=True)], [
        para(rt("PhD Researcher level: ", bold=True), rt("Let "), eq(r"X_1,\ldots,X_B"), rt(" be exchangeable with "), eq(r"\operatorname{Var}(X_i) = \sigma^2"), rt(" and "), eq(r"\operatorname{Cov}(X_i,X_j) = \rho\sigma^2"), rt(" for "), eq(r"i \neq j"), rt(". Then:")),
        para(eq(r"\operatorname{Var}(\bar{X}) = \frac{1}{B^2}\left[B\sigma^2 + B(B-1)\rho\sigma^2\right] = \frac{\sigma^2}{B}+\frac{B-1}{B}\rho\sigma^2 \xrightarrow{B\to\infty} \rho\sigma^2.")),
        para(rt("Note the exchangeability assumption. Without it (varying "), eq(r"\rho_{ij}"), rt(") the formula generalises to "), eq(r"\frac{1}{B^2}\left[\sum_i\sigma_i^2 + \sum_{i\neq j}\rho_{ij}\sigma_i\sigma_j\right]"), rt(".")),
        para(rt("Research Scientist level: ", bold=True), rt("The formula shows two regimes: for small "), eq(r"B"), rt(", the "), eq(r"1/B"), rt(" term dominates and adding models helps a lot; for large "), eq(r"B"), rt(", the floor "), eq(r"\rho\sigma^2"), rt(" dominates and extra models yield diminishing returns. This motivates tuning the number of trees via a validation curve rather than defaulting to 500.")),
    ]),
    toggle([rt("Q6 (Hard) — Why doesn't bagging reduce bias, but boosting does?", bold=True)], [
        para(rt("Answer: ", bold=True), rt("Bagging trains models in parallel on bootstrap resamples of the same data, then averages. Since each model has the same bias (same algorithm, similar data), the bias of the average equals the individual bias. Boosting trains sequentially, each model targeting the residuals of the previous ensemble — this iteratively corrects systematic errors (bias) rather than averaging them away.")),
        para(rt("System design angle: ", bold=True), rt("Use bagging / RF when your base model has low bias but high variance (deep trees). Use boosting (XGBoost, LightGBM) when you need to reduce bias (shallow trees + iteration). In production, gradient boosting often edges out RF on tabular data because it addresses both bias and variance.")),
    ]),
    toggle([rt("Q7 (Hard) — What is the effect of B (number of trees) on generalization error? Where is the knee?", bold=True)], [
        para(rt("Answer: ", bold=True), rt("Generalisation error ≈ "), eq(r"\rho\sigma^2 + (1-\rho)\sigma^2/B + \text{Bias}^2"), rt(". The reducible term decays as "), eq(r"1/B"), rt("; the floor is "), eq(r"\rho\sigma^2"), rt(". The knee occurs where the marginal reduction "), eq(r"\Delta\operatorname{Var} \approx (1-\rho)\sigma^2\cdot(1/B^2)"), rt(" becomes negligible relative to the floor. Empirically, for "), eq(r"\rho \approx 0.3"), rt(", "), eq(r"B \approx 100\text{–}300"), rt(" usually suffices; beyond that, gains are minimal and cost grows linearly with "), eq(r"B"), rt(".")),
    ]),
    callout("🚩", rt("Red Flags: ", bold=True), rt("(1) Claiming averaging reduces bias. (2) Saying 'more trees always help' without mentioning the ρσ² floor. (3) Not knowing that max_features='sqrt' is the RF default for classification but NOT regression. (4) Confusing the variance reduction from averaging with variance reduction from regularisation.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ───────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Method", "Targets Variance?", "Targets Bias?", "Corr. ρ", "Notes"]),
        table_row(["Single tree", "No", "No", "1.0", "Baseline"]),
        table_row(["Bagging", "Yes (modest)", "No", "~0.5", "Bootstrap only, same features"]),
        table_row(["Random Forest", "Yes (strong)", "No", "~0.15", "Bootstrap + feature subsampling"]),
        table_row(["Extra-Trees", "Yes (strongest)", "No", "~0.08", "+ random split thresholds, faster"]),
        table_row(["Gradient Boosting", "Yes (indirect)", "Yes (direct)", "Varies", "Sequential, higher bias reduction"]),
        table_row(["Stacking", "Yes", "Yes (partial)", "Varies", "Meta-learner combines base models"]),
    ),
    heading3("When to Use"),
    bullet(rt("Use Random Forest when base model is deep (low bias, high variance) and you want robust, calibrated predictions with minimal tuning.")),
    bullet(rt("Use Bagging over a single model whenever prediction variance is the main concern and computation budget allows B fits.")),
    bullet(rt("Use Extra-Trees for speed (no sorting at split candidates) when approximate splits are acceptable.")),
    heading3("When NOT to Use"),
    bullet(rt("Do not use bagging to fix underfitting (high bias). Ensemble of underfitting trees is still underfitting.")),
    bullet(rt("Do not add more trees indefinitely without checking a validation curve — beyond the knee it wastes computation.")),
    callout("🎯", rt("Decision guide: ", bold=True), rt("If your single model has high variance → use RF. If it has high bias → use boosting or a stronger base model. If both → consider stacking or XGBoost with tuned depth.")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ───────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/variance_reduction_averaging_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys. Adjust ρ and σ² sliders to see how the variance curve and floor shift in real time.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites (know these first)"),
    bullet(rt("Bias-Variance Tradeoff & Decomposition")),
    bullet(rt("Bootstrap Resampling")),
    bullet(rt("Decision Trees (CART)")),
    bullet(rt("Sample Mean and Variance")),
    heading3("What to Learn Next"),
    bullet(rt("Bagging in Depth")),
    bullet(rt("Random Forests — Feature Importance & OOB Error")),
    bullet(rt("Gradient Boosting (XGBoost, LightGBM)")),
    bullet(rt("Stacking & Blending")),
    bullet(rt("Bias-Variance Tradeoff in Deep Learning")),
    heading3("Key Papers"),
    bullet(rt("Breiman (1996). 'Bagging Predictors.' ML 24(2). ", bold=True), rt("Introduced bagging, showed empirical variance reduction.")),
    bullet(rt("Breiman (2001). 'Random Forests.' ML 45(1). ", bold=True), rt("Proved that ensemble error depends on tree strength and correlation.")),
    bullet(rt("Geurts, Ernst & Wehenkel (2006). 'Extremely Randomised Trees.' ML 63. ", bold=True), rt("Further decorrelation via random thresholds.")),
    bullet(rt("Hastie, Tibshirani & Friedman (2009). ESL §15. ", bold=True), rt("Canonical treatment of bagging and RF with the ρσ² formula.")),
    heading3("Best Resources"),
    bullet(rt("ESL Chapter 15 (free PDF) — most rigorous treatment of the variance formula")),
    bullet(rt("StatQuest 'Random Forests' series (YouTube) — intuitive visual build-up")),
    bullet(rt("Scikit-learn User Guide: Ensemble Methods — practical API details")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Bias-Variance Tradeoff · Bootstrap · Random Forests · Gradient Boosting · Stacking · Model Calibration")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
