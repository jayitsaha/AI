#!/usr/bin/env python3
"""Update Notion page for: Time series cross-validation: expanding window, sliding window"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8152-abd1-fc6d10de34c5"
ICON = "🟡"
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/time_series_cv_explainer.html"},
}

blocks = [

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1 — The 30-Second Version
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎯 The 30-Second Version"),

    heading3("What is this?"),
    para(rt("Time series cross-validation is a way to honestly measure how well a forecasting model will perform on unseen future data — without accidentally 'cheating' by training on data that hasn't happened yet. Instead of randomly splitting data into train/test (which would mix future and past), we always train on earlier observations and validate on later ones.")),

    heading3("Real-World Analogy"),
    para(rt("Imagine you're a stock trader back-testing a strategy. You train your rules on January–March data, then test them on April. Then train on January–April, test on May. You never look ahead — you only use what you knew at the time. That forward-chaining discipline is exactly time series CV.")),

    callout("💡",
        rt("If you remember one thing: ", bold=True),
        rt("Never shuffle time series data. Always train on the past, validate on the future. The two flavours are expanding window (train set grows each fold) and sliding window (train set stays the same size, slides forward).")
    ),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2 — Historical Context
    # ══════════════════════════════════════════════════════════════════════════
    heading2("📜 Why This Exists — Historical Context"),

    heading3("The Problem"),
    para(rt("Standard k-fold cross-validation randomly shuffles data before splitting into folds. For i.i.d. data this is optimal — but time series data is autocorrelated: observation t+1 depends on t. Randomly splitting means fold 3 might train on t=50,51,52... and validate on t=1,2,3... — the model trains on the future and validates on the past, a form of data leakage that produces wildly optimistic error estimates.")),

    heading3("What Came Before"),
    bullet(rt("Hold-out: single train/test split at a fixed cutoff. Simple but wastes data and gives a single noisy estimate.")),
    bullet(rt("k-fold CV: optimal for i.i.d. data but invalid for time series due to temporal leakage.")),
    bullet(rt("Walk-forward simulation: finance practitioners' name for the same concept, dating to the 1970s.")),

    heading3("The Breakthrough"),
    para(
        rt("The forward-chaining / time-series split became formalized in the ML literature in the early 2000s as time series forecasting competitions (M-competition, NN3, GEFCom) standardized evaluation protocols. Scikit-learn added "),
        rt("TimeSeriesSplit", code=True),
        rt(" in v0.18 (2016), making it mainstream.")
    ),

    heading3("Key Papers & Resources"),
    bullet(rt("Bergmeir & Benitez (2012) — 'On the use of cross-validation for time series predictor evaluation' — showed standard CV is biased for AR processes.")),
    bullet(rt("Cerqueira et al. (2020) — 'Evaluating time series forecasting models' — compared 12 CV strategies empirically; expanding window generally outperforms single hold-out.")),
    bullet(rt("Hyndman & Athanasopoulos (2018) — Forecasting: Principles and Practice — the canonical textbook treatment.")),

    heading3("Evolution Timeline"),
    numbered(rt("1970s — Walk-forward simulation in quantitative finance")),
    numbered(rt("1990s — M-competition establishes rolling-origin evaluation in forecasting")),
    numbered(rt("2000s — ML community formalizes time series split")),
    numbered(rt("2016 — scikit-learn TimeSeriesSplit added")),
    numbered(rt("2020s — Gap / purged CV variants developed for financial ML (de Prado 2018)")),

    table(3,
        table_row(["Dimension", "Standard k-fold", "Time Series CV"]),
        table_row(["Data order", "Ignored (shuffled)", "Preserved (critical)"]),
        table_row(["Leakage risk", "High for autocorrelated data", "None (future never seen)"]),
        table_row(["Fold count", "k (flexible)", "T/h − 1 (determined by horizon)"]),
        table_row(["Estimate bias", "Optimistic (for TS)", "Realistic"]),
        table_row(["Variance", "Low (many folds)", "Higher (fewer, dependent folds)"]),
    ),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3 — Core Concepts & Theory
    # ══════════════════════════════════════════════════════════════════════════
    heading2("⚙️ Core Concepts & Theory"),

    heading3("Key Definitions"),
    bullet(rt("T — total length of the time series")),
    bullet(rt("h — forecast horizon (how many steps ahead we predict)")),
    bullet(rt("s — step size between folds (stride)")),
    bullet(rt("W — window size for sliding window CV")),
    bullet(rt("K — total number of folds")),
    bullet(rt("Origin — the time point where training ends and validation begins")),

    heading3("Forward-Chaining Invariant"),
    callout("🔑",
        rt("Key Invariant: ", bold=True),
        rt("For every fold, ALL training observations occur strictly before ALL validation observations. Formally: "),
        eq(r"\max(\text{train}_k) < \min(\text{val}_k)"),
        rt(" for all k.")
    ),

    heading3("Expanding Window"),
    para(
        rt("In fold "),
        eq(r"k"),
        rt(" (with step size "),
        eq(r"s"),
        rt(" and horizon "),
        eq(r"h"),
        rt("):")
    ),
    equation_block(r"\text{Train}_k = \{t_1, t_2, \ldots, t_{k \cdot s}\}, \quad \text{Val}_k = \{t_{k \cdot s + 1}, \ldots, t_{k \cdot s + h}\}"),
    para(
        rt("Training set grows monotonically: "),
        eq(r"|\text{Train}_k| = k \cdot s"),
        rt(". The total number of folds is "),
        eq(r"K = \lfloor (T - h) / s \rfloor - \lfloor s_{\min} / s \rfloor"),
        rt(" where "),
        eq(r"s_{\min}"),
        rt(" is the minimum required training size.")
    ),

    heading3("Sliding Window"),
    para(
        rt("With fixed window "),
        eq(r"W"),
        rt(", step "),
        eq(r"s"),
        rt(", horizon "),
        eq(r"h"),
        rt(":")
    ),
    equation_block(r"\text{Train}_k = \{t_{(k-1)s+1}, \ldots, t_{(k-1)s+W}\}, \quad \text{Val}_k = \{t_{(k-1)s+W+1}, \ldots, t_{(k-1)s+W+h}\}"),
    para(
        rt("Training size is constant: "),
        eq(r"|\text{Train}_k| = W"),
        rt(". Number of folds: "),
        eq(r"K = \lfloor (T - W - h) / s \rfloor + 1")
    ),

    callout("⚠️",
        rt("Prerequisite check: ", bold=True),
        rt("You should know: stationarity, autocorrelation, bias-variance tradeoff, and basic supervised learning CV concepts before this topic.")
    ),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4 — Architecture & Internal Workings
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🔬 Architecture & Internal Workings (PhD-Level)"),

    heading3("Information Flow"),
    numbered(rt("Fix hyperparameters: T, h, s, W (for sliding)")),
    numbered(rt("Enumerate fold origins: k = 1, 2, …, K")),
    numbered(rt("For each fold k: extract train indices, extract val indices")),
    numbered(rt("Fit model on train set ONLY")),
    numbered(rt("Predict on val indices")),
    numbered(rt("Compute error metric (MAE, RMSE, MAPE, etc.) for this fold")),
    numbered(rt("Average errors across K folds → CV score")),

    heading3("Numerical Trace — Expanding Window (T=12, h=2, s=2, min_train=2)"),
    para(rt("Walk through all 4 folds:")),
    table(5,
        table_row(["Fold k", "Train indices", "Val indices", "Train size", "Val size"]),
        table_row(["1", "t1, t2", "t3, t4", "2", "2"]),
        table_row(["2", "t1–t4", "t5, t6", "4", "2"]),
        table_row(["3", "t1–t6", "t7, t8", "6", "2"]),
        table_row(["4", "t1–t8", "t9, t10", "8", "2"]),
    ),
    para(rt("Final CV score: average of 4 fold errors. Note: t11, t12 are never used as validation — they would require train up to t10.")),

    heading3("Numerical Trace — Sliding Window (T=12, h=2, W=4, s=2)"),
    table(5,
        table_row(["Fold k", "Train indices", "Val indices", "Train size", "Val size"]),
        table_row(["1", "t1–t4", "t5, t6", "4", "2"]),
        table_row(["2", "t3–t6", "t7, t8", "4", "2"]),
        table_row(["3", "t5–t8", "t9, t10", "4", "2"]),
    ),
    para(rt("Training size is always 4. t11, t12 unused.")),

    heading3("Design Decisions"),
    callout("🤔",
        rt("Why not random split? ", bold=True),
        rt("Temporal autocorrelation means training on t+1 and validating on t is unrealistic. The model would 'know the future' during training, making error estimates wildly optimistic.")
    ),
    callout("🤔",
        rt("Expanding vs sliding — the key trade-off: ", bold=True),
        rt("Expanding window assumes the data-generating process is stationary or slowly changing — more data is always better. Sliding window assumes regime shifts or non-stationarity — recent data is more relevant than distant past.")
    ),

    heading3("Edge Cases & Failure Modes"),
    bullet(rt("Too few folds: if T is small relative to h, you get K=1 or K=2 — essentially a single hold-out, high variance estimate.")),
    bullet(rt("Gap/contamination: in financial data, train[t] and val[t+1] may still share information (e.g. overlapping features). Use a gap parameter: skip g observations between train end and val start.")),
    bullet(rt("Non-stationarity: expanding window with very old data can hurt — model trained on pre-regime-change data gets 'confused'. Solution: add a min_train cutoff to discard oldest folds from averaging.")),
    bullet(rt("Horizon mismatch: CV with h=1 does not estimate performance for h=5. Always match CV horizon to deployment horizon.")),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5 — The Math
    # ══════════════════════════════════════════════════════════════════════════
    heading2("📐 The Math Behind It"),

    heading3("CV Score Definition"),
    para(rt("The cross-validation score is the average loss across all K folds:")),
    equation_block(r"\widehat{\text{CV}} = \frac{1}{K} \sum_{k=1}^{K} L\bigl(\hat{y}_{\text{val}_k},\, y_{\text{val}_k}\bigr)"),
    para(
        rt("where "),
        eq(r"L"),
        rt(" is a loss function (e.g. MSE, MAE) and "),
        eq(r"\hat{y}_{\text{val}_k}"),
        rt(" is the model's forecast for validation fold k.")
    ),

    heading3("Bias Analysis"),
    para(rt("Let the true expected loss be:")),
    equation_block(r"\mathcal{E} = \mathbb{E}\bigl[L(\hat{y}_{T+h},\, y_{T+h})\bigr]"),
    para(
        rt("Under mild stationarity assumptions, "),
        eq(r"\widehat{\text{CV}}"),
        rt(" is an approximately unbiased estimator of "),
        eq(r"\mathcal{E}"),
        rt(". The bias is:")
    ),
    equation_block(r"\text{Bias} = \mathbb{E}[\widehat{\text{CV}}] - \mathcal{E} \approx -\frac{\text{Cov}(\hat{y}, y)}{\mathcal{E}}"),
    para(rt("Bias tends to be pessimistic (over-estimates true error) rather than optimistic, unlike shuffled k-fold which is strongly optimistic for autocorrelated data.")),

    heading3("Variance of the CV Estimator"),
    para(rt("Because fold errors are correlated (overlapping training sets in expanding window):")),
    equation_block(r"\operatorname{Var}(\widehat{\text{CV}}) = \frac{1}{K^2}\left[\sum_{k=1}^K \operatorname{Var}(L_k) + 2\sum_{j < k} \operatorname{Cov}(L_j, L_k)\right]"),
    para(rt("The covariance terms are non-zero because fold k uses a strict superset of fold j's training data (expanding) or overlapping data (sliding with s < W). This means time-series CV has higher variance than standard k-fold with the same number of folds.")),

    heading3("Optimal Window Size (Sliding)"),
    para(rt("For an AR(p) process with known autocorrelation structure, the optimal window size W* minimizes MSE of the CV estimator:")),
    equation_block(r"W^* = \arg\min_W \left[\text{Bias}^2(W) + \text{Var}(W)\right]"),
    para(rt("In practice, W is a hyperparameter chosen by nested CV or domain knowledge (e.g. W = 2–3 seasonal cycles).")),

    callout("⚠️",
        rt("Common Mathematical Misconception: ", bold=True),
        rt("Many practitioners assume 'more folds = better estimate' always. For time series, adding folds by reducing min_train means early folds have tiny training sets — the model is severely underfitted, introducing downward bias in performance estimates. Set a sensible min_train (at least one full seasonal cycle or max(p, q) for ARIMA).")
    ),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6 — Code Implementation
    # ══════════════════════════════════════════════════════════════════════════
    heading2("💻 Code Implementation"),

    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """import numpy as np

def expanding_window_cv(y, h=1, min_train=2, step=1):
    \"\"\"
    Forward-chaining CV with expanding training window.

    Args:
        y:         time series array of length T
        h:         forecast horizon
        min_train: minimum training set size (skip early folds if too small)
        step:      stride between fold origins
    Yields:
        (train_idx, val_idx) tuples
    \"\"\"
    T = len(y)
    # Slide the origin from min_train to T-h, stepping by `step`
    for origin in range(min_train, T - h + 1, step):
        train_idx = list(range(origin))              # [0, 1, ..., origin-1]
        val_idx   = list(range(origin, origin + h))  # [origin, ..., origin+h-1]
        yield train_idx, val_idx


def sliding_window_cv(y, W, h=1, step=1):
    \"\"\"
    Forward-chaining CV with fixed sliding training window.

    Args:
        y:    time series array of length T
        W:    training window size (constant)
        h:    forecast horizon
        step: stride between fold origins
    Yields:
        (train_idx, val_idx) tuples
    \"\"\"
    T = len(y)
    for start in range(0, T - W - h + 1, step):
        train_idx = list(range(start, start + W))        # fixed size W
        val_idx   = list(range(start + W, start + W + h))
        yield train_idx, val_idx


# ── Usage example ────────────────────────────────────────────────────────────
y = np.array([1.2, 2.1, 1.8, 3.0, 2.5, 3.8, 3.2, 4.1, 3.9, 5.0, 4.5, 6.0])

def naive_forecast(y_train, h):
    \"\"\"Predict last observed value h steps ahead (baseline).\"\"\"
    return np.full(h, y_train[-1])

def cv_score(y, splits_fn, metric=lambda y_true, y_pred: np.mean(np.abs(y_true - y_pred))):
    errors = []
    for train_idx, val_idx in splits_fn:
        y_train, y_val = y[train_idx], y[val_idx]
        y_pred = naive_forecast(y_train, len(val_idx))
        errors.append(metric(y_val, y_pred))
    return np.mean(errors), np.std(errors)

mean_err, std_err = cv_score(y, expanding_window_cv(y, h=2, min_train=2, step=2))
print(f"Expanding CV  — MAE: {mean_err:.3f} ± {std_err:.3f}")

mean_err, std_err = cv_score(y, sliding_window_cv(y, W=4, h=2, step=2))
print(f"Sliding CV    — MAE: {mean_err:.3f} ± {std_err:.3f}")
"""),

    heading3("6b — Production (scikit-learn)"),
    code_block("python", """from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import Ridge
import numpy as np

# ── TimeSeriesSplit: expanding window ────────────────────────────────────────
tscv = TimeSeriesSplit(
    n_splits=5,          # number of folds K
    max_train_size=None, # None = expanding; set int for sliding-like behavior
    test_size=2,         # validation horizon h
    gap=0,               # observations to skip between train end and val start
)

# Feature matrix: lag features for AR(3) model
def make_features(y, lags=3):
    X, target = [], []
    for i in range(lags, len(y)):
        X.append(y[i-lags:i])
        target.append(y[i])
    return np.array(X), np.array(target)

y = np.array([1.2, 2.1, 1.8, 3.0, 2.5, 3.8, 3.2, 4.1, 3.9, 5.0, 4.5, 6.0])
X, y_target = make_features(y, lags=3)

model = Ridge(alpha=1.0)
fold_maes = []

for fold, (train_idx, val_idx) in enumerate(tscv.split(X), 1):
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y_target[train_idx], y_target[val_idx]

    model.fit(X_train, y_train)
    y_pred = model.predict(X_val)

    mae = np.mean(np.abs(y_val - y_pred))
    fold_maes.append(mae)
    print(f"Fold {fold}: train={len(train_idx)}, val={len(val_idx)}, MAE={mae:.3f}")

print(f"CV MAE: {np.mean(fold_maes):.3f} ± {np.std(fold_maes):.3f}")

# ⚠️ Gotcha: max_train_size is NOT exactly sliding window —
#    it caps train size but origin still advances. For true sliding,
#    combine max_train_size with a custom generator.

# ── Gap usage (financial/leakage prevention) ─────────────────────────────────
tscv_gap = TimeSeriesSplit(n_splits=4, test_size=2, gap=5)
# 5 observations skipped between train end and val start
# Prevents leakage from overlapping features (e.g. rolling means)
"""),

    callout("⚠️",
        rt("Gotcha: ", bold=True),
        rt("sklearn's TimeSeriesSplit with max_train_size is NOT a true sliding window — it still advances the origin. For strict sliding window use a custom generator. Also: n_splits in sklearn counts validation folds only; the first training set size is T/(n_splits+1) by default.")
    ),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 7 — Interview Deep-Dive
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎯 Interview Deep-Dive"),

    toggle(
        [rt("Q1 (Easy): Why can't we use standard k-fold for time series?", bold=True)],
        [
            para(rt("Standard k-fold randomly shuffles data before splitting. For time series, this means a model may be trained on t=100 and evaluated on t=50 — it has implicitly 'seen the future'. This is temporal leakage, producing wildly optimistic error estimates. We must always train on past, validate on future.")),
            callout("⚠️",
                rt("Follow-up trap: ", bold=True),
                rt("'What if the series is stationary — does ordering still matter?' Yes. Even for stationary processes, autocorrelation means fold errors become correlated in an unrealistic way, invalidating the i.i.d. assumption underlying standard CV theory.")
            ),
        ]
    ),

    toggle(
        [rt("Q2 (Easy): What is the difference between expanding and sliding window CV?", bold=True)],
        [
            para(rt("Expanding window: training set grows by adding new observations each fold. Fold 1 uses [t1…t_min], fold 2 uses [t1…t_{min+s}], etc. Sliding window: training set has fixed size W, and slides forward. Fold 1 = [t1…tW], fold 2 = [t_{s+1}…t_{W+s}].")),
            para(rt("Key difference: expanding assumes stationarity (all history is useful). Sliding assumes non-stationarity or regime shifts (recent history more relevant, old data harmful).")),
        ]
    ),

    toggle(
        [rt("Q3 (Medium): When would you prefer sliding window over expanding?", bold=True)],
        [
            para(rt("Use sliding window when:")),
            bullet(rt("Data exhibits concept drift (distribution of features/target changes over time)")),
            bullet(rt("Pre-regime-change data (e.g., pre-COVID, pre-restructuring) would mislead the model")),
            bullet(rt("You have strong domain knowledge that recent patterns are more predictive")),
            bullet(rt("The series has strong seasonality and you want each fold to contain exactly one full seasonal cycle")),
            para(rt("Use expanding when:")),
            bullet(rt("Series is stationary or slowly non-stationary")),
            bullet(rt("More data consistently improves model accuracy")),
            bullet(rt("T is small and you can't afford to discard any history")),
        ]
    ),

    toggle(
        [rt("Q4 (Medium): What is a 'gap' in time series CV and when is it needed?", bold=True)],
        [
            para(rt("A gap (also called embargo) is a set of observations skipped between the training set end and validation set start. For example, with gap=5, if training ends at t=100, validation starts at t=106.")),
            para(rt("Needed when:")),
            bullet(rt("Target is computed from rolling features (e.g., 7-day moving average) — overlapping windows cause leakage")),
            bullet(rt("Financial returns: if features include future prices indirectly (e.g., volume that anticipates a move)")),
            bullet(rt("Any derived feature whose computation window crosses the train/val boundary")),
            para(rt("Lopez de Prado (2018) 'Advances in Financial Machine Learning' formalizes purged CV and combinatorial purged CV for hedge fund ML.")),
        ]
    ),

    toggle(
        [rt("Q5 (Hard): Explain to a PhD Researcher: what is the bias-variance decomposition of time series CV error?", bold=True)],
        [
            para(rt("For a PhD audience:")),
            para(
                rt("The CV estimator "),
                eq(r"\widehat{\text{CV}} = K^{-1}\sum_k L_k"),
                rt(" is an estimator of the expected test loss "),
                eq(r"\mathcal{E}"),
                rt(". Its MSE decomposes as:")
            ),
            equation_block(r"\text{MSE}(\widehat{\text{CV}}) = \text{Bias}^2(\widehat{\text{CV}}) + \text{Var}(\widehat{\text{CV}})"),
            para(
                rt("Bias: In expanding window, early folds have small training sets → model underfits → loss "),
                eq(r"L_k"),
                rt(" overestimates "),
                eq(r"\mathcal{E}"),
                rt(" (pessimistic bias). Bergmeir & Benitez (2012) showed this bias is bounded for stationary processes.")
            ),
            para(
                rt("Variance: Folds are dependent — "),
                eq(r"\text{Cov}(L_j, L_k) > 0"),
                rt(" because the training sets are nested (expanding) or overlapping (sliding with s < W). Standard SE = "),
                eq(r"\text{SD}(L_k)/\sqrt{K}"),
                rt(" underestimates true uncertainty. Correct variance estimator must account for covariance structure.")
            ),
            para(
                rt("For research: Cerqueira et al. (2020) propose the blocked rolling-origin strategy and show it minimizes the sum of squared errors vs. a wide range of time series types. The optimal stride s depends on the autocorrelation structure of the error sequence "),
                eq(r"\{L_k\}"),
                rt(".")
            ),
        ]
    ),

    toggle(
        [rt("Q6 (Hard): Explain to a Research Scientist: how do you choose between expanding and sliding in practice?", bold=True)],
        [
            para(rt("For an ML practitioner audience:")),
            numbered(rt("Run an ADF or KPSS test. If the series is non-stationary (unit root), strongly consider sliding window.")),
            numbered(rt("Split series into thirds: early, mid, late. Train model on early, eval on mid. Train on early+mid, eval on late. If late performance >> mid performance, data is non-stationary — sliding is safer.")),
            numbered(rt("Try both and compare CV score stability (std across folds). High std in expanding = non-stationarity hurting; high std in sliding = window too small.")),
            numbered(rt("As a heuristic: W ≈ 2–3 seasonal cycles is a good starting point. Use nested CV to tune W if you have enough data.")),
            numbered(rt("In production: monitor model performance on live data; retrain trigger when rolling CV score degrades beyond threshold.")),
        ]
    ),

    toggle(
        [rt("Q7 (Hard): System design — how would you implement time series CV for a production ML pipeline with 10M rows and 500 models?", bold=True)],
        [
            para(rt("Architecture considerations:")),
            bullet(rt("Vectorize fold extraction using NumPy index arrays — avoid Python loops over rows")),
            bullet(rt("For 500 models: use joblib.Parallel or Ray to distribute fold evaluations across cores/machines")),
            bullet(rt("Feature computation is often the bottleneck — precompute all lag/rolling features once across full T, then slice per fold")),
            bullet(rt("Store CV results (fold index, model ID, train_end, val_start, metric) in a table for later analysis")),
            bullet(rt("With 10M rows and W=1M: each fold is ~1M rows — use chunked/incremental training (River, scikit-learn partial_fit) or reservoir sampling for older folds")),
            bullet(rt("Monitor CV score drift over calendar time: if performance degrades after t=2023, trigger retraining with post-2023 data only")),
        ]
    ),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 8 — Comparison & Trade-offs
    # ══════════════════════════════════════════════════════════════════════════
    heading2("⚖️ Comparison & Trade-offs"),

    table(4,
        table_row(["Dimension", "Expanding Window", "Sliding Window", "Single Hold-Out"]),
        table_row(["Train size", "Grows each fold", "Fixed (W)", "Fixed (one split)"]),
        table_row(["History used", "All history", "Last W observations", "First 1-h fraction"]),
        table_row(["Drift adaptation", "Slow (old data dilutes)", "Fast (old data dropped)", "None"]),
        table_row(["Fold count K", "T/s - min_train/s", "(T-W-h)/s + 1", "1"]),
        table_row(["Bias", "Pessimistic (early folds underfit)", "Low (if W chosen well)", "High variance"]),
        table_row(["Computation", "O(K · T) features; O(K · T²) for some models", "O(K · W)", "O(T)"]),
        table_row(["Best for", "Stationary or slow-drift TS", "Non-stationary / concept drift", "Large T, fast iteration"]),
        table_row(["sklearn support", "TimeSeriesSplit (default)", "TimeSeriesSplit(max_train_size=W)", "train_test_split"]),
    ),

    callout("🎯",
        rt("Decision guide: ", bold=True),
        rt("Stationary + want max data → Expanding. Non-stationary / regime shifts → Sliding. Research prototype / huge T → Hold-out. Financial ML with overlapping features → Sliding + Gap (purged CV).")
    ),

    bullet(rt("Expanding advantages: uses all available history; unbiased when data is stationary; simple to implement")),
    bullet(rt("Expanding disadvantages: slow adaptation to distribution shift; old folds may dominate if weighted equally")),
    bullet(rt("Sliding advantages: adapts to regime shifts; constant train size → predictable compute budget")),
    bullet(rt("Sliding disadvantages: discards potentially useful history; requires choosing W (additional hyperparameter)")),
    bullet(rt("Purged/Gap CV advantages: no leakage even with complex overlapping features")),
    bullet(rt("Purged CV disadvantages: fewer usable folds; complex to implement")),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 9 — Interactive Explainer
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎯 Interactive Visual Explainer"),

    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/time_series_cv_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),

    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10 — Related Topics & Further Reading
    # ══════════════════════════════════════════════════════════════════════════
    heading2("📚 Related Topics & Further Reading"),

    heading3("Prerequisites"),
    bullet(rt("Supervised learning fundamentals (train/test split, overfitting)")),
    bullet(rt("k-fold cross-validation (why it works for i.i.d. data)")),
    bullet(rt("Autocorrelation and stationarity (ADF test, KPSS test)")),
    bullet(rt("AR/MA/ARIMA models (what we're typically evaluating)")),

    heading3("What to Learn Next"),
    bullet(rt("Backtesting in quantitative finance (purged CV, combinatorial purged CV — Lopez de Prado 2018)")),
    bullet(rt("Blocked / stratified CV for panel data (multiple time series)")),
    bullet(rt("Hyperparameter tuning for time series models (nested TS-CV)")),
    bullet(rt("Online learning and concept drift detection (ADWIN, DDM)")),

    heading3("Key Papers"),
    bullet(rt("Bergmeir & Benitez (2012) — 'On the use of cross-validation for time series predictor evaluation', Information Sciences")),
    bullet(rt("Cerqueira, Torgo, & Mozetič (2020) — 'Evaluating time series forecasting models: An empirical study on performance estimation methods', Machine Learning")),
    bullet(rt("Lopez de Prado (2018) — 'Advances in Financial Machine Learning', Ch. 7 (Purged Cross-Validation)")),
    bullet(rt("Hyndman & Athanasopoulos (2018) — 'Forecasting: Principles and Practice', 2nd ed., Section 3.4")),

    callout("🔗",
        rt("This topic connects to: ", bold=True),
        rt("ARIMA & Seasonal Decomposition (STL) · Gradient Boosted Trees for time series (LightGBM) · Model selection & regularization · Evaluation metrics (MAE, RMSE, MAPE, SMAPE) · Online learning & concept drift")
    ),

]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
