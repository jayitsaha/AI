#!/usr/bin/env python3
"""Update Notion page for: Boosting concept: sequential, error-correcting"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8104-b84f-f5e3f82dd48c"
ICON = "🟡"  # Intermediate
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/boosting_concept_explainer.html"},
}

blocks = [
    # ── Section 1: The 30-Second Version ─────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is This?"),
    para(rt("Boosting trains a sequence of simple predictors (weak learners) where each new one focuses on the mistakes of all the previous ones combined. The final prediction is a weighted sum of every learner's output. Unlike bagging, which trains many models in parallel on random subsets of data, boosting is "), rt("sequential", bold=True), rt(" and "), rt("error-correcting", bold=True), rt(".")),
    heading3("Real-World Analogy"),
    para(rt("Think of a tutoring chain. A student sits an exam; the tutor circles the wrong answers in red (higher weight). The next tutor only studies those circled questions. The third tutor picks up whatever the second still got wrong. After five tutors the combined notes cover every question type — even the hardest ones no single tutor could handle alone.")),
    heading3("One-Sentence Summary"),
    para(rt("Boosting = add weak learners one at a time, each fitting the ensemble's current residual error, producing a strong learner primarily via "), rt("bias reduction", bold=True), rt(" (contrast: bagging reduces variance).")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Bagging reduces variance by averaging parallel models. Boosting reduces bias by chaining sequential models, each correcting the previous ensemble's systematic errors.")),
    divider(),

    # ── Section 2: Historical Context ────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("In the late 1980s, Kearns & Valiant posed a theoretical question: can a collection of weak learners (barely better than random) be combined into a strong learner (arbitrarily accurate)? PAC learning theory said yes in principle, but no practical algorithm existed.")),
    heading3("What Came Before"),
    para(rt("Decision trees and nearest-neighbour methods existed, but each individual model suffered from high bias or high variance. Bagging (Breiman, 1994) reduced variance by averaging, but did not attack systematic underfitting.")),
    heading3("The Breakthrough"),
    para(rt("Schapire (1990) proved in theory that boosting was possible. Freund & Schapire (1997) delivered the first practical algorithm: "), rt("AdaBoost", bold=True), rt(". Friedman (2001) recast boosting as gradient descent in function space — yielding "), rt("Gradient Boosting Machines", bold=True), rt(", which today power XGBoost, LightGBM, and CatBoost.")),
    heading3("Key Papers"),
    bullet(rt("\"A Decision-Theoretic Generalization of On-Line Learning...\" — Freund & Schapire, JCSS 1997. Introduced AdaBoost; showed exponential loss minimisation.")),
    bullet(rt("\"Greedy Function Approximation: A Gradient Boosting Machine\" — Friedman, Annals of Statistics 2001. Unified boosting as functional gradient descent.")),
    bullet(rt("\"XGBoost: A Scalable Tree Boosting System\" — Chen & Guestrin, KDD 2016. Engineering system that dominates tabular ML competitions.")),
    heading3("Evolution Timeline"),
    para(rt("Single decision trees (1984) → Bagging (1994) → AdaBoost (1997) → GBM / functional gradient (2001) → Stochastic GBM (2002) → XGBoost (2016) → LightGBM (2017) → CatBoost (2017)")),
    heading3("Before vs After"),
    table(3,
        table_row(["Dimension", "Before Boosting", "After Boosting"]),
        table_row(["Systematic bias", "Each weak model underfits", "Sequential correction drives bias to zero"]),
        table_row(["Training order", "Parallel / independent", "Sequential / dependent"]),
        table_row(["Error signal", "Full dataset equally", "Reweighted or residual — hard examples dominate"]),
        table_row(["Final vote", "Majority / average", "Weighted sum (accurate learners vote louder)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Weak learner: ", bold=True), rt("A model only slightly better than random chance (e.g. a decision stump: one-level tree).")),
    bullet(rt("Strong learner: ", bold=True), rt("A model that can achieve arbitrarily low error on a learning task.")),
    bullet(rt("Weighted error: ", bold=True), rt("The sum of sample weights for misclassified points — what each round minimises.")),
    bullet(rt("Residual: ", bold=True), rt("In gradient boosting, the negative gradient of the loss evaluated at current predictions; equals y − F(x) for squared error.")),
    bullet(rt("Shrinkage (learning rate η): ", bold=True), rt("Scales each weak learner's contribution to prevent over-correcting and improve generalisation.")),
    heading3("Prerequisites"),
    callout("📚", rt("To understand boosting fully, you should know: Decision Trees, Bias-Variance Tradeoff, Loss Functions (MSE, log-loss), Gradient Descent, and basic probability (weighted sampling).")),
    heading3("Core Invariant"),
    callout("🔑", rt("Key property: ", bold=True), rt("Every boosting algorithm maintains the invariant that the new weak learner is trained on a signal (reweighted samples or residuals) derived from the CURRENT ensemble, guaranteeing that each addition reduces the training error.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ───────────────────────────
    heading2("⚙️ Architecture & Internal Workings (PhD-Level)"),
    heading3("General Boosting Skeleton"),
    bullet(rt("1. Initialise: "), eq(r"F_0(x) = \underset{c}{\operatorname{argmin}} \sum_i L(y_i, c)")),
    bullet(rt("2. For t = 1, …, T:")),
    bullet(rt("   a. Compute pseudo-residuals: "), eq(r"r_i^{(t)} = -\left[\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\right]_{F=F_{t-1}}")),
    bullet(rt("   b. Fit weak learner "), eq(r"h_t"), rt(" to "), eq(r"\{(x_i, r_i^{(t)})\}")),
    bullet(rt("   c. Find step size: "), eq(r"\rho_t = \underset{\rho}{\operatorname{argmin}} \sum_i L(y_i, F_{t-1}(x_i) + \rho h_t(x_i))")),
    bullet(rt("   d. Update: "), eq(r"F_t(x) = F_{t-1}(x) + \eta \cdot \rho_t \cdot h_t(x)")),
    heading3("AdaBoost Internals — Numerical Trace"),
    para(rt("Binary classification with labels "), eq(r"y_i \in \{-1, +1\}"), rt(". Five samples. Initial weights "), eq(r"w_i^{(1)} = 0.2"), rt(" for all "), eq(r"i"), rt(".")),
    para(rt("Round 1: stump "), eq(r"h_1"), rt(" misclassifies 2 samples. Weighted error:")),
    equation_block(r"\varepsilon_1 = \sum_{i : h_1(x_i) \neq y_i} w_i^{(1)} = 0.2 + 0.2 = 0.40"),
    para(rt("Learner weight:")),
    equation_block(r"\alpha_1 = \frac{1}{2}\ln\!\left(\frac{1-\varepsilon_1}{\varepsilon_1}\right) = \frac{1}{2}\ln\!\left(\frac{0.60}{0.40}\right) = \frac{1}{2}\ln(1.5) \approx 0.2027"),
    para(rt("Weight update (unnormalised):")),
    equation_block(r"\tilde{w}_i^{(2)} = w_i^{(1)} \cdot \exp\!\bigl(-\alpha_1 \, y_i \, h_1(x_i)\bigr)"),
    para(rt("Correct sample: "), eq(r"\tilde{w} = 0.2 \cdot e^{-0.2027} \approx 0.163"), rt(". Misclassified: "), eq(r"\tilde{w} = 0.2 \cdot e^{+0.2027} \approx 0.245"), rt(". After normalisation the two wrong samples carry more weight — the next stump will specialise on them.")),
    heading3("Gradient Boosting Internals — Numerical Trace (MSE, η=0.5)"),
    para(rt("Training set: "), eq(r"y = [3, 7, 5, 8, 2, 6]"), rt(". Initialise "), eq(r"F_0(x) = \bar{y} = 31/6 \approx 5.167"), rt(".")),
    para(rt("Residuals "), eq(r"r^{(1)} = y - F_0 = [-2.167, +1.833, -0.167, +2.833, -3.167, +0.833]"), rt(".")),
    para(rt("Tree "), eq(r"h_1"), rt(" is fit to "), eq(r"r^{(1)}"), rt(". Suppose leaf predictions "), eq(r"h_1 = [-1.5, +1.5, -0.1, +2.0, -2.0, +0.6]"), rt(".")),
    para(rt("Update: "), eq(r"F_1 = F_0 + 0.5 \cdot h_1 = [4.417, 5.917, 5.117, 6.167, 4.167, 5.467]"), rt(".")),
    para(rt("New residuals "), eq(r"r^{(2)} = [-1.417, +1.083, -0.117, +1.833, -2.167, +0.533]"), rt(". Each round shrinks the error. This is gradient descent in function space: "), eq(r"F_t \leftarrow F_{t-1} - \eta \nabla_F \mathcal{L}"), rt(".")),
    heading3("Design Decisions"),
    callout("🔧", rt("Why shallow trees? ", bold=True), rt("Deep trees would fit the residuals exactly (zero training error, high variance). Shallow stumps have high bias individually, but the sequential composition drives bias down while keeping variance low — each stump has too few parameters to memorise noise.")),
    callout("🔧", rt("Why shrinkage? ", bold=True), rt("Without η < 1, each learner over-corrects. Shrinkage acts like regularisation: we take a small step in the right direction, allowing more rounds (learners) before overfitting, which usually improves test performance.")),
    heading3("Failure Modes"),
    bullet(rt("Noisy labels: boosting assigns high weight to noisy mislabelled examples, fitting the noise.")),
    bullet(rt("Too many rounds without regularisation: variance grows, overfitting occurs.")),
    bullet(rt("Very high learning rate: each corrective step overshoots, causing oscillation in the loss.")),
    divider(),

    # ── Section 5: The Math ───────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("AdaBoost Loss Minimisation"),
    para(rt("AdaBoost implicitly minimises the exponential loss:")),
    equation_block(r"\mathcal{L}(y, F) = \sum_{i=1}^n \exp(-y_i F(x_i))"),
    para(rt("At each round, the additive update "), eq(r"F_t = F_{t-1} + \alpha_t h_t"), rt(" is chosen to minimise this loss. The optimal "), eq(r"\alpha_t"), rt(" is:")),
    equation_block(r"\alpha_t = \frac{1}{2}\ln\!\left(\frac{1-\varepsilon_t}{\varepsilon_t}\right)"),
    para(rt("where "), eq(r"\varepsilon_t = \sum_{i=1}^n w_i^{(t)} \mathbb{1}[h_t(x_i) \neq y_i]"), rt(". The weight update follows from the gradient of the exponential loss.")),
    heading3("Gradient Boosting — Functional Gradient Descent"),
    para(rt("Define the loss over the entire training set as a functional "), eq(r"\mathcal{L}[F] = \sum_i L(y_i, F(x_i))"), rt(". The negative functional gradient is:")),
    equation_block(r"r_i^{(t)} = -\frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}\bigg|_{F=F_{t-1}}"),
    para(rt("For squared error "), eq(r"L(y,\hat{y}) = \tfrac{1}{2}(y-\hat{y})^2"), rt(", "), eq(r"r_i^{(t)} = y_i - F_{t-1}(x_i)"), rt(" (ordinary residuals). For log-loss, the negative gradient is "), eq(r"r_i^{(t)} = y_i - p_i"), rt(" where "), eq(r"p_i = \sigma(F_{t-1}(x_i))"), rt(".")),
    heading3("Convergence & Bias-Variance"),
    para(rt("Let "), eq(r"T"), rt(" be the number of rounds. With weak learners satisfying "), eq(r"\varepsilon_t \leq \frac{1}{2} - \gamma"), rt(" for some "), eq(r"\gamma > 0"), rt(", AdaBoost's training error decays exponentially:")),
    equation_block(r"\frac{1}{n}\sum_{i=1}^n \mathbb{1}[H_T(x_i) \neq y_i] \leq \exp\!\left(-2T\gamma^2\right)"),
    para(rt("This proves that boosting drives training error to zero. However, bias-variance decomposition shows:")),
    equation_block(r"\mathbb{E}\left[(y - F_T(x))^2\right] = \text{Bias}^2[F_T] + \text{Var}[F_T] + \sigma^2_\varepsilon"),
    para(rt("Each round primarily reduces "), rt("Bias²", bold=True), rt(" (the ensemble gets closer to the true function on training data). But Var["), eq(r"F_T"), rt("] grows slowly with T (more complex model), so overfitting eventually occurs without regularisation.")),
    callout("⚠️", rt("Warning: ", bold=True), rt("AdaBoost on noisy data does NOT converge gracefully — the exponential loss assigns enormous weight to consistently mislabelled points, leading the algorithm to focus on irreducible noise. Gradient boosting with robust losses (Huber, quantile) is more noise-resistant.")),
    divider(),

    # ── Section 6: Code Implementation ───────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("AdaBoost From Scratch (NumPy)"),
    code_block("python", """import numpy as np

class AdaBoostScratch:
    \"\"\"Binary AdaBoost with decision stumps. Labels must be {-1, +1}.\"\"\"
    def __init__(self, n_estimators=50):
        self.n_estimators = n_estimators
        self.alphas = []      # learner weights
        self.stumps = []      # (feature, threshold, polarity) tuples

    def _stump_predict(self, X, feat, thresh, polarity):
        preds = np.ones(len(X))
        if polarity == 1:
            preds[X[:, feat] < thresh] = -1
        else:
            preds[X[:, feat] >= thresh] = -1
        return preds

    def fit(self, X, y):
        n = len(y)
        w = np.full(n, 1/n)           # uniform initial weights

        for t in range(self.n_estimators):
            # Find best stump (minimise weighted error)
            best_err = float('inf')
            best_stump = None
            for feat in range(X.shape[1]):
                thresholds = np.unique(X[:, feat])
                for thresh in thresholds:
                    for polarity in [1, -1]:
                        preds = self._stump_predict(X, feat, thresh, polarity)
                        err = w[preds != y].sum()   # weighted error
                        if err < best_err:
                            best_err = err
                            best_stump = (feat, thresh, polarity)

            eps = max(best_err, 1e-10)          # avoid log(0)
            alpha = 0.5 * np.log((1 - eps) / eps)   # learner weight
            preds = self._stump_predict(X, *best_stump)

            # Update weights: increase for misclassified, decrease for correct
            w *= np.exp(-alpha * y * preds)
            w /= w.sum()                        # normalise to sum=1

            self.stumps.append(best_stump)
            self.alphas.append(alpha)

    def predict(self, X):
        # Weighted vote of all stumps
        F = sum(a * self._stump_predict(X, *s)
                for a, s in zip(self.alphas, self.stumps))
        return np.sign(F)
"""),
    heading3("Gradient Boosting From Scratch (NumPy, MSE)"),
    code_block("python", """import numpy as np
from sklearn.tree import DecisionTreeRegressor   # weak learner

class GradientBoostScratch:
    \"\"\"Gradient Boosting for regression with MSE loss.\"\"\"
    def __init__(self, n_estimators=100, learning_rate=0.1, max_depth=3):
        self.n_estimators = n_estimators
        self.lr = learning_rate
        self.max_depth = max_depth
        self.trees = []
        self.F0 = None

    def fit(self, X, y):
        # Initialise with mean (optimal constant for MSE)
        self.F0 = y.mean()
        F = np.full(len(y), self.F0)

        for t in range(self.n_estimators):
            # Negative gradient of MSE = residuals
            residuals = y - F

            # Fit weak learner to residuals
            tree = DecisionTreeRegressor(max_depth=self.max_depth)
            tree.fit(X, residuals)
            h = tree.predict(X)

            # Update ensemble (shrinkage applied)
            F += self.lr * h
            self.trees.append(tree)

    def predict(self, X):
        F = np.full(X.shape[0], self.F0)
        for tree in self.trees:
            F += self.lr * tree.predict(X)
        return F
"""),
    heading3("Production Usage (sklearn / XGBoost)"),
    code_block("python", """from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
import xgboost as xgb

# --- AdaBoost (sklearn) ---
ada = AdaBoostClassifier(
    n_estimators=200,
    learning_rate=1.0,     # ⚠️ AdaBoost uses α_t for weighting; this is a global scale
    algorithm='SAMME.R',   # real-valued probabilities (better than SAMME for most cases)
)
ada.fit(X_train, y_train)

# --- Gradient Boosting (sklearn) ---
gbm = GradientBoostingClassifier(
    n_estimators=500,
    learning_rate=0.05,    # shrinkage — lower = more robust, more trees needed
    max_depth=4,           # shallow trees = low variance weak learners
    subsample=0.8,         # stochastic GBM: reduces variance further
    min_samples_leaf=20,   # regularisation: avoid tiny leaves
)
gbm.fit(X_train, y_train)

# --- XGBoost (production standard) ---
model = xgb.XGBClassifier(
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,  # feature sampling per tree (like Random Forest feature bagging)
    reg_lambda=1.0,        # L2 regularisation on leaf weights
    reg_alpha=0.0,         # L1 regularisation
    early_stopping_rounds=50,   # stop when validation loss stops improving
    eval_metric='logloss',
)
model.fit(X_train, y_train,
          eval_set=[(X_val, y_val)],
          verbose=100)
# ⚠️ Gotcha: always use early stopping; n_estimators=1000 without it WILL overfit.
# ⚠️ Gotcha: feature importances in XGBoost can be misleading for high-cardinality features.
"""),
    divider(),

    # ── Section 7: Interview Deep Dive ────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is boosting and how does it differ from bagging?", bold=True)], [
        para(rt("Boosting trains weak learners sequentially; each one corrects the errors of the ensemble built so far. The key mechanism: misclassified examples (AdaBoost) or high-residual points (GBM) receive more emphasis in the next round. Bagging trains learners in parallel on random bootstrap samples and averages them. Bagging reduces variance; boosting reduces bias.")),
    ]),
    toggle([rt("Q2 (Easy): What is a weak learner in the context of boosting?", bold=True)], [
        para(rt("A weak learner is a model only marginally better than random guessing (for binary classification: error < 0.5). Decision stumps (one-split trees) are the canonical example. The power of boosting is the theoretical proof that any collection of weak learners can be combined into a strong learner.")),
    ]),
    toggle([rt("Q3 (Medium): Derive the AdaBoost learner weight α_t. Why does the formula make sense intuitively?", bold=True)], [
        para(rt("We minimise the exponential loss with respect to α:")),
        equation_block(r"\frac{d}{d\alpha}\sum_i w_i e^{-\alpha y_i h_t(x_i)} = 0"),
        para(rt("Splitting correct ("), eq(r"y_i h_t = +1"), rt(") and incorrect ("), eq(r"y_i h_t = -1"), rt(") terms:")),
        equation_block(r"-e^{-\alpha}(1-\varepsilon_t) + e^{\alpha}\varepsilon_t = 0 \implies \alpha = \frac{1}{2}\ln\frac{1-\varepsilon_t}{\varepsilon_t}"),
        para(rt("Intuition: when ε→0 (perfect learner), α→∞ (dominates). When ε→0.5 (random), α→0 (ignored). Negative α occurs if ε>0.5 (reverse the learner's predictions).")),
    ]),
    toggle([rt("Q4 (Medium): Explain gradient boosting as gradient descent in function space.", bold=True)], [
        para(rt("In parameter space, gradient descent updates θ ← θ − η∇_θ L. In function space, the 'parameters' are the function values F(x_i) at each training point. The gradient of the loss w.r.t. F(x_i) is:")),
        equation_block(r"g_i = \frac{\partial L(y_i, F(x_i))}{\partial F(x_i)}"),
        para(rt("We want to move F in the direction of steepest descent: add "), eq(r"-g_i"), rt(" to each "), eq(r"F(x_i)"), rt(". But we need a function (not just values at training points) so we fit a tree to the negative gradients "), eq(r"r_i = -g_i"), rt(" and add it. This is exactly 'gradient descent' but in the space of functions.")),
    ]),
    toggle([rt("Q5 (Hard): Why can boosting overfit? What controls this? What is the interplay between T, η, and tree depth?", bold=True)], [
        para(rt("Boosting reduces bias with each round but the model complexity (VC dimension) grows with T, so variance increases. Three regularisation levers:")),
        bullet(rt("Learning rate η (shrinkage): smaller η → smaller step per tree → need more trees → better generalisation. The optimal is usually small η with large T found by early stopping.")),
        bullet(rt("Tree depth: shallow trees → lower variance weak learners. Depth-1 stumps → very low variance but need many rounds.")),
        bullet(rt("Subsampling (stochastic GBM): training each tree on a random subset of data (like bagging within boosting) reduces variance and speeds training.")),
        para(rt("The key identity: smaller η requires larger T to achieve the same training error, but the test error at the optimum T is usually lower.")),
    ]),
    toggle([rt("Q6 (Hard — PhD Researcher level): What loss function does AdaBoost implicitly minimise, and what does this imply about its behaviour on noisy data?", bold=True)], [
        para(rt("AdaBoost minimises the exponential loss "), eq(r"\mathcal{L} = \sum_i e^{-y_i F(x_i)}"), rt(". The exponential loss grows very rapidly for large-margin violations (", ), eq(r"y_i F(x_i) \ll 0"), rt("). This means:")),
        bullet(rt("Mislabelled samples (noise) that are consistently assigned large negative margins get exponentially large weights → the algorithm fixates on unfittable noise.")),
        bullet(rt("Even after training error reaches zero, AdaBoost continues to increase margins, which is beneficial for well-separated classes.")),
        bullet(rt("On noisy data, use gradient boosting with robust losses (Huber, quantile) which bound the influence of large residuals.")),
    ]),
    toggle([rt("Q7 (Hard — System Design): How does boosting fit into an ML system for fraud detection at scale?", bold=True)], [
        para(rt("XGBoost/LightGBM are the standard for fraud detection. Key considerations:")),
        bullet(rt("Training: boosting is sequential per tree, but trees can be trained with histogram-based approximate splits in parallel across features → LightGBM trains in minutes on millions of rows.")),
        bullet(rt("Prediction latency: each tree traversal is O(depth) → with 1000 trees of depth 6, prediction is ~6000 comparisons, easily sub-millisecond.")),
        bullet(rt("Class imbalance: use scale_pos_weight (XGBoost) or is_unbalance (LightGBM) to up-weight the minority fraud class.")),
        bullet(rt("Feature importance: gain-based importances identify the most predictive signals; SHAP values give per-prediction explanations.")),
        bullet(rt("Drift: retrain periodically with a sliding time window; gradient boosting generalises well in distribution but is sensitive to feature drift.")),
    ]),
    callout("🚩", rt("Red Flags: ", bold=True), rt("'Boosting is just averaging many trees' (wrong — it's a weighted sum with sequential dependency). 'Boosting always outperforms bagging' (wrong — on noisy data, Random Forest often wins). 'Boosting is parallelisable' (wrong by design — it is fundamentally sequential).")),
    divider(),

    # ── Section 8: Comparisons & Trade-offs ──────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    heading3("Boosting vs All Alternatives"),
    table(5,
        table_row(["Dimension", "AdaBoost", "Gradient Boosting", "Random Forest", "Stacking"]),
        table_row(["Sequential?", "Yes", "Yes", "No (parallel)", "No"]),
        table_row(["Error targeted", "Variance in weights", "Loss gradient / residuals", "Variance by sampling", "Generalisation error"]),
        table_row(["Bias reduced?", "Yes (primary)", "Yes (primary)", "Minor", "Depends on meta-model"]),
        table_row(["Variance reduced?", "Minor", "Minor (+ subsampling)", "Yes (primary)", "Depends"]),
        table_row(["Noise robustness", "Low (exp. loss)", "Moderate (tune loss)", "High", "Depends"]),
        table_row(["Training speed", "Fast (stumps)", "Moderate–fast", "Fast (parallel)", "Slow"]),
        table_row(["Hyperparameter sensitivity", "Medium", "High", "Low", "High"]),
        table_row(["Tabular SOTA", "Rarely", "Yes (XGBoost/LGB)", "Often competitive", "Sometimes"]),
    ),
    callout("🎯", rt("Decision rule: ", bold=True), rt("Structured/tabular data → XGBoost or LightGBM (gradient boosting). Noisy labels or small data → Random Forest. Need maximum predictive accuracy in a competition → try stacking with GBM as a base. Pure interpretability required → single decision tree.")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ───────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/boosting_concept_explainer.html"),
    para(rt("Step through 8 stages of a 4-round gradient boosting run — watch residuals shrink sequentially as each weak learner is added.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Decision Trees — the canonical weak learner")),
    bullet(rt("Bias-Variance Tradeoff — the theoretical framing for why boosting works")),
    bullet(rt("Loss Functions (MSE, log-loss, exponential) — the objectives boosting minimises")),
    bullet(rt("Gradient Descent — the optimisation perspective on GBM")),
    heading3("What to Learn Next"),
    bullet(rt("Gradient Boosting Machines (GBM) — full functional gradient descent derivation")),
    bullet(rt("XGBoost — regularised boosting with second-order Newton steps")),
    bullet(rt("LightGBM — histogram-based splits, leaf-wise growth")),
    bullet(rt("CatBoost — ordered boosting, native categorical handling")),
    bullet(rt("Bagging vs Boosting vs Stacking — the ensemble taxonomy")),
    heading3("Key Papers"),
    bullet(rt("Freund & Schapire (1997), \"A Decision-Theoretic Generalization of On-Line Learning...\" JCSS — introduced AdaBoost.")),
    bullet(rt("Friedman (2001), \"Greedy Function Approximation: A Gradient Boosting Machine\", Annals of Statistics — unified boosting as functional gradient descent.")),
    bullet(rt("Friedman (2002), \"Stochastic Gradient Boosting\" — added subsampling for variance reduction.")),
    bullet(rt("Chen & Guestrin (2016), \"XGBoost\", KDD — regularised boosting system that dominates Kaggle tabular competitions.")),
    heading3("Best Resources"),
    bullet(rt("ESL Chapter 10 — Boosting and Additive Trees (Hastie, Tibshirani, Friedman) — the canonical graduate-level treatment")),
    bullet(rt("Friedman's original GBM paper — essential for understanding functional gradient descent")),
    bullet(rt("XGBoost documentation on tree methods — practical hyperparameter guide")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("AdaBoost · GBM / XGBoost / LightGBM / CatBoost · Random Forests · Stacking · Bias-Variance Tradeoff · Decision Trees · Loss Functions · Regularisation (Shrinkage, Early Stopping)")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
