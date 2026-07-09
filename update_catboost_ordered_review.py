#!/usr/bin/env python3
"""Update Notion page for: CatBoost — Ordered Boosting & Native Categorical Support"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-817f-b629-fa4587437f2b"
ICON = "🟠"  # Advanced
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/catboost_ordered_review_explainer.html"

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": EXPLAINER_URL},
}

blocks = [

    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("CatBoost is a gradient boosting library (Yandex, 2017) that fixes two subtle but serious flaws in standard GBDT: "
            "(1) target leakage when encoding categorical features, and "
            "(2) prediction shift — a bias that accumulates when the same data is used both to compute gradients and to fit the next tree. "
            "It handles both problems automatically, without requiring the user to do manual feature engineering for categorical columns.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine a teacher grading Student A's essay, but they already know Student A's historical average score. "
            "That prior knowledge biases the grade. Ordered boosting says: "
            "when grading essay #k, only consult grades from essays 1 through k−1. "
            "Each observation is evaluated by a model that has never seen it — eliminating the circularity.")),
    callout("💡",
            rt("If you remember one thing: ", bold=True),
            rt("CatBoost computes categorical target statistics for each row using only prior rows in a random permutation, "
               "guaranteeing zero target leakage. This is the core idea behind all of its correctness guarantees.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("By 2017, XGBoost and LightGBM dominated tabular ML competitions. Both required manual categorical encoding "
            "(one-hot, target encoding, label encoding). Naive target encoding — replacing a category with "
            "the mean target value of that category — leaks label information into features, "
            "inflating in-sample performance and causing test-set degradation. "
            "Additionally, all standard GBDT methods suffered from prediction shift: "
            "the gradient for example i at iteration t is computed using a model F^(t-1) that was fit on i itself, "
            "creating a subtle but persistent upward bias in leaf value estimates.")),
    heading3("Key Paper"),
    para(rt("Prokhorenkova, L., Gusev, G., Veronika, A., Gulin, A. (2018). "
            "\"CatBoost: unbiased boosting with categorical features.\" "
            "NeurIPS 2018. "
            "Contribution: formally defined prediction shift, proved ordered boosting eliminates it, "
            "and introduced ordered target statistics for leak-free categorical encoding.")),
    heading3("Evolution Timeline"),
    bullet(rt("2014 — XGBoost: regularised GBDT, manual categorical handling required")),
    bullet(rt("2016 — LightGBM: leaf-wise growth, histogram binning, optional cat splits (not TS-based)")),
    bullet(rt("2017 — CatBoost open-sourced; 2018 — NeurIPS paper formalises guarantees")),
    bullet(rt("2019–present — CatBoost adds GPU training, ONNX export, and improved 'Plain' mode for speed")),
    heading3("Before vs. After"),
    table(3,
        table_row(["Dimension", "Standard GBDT (XGB/LGB)", "CatBoost"]),
        table_row(["Categorical encoding", "Manual: OHE, TE, label-enc", "Automatic ordered target statistics"]),
        table_row(["Target leakage", "Present with naive TE", "Eliminated by construction"]),
        table_row(["Prediction shift", "Present in all standard methods", "Eliminated by ordered boosting"]),
        table_row(["Tree structure", "Level-wise or leaf-wise asymmetric", "Oblivious symmetric (same split per depth level)"]),
        table_row(["Prediction speed", "Moderate", "Excellent (lookup-table via oblivious trees)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧱 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Ordered Target Statistic (Ordered TS): ", bold=True),
           rt("A categorical encoding where, for row σ(i) in permutation σ, the statistic is computed "
              "from rows σ(1), …, σ(i−1) only. Prevents the current row's label from influencing its own encoding.")),
    bullet(rt("Ordered Boosting: ", bold=True),
           rt("A boosting variant that maintains n sub-models indexed by the permutation. "
              "The gradient for σ(i) is computed using a model trained on {σ(1), …, σ(i−1)}, "
              "eliminating prediction shift.")),
    bullet(rt("Oblivious Symmetric Tree: ", bold=True),
           rt("A decision tree where all nodes at the same depth use the identical (feature, threshold) split. "
              "A depth-d tree has 2^d leaves and can be evaluated as a d-bit bitmask lookup.")),
    bullet(rt("Prediction Shift: ", bold=True),
           rt("The bias introduced when a model is used to compute gradients for the same examples it was fit on. "
              "Formally: E[h(x_i) | leaf(x_i)] ≠ E[g_i | leaf(x_i)] when i is in the training set of h.")),
    callout("🔑",
            rt("Core invariant: ", bold=True),
            rt("In ordered boosting, the gradient for example σ(i) is computed using a model "
               "M^(i) that was never trained on σ(i). This makes the gradient an unbiased estimate "
               "of the true gradient under the current model.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ───────────────────────────
    heading2("🔬 Architecture & Internal Workings"),
    heading3("Step 1 — Permutation Draw"),
    para(rt("CatBoost draws s random permutations of the n training examples. "
            "For practical reasons (memory), s is small (1–4 in practice). "
            "Let σ = (σ(1), …, σ(n)) be one such permutation.")),
    heading3("Step 2 — Ordered Target Statistics"),
    para(rt("For each categorical feature k and each row position i in σ, compute:")),
    equation_block(
        r"\hat{x}_{\sigma(i),k} = \frac{\sum_{j=1}^{i-1} \mathbb{1}[x_{\sigma(j),k} = x_{\sigma(i),k}]\, y_{\sigma(j)} + a \cdot p}{\sum_{j=1}^{i-1} \mathbb{1}[x_{\sigma(j),k} = x_{\sigma(i),k}] + a}"
    ),
    para(rt("where ", italic=True), eq(r"a > 0"), rt(" is a prior weight (hyperparameter) and "),
         eq(r"p"), rt(" is a prior value (typically the global mean "), eq(r"\bar{y}"), rt("). "
            "For the first row in σ, no prior rows exist, so the estimate is purely the prior. "
            "As i grows, genuine category statistics dominate.")),
    para(rt("Key property: the label "), eq(r"y_{\sigma(i)}"), rt(" is never used when computing "),
         eq(r"\hat{x}_{\sigma(i),k}"), rt(". No target leakage by construction.")),
    heading3("Step 3 — Ordered Boosting"),
    para(rt("At iteration t, CatBoost needs the gradient "), eq(r"g_{\sigma(i)}^t"),
         rt(" for each training example. In standard GBDT, this is computed using "),
         eq(r"F^{t-1}"), rt(" which was fit on the full training set — introducing prediction shift. "
            "CatBoost instead maintains, for each permutation position i, a model "),
         eq(r"M_{t-1}^{(i)}"), rt(" built from "), eq(r"\{\sigma(1), \ldots, \sigma(i-1)\}"), rt(":")),
    equation_block(
        r"g_{\sigma(i)}^t = -\frac{\partial L(y_{\sigma(i)},\, F)}{\partial F}\bigg|_{F = M_{t-1}^{(i)}(x_{\sigma(i)})}"
    ),
    para(rt("Because "), eq(r"x_{\sigma(i)}"), rt(" was never used to build "), eq(r"M_{t-1}^{(i)}"),
         rt(", this gradient is unbiased. "
            "The leaf value for leaf ℓ in tree h^t is also computed using only the examples in ℓ "
            "under the same ordered principle.")),
    heading3("Step 4 — Oblivious Symmetric Tree Construction"),
    para(rt("CatBoost grows fixed-depth symmetric trees. At depth d, a single split "),
         eq(r"(f_d, \theta_d)"), rt(" is selected — the same for all nodes at depth d. "
            "The full tree is determined by d (feature, threshold) pairs. "
            "A sample is routed to leaf "), eq(r"\ell = \sum_{d=1}^{D} \mathbb{1}[x_{f_d} \geq \theta_d] \cdot 2^{d-1}"),
         rt(", i.e., a D-bit integer used as a direct array index.")),
    para(rt("Best split at each depth is chosen by greedy gain, typically symmetric: "
            "all 2^(d-1) nodes at depth d are split simultaneously with the same feature+threshold, "
            "and the one maximising total gain across all node pairs is selected.")),
    heading3("Numerical Trace — Ordered TS on a 5-Row Dataset"),
    para(rt("Permutation σ = [2, 0, 4, 1, 3]. Category column: {A, B}. Labels: y = [1.0, 0.0, 1.0, 0.5, 1.0]. Prior: a=1, p=0.6.")),
    bullet(rt("σ(0)=row2, cat=A: no priors → TS = (1×0.6)/(1) = 0.600")),
    bullet(rt("σ(1)=row0, cat=A: one prior A row (row2, y=1.0) → TS = (0.6+1.0)/(1+1) = 0.800")),
    bullet(rt("σ(2)=row4, cat=B: no prior B rows → TS = 0.600 (prior only)")),
    bullet(rt("σ(3)=row1, cat=B: one prior B row (row4, y=1.0) → TS = (0.6+1.0)/(1+1) = 0.800")),
    bullet(rt("σ(4)=row3, cat=A: two prior A rows (rows 2 y=1, row0 y=1) → TS = (0.6+1+1)/(1+2) = 0.867")),
    para(rt("Observe: row1's own label (y=0) does not influence its TS of 0.800 — leakage prevented.")),
    divider(),

    # ── Section 5: The Math ────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Prediction Shift — Formal Definition"),
    para(rt("Let "), eq(r"h^t"), rt(" be the t-th tree fit to gradients "), eq(r"g_i^t"),
         rt(" computed from "), eq(r"F^{t-1}"), rt(". For leaf "), eq(r"\ell"),
         rt(", the optimal leaf value is:")),
    equation_block(
        r"w^*_\ell = \frac{\sum_{i \in \ell} g_i^t}{\sum_{i \in \ell} h_i^t + \lambda}"
    ),
    para(rt("where "), eq(r"h_i^t"), rt(" is the second-order gradient (hessian). "
            "The prediction shift arises because "), eq(r"g_i^t"),
         rt(" and the assignment "), eq(r"i \in \ell"),
         rt(" are not independent when "), eq(r"F^{t-1}"), rt(" was trained on all examples including i.")),
    heading3("Ordered TS — Consistency as n→∞"),
    para(rt("As "), eq(r"n \to \infty"), rt(", for any fixed category value v, "
            "the number of prior rows with category v grows as "), eq(r"O(n)"),
         rt(". The prior term "), eq(r"a \cdot p"),
         rt(" becomes negligible, and the ordered TS converges to:")),
    equation_block(
        r"\hat{x}_{\sigma(i),k} \xrightarrow{n\to\infty} \mathbb{E}[y \mid x_k = v]"
    ),
    para(rt("This is exactly the optimal target encoding for a supervised model — achieved without leakage.")),
    heading3("Prior Weight Effect"),
    para(rt("The prior weight "), eq(r"a"), rt(" controls the bias-variance tradeoff for rare categories. "
            "For a category appearing "), eq(r"c"), rt(" times before position i:")),
    equation_block(
        r"\hat{x}_{\sigma(i),k} = \frac{c \cdot \bar{y}_c + a \cdot p}{c + a}"
    ),
    para(rt("When "), eq(r"c \ll a"), rt(", the estimate is dominated by the global prior "),
         eq(r"p"), rt(". When "), eq(r"c \gg a"),
         rt(", it converges to the sample mean for that category. "
            "Typical default: a ∈ [0.1, 10], chosen via cross-validation.")),
    callout("⚠️",
            rt("Warning: ", bold=True),
            rt("CatBoost uses multiple permutations during training but a single fixed permutation-averaged statistic at inference. "
               "This means inference TS values differ from any single training permutation's values — "
               "the test-time statistic uses all training rows, not the ordered subset.")),
    divider(),

    # ── Section 6: Code Implementation ────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — Ordered TS From Scratch (NumPy)"),
    code_block("python",
"""import numpy as np

def ordered_target_statistic(x_cat, y, prior_a=1.0, prior_p=None, seed=42):
    \"\"\"
    Compute ordered target statistics for a single categorical column.

    Args:
        x_cat: array of category labels (strings or ints), shape (n,)
        y:     target array, shape (n,)
        prior_a: prior weight (> 0, higher = more shrinkage for rare cats)
        prior_p: prior value (default: global mean of y)
        seed:  random seed for permutation
    Returns:
        ts: ordered TS values, shape (n,), in ORIGINAL row order
    \"\"\"
    n = len(x_cat)
    if prior_p is None:
        prior_p = np.mean(y)

    rng = np.random.default_rng(seed)
    sigma = rng.permutation(n)           # random permutation
    sigma_inv = np.argsort(sigma)        # inverse: original_idx -> perm_position

    ts = np.zeros(n)
    # Accumulators per category: {cat -> (numerator, denominator)}
    num_by_cat = {}
    den_by_cat = {}

    for perm_pos in range(n):
        orig_idx = sigma[perm_pos]
        cat = x_cat[orig_idx]

        # TS for this row = accumulated stats from PRIOR rows only
        cat_num = num_by_cat.get(cat, 0.0)
        cat_den = den_by_cat.get(cat, 0.0)
        ts[orig_idx] = (cat_num + prior_a * prior_p) / (cat_den + prior_a)

        # NOW update accumulators with this row's label
        num_by_cat[cat] = cat_num + y[orig_idx]
        den_by_cat[cat] = cat_den + 1.0

    return ts

# Example
x_cat = np.array(['A', 'B', 'A', 'A', 'B'])
y     = np.array([1.0, 0.0, 1.0, 0.5, 1.0])
ts = ordered_target_statistic(x_cat, y, prior_a=1.0, seed=42)
print("Ordered TS:", ts.round(3))
# Note: each ts[i] is computed without using y[i] — zero leakage
"""),
    heading3("6b — Production Usage (CatBoost Python API)"),
    code_block("python",
"""from catboost import CatBoostClassifier, Pool
import pandas as pd

# Suppose df has columns: 'city' (categorical), 'age', 'income', 'churn'
cat_cols = ['city', 'product_type', 'region']   # high-cardinality categoricals

train_pool = Pool(
    data=df_train.drop('churn', axis=1),
    label=df_train['churn'],
    cat_features=cat_cols,   # ← CRITICAL: tell CatBoost which cols are categorical
)
eval_pool = Pool(
    data=df_val.drop('churn', axis=1),
    label=df_val['churn'],
    cat_features=cat_cols,
)

model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.05,
    depth=6,                       # oblivious tree depth (2^6=64 leaves)
    l2_leaf_reg=3.0,               # L2 regularisation on leaf values
    bagging_temperature=1.0,       # Bayesian bootstrap for row sampling
    random_strength=1.0,           # randomness for split scoring
    border_count=254,              # quantisation bins for numeric features
    boosting_type='Ordered',       # 'Ordered' (default) or 'Plain' (faster, large data)
    eval_metric='AUC',
    use_best_model=True,
    early_stopping_rounds=50,
    verbose=100,
)
model.fit(train_pool, eval_set=eval_pool)

# Gotcha: if cat_features not specified, CatBoost silently treats cats as numeric
# Gotcha: use Pool objects (not raw DataFrames) for production — avoids type coercion

preds = model.predict_proba(df_test[features])[:, 1]
"""),
    callout("⚠️",
            rt("Gotcha: ", bold=True),
            rt("Always pass cat_features explicitly. CatBoost accepts feature names or indices. "
               "Forgetting this makes CatBoost treat string columns as numeric — "
               "it will error on string input but silently mishandle integer-encoded categoricals, "
               "losing all ordered TS benefits.")),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is CatBoost and how does it differ from XGBoost?", bold=True)], [
        para(rt("CatBoost is a gradient boosting library with two key innovations: "
                "(1) ordered target statistics for leak-free categorical encoding, and "
                "(2) ordered boosting to eliminate prediction shift. "
                "XGBoost uses the same gradient computation and the same training data to fit trees — "
                "a subtle circularity that inflates residual estimates. "
                "CatBoost also uses oblivious symmetric trees, making prediction faster.")),
    ]),
    toggle([rt("Q2 (Medium): What is prediction shift and why does it matter?", bold=True)], [
        para(rt("In standard GBDT, the gradient for example i at step t is computed from a model F^(t-1) "
                "that was fit on example i. This means the gradient and the tree-leaf assignment are correlated: "
                "the leaf containing i was partly shaped by i's label, inflating the leaf value estimate. "
                "Over many iterations this bias compounds, hurting generalisation. "
                "Ordered boosting eliminates this by computing the gradient for σ(i) using a model "
                "trained only on {σ(1), …, σ(i−1)}.")),
        para(rt("Follow-up trap — 'Doesn't this make training O(n²)?'"),
             rt(" Yes, naive ordered boosting is O(n²) — CatBoost approximates it by grouping permutation prefixes "
                "into a log-scale sequence (2^0, 2^1, …, 2^⌊log n⌋), reducing to O(n log n).", italic=True)),
    ]),
    toggle([rt("Q3 (Medium): Explain ordered target statistics. How do they prevent leakage?", bold=True)], [
        para(rt("For position i in permutation σ, the TS for row σ(i) uses only rows σ(1..i-1):")),
        para(eq(r"\hat{x}_{\sigma(i),k} = \frac{\sum_{j<i} \mathbb{1}[\text{cat match}] y_{\sigma(j)} + ap}{\sum_{j<i} \mathbb{1}[\text{cat match}] + a}")),
        para(rt("The label y_{σ(i)} is never used in its own encoding, so no label information leaks into the features. "
                "At inference time, CatBoost uses training-set-wide statistics (all rows, ordered by permutation average), "
                "which converge to the true conditional mean as n grows.")),
    ]),
    toggle([rt("Q4 (Medium): What is an oblivious symmetric tree? Why does CatBoost use them?", bold=True)], [
        para(rt("An oblivious tree constrains all nodes at the same depth to use the identical split (feature + threshold). "
                "A depth-d tree is defined by exactly d (feature, threshold) pairs. "
                "To predict: compute a d-bit key (one bit per depth level) and index directly into a 2^d leaf array. "
                "Benefits: (1) O(1) prediction via lookup table, GPU-friendly bitmask operations, "
                "(2) implicit regularisation — the constrained structure reduces overfitting, "
                "(3) cache-friendly memory access. "
                "Drawback: less expressive per tree than asymmetric trees — compensated by using more iterations.")),
    ]),
    toggle([rt("Q5 (Hard): Explain the prior weight a in ordered TS. How do you choose it?", bold=True)], [
        para(rt("The prior weight a controls smoothing for rare categories. "
                "When a category appears c times before position i, the estimate is a weighted average:")),
        para(eq(r"\hat{x} = \frac{c \bar{y}_c + a p}{c + a}")),
        para(rt("For c >> a: estimate ≈ sample mean for this category (data-driven). "
                "For c << a: estimate ≈ prior p (global mean). "
                "Choosing a: typically tuned via CV in the range [0.1, 10]. "
                "Higher a is safer when categories have low counts (e.g., long-tail user IDs). "
                "CatBoost exposes this as the 'counter_calc_method' and related hyperparameters.")),
        para(rt("PhD-level angle: the optimal a under MSE loss is the ratio of the variance of the global mean "
                "to the within-category variance: a* = Var(y) / Var(y | x_k = v). "
                "This is related to James-Stein shrinkage.")),
    ]),
    toggle([rt("Q6 (Hard): When would you prefer LightGBM over CatBoost?", bold=True)], [
        para(rt("Prefer LightGBM when: (1) dataset is large (>10M rows) and training speed is critical — "
                "ordered boosting adds overhead that 'Plain' mode only partially recovers; "
                "(2) features are mostly numeric with no high-cardinality categoricals; "
                "(3) you need leaf-wise asymmetric trees for capturing rare high-impact patterns "
                "(oblivious trees are less expressive per tree). "
                "Prefer CatBoost when: (1) many high-cardinality categoricals, "
                "(2) need fast inference (oblivious tree lookup), "
                "(3) want protection against target leakage with minimal preprocessing.")),
    ]),
    callout("🚩",
            rt("Red flag: ", bold=True),
            rt("Saying 'CatBoost is just XGBoost with categorical support' misses the point entirely. "
               "The ordered boosting principle (eliminating prediction shift) is architecturally distinct "
               "and applies to numeric features too. Categorical handling is a separate innovation.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(4,
        table_row(["Dimension", "XGBoost", "LightGBM", "CatBoost"]),
        table_row(["Tree structure", "Level-wise asymmetric", "Leaf-wise asymmetric", "Oblivious symmetric"]),
        table_row(["Categorical encoding", "Manual required", "Built-in split (not TS)", "Ordered TS, automatic"]),
        table_row(["Target leakage risk", "High (naive TE)", "Medium", "None"]),
        table_row(["Prediction shift", "Present", "Present", "Eliminated (Ordered mode)"]),
        table_row(["Training speed", "Good", "Fastest", "Slower (ordered overhead)"]),
        table_row(["Inference speed", "Good", "Good", "Excellent (lookup table)"]),
        table_row(["High-cardinality cats", "Poor (OHE blowup)", "Fair", "Excellent"]),
        table_row(["GPU support", "Yes", "Yes", "Yes (well-optimised)"]),
        table_row(["Default hyperparams", "Needs tuning", "Needs tuning", "Good defaults"]),
        table_row(["Ecosystem", "Widest (Spark, ONNX…)", "Wide", "Good, growing"]),
    ),
    heading3("When to Use"),
    bullet(rt("CatBoost: high-cardinality categoricals, fast inference requirements, minimal preprocessing, fraud/click-through datasets")),
    bullet(rt("LightGBM: large numeric datasets (>10M rows), speed-critical training pipelines")),
    bullet(rt("XGBoost: legacy integrations, Spark/distributed environments, broadest ONNX support")),
    heading3("Advantages of CatBoost"),
    bullet(rt("Leak-free categorical encoding without any manual feature engineering")),
    bullet(rt("Ordered boosting eliminates prediction shift — better calibration and generalisation")),
    bullet(rt("Oblivious trees enable ultra-fast inference (bitmask + array lookup)")),
    bullet(rt("Strong defaults: often competitive with less tuning than XGB/LGB")),
    heading3("Disadvantages"),
    bullet(rt("Slower training in Ordered mode — overhead from maintaining permutation sub-models")),
    bullet(rt("Oblivious trees less expressive per tree; needs more iterations to match leaf-wise models")),
    bullet(rt("Smaller community and ecosystem than XGBoost")),
    callout("🎯",
            rt("Decision: ", bold=True),
            rt("Use CatBoost when categorical features are central to the problem (e.g. user_id, product_id, geo). "
               "Use LightGBM when dataset is large and mostly numeric. "
               "Use XGBoost when ecosystem compatibility (Spark, ONNX, Triton) is the hard constraint.")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ───────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Gradient Boosting / GBDT fundamentals")),
    bullet(rt("Decision trees: splitting criteria (Gini, entropy, variance reduction)")),
    bullet(rt("Target encoding & the target leakage problem")),
    bullet(rt("XGBoost: level-wise tree growth, second-order gradients")),
    heading3("What to Learn Next"),
    bullet(rt("LightGBM: leaf-wise growth, GOSS, EFB")),
    bullet(rt("Hyperparameter tuning for boosting (Optuna, Hyperopt)")),
    bullet(rt("Stacking / blending ensembles combining CatBoost with neural nets")),
    bullet(rt("Feature importance methods: SHAP for tree models")),
    heading3("Key Papers"),
    bullet(rt("Prokhorenkova et al. (2018). CatBoost: unbiased boosting with categorical features. NeurIPS 2018.")),
    bullet(rt("Chen & Guestrin (2016). XGBoost: A scalable tree boosting system. KDD 2016.")),
    bullet(rt("Ke et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. NeurIPS 2017.")),
    bullet(rt("Friedman (2001). Greedy function approximation: A gradient boosting machine. Annals of Statistics.")),
    heading3("Best Resources"),
    bullet(rt("CatBoost paper (NeurIPS 2018): https://arxiv.org/abs/1706.09516")),
    bullet(rt("CatBoost docs: https://catboost.ai/en/docs/")),
    bullet(rt("Kaggle CatBoost tutorials — practical parameter tuning examples")),
    callout("🔗",
            rt("This topic connects to: ", bold=True),
            rt("XGBoost, LightGBM, Decision Trees, Target Encoding, SHAP Feature Importance, "
               "Gradient Descent, Ensemble Methods.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
