#!/usr/bin/env python3
"""Update Notion page for: Practical solvers — libSVM, LIBLINEAR"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8193-a14f-ebb612d1beaa"
ICON = "🟡"   # Intermediate

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/svm_solvers_libsvm_explainer.html"},
}

blocks = [

    # ── Section 1: 30-Second Version ──────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("SVMs need an optimizer to find the maximum-margin hyperplane. Two open-source libraries dominate practice: "),
         rt("libSVM", bold=True),
         rt(" (Chang & Lin, 2001–2011) and "),
         rt("LIBLINEAR", bold=True),
         rt(" (Fan et al., 2008). They share a goal but diverge sharply on algorithm and applicable problem class.")),
    heading3("Real-World Analogy"),
    para(rt("libSVM is a bespoke tailor who can craft any silhouette (kernel boundary) but must measure every pair of customers against each other — quadratic effort. LIBLINEAR is a factory line: it only makes straight-cut suits but finishes a million in the time libSVM does a thousand.")),
    heading3("One-Sentence Summary"),
    para(rt("Use libSVM when you need kernels or have "),
         eq("n < 100{,}000"),
         rt("; switch to LIBLINEAR when "),
         eq("n > 100{,}000"),
         rt(" and a linear boundary suffices.")),
    callout("💡",
            rt("If you remember one thing: ", bold=True),
            rt("libSVM ↔ SMO ↔ kernels ↔ "),
            eq("O(n^2)"),
            rt(" – "),
            eq("O(n^3)"),
            rt(" — LIBLINEAR ↔ coordinate descent ↔ linear only ↔ "),
            eq("O(n \\cdot d)"),
            rt(".")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Solving the SVM dual is a Quadratic Program (QP) in "),
         eq("n"),
         rt(" variables. Generic interior-point QP solvers are "),
         eq("O(n^3)"),
         rt(" in time and "),
         eq("O(n^2)"),
         rt(" in memory — prohibitive for even moderate datasets ("),
         eq("n = 10{,}000"),
         rt(" → 800 MB kernel matrix, hours of compute).")),
    heading3("What Came Before"),
    para(rt("Early SVM work (Vapnik 1995, Boser et al. 1992) used standard QP solvers (MINOS, LOQO). These required the full "),
         eq("n \\times n"),
         rt(" kernel matrix in RAM and off-the-shelf QP solvers. Practical limit was "),
         eq("n \\approx 1{,}000"),
         rt(".")),
    heading3("The Breakthroughs"),
    bullet(rt("1998 — "), rt("Platt's SMO", bold=True), rt(": decompose dual QP into 2-variable sub-problems solvable analytically. Enables "), eq("n \\approx 50{,}000"), rt(" with kernel caching.")),
    bullet(rt("2001 — "), rt("libSVM (Chang & Lin)", bold=True), rt(": packaged SMO with working-set selection, kernel cache management, and multi-class support. Became the de-facto standard.")),
    bullet(rt("2008 — "), rt("LIBLINEAR (Fan et al., JMLR)", bold=True), rt(": coordinate descent directly on primal/dual for linear SVMs. Scales to "), eq("n = 10^6"), rt(" in minutes. Handles logistic regression too.")),
    heading3("Before vs. After"),
    table(3,
        table_row(["Dimension", "Pre-SMO / Generic QP", "libSVM (SMO) / LIBLINEAR (CD)"]),
        table_row(["Memory", "O(n²) full kernel matrix", "O(n·cache) or O(d)"]),
        table_row(["Practical n limit", "~1,000", "50k–100k (libSVM), millions (LIBLINEAR)"]),
        table_row(["Kernel support", "Any", "Any (libSVM) / Linear only (LIBLINEAR)"]),
        table_row(["Sub-problem solved", "Full QP (n variables)", "2 variables (SMO) / 1 variable (CD)"]),
        table_row(["Time complexity", "O(n³)", "O(n²–n³) libSVM / O(nd) LIBLINEAR"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ─────────────────────────────────────
    heading2("📐 Core Concepts & Theory"),
    heading3("Definitions"),
    para(rt("Let "),
         eq("\\{(x_i, y_i)\\}_{i=1}^n"),
         rt(", "),
         eq("x_i \\in \\mathbb{R}^d"),
         rt(", "),
         eq("y_i \\in \\{-1, +1\\}"),
         rt(". The feature map is "),
         eq("\\phi: \\mathbb{R}^d \\to \\mathcal{H}"),
         rt(", kernel "),
         eq("k(x, x') = \\langle \\phi(x), \\phi(x') \\rangle_{\\mathcal{H}}"),
         rt(".")),
    heading3("Primal Problem (soft-margin SVM)"),
    equation_block(r"\min_{w,b,\xi}\; \frac{1}{2}\|w\|^2 + C\sum_{i=1}^n \xi_i \quad \text{s.t.}\quad y_i(w^\top\phi(x_i)+b)\ge 1-\xi_i,\;\xi_i\ge 0"),
    heading3("Dual Problem"),
    equation_block(r"\max_\alpha\; \sum_i \alpha_i - \frac{1}{2}\sum_{i,j}\alpha_i\alpha_j y_i y_j K_{ij} \quad \text{s.t.}\quad 0\le\alpha_i\le C,\;\sum_i\alpha_i y_i = 0"),
    para(rt("Both libSVM and LIBLINEAR optimize the dual, but via fundamentally different decomposition strategies.")),
    callout("🔑",
            rt("Core Property: ", bold=True),
            rt("libSVM decomposes the dual QP into 2-variable sub-problems (closed-form solution via analytic clipping). LIBLINEAR decomposes it into 1-variable sub-problems that have a closed-form update because "),
            eq("K_{ij} = x_i^\\top x_j"),
            rt(" is cheap to compute for linear kernels.")),
    heading3("Prerequisites"),
    bullet(rt("SVM primal/dual formulation (hard- and soft-margin)")),
    bullet(rt("Quadratic programming and KKT conditions")),
    bullet(rt("Mercer's theorem (kernel PSD condition)")),
    bullet(rt("Convex optimization basics")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ───────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD-Level)"),
    heading3("libSVM — SMO Algorithm"),
    para(rt("SMO (Platt 1998) solves the dual QP by repeatedly picking a working set of exactly 2 dual variables and solving the resulting 1-D QP analytically.")),
    heading3("Working Set Selection"),
    para(rt("libSVM uses the maximal violating pair (MVP) rule: find "),
         eq("i = \\arg\\max_{\\alpha_i < C} (-y_i f_i)"),
         rt(" and "),
         eq("j = \\arg\\min_{\\alpha_j > 0} (-y_j f_j)"),
         rt(", where "),
         eq("f_i = \\sum_k \\alpha_k y_k K_{ki} + b"),
         rt(" is the current decision value. These two points are the most KKT-violating pair, guaranteeing maximal dual improvement per step.")),
    heading3("Analytic Update"),
    equation_block(r"\eta = K_{ii} + K_{jj} - 2K_{ij}"),
    equation_block(r"\alpha_j^{\text{new}} = \alpha_j + \frac{y_j(E_i - E_j)}{\eta}, \quad E_k = f_k - y_k"),
    para(rt("Then clip "),
         eq("\\alpha_j^{\\text{new}}"),
         rt(" to "),
         eq("[L, H]"),
         rt(" where:"),
         ),
    bullet(rt("If "),
           eq("y_i \\ne y_j"),
           rt(": "),
           eq("L = \\max(0, \\alpha_j - \\alpha_i)"),
           rt(", "),
           eq("H = \\min(C, C + \\alpha_j - \\alpha_i)")),
    bullet(rt("If "),
           eq("y_i = y_j"),
           rt(": "),
           eq("L = \\max(0, \\alpha_j + \\alpha_i - C)"),
           rt(", "),
           eq("H = \\min(C, \\alpha_j + \\alpha_i)")),
    para(rt("Finally update "),
         eq("\\alpha_i^{\\text{new}} = \\alpha_i + y_i y_j(\\alpha_j^{\\text{old}} - \\alpha_j^{\\text{new}})"),
         rt(" (from the equality constraint "),
         eq("\\sum_k \\alpha_k y_k = 0"),
         rt(").")),
    para(rt("When "),
         eq("\\eta = 0"),
         rt(" (degenerate case: "),
         eq("K_{ii} + K_{jj} = 2K_{ij}"),
         rt("), libSVM evaluates the dual at both boundary candidates "),
         eq("L"),
         rt(" and "),
         eq("H"),
         rt(" and takes the one with larger objective — a safe fallback.")),
    heading3("Kernel Caching"),
    para(rt("Computing "),
         eq("K_{ij}"),
         rt(" costs "),
         eq("O(d)"),
         rt(" per pair. libSVM maintains an LRU cache of kernel columns (default 200 MB). Cache hit rate is critical: poor cache use makes the algorithm behave as "),
         eq("O(n^3)"),
         rt("; good cache use approaches "),
         eq("O(n^2 d)"),
         rt(".")),
    heading3("LIBLINEAR — Dual Coordinate Descent"),
    para(rt("For linear kernels, "),
         eq("K_{ij} = x_i^\\top x_j"),
         rt(" and "),
         eq("w = \\sum_i \\alpha_i y_i x_i \\in \\mathbb{R}^d"),
         rt(". Maintain "),
         eq("w"),
         rt(" explicitly; updating one "),
         eq("\\alpha_i"),
         rt(" costs "),
         eq("O(d)"),
         rt(" rather than "),
         eq("O(n)"),
         rt(".")),
    heading3("L2-regularized L2-loss SVC Dual CD Step"),
    equation_block(r"G_i = y_i(w^\top x_i) - 1 + \frac{\alpha_i}{2C}"),
    equation_block(r"\Delta\alpha_i = \min\!\left(\max\!\left(\frac{-G_i}{\|x_i\|^2 + \frac{1}{2C}},\; -\alpha_i\right),\; C - \alpha_i\right)"),
    equation_block(r"w \leftarrow w + \Delta\alpha_i\, y_i\, x_i"),
    para(rt("One pass through all "),
         eq("n"),
         rt(" coordinates costs "),
         eq("O(n \\cdot d)"),
         rt(" (or "),
         eq("O(\\sum_i \\mathrm{nnz}(x_i))"),
         rt(" for sparse data). LIBLINEAR shuffles the coordinate order each pass to improve convergence.")),
    heading3("Convergence Guarantees"),
    para(rt("For L2-regularized objectives (strongly convex), dual CD has "),
         rt("R-linear (geometric) convergence rate", bold=True),
         rt(": the duality gap shrinks as "),
         eq("O(\\rho^k)"),
         rt(" for some "),
         eq("\\rho \\in (0,1)"),
         rt(". Empirically 10–50 passes suffice for "),
         eq("\\epsilon = 10^{-3}"),
         rt(" precision, regardless of "),
         eq("n"),
         rt(".")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("libSVM with large "), eq("n"), rt(" (>200k): training time > hours; kernel cache thrashes.")),
    bullet(rt("LIBLINEAR on non-linearly separable data with wrong C: may not converge within max_iter; increase max_iter or tune C.")),
    bullet(rt("libSVM with "), eq("\\eta < 0"), rt(": should not happen with valid PSD kernels; if it does, a non-Mercer kernel was used (bug).")),
    bullet(rt("libSVM probability=True: adds Platt scaling (another 5-fold CV), doubles training time.")),
    divider(),

    # ── Section 5: The Math Behind It ─────────────────────────────────────────
    heading2("📏 The Math Behind It"),
    heading3("Dual Derivation (shared)"),
    para(rt("Introduce dual variables "),
         eq("\\alpha_i \\ge 0"),
         rt(" for inequality constraints and "),
         eq("\\nu \\in \\mathbb{R}"),
         rt(" for equality. The Lagrangian is:")),
    equation_block(r"L = \frac{1}{2}\|w\|^2 + C\sum_i\xi_i - \sum_i\alpha_i[y_i(w^\top\phi(x_i)+b)-1+\xi_i] - \sum_i\mu_i\xi_i - \nu\sum_i\alpha_i y_i"),
    para(rt("Setting partial derivatives to zero:")),
    bullet(eq("\\partial L/\\partial w = 0 \\implies w = \\sum_i \\alpha_i y_i \\phi(x_i)")),
    bullet(eq("\\partial L/\\partial b = 0 \\implies \\sum_i \\alpha_i y_i = 0")),
    bullet(eq("\\partial L/\\partial \\xi_i = 0 \\implies \\alpha_i + \\mu_i = C \\implies 0 \\le \\alpha_i \\le C")),
    para(rt("Substituting back gives the dual:")),
    equation_block(r"\max_\alpha \;\mathbf{1}^\top\alpha - \frac{1}{2}\alpha^\top Q\alpha \quad \text{s.t.}\quad y^\top\alpha = 0,\; 0 \le \alpha \le C\mathbf{1}"),
    para(rt("where "),
         eq("Q_{ij} = y_i y_j K_{ij}"),
         rt(". Decision function: "),
         eq("f(x) = \\sum_i \\alpha_i y_i k(x_i, x) + b"),
         rt(".")),
    heading3("SMO Two-Variable Optimality"),
    para(rt("Fixing all "),
         eq("\\alpha"),
         rt(" except "),
         eq("(\\alpha_i, \\alpha_j)"),
         rt(", the sub-problem becomes a 1-D quadratic in "),
         eq("\\alpha_j"),
         rt(" (using the equality constraint to eliminate "),
         eq("\\alpha_i"),
         rt("):")),
    equation_block(r"\max_{\alpha_j}\; (E_i - E_j)\alpha_j - \frac{\eta}{2}\alpha_j^2 + \text{const}, \quad \eta = K_{ii}+K_{jj}-2K_{ij}"),
    para(rt("Unconstrained optimum: "),
         eq("\\alpha_j^* = \\alpha_j + (E_i - E_j)/\\eta"),
         rt(". Clip to "),
         eq("[L,H]"),
         rt(". By Mercer's theorem, "),
         eq("\\eta \\ge 0"),
         rt("; when "),
         eq("\\eta > 0"),
         rt(" this is a concave quadratic with unique maximum.")),
    heading3("Coordinate Descent Derivation for L2-SVM"),
    para(rt("The dual objective for L2-regularized L2-loss SVM is:")),
    equation_block(r"D(\alpha) = \sum_i \alpha_i - \frac{1}{2}\alpha^\top Q\alpha - \frac{1}{2C}\sum_i\alpha_i^2"),
    para(rt("Gradient w.r.t. "),
         eq("\\alpha_i"),
         rt(":")),
    equation_block(r"\nabla_i D = 1 - \sum_j Q_{ij}\alpha_j - \frac{\alpha_i}{C} = 1 - y_i(w^\top x_i) - \frac{\alpha_i}{C} = -G_i"),
    para(rt("The L2 diagonal term "),
         eq("\\frac{\\alpha_i}{C}"),
         rt(" (from the primal "),
         eq("\\frac{1}{2C}"),
         rt("-regularization of "),
         eq("\\xi_i"),
         rt(") ensures the Hessian diagonal "),
         eq("Q_{ii} + \\frac{1}{C} = \\|x_i\\|^2 + \\frac{1}{C} > 0"),
         rt(", making the 1-D subproblem strongly convex and the update unique.")),
    callout("⚠️",
            rt("Warning: ", bold=True),
            rt("sklearn's LinearSVC uses L2-regularized L1-loss by default, not L2-loss. The dual has box constraints "),
            eq("0 \\le \\alpha_i \\le C"),
            rt(" without the diagonal term. Use "),
            rt("loss='squared_hinge'", code=True),
            rt(" for L2-loss. The convergence and accuracy differ.")),
    divider(),

    # ── Section 6: Code Implementation ────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — SMO From Scratch (NumPy, binary classification)"),
    code_block("python", '''import numpy as np

def smo_svm(X, y, C=1.0, tol=1e-3, max_passes=50, kernel="rbf", gamma=1.0):
    """Minimal SMO implementation for binary SVM.

    Args:
        X: (n, d) feature matrix
        y: (n,) labels in {-1, +1}
        C: regularization (box constraint upper bound)
        tol: KKT violation tolerance
        max_passes: max passes without alpha change
        kernel: "rbf" or "linear"
        gamma: RBF bandwidth
    Returns:
        alpha: (n,) dual variables
        b: bias scalar
    """
    n = X.shape[0]

    # --- Kernel matrix (full, for simplicity) ---
    if kernel == "rbf":
        # K[i,j] = exp(-gamma * ||x_i - x_j||^2)
        sq_dists = np.sum(X**2, axis=1).reshape(-1,1) + np.sum(X**2, axis=1) - 2*X@X.T
        K = np.exp(-gamma * sq_dists)
    else:
        K = X @ X.T  # linear kernel

    alpha = np.zeros(n)
    b = 0.0
    passes = 0

    while passes < max_passes:
        num_changed = 0

        for i in range(n):
            # Decision function value and error for sample i
            fi = float((alpha * y) @ K[i]) + b
            Ei = fi - y[i]

            # Check KKT violation
            if not (
                (y[i]*Ei < -tol and alpha[i] < C) or
                (y[i]*Ei >  tol and alpha[i] > 0)
            ):
                continue

            # Pick j != i randomly (heuristic; production libSVM uses MVP)
            j = i
            while j == i:
                j = np.random.randint(n)

            fj = float((alpha * y) @ K[j]) + b
            Ej = fj - y[j]

            ai_old, aj_old = alpha[i], alpha[j]

            # Compute bounds L, H
            if y[i] == y[j]:
                L = max(0.0, alpha[j] + alpha[i] - C)
                H = min(C,   alpha[j] + alpha[i])
            else:
                L = max(0.0, alpha[j] - alpha[i])
                H = min(C,   C + alpha[j] - alpha[i])
            if L >= H:
                continue

            # Compute eta (denominator)
            eta = K[i,i] + K[j,j] - 2*K[i,j]
            if eta <= 0:
                # Degenerate: evaluate at boundaries (libSVM fallback)
                continue

            # Update alpha_j
            alpha[j] += y[j] * (Ei - Ej) / eta
            alpha[j] = np.clip(alpha[j], L, H)  # clip to [L, H]

            if abs(alpha[j] - aj_old) < 1e-5:
                continue

            # Update alpha_i (from equality constraint sum(alpha*y)=0)
            alpha[i] += y[i] * y[j] * (aj_old - alpha[j])

            # Update bias b
            b1 = b - Ei - y[i]*(alpha[i]-ai_old)*K[i,i] - y[j]*(alpha[j]-aj_old)*K[i,j]
            b2 = b - Ej - y[i]*(alpha[i]-ai_old)*K[i,j] - y[j]*(alpha[j]-aj_old)*K[j,j]
            if 0 < alpha[i] < C:
                b = b1
            elif 0 < alpha[j] < C:
                b = b2
            else:
                b = (b1 + b2) / 2.0

            num_changed += 1

        passes = 0 if num_changed > 0 else passes + 1

    return alpha, b

# Predict
def predict(X_train, X_test, y_train, alpha, b, kernel="rbf", gamma=1.0):
    if kernel == "rbf":
        dists = (np.sum(X_test**2, axis=1, keepdims=True)
                 + np.sum(X_train**2, axis=1)
                 - 2 * X_test @ X_train.T)
        K = np.exp(-gamma * dists)
    else:
        K = X_test @ X_train.T
    return np.sign(K @ (alpha * y_train) + b)
'''),
    heading3("6b — Coordinate Descent Update (LIBLINEAR-style, NumPy)"),
    code_block("python", '''import numpy as np

def liblinear_svm(X, y, C=1.0, max_iter=100, tol=1e-4):
    """L2-regularized L2-loss SVM via dual coordinate descent.

    Mirrors LIBLINEAR's core loop (linear kernel only).
    Args:
        X: (n, d) — dense or use sparse equivalent
        y: (n,) in {-1, +1}
        C: regularization parameter
        max_iter: max full passes over coordinates
    Returns:
        w: (d,) weight vector
        b: float bias (set to 0 here; LIBLINEAR uses bias feature x_{d+1}=1)
    """
    n, d = X.shape
    alpha = np.zeros(n)    # dual variables
    w = np.zeros(d)        # primal weights = sum_i alpha_i y_i x_i

    # Precompute ||x_i||^2 for efficiency
    xsq = np.einsum('ij,ij->i', X, X)   # shape (n,)

    for iteration in range(max_iter):
        max_change = 0.0
        # Shuffle indices each pass (improves convergence)
        perm = np.random.permutation(n)

        for i in perm:
            xi = X[i]
            # Gradient of dual objective w.r.t. alpha_i
            # G_i = y_i*(w^T x_i) - 1 + alpha_i / (2C)  [L2-loss]
            G = y[i] * (w @ xi) - 1.0 + alpha[i] / (2.0 * C)

            # Hessian diagonal: Q_ii + 1/C = ||x_i||^2 + 1/(2C)
            PG_denom = xsq[i] + 1.0 / (2.0 * C)

            # Newton-like step (unconstrained)
            delta = -G / PG_denom

            # Clip to box [0, C] for L1-loss; [-inf, C] for L2-loss
            # L2-loss: alpha_i >= 0
            alpha_new = max(0.0, alpha[i] + delta)
            delta_alpha = alpha_new - alpha[i]

            if abs(delta_alpha) > 0:
                alpha[i] = alpha_new
                # Update w in O(d)
                w += delta_alpha * y[i] * xi
                max_change = max(max_change, abs(delta_alpha))

        if max_change < tol:
            print(f"Converged at iteration {iteration+1}")
            break

    return w
'''),
    heading3("6c — Production Usage (sklearn)"),
    code_block("python", '''from sklearn.svm import SVC, LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.calibration import CalibratedClassifierCV
import numpy as np

# ──────────────────────────────────────────────
# libSVM (SVC) — for n < 100k, non-linear data
# ──────────────────────────────────────────────
pipeline_rbf = Pipeline([
    ("scaler", StandardScaler()),   # CRITICAL: SVM needs scaled features
    ("svm", SVC(
        kernel="rbf",
        C=1.0,          # regularization; try [0.01, 0.1, 1, 10, 100]
        gamma="scale",  # 1/(n_features * X.var()) — recommended default
        cache_size=500, # MB for kernel cache; increase for large n
        probability=False,  # True adds 5-fold CV for Platt scaling (slow)
    ))
])

# ──────────────────────────────────────────────
# LIBLINEAR (LinearSVC) — for n > 100k, text/sparse
# ──────────────────────────────────────────────
pipeline_linear = Pipeline([
    ("scaler", StandardScaler(with_mean=False)),  # with_mean=False for sparse
    ("svm", LinearSVC(
        C=1.0,
        max_iter=2000,   # increase if "ConvergenceWarning" fires
        dual=True,       # dual=True preferred when n > d; False when d > n
        loss="squared_hinge",  # L2-loss (matches LIBLINEAR L2-SVM exactly)
        # loss="hinge"   # L1-loss (default in sklearn, slightly different problem)
    ))
])

# For probabilities with LinearSVC (LIBLINEAR has no built-in):
pipeline_calib = Pipeline([
    ("scaler", StandardScaler(with_mean=False)),
    ("svm", CalibratedClassifierCV(
        LinearSVC(C=1.0, max_iter=2000),
        method="sigmoid",  # Platt scaling equivalent
        cv=5,
    ))
])

# ─── Common Gotchas ───────────────────────────
# 1. SVC(kernel="linear") on n=1M → VERY SLOW (uses SMO)
#    FIX: use LinearSVC instead — same model, 100x faster
#
# 2. LinearSVC convergence warning:
#    FIX: increase max_iter=5000 or normalize features better
#
# 3. Multiclass: both use one-vs-rest (OVR) by default
#    SVC also supports one-vs-one (decision_function_shape="ovo")
#
# 4. Feature scaling: SVM is NOT scale-invariant — always scale!
'''),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎯 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy) — What is the difference between libSVM and LIBLINEAR?", bold=True)], [
        para(rt("libSVM implements SMO and supports any Mercer kernel (RBF, polynomial, etc.) with "),
             eq("O(n^2)"),
             rt("–"),
             eq("O(n^3)"),
             rt(" training. LIBLINEAR implements coordinate descent for linear kernels only with "),
             eq("O(n \\cdot d)"),
             rt(" training. The key practical takeaway: use LinearSVC (LIBLINEAR) for text classification with millions of samples; use SVC (libSVM) when you need non-linear boundaries.")),
    ]),
    toggle([rt("Q2 (Easy) — Why can't LIBLINEAR use RBF or polynomial kernels?", bold=True)], [
        para(rt("LIBLINEAR's efficiency relies on maintaining "),
             eq("w = \\sum_i \\alpha_i y_i x_i"),
             rt(" explicitly. Each coordinate update is "),
             eq("O(d)"),
             rt(". If a kernel were used, computing "),
             eq("K(x_i, x_j)"),
             rt(" inside the loop would cost "),
             eq("O(n)"),
             rt(" per step (need to sum over all training points), destroying the linear-time guarantee. The kernel trick's appeal — avoiding explicit feature maps — requires materializing or caching "),
             eq("K_{ij}"),
             rt(", which is "),
             eq("O(n^2)"),
             rt(" memory.")),
    ]),
    toggle([rt("Q3 (Medium) — Explain the SMO update step. Why is η = K_ii + K_jj − 2K_ij the correct denominator?", bold=True)], [
        para(rt("Fixing all "),
             eq("\\alpha"),
             rt(" except "),
             eq("(\\alpha_i, \\alpha_j)"),
             rt(", the equality constraint "),
             eq("\\alpha_i y_i + \\alpha_j y_j = \\text{const}"),
             rt(" lets us express "),
             eq("\\alpha_i"),
             rt(" as a function of "),
             eq("\\alpha_j"),
             rt(". The sub-problem becomes maximizing a 1-D quadratic in "),
             eq("\\alpha_j"),
             rt(":")),
        equation_block(r"\max_{\alpha_j}\; c_1 \alpha_j - \frac{\eta}{2}\alpha_j^2, \quad c_1 = E_i y_j - E_j y_j"),
        para(rt("The coefficient of "),
             eq("-\\frac{1}{2}\\alpha_j^2"),
             rt(" is "),
             eq("Q_{jj} + Q_{ii} - 2Q_{ij} = y_j^2 K_{jj} + y_i^2 K_{ii} - 2y_iy_jK_{ij}"),
             rt(". Since "),
             eq("y_i^2 = y_j^2 = 1"),
             rt(", this simplifies to "),
             eq("\\eta = K_{ii} + K_{jj} - 2K_{ij}"),
             rt(". By Mercer's theorem "),
             eq("\\eta \\ge 0"),
             rt("; the quadratic is concave with unique maximum.")),
    ]),
    toggle([rt("Q4 (Medium) — When would you use kernel approximations instead of libSVM?", bold=True)], [
        para(rt("When "),
             eq("n > 100{,}000"),
             rt(" but a non-linear boundary is needed. Approaches:")),
        bullet(rt("Random Fourier Features (RFF / Bochner's theorem): approximate "),
               eq("k(x,x') \\approx z(x)^\\top z(x')"),
               rt(" with "),
               eq("D"),
               rt(" random features, then use LinearSVC on "),
               eq("z(x)"),
               rt(". Cost: "),
               eq("O(n D d)"),
               rt(" with "),
               eq("D \\approx 1000"),
               rt(".")),
        bullet(rt("Nyström method: subsample "),
               eq("m \\ll n"),
               rt(" landmark points, approximate kernel with "),
               eq("K \\approx K_{nm} K_{mm}^{-1} K_{mn}"),
               rt(".")),
        para(rt("sklearn: "),
             rt("RBFSampler", code=True),
             rt(" (RFF) and "),
             rt("Nystroem", code=True),
             rt(" transformers, then pipe into LinearSVC.")),
    ]),
    toggle([rt("Q5 (Hard) — What is the time complexity of libSVM and why? What determines the constant factor?", bold=True)], [
        para(rt("libSVM's per-iteration cost is "),
             eq("O(n_{sv} \\cdot d)"),
             rt(" for computing "),
             eq("f(x_i)"),
             rt(" (dot-product over support vectors plus kernel cache). The number of iterations to convergence is empirically "),
             eq("O(n^2)"),
             rt(" in the worst case (theoretical bound from Joachims 1999 analysis of SVM^light), giving "),
             eq("O(n^2 \\cdot d)"),
             rt(" total. The constant factors depend on:")),
        bullet(rt("Kernel cache hit rate: better cache → fewer kernel recomputations → faster")),
        bullet(rt("Number of support vectors: if "),
               eq("n_{sv} \\ll n"),
               rt(", each f(x) evaluation is cheap")),
        bullet(rt("Data separability: nearly-separable data → fewer SMO iterations")),
        bullet(rt("C value: large C → many support vectors → slow")),
        para(rt("For Researcher audience: the convergence is "),
             rt("sublinear (O(1/k) or worse) in general", italic=True),
             rt(" — SMO does not have a formal rate guarantee like CD does for strongly convex objectives. LIBLINEAR's coordinate descent on strongly convex duals has "),
             rt("R-linear (geometric) convergence", italic=True),
             rt(" — exponentially faster asymptotically.")),
    ]),
    toggle([rt("Q6 (Hard) — Explain the box constraint clipping in SMO. What happens when L = H?", bold=True)], [
        para(rt("After the unconstrained update "),
             eq("\\alpha_j^* = \\alpha_j + y_j(E_i-E_j)/\\eta"),
             rt(", we must enforce "),
             eq("0 \\le \\alpha_j \\le C"),
             rt(" AND "),
             eq("\\alpha_i y_i + \\alpha_j y_j = \\kappa"),
             rt(" (equality constraint). Together these define "),
             eq("[L, H]"),
             rt(". When "),
             eq("L = H"),
             rt(", the feasible segment is a single point — "),
             eq("\\alpha_j"),
             rt(" is already optimal for this working set (no improvement possible). libSVM skips this pair and picks a new working set. This happens when the two chosen "),
             eq("\\alpha"),
             rt(" are both on the same boundary of the box.")),
    ]),
    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(4,
        table_row(["Dimension", "libSVM (SVC)", "LIBLINEAR (LinearSVC)", "When to prefer"]),
        table_row(["Kernel", "Any Mercer kernel", "Linear only", "Non-linear → libSVM"]),
        table_row(["Time", "O(n²–n³)", "O(n·d)", "n>100k → LIBLINEAR"]),
        table_row(["Memory", "O(n·cache)", "O(d)", "Large n → LIBLINEAR"]),
        table_row(["Probability", "Built-in Platt", "External calibration", "Probs needed → SVC"]),
        table_row(["Sparse data", "Supported", "Natively efficient", "Text/NLP → LIBLINEAR"]),
        table_row(["Multi-class", "OVO or OVR", "OVR only", "Many classes → LinearSVC"]),
        table_row(["Convergence guarantee", "Heuristic (MVP)", "R-linear (strongly convex)", "Theory → LIBLINEAR"]),
    ),
    callout("🎯",
            rt("Decision: ", bold=True),
            rt("n < 10k + non-linear → SVC(kernel='rbf'). "
               "n > 100k + text/sparse → LinearSVC. "
               "n > 100k + non-linear → RBFSampler + LinearSVC, or XGBoost. "
               "Never SVC(kernel='linear') on large data — use LinearSVC instead.")),
    heading3("Advantages of libSVM"),
    bullet(rt("Handles non-linear boundaries via kernel trick")),
    bullet(rt("Built-in multi-class (OVO) and probability calibration")),
    bullet(rt("Gold-standard for small–medium kernel SVM tasks")),
    heading3("Disadvantages of libSVM"),
    bullet(eq("O(n^2)"), rt(" – "), eq("O(n^3)"), rt(" training makes n > 100k impractical")),
    bullet(rt("Quadratic kernel cache memory")),
    bullet(rt("No convergence rate guarantee")),
    heading3("Advantages of LIBLINEAR"),
    bullet(eq("O(n \\cdot d)"), rt(" training — scales to millions")),
    bullet(rt("R-linear convergence guarantee")),
    bullet(rt("Memory-efficient: only stores "), eq("w \\in \\mathbb{R}^d")),
    heading3("Disadvantages of LIBLINEAR"),
    bullet(rt("Linear kernel only — cannot capture non-linear patterns")),
    bullet(rt("No built-in probability output")),
    bullet(rt("May need more tuning (max_iter, dual vs primal) to converge")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/svm_solvers_libsvm_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Hard-margin SVM: maximum margin hyperplane, support vectors")),
    bullet(rt("Soft-margin SVM: slack variables, C parameter, hinge loss")),
    bullet(rt("Dual formulation & quadratic programming")),
    bullet(rt("Kernel trick: Mercer's theorem, positive semi-definiteness")),
    heading3("What to Learn Next"),
    bullet(rt("Kernel properties & Mercer's theorem")),
    bullet(rt("Multi-class SVM (OVO, OVR)")),
    bullet(rt("SVR (Support Vector Regression)")),
    bullet(rt("Random Fourier Features (Nyström, RFF) — kernel approximations")),
    heading3("Key Papers"),
    bullet(rt("Platt (1998) — ", bold=True), rt("'Sequential Minimal Optimization: A Fast Algorithm for Training Support Vector Machines.' Microsoft Research TR. Introduced SMO.")),
    bullet(rt("Chang & Lin (2011) — ", bold=True), rt("'LIBSVM: A library for support vector machines.' ACM TIST 2(3). ~60k citations, describes the full libSVM implementation.")),
    bullet(rt("Fan, Chang, Hsieh, Wang, Lin (2008) — ", bold=True), rt("'LIBLINEAR: A library for large linear classification.' JMLR 9. Introduced coordinate descent for linear SVMs.")),
    bullet(rt("Joachims (1999) — ", bold=True), rt("'Making large-scale SVM learning practical.' Advances in Kernel Methods. SVM^light, theoretical analysis of chunking/SMO complexity.")),
    bullet(rt("Hsieh et al. (2008) — ", bold=True), rt("'A dual coordinate descent method for large-scale linear SVM.' ICML 2008. Theoretical basis for LIBLINEAR's CD convergence.")),
    heading3("Best Resources"),
    bullet(rt("libSVM documentation: https://www.csie.ntu.edu.tw/~cjlin/libsvm/")),
    bullet(rt("LIBLINEAR documentation: https://www.csie.ntu.edu.tw/~cjlin/liblinear/")),
    bullet(rt("sklearn SVM User Guide: https://scikit-learn.org/stable/modules/svm.html")),
    bullet(rt("Bottou & Lin (2007) — 'Support vector machine solvers' — comprehensive solver survey")),
    callout("🔗",
            rt("This topic connects to: ", bold=True),
            rt("Hard-margin SVM, Soft-margin SVM, Kernel trick (Mercer's theorem), Dual formulation & QP, SVR, Multi-class SVM, Random Fourier Features, Logistic regression (LIBLINEAR also solves LR).")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
