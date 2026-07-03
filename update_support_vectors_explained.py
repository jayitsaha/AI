#!/usr/bin/env python3
"""Update Notion page for: Support vectors — what they are and why they matter"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81b7-9c8e-fb7fe6ddf966"
ICON = "🟡"  # Intermediate
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/support_vectors_explained_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Imagine drawing a line between two groups of coloured dots. You want the line to have maximum breathing room from both sides — the widest possible corridor. The only dots that actually decide where the line goes are the ones sitting closest to it. Remove any other dot and the line doesn't budge. Those critical, line-defining dots are called "), rt("support vectors", bold=True), rt(".")),
    heading3("Real-World Analogy"),
    para(rt("Think of border negotiation between two countries. The exact border location is determined by the frontier towns on each side — move any inland town and the border doesn't change. Support vectors are those frontier towns. Every other training point is an irrelevant inland city.")),
    heading3("One-Sentence Summary"),
    para(rt("Support vectors are the training points with "), eq(r"\alpha_i > 0"), rt(" in the dual SVM; they are the only points that define "), eq(r"\mathbf{w}"), rt(" and "), eq(r"b"), rt(", and all other points contribute nothing.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("The SVM decision boundary is a sparse weighted sum of training points — only those with "), eq(r"\alpha_i > 0"), rt(" (on or inside the margin) count. This is enforced by the KKT complementary slackness condition.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("By the late 1980s, neural networks showed promise but had no theoretical guarantees on generalisation. How could one choose among the infinitely many hyperplanes that separate two classes? The choice of boundary directly determines robustness to unseen data.")),
    heading3("What Came Before"),
    para(rt("The "), rt("Perceptron", bold=True), rt(" (Rosenblatt, 1958) finds "), rt("any", italic=True), rt(" separating hyperplane — whichever the gradient descent happens to converge to. It has no preference for well-separated boundaries. On noisy or nearly-separable data this leads to brittle classifiers.")),
    heading3("The Breakthrough"),
    para(rt("Vapnik & Lerner (1963) and later Boser, Guyon & Vapnik (COLT 1992) formalised the "), rt("maximum-margin hyperplane", bold=True), rt(": among all separating planes, pick the one with the largest margin. This yields a unique solution, rooted in VC theory, with strong generalisation guarantees. The concept of support vectors is central: they "), rt("are", italic=True), rt(" the margin.")),
    heading3("Key Papers"),
    bullet(rt("Boser, Guyon, Vapnik — \"A Training Algorithm for Optimal Margin Classifiers\" — COLT 1992. Introduced the kernel trick and posed SVM as a QP.")),
    bullet(rt("Cortes & Vapnik — \"Support-Vector Networks\" — Machine Learning 1995. Extended to soft-margin (slack variables) and named the method.")),
    bullet(rt("Schölkopf & Smola — \"Learning with Kernels\" — MIT Press 2002. Comprehensive treatment including theoretical foundations.")),
    heading3("Evolution Timeline"),
    para(rt("Perceptron (1958) → Optimal margin hyperplane (1963) → Kernel SVM / support vectors (1992) → Soft-margin SVM (1995) → SMO solver (Platt 1998) → SVMs applied in NLP and bioinformatics (2000s) → Deep learning surpasses SVMs on images (2012), but SVMs remain strong for tabular / small data.")),
    table(
        4,
        table_row(["Dimension", "Perceptron (Before)", "Hard-Margin SVM", "Soft-Margin SVM"]),
        table_row(["Boundary selection", "Any separating plane", "Maximum-margin plane", "Maximum-margin with slack"]),
        table_row(["Uniqueness of solution", "Not unique", "Unique", "Unique (given C)"]),
        table_row(["Handles noise/overlap", "No (crashes)", "No (requires strict sep.)", "Yes (via slack ξᵢ)"]),
        table_row(["Generalisation theory", "Ad hoc", "VC-dimension bound", "Margin-based bound"]),
        table_row(["Sparsity", "Dense (all points used)", "Sparse (SVs only)", "Sparse (SVs only)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ──────────────────────────────────────
    heading2("🧱 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Hyperplane: ", bold=True), rt("the set "), eq(r"\{\mathbf{x} : \mathbf{w}^\top \mathbf{x} + b = 0\}"), rt(". Separates the two classes.")),
    bullet(rt("Margin: ", bold=True), rt("the perpendicular distance from the hyperplane to the nearest point of either class. For a normalised "), eq(r"\mathbf{w}"), rt(", margin = "), eq(r"\frac{2}{\|\mathbf{w}\|}")),
    bullet(rt("Support vectors: ", bold=True), rt("training points "), eq(r"\mathbf{x}_i"), rt(" satisfying "), eq(r"y_i(\mathbf{w}^\top \mathbf{x}_i + b) = 1"), rt(". Equivalently, points with dual variable "), eq(r"\alpha_i > 0"), rt(".")),
    bullet(rt("Dual variable αᵢ: ", bold=True), rt("Lagrange multiplier for the constraint on point "), eq(r"i"), rt(" in the dual QP. Its magnitude encodes how much point "), eq(r"i"), rt(" 'participates' in defining "), eq(r"\mathbf{w}"), rt(".")),
    heading3("Building Blocks"),
    para(rt("The SVM rests on three pillars:")),
    numbered(rt("Margin maximisation — geometric objective")),
    numbered(rt("Lagrangian duality — converts constrained primal to unconstrained dual")),
    numbered(rt("KKT conditions — enforce sparsity by zeroing out non-margin-touching αᵢ")),
    callout("🔑", rt("Core invariant: ", bold=True), rt("The optimal weight vector "), eq(r"\mathbf{w}^*"), rt(" lies in the span of the training data, but only in the span of the "), rt("support vectors", italic=True), rt(". Every other training point contributes a zero coefficient.")),
    heading3("Prerequisites Check"),
    para(rt("To fully understand this topic, you should know: constrained optimisation (Lagrangians), KKT conditions, inner products / dot products, binary classification fundamentals.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ────────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD-Level)"),
    heading3("Primal Formulation"),
    para(rt("The hard-margin SVM primal problem:")),
    equation_block(r"\min_{\mathbf{w}, b} \frac{1}{2}\|\mathbf{w}\|^2 \quad \text{subject to} \quad y_i(\mathbf{w}^\top \mathbf{x}_i + b) \geq 1 \quad \forall i = 1, \ldots, n"),
    para(rt("Geometric reading: "), eq(r"\frac{1}{2}\|\mathbf{w}\|^2"), rt(" is minimised to maximise margin "), eq(r"\frac{2}{\|\mathbf{w}\|}"), rt(". The constraint ensures every point is correctly classified at margin ≥ 1.")),
    heading3("Lagrangian & Dual Derivation"),
    para(rt("Introduce one non-negative multiplier "), eq(r"\alpha_i \geq 0"), rt(" per constraint:")),
    equation_block(r"\mathcal{L}(\mathbf{w}, b, \boldsymbol{\alpha}) = \frac{1}{2}\|\mathbf{w}\|^2 - \sum_{i=1}^n \alpha_i \bigl[y_i(\mathbf{w}^\top \mathbf{x}_i + b) - 1\bigr]"),
    para(rt("Setting "), eq(r"\nabla_\mathbf{w} \mathcal{L} = 0"), rt(" gives "), eq(r"\mathbf{w} = \sum_i \alpha_i y_i \mathbf{x}_i"), rt(". Setting "), eq(r"\partial \mathcal{L}/\partial b = 0"), rt(" gives "), eq(r"\sum_i \alpha_i y_i = 0"), rt(". Substituting back, the Lagrangian becomes the dual objective:")),
    equation_block(r"\max_{\boldsymbol{\alpha}} \sum_{i=1}^n \alpha_i - \frac{1}{2}\sum_{i=1}^n\sum_{j=1}^n \alpha_i \alpha_j y_i y_j \mathbf{x}_i^\top \mathbf{x}_j \quad \text{s.t.} \quad \alpha_i \geq 0,\; \sum_i \alpha_i y_i = 0"),
    heading3("KKT Complementary Slackness — The Source of Sparsity"),
    para(rt("At the optimum, the KKT conditions require:")),
    equation_block(r"\alpha_i \bigl[y_i(\mathbf{w}^\top \mathbf{x}_i + b) - 1\bigr] = 0 \quad \forall i"),
    para(rt("This product is zero iff at least one factor is zero. Two exhaustive cases:")),
    bullet(rt("Case A: "), eq(r"\alpha_i = 0"), rt(" — the constraint is strictly satisfied ("), eq(r"y_i(\mathbf{w}^\top \mathbf{x}_i + b) > 1"), rt("). The point is outside the margin, does NOT appear in "), eq(r"\mathbf{w}"), rt(".")),
    bullet(rt("Case B: "), eq(r"y_i(\mathbf{w}^\top \mathbf{x}_i + b) = 1"), rt(" — the point lies exactly on the margin boundary. Here "), eq(r"\alpha_i > 0"), rt(". This is a "), rt("support vector", bold=True), rt(".")),
    heading3("Numerical Trace (Concrete Example)"),
    para(rt("Let n = 4 points in "), eq(r"\mathbb{R}^2"), rt(":")),
    code_block("plain text",
        "Point 1: x1 = [2, 1],  y1 = +1\n"
        "Point 2: x2 = [3, 2],  y2 = +1\n"
        "Point 3: x3 = [-2, -1], y3 = -1\n"
        "Point 4: x4 = [-1, 0],  y4 = -1\n"
        "\n"
        "Optimal solution: w = [0.5, 0.0], b = -0.5\n"
        "  → Decision boundary: 0.5*x₁ - 0.5 = 0  ⟹  x₁ = 1\n"
        "  → Margin lines:       0.5*x₁ - 0.5 = ±1 ⟹  x₁ = 3  and  x₁ = -1\n"
        "\n"
        "Check each point:\n"
        "  x1=[2,1]:  y1*(0.5*2 + 0 - 0.5) = 1*(0.5) < 1  → NOT on margin → α1=0\n"
        "  x2=[3,2]:  y2*(0.5*3 + 0 - 0.5) = 1*(1.0) = 1  → ON margin  → α2>0 (SV!)\n"
        "  x3=[-2,-1]:y3*(0.5*(-2)+0-0.5) = (-1)*(-1.5) = 1.5 > 1 → NOT SV → α3=0\n"
        "  x4=[-1,0]: y4*(0.5*(-1)+0-0.5) = (-1)*(-1.0) = 1.0 = 1 → ON margin → α4>0 (SV!)\n"
        "\n"
        "Dual: α = [0, α2, 0, α4]\n"
        "w = α2*y2*x2 + α4*y4*x4 = α2*(+1)*[3,2] + α4*(-1)*[-1,0]\n"
        "Solving dual QP gives α2 = 0.5, α4 = 0.5\n"
        "w = 0.5*[3,2] + 0.5*[1,0] = [2, 1] (scaled version of [0.5, 0]; normalise separately)\n"
        "\n"
        "Points x1 and x3 are completely irrelevant to the model."
    ),
    heading3("Soft-Margin (C-SVM) — Three Types of Support Vectors"),
    para(rt("With slack variables "), eq(r"\xi_i \geq 0"), rt(", the primal becomes:")),
    equation_block(r"\min_{\mathbf{w}, b, \boldsymbol{\xi}} \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_i \xi_i \quad \text{s.t.} \quad y_i(\mathbf{w}^\top\mathbf{x}_i + b) \geq 1 - \xi_i,\; \xi_i \geq 0"),
    para(rt("Dual variables are now bounded: "), eq(r"0 \leq \alpha_i \leq C"), rt(". KKT conditions yield three types:")),
    bullet(rt("α = 0: non-SV, correctly outside margin")),
    bullet(rt("0 < α < C: free SV, sits exactly on margin (ξᵢ = 0)")),
    bullet(rt("α = C: bounded SV, inside margin or misclassified (ξᵢ > 0)")),
    heading3("Design Decision: Why Dual?"),
    callout("🤔", rt("Why solve the dual instead of the primal? ", bold=True), rt("(1) The dual depends on data only via inner products "), eq(r"\mathbf{x}_i^\top \mathbf{x}_j"), rt(", enabling the kernel trick without ever computing "), eq(r"\phi(\mathbf{x})"), rt(" explicitly. (2) The dual has "), eq(r"n"), rt(" variables vs "), eq(r"d+1"), rt(" in the primal — favourable when "), eq(r"d \gg n"), rt(". (3) Sparsity of the solution is immediately visible.")),
    divider(),

    # ── Section 5: The Math Behind It ─────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Margin Width Derivation"),
    para(rt("For a hyperplane "), eq(r"\mathbf{w}^\top \mathbf{x} + b = 0"), rt(", the signed distance from point "), eq(r"\mathbf{x}_i"), rt(" to the hyperplane is:")),
    equation_block(r"d_i = \frac{y_i(\mathbf{w}^\top \mathbf{x}_i + b)}{\|\mathbf{w}\|}"),
    para(rt("The margin is twice the minimum distance from the boundary to any point. With the canonical scaling "), eq(r"y_i(\mathbf{w}^\top \mathbf{x}_i + b) \geq 1"), rt(", the margin equals:")),
    equation_block(r"\gamma = \frac{2}{\|\mathbf{w}\|}"),
    para(rt("Maximising "), eq(r"\gamma"), rt(" is equivalent to minimising "), eq(r"\|\mathbf{w}\|^2"), rt(", which is the primal objective.")),
    heading3("Reconstruction of w"),
    equation_block(r"\mathbf{w}^* = \sum_{i=1}^{n} \alpha_i^* y_i \mathbf{x}_i = \sum_{i \in \mathcal{S}} \alpha_i^* y_i \mathbf{x}_i"),
    para(rt("where "), eq(r"\mathcal{S} = \{i : \alpha_i^* > 0\}"), rt(" is the support set. Note: "), eq(r"|\mathcal{S}| \ll n"), rt(" in practice.")),
    heading3("Bias Recovery"),
    para(rt("For any free support vector "), eq(r"s \in \mathcal{S}"), rt(" (with "), eq(r"0 < \alpha_s < C"), rt("):")),
    equation_block(r"b^* = y_s - \mathbf{w}^{*\top} \mathbf{x}_s = y_s - \sum_{i \in \mathcal{S}} \alpha_i^* y_i \mathbf{x}_i^\top \mathbf{x}_s"),
    para(rt("In practice, "), eq(r"b^*"), rt(" is averaged over all free SVs for numerical stability.")),
    heading3("Prediction"),
    equation_block(r"\hat{y}(\mathbf{x}) = \operatorname{sign}\!\left(\sum_{i \in \mathcal{S}} \alpha_i^* y_i \langle \mathbf{x}_i, \mathbf{x}\rangle + b^*\right)"),
    para(rt("With a kernel "), eq(r"K(\mathbf{x}_i, \mathbf{x}) = \phi(\mathbf{x}_i)^\top \phi(\mathbf{x})"), rt(":")),
    equation_block(r"\hat{y}(\mathbf{x}) = \operatorname{sign}\!\left(\sum_{i \in \mathcal{S}} \alpha_i^* y_i K(\mathbf{x}_i, \mathbf{x}) + b^*\right)"),
    heading3("VC Dimension Bound (Generalisation)"),
    para(rt("The expected test error is bounded by:")),
    equation_block(r"\mathbb{E}[\text{test error}] \leq \frac{\mathbb{E}[|\mathcal{S}|]}{n-1}"),
    para(rt("(leave-one-out bound). Fewer support vectors → better generalisation. This is why SVMs favour solutions with small "), eq(r"|\mathcal{S}|"), rt(". The margin maximisation implicitly minimises the VC dimension.")),
    callout("⚠️", rt("Warning: ", bold=True), rt("The margin bound "), eq(r"\gamma = 2/\|\mathbf{w}\|"), rt(" is a "), rt("canonical", italic=True), rt(" margin under the constraint "), eq(r"\min_i y_i(\mathbf{w}^\top\mathbf{x}_i + b) = 1"), rt(". Without this normalisation, scaling "), eq(r"\mathbf{w}"), rt(" arbitrarily changes "), eq(r"\|\mathbf{w}\|"), rt(" but not the boundary. The QP implicitly enforces the normalisation via the constraints.")),
    divider(),

    # ── Section 6: Code Implementation ────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python",
        "import numpy as np\n"
        "from scipy.optimize import minimize\n"
        "\n"
        "def svm_fit(X, y, C=1e9):  # C large → hard margin\n"
        "    \"\"\"Solve the SVM dual QP and return alpha, w, b, support_mask.\"\"\"\n"
        "    n, d = X.shape\n"
        "\n"
        "    # Gram matrix (n x n): Q[i,j] = y_i * y_j * x_i . x_j\n"
        "    Q = (y[:, None] * X) @ (y[:, None] * X).T  # (n, n)\n"
        "\n"
        "    # Dual objective: maximise sum(alpha) - 0.5 * alpha^T Q alpha\n"
        "    # scipy minimises, so negate\n"
        "    def obj(a): return 0.5 * a @ Q @ a - np.sum(a)\n"
        "    def jac(a): return Q @ a - 1.0\n"
        "\n"
        "    # Constraints: sum(alpha_i * y_i) = 0\n"
        "    constraints = [{'type': 'eq', 'fun': lambda a: np.dot(a, y)}]\n"
        "    # Bounds: 0 <= alpha_i <= C\n"
        "    bounds = [(0, C)] * n\n"
        "\n"
        "    result = minimize(obj, np.zeros(n), jac=jac,\n"
        "                      method='SLSQP', bounds=bounds,\n"
        "                      constraints=constraints,\n"
        "                      options={'ftol': 1e-9, 'maxiter': 1000})\n"
        "    alpha = result.x\n"
        "\n"
        "    # Support vectors: alpha_i > threshold\n"
        "    tol = 1e-5\n"
        "    support_mask = alpha > tol  # boolean array\n"
        "    print(f'Support vectors: {support_mask.sum()} / {n} '  # sparsity!\n"
        "          f'({100*support_mask.mean():.1f}%)')\n"
        "\n"
        "    # Reconstruct w from support vectors only\n"
        "    w = (alpha * y) @ X  # shape (d,) — zero terms contribute nothing\n"
        "\n"
        "    # Recover b: average over free SVs (0 < alpha < C)\n"
        "    free_mask = support_mask & (alpha < C - tol)\n"
        "    if free_mask.any():\n"
        "        b = np.mean(y[free_mask] - X[free_mask] @ w)\n"
        "    else:\n"
        "        b = np.mean(y[support_mask] - X[support_mask] @ w)\n"
        "\n"
        "    return alpha, w, b, support_mask\n"
        "\n"
        "\n"
        "def svm_predict(X, w, b):\n"
        "    \"\"\"Predict labels using only w and b (support vectors already baked in).\"\"\"\n"
        "    return np.sign(X @ w + b)\n"
        "\n"
        "\n"
        "# Demo\n"
        "np.random.seed(42)\n"
        "X_pos = np.random.randn(30, 2) + [2, 0]\n"
        "X_neg = np.random.randn(30, 2) + [-2, 0]\n"
        "X = np.vstack([X_pos, X_neg])\n"
        "y = np.array([1]*30 + [-1]*30)\n"
        "\n"
        "alpha, w, b, sv_mask = svm_fit(X, y)\n"
        "# Typical output: 'Support vectors: 4 / 60 (6.7%)'\n"
        "# The 56 non-SVs are completely irrelevant to the boundary!\n"
        "\n"
        "preds = svm_predict(X, w, b)\n"
        "print(f'Train acc: {(preds == y).mean()*100:.1f}%')\n"
        "print(f'w = {w}')\n"
        "print(f'Alpha values: {alpha[sv_mask].round(4)}')"
    ),
    heading3("6b — Production Usage (scikit-learn)"),
    code_block("python",
        "from sklearn.svm import SVC\nimport numpy as np\n\n"
        "# Fit\nclf = SVC(\n    kernel='linear',   # or 'rbf', 'poly', 'sigmoid'\n    C=1.0,             # Regularisation: small C → more SVs, wider margin\n    # C=100 → fewer SVs, tries harder to separate exactly\n)\nclf.fit(X, y)\n\n"
        "# Inspect support vectors\nprint(f'Support vectors: {len(clf.support_)} / {len(X)} ({100*len(clf.support_)/len(X):.1f}%)')\nprint(f'Support vector indices: {clf.support_}')\nprint(f'Alpha values: {clf.dual_coef_}')  # shape (1, n_SVs) = alpha_i * y_i\nprint(f'w = {clf.coef_}')                   # Only available for linear kernel!\nprint(f'b = {clf.intercept_}')\n\n"
        "# Predict\npreds = clf.predict(X_test)\nscores = clf.decision_function(X_test)  # distance to boundary\n\n"
        "# ⚠️ Gotcha: clf.coef_ only exists for kernel='linear'\n# For RBF/poly, w doesn't exist in input space — use dual_coef_ instead\n# ⚠️ Gotcha: C has INVERSE effect vs regularisation lambda\n#   Small C = more regularisation (more SVs, wider margin)\n#   Large C = less regularisation (fewer SVs, narrower margin, tries to fit all points)\n# ⚠️ Gotcha: scaling matters! Always StandardScaler before SVC\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.pipeline import Pipeline\n\npipe = Pipeline([\n    ('scaler', StandardScaler()),\n    ('svm', SVC(kernel='rbf', C=10, gamma='scale'))\n])\npipe.fit(X_train, y_train)"
    ),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy): What is a support vector?"),
    para(rt("A support vector is a training point "), eq(r"\mathbf{x}_i"), rt(" that lies exactly on the margin boundary: "), eq(r"y_i(\mathbf{w}^\top\mathbf{x}_i + b) = 1"), rt(". Equivalently, it is any point with dual variable "), eq(r"\alpha_i > 0"), rt(" in the SVM solution. Support vectors are the only points that contribute to the weight vector "), eq(r"\mathbf{w} = \sum_i \alpha_i y_i \mathbf{x}_i"), rt("; all others have "), eq(r"\alpha_i = 0"), rt(".")),
    heading3("Q2 (Easy): What happens if you remove a non-support-vector point?"),
    para(rt("Nothing changes. Since its "), eq(r"\alpha_i = 0"), rt(", removing it doesn't alter "), eq(r"\mathbf{w}"), rt(" or "), eq(r"b"), rt(". The decision boundary is identical.")),
    callout("⚠️", rt("Follow-up trap: ", bold=True), rt("'But doesn't it affect the objective?' — Yes, in principle a non-SV at a different position could become a SV. But removing an existing non-SV (keeping its current position as a constraint) does not change the optimal solution.")),
    heading3("Q3 (Medium): Why does the SVM solution have sparsity?"),
    para(rt("From KKT complementary slackness: "), eq(r"\alpha_i[y_i(\mathbf{w}^\top\mathbf{x}_i+b)-1]=0"), rt(". A point either sits exactly on the margin (and may have "), eq(r"\alpha_i > 0"), rt("), or strictly satisfies the constraint (and must have "), eq(r"\alpha_i = 0"), rt("). In practice most points are far from the margin → most "), eq(r"\alpha_i = 0"), rt(" → sparse solution.")),
    heading3("Q4 (Medium): How do you recover the bias b?"),
    para(rt("Use a free support vector "), eq(r"s"), rt(" (with "), eq(r"0 < \alpha_s < C"), rt("): "), eq(r"b = y_s - \mathbf{w}^\top\mathbf{x}_s"), rt(". Average over all free SVs for stability. Bounded SVs ("), eq(r"\alpha_s = C"), rt(") violate the margin (ξ > 0) and cannot be used.")),
    heading3("Q5 (Hard): What is the effect of C on the number of support vectors?"),
    para(rt("Large C penalises slack heavily → the SVM tries to classify all points correctly → fewer SVs, potentially a narrow/overfit margin. Small C is more tolerant → more violations allowed → more SVs, wider margin, more regularisation. The fraction of SVs is an implicit measure of model complexity.")),
    heading3("Q6 (Hard): How does the kernel trick use support vectors?"),
    para(rt("The prediction function becomes "), eq(r"\hat{y}(\mathbf{x}) = \text{sign}(\sum_{i\in\mathcal{S}} \alpha_i y_i K(\mathbf{x}_i, \mathbf{x}) + b)"), rt(". The kernel "), eq(r"K(\mathbf{x}_i, \mathbf{x}) = \phi(\mathbf{x}_i)^\top\phi(\mathbf{x})"), rt(" is only ever evaluated at support vector positions. This is why sparsity is crucial for kernel SVMs: fewer SVs → fewer kernel evaluations at inference time.")),
    heading3("Q7 (Hard, Follow-up Trap): Can support vectors change if you add more data?"),
    para(rt("Yes. Adding a new training point can either: (a) fall outside the current margin (becomes a non-SV, no change), or (b) fall inside or on the margin, reshaping the boundary and changing which points are SVs. This is why online SVM updates are non-trivial (see: incremental/decremental SVM, Cauwenberghs & Poggio 2001).")),
    heading3("Two-Level Explanation"),
    toggle([rt("Explain to a PhD Researcher", bold=True)], [
        para(rt("The SVM dual is a strictly convex QP: "), eq(r"\max_\alpha \mathbf{1}^\top\alpha - \frac{1}{2}\alpha^\top Q\alpha"), rt(" s.t. "), eq(r"\alpha^\top\mathbf{y} = 0"), rt(", "), eq(r"\mathbf{0} \leq \alpha \leq C\mathbf{1}"), rt(", where "), eq(r"Q_{ij} = y_iy_j\langle\phi(\mathbf{x}_i),\phi(\mathbf{x}_j)\rangle"), rt(". Strong duality holds (Slater's condition satisfied). The optimal "), eq(r"\boldsymbol{\alpha}^*"), rt(" is unique by strict convexity. KKT stationarity yields "), eq(r"\mathbf{w}^* = \sum_i\alpha_i^*y_i\phi(\mathbf{x}_i)"), rt("; complementary slackness yields the support set "), eq(r"\mathcal{S}"), rt(". The VC-bound "), eq(r"\mathbb{E}[\text{err}] \leq \mathbb{E}[|\mathcal{S}|]/(n-1)"), rt(" provides margin-based generalisation (Vapnik 1998). The SMO algorithm (Platt 1998) exploits sparsity for "), eq(r"O(n|\mathcal{S}|)"), rt(" iteration cost.")),
    ]),
    toggle([rt("Explain to a Research Scientist/Engineer", bold=True)], [
        para(rt("SVMs solve a QP in the dual. The dual variables "), eq(r"\alpha_i"), rt(" play the role of learned 'importance weights' for each training point. By the KKT conditions, only the points on or inside the margin can have "), eq(r"\alpha_i > 0"), rt(" — these are the support vectors. The decision function is ")),
        para(eq(r"\hat{y}(\mathbf{x}) = \text{sign}(\sum_{i\in\mathcal{S}}\alpha_iy_iK(\mathbf{x}_i,\mathbf{x}) + b)")),
        para(rt("so inference only accesses the training set through the SVs. This means: (1) you can discard non-SVs after training, (2) C controls the trade-off between margin width and number of SVs, and (3) sklearn's clf.dual_coef_ = alpha_i * y_i for each SV.")),
    ]),
    heading3("Red Flags (Wrong Answers)"),
    bullet(rt("'Support vectors are the most difficult/ambiguous points' — False. They're just the nearest to the margin, even if well-separated.")),
    bullet(rt("'All training data is needed for prediction' — False. Only SVs are used.")),
    bullet(rt("'Removing a support vector doesn't change the boundary' — WRONG. Removing a SV changes the solution entirely.")),
    divider(),

    # ── Section 8: Comparisons & Trade-offs ──────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(
        5,
        table_row(["Dimension", "Hard-Margin SVM", "Soft-Margin SVM", "Logistic Regression", "Neural Networks"]),
        table_row(["Support vectors", "Points on margin", "Points on/inside margin", "N/A (dense)", "N/A (dense)"]),
        table_row(["Sparsity", "High (few SVs)", "Medium (more SVs with small C)", "None", "None"]),
        table_row(["Requires separability", "Yes (strict)", "No (slack ξ)", "No", "No"]),
        table_row(["Kernel trick", "Yes", "Yes", "Limited", "Via hidden layers"]),
        table_row(["Probability output", "No (scores)", "No (need Platt scaling)", "Yes (direct)", "Yes (softmax)"]),
        table_row(["Scalability", "O(n²) to O(n³)", "O(n²) to O(n³)", "O(n·d)", "O(n·params)"]),
        table_row(["Handles high-d sparse data", "Excellent", "Excellent", "Good", "Needs tuning"]),
        table_row(["Interpretability", "Support vectors", "Support vectors", "Coefficients", "Low"]),
    ),
    callout("🎯", rt("Decision Guide: ", bold=True), rt("Use SVM when data has clear margin structure, d is large (text/genomics), or n is small-medium (< 100K). Use logistic regression when you need calibrated probabilities. Use neural networks when n is large and features are raw (images, audio). Use soft-margin SVM (over hard-margin) whenever any class overlap exists.")),
    heading3("When Support Vector Sparsity Matters Most"),
    bullet(rt("Kernel SVMs on large feature spaces: inference cost is "), eq(r"O(|\mathcal{S}| \cdot d_\text{eff})"), rt(", not "), eq(r"O(n \cdot d_\text{eff}"), rt(")")),
    bullet(rt("Intrerpretability: SVs are prototype examples of each class")),
    bullet(rt("Active learning: SVs indicate the 'confusion boundary' — label points near the current SVs")),
    bullet(rt("Memory-constrained deployment: store only SVs (α, x) pairs")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ──────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Hard-margin SVM: maximum margin hyperplane — understand the primal formulation first")),
    bullet(rt("KKT conditions in SVM context — the mathematical underpinning of why sparsity emerges")),
    bullet(rt("Lagrangian duality — understanding the move from primal to dual")),
    bullet(rt("Inner products & dot products — required for the kernel trick")),
    heading3("What to Learn Next"),
    bullet(rt("Dual formulation & quadratic programming — solving the QP explicitly")),
    bullet(rt("Soft-margin SVM: slack variables, C parameter, hinge loss — generalisation")),
    bullet(rt("Kernel trick: RBF, polynomial kernels — infinite-dimensional feature maps")),
    bullet(rt("Kernel properties: Mercer's theorem, positive semi-definiteness — validity conditions")),
    bullet(rt("SMO algorithm (Platt 1998) — how the dual QP is solved efficiently")),
    heading3("Key Papers"),
    bullet(rt("Boser, Guyon, Vapnik — 'A Training Algorithm for Optimal Margin Classifiers' — COLT 1992. Introduced the kernel SVM.")),
    bullet(rt("Cortes & Vapnik — 'Support-Vector Networks' — Machine Learning 1995. Named the method; introduced soft margins.")),
    bullet(rt("Platt — 'Sequential Minimal Optimization' — 1998. Efficient QP solver still used in libSVM/sklearn.")),
    bullet(rt("Schölkopf, Smola et al. — 'Learning with Kernels' — 2002. Definitive textbook.")),
    heading3("Best Resources"),
    bullet(rt("ESL (Hastie, Tibshirani, Friedman) — Chapter 12: Support Vector Machines and Flexible Discriminants")),
    bullet(rt("Bishop — Pattern Recognition and Machine Learning — Chapter 7: Sparse Kernel Machines")),
    bullet(rt("Andrew Ng — CS229 Lecture Notes on SVMs (freely available online, very clear derivation)")),
    bullet(rt("scikit-learn SVM User Guide — practical notes on C, gamma, kernel selection")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Hard-margin SVM (primal), Soft-margin SVM, Dual formulation & QP, Kernel trick, SMO algorithm, VC dimension & margin bounds, One-class SVM, SVR, KKT conditions.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
