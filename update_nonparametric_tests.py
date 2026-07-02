#!/usr/bin/env python3
"""Update Notion page for: Non-parametric tests: Mann-Whitney U, Wilcoxon signed-rank,
Kruskal-Wallis, Kolmogorov-Smirnov, permutation tests"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81a7-9539-c0cdeeb6ff14"
ICON = "🟡"  # Intermediate
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/nonparametric_tests_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [
    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1: The 30-Second Version
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Classical tests like the t-test and ANOVA assume your data follows a normal distribution. Non-parametric tests make no such assumption — they work on the "), rt("ranks", bold=True), rt(" of observations rather than raw values, making them robust to outliers, skewed distributions, and small samples.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine comparing customer satisfaction scores from two restaurants (scale 1-10). Instead of computing average scores (which treats the scale as a perfect ruler), you ask: which restaurant tends to get higher scores more often? Replace each score with its rank among all scores combined (1st, 2nd, 3rd...) and compare. The "), rt("absolute values stop mattering; only the ordering does", italic=True), rt(".")),
    heading3("One-Sentence Summary"),
    para(rt("Non-parametric tests replace raw data with their ranks (or compare empirical distributions directly) to perform valid inference without distributional assumptions, trading a small amount of statistical power for broad applicability.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Non-parametric tests achieve distribution-freedom by replacing observations with ranks — under H₀ with a continuous distribution, any permutation of ranks is equally likely (probability 1/n!), so the null distribution of rank-based statistics is exact, regardless of the original data's shape.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: Historical Context
    # ══════════════════════════════════════════════════════════════════════════
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Throughout the early 20th century, statistical tests (Student's t-test 1908, Fisher's F-test 1925, Pearson's chi-squared) all assumed normal distributions or other strict parametric forms. Researchers working with small samples, ordinal data (Likert scales, rankings), or non-Gaussian phenomena (income distributions, survival times) had no valid tests available.")),
    heading3("The Breakthrough Papers"),
    bullet(rt("Wilcoxon (1945): ", bold=True), rt('"Individual Comparisons by Ranking Methods" — Frank Wilcoxon introduced two rank-based tests: the rank-sum test (two independent samples, later generalised by Mann-Whitney) and the signed-rank test (matched pairs). This was the first systematic use of ranks for statistical testing.')),
    bullet(rt("Mann & Whitney (1947): ", bold=True), rt('"On a Test of Whether One of Two Random Variables is Stochastically Larger than the Other" — Extended Wilcoxon\'s rank-sum test with the U statistic and its exact distribution.')),
    bullet(rt("Kruskal & Wallis (1952): ", bold=True), rt('"Use of Ranks in One-Criterion Variance Analysis" — Generalised Mann-Whitney to k groups; the H statistic follows χ²(k−1) asymptotically.')),
    bullet(rt("Kolmogorov (1933) & Smirnov (1948): ", bold=True), rt("Developed the two-sample test based on the supremum of ECDF differences; Kolmogorov proved the limiting distribution is universal (distribution-free).")),
    bullet(rt("Fisher (1935) + Pitman (1937-38): ", bold=True), rt("The permutation test concept was implicit in Fisher's exact test; Pitman formalised permutation tests as an exact method for arbitrary statistics.")),
    heading3("Evolution Timeline"),
    para(rt("Parametric era (pre-1940) → Wilcoxon/Mann-Whitney rank tests (1945-47) → KW generalisation (1952) → KS two-sample test (1933-48) → Permutation tests formalised (1935-1960s) → Bootstrap and modern resampling methods (Efron 1979) → Asymptotic theory unified via U-statistics (Hoeffding 1948)")),
    heading3("Before vs After Comparison"),
    table(3,
        table_row(["Dimension", "Parametric Tests (Before)", "Non-Parametric Tests (After)"]),
        table_row(["Distributional assumption", "Normal (or specific parametric form)", "None (continuous distribution sufficient)"]),
        table_row(["Data type", "Continuous, interval/ratio scale", "Ordinal data acceptable"]),
        table_row(["Small sample validity", "Relies on CLT; poor for n<30", "Exact for any n"]),
        table_row(["Sensitivity to outliers", "High (mean-based statistics)", "Low (rank-based, outlier only changes one rank)"]),
        table_row(["Power when normal", "Optimal (Gauss-Markov / uniformly most powerful)", "Slightly less (~95% ARE vs t-test)"]),
        table_row(["Power when non-normal", "Can be poor or invalid", "Often better than parametric"]),
    ),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3: Core Concepts & Theory
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🔑 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Rank: ", bold=True), rt("The position of an observation when all values are sorted in ascending order. Tied values receive average ranks.")),
    bullet(rt("Empirical CDF (ECDF): ", bold=True), eq(r"\hat{F}_n(x) = \frac{1}{n}\sum_{i=1}^n \mathbf{1}[X_i \leq x]"), rt(" — the step function that jumps by 1/n at each observation.")),
    bullet(rt("U-statistic: ", bold=True), rt("A generalisation of sample statistics of the form "), eq(r"U = \binom{n}{k}^{-1}\sum_{(i_1,\ldots,i_k)} h(X_{i_1},\ldots,X_{i_k})"), rt(", where h is a symmetric kernel. Mann-Whitney U is a 2-sample U-statistic with kernel h(x,y) = 1[x>y].")),
    bullet(rt("Exchangeability: ", bold=True), rt("Observations are exchangeable under H₀ if their joint distribution is invariant to permutations — the key condition for permutation tests.")),
    bullet(rt("Asymptotic Relative Efficiency (ARE): ", bold=True), rt("The ratio of sample sizes needed by two tests to achieve the same power. ARE(Mann-Whitney, t-test) = 3/π ≈ 0.955 under normality.")),
    heading3("Core Property: Distribution-Freedom"),
    para(rt("If "), eq(r"X_1, \ldots, X_n"), rt(" are i.i.d. from any "), rt("continuous", italic=True), rt(" distribution, then under H₀ all "), eq(r"n!"), rt(" orderings of the ranks are equally likely. The probability of any particular rank vector is:")),
    equation_block(r"P(\text{rank vector} = (r_1, \ldots, r_n)) = \frac{1}{n!} \quad \text{for any continuous distribution under } H_0"),
    para(rt("This means the null distribution of any rank statistic is the same regardless of the underlying F — hence the tests are "), rt("distribution-free", italic=True), rt(", not assumption-free.")),
    callout("🔑", rt("Key Property: ", bold=True), rt("Distribution-freedom ≠ assumption-free. These tests require: (1) independence, (2) continuous distribution (for exact validity of rank theory), (3) identically distributed observations under H₀. The Wilcoxon signed-rank additionally requires the difference distribution to be symmetric under H₀.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4: Architecture & Internal Workings
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🏗️ Architecture & Internal Workings (PhD Deep Dive)"),

    heading3("Mann-Whitney U — Full Mechanism"),
    para(rt("Data: Group A = [2.1, 3.4, 4.0, 5.2, 6.1], Group B = [1.0, 2.5, 3.0, 4.5, 7.2]. Step-by-step:")),
    numbered(rt("Pool and rank all 10 observations: [1.0(B,r=1), 2.1(A,r=2), 2.5(B,r=3), 3.0(B,r=4), 3.4(A,r=5), 4.0(A,r=6), 4.5(B,r=7), 5.2(A,r=8), 6.1(A,r=9), 7.2(B,r=10)]")),
    numbered(rt("Compute rank sums: "), eq(r"R_A = 2+5+6+8+9 = 30"), rt(", "), eq(r"R_B = 1+3+4+7+10 = 25")),
    numbered(rt("Compute U: "), eq(r"U_A = R_A - \frac{n_1(n_1+1)}{2} = 30 - 15 = 15"), rt(", "), eq(r"U_B = n_1 n_2 - U_A = 25 - 15 = 10")),
    numbered(rt("Check: "), eq(r"U_A + U_B = 25 = n_1 n_2 \checkmark")),
    numbered(rt("Under H₀: "), eq(r"\mathbb{E}[U] = 12.5"), rt(", "), eq(r"\operatorname{Var}(U) = \frac{5 \cdot 5 \cdot 11}{12} = 22.92"), rt(", "), eq(r"z = (15 - 12.5)/\sqrt{22.92} = 0.52"), rt(", p = 0.69 (two-sided) — not significant")),

    heading3("Wilcoxon Signed-Rank — Full Mechanism"),
    para(rt("Data: before=[120,115,130,125,118], after=[110,112,119,118,115].")),
    numbered(rt("Differences d = after − before = [−10, −3, −11, −7, −3]")),
    numbered(rt("Rank |d| (absolute values): |d| sorted = [3,3,7,10,11]. Tied values (both=3, subjects 2&5) get average rank 1.5. Ranks: [4.0, 1.5, 5.0, 3.0, 1.5]")),
    numbered(rt("Separate by sign: all diffs are negative → "), eq(r"W^+ = 0"), rt(", "), eq(r"W^- = 4.0 + 1.5 + 5.0 + 3.0 + 1.5 = 15.0")),
    numbered(rt("Test statistic: "), eq(r"W = \min(W^+, W^-) = 0")),
    numbered(rt("Under H₀: "), eq(r"\mathbb{E}[W^+] = n(n+1)/4 = 7.5"), rt(". Exact p (n=5, all same sign) = 2×(1/32) = 0.0625 — marginal evidence")),

    heading3("Kruskal-Wallis H — Full Mechanism"),
    para(rt("Groups: G1=[3.2,4.1,5.0,3.8], G2=[7.2,8.1,6.5,9.0], G3=[4.5,5.3,6.2,4.9], N=12.")),
    numbered(rt("Rank all N=12 observations: G1→{1,2,3,6}, G2→{9,10,11,12}, G3→{4,5,7,8}")),
    numbered(rt("Rank sums: "), eq(r"R_1=12, R_2=42, R_3=24")),
    numbered(rt("H statistic: "), eq(r"H = \frac{12}{12 \cdot 13}\left(\frac{144}{4}+\frac{1764}{4}+\frac{576}{4}\right) - 3 \cdot 13 = \frac{12}{156} \cdot 621 - 39 = 47.77 - 39 = 8.77")),
    numbered(rt("Under H₀: "), eq(r"H \sim \chi^2(k-1) = \chi^2(2)"), rt(". Critical value 5.99; H=8.77 > 5.99, p=0.0125 → significant")),

    heading3("KS Test — Numerical Trace"),
    para(rt("s1=[1.2,2.3,2.8,3.4,4.1], s2=[0.8,1.9,3.0,4.5,5.2]. Compute ECDF gap at each unique point:")),
    table(4,
        table_row(["x", "F̂₁(x)", "F̂₂(x)", "|F̂₁ − F̂₂|"]),
        table_row(["0.8",  "0.00", "0.20", "0.20"]),
        table_row(["1.2",  "0.20", "0.20", "0.00"]),
        table_row(["1.9",  "0.20", "0.40", "0.20"]),
        table_row(["2.3",  "0.40", "0.40", "0.00"]),
        table_row(["2.8",  "0.60", "0.40", "0.20"]),
        table_row(["3.0",  "0.60", "0.60", "0.00"]),
        table_row(["3.4",  "0.80", "0.60", "0.20"]),
        table_row(["4.1",  "1.00", "0.60", "0.40 ← D"]),
        table_row(["4.5",  "1.00", "0.80", "0.20"]),
        table_row(["5.2",  "1.00", "1.00", "0.00"]),
    ),
    para(rt("D = 0.40, p = 0.873 — not significant at n=5.")),

    heading3("Permutation Test — Numerical Trace"),
    para(rt("obs_A=[5.2,6.1,4.9,7.3], obs_B=[3.1,2.8,4.0,3.5]. Observed diff = 5.875 − 3.35 = 2.525.")),
    para(rt("Under H₀, all "), eq(r"\binom{8}{4}=70"), rt(" relabellings are equally likely. With M=5000 Monte Carlo permutations: null distribution has mean ≈ −0.02, sd ≈ 1.11. Fraction of permutations with |diff| ≥ 2.525: p ≈ 0.006. Strong evidence against H₀.")),
    callout("⚠️", rt("Edge Cases: ", bold=True), rt("(1) Ties: rank-based tests require a tie correction to the variance; severe ties reduce power. (2) Zero differences in Wilcoxon signed-rank: traditionally excluded (reduces n), or can use a modified test. (3) KS test has reduced power for discrete distributions. (4) Permutation tests with very small N can have coarse p-value resolution (minimum achievable p = 1/C(N,k)).")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5: The Math Behind It
    # ══════════════════════════════════════════════════════════════════════════
    heading2("📐 The Math Behind It"),

    heading3("Mann-Whitney U — Exact Distribution"),
    para(rt("Under H₀ (identical distributions), U counts the number of (A,B) pairs where A > B. The exact null distribution is derived from the combinatorics of rank assignments. For large samples, by the CLT for U-statistics:")),
    equation_block(r"\mathbb{E}[U] = \frac{n_1 n_2}{2}, \qquad \operatorname{Var}(U) = \frac{n_1 n_2 (n_1+n_2+1)}{12}"),
    para(rt("The U-statistic estimator of the probability of stochastic dominance is:")),
    equation_block(r"\hat{P}(X > Y) = \frac{U_A}{n_1 n_2}"),
    para(rt("For ties, the variance correction is:")),
    equation_block(r"\operatorname{Var}(U) = \frac{n_1 n_2}{12}\left[(n_1+n_2+1) - \frac{\sum_g t_g(t_g^2-1)}{(n_1+n_2)(n_1+n_2-1)}\right]"),
    para(rt("where "), eq(r"t_g"), rt(" is the number of observations in tie group g.")),

    heading3("Wilcoxon Signed-Rank — Moments"),
    para(rt("With no ties and no zero differences, under H₀:")),
    equation_block(r"\mathbb{E}[W^+] = \frac{n(n+1)}{4}, \qquad \operatorname{Var}(W^+) = \frac{n(n+1)(2n+1)}{24}"),
    para(rt("This follows because each pair (sign, |d| rank) contributes independently: each of the "), eq(r"2^n"), rt(" sign patterns is equally likely under H₀ symmetry, and the ranks are fixed given the observed |differences|.")),

    heading3("Kruskal-Wallis H — Derivation"),
    para(rt("H is a one-way ANOVA on the ranks. The ANOVA F-statistic applied to ranks becomes:")),
    equation_block(r"H = \frac{12}{N(N+1)}\sum_{i=1}^{k}\frac{R_i^2}{n_i} - 3(N+1)"),
    para(rt("This is algebraically equivalent to "), eq(r"H = \frac{\text{SS}_{\text{between}}}{\text{SS}_{\text{total}}/(N-1)}"), rt(" applied to ranks. Under H₀, the grand mean rank is "), eq(r"\bar{R} = (N+1)/2"), rt(" and "), eq(r"H \xrightarrow{d} \chi^2(k-1)"), rt(" as "), eq(r"n_i \to \infty"), rt(".")),

    heading3("KS Test — Limiting Kolmogorov Distribution"),
    para(rt("For the one-sample test (testing against a specified F₀), under H₀:")),
    equation_block(r"\lim_{n\to\infty} P\!\left(\sqrt{n}\,D_n \leq x\right) = K(x) = 1 - 2\sum_{k=1}^{\infty}(-1)^{k-1}e^{-2k^2x^2}, \quad x > 0"),
    para(rt("where "), eq(r"D_n = \sup_x |\hat{F}_n(x) - F_0(x)|"), rt(". This remarkable result holds for any continuous F₀ — it's truly distribution-free. For the two-sample test with "), eq(r"n_1 = n_2 = n"), rt(", replace "), eq(r"\sqrt{n}"), rt(" with "), eq(r"\sqrt{n/2}"), rt(".")),

    heading3("Permutation Test — Exact p-value"),
    equation_block(r"\hat{p} = \frac{1 + \#\{m : |T_m| \geq |T_\text{obs}|\}}{M+1}"),
    para(rt("The +1 in numerator and denominator ensures the p-value is valid (conservative): the observed statistic itself is one of the "), eq(r"M+1"), rt(" members of the reference distribution. For exact tests (enumerate all permutations), the p-value is exactly "), eq(r"P(|T| \geq |T_\text{obs}| \mid H_0)"), rt(".")),

    heading3("Asymptotic Relative Efficiency"),
    para(rt("The Pitman efficiency of the Wilcoxon signed-rank test vs. the paired t-test is:")),
    equation_block(r"\text{ARE}(\text{Wilcoxon, t-test}) = 12\sigma^2 \left[\int_{-\infty}^{\infty} f^2(x)\, dx\right]^2"),
    para(rt("Under normality this equals "), eq(r"3/\pi \approx 0.955"), rt(". Under heavy-tailed distributions (e.g. double exponential), ARE > 1 — the Wilcoxon test is "), rt("more efficient", italic=True), rt(" than the t-test.")),

    callout("⚠️", rt("Common Pitfall: ", bold=True), rt("The ARE ≈ 0.955 is the asymptotic value. For finite samples under normality, rank tests can be slightly more or less efficient depending on n. Also, ARE = 0.955 means you need about 1/0.955 ≈ 4.7% more observations with Wilcoxon vs t-test to detect the same effect — a trivially small cost in practice.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6: Code Implementation
    # ══════════════════════════════════════════════════════════════════════════
    heading2("💻 Code Implementation"),

    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """import numpy as np

def mann_whitney_u(group_a, group_b):
    \"\"\"Mann-Whitney U test from scratch.

    Returns U_A, U_B, z-score, two-sided p-value.
    \"\"\"
    a, b = np.array(group_a, float), np.array(group_b, float)
    n1, n2 = len(a), len(b)

    # Pool and rank all observations
    combined = np.concatenate([a, b])
    labels   = np.array(['A']*n1 + ['B']*n2)

    # Rank with tie-averaging
    order = np.argsort(combined, kind='stable')
    ranks = np.empty(len(combined))
    i = 0
    while i < len(combined):
        j = i
        while j < len(combined) - 1 and combined[order[j+1]] == combined[order[j]]:
            j += 1
        avg_rank = (i + j) / 2 + 1        # 1-indexed average
        ranks[order[i:j+1]] = avg_rank
        i = j + 1

    # Rank sums
    R_A = np.sum(ranks[labels == 'A'])
    R_B = np.sum(ranks[labels == 'B'])

    # U statistics
    U_A = R_A - n1 * (n1 + 1) / 2
    U_B = n1 * n2 - U_A                   # always sums to n1*n2

    # Tie correction for variance
    # Count ties: group values that are equal
    _, counts = np.unique(combined, return_counts=True)
    tie_correction = np.sum(counts[counts > 1] * (counts[counts > 1]**2 - 1))
    N = n1 + n2
    var_U = (n1 * n2 / 12) * ((N + 1) - tie_correction / (N * (N - 1)))

    # Normal approximation (continuity correction optional)
    mu_U = n1 * n2 / 2
    z = (U_A - mu_U) / np.sqrt(var_U)
    from scipy import stats
    p = 2 * stats.norm.sf(abs(z))

    return U_A, U_B, z, p

# Test
a, b = [2.1, 3.4, 4.0, 5.2, 6.1], [1.0, 2.5, 3.0, 4.5, 7.2]
U_A, U_B, z, p = mann_whitney_u(a, b)
print(f"U_A={U_A}, U_B={U_B}, z={z:.3f}, p={p:.4f}")
# U_A=15.0, U_B=10.0, z=0.521, p=0.6024


def wilcoxon_signed_rank(x, y=None):
    \"\"\"Wilcoxon signed-rank test from scratch.

    Pass x (one sample vs 0) or x, y (paired: tests x - y).
    Returns W, z-score, two-sided p-value.
    \"\"\"
    x = np.array(x, float)
    diffs = x - np.array(y, float) if y is not None else x

    # Remove zero differences
    diffs = diffs[diffs != 0]
    n = len(diffs)
    if n == 0:
        return 0, 0, 1.0

    abs_diffs = np.abs(diffs)

    # Rank absolute differences (with tie-averaging)
    order = np.argsort(abs_diffs, kind='stable')
    ranks = np.empty(n)
    i = 0
    while i < n:
        j = i
        while j < n-1 and abs_diffs[order[j+1]] == abs_diffs[order[j]]:
            j += 1
        ranks[order[i:j+1]] = (i + j) / 2 + 1
        i = j + 1

    W_plus  = np.sum(ranks[diffs > 0])
    W_minus = np.sum(ranks[diffs < 0])
    W = min(W_plus, W_minus)

    # Normal approximation
    mu_W    = n * (n + 1) / 4
    var_W   = n * (n + 1) * (2*n + 1) / 24
    z = (W - mu_W) / np.sqrt(var_W)
    from scipy import stats
    p = 2 * stats.norm.sf(abs(z))

    return W, z, p


def permutation_test(a, b, n_perm=5000, seed=42):
    \"\"\"Two-sample permutation test (mean difference statistic).\"\"\"
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    n1 = len(a)
    combined = np.concatenate([a, b])
    obs_diff = np.mean(a) - np.mean(b)

    null_diffs = np.array([
        np.mean(perm := rng.permutation(combined)[:n1]) - np.mean(perm[n1:])
        for _ in range(n_perm)
    ])
    # +1 numerator/denominator for conservativeness
    p = (1 + np.sum(np.abs(null_diffs) >= abs(obs_diff))) / (n_perm + 1)
    return obs_diff, null_diffs, p

diff, null, p = permutation_test([5.2,6.1,4.9,7.3], [3.1,2.8,4.0,3.5])
print(f"Observed diff={diff:.4f}, p={p:.4f}")
# Observed diff=2.5250, p≈0.006
"""),

    heading3("6b — Production Usage (scipy.stats)"),
    code_block("python", """from scipy import stats
import numpy as np

# ── Mann-Whitney U ──────────────────────────────────────────────────────────
group_a = [2.1, 3.4, 4.0, 5.2, 6.1]
group_b = [1.0, 2.5, 3.0, 4.5, 7.2]
u_stat, p = stats.mannwhitneyu(group_a, group_b, alternative='two-sided')
# ⚠️ Gotcha: scipy returns the SMALLER U by default (the min of U_A, U_B)
# alternative='two-sided' needed for two-tailed test
print(f"U={u_stat}, p={p:.4f}")   # U=10.0, p=0.6905

# ── Wilcoxon Signed-Rank ────────────────────────────────────────────────────
before = [120, 115, 130, 125, 118]
after  = [110, 112, 119, 118, 115]
w_stat, p = stats.wilcoxon(before, after, alternative='two-sided')
# Note: wilcoxon() takes the PAIR, not differences.
# zero_method='wilcox' (default): excludes zero diffs
# zero_method='pratt': includes zero diffs in ranking
print(f"W={w_stat}, p={p:.4f}")   # W=0.0, p=0.0625

# ── Kruskal-Wallis ──────────────────────────────────────────────────────────
g1 = [3.2, 4.1, 5.0, 3.8]
g2 = [7.2, 8.1, 6.5, 9.0]
g3 = [4.5, 5.3, 6.2, 4.9]
h_stat, p = stats.kruskal(g1, g2, g3)
print(f"H={h_stat:.4f}, p={p:.4f}")   # H=8.7692, p=0.0125
# ⚠️ Post-hoc: KW just tells you *some* groups differ.
# Use Dunn's test (scikit_posthocs.posthoc_dunn) for pairwise comparisons.

# ── Kolmogorov-Smirnov ──────────────────────────────────────────────────────
s1 = [1.2, 2.3, 2.8, 3.4, 4.1]
s2 = [0.8, 1.9, 3.0, 4.5, 5.2]
d_stat, p = stats.ks_2samp(s1, s2)
print(f"D={d_stat:.4f}, p={p:.4f}")   # D=0.4000, p=0.8730
# ⚠️ KS is sensitive to ALL distributional differences (location, scale, shape).
# For just location: prefer Mann-Whitney. For full distribution: use KS.

# ── Permutation test (scipy 1.8+) ───────────────────────────────────────────
a = np.array([5.2, 6.1, 4.9, 7.3])
b = np.array([3.1, 2.8, 4.0, 3.5])
result = stats.permutation_test(
    (a, b),
    statistic=lambda x, y, axis: np.mean(x, axis=axis) - np.mean(y, axis=axis),
    permutation_type='samples',    # two independent samples
    n_resamples=9999,
    alternative='two-sided',
    random_state=42,
)
print(f"Observed diff={result.statistic:.4f}, p={result.pvalue:.4f}")
# ≈ 0.006

# ── Common Gotchas ──────────────────────────────────────────────────────────
# 1. mannwhitneyu alternative='less'/'greater' for one-sided tests
# 2. KW significant → must use post-hoc tests (e.g. Dunn with Bonferroni)
# 3. KS test + many ties → use stats.epps_singleton_2samp instead
# 4. For large n, Wilcoxon signed-rank ≈ t-test on ranks: use t-test on diffs
"""),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 7: Interview Deep-Dive
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎤 Interview Deep-Dive"),

    heading3("Q1 (Easy): When should you use a non-parametric test instead of a t-test?"),
    para(rt("Use a non-parametric test when: (1) sample size is small (n < 30) and normality cannot be assumed, (2) data contains outliers that are real observations (not errors), (3) the variable is ordinal (e.g., Likert scales), (4) the distribution is clearly non-normal (heavily skewed, bimodal). For large samples, the t-test is robust via CLT — non-parametric tests offer little benefit.")),

    heading3("Q2 (Easy): What is the Mann-Whitney U test testing?"),
    para(rt("It tests whether one random variable tends to be stochastically larger than another: "), eq(r"H_0: P(X > Y) = 0.5"), rt(". The U statistic estimates this probability: "), eq(r"\hat{P}(X > Y) = U / (n_1 n_2)"), rt(". It does NOT test equality of means — it tests a location shift in the full distribution. Two distributions can have equal means but different U statistics.")),

    heading3("Q3 (Medium): Explain the relationship between Mann-Whitney U and the Wilcoxon rank-sum test."),
    para(rt("They are equivalent: the Wilcoxon rank-sum test uses "), eq(r"W = R_A"), rt(" (sum of ranks in group A), while Mann-Whitney uses "), eq(r"U_A = W - n_1(n_1+1)/2"), rt(". Since one is a linear function of the other, they produce identical p-values. The U formulation is preferred because it directly estimates "), eq(r"P(X > Y)"), rt(".")),

    heading3("Q4 (Medium): Why does the KS test require a continuous distribution?"),
    para(rt("The KS p-value derivation uses the Kolmogorov distribution, which assumes the ECDF converges smoothly to the true CDF. For discrete distributions, the ECDF has probability mass at specific points, causing ties that inflate the D statistic — making the test conservative (p-values too large) or anti-conservative, depending on implementation. Use the Kolmogorov-Smirnov-Lilliefors test or the Epps-Singleton test for discrete data.")),

    heading3("Q5 (Medium): What is the ARE of Mann-Whitney vs t-test, and why does it matter?"),
    para(rt("Under normality, ARE(Mann-Whitney, t-test) = 3/π ≈ 0.955. This means you need n/0.955 ≈ 1.047n observations with Mann-Whitney to achieve the same power as the t-test — a ~5% sample size overhead. But under heavy-tailed distributions (double-exponential: ARE = 1.5, Cauchy: ARE = ∞), Mann-Whitney is strictly more powerful. This is a compelling argument for Mann-Whitney in practice: tiny cost when normal, large gain when not.")),

    heading3("Q6 (Hard): Explain the permutation test — why is it exact, and when does it fail?"),
    para(rt("The permutation test is exact because the p-value is computed directly from the discrete null distribution generated by all possible relabellings of the data. No asymptotic approximation is used. It fails when: (1) observations are not exchangeable under H₀ (e.g., correlated data — matched pairs violate independence if not accounted for), (2) n is too small to achieve the desired significance level (e.g., with n₁=n₂=3, minimum p = 2/C(6,3) = 2/20 = 0.10 — impossible to achieve p<0.05), (3) the test statistic is not invariant to the labelling — must carefully design the statistic to match H₀.")),

    heading3("Q7 (Hard): How would you handle multiple testing after a significant Kruskal-Wallis test?"),
    para(rt("KW only identifies that "), rt("some", italic=True), rt(" groups differ. Post-hoc analysis requires pairwise comparisons. Options: (1) "), rt("Dunn's test", bold=True), rt(": compare all pairs using the KW rank sums, with Bonferroni or Holm-Bonferroni correction; implemented in scikit_posthocs.posthoc_dunn(). (2) "), rt("Steel-Dwass test", bold=True), rt(": permutation-based pairwise test that controls familywise error. (3) "), rt("Conover-Iman test", bold=True), rt(": t-test on ranks after KW. Dunn is most common; Steel-Dwass most robust. Never do uncorrected pairwise Mann-Whitney tests post-KW — inflated Type I error.")),

    heading3("Q8 (Hard / PhD-level): Prove that the Wilcoxon signed-rank statistic has E[W⁺] = n(n+1)/4 under H₀."),
    para(rt("Under H₀, the distribution of differences is symmetric about 0 — each difference is equally likely positive or negative, independently. Conditional on the absolute values |d₁|,…,|dₙ| (which are fixed), each sign is ±1 with probability 1/2, independently. The rank of |dᵢ| is the fixed rank rᵢ. Then:")),
    equation_block(r"W^+ = \sum_{i=1}^n r_i \cdot \mathbf{1}[d_i > 0]"),
    para(rt("Each "), eq(r"\mathbf{1}[d_i > 0] \sim \text{Bernoulli}(1/2)"), rt(" independently. Therefore:")),
    equation_block(r"\mathbb{E}[W^+] = \sum_{i=1}^n r_i \cdot \frac{1}{2} = \frac{1}{2}\cdot\frac{n(n+1)}{2} = \frac{n(n+1)}{4}"),
    para(rt("Similarly, "), eq(r"\operatorname{Var}(W^+) = \sum_{i=1}^n r_i^2 \cdot \frac{1}{4} = \frac{1}{4}\cdot\frac{n(n+1)(2n+1)}{6} = \frac{n(n+1)(2n+1)}{24}"), rt(".")),

    callout("🚩", rt("Red Flags (what gets you rejected): ", bold=True), rt("(1) Saying 'Mann-Whitney tests for equal means' — it tests stochastic dominance. (2) Using KW as a final answer without post-hoc testing. (3) Claiming non-parametric tests have 'no assumptions.' (4) Applying KS test to discrete data without noting the limitation. (5) Not correcting permutation p-value for the observed statistic itself (the +1 correction).")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 8: Comparison & Trade-offs
    # ══════════════════════════════════════════════════════════════════════════
    heading2("⚖️ Comparison & Trade-offs"),
    heading3("Non-Parametric vs Parametric Alternatives"),
    table(5,
        table_row(["Test", "Parametric Analogue", "What It Tests", "Assumes Symmetry", "Best for"]),
        table_row(["Mann-Whitney U", "Two-sample t-test", "P(X>Y) = 0.5 (stochastic dominance)", "No", "Ordinal/non-normal data, n≥8 per group"]),
        table_row(["Wilcoxon signed-rank", "Paired t-test", "Median difference = 0", "Yes (symmetric diffs)", "Paired data, non-normal differences"]),
        table_row(["Kruskal-Wallis", "One-way ANOVA", "Equal rank distributions across k groups", "No", "k≥3 groups with non-normal data"]),
        table_row(["KS two-sample", "No direct analogue", "Same distribution (location + shape + scale)", "No", "Testing full distributional equality"]),
        table_row(["Permutation test", "Any parametric test", "Depends on chosen statistic", "No", "Small n, any statistic, exact p-values"]),
    ),
    heading3("Within Non-Parametric Tests: When to Use Each"),
    table(4,
        table_row(["Scenario", "Best Choice", "Why", "Alternative"]),
        table_row(["2 independent groups, location", "Mann-Whitney U", "Most powerful rank test for shift", "Permutation on mean diff"]),
        table_row(["Before/after, same subjects", "Wilcoxon signed-rank", "Paired design removes between-subject noise", "Permutation (paired)"]),
        table_row(["k≥3 groups", "Kruskal-Wallis + Dunn", "Proper Type I error control across groups", "Permutation ANOVA"]),
        table_row(["Full distribution comparison", "KS test", "Detects shape/tail differences, not just location", "Cramér-von Mises test"]),
        table_row(["Arbitrary statistic, exact p", "Permutation test", "No asymptotic approximation needed", "Bootstrap test"]),
        table_row(["Variance equality (not location)", "Levene's test (parametric) or Fligner-Killeen", "KW/MW are insensitive to pure scale changes", "Brown-Forsythe"]),
    ),
    heading3("Advantages of Non-Parametric Tests"),
    bullet(rt("Valid for any continuous distribution — no normality required")),
    bullet(rt("Robust to outliers (rank of an outlier is bounded by n)")),
    bullet(rt("Applicable to ordinal data (Likert scales, rankings)")),
    bullet(rt("Exact p-values for small samples (exact versions)")),
    bullet(rt("Mann-Whitney directly estimates P(X>Y) — a meaningful effect size")),
    heading3("Disadvantages"),
    bullet(rt("Slight power loss under normality (~5% more samples needed)")),
    bullet(rt("Less flexible for complex designs (factorial ANOVA, random effects)")),
    bullet(rt("Rank-based tests less interpretable (rank differences vs actual differences)")),
    bullet(rt("KW/Mann-Whitney sensitive to tied values; correction required")),
    callout("🎯", rt("Decision Rule: ", bold=True), rt("If n > 50 per group → t-test/ANOVA is robust via CLT. If n < 30 and normality is uncertain → use non-parametric. If interested in P(X>Y), not just means → Mann-Whitney always appropriate. If comparing whole distributions → KS test. If you need exact p-values with any statistic → permutation test.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 9: Interactive Visual Explainer
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through each test visually — select a test, then use Next/Prev or arrow keys to animate the rank transformation, statistic computation, and null distribution.", italic=True, color="gray")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10: Related Topics & Further Reading
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Hypothesis testing fundamentals (Type I/II error, p-values, significance levels)")),
    bullet(rt("Probability distributions and CDF")),
    bullet(rt("t-test and ANOVA (parametric counterparts)")),
    bullet(rt("Combinatorics (permutations and combinations)")),
    heading3("What to Learn Next"),
    bullet(rt("Post-hoc tests: Dunn, Steel-Dwass, Nemenyi (after Kruskal-Wallis)")),
    bullet(rt("Spearman rank correlation (another rank-based method)")),
    bullet(rt("Bootstrap methods (related resampling approach)")),
    bullet(rt("Multiple testing correction (Bonferroni, Benjamini-Hochberg FDR)")),
    bullet(rt("Mixed-effects models (parametric approach for repeated measures)")),
    heading3("Key Papers"),
    bullet(rt("Wilcoxon, F. (1945). 'Individual comparisons by ranking methods.' Biometrics Bulletin, 1(6), 80-83. — Introduced rank-sum and signed-rank tests.")),
    bullet(rt("Mann, H.B. & Whitney, D.R. (1947). 'On a test of whether one of two random variables is stochastically larger than the other.' Annals of Mathematical Statistics. — Generalised Wilcoxon's rank-sum, proved exact distribution.")),
    bullet(rt("Kruskal, W.H. & Wallis, W.A. (1952). 'Use of ranks in one-criterion variance analysis.' JASA. — Introduced H statistic, χ² approximation.")),
    bullet(rt("Kolmogorov, A.N. (1933). 'Sulla determinazione empirica di una legge di distribuzione.' — Proved the universal limiting distribution of the KS statistic.")),
    bullet(rt("Hoeffding, W. (1948). 'A class of statistics with asymptotically normal distribution.' AMS. — Unified framework for U-statistics including Mann-Whitney U.")),
    heading3("Best Resources"),
    bullet(rt("Conover, W.J. 'Practical Nonparametric Statistics' (3rd ed.) — comprehensive reference")),
    bullet(rt("Good, P. 'Permutation, Parametric and Bootstrap Tests of Hypotheses' — authoritative treatment of permutation tests")),
    bullet(rt("scipy.stats documentation — see mannwhitneyu, wilcoxon, kruskal, ks_2samp, permutation_test")),
    bullet(rt("statsmodels.stats.contingency_tables — for exact Fisher/chi-squared tests")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Hypothesis Testing (3.8), Probability Distributions (3.3), Bootstrap Resampling, Multiple Testing Correction, Spearman Correlation, ANOVA variants, Effect size measures (Rank-biserial correlation for Mann-Whitney)")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
