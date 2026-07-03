#!/usr/bin/env python3
"""Update Notion page for: Computational complexity: O(n²) to O(n³) training (SVM)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8135-939b-dc5b5a83c40e"
ICON = "🟠"  # Advanced
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/svm_computational_complexity_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [

    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),

    heading3("What is this?"),
    para(rt("A kernel Support Vector Machine must compare every training example with every other example — producing an "), eq(r"n \times n"), rt(" matrix of similarity scores called the "), rt("Gram matrix", bold=True), rt(". This single data structure costs "), eq(r"O(n^2)"), rt(" memory and makes training cost "), eq(r"O(n^2)"), rt(" to "), eq(r"O(n^3)"), rt(" in time — the root cause of why SVMs stop working at large scale.")),

    heading3("Real-World Analogy"),
    para(rt("Imagine a round-robin tournament: every team (data point) must play every other team (kernel evaluation) before you can rank them (train the SVM). Doubling the teams quadruples the matches. At 10,000 teams, you have 100 million matches just to fill the bracket — before the actual ranking even begins.")),

    heading3("One-Sentence Summary"),
    para(rt("Kernel SVM's "), eq(r"n \times n"), rt(" Gram matrix is its superpower and its Achilles heel — exact nonlinear decision boundaries but quadratic memory and cubic worst-case training that caps practical use at ~50,000 samples.")),

    callout("💡", rt("If you remember one thing: ", bold=True), rt("Kernel SVM needs "), eq(r"O(n^2)"), rt(" memory (the Gram matrix) and "), eq(r"O(n^2)"), rt("–"), eq(r"O(n^3)"), rt(" training (QP solve). For large "), eq(r"n"), rt(", use Linear SVM, SGD, or kernel approximations (RFF, Nyström).")),

    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),

    heading3("The Problem"),
    para(rt("When Cortes & Vapnik (1995) introduced SVMs, datasets had hundreds to thousands of samples. The quadratic complexity was acceptable. But as the internet produced millions of training examples and practitioners found that kernel tricks gave excellent accuracy, scalability became the key limitation of the method.")),

    heading3("What Came Before"),
    para(rt("Perceptrons (Rosenblatt, 1958) were linear and fast but incapable of nonlinear problems. Kernel methods (Aizerman et al., 1964) could handle nonlinear boundaries, but the computational cost question was poorly understood until SVMs made kernel methods popular.")),

    heading3("Key Papers"),
    bullet(rt("Cortes & Vapnik (1995) — 'Support-Vector Networks', Machine Learning. Introduced soft-margin SVM with kernels.")),
    bullet(rt("Platt (1998) — 'Sequential Minimal Optimization: A Fast Algorithm for Training SVMs'. Reduced the QP solve from "), eq(r"O(n^3)"), rt(" to "), eq(r"O(n^2)"), rt(" per pass using 2-variable sub-problems.")),
    bullet(rt("Fan et al. (2008) — 'LIBLINEAR: A Library for Large Linear Classification'. Showed "), eq(r"O(nd)"), rt(" primal solves for linear SVMs, reaching millions of samples.")),
    bullet(rt("Rahimi & Recht (2007) — 'Random Features for Large-Scale Kernel Machines' (NeurIPS). Showed kernels can be approximated with explicit "), eq(r"D"), rt("-dimensional feature maps, enabling "), eq(r"O(nD)"), rt(" training.")),

    heading3("Evolution Timeline"),
    para(rt("Hard-margin SVM (1963 Aizerman, 1992 Boser) → Soft-margin + kernel SVM (Cortes & Vapnik 1995) → SMO for faster QP (Platt 1998) → LIBLINEAR for linear at scale (2008) → Random Fourier Features / Nyström for approximate kernels (2007–2012) → Neural networks replace SVMs for very large n (2012+)")),

    heading3("Before vs After — Scalability"),
    table(4,
        table_row(["Dimension", "Generic QP (Before SMO)", "SMO (libsvm)", "LIBLINEAR / SGD"]),
        table_row(["Training complexity", "O(n³)", "O(n²) amortised", "O(nd) per epoch"]),
        table_row(["Memory", "O(n²) Gram matrix", "O(n²) Gram matrix", "O(d) — no Gram"]),
        table_row(["Practical n limit", "~1,000", "~50,000", "Millions"]),
        table_row(["Nonlinear boundaries", "Yes (kernel)", "Yes (kernel)", "No (linear only)"]),
        table_row(["GPU-friendly", "No", "No", "Yes"]),
    ),

    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),

    heading3("Key Definitions"),
    bullet(rt("Kernel function: ", bold=True), eq(r"k(\mathbf{x}_i, \mathbf{x}_j) = \langle \phi(\mathbf{x}_i), \phi(\mathbf{x}_j) \rangle_\mathcal{H}"), rt(" — implicitly computes inner products in a (possibly infinite-dimensional) feature space "), eq(r"\mathcal{H}"), rt(".")),
    bullet(rt("Gram matrix: ", bold=True), eq(r"\mathbf{K} \in \mathbb{R}^{n \times n}"), rt(", where "), eq(r"K_{ij} = k(\mathbf{x}_i, \mathbf{x}_j)"), rt(". Must be positive semi-definite (Mercer's theorem).")),
    bullet(rt("Support vectors: ", bold=True), rt("Training points with "), eq(r"\alpha_i > 0"), rt(" — only these contribute to the decision boundary. Denoted "), eq(r"n_\text{SV} \le n"), rt(".")),
    bullet(rt("Dual variables: ", bold=True), eq(r"\alpha_1, \ldots, \alpha_n \ge 0"), rt(" — the "), eq(r"n"), rt(" unknowns of the dual QP. This is why complexity scales with "), eq(r"n"), rt(".")),

    callout("🔑", rt("Core property: ", bold=True), rt("The decision function "), eq(r"f(\mathbf{x}) = \sum_{i \in \text{SV}} \alpha_i y_i k(\mathbf{x}_i, \mathbf{x}) + b"), rt(" depends on training data only through kernel evaluations — the kernel trick. But building all "), eq(r"n^2"), rt(" kernel values is unavoidable in the exact dual formulation.")),

    heading3("Prerequisites to understand this topic"),
    bullet(rt("Dual formulation of SVM (Lagrangian duality, KKT conditions)")),
    bullet(rt("Kernel trick and Mercer's theorem")),
    bullet(rt("Quadratic programming basics")),
    bullet(rt("Big-O notation and asymptotic analysis")),

    divider(),

    # ── Section 4: Architecture & Internal Workings ────────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD-Level)"),

    heading3("Step 1 — Compute the Gram Matrix"),
    para(rt("Given "), eq(r"n"), rt(" samples "), eq(r"\{\mathbf{x}_i\}_{i=1}^n"), rt(" with "), eq(r"\mathbf{x}_i \in \mathbb{R}^d"), rt(", build:")),
    equation_block(r"\mathbf{K} \in \mathbb{R}^{n \times n}, \quad K_{ij} = k(\mathbf{x}_i, \mathbf{x}_j)"),
    para(rt("For the RBF kernel: "), eq(r"k(\mathbf{x}_i, \mathbf{x}_j) = \exp\!\left(-\frac{\|\mathbf{x}_i - \mathbf{x}_j\|^2}{2\sigma^2}\right)"), rt(". Each evaluation costs "), eq(r"O(d)"), rt(". Total evaluations: "), eq(r"\frac{n(n-1)}{2}"), rt(" (symmetric). Total compute: "), eq(r"O(n^2 d)"), rt(". Total memory: "), eq(r"O(n^2)"), rt(" floats = "), eq(r"4n^2"), rt(" bytes (float32).")),

    heading3("Numerical Example: Memory at Various n"),
    bullet(rt("n = 100: "), eq(r"100^2 \times 4"), rt(" bytes = 40 KB ✓ trivial")),
    bullet(rt("n = 1,000: "), eq(r"1000^2 \times 4"), rt(" bytes = 4 MB ✓ fine")),
    bullet(rt("n = 10,000: "), eq(r"10000^2 \times 4"), rt(" bytes = 400 MB — tight for RAM")),
    bullet(rt("n = 50,000: "), eq(r"50000^2 \times 4"), rt(" bytes = 10 GB — exceeds typical RAM")),
    bullet(rt("n = 100,000: "), eq(r"100000^2 \times 4"), rt(" bytes = 40 GB — completely impractical")),

    heading3("Step 2 — Solve the Dual QP"),
    para(rt("The dual objective (after substituting the kernel):")),
    equation_block(r"\max_{\boldsymbol{\alpha}} \sum_{i=1}^n \alpha_i - \frac{1}{2}\sum_{i=1}^n\sum_{j=1}^n \alpha_i \alpha_j y_i y_j K_{ij}"),
    para(rt("Subject to: "), eq(r"0 \le \alpha_i \le C"), rt(" for all "), eq(r"i"), rt(", and "), eq(r"\sum_{i=1}^n \alpha_i y_i = 0"), rt(".")),
    para(rt("This is a QP in "), eq(r"n"), rt(" variables. Generic interior-point methods: "), eq(r"O(n^3)"), rt(". SMO decomposes into 2-variable sub-problems solvable analytically — each iteration is "), eq(r"O(n)"), rt(" (one row of "), eq(r"\mathbf{K}"), rt("). Total iterations empirically: "), eq(r"O(n)"), rt(" to "), eq(r"O(n^2)"), rt(", giving "), eq(r"O(n^2)"), rt(" to "), eq(r"O(n^3)"), rt(" overall.")),

    heading3("Step 3 — Extract the Model"),
    para(rt("After solving, identify support vectors: "), eq(r"\{i : \alpha_i > 0\}"), rt(". Compute bias:")),
    equation_block(r"b = y_j - \sum_{i \in \text{SV}} \alpha_i y_i K_{ij} \quad \text{for any } j \text{ with } 0 < \alpha_j < C"),

    heading3("Step 4 — Prediction"),
    equation_block(r"f(\mathbf{x}) = \text{sign}\!\left(\sum_{i \in \text{SV}} \alpha_i y_i k(\mathbf{x}_i, \mathbf{x}) + b\right)"),
    para(rt("Prediction cost: "), eq(r"O(n_\text{SV} \cdot d)"), rt(" per new sample. In degenerate cases "), eq(r"n_\text{SV} \to n"), rt(", prediction also becomes slow.")),

    heading3("Design Decision: Why Not Primal?"),
    para(rt("The primal SVM involves "), eq(r"d"), rt(" variables (weight vector "), eq(r"\mathbf{w} \in \mathbb{R}^d"), rt("). When "), eq(r"d \gg n"), rt(" (high-dimensional feature space from kernel), the dual with "), eq(r"n"), rt(" variables is smaller. But when "), eq(r"d \le n"), rt(" (linear case), the primal is preferable — this is exactly what LIBLINEAR does.")),

    callout("⚙️", rt("Edge case: ", bold=True), rt("With large "), eq(r"C"), rt(" (low regularization), almost all points become support vectors ("), eq(r"n_\text{SV} \approx n"), rt("). This makes prediction slow and hints the model is overfitting. Reduce "), eq(r"C"), rt(" or use a different model.")),

    divider(),

    # ── Section 5: The Math ────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),

    heading3("Full Dual Derivation"),
    para(rt("Start from the primal soft-margin SVM:")),
    equation_block(r"\min_{\mathbf{w},b,\boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^n \xi_i \quad \text{s.t. } y_i(\mathbf{w}^\top\phi(\mathbf{x}_i)+b) \ge 1-\xi_i,\ \xi_i \ge 0"),
    para(rt("Introduce dual variables "), eq(r"\alpha_i \ge 0"), rt(" (for margin constraints) and "), eq(r"\mu_i \ge 0"), rt(" (for "), eq(r"\xi_i \ge 0"), rt("). The Lagrangian:")),
    equation_block(r"\mathcal{L} = \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_i\xi_i - \sum_i\alpha_i[y_i(\mathbf{w}^\top\phi(\mathbf{x}_i)+b)-1+\xi_i] - \sum_i\mu_i\xi_i"),
    para(rt("Setting stationarity conditions:")),
    equation_block(r"\frac{\partial\mathcal{L}}{\partial\mathbf{w}} = 0 \Rightarrow \mathbf{w} = \sum_i \alpha_i y_i \phi(\mathbf{x}_i)"),
    equation_block(r"\frac{\partial\mathcal{L}}{\partial b} = 0 \Rightarrow \sum_i \alpha_i y_i = 0"),
    equation_block(r"\frac{\partial\mathcal{L}}{\partial\xi_i} = 0 \Rightarrow \alpha_i + \mu_i = C \Rightarrow 0 \le \alpha_i \le C"),
    para(rt("Substituting "), eq(r"\mathbf{w}"), rt(" back and using "), eq(r"\langle\phi(\mathbf{x}_i),\phi(\mathbf{x}_j)\rangle = k(\mathbf{x}_i,\mathbf{x}_j)"), rt(":")),
    equation_block(r"\max_{\boldsymbol{\alpha}} \sum_{i=1}^n\alpha_i - \frac{1}{2}\sum_{i,j}\alpha_i\alpha_j y_i y_j k(\mathbf{x}_i,\mathbf{x}_j)"),
    para(rt("In matrix form (where "), eq(r"H_{ij} = y_i y_j K_{ij}"), rt("):")),
    equation_block(r"\max_{\boldsymbol{\alpha}} \mathbf{1}^\top\boldsymbol{\alpha} - \frac{1}{2}\boldsymbol{\alpha}^\top H\boldsymbol{\alpha} \quad \text{s.t. } 0 \le \boldsymbol{\alpha} \le C,\ \mathbf{y}^\top\boldsymbol{\alpha}=0"),
    para(rt("This is where "), eq(r"n^2"), rt(" appears: "), eq(r"\boldsymbol{\alpha}^\top H\boldsymbol{\alpha}"), rt(" requires forming/accessing the "), eq(r"n \times n"), rt(" matrix "), eq(r"H"), rt(" (the kernel Gram matrix times "), eq(r"y_i y_j"), rt(").")),

    heading3("SMO Complexity Analysis"),
    para(rt("SMO picks the pair "), eq(r"(\alpha_i, \alpha_j)"), rt(" that most violates the KKT conditions (via the Karush-Kuhn-Tucker check). The 2-variable sub-problem has an analytical solution:")),
    equation_block(r"\alpha_j^{new} = \alpha_j^{old} + \frac{y_j(E_i - E_j)}{\eta}, \quad \eta = 2K_{ij} - K_{ii} - K_{jj}"),
    para(rt("where "), eq(r"E_i = f(\mathbf{x}_i) - y_i"), rt(" is the prediction error. Each SMO step: "), eq(r"O(n)"), rt(" (computing "), eq(r"E_i"), rt(" requires evaluating "), eq(r"K_{ij}"), rt(" for all "), eq(r"j \in \text{SV}"), rt("). Number of steps: empirically "), eq(r"O(n)"), rt(" to "), eq(r"O(n^2)"), rt(". Total: "), eq(r"O(n^2)"), rt(" to "), eq(r"O(n^3)"), rt(".")),

    heading3("Random Fourier Features — Mathematical Justification"),
    para(rt("By Bochner's theorem: a continuous shift-invariant kernel "), eq(r"k(\mathbf{x}-\mathbf{x}')"), rt(" on "), eq(r"\mathbb{R}^d"), rt(" is positive definite if and only if "), eq(r"k"), rt(" is the Fourier transform of a non-negative measure "), eq(r"p(\boldsymbol{\omega})"), rt(":")),
    equation_block(r"k(\mathbf{x}-\mathbf{x}') = \int_{\mathbb{R}^d} p(\boldsymbol{\omega}) e^{j\boldsymbol{\omega}^\top(\mathbf{x}-\mathbf{x}')} d\boldsymbol{\omega} = \mathbb{E}_{\boldsymbol{\omega}}[e^{j\boldsymbol{\omega}^\top\mathbf{x}}\overline{e^{j\boldsymbol{\omega}^\top\mathbf{x}'}}]"),
    para(rt("For RBF: "), eq(r"k(\mathbf{x},\mathbf{x}') = e^{-\|\mathbf{x}-\mathbf{x}'\|^2/2\sigma^2}"), rt(", so "), eq(r"p(\boldsymbol{\omega}) = \mathcal{N}(\mathbf{0}, \sigma^{-2}\mathbf{I})"), rt(". Sample "), eq(r"D"), rt(" frequencies "), eq(r"\boldsymbol{\omega}_j \sim p(\boldsymbol{\omega})"), rt(", phases "), eq(r"b_j \sim \text{Uniform}[0,2\pi]"), rt(". The random feature map:")),
    equation_block(r"z_j(\mathbf{x}) = \sqrt{\frac{2}{D}}\cos(\boldsymbol{\omega}_j^\top\mathbf{x} + b_j)"),
    para(rt("By the law of large numbers: "), eq(r"\mathbf{z}(\mathbf{x})^\top\mathbf{z}(\mathbf{x}') \xrightarrow{D\to\infty} k(\mathbf{x},\mathbf{x}')"), rt(". Convergence: "), eq(r"\Pr[|\hat{k}-k| > \epsilon] \le 2\exp(-D\epsilon^2/4)"), rt(". With "), eq(r"D = O(\epsilon^{-2}\log(n/\delta))"), rt(", the approximation holds uniformly over all training pairs with probability "), eq(r"1-\delta"), rt(".")),

    callout("⚠️", rt("Warning: ", bold=True), eq(r"\eta = 2K_{ij} - K_{ii} - K_{jj}"), rt(" in SMO. If "), eq(r"\eta \ge 0"), rt(", the kernel matrix restricted to the pair is not positive definite — this happens with some non-Mercer kernels or numerical issues. SMO handles this by clipping. Always verify "), eq(r"K_{ii} > 0"), rt(" for your kernel.")),

    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),

    heading3("6a — From Scratch: Gram Matrix Construction & Complexity Demo"),
    code_block("python", """import numpy as np
import time

def rbf_kernel(X, gamma=1.0):
    \"\"\"Build the n×n Gram matrix for RBF kernel.

    Args:
        X: (n, d) data matrix
        gamma: RBF bandwidth parameter (k = exp(-gamma * ||xi - xj||²))
    Returns:
        K: (n, n) Gram matrix — O(n²) memory

    Complexity:
        Memory: O(n²) → 4n² bytes (float32)
        Compute: O(n² * d) but vectorized below as O(n² + nd)
    \"\"\"
    # Efficient: ||xi - xj||² = ||xi||² + ||xj||² - 2 xi·xj
    # This avoids explicit O(n² d) loop — uses BLAS matmul
    sq_dists = (np.sum(X**2, axis=1, keepdims=True)   # (n, 1)
                + np.sum(X**2, axis=1)                 # (n,) broadcasts to (n, n)
                - 2 * X @ X.T)                         # (n, n) — O(n² d) BLAS
    # Clamp numerical negatives to 0 (should be ~0 on diagonal)
    sq_dists = np.maximum(sq_dists, 0)
    return np.exp(-gamma * sq_dists)  # element-wise exp

# Empirical scaling demo
print(f"{'n':>8} | {'Memory (MB)':>12} | {'Build time (s)':>14}")
print("-" * 42)
for n in [100, 500, 1000, 2000, 5000]:
    X = np.random.randn(n, 50)
    mem_mb = (n * n * 4) / (1024**2)
    t0 = time.time()
    K = rbf_kernel(X, gamma=0.1)
    elapsed = time.time() - t0
    print(f"{n:>8} | {mem_mb:>12.2f} | {elapsed:>14.4f}")
    del K  # free immediately
# Output (approx):
#      100 |         0.04 |         0.0003
#      500 |         1.00 |         0.0012
#     1000 |         3.81 |         0.0048
#     2000 |        15.26 |         0.0190
#     5000 |        95.37 |         0.1200

def smo_minimal(K, y, C=1.0, tol=1e-3, max_passes=100):
    \"\"\"Minimal SMO implementation to demonstrate O(n²) inner loop.

    This is pedagogical — use libsvm/sklearn for production.
    K: (n, n) precomputed Gram matrix
    y: (n,) labels in {-1, +1}
    \"\"\"
    n = len(y)
    alpha = np.zeros(n)
    b = 0.0
    passes = 0

    while passes < max_passes:
        num_changed = 0
        for i in range(n):
            # Prediction error for sample i
            # This inner product is O(n) — the dominant cost
            Ei = (alpha * y) @ K[:, i] + b - y[i]

            if (y[i]*Ei < -tol and alpha[i] < C) or (y[i]*Ei > tol and alpha[i] > 0):
                # Pick j != i randomly (simplified heuristic)
                j = np.random.choice([k for k in range(n) if k != i])
                Ej = (alpha * y) @ K[:, j] + b - y[j]

                alpha_i_old, alpha_j_old = alpha[i], alpha[j]

                # Bounds for alpha_j
                if y[i] != y[j]:
                    L = max(0, alpha[j] - alpha[i]); H = min(C, C + alpha[j] - alpha[i])
                else:
                    L = max(0, alpha[i] + alpha[j] - C); H = min(C, alpha[i] + alpha[j])
                if L >= H: continue

                # Second-order step size: eta = 2K_ij - K_ii - K_jj
                eta = 2*K[i,j] - K[i,i] - K[j,j]
                if eta >= 0: continue  # Mercer violation safeguard

                # Update alpha_j
                alpha[j] -= y[j] * (Ei - Ej) / eta
                alpha[j] = np.clip(alpha[j], L, H)
                if abs(alpha[j] - alpha_j_old) < 1e-5: continue

                # Update alpha_i (from equality constraint sum(alpha*y) = 0)
                alpha[i] += y[i] * y[j] * (alpha_j_old - alpha[j])

                # Update bias b
                b1 = b - Ei - y[i]*(alpha[i]-alpha_i_old)*K[i,i] - y[j]*(alpha[j]-alpha_j_old)*K[i,j]
                b2 = b - Ej - y[i]*(alpha[i]-alpha_i_old)*K[i,j] - y[j]*(alpha[j]-alpha_j_old)*K[j,j]
                b = (b1 + b2) / 2  # average when neither SV is on boundary
                num_changed += 1

        passes = passes + 1 if num_changed == 0 else 0

    return alpha, b
"""),

    heading3("6b — Production: sklearn (Kernel SVM vs Linear SVM vs RFF)"),
    code_block("python", """from sklearn.svm import SVC, LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.kernel_approximation import RBFSampler, Nystroem
import numpy as np, time

# ── 1. Kernel SVM (exact, O(n²) memory, O(n²–n³) train) ──────────────────
clf_kernel = SVC(kernel='rbf', C=1.0, gamma='scale', cache_size=2000)
# cache_size=2000 means 2GB cache for K rows — helps SMO locality

# ── 2. Linear SVM (O(nd) train, no Gram matrix) ───────────────────────────
clf_linear = LinearSVC(C=1.0, max_iter=2000)
# Internally: LIBLINEAR dual coordinate descent for classification

# ── 3. RFF approximation (O(nD) train, approximate RBF) ──────────────────
clf_rff = Pipeline([
    ('rff', RBFSampler(gamma=0.1, n_components=2000, random_state=42)),
    ('svm', LinearSVC(C=1.0))
])
# n_components=D = 2000 random Fourier features
# Each feature: z_j(x) = sqrt(2/D) * cos(omega_j . x + b_j)

# ── 4. Nyström approximation (O(nm) feature map) ──────────────────────────
clf_nystrom = Pipeline([
    ('nystrom', Nystroem(kernel='rbf', gamma=0.1, n_components=500, random_state=42)),
    ('svm', LinearSVC(C=1.0))
])
# n_components=m=500 landmark points; feature map dim is also m

# Benchmark
n_sizes = [1000, 5000, 10000]
X_all = np.random.randn(max(n_sizes), 50)
y_all = np.sign(X_all[:, 0] + X_all[:, 1])

for n in n_sizes:
    X, y = X_all[:n], y_all[:n]
    print(f"\\nn = {n}")
    for name, clf in [("Kernel SVM", clf_kernel), ("LinearSVC", clf_linear),
                      ("RFF+LinSVC", clf_rff), ("Nystroem+LinSVC", clf_nystrom)]:
        t0 = time.time()
        try:
            clf.fit(X, y)
            acc = clf.score(X, y)
            print(f"  {name:20s}: {time.time()-t0:.3f}s, train acc={acc:.3f}")
        except Exception as e:
            print(f"  {name:20s}: {e}")

# ⚠️ Gotcha 1: SVC with kernel='rbf' silently runs out of RAM at n~100K
# ⚠️ Gotcha 2: SVC's cache_size is in MB — set it high (2000+) for SMO speed
# ⚠️ Gotcha 3: RBFSampler uses gamma differently from SVC (check sklearn docs)
# ⚠️ Gotcha 4: LinearSVC has max_iter — increase if convergence warnings appear
# ⚠️ Gotcha 5: SGDClassifier(loss='hinge') = online SVM, fastest for huge n:
from sklearn.linear_model import SGDClassifier
clf_sgd = SGDClassifier(loss='hinge', alpha=1e-4, max_iter=1000)
# alpha = lambda (regularization), loss='hinge' = soft-margin SVM primal
"""),

    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎯 Interview Deep-Dive"),

    toggle([rt("Q1 (Easy): Why does kernel SVM not scale to large datasets?", bold=True)], [
        para(rt("The dual formulation requires evaluating "), eq(r"k(\mathbf{x}_i, \mathbf{x}_j)"), rt(" for all "), eq(r"\binom{n}{2}"), rt(" pairs, producing an "), eq(r"n \times n"), rt(" Gram matrix. This costs "), eq(r"O(n^2)"), rt(" memory — for "), eq(r"n = 100{,}000"), rt(", that's 40GB in float32. The QP solve over this matrix adds "), eq(r"O(n^2)"), rt("–"), eq(r"O(n^3)"), rt(" training time. Both are hard limits that cannot be parallelized away without approximation.")),
    ]),

    toggle([rt("Q2 (Easy): What is the Gram matrix and why must it be n×n?", bold=True)], [
        para(rt("The Gram matrix "), eq(r"\mathbf{K}"), rt(" encodes all pairwise similarities: "), eq(r"K_{ij} = k(\mathbf{x}_i, \mathbf{x}_j)"), rt(". The dual SVM objective is quadratic in "), eq(r"\boldsymbol{\alpha}"), rt(" with "), eq(r"\mathbf{K}"), rt(" as the coefficient matrix. Since you have "), eq(r"n"), rt(" dual variables and their interactions matter, the matrix must be "), eq(r"n \times n"), rt(". You cannot reduce this without changing the optimization problem.")),
    ]),

    toggle([rt("Q3 (Medium): How does SMO reduce O(n³) to O(n²)? What's the core insight?", bold=True)], [
        para(rt("SMO (Platt, 1998) solves the simplest possible sub-problem: optimize over just 2 variables "), eq(r"(\alpha_i, \alpha_j)"), rt(" at a time while holding the rest fixed. The 2-variable QP subject to "), eq(r"\alpha_i y_i + \alpha_j y_j = \text{const}"), rt(" has a closed-form solution — no iterative solver needed. This replaces an "), eq(r"n \times n"), rt(" linear system solve with an "), eq(r"O(1)"), rt(" formula per step. The kernel evaluations per step are "), eq(r"O(n)"), rt(" (to find the most violated constraint), and the number of outer iterations is typically "), eq(r"O(n)"), rt(" to "), eq(r"O(n^2)"), rt(", giving total "), eq(r"O(n^2)"), rt(" to "), eq(r"O(n^3)"), rt(".")),
    ]),

    toggle([rt("Q4 (Medium): What is the Random Fourier Features trick and how does it change the complexity?", bold=True)], [
        para(rt("By Bochner's theorem, any shift-invariant kernel equals the expectation of a product of random features: "), eq(r"k(\mathbf{x},\mathbf{x}') = \mathbb{E}_\omega[z_\omega(\mathbf{x}) z_\omega(\mathbf{x}')]"), rt(" where "), eq(r"z_\omega(\mathbf{x}) = e^{j\omega^\top\mathbf{x}}"), rt(". We approximate with "), eq(r"D"), rt(" samples: compute explicit "), eq(r"D"), rt("-dimensional feature vectors "), eq(r"\mathbf{z}(\mathbf{x}) \in \mathbb{R}^D"), rt(", then train a linear SVM. Memory drops from "), eq(r"O(n^2)"), rt(" to "), eq(r"O(nD)"), rt(". Training drops from "), eq(r"O(n^2)"), rt("–"), eq(r"O(n^3)"), rt(" to "), eq(r"O(nD)"), rt(" per epoch. With "), eq(r"D = 2{,}000"), rt(", this is often 100× faster than kernel SVM with <1% accuracy loss.")),
    ]),

    toggle([rt("Q5 (Hard): Walk me through the full complexity analysis of kernel SVM — memory, training, and prediction.", bold=True)], [
        para(rt("Memory: "), eq(r"O(n^2)"), rt(" — the Gram matrix "), eq(r"\mathbf{K} \in \mathbb{R}^{n \times n}"), rt(" must be stored. Even SMO which caches working sets still has "), eq(r"O(n^2)"), rt(" total kernel evaluations.")),
        para(rt("Training: Building "), eq(r"\mathbf{K}"), rt(" costs "), eq(r"O(n^2 d)"), rt(". The QP solve over "), eq(r"n"), rt(" variables: generic interior-point "), eq(r"O(n^3)"), rt("; SMO "), eq(r"O(n^2)"), rt(" amortized (each step "), eq(r"O(n)"), rt(", empirically "), eq(r"O(n)"), rt("–"), eq(r"O(n^2)"), rt(" steps).")),
        para(rt("Prediction: "), eq(r"O(n_\text{SV} \cdot d)"), rt(" per query. "), eq(r"n_\text{SV}"), rt(" scales with "), eq(r"n"), rt(" — with large "), eq(r"C"), rt(" and non-separable data, "), eq(r"n_\text{SV} \approx n"), rt(", so prediction is also "), eq(r"O(nd)"), rt(".")),
        para(rt("The memory wall is the harder constraint: even if training were instant, storing "), eq(r"\mathbf{K}"), rt(" for "), eq(r"n = 10^5"), rt(" requires 40GB RAM.")),
    ]),

    toggle([rt("Q6 (Hard): Compare the Nyström method and RFF — when would you choose each?", bold=True)], [
        para(rt("RFF (Random Fourier Features): Approximates shift-invariant kernels (RBF, Laplace) using random spectral sampling. Embarrassingly parallel to compute. "), eq(r"D"), rt(" is a tunable accuracy knob. Does NOT require seeing training data to build the feature map — features are data-independent projections. Scales to streaming data.")),
        para(rt("Nyström: Approximates any PSD kernel (including string kernels) using landmark points sampled from training data. Feature map is data-dependent. Generally more accurate than RFF for same "), eq(r"D = m"), rt(" because it uses the actual data geometry. Requires "), eq(r"O(m^3)"), rt(" inversion. Better when the effective rank of "), eq(r"\mathbf{K}"), rt(" is small (low-dimensional manifold). Worse for truly high-dimensional kernels.")),
        para(rt("Rule: For RBF in practice, try RFF first — simpler. Use Nyström when RFF accuracy is insufficient or the kernel is not shift-invariant.")),
    ]),

    toggle([rt("Q7 (Expert, PhD Researcher): How does the kernel approximation error propagate into the SVM generalization bound?", bold=True)], [
        para(rt("Let "), eq(r"\hat{k}(\mathbf{x},\mathbf{x}') = \mathbf{z}(\mathbf{x})^\top\mathbf{z}(\mathbf{x}')"), rt(" be the RFF approximation. The approximation error is uniform: "), eq(r"\sup_{\mathbf{x},\mathbf{x}'} |k(\mathbf{x},\mathbf{x}') - \hat{k}(\mathbf{x},\mathbf{x}')| \le \epsilon"), rt(" w.p. "), eq(r"\ge 1-\delta"), rt(" with "), eq(r"D = O(\epsilon^{-2}\log(1/\delta))"), rt(".")),
        para(rt("The SVM objective evaluated on the approximate Gram matrix "), eq(r"\hat{\mathbf{K}}"), rt(" differs from the exact objective by "), eq(r"O(\epsilon \cdot \|\boldsymbol{\alpha}\|_1^2)"), rt(". Since "), eq(r"\|\boldsymbol{\alpha}\|_1 \le C \cdot n_\text{SV}"), rt(", the additional generalization error is "), eq(r"O(C \cdot n_\text{SV} \cdot \epsilon)"), rt(". For fixed "), eq(r"C"), rt(" and "), eq(r"\epsilon"), rt(", the bound holds uniformly — you lose "), eq(r"O(\epsilon)"), rt(" in SVM margin quality but gain exponential speedup in "), eq(r"D"), rt(" vs "), eq(r"n"), rt(".")),
    ]),

    callout("🚩", rt("Red flags in interviews: ", bold=True), rt("Saying kernel SVM is 'O(n)' or 'scalable'. Confusing the number of support vectors with the training complexity. Claiming RFF gives 'exact' kernel computation. Forgetting that kernel SVM prediction is "), eq(r"O(n_\text{SV} \cdot d)"), rt(", not "), eq(r"O(1)"), rt(".")),

    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),

    table(6,
        table_row(["Method", "Memory", "Train Time", "Max Practical n", "Non-linear?", "Best For"]),
        table_row(["Kernel SVM (RBF)", "O(n²)", "O(n²–n³)", "~50K", "Yes (exact)", "Small n, high accuracy"]),
        table_row(["Linear SVM (LIBLINEAR)", "O(nd)", "O(nd)/epoch", "Millions", "No", "Text, sparse high-d"]),
        table_row(["SGD + Hinge", "O(d)", "O(d)/update", "Billions (online)", "No (primal)", "Streaming, huge n"]),
        table_row(["RFF + LinearSVC", "O(nD)", "O(nD)/epoch", "Millions", "Approx", "Large n, RBF/shift-inv"]),
        table_row(["Nyström + LinearSVC", "O(nm)", "O(nm²)", "Millions", "Approx", "Any PSD kernel, low-rank K"]),
        table_row(["Gradient Boosting", "O(n)", "O(n log n)/tree", "Millions", "Yes", "Tabular, general purpose"]),
        table_row(["Neural Network", "O(params)", "O(nd·layers)/epoch", "Billions", "Yes", "Images, text, huge n"]),
    ),

    heading3("When to Use Kernel SVM"),
    bullet(rt("n < 10,000–50,000 samples")),
    bullet(rt("Features already meaningful (no need for complex feature learning)")),
    bullet(rt("Non-linear decision boundary clearly present")),
    bullet(rt("Margin maximization / generalization is top priority")),
    bullet(rt("Interpretability of support vectors is valuable")),

    heading3("When NOT to Use Kernel SVM"),
    bullet(rt("n > 50,000 (memory wall)")),
    bullet(rt("Prediction latency is critical (n_SV can be large)")),
    bullet(rt("Data is streaming or arriving online")),
    bullet(rt("Problem is image/speech/text where neural feature learning matters")),

    callout("🎯", rt("Decision: ", bold=True), rt("n < 10K + non-linear → Kernel SVM. n < 1M + linear boundary → LinearSVC. n > 10K + need non-linearity → RFF/Nyström + LinearSVC, gradient boosting, or neural network.")),

    divider(),

    # ── Section 9: Explainer Embed ─────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),

    divider(),

    # ── Section 10: Related Topics & Further Reading ────────────────────────────
    heading2("📚 Related Topics & Further Reading"),

    heading3("Prerequisites"),
    bullet(rt("Dual formulation & quadratic programming (KKT conditions, Lagrangian duality)")),
    bullet(rt("Kernel trick: polynomial kernel, RBF (Gaussian) kernel, sigmoid kernel, string kernels")),
    bullet(rt("Kernel properties: Mercer's theorem, positive semi-definiteness")),
    bullet(rt("Big-O notation, asymptotic analysis")),
    bullet(rt("Hard-margin SVM: maximum margin hyperplane, support vectors")),

    heading3("What to Learn Next"),
    bullet(rt("SMO algorithm in full detail (Platt 1998 paper)")),
    bullet(rt("Gaussian Processes — share the kernel + Gram matrix structure")),
    bullet(rt("Nyström method for low-rank matrix approximation")),
    bullet(rt("Random kitchen sinks (extensions of RFF)")),
    bullet(rt("Neural Tangent Kernel — why wide neural nets behave like kernel SVMs")),

    heading3("Key Papers"),
    bullet(rt("Cortes & Vapnik (1995) — Support-Vector Networks. Machine Learning 20(3):273–297. Introduced soft-margin SVM.")),
    bullet(rt("Platt (1998) — Sequential Minimal Optimization. Microsoft Research TR-98-14. O(n²) SMO solver.")),
    bullet(rt("Fan, Chang, Hsieh, Wang, Lin (2008) — LIBLINEAR. JMLR 9:1871–1874. O(nd) linear SVM.")),
    bullet(rt("Rahimi & Recht (2007) — Random Features for Large-Scale Kernel Machines. NeurIPS. RFF for kernel approximation.")),
    bullet(rt("Williams & Seeger (2001) — Using the Nyström Method to Speed Up Kernel Machines. NeurIPS. Low-rank Gram approximation.")),

    heading3("Best Resources"),
    bullet(rt("Schölkopf & Smola (2002) — Learning with Kernels. MIT Press. The definitive kernel methods textbook.")),
    bullet(rt("Bishop PRML Chapter 7 — SVMs with full dual derivation.")),
    bullet(rt("libsvm guide (https://www.csie.ntu.edu.tw/~cjlin/libsvm/) — practical parameter tuning.")),
    bullet(rt("Sklearn User Guide: Kernel Approximation — practical RFF/Nyström examples.")),

    callout("🔗", rt("This topic connects to: ", bold=True), rt("Dual formulation & QP · Kernel trick · Mercer's theorem · Gaussian Processes · Random Fourier Features · Nyström approximation · LIBLINEAR · Gradient Boosting (when SVM isn't practical)")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
