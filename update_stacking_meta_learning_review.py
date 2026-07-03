#!/usr/bin/env python3
"""Update Notion page for: Stacking (meta-learning): level-0 and level-1 models"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8196-903b-df345a3f1af8"
ICON = "🟡"  # Intermediate
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/stacking_meta_learning_review_explainer.html"},
}

blocks = [
    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Stacking (stacked generalisation) trains several different models — the "), rt("level-0 base learners", bold=True), rt(" — on the same data, then trains a second model — the "), rt("level-1 meta-learner", bold=True), rt(" — to optimally combine their predictions. The meta-learner learns how to correct each base learner's systematic errors.")),
    heading3("Real-World Analogy"),
    para(rt("Three doctors each examine a patient and give a probability estimate for a diagnosis. A senior consultant (the meta-learner) weighs those three opinions — knowing which doctor tends to be over-confident and which under-estimates — to produce the final verdict. The consultant never saw the original lab results; she only sees the doctors' probability scores.")),
    heading3("One-Sentence Summary"),
    para(rt("Stacking turns K diverse models into meta-features, then learns a combiner that is provably at least as good as the best single model.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("OOF (out-of-fold) prediction is the critical mechanism — each training sample's level-0 features come from a base model that never saw that sample, preventing leakage into the meta-learner.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Individual ML models have characteristic biases: linear models underfit complex decision boundaries; deep trees overfit; kNN is sensitive to irrelevant features. Simple averaging treats all models equally even when their error patterns are complementary.")),
    heading3("The Breakthrough"),
    para(rt("David Wolpert introduced stacked generalisation in his 1992 paper \"Stacked Generalization\" (Neural Networks, 1992). The key insight: instead of hand-weighting models, learn the combination function itself, using held-out predictions so the combination is not contaminated by training-set memorisation.")),
    heading3("Evolution Timeline"),
    para(rt("Wolpert (1992): stacking principle → Breiman (1996): bagging (parallel ensemble) → Freund & Schapire (1997): boosting (sequential ensemble) → Kaggle era (2012–): stacking becomes standard competition technique for top-5 finishes → sklearn 0.22+ (2020): StackingClassifier/StackingRegressor in standard library.")),
    heading3("Before vs After"),
    table(3,
        table_row(["Dimension", "Simple averaging (before)", "Stacking (after)"]),
        table_row(["Combination weights", "Equal — ignores model quality", "Learned from data"]),
        table_row(["Bias correction", "None — averages remain biased", "Meta-learner corrects per-region bias"]),
        table_row(["Data efficiency", "Full n for each model", "OOF uses all n with no leakage"]),
        table_row(["Heterogeneous models", "Awkward (different output scales)", "Meta-features normalise naturally"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧠 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Level-0 learners (base learners): ", bold=True), rt("K models "), eq(r"h_1,\ldots,h_K"), rt(" fit to the training data. Ideally diverse — different model families (tree, linear, kNN).")),
    bullet(rt("Level-1 learner (meta-learner): ", bold=True), rt("Model "), eq(r"g"), rt(" fit to "), eq(r"(Z, y)"), rt(", where "), eq(r"Z"), rt(" is the OOF meta-feature matrix.")),
    bullet(rt("OOF predictions: ", bold=True), rt("Prediction "), eq(r"\hat{z}_{i,j}"), rt(" for sample "), eq(r"i"), rt(" by learner "), eq(r"j"), rt(", where the model was trained without sample "), eq(r"i"), rt(".")),
    bullet(rt("Meta-feature matrix: ", bold=True), eq(r"Z \in \mathbb{R}^{n \times K}"), rt(", row "), eq(r"i"), rt(" = "), eq(r"[\hat{z}_{i,1},\ldots,\hat{z}_{i,K}]"), rt(".")),
    heading3("Core Property"),
    callout("🔑", rt("OOF predictions are ", bold=True), rt("unbiased estimates"), rt(" of each base learner's generalisation performance. The meta-learner therefore learns to combine models based on their generalisation ability, not their training-set performance.")),
    heading3("Prerequisites"),
    bullet(rt("Cross-validation (k-fold, stratified)")),
    bullet(rt("Bias–variance decomposition")),
    bullet(rt("Bagging and random forests (ensemble baseline)")),
    divider(),

    # ── Section 4: Architecture & Deep Dive ───────────────────────────────────
    heading2("🔬 Architecture & Internal Workings"),
    heading3("Two-Pass Training Protocol"),
    para(rt("Pass 1 — OOF generation: For each fold "), eq(r"f \in \{1,\ldots,k\}"), rt(" and each base learner "), eq(r"j"), rt(":")),
    equation_block(r"\hat{z}_{i,j} = h_j\!\left(x_i;\; D \setminus D_f\right), \quad x_i \in D_f"),
    para(rt("Each sample "), eq(r"i"), rt(" is predicted exactly once, by a version of "), eq(r"h_j"), rt(" trained without it. After all folds, collect into "), eq(r"Z")),
    para(rt("Pass 2 — Full refit: Retrain each base learner on all "), eq(r"n"), rt(" samples:")),
    equation_block(r"\tilde{h}_j = \text{fit}(h_j,\; D), \quad j = 1,\ldots,K"),
    para(rt("These fully-fitted models are stored for inference. They see more data than the OOF clones, so are slightly stronger — acceptable because they are only used in production, not to generate training features for the meta-learner.")),
    heading3("Meta-Learner Training"),
    equation_block(r"\hat{g} = \underset{g \in \mathcal{G}}{\operatorname{argmin}}\; \mathcal{L}\!\left(g(Z), y\right)"),
    para(rt("For regression, "), eq(r"\mathcal{G}"), rt(" = Ridge regression. For classification, Logistic Regression. Using a high-capacity "), eq(r"g"), rt(" (e.g. deep tree) on the low-dimensional "), eq(r"K"), rt("-column "), eq(r"Z"), rt(" invites overfitting.")),
    heading3("Inference"),
    equation_block(r"\hat{y}^* = \hat{g}\!\left(\tilde{h}_1(x^*), \tilde{h}_2(x^*), \ldots, \tilde{h}_K(x^*)\right)"),
    heading3("Numerical Trace (K=2, k=3, n=6)"),
    para(rt("Labels "), eq(r"y=[1,0,1,0,1,0]"), rt(". Base learners: Ridge Regression (L1), Decision Tree.")),
    para(rt("Fold 1 — train on {3,4,5,6}, predict {1,2}:")),
    bullet(rt("Ridge OOF: "), eq(r"\hat{z}_{1,1}=0.62,\; \hat{z}_{2,1}=0.41")),
    bullet(rt("Tree  OOF: "), eq(r"\hat{z}_{1,2}=0.80,\; \hat{z}_{2,2}=0.20")),
    para(rt("Fold 2 — train on {1,2,5,6}, predict {3,4}:")),
    bullet(rt("Ridge OOF: "), eq(r"\hat{z}_{3,1}=0.71,\; \hat{z}_{4,1}=0.35")),
    bullet(rt("Tree  OOF: "), eq(r"\hat{z}_{3,2}=0.90,\; \hat{z}_{4,2}=0.10")),
    para(rt("Fold 3 — train on {1,2,3,4}, predict {5,6}:")),
    bullet(rt("Ridge OOF: "), eq(r"\hat{z}_{5,1}=0.68,\; \hat{z}_{6,1}=0.38")),
    bullet(rt("Tree  OOF: "), eq(r"\hat{z}_{5,2}=0.85,\; \hat{z}_{6,2}=0.15")),
    para(rt("Meta-feature matrix "), eq(r"Z"), rt(":")),
    equation_block(r"Z = \begin{bmatrix}0.62 & 0.80\\ 0.41 & 0.20\\ 0.71 & 0.90\\ 0.35 & 0.10\\ 0.68 & 0.85\\ 0.38 & 0.15\end{bmatrix}"),
    para(rt("Logistic meta-learner fitted on "), eq(r"(Z, y)"), rt(" learns weights "), eq(r"w \approx [1.2,\; 2.1]"), rt(". Test sample: Ridge→0.65, Tree→0.88:")),
    equation_block(r"\hat{y}^* = \sigma(1.2 \times 0.65 + 2.1 \times 0.88) = \sigma(2.628) \approx 0.933"),
    divider(),

    # ── Section 5: Math ────────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Bias–Variance Decomposition"),
    para(rt("For any predictor "), eq(r"\hat{f}"), rt(":")),
    equation_block(r"\mathbb{E}[(y - \hat{f}(x))^2] = \text{Bias}^2(\hat{f}) + \text{Var}(\hat{f}) + \sigma^2_\varepsilon"),
    heading3("Variance of Combined Estimator"),
    para(rt("Suppose "), eq(r"K"), rt(" learners each have variance "), eq(r"\sigma^2"), rt(" and pairwise error correlation "), eq(r"\rho"), rt(". With equal weights "), eq(r"w_j = 1/K"), rt(":")),
    equation_block(r"\text{Var}\!\left(\frac{1}{K}\sum_{j=1}^K h_j\right) = \frac{\sigma^2}{K} + \frac{K-1}{K}\,\rho\,\sigma^2"),
    para(rt("As "), eq(r"\rho \to 0"), rt(" (diverse models), variance → "), eq(r"\sigma^2/K"), rt(" — full averaging benefit. As "), eq(r"\rho \to 1"), rt(" (identical models), variance → "), eq(r"\sigma^2"), rt(" — no benefit. This quantifies why diversity of base learners is essential.")),
    heading3("Optimal Meta-Learner (Ridge)"),
    equation_block(r"\hat{w} = (Z^\top Z + \lambda I)^{-1} Z^\top y"),
    para(rt("where "), eq(r"\lambda > 0"), rt(" is the regularisation strength. Setting "), eq(r"\lambda=0"), rt(" recovers OLS which can overfit when base learner predictions are correlated (near-collinear columns in "), eq(r"Z"), rt(").")),
    heading3("Wolpert's Guarantee (Informal)"),
    para(rt("With infinitely capable "), eq(r"g"), rt(" and unbiased OOF predictions, the stacked ensemble's expected loss is upper-bounded by the best base learner's expected loss. Formally: "), eq(r"\mathbb{E}[\mathcal{L}(\hat{g})] \leq \min_j \mathbb{E}[\mathcal{L}(h_j)]"), rt(" under mild regularity conditions.")),
    callout("⚠️", rt("Common misconception: ", bold=True), rt("More base learners always helps. In practice, adding highly correlated learners inflates "), eq(r"\rho"), rt(" without reducing variance. Use learners from different algorithm families.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("From Scratch (NumPy / sklearn)"),
    code_block("python", """import numpy as np
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

class Stacker:
    def __init__(self, base_learners, meta_learner, n_folds=5):
        self.base = base_learners   # list of (name, estimator) tuples
        self.meta = meta_learner    # level-1 model (keep it simple!)
        self.k = n_folds

    def fit(self, X, y):
        n, K = len(X), len(self.base)
        Z = np.zeros((n, K))        # meta-feature matrix (OOF)
        kf = KFold(n_splits=self.k, shuffle=True, random_state=42)

        # Pass 1: generate OOF predictions (no leakage)
        for j, (name, clf) in enumerate(self.base):
            for train_idx, val_idx in kf.split(X):
                clf.fit(X[train_idx], y[train_idx])
                Z[val_idx, j] = clf.predict_proba(X[val_idx])[:, 1]

        # Pass 2: retrain each base learner on full data
        self.fitted_base = []
        for _, clf in self.base:
            clf.fit(X, y)
            self.fitted_base.append(clf)

        # Train meta-learner on OOF meta-features — honest signal
        self.meta.fit(Z, y)
        return self

    def predict_proba(self, X):
        Z_test = np.column_stack(
            [clf.predict_proba(X)[:, 1] for clf in self.fitted_base]
        )
        return self.meta.predict_proba(Z_test)

# Usage
base = [
    ('ridge_clf', LogisticRegression(C=10)),
    ('tree',      DecisionTreeClassifier(max_depth=5, random_state=0)),
    ('knn',       KNeighborsClassifier(n_neighbors=7)),
]
stacker = Stacker(base, LogisticRegression(C=1.0), n_folds=5)
stacker.fit(X_train, y_train)
y_pred = stacker.predict_proba(X_test)[:, 1]
"""),
    heading3("Production Usage (scikit-learn)"),
    code_block("python", """from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC

estimators = [
    ('rf',  RandomForestClassifier(n_estimators=200, random_state=0)),
    ('gbm', GradientBoostingClassifier(n_estimators=100, random_state=0)),
    ('svc', SVC(probability=True, kernel='rbf')),
]

stacker = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression(C=0.5),
    cv=5,             # k-fold OOF
    stack_method='predict_proba',
    passthrough=False,  # set True to also feed original X to meta-learner
    n_jobs=-1,
)
stacker.fit(X_train, y_train)
# ⚠️ passthrough=True: meta-learner receives [Z | X], not just Z.
#    Useful when meta-learner benefits from raw features the base learners
#    summarise away (e.g., sparse ID features).
"""),
    divider(),

    # ── Section 7: Interview Q&A ───────────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy) — What is the difference between blending and stacking?", bold=True)], [
        para(rt("Blending uses a fixed holdout set (e.g. 20% of training data) to generate level-0 predictions. The base learners train on the remaining 80%. Stacking uses k-fold OOF so every training sample contributes a meta-feature without leakage. Stacking wastes less data but costs k × K fits vs one × K fits.")),
    ]),
    toggle([rt("Q2 (Medium) — Why should the meta-learner be simple?", bold=True)], [
        para(rt("The meta-feature matrix "), eq(r"Z"), rt(" has "), eq(r"K"), rt(" columns — typically ≤ 10. A high-capacity model (e.g., deep tree) overfits this low-dimensional space. A regularised linear model (Ridge, Lasso, Logistic Regression) provides well-calibrated combination weights. In Kaggle competitions, a simple weighted average sometimes outperforms a trained meta-learner.")),
    ]),
    toggle([rt("Q3 (Hard) — What leakage risk remains after OOF, and how do you guard against it?", bold=True)], [
        para(rt("Three residual risks: (1) "), rt("Test-set features fed back to model selection", bold=True), rt(" — never use test OOF, evaluate on true holdout only. (2) "), rt("Target encoding inside OOF folds", bold=True), rt(" — if base learners use target statistics, recompute them inside each fold. (3) "), rt("Time-series data", bold=True), rt(" — use purged k-fold (no overlap between train and val windows) to prevent temporal leakage. OOF alone does not guard against within-fold feature engineering that peeks at the target.")),
    ]),
    toggle([rt("Q4 (Hard) — Explain stacking from a Bayesian model averaging perspective.", bold=True)], [
        para(rt("Bayesian Model Averaging weights each model by its posterior probability given data: "), eq(r"\hat{y} = \sum_j P(M_j|D)\, h_j(x)"), rt(". Stacking approximates this but optimises predictive performance rather than posterior probability. Clarke (2003) and Clyde & Iversen (2013) show that stacking weights correspond to leave-one-out cross-validated Bayesian model probabilities under regularity conditions. The critical difference: BMA cannot outperform the true best model in expectation; stacking's learned combiner can, because it exploits model correlation structure.")),
    ]),
    toggle([rt("Explain to a PhD Researcher", bold=True)], [
        para(rt("Stacking is an instance of empirical risk minimisation in a two-level hierarchy. Level-0 defines a feature map "), eq(r"\phi: \mathcal{X} \to \mathbb{R}^K"), rt(" via OOF cross-validation; level-1 minimises "), eq(r"\mathbb{E}[\ell(g \circ \phi(x), y)]"), rt(" over a restricted function class "), eq(r"\mathcal{G}"), rt(". The OOF construction ensures "), eq(r"\phi"), rt(" is measurable with respect to the held-out fold's sigma-algebra, preventing information leakage. Wolpert (1992) proved the approach is consistent under mild conditions; Breiman (1996) connected it to the jackknife estimator.")),
    ]),
    toggle([rt("System Design Angle", bold=True)], [
        para(rt("In production ML systems, stacking adds latency: inference requires K sequential (or parallel) model calls before the meta-learner. Mitigation: parallelise the K base learner calls (O(latency of slowest)), cache predictions for repeated queries, or distil the stacked ensemble into a single model post-hoc. At training time, the K × k full fits can be parallelised across workers.")),
    ]),
    divider(),

    # ── Section 8: Comparisons ─────────────────────────────────────────────────
    heading2("⚖️ Comparisons & Trade-offs"),
    table(4,
        table_row(["Dimension", "Bagging", "Boosting", "Stacking"]),
        table_row(["Combination", "Average / majority vote", "Weighted additive (sequential)", "Learned meta-model"]),
        table_row(["Diversity source", "Bootstrapped subsets, same algorithm", "Reweighted samples, same algorithm", "Different algorithms encouraged"]),
        table_row(["Bias reduction", "Low", "High", "Medium"]),
        table_row(["Variance reduction", "High", "Low–Medium", "High"]),
        table_row(["Overfit risk", "Low", "Medium–High (early stop needed)", "Medium (OOF + simple meta)"]),
        table_row(["Training cost", r"O(K·n)", r"O(T·n) sequential", r"O(K·k·n) parallelisable"]),
        table_row(["Inference cost", "K calls, parallel", "T calls, parallel", "K calls + 1 meta call"]),
        table_row(["Best use case", "High-variance models (trees)", "Weak learners on structured data", "Heterogeneous model ensembles"]),
    ),
    callout("🎯", rt("Decision: ", bold=True), rt("Use stacking when you have ≥3 diverse well-tuned base learners from different families and sufficient data ("), eq(r"n \gtrsim 1000"), rt("). Prefer boosting (XGBoost, LightGBM) as a standalone when a single strong model is competitive — stacking's overhead is not justified.")),
    divider(),

    # ── Section 9: Visual Explainer ───────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/stacking_meta_learning_review_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Cross-validation (k-fold, stratified, purged)")),
    bullet(rt("Bias–variance decomposition")),
    bullet(rt("Bagging and Random Forests")),
    bullet(rt("Regularised linear models (Ridge, Lasso, Logistic Regression)")),
    heading3("What to Learn Next"),
    bullet(rt("Blending: holdout-based stacking (simpler, faster)")),
    bullet(rt("Multi-level stacking (3+ levels)")),
    bullet(rt("Practical considerations: diversity of base learners, overfitting in stacking")),
    bullet(rt("MAML (meta-learning via gradient-based optimisation)")),
    heading3("Key Papers"),
    bullet(rt("Wolpert, D. (1992). Stacked Generalization. Neural Networks, 5(2), 241–259. — original formulation.")),
    bullet(rt("Breiman, L. (1996). Stacked Regressions. Machine Learning, 24(1), 49–64. — regression focus, CV analysis.")),
    bullet(rt("Clarke, B. (2003). Comparing Bayes Model Averaging and Stacking. Journal of Machine Learning Research. — theoretical connection to BMA.")),
    bullet(rt("van Rijn et al. (2018). The Online Performance Estimation Framework: Heterogeneous Ensemble Learning for Data Streams. — streaming stacking.")),
    heading3("Best Resources"),
    bullet(rt("sklearn docs: StackingClassifier / StackingRegressor (with cv parameter detail)")),
    bullet(rt("mlwave.com — Kaggle Ensembling Guide (Ivan Kadochnikov): practical stacking recipes")),
    bullet(rt("ESL Chapter 8.8 — Model Averaging and Stacking (Hastie, Tibshirani, Friedman)")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Bagging · Boosting (XGBoost) · MAML · Bayesian Model Averaging · AutoML ensembling · Feature engineering for meta-learners")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
