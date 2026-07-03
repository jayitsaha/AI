"""
Notion updater for: Model Complexity vs Generalization
Page ID: 33c93418-809c-8106-a943-ecffc8b552b5
"""

from notion_template import (
    update_page,
    heading2, heading3,
    para, equation_block,
    rt, eq,
    callout, bullet, numbered,
    code_block, divider,
    toggle, table, table_row,
    embed,
)

# ── Constants ──────────────────────────────────────────────────────────────────
PAGE_ID = "33c93418-809c-8106-a943-ecffc8b552b5"
ICON = "🟡"
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/complexity_generalization_explainer.html"

PROPERTIES = {
    "Status":              {"select": {"name": "Completed"}},
    "Depth":               {"select": {"name": "Intermediate"}},
    "Interview Priority":  {"select": {"name": "Must Know"}},
    "Has Explainer":       {"checkbox": True},
    "Explainer URL":       {"url": EXPLAINER_URL},
}

# ══════════════════════════════════════════════════════════════════════════════
#  BLOCKS
# ══════════════════════════════════════════════════════════════════════════════

blocks = []

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — THE 30-SECOND VERSION
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("🎯 The 30-Second Version"))

blocks.append(bullet(
    rt("What is this? "), rt("A model that's too simple can't learn the pattern (", bold=True),
    rt("underfitting", bold=True), rt("). A model that's too complex memorises noise instead "
       "of patterns (", bold=True), rt("overfitting", bold=True),
    rt("). Complexity vs generalization is about finding the sweet spot."),
))

blocks.append(bullet(
    rt("Analogy: "), rt("Goldilocks", bold=True),
    rt(" — too cold (underfit), too hot (overfit), just right (good generalisation)."),
))

blocks.append(bullet(
    rt("One-sentence summary: "),
    rt("As model complexity grows, training error falls monotonically but test error follows a "
       "U-shape — the bottom of the U is the generalization sweet spot."),
))

blocks.append(callout(
    "💡",
    rt("If you remember one thing: ", bold=True),
    rt("training error always decreases with complexity; test error has a minimum — "
       "that minimum is your target."),
))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — HISTORICAL CONTEXT
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("📜 Historical Context"))

blocks.append(heading3("The Problem"))
blocks.append(para(
    rt("Early ML models (linear regression, perceptrons) were too rigid. Increasing their capacity "
       "(polynomial features, wider networks) improved training fit but hurt test performance "
       "unexpectedly."),
))

blocks.append(heading3("Before: Pure Empirical Risk Minimisation"))
blocks.append(para(
    rt("Minimise training loss and hope for the best. Problem: zero training loss doesn't mean "
       "zero test loss."),
))

blocks.append(heading3("Breakthrough: Statistical Learning Theory"))
blocks.append(para(
    rt("Vapnik & Chervonenkis (1971) formalised why: "),
    rt("VC dimension", bold=True),
    rt(" bounds how much a model class can overfit. "),
    rt("Structural Risk Minimisation (SRM)", bold=True),
    rt(" added a complexity penalty."),
))

blocks.append(heading3("Key Papers"))
blocks.append(bullet(
    rt('"On the Uniform Convergence of Relative Frequencies of Events to Their Probabilities"', italic=True),
    rt(" — Vapnik & Chervonenkis, 1971 — introduced VC dimension"),
))
blocks.append(bullet(
    rt('"A Training Algorithm for Optimal Margin Classifiers"', italic=True),
    rt(" — Boser, Guyon, Vapnik, 1992 — SVMs as capacity control"),
))
blocks.append(bullet(
    rt('"Reconciling modern machine-learning practice and the classical bias–variance trade-off"', italic=True),
    rt(" — Belkin et al., PNAS 2019 — double-descent"),
))

blocks.append(heading3("Timeline"))
blocks.append(para(
    rt("Curve fitting (1800s) → VC theory (1971) → SRM/SVMs (1990s) → "
       "Bias-Variance decomposition (Geman et al., 1992) → Regularisation (L1/L2, dropout) → "
       "Double-descent discovered (2019)"),
))

blocks.append(heading3("Classical vs Modern Deep Learning"))
blocks.append(table(
    4,
    table_row(["Dimension", "Classical (Pre-2000)", "Modern DL", ""]),
    table_row([
        "Overfitting definition",
        "Model complexity > data size",
        "Same, but models now have billions of params",
        "",
    ]),
    table_row([
        "Main fix",
        "Regularisation, pruning, early stopping",
        "Same + over-parameterisation surprisingly helps",
        "",
    ]),
    table_row([
        "Theoretical tool",
        "VC dimension, Rademacher complexity",
        "PAC-Bayes, NTK, double-descent",
        "",
    ]),
    table_row([
        "Modern twist",
        "—",
        "Interpolating models can still generalise (double-descent)",
        "",
    ]),
))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — CORE CONCEPTS & THEORY
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("🧠 Core Concepts & Theory"))

blocks.append(heading3("Underfitting (High Bias)"))
blocks.append(para(
    rt("Model too simple. Cannot capture true pattern. Both train and test error high."),
))
blocks.append(equation_block(r"\text{Bias}^2[\hat{y}] = \left(\mathbb{E}[\hat{y}] - f(x)\right)^2"))

blocks.append(heading3("Overfitting (High Variance)"))
blocks.append(para(
    rt("Model too complex. Memorises training noise. Train error → 0, test error ↑."),
))
blocks.append(equation_block(r"\text{Var}[\hat{y}] = \mathbb{E}\!\left[(\hat{y} - \mathbb{E}[\hat{y}])^2\right]"))

blocks.append(heading3("Irreducible Error"))
blocks.append(para(
    eq(r"\sigma^2"),
    rt(" — noise inherent in data; cannot be reduced."),
))

blocks.append(heading3("Total Expected Loss (Bias-Variance-Noise Decomposition)"))
blocks.append(equation_block(
    r"\mathbb{E}\!\left[(y - \hat{y})^2\right] = \text{Bias}^2[\hat{y}] + \text{Var}[\hat{y}] + \sigma^2"
))

blocks.append(heading3("Capacity / VC Dimension"))
blocks.append(para(
    rt("The number of distinct patterns a model class can shatter. A polynomial of degree "),
    eq(r"d"),
    rt(" has VC dimension "),
    eq(r"d + 1"),
    rt("."),
))

blocks.append(callout(
    "🔑",
    rt("Key insight: ", bold=True),
    rt("The bias-variance tradeoff is not a law of nature — it's a property of fixed-size datasets. "
       "With infinite data, complex models always win."),
))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — ARCHITECTURE & INTERNAL WORKINGS
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("⚙️ Architecture & Internal Workings (PhD-Level)"))

blocks.append(heading3("Training Error vs Test Error"))

blocks.append(para(rt("Training error (empirical risk):")))
blocks.append(equation_block(
    r"R_{\text{emp}}(h) = \frac{1}{n} \sum_{i=1}^{n} L\!\left(y_i,\, h(x_i)\right)"
))

blocks.append(para(rt("Expected test error (true risk):")))
blocks.append(equation_block(
    r"R(h) = \mathbb{E}_{x,y}\!\left[L\!\left(y,\, h(x)\right)\right]"
))

blocks.append(para(rt("Generalisation gap:")))
blocks.append(equation_block(
    r"R(h) - R_{\text{emp}}(h) \;\geq\; 0 \quad \text{(almost always)}"
))

blocks.append(heading3("Numerical Trace — Polynomial Regression"))
blocks.append(para(
    rt("n = 30 samples from ", italic=True),
    eq(r"\sin(x) + \varepsilon"),
    rt(":"),
))
blocks.append(bullet(
    rt("Degree 1:  ", code=True), rt("Train MSE = 0.38, Test MSE = 0.40"),
    rt(" — Can't fit the curve. Bias dominates."),
))
blocks.append(bullet(
    rt("Degree 3:  ", code=True), rt("Train MSE = 0.15, Test MSE = 0.21"),
    rt(" — Getting better."),
))
blocks.append(bullet(
    rt("Degree 6:  ", code=True), rt("Train MSE = 0.04, Test MSE = 0.12"),
    rt(" — Sweet spot. Bias and variance balanced."),
))
blocks.append(bullet(
    rt("Degree 10: ", code=True), rt("Train MSE = 0.010, Test MSE = 0.26"),
    rt(" — Overfitting visible — test diverges."),
))
blocks.append(bullet(
    rt("Degree 15: ", code=True), rt("Train MSE = 0.001, Test MSE = 0.82"),
    rt(" — Catastrophic overfitting. 30 params, 30 data points = interpolation."),
))

blocks.append(heading3("Capacity Control Methods"))
blocks.append(numbered(
    rt("Regularisation: ", bold=True),
    rt("Add penalty to loss. L2: "),
    eq(r"\lambda\|w\|^2"),
    rt(". L1: "),
    eq(r"\lambda\|w\|_1"),
    rt(". Ridge shrinks coefficients, Lasso zeros them."),
))
blocks.append(numbered(
    rt("Early Stopping: ", bold=True),
    rt("Monitor validation loss during training. Stop when it starts rising."),
))
blocks.append(numbered(
    rt("Cross-Validation: ", bold=True),
    rt("k-fold CV estimates test error without a held-out set. "
       "Choose the complexity with best CV score."),
))
blocks.append(numbered(
    rt("Dropout: ", bold=True),
    rt("Randomly zeroes neurons during training (equivalent to ensemble of thinner networks)."),
))
blocks.append(numbered(
    rt("Data Augmentation: ", bold=True),
    rt("Artificially expand training set — reduces effective model-to-data ratio."),
))

blocks.append(heading3("Double-Descent (Brief)"))
blocks.append(para(
    rt("Beyond the classical U-shape, modern over-parameterised models (more parameters than data "
       "points) show a second descent. At the "),
    rt("interpolation threshold", bold=True),
    rt(" (params ≈ data), test error peaks. Then, as parameters increase further "
       "(over-parameterised), test error decreases again — because gradient descent finds the "
       "minimum-norm interpolating solution, which generalises."),
))
blocks.append(callout(
    "🔬",
    rt("Key insight: ", bold=True),
    rt("Classical bias-variance thinking breaks down in the over-parameterised regime."),
))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — THE MATH
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("📐 The Math"))

blocks.append(heading3("Bias-Variance Decomposition — Full Derivation"))
blocks.append(para(
    rt("Let "),
    eq(r"f(x)"),
    rt(" be the true function, "),
    eq(r"y = f(x) + \varepsilon"),
    rt(" where "),
    eq(r"\varepsilon \sim \mathcal{N}(0, \sigma^2)"),
    rt(". Let "),
    eq(r"\hat{y} = h_D(x)"),
    rt(" be the model trained on dataset "),
    eq(r"D"),
    rt("."),
))

blocks.append(equation_block(
    r"\mathbb{E}_D\!\left[(y - \hat{y})^2\right]"
    r"= \mathbb{E}_D\!\left[(f(x) + \varepsilon - \hat{y})^2\right]"
))
blocks.append(equation_block(
    r"= \mathbb{E}_D\!\left[(f(x) - \hat{y})^2\right] + \sigma^2"
    r"\quad \text{(since } \varepsilon \text{ independent of } D\text{)}"
))
blocks.append(equation_block(
    r"= \mathbb{E}_D\!\left[\left(f(x) - \mathbb{E}_D[\hat{y}] + \mathbb{E}_D[\hat{y}] - \hat{y}\right)^2\right] + \sigma^2"
))
blocks.append(equation_block(
    r"= \underbrace{\left(f(x) - \mathbb{E}_D[\hat{y}]\right)^2}_{\text{Bias}^2[\hat{y}]}"
    r"+ \underbrace{\mathbb{E}_D\!\left[(\mathbb{E}_D[\hat{y}] - \hat{y})^2\right]}_{\text{Var}[\hat{y}]}"
    r"+ \sigma^2"
))
blocks.append(para(
    rt("The cross term "),
    eq(r"\mathbb{E}_D\!\left[(f(x) - \mathbb{E}_D[\hat{y}])(\mathbb{E}_D[\hat{y}] - \hat{y})\right] = 0"),
    rt(" since "),
    eq(r"\mathbb{E}_D[\hat{y}] - \hat{y}"),
    rt(" has zero mean."),
))

blocks.append(heading3("VC Generalisation Bound"))
blocks.append(para(
    rt("With probability "),
    eq(r"\geq 1 - \delta"),
    rt(", for all "),
    eq(r"h \in \mathcal{H}"),
    rt(" with VC dimension "),
    eq(r"d"),
    rt(":"),
))
blocks.append(equation_block(
    r"R(h) \;\leq\; R_{\text{emp}}(h) + \sqrt{\frac{d\!\left(\ln\!\tfrac{2n}{d} + 1\right) + \ln\!\tfrac{4}{\delta}}{n}}"
))

blocks.append(heading3("Structural Risk Minimisation (Vapnik)"))
blocks.append(equation_block(
    r"h^* = \arg\min_{h}\;\left[R_{\text{emp}}(h) + \Omega\!\left(\text{complexity}(h)\right)\right]"
))
blocks.append(para(
    rt("where "),
    eq(r"\Omega"),
    rt(" is a monotone complexity penalty."),
))

blocks.append(heading3("Ridge Regression — Closed Form"))
blocks.append(equation_block(
    r"\hat{w}_{\text{ridge}} = \arg\min_{w}\;\|y - Xw\|^2 + \lambda\|w\|^2"
))
blocks.append(equation_block(
    r"= (X^\top X + \lambda I)^{-1} X^\top y"
))
blocks.append(para(
    rt("As "),
    eq(r"\lambda \to \infty"),
    rt(": "),
    eq(r"\hat{w} \to 0"),
    rt(" (maximum regularisation). As "),
    eq(r"\lambda \to 0"),
    rt(": "),
    eq(r"\hat{w} \to \hat{w}_{\text{OLS}}"),
    rt("."),
))

blocks.append(callout(
    "⚠️",
    rt("Warning: ", bold=True),
    rt("High training accuracy ≠ good generalisation. A degree-15 polynomial on 30 points achieves "
       "train MSE ≈ 0 but test MSE ≈ 0.82. Always evaluate on held-out data."),
))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — CODE IMPLEMENTATION
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("💻 Code Implementation"))

blocks.append(heading3("6a — From Scratch (NumPy Polynomial Regression + Bias-Variance Analysis)"))

_code_scratch = '''\
import numpy as np
import matplotlib.pyplot as plt

# --- Generate data ---
np.random.seed(42)
n = 30
x_train = np.linspace(0, 1, n)
y_train = np.sin(2 * np.pi * x_train) + np.random.randn(n) * 0.3
x_test = np.linspace(0, 1, 200)
y_test = np.sin(2 * np.pi * x_test)

def fit_polynomial(x_tr, y_tr, degree):
    """Fit polynomial via NumPy least-squares."""
    # Design matrix: [1, x, x^2, ..., x^d]
    X = np.vander(x_tr, degree + 1, increasing=True)  # shape (n, d+1)
    # Solve normal equations (no regularisation)
    coeffs = np.linalg.lstsq(X, y_tr, rcond=None)[0]
    return coeffs

def predict_polynomial(x, coeffs):
    degree = len(coeffs) - 1
    X = np.vander(x, degree + 1, increasing=True)
    return X @ coeffs

# --- Bias-Variance sweep ---
degrees = range(1, 16)
train_errors, test_errors = [], []

for d in degrees:
    coeffs = fit_polynomial(x_train, y_train, d)
    y_hat_train = predict_polynomial(x_train, coeffs)
    y_hat_test  = predict_polynomial(x_test, coeffs)

    train_mse = np.mean((y_train - y_hat_train) ** 2)
    test_mse  = np.mean((y_test  - y_hat_test ) ** 2)

    train_errors.append(train_mse)
    test_errors.append(test_mse)
    print(f"Degree {d:2d}: Train MSE={train_mse:.4f}  Test MSE={test_mse:.4f}")

# Optimal degree
best_degree = degrees[np.argmin(test_errors)]
print(f"\\nBest degree (lowest test MSE): {best_degree}")
'''

blocks.append(code_block("python", _code_scratch))

blocks.append(heading3("6b — Production (sklearn with Cross-Validation)"))

_code_prod = '''\
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV
import numpy as np

# Proper complexity selection via CV
param_grid = {
    "poly__degree": range(1, 16),
    "ridge__alpha": [0.001, 0.01, 0.1, 1.0, 10.0],
}

pipe = Pipeline([
    ("poly", PolynomialFeatures(include_bias=True)),
    ("ridge", Ridge()),
])

# 5-fold cross-validation to find optimal (degree, alpha)
search = GridSearchCV(pipe, param_grid, cv=5, scoring="neg_mean_squared_error")
search.fit(X_train, y_train)

print(f"Best params: {search.best_params_}")
print(f"Best CV MSE: {-search.best_score_:.4f}")
# Gotcha: degree + regularisation interact.
# A high degree with strong Ridge can outperform a lower degree with no regularisation.
'''

blocks.append(code_block("python", _code_prod))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — INTERVIEW DEEP-DIVE
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("🎤 Interview Deep-Dive"))

# Q1
blocks.append(toggle(
    [rt("Q1 (Easy): ", bold=True), rt("What is overfitting and how do you detect it?")],
    [
        para(
            rt("Overfitting = model performs well on training data but poorly on new data. "),
            rt("Detect: ", bold=True),
            rt("training loss ≪ validation loss. The gap between them is the generalisation gap."),
        ),
    ],
))

# Q2
blocks.append(toggle(
    [rt("Q2 (Medium): ", bold=True), rt("Explain the bias-variance tradeoff.")],
    [
        para(
            rt("For any model: "),
        ),
        equation_block(
            r"\mathbb{E}[\text{Test Loss}] = \text{Bias}^2 + \text{Variance} + \text{Noise}"
        ),
        para(
            rt("Simple models have "),
            rt("high bias", bold=True),
            rt(" (can't fit), low variance (stable). Complex models have "),
            rt("low bias", bold=True),
            rt(" (fit well), high variance (sensitive to data). Optimal is the minimum of "),
            eq(r"\text{Bias}^2 + \text{Variance}"),
            rt("."),
        ),
    ],
))

# Q3
blocks.append(toggle(
    [rt("Q3 (Medium): ", bold=True), rt("How does regularisation reduce overfitting?")],
    [
        para(
            rt("L2 (Ridge): adds "),
            eq(r"\lambda\|w\|^2"),
            rt(" to loss → shrinks all weights toward zero → reduces effective degrees of freedom "
               "→ effectively reduces model complexity. The closed-form solution becomes:"),
        ),
        equation_block(r"(X^\top X + \lambda I)^{-1} X^\top y"),
        para(
            rt("As "),
            eq(r"\lambda"),
            rt(" increases, the effective VC dimension decreases."),
        ),
    ],
))

# Q4
blocks.append(toggle(
    [rt("Q4 (Hard): ", bold=True),
     rt("What is double-descent and why does it matter for deep learning?")],
    [
        para(
            rt("Classical U-shaped test error assumes you stop at the interpolation threshold. "
               "Modern findings (Belkin et al., 2019) show: if you continue increasing parameters "
               "past the point where train error = 0, test error first "),
            rt("peaks", bold=True),
            rt(" (interpolation threshold) then "),
            rt("decreases again", bold=True),
            rt(" (second descent). This explains why billion-parameter models generalise despite "
               "having more params than data. The minimum-norm interpolating solution found by "
               "gradient descent has implicit regularisation."),
        ),
    ],
))

# Q5
blocks.append(toggle(
    [rt("Q5 (Hard): ", bold=True),
     rt("What does VC dimension measure and how does it bound generalisation?")],
    [
        para(
            rt("VC dim of hypothesis class "),
            eq(r"\mathcal{H}"),
            rt(" = largest "),
            eq(r"n"),
            rt(" such that "),
            eq(r"\mathcal{H}"),
            rt(" can 'shatter' "),
            eq(r"n"),
            rt(" points (produce any labelling). It measures capacity. Generalisation bound:"),
        ),
        equation_block(
            r"R(h) \;\leq\; R_{\text{emp}}(h) + \mathcal{O}\!\left(\sqrt{\frac{d}{n}}\right)"
        ),
        para(
            rt("where "),
            eq(r"d"),
            rt(" = VC dim, "),
            eq(r"n"),
            rt(" = data size. Larger "),
            eq(r"d"),
            rt(" → looser bound → more data needed to ensure generalisation. "
               "A class is PAC-learnable iff its VC dim is finite."),
        ),
    ],
))

blocks.append(heading3("PhD Researcher Perspective"))
blocks.append(para(
    rt("The bias-variance decomposition is a consequence of the bias-variance-noise decomposition "
       "of squared loss. For squared loss under the Bayesian predictive risk framework, the optimal "
       "predictor is "),
    eq(r"\mathbb{E}[y \mid x]"),
    rt(", and the decomposition holds pointwise in "),
    eq(r"x"),
    rt(". The expected test MSE decomposes into: (1) the squared bias of the model class, "
       "(2) the estimation variance due to finite data, and (3) the irreducible noise "),
    eq(r"\sigma^2"),
    rt(". Structural Risk Minimisation minimises an empirical proxy for "),
    eq(r"R(h)"),
    rt(" by choosing the smallest consistent hypothesis class."),
))

blocks.append(heading3("Research Scientist / Engineer Perspective"))
blocks.append(para(
    rt("In practice: train multiple model sizes, plot train and val loss, pick the elbow of the "
       "val loss U-curve. Use regularisation (weight decay, dropout) to push the sweet spot toward "
       "larger models without overfitting. Learning rate schedule and early stopping are implicit "
       "complexity controls."),
))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 8 — COMPARISON & TRADE-OFFS
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("⚖️ Comparison & Trade-Offs"))

blocks.append(table(
    5,
    table_row(["Method", "Reduces Variance", "Reduces Bias", "New Hyperparams", "Best For"]),
    table_row(["L2 Regularisation (Ridge)", "Yes", "Slightly", "λ", "Linear / polynomial models"]),
    table_row(["L1 Regularisation (Lasso)", "Yes", "Slightly", "λ", "Feature selection"]),
    table_row(["Early Stopping",            "Yes", "No",       "patience",      "Neural networks"]),
    table_row(["Dropout",                   "Yes", "No",       "drop rate",     "Deep networks"]),
    table_row(["Cross-Validation",          "Diagnostic", "—", "k-folds",       "Any model selection"]),
    table_row(["Data Augmentation",         "Yes", "No",       "—",             "CV, NLP"]),
    table_row(["Ensemble (Bagging)",        "Yes (much)", "No", "n_estimators", "High-variance models"]),
    table_row(["Boosting",                  "No",  "Yes (much)", "n_estimators, lr", "High-bias models"]),
))

blocks.append(callout(
    "🔍",
    rt("Decision guide: ", bold=True),
    rt("If train error ≪ test error → overfit → add regularisation or more data. "
       "If both errors are high → underfit → increase model capacity or improve features. "
       "If test error is at its U-curve minimum → stop increasing complexity."),
))

blocks.append(heading3("When to Increase Complexity"))
blocks.append(bullet(rt("Small generalisation gap, both train and test error still high.")))
blocks.append(bullet(rt("You have enough data to support the additional parameters.")))

blocks.append(heading3("When NOT to Increase Complexity"))
blocks.append(bullet(rt("Validation loss rising while train loss is still falling.")))
blocks.append(bullet(rt("Train accuracy near 100% but validation accuracy low.")))
blocks.append(bullet(rt("Small dataset — prefer simpler models or stronger regularisation.")))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 9 — INTERACTIVE VISUAL EXPLAINER
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("🎨 Interactive Visual Explainer"))

blocks.append(embed(EXPLAINER_URL))

blocks.append(divider())

# ─────────────────────────────────────────────────────────────────────────────
# SECTION 10 — RELATED TOPICS
# ─────────────────────────────────────────────────────────────────────────────
blocks.append(heading2("🔗 Related Topics"))

blocks.append(heading3("Prerequisites"))
blocks.append(para(
    rt("Linear Regression, Loss Functions, Train/Val/Test Split, Gradient Descent"),
))

blocks.append(heading3("What to Learn Next"))
blocks.append(para(
    rt("Regularisation (L1/L2), Cross-Validation, Ensemble Methods, "
       "Neural Network Training Dynamics, Double-Descent in Deep Learning"),
))

blocks.append(heading3("Key Papers"))
blocks.append(numbered(
    rt("Vapnik & Chervonenkis (1971) — VC dimension"),
))
blocks.append(numbered(
    rt("Geman et al. (1992) — Bias-Variance Decomposition — "),
    rt("Neural Computation", italic=True),
))
blocks.append(numbered(
    rt("Belkin et al. (2019) — Reconciling modern ML practice and the classical "
       "bias-variance tradeoff — "),
    rt("PNAS", italic=True),
))
blocks.append(numbered(
    rt("Zhang et al. (2017) — Understanding deep learning requires rethinking generalization — "),
    rt("ICLR", italic=True),
))

blocks.append(heading3("Resources"))
blocks.append(bullet(
    rt("Bishop, "),
    rt("Pattern Recognition and Machine Learning", italic=True),
    rt(" Ch. 3 (polynomial regression example)"),
))
blocks.append(bullet(
    rt("Hastie, Tibshirani, Friedman — "),
    rt("The Elements of Statistical Learning", italic=True),
    rt(" Ch. 2 & 7"),
))
blocks.append(bullet(
    rt("Belkin et al. 2019 (double-descent)"),
))
blocks.append(bullet(
    rt("Andrew Ng's ML course — bias-variance lecture"),
))

# ══════════════════════════════════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    update_page(PAGE_ID, ICON, PROPERTIES, blocks)
