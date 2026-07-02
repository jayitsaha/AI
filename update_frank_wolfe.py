#!/usr/bin/env python3
"""Update Notion page for: Frank-Wolfe (Conditional Gradient) Method"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-814b-a516-ebe064a0aabb"
ICON = "🟠"  # Advanced
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/frank_wolfe_explainer.html"

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
    para(rt("The Frank-Wolfe algorithm (also called the conditional gradient method) solves constrained optimization problems without ever computing a projection. Most gradient methods, after taking a step, must 'snap back' to the feasible set — an expensive operation for complex constraints. Frank-Wolfe avoids this entirely: instead of projecting, it asks 'which corner of the feasible region does the gradient point toward?' and then moves partway toward that corner.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine navigating inside a diamond-shaped room (the feasible set) while trying to get as close as possible to a target point outside the room. Projected Gradient Descent would: step toward the target, land outside the room, then teleport to the nearest wall point (expensive!). Frank-Wolfe instead looks at the direction toward the target, identifies which corner of the room aligns best with that direction, then walks part-way toward that corner — always staying inside, and naturally gravitating to corners (sparse solutions).")),
    heading3("One-Sentence Summary"),
    para(rt("Frank-Wolfe replaces expensive projections with cheap linear minimizations over the constraint set, producing sparse solutions via convex combinations of vertices, at an "), eq(r"O(1/k)"), rt(" convergence rate.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Each FW step solves "), eq(r"s_k = \underset{s \in \mathcal{C}}{\operatorname{argmin}}\; \nabla f(x_k)^\top s"), rt(" (a linear program over the constraint set), then updates "), eq(r"x_{k+1} = (1-\gamma_k)x_k + \gamma_k s_k"), rt(". The convex combination guarantees feasibility without projection. The FW gap "), eq(r"g_k = \nabla f(x_k)^\top(x_k - s_k)"), rt(" is a computable upper bound on "), eq(r"f(x_k) - f^*"), rt(".")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem: Projection is Expensive"),
    para(rt("Constrained optimization appeared throughout 1950s operations research and machine learning. The natural approach — gradient descent followed by projection onto the constraint set — works well for simple constraints (boxes, balls) but became prohibitively expensive for structured constraints: the nuclear norm ball (requires full SVD, "), eq(r"O(n^3)"), rt("), the flow polytope (requires minimum-cost flow), the spectrahedron (PSD cone, requires eigendecomposition). A fundamentally cheaper per-iteration approach was needed.")),
    heading3("The Breakthrough"),
    para(rt("Marguerite Frank and Philip Wolfe introduced the conditional gradient method in 1956, originally for quadratic programming. The key insight: minimizing a linear function over a convex set is typically much cheaper than projecting onto it. For polytopes, it reduces to a linear program (LP) with combinatorial structure; for the nuclear norm ball it reduces to a rank-1 matrix computation. The algorithm lay dormant for decades, then experienced a major revival after 2012 when Jaggi (2013) unified the framework and proved tight "), eq(r"O(1/k)"), rt(" convergence, and when the nuclear norm ball LMO — solvable in "), eq(r"O(n^2)"), rt(" via power iteration vs "), eq(r"O(n^3)"), rt(" for projection — made FW the method of choice for matrix completion.")),
    heading3("Key Papers"),
    bullet(rt("Frank, M. & Wolfe, P. (1956). 'An Algorithm for Quadratic Programming.' Naval Research Logistics Quarterly. — Original paper; quadratic objectives, simplex constraints.")),
    bullet(rt("Jaggi, M. (2013). 'Revisiting Frank-Wolfe: Projection-Free Sparse Convex Optimization.' ICML. — Modern convergence analysis, FW gap certificate, sparse representation theorem.")),
    bullet(rt("Lacoste-Julien, S. & Jaggi, M. (2015). 'On the Global Linear Convergence of Frank-Wolfe Optimization Variants.' NeurIPS. — Away-step and pairwise FW, linear convergence on polytopes.")),
    bullet(rt("Hazan, E. & Kale, S. (2012). 'Projection-Free Online Learning.' ICML. — Online Frank-Wolfe with O(√T) regret.")),
    heading3("Evolution Timeline"),
    para(rt("1956: Frank & Wolfe introduce conditional gradient for quadratic programming. → 1970s–2000s: Largely replaced by interior-point methods for small-scale problems. → 2012–2013: Revival for large-scale ML — matrix completion (nuclear norm), structured SVMs, Lasso boosting. → 2015–present: Variants (Away-step FW, Pairwise FW, Blended FW) achieve linear convergence on polytopes; Stochastic FW for deep learning; FW for federated learning.")),
    heading3("Before vs After: FW vs Projected Gradient Descent"),
    table(4,
        table_row(["Dimension", "Projected GD", "Frank-Wolfe", "Winner"]),
        table_row(["Per-iteration cost", "Gradient + projection", "Gradient + LMO", "FW for complex C"]),
        table_row(["Nuclear norm ball", "O(n³) full SVD", "O(n²) power iteration", "FW"]),
        table_row(["Simplex / polytope", "O(n log n) sort", "O(n) argmin", "PGD slightly"]),
        table_row(["Convergence rate", "O(1/k²) with momentum", "O(1/k) classical", "PGD"]),
        table_row(["Sparsity of iterates", "Dense generally", "≤k+1 atoms (sparse)", "FW"]),
        table_row(["Feasibility guarantee", "After projection", "Always (convex combo)", "FW"]),
        table_row(["Suboptimality certificate", "None (must guess)", "FW gap g_k ≥ f-f*", "FW"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Setup and Key Definitions"),
    para(rt("We want to solve: "), eq(r"\min_{x \in \mathcal{C}} f(x)")),
    para(rt("where "), eq(r"\mathcal{C} \subset \mathbb{R}^d"), rt(" is a compact convex set (constraint set), and "), eq(r"f: \mathbb{R}^d \to \mathbb{R}"), rt(" is convex and "), eq(r"L"), rt("-smooth: "), eq(r"\|\nabla f(x) - \nabla f(y)\| \leq L\|x - y\|"), rt(" for all "), eq(r"x,y")),
    heading3("Linear Minimization Oracle (LMO)"),
    para(rt("The LMO is the computational primitive unique to Frank-Wolfe. Given a direction "), eq(r"g \in \mathbb{R}^d"), rt(", the oracle returns:")),
    equation_block(r"\mathcal{L}(g) = \underset{s \in \mathcal{C}}{\operatorname{argmin}}\; g^\top s"),
    para(rt("For a polytope, this always returns a vertex of "), eq(r"\mathcal{C}"), rt(". The LMO replaces the projection operator "), eq(r"\Pi_\mathcal{C}(x - \alpha \nabla f(x))"), rt(" of gradient descent. Key fact: for "), eq(r"\mathcal{C}"), rt(" a polytope with "), eq(r"V"), rt(" vertices, the LMO is a linear program solvable by combinatorial structure — often in "), eq(r"O(d)"), rt(" time.")),
    heading3("The Frank-Wolfe Gap"),
    para(rt("Define the Frank-Wolfe gap at iteration "), eq(r"k"), rt(" as:")),
    equation_block(r"g_k = \nabla f(x_k)^\top (x_k - s_k) = \max_{s \in \mathcal{C}}\; \nabla f(x_k)^\top (x_k - s)"),
    para(rt("Three properties make "), eq(r"g_k"), rt(" essential: (1) "), eq(r"g_k \geq 0"), rt(" always (LMO minimizes "), eq(r"\nabla f \cdot s"), rt(", so "), eq(r"s_k"), rt(" direction is descent). (2) "), eq(r"g_k \geq f(x_k) - f^*"), rt(" (by convexity: "), eq(r"f(x^*) \geq f(x_k) + \nabla f(x_k)^\top(x^*-x_k) \geq f(x_k)-g_k"), rt("). (3) "), eq(r"g_k = 0"), rt(" if and only if "), eq(r"x_k"), rt(" is optimal. This means "), eq(r"g_k"), rt(" is a computable certificate of "), eq(r"\varepsilon"), rt("-optimality.")),
    callout("🔑", rt("Key property — Sparsity: ", bold=True), rt("After "), eq(r"k"), rt(" iterations, the FW iterate can be written as a convex combination of at most "), eq(r"k+1"), rt(" vertices of "), eq(r"\mathcal{C}"), rt(": "), eq(r"x_k = \sum_{i=1}^{k+1} \lambda_i v_i"), rt(" with "), eq(r"\sum \lambda_i = 1, \lambda_i \geq 0"), rt(". This is the atomic decomposition / boosting connection: each FW step 'adds an atom' (vertex/weak learner).")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ─────────────────────────
    heading2("🏗️ Architecture & Internal Workings (PhD Deep-Dive)"),
    heading3("The Algorithm in Full"),
    para(rt("Input: "), eq(r"f"), rt(" (objective), "), eq(r"\nabla f"), rt(" (gradient oracle), LMO (linear minimization oracle), "), eq(r"x_0 \in \mathcal{C}"), rt(" (initial feasible point), step schedule "), eq(r"\{\gamma_k\}"), rt(".")),
    code_block("python", """# Frank-Wolfe / Conditional Gradient — complete implementation
import numpy as np

def frank_wolfe(f, grad_f, lmo, x0, n_iters=100, tol=1e-8):
    \"\"\"
    Solve min_{x in C} f(x) via the Frank-Wolfe algorithm.

    Args:
        f       : objective f(x) -> float
        grad_f  : gradient oracle, grad_f(x) -> array shape (d,)
        lmo     : linear minimization oracle, lmo(g) -> argmin_{s in C} g.dot(s)
        x0      : initial point in C, shape (d,)
        n_iters : maximum iterations
        tol     : convergence tolerance on FW gap

    Returns:
        x       : final iterate (approximately optimal)
        history : list of dicts with per-iteration diagnostics
    \"\"\"
    x = x0.copy()
    history = [{'k': 0, 'x': x.copy(), 'f': f(x), 'fw_gap': None}]

    for k in range(1, n_iters + 1):
        # Step 1: Compute gradient
        g = grad_f(x)

        # Step 2: Solve LMO — the key computation that replaces projection
        s = lmo(g)  # argmin_{s in C} g.dot(s)

        # Step 3: Compute FW gap (suboptimality certificate)
        fw_gap = float(g.dot(x - s))

        # Step 4: Convergence check — gap is computable bound on f(x)-f*
        if fw_gap <= tol:
            print(f"Converged at k={k}, FW gap={fw_gap:.2e}")
            break

        # Step 5: Choose step size
        gamma = 2.0 / (k + 2)  # Classical decreasing schedule: O(1/k) rate
        # Alternative: line search for faster practical convergence
        # gamma = line_search(f, x, s, g)  # minimize f(x + gamma*(s-x)) over [0,1]

        # Step 6: Update — CONVEX COMBINATION guarantees x stays in C
        x = (1.0 - gamma) * x + gamma * s

        history.append({
            'k': k, 'x': x.copy(), 'f': f(x),
            'fw_gap': fw_gap, 's': s.copy(), 'gamma': gamma
        })

    return x, history

# ── Example: Matrix completion (nuclear norm ball) ─────────────────────
# min_{X: ||X||_* <= tau} (1/2)||P_Omega(X) - M_Omega||_F^2
# LMO: rank-1 update via power iteration (O(n^2)) vs full SVD for projection (O(n^3))

def nuclear_norm_lmo(G, tau):
    \"\"\"LMO for nuclear norm ball: argmin_{||S||_* <= tau} <G, S>
    Solution: -tau * u v^T where u,v are left/right singular vectors of G.
    Computed via O(n^2) power iteration, NOT O(n^3) full SVD.
    \"\"\"
    # Power iteration for top singular vectors
    n, m = G.shape
    v = np.random.randn(m); v /= np.linalg.norm(v)
    for _ in range(20):
        u = G @ v; u /= np.linalg.norm(u)
        v = G.T @ u; v /= np.linalg.norm(v)
    sigma = u @ G @ v
    return -tau * np.outer(u, v) if sigma > 0 else tau * np.outer(u, v)
"""),
    heading3("Numerical Trace — 4 Iterations on the ℓ₁ Ball"),
    para(rt("Minimize "), eq(r"f(x) = \tfrac{1}{2}\|x - (2,2)\|^2"), rt(" over "), eq(r"\|x\|_1 \leq 1"), rt(". Vertices: "), eq(r"\{(\pm1,0),(0,\pm1)\}"), rt(". Optimal: "), eq(r"x^* = (0.5, 0.5)"), rt(", "), eq(r"f^* = 2.25"), rt(".")),
    table(7,
        table_row(["k", "x_k", "∇f(x_k)", "LMO s_k", "FW gap g_k", "γ_k", "f(x_k)−f*"]),
        table_row(["0", "(0, 0)", "(−2, −2)", "—", "—", "—", "1.750"]),
        table_row(["1", "(0, 0)", "(−2, −2)", "(1, 0)", "2.000", "2/3", "0.639"]),
        table_row(["2", "(0.667, 0)", "(−1.333, −2)", "(0, 1)", "1.111", "1/2", "0.264"]),
        table_row(["3", "(0.333, 0.5)", "(−1.667, −1.5)", "(1, 0)", "0.361", "2/5", "0.175"]),
        table_row(["4", "(0.6, 0.3)", "(−1.4, −1.7)", "(0, 1)", "0.350", "1/3", "0.106"]),
    ),
    heading3("Design Decision: Why Convex Combination (Not Gradient Step)?"),
    para(rt("PGD takes a gradient step "), eq(r"x - \alpha \nabla f(x)"), rt(" (which may leave "), eq(r"\mathcal{C}"), rt("), then projects back. FW instead takes "), eq(r"(1-\gamma)x + \gamma s"), rt(" — a point on the segment from "), eq(r"x"), rt(" to "), eq(r"s"), rt(". Since both "), eq(r"x"), rt(" and "), eq(r"s"), rt(" are in the convex set "), eq(r"\mathcal{C}"), rt(", every convex combination is also in "), eq(r"\mathcal{C}"), rt(". No projection needed. The tradeoff: FW can only move along the segment "), eq(r"[x, s]"), rt(", which is a 1D restriction — this is why FW can't achieve the "), eq(r"O(1/k^2)"), rt(" rate of accelerated PGD.")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("Non-smooth f: FW requires a gradient. For non-smooth objectives, use subgradient methods or smooth approximations.")),
    bullet(rt("Unbounded C: The FW gap is 0 for any x when C is all of ℝ^d — the LMO returns −∞. FW only works for compact C.")),
    bullet(rt("Zigzag near polytope faces: On polytopes, classical FW can 'zig-zag' between two vertices without converging linearly. Away-step FW (Lacoste-Julien & Jaggi, 2015) fixes this.")),
    bullet(rt("Step size sensitivity: Using γ=2/(k+2) is safe but slow. Line search typically gives 5-10× faster practical convergence.")),
    divider(),

    # ── Section 5: The Math ────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Full Convergence Proof (Smooth Convex Case)"),
    para(rt("Assume "), eq(r"f"), rt(" is convex and "), eq(r"L"), rt("-smooth on "), eq(r"\mathcal{C}"), rt(" with diameter "), eq(r"D = \max_{x,y \in \mathcal{C}} \|x-y\|"), rt(". Set "), eq(r"\gamma_k = 2/(k+2)"), rt(". We prove "), eq(r"f(x_k) - f^* \leq \frac{2LD^2}{k+2}"), rt(".")),
    para(rt("Step 1 — Descent from smoothness. With "), eq(r"d_k = s_k - x_k"), rt(", the "), eq(r"L"), rt("-smoothness quadratic upper bound gives:")),
    equation_block(r"f(x_{k+1}) \leq f(x_k) + \gamma_k \underbrace{\nabla f(x_k)^\top d_k}_{= -g_k} + \frac{L \gamma_k^2}{2} \|d_k\|^2 \leq f(x_k) - \gamma_k g_k + \frac{L \gamma_k^2 D^2}{2}"),
    para(rt("Step 2 — Lower bound on gap from convexity. Since "), eq(r"f"), rt(" is convex and "), eq(r"x^*"), rt(" is optimal in "), eq(r"\mathcal{C}"), rt(":")),
    equation_block(r"f(x_k) - f^* \leq \nabla f(x_k)^\top (x_k - x^*) \leq \max_{s \in \mathcal{C}} \nabla f(x_k)^\top (x_k - s) = g_k"),
    para(rt("So "), eq(r"g_k \geq f(x_k) - f^*"), rt(". Define "), eq(r"h_k = f(x_k) - f^*"), rt(". Then:")),
    equation_block(r"h_{k+1} \leq h_k - \gamma_k h_k + \frac{L \gamma_k^2 D^2}{2} = (1-\gamma_k) h_k + \frac{L \gamma_k^2 D^2}{2}"),
    para(rt("Step 3 — Telescoping. Set "), eq(r"\gamma_k = 2/(k+2)"), rt(". Claim: "), eq(r"h_k \leq \frac{2LD^2}{k+2}"), rt(". Proof by induction: base "), eq(r"k=0"), rt(": "), eq(r"h_0 \leq LD^2/2"), rt(" (by smoothness). Inductive step with "), eq(r"h_k \leq \frac{2LD^2}{k+2}"), rt(":")),
    equation_block(r"h_{k+1} \leq \left(1-\frac{2}{k+2}\right)\frac{2LD^2}{k+2} + \frac{L}{2}\cdot\frac{4}{(k+2)^2}\cdot D^2 = \frac{2LD^2}{k+2}\cdot\frac{k}{k+2}+\frac{2LD^2}{(k+2)^2} = \frac{2LD^2}{(k+2)^2}(k+1) = \frac{2LD^2}{k+3}"),
    heading3("Optimal Step Size via Line Search"),
    para(rt("On the segment "), eq(r"x_k + \gamma(s_k - x_k)"), rt(", the optimal step is:")),
    equation_block(r"\gamma_k^* = \underset{\gamma \in [0,1]}{\operatorname{argmin}}\; f(x_k + \gamma(s_k - x_k))"),
    para(rt("For quadratic "), eq(r"f(x) = \tfrac{1}{2}x^\top A x + b^\top x"), rt(", this has a closed form:")),
    equation_block(r"\gamma_k^* = \min\!\left(1,\; \frac{-\nabla f(x_k)^\top d_k}{d_k^\top A\, d_k}\right) = \min\!\left(1,\; \frac{g_k}{d_k^\top A\, d_k}\right)"),
    heading3("Linear Convergence on Polytopes (Away-Step FW)"),
    para(rt("For strongly convex "), eq(r"f"), rt(" ("), eq(r"\mu > 0"), rt(") on a polytope, classical FW still only achieves "), eq(r"O(1/k)"), rt(" due to zigzagging. The away-step variant achieves linear convergence. At each step, choose the better of:")),
    bullet(rt("FW direction: toward s_k (LMO vertex)")),
    bullet(rt("Away direction: away from the vertex v_k with largest gradient inner product — 'removes' a bad atom from the current decomposition")),
    para(rt("Result: away-step FW achieves "), eq(r"f(x_k) - f^* \leq (1-\rho)^k (f(x_0)-f^*)"), rt(" where "), eq(r"\rho"), rt(" depends on the geometry of "), eq(r"\mathcal{C}"), rt(" (pyramidal width).")),
    callout("⚠️", rt("Common misconception: ", bold=True), rt("Frank-Wolfe is sometimes called a 'first-order method with O(1/k) rate, matching gradient descent.' But classical GD on unconstrained smooth convex achieves O(1/k) too. The advantage of FW is NOT rate — it is "), rt("projection-free operation + sparse iterates + built-in feasibility certificate", bold=True), rt(". For strongly convex f without constraint structure, use L-BFGS or accelerated PGD instead.")),
    divider(),

    # ── Section 6: Code Implementation ────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """import numpy as np
from typing import Callable, Optional

def frank_wolfe(
    f: Callable,
    grad_f: Callable,
    lmo: Callable,
    x0: np.ndarray,
    n_iters: int = 200,
    tol: float = 1e-7,
    step: str = 'decreasing',  # 'decreasing' | 'line_search'
    verbose: bool = True,
) -> tuple:
    \"\"\"Frank-Wolfe / Conditional Gradient.

    Args:
        step: 'decreasing' uses γ=2/(k+2); 'line_search' uses exact minimization.
    Returns: (x_opt, history)
    \"\"\"
    x = x0.copy().astype(float)
    history = []

    for k in range(1, n_iters + 1):
        g = grad_f(x)                       # gradient oracle call
        s = lmo(g)                          # LMO: argmin_{v in C} g.dot(v)
        d = s - x                           # Frank-Wolfe direction
        fw_gap = float(np.dot(g, x - s))   # g_k >= f(x)-f*, computable certificate

        if fw_gap <= tol:
            if verbose: print(f"[FW] Converged k={k}, gap={fw_gap:.2e}")
            break

        if step == 'decreasing':
            gamma = 2.0 / (k + 2)
        elif step == 'line_search':
            # Bisection or closed-form if f is quadratic
            gamma = _line_search(f, x, d)
        else:
            gamma = float(step)

        x = x + gamma * d  # Equiv: (1-gamma)*x + gamma*s

        if verbose and k % 10 == 0:
            print(f"  k={k:4d} | f(x)={f(x):.6f} | gap={fw_gap:.4e} | γ={gamma:.4f}")

        history.append({'k': k, 'fw_gap': fw_gap, 'gamma': gamma, 'f': f(x)})

    return x, history

def _line_search(f, x, d, n_pts=20):
    \"\"\"Simple grid line search over gamma in [0,1].\"\"\"
    gammas = np.linspace(0, 1, n_pts + 1)
    vals = [f(x + g * d) for g in gammas]
    return gammas[int(np.argmin(vals))]

# ── LMOs for common constraint sets ──────────────────────────────────────
def lmo_simplex(g):
    \"\"\"LMO for probability simplex {x: sum=1, x>=0}. O(d).\"\"\"
    return np.eye(len(g))[np.argmin(g)]  # e_i where i = argmin g_i

def lmo_l1_ball(g, radius=1.0):
    \"\"\"LMO for L1 ball {x: ||x||_1 <= r}. O(d).\"\"\"
    # Minimize g.dot(s) over ||s||_1 <= r: s* = -r * sign(g_i*) * e_{i*}
    i_star = np.argmax(np.abs(g))
    s = np.zeros_like(g)
    s[i_star] = -radius * np.sign(g[i_star])
    return s

def lmo_nuclear_ball(G, tau=1.0):
    \"\"\"LMO for nuclear norm ball {X: ||X||_* <= tau}. O(n^2) via power iteration.\"\"\"
    # argmin_{||S||_* <= tau} <G, S> = -tau * u * v^T (top left/right singular vectors)
    n, m = G.shape
    v = np.random.randn(m); v /= np.linalg.norm(v)
    for _ in range(30):  # power iteration
        u = G @ v; u /= np.linalg.norm(u)
        v = G.T @ u; v /= np.linalg.norm(v)
    # sign: want to minimize <G, S> = sigma * u^T G v, so S = -tau*u*v^T
    return -tau * np.outer(u, v)

def lmo_spectahedron(G, d):
    \"\"\"LMO for spectrahedron {X psd: Tr(X)=1}. O(d^2) via top eigenvector.\"\"\"
    # argmin_{Tr(X)=1, X>=0} <G, X> = v_min * v_min^T (outer product of smallest eigenvec)
    eigvals, eigvecs = np.linalg.eigh(G)
    v = eigvecs[:, 0]  # smallest eigenvalue's vector
    return np.outer(v, v)
"""),
    heading3("6b — Production Usage (sklearn / cvxpy)"),
    code_block("python", """# Production: Frank-Wolfe for Lasso via boosting (coordinate-wise FW on simplex)
import numpy as np
from sklearn.linear_model import Lasso

# Method 1: LASSO via sklearn (interior-point, not FW, but shows the problem)
model = Lasso(alpha=0.1, max_iter=1000, tol=1e-4)
model.fit(X_train, y_train)
print(f"sklearn Lasso: {np.sum(model.coef_ != 0)} nonzero coefs")

# Method 2: Frank-Wolfe on simplex (sparse basis pursuit)
# Useful when: d >> n, need interpretable sparse model, projection is expensive
def lasso_fw(X, y, tau, n_iters=500):
    \"\"\"
    Solve min_{||w||_1 <= tau} (1/2n)||Xw - y||^2 via Frank-Wolfe.
    Each LMO step selects one feature (coordinate) — naturally sparse!
    \"\"\"
    n, d = X.shape
    w = np.zeros(d)
    for k in range(1, n_iters + 1):
        residual = X @ w - y
        grad = X.T @ residual / n           # gradient w.r.t. w
        # LMO on L1 ball: pick the coordinate with largest |gradient|
        i = np.argmax(np.abs(grad))
        s = np.zeros(d)
        s[i] = -tau * np.sign(grad[i])     # vertex of L1 ball
        fw_gap = np.dot(grad, w - s)
        if fw_gap < 1e-7:
            break
        gamma = 2.0 / (k + 2)
        w = (1 - gamma) * w + gamma * s
        # Note: w has at most k+1 nonzero entries after k steps!
    return w

# Gotchas:
# ⚠️ Line search dramatically outperforms fixed schedule in practice
# ⚠️ For strongly convex f, use Away-Step FW (sklearn.linear_model.OrthogonalMatchingPursuit)
# ⚠️ Nuclear norm: use sklearn.decomposition.NMF or implement via power iteration
# ⚠️ FW for matrix factorization: each LMO is a rank-1 SVD (fast via LAPACK dsyevd)
"""),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎯 Interview Deep-Dive"),
    heading3("Q1 (Easy): What is the Frank-Wolfe algorithm and how does it differ from projected gradient descent?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Frank-Wolfe (conditional gradient) solves constrained optimization by replacing the projection step with a linear minimization oracle (LMO). At each step: (1) compute gradient ∇f(x_k), (2) find s_k = argmin_{s∈C} ∇f(x_k)ᵀs (linear oracle), (3) update x_{k+1} = (1-γ_k)x_k + γ_k s_k (convex combination, always feasible).")),
        para(rt("PGD instead: (1) take gradient step x̃ = x_k - α∇f(x_k), (2) project x_{k+1} = Π_C(x̃). FW is preferred when projection is expensive (nuclear norm ball, spectrahedron) but the LMO is cheap.")),
    ]),
    heading3("Q2 (Easy): What is the Frank-Wolfe gap and why is it important?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("The FW gap at iteration k is g_k = ∇f(x_k)ᵀ(x_k - s_k) ≥ 0. It is important because: (1) it is computable at every iteration (no extra cost), (2) by convexity, g_k ≥ f(x_k) - f*, so it is a certificate of ε-suboptimality, (3) g_k = 0 iff x_k is optimal. Unlike PGD which requires knowing f*, FW has a built-in stopping criterion.")),
    ]),
    heading3("Q3 (Medium): What is the convergence rate of classical Frank-Wolfe, and why can't it be accelerated to O(1/k²)?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Classical FW achieves O(1/k) for smooth convex f. Nesterov's acceleration for PGD achieves O(1/k²) by using a 'momentum' step that overshoots the feasible set and then projects back. FW cannot overshoot: every iterate is a convex combination of points in C, so all iterates lie in C. The momentum step would require going outside C momentarily, which FW's convex-combination structure forbids. Gradient sliding (Lan, 2016) can achieve O(1/k²) FW-style but with different LMO oracle complexity.")),
    ]),
    heading3("Q4 (Medium): When does FW converge linearly on polytopes?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Classical FW does NOT converge linearly on polytopes for strongly convex f — it suffers from zigzag oscillation between two vertices. The away-step variant (Lacoste-Julien & Jaggi, 2015) adds an 'away direction': move away from the current worst vertex in the decomposition. This achieves linear convergence: f(x_k) - f* ≤ (1-ρ)^k(f(x_0)-f*) where ρ ∝ μ/(LD) depends on the strong convexity constant μ, Lipschitz constant L, and pyramidal width δ of the polytope. The pairwise FW variant also achieves this and keeps the iterate's decomposition even sparser.")),
    ]),
    heading3("Q5 (Hard): Explain the connection between Frank-Wolfe and boosting in machine learning."),
    toggle([rt("Answer", bold=True)], [
        para(rt("Boosting (AdaBoost, gradient boosting) iteratively adds weak learners (hypotheses from a hypothesis class H) to build a strong ensemble. Each round: compute residuals/functional gradient, find the weak learner h* that best aligns with residuals, update ensemble. This is exactly Frank-Wolfe on the simplex over H. The feasible set C = conv(H) (the convex hull of all hypotheses). The LMO = argmin_{h∈H} ⟨functional gradient, h⟩ = finding the weak learner that correlates most with the current residual. The FW update = adding h* with weight γ_k. The FW sparsity property means boosting produces an ensemble using at most k weak learners after k rounds. This structural equivalence was proved by Jaggi (2013) and connects the convergence analysis of boosting to FW theory.")),
        callout("⚠️", rt("Follow-up trap: ", bold=True), rt("'So boosting converges at O(1/k)?' — Yes, for the convex surrogate loss. AdaBoost's original analysis was different (exponential convergence to zero training error for linearly separable data). The FW analysis gives convergence guarantees for the functional gradient view.")),
    ]),
    heading3("Q6 (Hard): How is Frank-Wolfe used for matrix completion, and what is the LMO complexity?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Matrix completion: given partial observations M_Ω, solve min_{||X||_* ≤ τ} (1/2)||P_Ω(X)-M_Ω||_F². The constraint is the nuclear norm ball (set of matrices with nuclear norm ≤ τ). Projection onto this set requires full SVD (O(n³) for n×n matrices). The FW LMO: argmin_{||S||_*≤τ} ⟨G, S⟩ = -τ·u₁v₁ᵀ where u₁,v₁ are the top left/right singular vectors of G. These can be computed by power iteration in O(n²) without the full SVD. Each FW iterate is a sum of at most k rank-1 matrices — the implicit low-rank structure. For the matrix completion setting n=10,000 (MovieLens 10M), FW with O(n²) LMO vs O(n³) projection means 100× cheaper per iteration.")),
    ]),
    heading3("Multi-Level Explanations"),
    heading3("To a PhD Researcher:"),
    para(rt("FW achieves the information-theoretic lower bound of "), eq(r"O(1/k)"), rt(" for smooth convex optimization with projection-free oracle access. The analysis via the FW gap immediately gives an instance-adaptive stopping criterion. On polytopes, the pyramidal width "), eq(r"\delta(\mathcal{P})"), rt(" controls linear convergence of away-step FW. The FW sparsity theorem — after "), eq(r"k"), rt(" steps, "), eq(r"x_k = \sum_{i \leq k+1} \lambda_i v_i"), rt(" — connects to the notion of 'boosting complexity' in learning theory. Open questions: tight convergence under weaker smoothness; FW with higher-order oracles; optimal rates for stochastic FW.")),
    heading3("To a Research Scientist/Engineer:"),
    para(rt("Use FW when: your constraint is a nuclear norm ball or spectrahedron (projection = full SVD, but LMO = power iteration). Practically, always use line search — the classical γ=2/(k+2) schedule is conservative. Away-step FW is a drop-in improvement with no additional LMO cost. For large-scale matrix problems, exploit the implicit low-rank structure of FW iterates — don't form the full n×n matrix, store the rank-k decomposition. Monitor the FW gap as a stopping criterion; never guess based on iteration count.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ───────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Method", "Rate (smooth cvx)", "Projection needed?", "Sparsity", "Best for"]),
        table_row(["Frank-Wolfe (classical)", "O(1/k)", "No", "Yes, ≤k+1 atoms", "Nuclear norm, polytopes"]),
        table_row(["Projected GD", "O(1/k)", "Yes", "No", "Simple constraints"]),
        table_row(["Acc. PGD (Nesterov)", "O(1/k²)", "Yes", "No", "Smooth + simple C"]),
        table_row(["Away-Step FW", "Linear (str. cvx + polytope)", "No", "Yes", "Strongly cvx, polytopes"]),
        table_row(["Interior Point", "Polynomial (Newton)", "No", "No", "Small-scale, exact soln"]),
        table_row(["ADMM", "O(1/k)", "Implicit", "Depends", "Distributed, separable"]),
        table_row(["Subgradient", "O(1/√k)", "Yes", "No", "Non-smooth objectives"]),
    ),
    heading3("When to Use Frank-Wolfe"),
    bullet(rt("Nuclear norm ball constraint (matrix completion, multi-task learning) — LMO is O(n²) vs O(n³) projection.")),
    bullet(rt("Simplex / probability simplex — sparse solutions needed (boosting, attention allocation, online learning).")),
    bullet(rt("Flow polytopes, matching polytopes — LMO is a min-cost flow or assignment problem (polynomial, but combinatorial).")),
    bullet(rt("Spectrahedron (PSD matrices with unit trace) — LMO is top eigenvector, O(d²).")),
    heading3("When NOT to Use Frank-Wolfe"),
    bullet(rt("Simple box or L2 constraints — projection is O(d) and trivial; use accelerated PGD.")),
    bullet(rt("Non-smooth objectives — FW requires gradients; use subgradient methods or smooth proximal operators.")),
    bullet(rt("Need O(1/k²) rate — use Nesterov acceleration with PGD if projection is affordable.")),
    bullet(rt("Stochastic objectives with small batch noise — stochastic FW has O(1/k^(1/3)) rate (Mokhtari et al., 2020), often worse than stochastic PGD.")),
    callout("🎯", rt("Decision rule: ", bold=True), rt("If "), rt("projection_cost > LMO_cost by ≥ 5×", bold=True), rt(", use Frank-Wolfe. If you also need sparse solutions or the constraint has combinatorial structure, FW is strongly preferred. If you need "), eq(r"O(1/k^2)"), rt(" and projection is cheap, use accelerated PGD.")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ───────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through Frank-Wolfe iterations on the ℓ₁-ball — watch the LMO select vertices, compare with PGD path, and observe the FW gap convergence certificate. Use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Convex optimization fundamentals (convex sets, convex functions, optimality conditions)")),
    bullet(rt("Gradient descent and convergence analysis (smooth convex, L-smoothness, strong convexity)")),
    bullet(rt("Linear programming basics (vertices of polytopes, simplex method)")),
    bullet(rt("Projected Gradient Descent (Euclidean projection, Moreau envelope)")),
    heading3("What to Learn Next"),
    bullet(rt("Proximal Gradient Methods — alternative to projection, handles composite objectives")),
    bullet(rt("Mirror Descent — generalized projection via Bregman divergence")),
    bullet(rt("ADMM (Alternating Direction Method of Multipliers) — decomposable constraints")),
    bullet(rt("Stochastic Frank-Wolfe — variance reduction techniques (SPIDER-FW, MomentumFW)")),
    bullet(rt("Non-smooth constrained optimization — bundle methods, cutting plane methods")),
    heading3("Key Papers"),
    bullet(rt("Frank & Wolfe (1956). 'An Algorithm for Quadratic Programming.' Naval Res. Logistics. — The original paper.")),
    bullet(rt("Jaggi (2013). 'Revisiting Frank-Wolfe: Projection-Free Sparse Convex Optimization.' ICML. — Modern convergence, sparsity, FW gap certificate.")),
    bullet(rt("Lacoste-Julien & Jaggi (2015). 'On the Global Linear Convergence of Frank-Wolfe Optimization Variants.' NeurIPS. — Away-step FW, pairwise FW, linear convergence.")),
    bullet(rt("Hazan & Kale (2012). 'Projection-Free Online Learning.' ICML. — Online FW with O(√T) regret bound.")),
    bullet(rt("Lan (2016). 'Conditional Gradient Sliding for Convex Optimization.' SIAM J. Optim. — O(1/k²) rate using gradient sliding.")),
    heading3("Best Resources"),
    bullet(rt("Jaggi (2011). 'Sparse Convex Optimization.' PhD thesis, ETH Zurich — comprehensive FW coverage.")),
    bullet(rt("Boyd & Vandenberghe 'Convex Optimization' (free online) — Ch. 9 for descent methods framework.")),
    bullet(rt("Simon Lacoste-Julien's ICML 2016 tutorial on Frank-Wolfe methods (slides available online).")),
    bullet(rt("FrankWolfe.jl (Julia) and COPT/Gurobi Python bindings for the LMO — practical implementations.")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Gradient Descent, Projected Gradient Descent, Proximal Gradient, Mirror Descent, ADMM, Boosting (Gradient Boosting = FW on function space), Matrix Completion (nuclear norm optimization), Stochastic Optimization, Online Convex Optimization.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
