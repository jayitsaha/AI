#!/usr/bin/env python3
"""Update Notion page for: F-test, ANOVA (one-way, two-way)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81b7-96b2-cb64593411b3"
ICON = "🟡"  # Intermediate

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/f_test_anova_explainer.html"},
}

EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/f_test_anova_explainer.html"

blocks = [

    # ── Section 1: 30-Second Version ─────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("ANOVA (Analysis of Variance) is a statistical test that checks whether the means of three or more groups are significantly different from each other. The F-test is the specific significance test ANOVA uses — it computes a ratio of between-group variance to within-group variance.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine you're testing three fertilisers on crops. Some yield variation is due to fertiliser differences (signal), and some is just random weather/soil fluctuation (noise). ANOVA is a signal-to-noise ratio: if the between-fertiliser variation is much larger than the random within-plot variation, the fertilisers genuinely differ.")),
    heading3("One-Sentence Summary"),
    para(rt("ANOVA decomposes total variance into between-group and within-group components; the F-ratio of these components, compared to the F-distribution, tests whether group means differ beyond chance.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("F = MS_Between / MS_Within. Under H₀ (all means equal), F ≈ 1. A large F means groups differ far more than random noise predicts → reject H₀.")),
    divider(),

    # ── Section 2: Historical Context ────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Before ANOVA, comparing multiple groups required running multiple t-tests (A vs B, A vs C, B vs C, …). With k groups, that is "), eq(r"\binom{k}{2}"), rt(" tests. Each test inflates the probability of at least one false positive (Type I error) — the family-wise error rate (FWER) grows rapidly: 1 − 0.95³ ≈ 14% just for 3 groups.")),
    heading3("What Came Before"),
    para(rt("The two-sample Student's t-test (1908, William Gosset) could compare only two groups at a time. Researchers who wanted to compare k ≥ 3 groups had no single, principled test.")),
    heading3("The Breakthrough"),
    para(rt("Ronald A. Fisher developed ANOVA in the 1920s (formalised in Statistical Methods for Research Workers, 1925 and The Design of Experiments, 1935). His key insight: decompose the total sum of squares into orthogonal components and use the ratio of variance estimates as a test statistic that follows a known null distribution.")),
    heading3("Key Papers"),
    bullet(rt("Fisher, R. A. (1925). "), rt("Statistical Methods for Research Workers.", italic=True), rt(" — Introduced ANOVA as a unified framework for designed experiments.")),
    bullet(rt("Fisher, R. A. (1935). "), rt("The Design of Experiments.", italic=True), rt(" — Formalised one-way and multi-way factorial designs.")),
    bullet(rt("Snedecor, G. W. (1934). "), rt("Calculation and Interpretation of Analysis of Variance and Covariance.", italic=True), rt(" — Popularised the F-distribution table (named F in Fisher's honour by Snedecor).")),
    heading3("Evolution Timeline"),
    numbered(rt("1908 — Student's t-test: two-sample comparison.")),
    numbered(rt("1925 — Fisher's one-way ANOVA: k ≥ 3 groups, one factor.")),
    numbered(rt("1935 — Factorial (two-way, multi-way) ANOVA: multiple crossed factors.")),
    numbered(rt("1950s — Tukey, Scheffé, Bonferroni post-hoc tests for pairwise comparisons.")),
    numbered(rt("1960s–70s — Repeated-measures ANOVA, mixed-effects models.")),
    numbered(rt("1980s–present — MANOVA, non-parametric alternatives (Kruskal-Wallis), Welch's ANOVA for unequal variances, mixed-effects / hierarchical models that generalise ANOVA.")),
    heading3("Before vs After Comparison"),
    table(4,
        table_row(["Dimension", "Multiple t-tests (Before)", "ANOVA (After)", "Notes"]),
        table_row(["FWER control", "❌ Inflates with k", "✅ Single α-level", "Core motivation"]),
        table_row(["Number of tests", "C(k,2) separate tests", "One omnibus F-test", "—"]),
        table_row(["Interaction effects", "Cannot detect", "Two-way ANOVA detects A×B", "Huge advantage"]),
        table_row(["Post-hoc required?", "Not applicable", "Yes (Tukey/Bonferroni)", "ANOVA is omnibus"]),
        table_row(["Theoretical basis", "t-distribution", "F = χ²/χ² ratio → F-dist", "Elegant unification"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Sum of Squares (SS): ", bold=True), rt("A measure of total variation — the sum of squared deviations from a mean.")),
    bullet(rt("SS_Total: ", bold=True), rt("Total variation in all observations around the grand mean.")),
    bullet(rt("SS_Between (SS_Treatment): ", bold=True), rt("Variation in group means around the grand mean — the 'signal'.")),
    bullet(rt("SS_Within (SS_Error/Residual): ", bold=True), rt("Variation of observations around their own group mean — the 'noise'.")),
    bullet(rt("Mean Square (MS): ", bold=True), rt("SS divided by its degrees of freedom — a variance estimate.")),
    bullet(rt("F-statistic: ", bold=True), rt("The ratio MS_Between / MS_Within. Under H₀ follows an F(df_B, df_W) distribution.")),
    bullet(rt("Grand mean (ȳ..): ", bold=True), rt("The mean of all N observations pooled together.")),
    heading3("The Fundamental Decomposition"),
    para(rt("Every observation can be written as:")),
    equation_block(r"y_{ij} = \mu + \tau_i + \varepsilon_{ij}"),
    para(rt("where "), eq(r"\mu"), rt(" is the overall mean, "), eq(r"\tau_i"), rt(" is the treatment effect for group i ("), eq(r"\sum_i n_i \tau_i = 0"), rt("), and "), eq(r"\varepsilon_{ij} \sim \mathcal{N}(0,\sigma^2)"), rt(" is random error. ANOVA tests H₀: τ₁ = τ₂ = … = τₖ = 0.")),
    heading3("Core Invariant"),
    callout("🔑", rt("SS_Total = SS_Between + SS_Within — always. This orthogonal decomposition is the mathematical heart of ANOVA: variance attributable to group differences plus variance attributable to random noise exhausts all variance in the data.")),
    heading3("Prerequisites"),
    bullet(rt("Normal distribution and sampling distributions")),
    bullet(rt("t-test (two-sample)")),
    bullet(rt("Chi-squared distribution (SS/σ² ~ χ²)")),
    bullet(rt("F-distribution (ratio of chi-squared variables)")),
    bullet(rt("Hypothesis testing framework (H₀, H₁, p-value, Type I/II error)")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ───────────────────────────
    heading2("🏗️ Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("One-Way ANOVA: Step-by-Step Computation"),
    para(rt("Setup: k groups, group i has nᵢ observations yᵢⱼ, total N = Σnᵢ.")),
    heading3("Step 1 — Compute Means"),
    equation_block(r"\bar{y}_{i\cdot} = \frac{1}{n_i}\sum_{j=1}^{n_i} y_{ij}, \qquad \bar{y}_{\cdot\cdot} = \frac{1}{N}\sum_{i=1}^k\sum_{j=1}^{n_i} y_{ij}"),
    heading3("Step 2 — Compute Sums of Squares"),
    equation_block(r"SS_B = \sum_{i=1}^k n_i(\bar{y}_{i\cdot} - \bar{y}_{\cdot\cdot})^2, \quad df_B = k-1"),
    equation_block(r"SS_W = \sum_{i=1}^k\sum_{j=1}^{n_i}(y_{ij} - \bar{y}_{i\cdot})^2, \quad df_W = N-k"),
    equation_block(r"SS_T = \sum_{i=1}^k\sum_{j=1}^{n_i}(y_{ij} - \bar{y}_{\cdot\cdot})^2, \quad df_T = N-1"),
    para(rt("Check: "), eq(r"SS_T = SS_B + SS_W"), rt(". This holds exactly by the algebraic identity for orthogonal projections.")),
    heading3("Step 3 — Mean Squares and F-Statistic"),
    equation_block(r"MS_B = \frac{SS_B}{k-1}, \quad MS_W = \frac{SS_W}{N-k}, \quad F = \frac{MS_B}{MS_W}"),
    heading3("Numerical Trace (3 Groups, n=4 each)"),
    para(rt("Groups: G₁=[2.0, 3.0, 4.0, 3.5], G₂=[5.0, 6.5, 7.0, 5.5], G₃=[1.5, 2.5, 2.0, 2.5]")),
    para(rt("Group means: ȳ₁. = 3.125, ȳ₂. = 6.000, ȳ₃. = 2.125. Grand mean ȳ.. = 3.750.")),
    equation_block(r"SS_B = 4(3.125-3.75)^2 + 4(6.000-3.75)^2 + 4(2.125-3.75)^2 = 1.5625 + 20.25 + 10.5625 = 32.375"),
    equation_block(r"SS_W = [(2-3.125)^2+\cdots+(3.5-3.125)^2] + [\cdots] + [\cdots] = 1.875 + 2.75 + 0.75 = 5.375"),
    equation_block(r"F = \frac{32.375/2}{5.375/9} = \frac{16.188}{0.597} = 27.11 \quad (p = 0.000155)"),
    para(rt("Critical value: F(0.05; 2, 9) = 4.26. Since 27.11 >> 4.26, we reject H₀ with overwhelming evidence.")),
    heading3("Why F Follows the F-Distribution Under H₀"),
    para(rt("Under H₀ and the normality assumption, it can be shown that:")),
    equation_block(r"\frac{SS_B}{\sigma^2} \sim \chi^2(k-1), \qquad \frac{SS_W}{\sigma^2} \sim \chi^2(N-k)"),
    para(rt("and these two quantities are independent (by Cochran's theorem). The ratio of two independent chi-squared variables divided by their degrees of freedom is by definition an F-distributed variable:")),
    equation_block(r"F = \frac{SS_B/(k-1)}{SS_W/(N-k)} = \frac{\chi^2(k-1)/(k-1)}{\chi^2(N-k)/(N-k)} \sim F(k-1,\; N-k)"),
    heading3("Expected Values — Why Large F → Groups Differ"),
    equation_block(r"\mathbb{E}[MS_B] = \sigma^2 + \frac{\sum_i n_i \tau_i^2}{k-1}, \qquad \mathbb{E}[MS_W] = \sigma^2"),
    para(rt("When H₀ is false (some τᵢ ≠ 0), MS_B is inflated by the non-centrality parameter Σnᵢτᵢ²/(k-1) while MS_W remains an unbiased estimate of σ². Their ratio F then exceeds 1 systematically — this is the mathematical engine of the test.")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("Unequal variances (heteroscedasticity): ", bold=True), rt("F-test is non-robust. Use Welch's ANOVA (unequal-variance version) or Brown-Forsythe test.")),
    bullet(rt("Non-normal data with small n: ", bold=True), rt("Use Kruskal-Wallis H-test (non-parametric one-way ANOVA).")),
    bullet(rt("Unbalanced designs: ", bold=True), rt("Two-way ANOVA SS are not orthogonal. Use Type III SS (partial) rather than Type I (sequential).")),
    bullet(rt("ANOVA is omnibus: ", bold=True), rt("A significant p-value tells you at least one group differs — not which ones. Always follow with post-hoc tests.")),
    callout("⚠️", rt("Design decision: ", bold=True), rt("Why MS_Within (not MS_Total) in the denominator? MS_Within estimates σ² free of any group effects — it's a pure noise benchmark. MS_Between includes σ² plus any treatment signal, so their ratio cleanly isolates the signal-to-noise ratio.")),
    divider(),

    # ── Section 5: The Math Behind It ────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Linear Model Formulation"),
    para(rt("One-way ANOVA is a special case of the general linear model. Define the "), eq(r"N \times k"), rt(" design matrix X (indicator/dummy coding). The model is:")),
    equation_block(r"\mathbf{y} = X\boldsymbol{\mu} + \boldsymbol{\varepsilon}, \qquad \boldsymbol{\varepsilon} \sim \mathcal{N}(\mathbf{0},\, \sigma^2 I_N)"),
    para(rt("The OLS estimator gives "), eq(r"\hat{\boldsymbol{\mu}} = (X^\top X)^{-1} X^\top \mathbf{y}"), rt(" — which reduces to the group sample means.")),
    heading3("Cochran's Theorem (Formal Basis)"),
    para(rt("If "), eq(r"\mathbf{y} \sim \mathcal{N}(\boldsymbol{\mu},\, \sigma^2 I)"), rt(" and "), eq(r"\mathbf{y}^\top \mathbf{y} = Q_1 + Q_2 + \cdots + Q_k"), rt(" is a decomposition of the total SS into quadratic forms with ranks r₁, r₂, …, rₖ summing to N, then the Qᵢ/σ² are independent chi-squared variables with their respective degrees of freedom.")),
    para(rt("For ANOVA: "), eq(r"SS_T = SS_B + SS_W"), rt(" with ranks (k−1) and (N−k) summing to N−1 (one degree of freedom is lost to estimating the grand mean). By Cochran's theorem, SS_B/σ² and SS_W/σ² are independent "), eq(r"\chi^2"), rt(" variates.")),
    heading3("F-Distribution PDF"),
    equation_block(r"f(x;\, d_1,d_2) = \frac{\sqrt{\dfrac{(d_1 x)^{d_1}\, d_2^{d_2}}{(d_1 x + d_2)^{d_1+d_2}}}}{x\, B(d_1/2,\, d_2/2)}, \quad x > 0"),
    para(rt("where "), eq(r"B(a,b) = \Gamma(a)\Gamma(b)/\Gamma(a+b)"), rt(" is the beta function. The p-value for the test is "), eq(r"P(F_{d_1,d_2} \geq F_{\text{obs}})"), rt(", the upper tail probability.")),
    heading3("Effect Size: η² (Eta-Squared)"),
    equation_block(r"\eta^2 = \frac{SS_B}{SS_T} \in [0,1]"),
    para(rt("Interpretation: η² = 0.86 (as in our example) means 86% of the total variance is explained by group membership. Conventional benchmarks: η² ≈ 0.01 (small), 0.06 (medium), 0.14 (large).")),
    heading3("Power Analysis"),
    para(rt("The non-central F-distribution governs power. The non-centrality parameter is:")),
    equation_block(r"\lambda = \frac{\sum_{i=1}^k n_i \tau_i^2}{\sigma^2}"),
    para(rt("Power = P(F_{k-1,\,N-k,\,\lambda} > F_{\text{crit}}). Increasing n or effect size (larger τᵢ) or reducing σ² all increase power.")),
    heading3("Two-Way ANOVA Decomposition"),
    para(rt("With factors A (a levels) and B (b levels), n replicates per cell:")),
    equation_block(r"SS_T = SS_A + SS_B + SS_{AB} + SS_W"),
    equation_block(r"SS_A = bn\sum_{i=1}^a(\bar{y}_{i\cdot\cdot} - \bar{y}_{\cdot\cdot\cdot})^2, \quad df_A = a-1"),
    equation_block(r"SS_B = an\sum_{j=1}^b(\bar{y}_{\cdot j\cdot} - \bar{y}_{\cdot\cdot\cdot})^2, \quad df_B = b-1"),
    equation_block(r"SS_{AB} = n\sum_{i,j}(\bar{y}_{ij\cdot} - \bar{y}_{i\cdot\cdot} - \bar{y}_{\cdot j\cdot} + \bar{y}_{\cdot\cdot\cdot})^2, \quad df_{AB}=(a-1)(b-1)"),
    callout("⚠️", rt("Warning: ", bold=True), rt("In unbalanced two-way designs, SS_A + SS_B + SS_AB ≠ SS_T. Use Type III (partial) sums of squares (default in SAS PROC GLM, R's drop1(), Python statsmodels). Type I SS are order-dependent and misleading.")),
    divider(),

    # ── Section 6: Code Implementation ───────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — One-Way ANOVA from Scratch (NumPy)"),
    code_block("python", """\
import numpy as np
from scipy import stats

def one_way_anova(*groups):
    \"\"\"One-way ANOVA from scratch.

    Args:
        *groups: arrays of observations for each group
    Returns:
        dict with F, p_value, SS_between, SS_within, df_between, df_within, eta_sq
    \"\"\"
    k = len(groups)                          # number of groups
    n_i = [len(g) for g in groups]           # group sizes
    N = sum(n_i)                             # total observations

    group_means = [np.mean(g) for g in groups]
    grand_mean  = np.mean(np.concatenate(groups))

    # Sum of Squares
    SS_B = sum(n_i[i] * (group_means[i] - grand_mean)**2 for i in range(k))
    SS_W = sum(np.sum((groups[i] - group_means[i])**2) for i in range(k))
    SS_T = SS_B + SS_W                       # partition: always holds exactly

    df_B = k - 1                             # between-group degrees of freedom
    df_W = N - k                             # within-group degrees of freedom

    MS_B = SS_B / df_B                       # mean square between
    MS_W = SS_W / df_W                       # mean square within (unbiased σ² estimator)

    F = MS_B / MS_W                          # F-statistic
    p = stats.f.sf(F, df_B, df_W)           # right-tail p-value from F distribution

    eta_sq = SS_B / SS_T                     # effect size

    return {
        "F": F, "p_value": p,
        "SS_between": SS_B, "SS_within": SS_W,
        "df_between": df_B, "df_within": df_W,
        "MS_between": MS_B, "MS_within": MS_W,
        "eta_sq": eta_sq,
    }

# Example
g1 = np.array([2.0, 3.0, 4.0, 3.5])
g2 = np.array([5.0, 6.5, 7.0, 5.5])
g3 = np.array([1.5, 2.5, 2.0, 2.5])

result = one_way_anova(g1, g2, g3)
print(f"F = {result['F']:.4f}")             # 27.1047
print(f"p = {result['p_value']:.6f}")       # 0.000155
print(f"η² = {result['eta_sq']:.4f}")       # 0.8577
# Verify with scipy
F_v, p_v = stats.f_oneway(g1, g2, g3)
print(f"scipy check: F={F_v:.4f}, p={p_v:.6f}")  # matches
"""),
    heading3("6b — Two-Way ANOVA (Production: statsmodels)"),
    code_block("python", """\
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Create a tidy DataFrame
data = pd.DataFrame({
    'weight_loss': [3.2, 2.8, 3.0,  # Low-fat, No exercise
                    5.5, 5.8, 5.3,  # Low-fat, Daily exercise
                    4.0, 4.5, 4.2,  # High-fat, No exercise
                    4.8, 5.2, 5.0], # High-fat, Daily exercise
    'diet':     ['Low']*3 + ['Low']*3 + ['High']*3 + ['High']*3,
    'exercise': ['None']*3 + ['Daily']*3 + ['None']*3 + ['Daily']*3,
})

# Fit two-way ANOVA model (C() for categorical, C(diet):C(exercise) for interaction)
model = ols('weight_loss ~ C(diet) + C(exercise) + C(diet):C(exercise)', data=data).fit()

# Type III SS ANOVA table (order-independent — use this for unbalanced designs)
anova_table = sm.stats.anova_lm(model, typ=3)
print(anova_table)
# Output:
#                    sum_sq  df          F    PR(>F)
# Intercept        ...
# C(diet)          0.3675    1    7.1129   0.0285   <- Diet: significant
# C(exercise)      8.1675    1  158.0806   <0.001   <- Exercise: very significant
# C(diet):C(exercise) 2.3408  1   45.3065  0.0001  <- Interaction: significant!
# Residual         0.4133    8

# ⚠️ Gotcha: significant interaction means main effects cannot be interpreted
# in isolation. Plot interaction plot first!
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot
interaction_plot(data['exercise'], data['diet'], data['weight_loss'],
                 colors=['blue','green'], markers=['D','^'])
plt.title('Interaction plot: Exercise × Diet')
plt.show()
"""),
    heading3("6c — Post-hoc Tests (Tukey HSD)"),
    code_block("python", """\
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import numpy as np

# After a significant one-way ANOVA, identify which pairs differ
g1 = np.array([2.0, 3.0, 4.0, 3.5])
g2 = np.array([5.0, 6.5, 7.0, 5.5])
g3 = np.array([1.5, 2.5, 2.0, 2.5])

data   = np.concatenate([g1, g2, g3])
labels = ['G1']*4 + ['G2']*4 + ['G3']*4

tukey = pairwise_tukeyhsd(data, labels, alpha=0.05)
print(tukey)
# All three pairs will be significant (G1 vs G2, G1 vs G3, G2 vs G3)
# Tukey controls family-wise error rate at 0.05

# ⚠️ Gotcha: run post-hoc tests ONLY after a significant omnibus ANOVA.
# Running them on non-significant ANOVA inflates Type I error even with
# correction because the overall result already told you H₀ is plausible.
"""),
    divider(),

    # ── Section 7: Interview Deep-Dive ───────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is ANOVA and when do you use it?", bold=True)], [
        para(rt("ANOVA tests whether the means of three or more independent groups differ significantly. Use it when you have a continuous outcome and one or more categorical predictors (factors) and want a single omnibus test without inflating the Type I error rate from multiple pairwise t-tests.")),
        para(rt('Follow-up trap: "Why not just run multiple t-tests?" -> The FWER balloons: with k=5 groups, C(5,2)=10 t-tests at alpha=0.05 each gives FWER = 1-0.95^10 ~ 40%. ANOVA keeps it at 5%.')),
    ]),
    toggle([rt("Q2 (Easy-Medium): What are the assumptions of ANOVA?", bold=True)], [
        numbered(rt("Independence: observations within and across groups are independent.")),
        numbered(rt("Normality: residuals within each group are ~Normal. Robust for n > 30 by CLT.")),
        numbered(rt("Homoscedasticity (equal variances): σ₁² = σ₂² = … = σₖ². Test with Levene's test. Violation → Welch's ANOVA.")),
        para(rt("If data is ordinal or heavily skewed, use Kruskal-Wallis (non-parametric one-way ANOVA).")),
    ]),
    toggle([rt("Q3 (Medium): Walk me through the mathematics of a one-way ANOVA F-test.", bold=True)], [
        para(rt("The total SS is partitioned as SS_T = SS_B + SS_W. Mean squares are MS_B = SS_B/(k−1) and MS_W = SS_W/(N−k). Under H₀, both are unbiased estimates of σ², so their ratio F ~ F(k−1, N−k). Under H₁, E[MS_B] = σ² + Σnᵢτᵢ²/(k−1) > σ², so F is inflated. The p-value is the right-tail probability of F(k−1, N−k) exceeding the observed F.")),
    ]),
    toggle([rt("Q4 (Medium-Hard): What is the difference between Type I, II, and III Sums of Squares?", bold=True)], [
        para(rt("Type I (sequential): SS assigned in the order terms enter the model. Order-dependent — misleading in unbalanced designs.")),
        para(rt("Type II: SS for each effect controlling for all other main effects (not interactions). Appropriate when no interaction.")),
        para(rt("Type III (partial): SS for each effect controlling for ALL other effects including interactions. Order-independent. The standard for unbalanced designs (default in SAS, R's drop1(), statsmodels typ=3).")),
        callout("⚠️", rt("Red flag: ", bold=True), rt("Using Type I SS on an unbalanced two-way design and reporting main effects is a common analysis error that reviewers will catch.")),
    ]),
    toggle([rt("Q5 (Hard): How does ANOVA relate to regression?", bold=True)], [
        para(rt("ANOVA is a special case of the General Linear Model (GLM). A one-way ANOVA with k groups is equivalent to OLS regression with k−1 dummy variables. The F-statistic for overall model significance in regression is the same F as in ANOVA. ANCOVA (Analysis of Covariance) extends ANOVA by adding continuous covariates as regressors — again just a GLM.")),
        para(rt("Explain to PhD researcher: The F-test in one-way ANOVA tests the null that H₀: Cβ = 0 for the contrast matrix C that spans the group-effect subspace. This generalises to F-tests for any linear hypothesis in a GLM via the Wald statistic (Cβ̂)ᵀ(C(XᵀX)⁻¹Cᵀ)⁻¹(Cβ̂)/rankC, which follows F(rankC, N−p) under H₀.")),
    ]),
    toggle([rt("Q6 (Hard): What is the interaction effect in two-way ANOVA and why does it matter?", bold=True)], [
        para(rt("An interaction (A×B) exists when the effect of factor A on the outcome depends on which level of factor B is present. Visually: interaction plot lines cross or are non-parallel.")),
        para(rt("If the interaction is significant, the main effects of A and B cannot be interpreted in isolation — you must examine cell means. Reporting that 'Diet A is better' ignores that this may only be true for Exercise=Daily.")),
        para(rt("Formally: the interaction term in the model is (αβ)ᵢⱼ where αᵢ is the effect of A level i and βⱼ is the effect of B level j. Non-zero (αβ)ᵢⱼ means the cell mean deviates from the additive prediction α+β.")),
    ]),
    divider(),

    # ── Section 8: Comparison & Trade-offs ───────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Method", "Groups", "Factors", "Parametric?", "When to use"]),
        table_row(["One-Way ANOVA", "k ≥ 3", "1", "Yes", "Equal variance, normality, single factor"]),
        table_row(["Two-Way ANOVA", "k × l", "2", "Yes", "Two crossed factors, test interaction"]),
        table_row(["Welch's ANOVA", "k ≥ 3", "1", "Yes", "Unequal group variances"]),
        table_row(["Kruskal-Wallis", "k ≥ 3", "1", "No", "Non-normal data, ordinal outcome"]),
        table_row(["Repeated-Measures ANOVA", "k ≥ 2", "1+", "Yes", "Same subjects measured at each level"]),
        table_row(["MANOVA", "k ≥ 3", "1+", "Yes", "Multiple continuous outcome variables simultaneously"]),
        table_row(["Linear Mixed Model (LMM)", "any", "any", "Yes", "Hierarchical data, missing values, unbalanced"]),
    ),
    callout("🎯", rt("Decision guide: ", bold=True), rt("Use ANOVA when assumptions hold, factors are categorical, and outcome is continuous. Switch to Welch's if Levene's test is significant. Switch to Kruskal-Wallis if data is heavily non-normal and n is small. Use LMM for nested/repeated data or many missing values.")),
    heading3("Advantages"),
    bullet(rt("Controls FWER — single α-level for k groups simultaneously.")),
    bullet(rt("Two-way ANOVA detects interaction effects that pairwise tests cannot.")),
    bullet(rt("Directly linked to GLM — interpretable via regression framework.")),
    bullet(rt("Well-understood null distribution (F) with exact critical values.")),
    heading3("Disadvantages"),
    bullet(rt("Omnibus test: significant result does not say which groups differ → need post-hoc.")),
    bullet(rt("Assumes equal variances and normality (can be violated).")),
    bullet(rt("Unbalanced two-way ANOVA requires careful choice of SS type.")),
    bullet(rt("Cannot handle crossed random effects without moving to mixed models.")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ───────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the ANOVA variance decomposition — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("3.1 Probability Fundamentals")),
    bullet(rt("3.3 Common Distributions (Normal, F, Chi-Squared)")),
    bullet(rt("3.7 Hypothesis Testing (t-test, p-values, Type I/II error)")),
    heading3("What to Learn Next"),
    bullet(rt("3.9 ANCOVA (Analysis of Covariance) — add continuous covariates")),
    bullet(rt("MANOVA — multivariate extension")),
    bullet(rt("Linear Mixed-Effects Models — hierarchical / repeated-measures")),
    bullet(rt("3.6 Regression Analysis — ANOVA as a special case of GLM")),
    heading3("Key Papers & Resources"),
    bullet(rt("Fisher, R. A. (1925). Statistical Methods for Research Workers — original ANOVA framework.")),
    bullet(rt("Scheffe, H. (1959). The Analysis of Variance — definitive mathematical treatment.")),
    bullet(rt("Levene, H. (1960). Robust tests for equality of variances — Levene's test reference.")),
    bullet(rt("Tukey, J. W. (1953). The problem of multiple comparisons — Tukey HSD origin.")),
    bullet(rt("Best textbooks: Kutner et al. Applied Linear Statistical Models (Ch. 16–19); Montgomery Design and Analysis of Experiments.")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("t-test, chi-squared test, F-distribution, regression (GLM), MANOVA, mixed models, Bayesian ANOVA (using credible intervals instead of p-values).")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
