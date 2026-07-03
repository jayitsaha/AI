#!/usr/bin/env python3
"""Update Notion page for: Friedman's GBM — Stagewise Additive Modeling"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-813b-914b-e0d908fe8dc8"
ICON = "🟠"  # Advanced
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/friedman_gbm_stagewise_explainer.html"

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: 30-Second Version ──────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Gradient Boosting Machines (GBM), introduced by Jerome Friedman in 2001, build a predictive model by adding many simple models — shallow decision trees — one at a time. Each new tree is trained not on the original labels, but on the "), rt("errors", bold=True), rt(" of the current combined model: specifically, the negative gradient of the loss function. The result is a powerful ensemble that is the engine inside XGBoost, LightGBM, and CatBoost.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine a committee of advisors forecasting next quarter's revenue. The first advisor makes a rough guess. The second advisor ignores the first's output entirely — instead, they study only "), rt("what the first got wrong", italic=True), rt(" and correct those mistakes. The third corrects what both got wrong. Each specialist focuses on residual errors; together they converge on an accurate forecast. That is forward stagewise additive modeling.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("GBM fits each new tree to the negative gradient of the loss — called pseudo-residuals — not to the raw targets. This turns boosting into gradient descent in function space.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("AdaBoost (Freund & Schapire, 1997) was the first practical boosting algorithm and proved that weak learners can be combined into a strong one. However, AdaBoost is tied to exponential loss and provides no mechanism for using arbitrary loss functions (e.g., absolute error, Huber, logistic loss for calibrated probabilities).")),
    heading3("Friedman's Insight"),
    para(rt("Leo Breiman (1997) first noted that AdaBoost is gradient descent in function space. Friedman formalised this into a general algorithm — "), rt("Gradient Boosting", bold=True), rt(" — that works for any differentiable loss, framed as "), rt("forward stagewise additive modeling (FSAM)", italic=True), rt(". The additive model is:")),
    equation_block(r"F(x) = \sum_{m=0}^{M} \nu \cdot h_m(x)"),
    para(rt("where each "), eq(r"h_m"), rt(" is a regression tree and "), eq(r"\nu \in (0,1]"), rt(" is the shrinkage (learning rate). Trees are added one at a time; previously fitted trees are never modified.")),
    heading3("Key Papers"),
    bullet(rt("Friedman, J. (2001). "), rt("Greedy function approximation: A gradient boosting machine", italic=True), rt(". Annals of Statistics, 29(5). [The foundational paper — defines the full algorithm for arbitrary loss]")),
    bullet(rt("Friedman, J. (2002). "), rt("Stochastic gradient boosting", italic=True), rt(". Computational Statistics & Data Analysis. [Adds row subsampling for regularisation and speed]")),
    bullet(rt("Breiman, L. (1997). "), rt("Prediction games and arcing algorithms", italic=True), rt(". [First connects AdaBoost to gradient descent]")),
    heading3("Before vs After"),
    table(4,
        table_row(["Dimension", "AdaBoost (Before)", "Friedman GBM (After)", "XGBoost/LGBM (Extension)"]),
        table_row(["Loss function", "Exponential only", "Any differentiable L", "Any + 2nd-order approx"]),
        table_row(["Gradient order", "1st (implicit)", "1st (negative gradient)", "2nd (Newton step)"]),
        table_row(["Weak learner", "Binary classifier", "Regression tree", "Regression tree + regularised"]),
        table_row(["Shrinkage", "No", "Yes (ν)", "Yes (η)"]),
        table_row(["Subsampling", "No", "Optional (stochastic GBM)", "Row + column"]),
        table_row(["Theoretical framing", "Weight resampling", "Functional gradient descent", "Regularised objective + approx"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Forward Stagewise Additive Modeling (FSAM)"),
    para(rt("FSAM builds the additive expansion by greedily solving, at each stage "), eq(r"m"), rt(":")),
    equation_block(r"(h_m, \gamma_m) = \underset{h, \gamma}{\operatorname{argmin}} \sum_{i=1}^n L\!\left(y_i,\; F_{m-1}(x_i) + \gamma \cdot h(x_i)\right)"),
    para(rt("This is intractable for arbitrary "), eq(r"h"), rt(" (tree search is NP-hard for depth > 1). Friedman's approximation: replace exact minimisation with one step of steepest descent in function space.")),
    heading3("Functional Gradient Descent"),
    para(rt("Think of the training predictions "), eq(r"F(x_1), \ldots, F(x_n)"), rt(" as "), eq(r"n"), rt(" free parameters. The gradient of total loss with respect to these parameters is:")),
    equation_block(r"g_{im} = \left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F = F_{m-1}}"),
    para(rt("The "), rt("pseudo-residuals", bold=True), rt(" are the negative gradient:")),
    equation_block(r"r_{im} = -g_{im} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F = F_{m-1}}"),
    para(rt("A regression tree fitted to "), eq(r"\{(x_i, r_{im})\}"), rt(" approximates this negative gradient direction. Adding the tree (with shrinkage "), eq(r"\nu"), rt(") takes one gradient descent step in function space.")),
    heading3("Loss-Specific Pseudo-Residuals"),
    table(3,
        table_row(["Loss L(y, F)", "Formula", "Pseudo-residual rᵢₘ"]),
        table_row(["Squared error ½(y−F)²", "Regression", "y − F (ordinary residual)"]),
        table_row(["Absolute error |y−F|", "Robust regression", "sign(y − F)"]),
        table_row(["Log-loss y log p + (1−y) log(1−p)", "Classification", "y − p = y − σ(F)"]),
        table_row(["Huber (δ-threshold)", "Robust regression", "Clipped residual"]),
        table_row(["Poisson: y·F − eᶠ", "Count data", "y − eᶠ"]),
    ),
    callout("🔑", rt("Key property: ", bold=True), rt("For "), eq(r"L = \frac{1}{2}(y-F)^2"), rt(", pseudo-residuals equal ordinary residuals "), eq(r"y_i - F_{m-1}(x_i)"), rt(". This equivalence only holds for squared-error loss.")),
    divider(),

    # ── Section 4: Architecture Deep-Dive ─────────────────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD-Level)"),
    heading3("The Full Algorithm"),
    para(rt("Algorithm 1 (Friedman 2001) — Gradient Boost:")),
    numbered(rt("Initialise: "), eq(r"F_0(x) = \underset{\gamma}{\operatorname{argmin}} \sum_{i=1}^n L(y_i, \gamma)")),
    numbered(rt("For "), eq(r"m = 1, \ldots, M"), rt(":")),
    bullet(rt("(a) Compute pseudo-residuals: "), eq(r"r_{im} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F=F_{m-1}}")),
    bullet(rt("(b) Fit regression tree "), eq(r"h_m"), rt(" to "), eq(r"\{(x_i, r_{im})\}_{i=1}^n"), rt(", producing leaf regions "), eq(r"\{R_{jm}\}_{j=1}^J")),
    bullet(rt("(c) Compute optimal leaf values: "), eq(r"\gamma_{jm} = \underset{\gamma}{\operatorname{argmin}} \sum_{x_i \in R_{jm}} L\!\left(y_i,\; F_{m-1}(x_i) + \gamma\right)")),
    bullet(rt("(d) Update: "), eq(r"F_m(x) = F_{m-1}(x) + \nu \sum_{j=1}^J \gamma_{jm} \,\mathbf{1}[x \in R_{jm}]")),
    heading3("Why Separate Steps (b) and (c)?"),
    para(rt("Step (b) finds the "), rt("tree structure", italic=True), rt(" (which features to split on, at which thresholds) by fitting to pseudo-residuals with squared-error. This is always possible since regression trees minimise squared-error by design.")),
    para(rt("Step (c) then re-fits the "), rt("leaf values", italic=True), rt(" to minimise the actual loss (not squared-error on residuals). For squared-error loss, "), eq(r"\gamma_{jm} = \text{mean}(r_{im})"), rt(" in leaf "), eq(r"j"), rt(". For logloss, a one-step Newton approximation is used:")),
    equation_block(r"\gamma_{jm}^{\text{Newton}} = \frac{\sum_{x_i \in R_{jm}} r_{im}}{\sum_{x_i \in R_{jm}} p_i(1-p_i)}"),
    para(rt("This two-step split is Friedman's key practical trick: use squared-error to build the structure (fast, always works), then re-optimise leaf values for the true loss (cheap once structure is fixed).")),
    heading3("Shrinkage ν — Information Flow"),
    para(rt("Shrinkage is applied "), rt("every stage", bold=True), rt(", scaling down each tree's contribution. Without shrinkage ("), eq(r"\nu = 1"), rt("), GBM memorises training data quickly. With small "), eq(r"\nu"), rt(", the model approaches the solution gradually — more stages are needed but each is less likely to overfit a single noisy gradient step.")),
    para(rt("The effective trade-off: ")),
    equation_block(r"\text{MSE test error} \approx f\!\left(\frac{M \cdot \nu}{\text{regularisation}}\right)"),
    para(rt("Doubling "), eq(r"M"), rt(" while halving "), eq(r"\nu"), rt(" yields approximately the same test error — a useful tuning heuristic.")),
    heading3("Leaf Count J — Interaction Depth"),
    para(rt("A tree with "), eq(r"J"), rt(" leaves can represent at most "), eq(r"J-1"), rt(" splits, modelling interactions between "), eq(r"\lfloor \log_2 J \rfloor"), rt(" features. Friedman recommends "), eq(r"J \in [4, 8]"), rt(" for most real-world data. Stumps ("), eq(r"J=2"), rt(") model only main effects — suitable as a sanity check or for very regularised fits.")),
    callout("⚙️", rt("Design decision: ", bold=True), rt("Why not just use ordinary gradient descent on weights? Because trees provide "), rt("variable selection", italic=True), rt(" automatically — the split criteria ignore irrelevant features. Parameter-space gradient descent would require explicit feature selection and cannot handle mixed types or missing values as naturally.")),
    divider(),

    # ── Section 5: The Math ────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Functional Gradient Descent — Formal Derivation"),
    para(rt("Define the empirical risk as a function of the vector of predictions "), eq(r"\mathbf{F} = (F(x_1), \ldots, F(x_n)) \in \mathbb{R}^n"), rt(":")),
    equation_block(r"\mathcal{L}(\mathbf{F}) = \sum_{i=1}^n L(y_i, F(x_i))"),
    para(rt("The steepest descent direction in "), eq(r"\mathbb{R}^n"), rt(" is "), eq(r"-\nabla_\mathbf{F} \mathcal{L}"), rt(". Its "), eq(r"i"), rt("-th component:")),
    equation_block(r"-\frac{\partial \mathcal{L}}{\partial F(x_i)} = -\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)} = r_{im}"),
    para(rt("We cannot take this step directly in function space (we need a function, not just an "), eq(r"n"), rt("-vector). So we project: fit a regression tree "), eq(r"h_m"), rt(" to minimise the squared distance to the pseudo-residual vector:")),
    equation_block(r"h_m = \underset{h \in \mathcal{H}}{\operatorname{argmin}} \sum_{i=1}^n \left(r_{im} - h(x_i)\right)^2"),
    para(rt("This is the "), rt("projection of the gradient onto the hypothesis class", italic=True), rt(" "), eq(r"\mathcal{H}"), rt(" of regression trees. Then the update is a gradient step of size "), eq(r"\nu"), rt(" in function space:")),
    equation_block(r"F_m = F_{m-1} + \nu \cdot h_m"),
    heading3("Convergence"),
    para(rt("For convex "), eq(r"L"), rt(" and sufficient "), eq(r"M"), rt(", GBM converges to the optimal function. However, for finite "), eq(r"M"), rt(" and small trees (weak learners), the generalisation bound follows from the bias-variance decomposition: small "), eq(r"\nu"), rt(" keeps bias high initially but variance low, while large "), eq(r"M"), rt(" reduces bias.")),
    heading3("Squared-Error Loss — Full Derivation"),
    para(rt("With "), eq(r"L(y, F) = \tfrac{1}{2}(y - F)^2"), rt(":")),
    equation_block(r"\frac{\partial L}{\partial F} = F - y \implies r_{im} = y_i - F_{m-1}(x_i)"),
    para(rt("Optimal leaf value (step c): minimise "), eq(r"\sum_{i \in R_j} \tfrac{1}{2}(y_i - F_{m-1}(x_i) - \gamma)^2"), rt(" over "), eq(r"\gamma"), rt(":")),
    equation_block(r"\gamma_{jm} = \frac{1}{|R_j|} \sum_{i \in R_j} r_{im} = \bar{r}_j"),
    para(rt("The optimal leaf value is simply the mean of residuals in the leaf — so for squared-error, GBM reduces to iteratively fitting trees to residuals, which is the intuition often stated (but only valid for this loss).")),
    heading3("Logloss — Newton Leaf Values"),
    para(rt("With "), eq(r"L(y, F) = -y \log \sigma(F) - (1-y) \log(1-\sigma(F))"), rt(", where "), eq(r"\sigma(F) = 1/(1+e^{-F})"), rt(":")),
    equation_block(r"r_{im} = y_i - \sigma(F_{m-1}(x_i)) = y_i - p_i"),
    para(rt("Optimal leaf value (one Newton step):")),
    equation_block(r"\gamma_{jm} = \frac{\sum_{i \in R_j}(y_i - p_i)}{\sum_{i \in R_j} p_i(1-p_i)}"),
    callout("⚠️", rt("Warning: ", bold=True), rt("The tree structure in step (b) is still found by fitting to "), eq(r"r_{im}"), rt(" with squared-error. Only the leaf values in step (c) use the true loss. This approximation is a practical compromise; XGBoost extends Friedman's approach by also using 2nd-order information to find better splits.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", '''\
import numpy as np
from sklearn.tree import DecisionTreeRegressor

class GradientBoostingFromScratch:
    """Friedman's GBM for squared-error loss — pure NumPy + sklearn trees."""

    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.M = n_estimators
        self.nu = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.F0 = None  # initial constant

    # -- Loss and gradient (squared-error) -----------------------------------
    def _loss(self, y, F):
        return 0.5 * np.mean((y - F) ** 2)

    def _negative_gradient(self, y, F):
        """Pseudo-residuals = negative gradient of squared-error loss."""
        return y - F  # r_im = y_i - F_{m-1}(x_i)

    def fit(self, X, y):
        n = len(y)
        # Step 0: initialise with best constant (mean for squared-error)
        self.F0 = np.mean(y)
        F = np.full(n, self.F0)

        for m in range(self.M):
            # Step (a): compute pseudo-residuals
            r = self._negative_gradient(y, F)

            # Step (b): fit regression tree to pseudo-residuals
            tree = DecisionTreeRegressor(max_depth=self.max_depth)
            tree.fit(X, r)
            leaf_ids = tree.apply(X)  # which leaf each sample lands in

            # Step (c): re-optimise leaf values for true loss
            # For squared-error, leaf mean of residuals is optimal
            leaf_means = {}
            for leaf in np.unique(leaf_ids):
                mask = leaf_ids == leaf
                leaf_means[leaf] = np.mean(r[mask])  # = argmin sum L(y_i, F+gamma)

            # Overwrite tree leaf values (hack: directly set tree internals)
            # In practice sklearn's predict already gives leaf means of RESIDUALS
            # which is what we want. So tree.predict(X) ≈ our leaf means.
            self.trees.append(tree)

            # Step (d): update model
            F = F + self.nu * tree.predict(X)

            if (m + 1) % 20 == 0:
                print(f"  Stage {m+1:3d}  MSE={self._loss(y, F):.6f}")

        return self

    def predict(self, X):
        F = np.full(len(X), self.F0)
        for tree in self.trees:
            F += self.nu * tree.predict(X)
        return F

# --- Toy example ---
rng = np.random.default_rng(42)
X = rng.uniform(-3, 3, (200, 1))
y = np.sin(X[:, 0]) + rng.normal(0, 0.1, 200)

model = GradientBoostingFromScratch(n_estimators=100, learning_rate=0.1, max_depth=3)
model.fit(X, y)
preds = model.predict(X)
print(f"Final train MSE: {np.mean((y - preds)**2):.4f}")
'''),
    heading3("6b — Production (sklearn)"),
    code_block("python", '''\
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
import numpy as np

# ── Regression example ──────────────────────────────────────────────────────
X, y = make_regression(n_samples=1000, n_features=20, noise=10, random_state=42)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

reg = GradientBoostingRegressor(
    n_estimators=300,       # M: total trees — use more with smaller learning_rate
    learning_rate=0.05,     # ν: shrinkage — smaller = more regularisation
    max_depth=4,            # J-1 splits; J=2^depth leaves (depth-limited)
    subsample=0.8,          # stochastic GBM: row fraction per stage
    min_samples_leaf=10,    # min samples per leaf — prevents overfitting small leaves
    max_features=0.8,       # column subsampling per split (Friedman 2002 extension)
    loss="squared_error",   # also: "absolute_error", "huber", "quantile"
    n_iter_no_change=20,    # early stopping: halt if val loss doesn't improve
    validation_fraction=0.1,
    random_state=42,
)
reg.fit(X_tr, y_tr)
print(f"Test MSE: {np.mean((reg.predict(X_te) - y_te)**2):.2f}")

# ⚠️ Gotcha 1: n_estimators is NOT automatically optimal — always use early stopping
# ⚠️ Gotcha 2: learning_rate and n_estimators trade off: halve lr, double n_estimators
# ⚠️ Gotcha 3: subsample < 1 gives stochastic GBM (needs larger M)

# ── Classification example ──────────────────────────────────────────────────
Xc, yc = make_classification(n_samples=1000, n_features=20, random_state=42)
clf = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=3,
    subsample=0.8,
    loss="log_loss",  # pseudo-residuals = y - sigma(F)
)
clf.fit(*train_test_split(Xc, yc)[:2])
# clf.predict_proba(X_te) for calibrated probabilities

# ── Feature importance (MDI — mean decrease in impurity) ────────────────────
importances = reg.feature_importances_
# Note: MDI can be biased toward high-cardinality features. Prefer SHAP for production.
'''),
    divider(),

    # ── Section 7: Interview Q&A ───────────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What does GBM do at each boosting stage?", bold=True)], [
        para(rt("At stage "), eq(r"m"), rt(", GBM: (1) computes pseudo-residuals "), eq(r"r_{im} = -\partial L/\partial F(x_i)"), rt(" from the current model "), eq(r"F_{m-1}"), rt("; (2) fits a regression tree to these residuals; (3) re-optimises leaf values for the true loss; (4) adds the tree (scaled by learning rate "), eq(r"\nu"), rt(") to the model: "), eq(r"F_m = F_{m-1} + \nu h_m"), rt(".")),
    ]),
    toggle([rt("Q2 (Easy): Why do we use the negative gradient, not raw residuals?", bold=True)], [
        para(rt("Raw residuals "), eq(r"y_i - F_{m-1}(x_i)"), rt(" are the negative gradient only for squared-error loss. For other losses (logloss, absolute error, Huber), the pseudo-residuals differ. Using the negative gradient generalises boosting to any differentiable loss — that is the core of Friedman's contribution.")),
    ]),
    toggle([rt("Q3 (Medium): What is shrinkage ν and why does it help?", bold=True)], [
        para(rt("Shrinkage multiplies each tree's contribution by "), eq(r"\nu \in (0,1]"), rt(". Mechanistically, it slows down gradient descent in function space — each step is smaller, so the model takes a more conservative path toward the optimum. This acts as regularisation: small "), eq(r"\nu"), rt(" with large "), eq(r"M"), rt(" finds flatter loss minima that generalise better. Empirically, "), eq(r"\nu \leq 0.1"), rt(" with early stopping is almost universally recommended.")),
        para(rt("Follow-up trap: "Is shrinkage equivalent to L2 regularisation?" Answer: No. L2 penalises parameter magnitudes; shrinkage scales the step size at each stage. They have different geometric effects, though both reduce overfitting.")),
    ]),
    toggle([rt("Q4 (Medium): How does GBM differ from AdaBoost?", bold=True)], [
        para(rt("AdaBoost reweights training examples: misclassified points get higher weight, forcing the next learner to focus on them. GBM fits each tree to the "), rt("gradient of the loss", italic=True), rt(" — a more general framework that recovers AdaBoost as a special case when "), eq(r"L"), rt(" is exponential loss.")),
        para(rt("GBM is more flexible (arbitrary loss), more robust to noise (stumps vs. classifiers), and naturally handles regression. AdaBoost requires that weak learners produce a binary decision; GBM requires regression trees only.")),
    ]),
    toggle([rt("Q5 (Hard): Explain to a PhD Researcher — why does functional gradient descent converge?", bold=True)], [
        para(rt("For convex "), eq(r"L"), rt(" and sufficiently expressive "), eq(r"\mathcal{H}"), rt(", the projected gradient step "), eq(r"F_m = F_{m-1} + \nu h_m"), rt(" decreases "), eq(r"\mathcal{L}"), rt(" at each stage (provided the tree approximates the gradient well). The rate depends on: (a) approximation quality of "), eq(r"\mathcal{H}"), rt(" to the gradient, (b) step size "), eq(r"\nu"), rt(", and (c) curvature of "), eq(r"L"), rt(". For non-convex "), eq(r"L"), rt(" (e.g., MART with Huber), convergence to a local minimum is guaranteed, not global.")),
        para(rt("The deeper result (Mason et al., 1999; Friedman 2001) is that boosting can be interpreted as gradient descent in the reproducing kernel Hilbert space (RKHS) of the tree function class, with a step-size "), eq(r"\nu"), rt(" that trades off between fast convergence and approximation error from the tree projection.")),
    ]),
    toggle([rt("Q6 (Hard): Explain to a Research Scientist — how does XGBoost improve on Friedman GBM?", bold=True)], [
        para(rt("Friedman GBM uses only first-order (gradient) information for the tree structure and re-fits leaf values using the true loss. XGBoost (Chen & Guestrin, 2016) adds a regularised objective and uses "), rt("second-order Taylor approximation", italic=True), rt(":")),
        equation_block(r"\tilde{\mathcal{L}}^{(m)} = \sum_i \left[g_i f_m(x_i) + \tfrac{1}{2} h_i f_m^2(x_i)\right] + \Omega(f_m)"),
        para(rt("where "), eq(r"g_i = \partial L / \partial \hat{y}_i"), rt(", "), eq(r"h_i = \partial^2 L / \partial \hat{y}_i^2"), rt(" (Hessian), and "), eq(r"\Omega(f) = \gamma T + \tfrac{1}{2}\lambda \|w\|^2"), rt(" penalises tree complexity. This gives closed-form optimal leaf weights "), eq(r"w_j^* = -G_j / (H_j + \lambda)"), rt(" and exact gain for each split — no re-optimisation step needed. Result: better splits, stable leaf values, and built-in L2 regularisation.")),
    ]),
    heading3("System Design Angle"),
    para(rt("In a production ML system, GBM is often the go-to for tabular data. Key design considerations: (1) hyperparameter search: "), eq(r"\nu"), rt(", "), eq(r"M"), rt(", "), eq(r"J"), rt(" jointly — use Bayesian optimisation with early stopping as the inner loop; (2) drift detection: GBM feature importances shift when distribution changes; (3) serialisation: sklearn's joblib pickling vs ONNX for cross-platform serving; (4) latency: depth-3 tree with 300 estimators processes ~50k predictions/sec on CPU — appropriate for batch but marginal for <10ms online serving.")),
    callout("🚫", rt("Red flag: ", bold=True), rt("Saying 'GBM fits each tree to residuals' — only true for squared-error loss. Interviewers at FAANG probe this distinction. The correct statement is 'GBM fits each tree to the negative gradient of the loss, which equals residuals for squared-error loss only'.")),
    divider(),

    # ── Section 8: Comparisons ─────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Dimension", "Friedman GBM", "XGBoost", "LightGBM", "CatBoost"]),
        table_row(["Gradient order", "1st", "2nd (Newton)", "2nd (Newton)", "2nd (Newton)"]),
        table_row(["Split finding", "Exact (brute force)", "Approximate (histogram, weighted)", "Histogram (fast)", "Ordered splits (gradient-based)"]),
        table_row(["Tree growth", "Level-wise (depth-limited)", "Level-wise", "Leaf-wise (deeper, faster)", "Symmetric (oblivious trees)"]),
        table_row(["Row subsampling", "Yes (stochastic GBM)", "Yes", "GOSS (gradient-based)", "Yes (ordered)"]),
        table_row(["Column subsampling", "Yes (max_features)", "Yes (colsample)", "EFB bundling", "Yes"]),
        table_row(["Missing values", "Impute externally", "Built-in (sparsity-aware)", "Built-in", "Built-in"]),
        table_row(["Categorical native", "No", "No", "Yes", "Yes (ordered target enc)"]),
        table_row(["Speed (large data)", "Moderate", "Fast", "Very fast", "Moderate-fast"]),
        table_row(["Reference implementation", "sklearn GBM", "xgboost", "lightgbm", "catboost"]),
    ),
    callout("🎯", rt("When to use Friedman GBM (sklearn): ", bold=True), rt("Small datasets (<100k rows), research/baseline, need exact reproducibility, or studying the algorithm. Use XGBoost/LightGBM in production: faster, better regularisation, missing value handling, and GPU support. CatBoost shines with high-cardinality categoricals.")),
    divider(),

    # ── Section 9: Explainer ──────────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the stagewise build — each stage shows pseudo-residuals, tree fit, and loss curve. Use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Decision Trees (CART): splitting criteria, leaf structure")),
    bullet(rt("AdaBoost: intuition for boosting before the functional gradient framing")),
    bullet(rt("Gradient Descent: parameter-space analogue of what GBM does in function space")),
    bullet(rt("Loss Functions: squared-error, logloss, Huber — GBM behaviour changes with each")),
    heading3("What to Learn Next"),
    bullet(rt("XGBoost: adds 2nd-order Taylor expansion, regularised objective, histogram splits")),
    bullet(rt("LightGBM: leaf-wise growth, GOSS, EFB — industrial-scale boosting")),
    bullet(rt("CatBoost: ordered boosting, oblivious trees, native categorical handling")),
    bullet(rt("SHAP values: Shapley-based feature importance for any tree ensemble")),
    heading3("Key Papers"),
    bullet(rt("Friedman (2001). Greedy function approximation: A gradient boosting machine. "), rt("Annals of Statistics", italic=True), rt(", 29(5), 1189–1232. [The paper — read sections 4–5]")),
    bullet(rt("Friedman (2002). Stochastic gradient boosting. "), rt("Computational Statistics & Data Analysis", italic=True), rt(", 38(4). [Subsampling extension]")),
    bullet(rt("Chen & Guestrin (2016). XGBoost: A scalable tree boosting system. "), rt("KDD 2016", italic=True), rt(". [2nd-order extension]")),
    bullet(rt("Mason, Bartlett, Baxter, Frean (1999). Boosting algorithms as gradient descent. "), rt("NeurIPS 1999", italic=True), rt(". [Theoretical grounding]")),
    heading3("Best Resources"),
    bullet(rt("ESL Chapter 10 (Hastie, Tibshirani, Friedman): definitive textbook treatment of boosting")),
    bullet(rt("Friedman's original paper: dense but self-contained; focus on Algorithms 1 and 2")),
    bullet(rt("fast.ai Tabular Lesson: practical GBM workflow with feature importance and ensembling")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("AdaBoost · Random Forest · XGBoost · LightGBM · CatBoost · SHAP · Ensemble Methods · Loss Functions · Functional Analysis (RKHS)")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
