#!/usr/bin/env python3
"""Update Notion page for: Exact inference: variable elimination, belief propagation"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81ad-9ecd-eb09387a5cce"
ICON = "🟠"
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/exact_inference_ve_bp_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: 30-Second Version ──────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("A Bayesian Network stores a joint probability distribution as a product of small factors. "
            "To answer a query like P(disease | symptoms), you need to sum out all unobserved variables. "
            "Exact inference algorithms do this precisely -- no guessing, no sampling -- by exploiting the graph's structure.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine computing the total cost of a shopping trip where each item's price depends on the previous. "
            "Instead of listing every possible combination of purchases and summing, you 'factor out' common terms early "
            "— cancelling variables as you go. Variable Elimination and Belief Propagation are systematic ways to do exactly that.")),
    heading3("One-Sentence Summary"),
    para(rt("Both algorithms exploit distributivity of summation over multiplication to push 'sum-outs' inside factor products, "
            "reducing exponential enumeration to a computation whose cost scales as ", bold=False),
        eq(r"O(n \cdot k^{w+1})"),
        rt(" where ", bold=False), eq(r"w"), rt(" is the graph's treewidth.", bold=False)),
    callout("💡", rt("If you remember one thing: ", bold=True),
            rt("Variable Elimination and Belief Propagation are the same algebraic trick (push sums inside products) "
               "scheduled differently — VE answers one query; BP answers all marginals simultaneously.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Early probabilistic models required explicit enumeration of all states. A network with 20 binary variables "
            "has 2²⁰ ≈ 1 million states; with 100 variables, 2¹⁰⁰ — completely intractable.")),
    heading3("Key Papers & Timeline"),
    bullet(rt("1988 — "), rt("Pearl, J., ", italic=True), rt('"Probabilistic Reasoning in Intelligent Systems." ', italic=True),
           rt("Morgan Kaufmann. Introduced Belief Propagation on trees and laid foundations for exact graphical-model inference.")),
    bullet(rt("1990 — "), rt("Zhang & Poole, ", italic=True), rt('"Exploiting Causal Independence in Bayesian Network Inference." ', italic=True),
           rt("Formalized variable elimination.")),
    bullet(rt("1994 — "), rt("Lauritzen & Spiegelhalter; Jensen et al. ", italic=True),
           rt("Junction Tree / Clique Tree propagation for exact inference on general graphs.")),
    bullet(rt("1999 — "), rt("Yedidia, Freeman & Weiss — Loopy BP; showed BP is fixed-point of Bethe free energy minimization.")),
    heading3("Before vs After"),
    table(4,
        table_row(["Dimension", "Naïve Enumeration", "Variable Elimination", "Belief Propagation"]),
        table_row(["Complexity", "O(k^n)", "O(n · k^{w+1})", "O(n · k^2) on trees"]),
        table_row(["Answers", "All (expensive)", "One query", "All marginals"]),
        table_row(["Structure used", "None", "Elimination order", "Message schedule"]),
        table_row(["Handles cycles", "Yes (slow)", "Yes (junction tree)", "Exact on trees; approx loopy"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Factor", bold=True), rt(": A function "), eq(r"\phi_s(\mathbf{x}_{C_s})"), rt(" over a subset "), eq(r"C_s"), rt(" of variables. Encodes local dependencies.")),
    bullet(rt("Factor Graph", bold=True), rt(": Bipartite graph with variable nodes and factor nodes. Edge "), eq(r"(X_i, f_s)"), rt(" iff "), eq(r"X_i \in C_s"), rt(".")),
    bullet(rt("Treewidth", bold=True), rt(" ("), eq(r"w"), rt("): The minimum, over all elimination orderings, of the maximum clique size minus 1 in the induced graph. Governs inference complexity.")),
    bullet(rt("Message", bold=True), rt(": A function over one variable's domain, passed along a factor-graph edge during BP.")),
    callout("🔑", rt("Key Property: ", bold=True),
            rt("Both VE and BP are instances of the same algebraic semiring computation (sum-product) scheduled on the factor graph. "
               "On a tree, this is exact; on a loopy graph, running BP iteratively ("Loopy BP") is an approximation.")),
    heading3("Prerequisites"),
    bullet(rt("Bayesian Networks and conditional independence (d-separation).")),
    bullet(rt("Probability: marginalization, conditional probability, Bayes' theorem.")),
    bullet(rt("Factor graphs and their relationship to directed / undirected graphical models.")),
    divider(),

    # ── Section 4: Architecture Deep-Dive ─────────────────────────────────────
    heading2("🔬 Architecture & Internal Workings"),
    heading3("Variable Elimination Algorithm"),
    numbered(rt("Represent joint as a pool of factors: "), eq(r"\mathcal{F} = \{\phi_1, \phi_{12}, \phi_{23}, \ldots\}")),
    numbered(rt("Choose an elimination ordering "), eq(r"\pi = (X_1, X_2, \ldots, X_{n-1})"), rt(" of all non-query variables.")),
    numbered(rt("For each "), eq(r"X_k"), rt(" in "), eq(r"\pi"), rt(":")),
    bullet(rt("Collect all "), eq(r"\phi \in \mathcal{F}"), rt(" that contain "), eq(r"X_k"), rt(": form "), eq(r"\psi_k = \prod \{\phi : X_k \in \text{scope}(\phi)\}")),
    bullet(rt("Sum out: "), eq(r"\tau_k(\mathbf{x}_{\text{scope}(\psi_k) \setminus X_k}) = \sum_{x_k} \psi_k")),
    bullet(rt("Remove used factors; add "), eq(r"\tau_k"), rt(" to "), eq(r"\mathcal{F}")),
    numbered(rt("Multiply remaining factors (only mention query), normalize: "), eq(r"P(X_q) \propto \prod_{\phi \in \mathcal{F}} \phi")),

    heading3("Numerical Trace — 4-node Chain"),
    para(rt("Binary variables "), eq(r"X_1, X_2, X_3, X_4"), rt(". Factors:")),
    bullet(eq(r"\phi_1 = [0.6,\;0.4]")),
    bullet(eq(r"\phi_{12} = \begin{bmatrix}0.9 & 0.1\\0.2 & 0.8\end{bmatrix}")),
    bullet(eq(r"\phi_{23} = \begin{bmatrix}0.7 & 0.3\\0.4 & 0.6\end{bmatrix}")),
    bullet(eq(r"\phi_{34} = \begin{bmatrix}0.8 & 0.2\\0.3 & 0.7\end{bmatrix}")),
    para(rt("Eliminate "), eq(r"X_1"), rt(":")),
    equation_block(r"\tau_1(x_2) = \sum_{x_1}\phi_1(x_1)\phi_{12}(x_1,x_2) = [0.6\cdot0.9+0.4\cdot0.2,\;0.6\cdot0.1+0.4\cdot0.8] = [0.62,\;0.38]"),
    para(rt("Eliminate "), eq(r"X_2"), rt(":")),
    equation_block(r"\tau_2(x_3) = \sum_{x_2}\tau_1(x_2)\phi_{23}(x_2,x_3) = [0.62\cdot0.7+0.38\cdot0.4,\;0.62\cdot0.3+0.38\cdot0.6] = [0.586,\;0.414]"),
    para(rt("Eliminate "), eq(r"X_3"), rt(":")),
    equation_block(r"\tau_3(x_4) = \sum_{x_3}\tau_2(x_3)\phi_{34}(x_3,x_4) = [0.586\cdot0.8+0.414\cdot0.3,\;0.586\cdot0.2+0.414\cdot0.7] = [0.5928,\;0.4072]"),
    para(rt("Normalized: "), eq(r"P(X_4=0)\approx0.593,\quad P(X_4=1)\approx0.407")),

    heading3("Belief Propagation on Factor Graphs"),
    para(rt("Messages between variable node "), eq(r"X_i"), rt(" and factor node "), eq(r"f_s"), rt(":")),
    equation_block(r"\mu_{X_i \to f_s}(x_i) = \prod_{f_t \in \text{ne}(X_i)\setminus f_s} \mu_{f_t \to X_i}(x_i)"),
    equation_block(r"\mu_{f_s \to X_i}(x_i) = \sum_{\mathbf{x}_{C_s \setminus i}} f_s(\mathbf{x}_{C_s}) \prod_{X_j \in C_s \setminus \{i\}} \mu_{X_j \to f_s}(x_j)"),
    para(rt("Belief (marginal) at "), eq(r"X_i"), rt(":")),
    equation_block(r"b(x_i) \propto \prod_{f_s \in \text{ne}(X_i)} \mu_{f_s \to X_i}(x_i)"),

    callout("⚙️", rt("Design Decision: ", bold=True),
            rt("VE produces one intermediate factor table per eliminated variable. BP reuses these as messages sent in both directions. "
               "The junction-tree algorithm makes this relationship exact: VE along a clique tree IS BP on the junction tree.")),
    divider(),

    # ── Section 5: Math ────────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Distributive Law — The Core Identity"),
    para(rt("The key identity enabling both algorithms:")),
    equation_block(r"\sum_x \prod_s \phi_s(\mathbf{x}_{C_s}) = \prod_{s: x \notin C_s} \phi_s \cdot \sum_x \prod_{s: x \in C_s} \phi_s"),
    para(rt("We can push the summation over "), eq(r"x"), rt(" inside, affecting only factors that mention "), eq(r"x"), rt(". "
            "The result is a new factor over the remaining variables.")),

    heading3("Induced Width & Treewidth"),
    para(rt("Given elimination ordering "), eq(r"\pi"), rt(", the induced graph adds an edge between all variables that are "
            "simultaneously in the same factor at the time of elimination. The induced width "), eq(r"w_\pi"), rt(" is the "
            "maximum clique size minus 1. Treewidth:")),
    equation_block(r"w^* = \min_{\pi} w_\pi"),
    para(rt("VE complexity: "), eq(r"O(n \cdot k^{w^*+1})"), rt(" where "), eq(r"k"), rt(" = domain size. Finding optimal "), eq(r"\pi"), rt(" is NP-hard.")),

    heading3("BP Correctness on Trees (Proof Sketch)"),
    para(rt("Claim: on a tree factor graph, beliefs "), eq(r"b(x_i)"), rt(" equal the true marginals "), eq(r"p(x_i)"), rt(".")),
    para(rt("Proof by induction on the tree structure. Base case: leaf variable "), eq(r"X_\ell"), rt(" has one neighbor factor "), eq(r"f"), rt(". "
            "Its message "), eq(r"\mu_{X_\ell \to f}(x_\ell) = 1"), rt(" (uniform, no other neighbors). "
            "The factor message back integrates the local factor: "), eq(r"\mu_{f \to X_i}(x_i) = \sum_{x_\ell} f(x_i, x_\ell)"), rt(", "
            "which is exactly the marginal contribution of the subtree.")),
    para(rt("Inductive step: assume all messages from subtrees rooted at "), eq(r"f"), rt("'s children are exact marginals of their subtrees. "
            "Then "), eq(r"\mu_{f \to X_i}"), rt(" correctly marginalizes "), eq(r"f"), rt(" over all child subtrees by the definition of conditional independence in a tree. "
            "The product of all incoming messages at "), eq(r"X_i"), rt(" therefore equals "), eq(r"p(x_i)"), rt(". ∎")),

    heading3("Loopy BP & Bethe Free Energy"),
    para(rt("On graphs with cycles, running BP iteratively is equivalent to minimizing the "), rt("Bethe free energy", italic=True), rt(":")),
    equation_block(r"F_{\text{Bethe}} = \sum_s \sum_{\mathbf{x}_{C_s}} b_s(\mathbf{x}_{C_s}) \ln \frac{b_s(\mathbf{x}_{C_s})}{f_s(\mathbf{x}_{C_s})} - \sum_i (d_i-1)\sum_{x_i} b_i(x_i)\ln b_i(x_i)"),
    para(rt("where "), eq(r"d_i"), rt(" = degree of variable "), eq(r"X_i"), rt(". Fixed points of Loopy BP satisfy the stationarity conditions of this approximate free energy.")),

    callout("⚠️", rt("Warning: ", bold=True),
            rt("Loopy BP can cycle (no convergence guarantee), give overconfident beliefs (double-counting evidence along cycles), "
               "and produce inconsistent marginals. For guaranteed exact inference on loopy graphs, use the junction-tree algorithm.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch: Variable Elimination"),
    code_block("python", """\
import numpy as np
from itertools import product as iproduct

# Represent a factor as (tuple_of_variable_names, np.ndarray)
# Array axis order matches variable order in the tuple.

def factor_product(factors):
    \"\"\"Multiply a list of factors, returning (combined_vars, combined_table).\"\"\"
    if not factors:
        return ([], np.array([1.0]))
    # collect union of variables (preserving first-seen order)
    all_vars = list(dict.fromkeys(v for f in factors for v in f[0]))
    # compute total shape
    # (assume all variables are binary for simplicity; generalise via domain sizes)
    shape = [2] * len(all_vars)
    result = np.ones(shape)
    for (fvars, ftable) in factors:
        # expand ftable axes to align with all_vars
        expand_shape = [1] * len(all_vars)
        for i, v in enumerate(all_vars):
            if v in fvars:
                ax = fvars.index(v)
                expand_shape[i] = ftable.shape[ax]
        # find transpose to put axes in all_vars order
        axes = [fvars.index(v) for v in all_vars if v in fvars]
        ftable_T = ftable.transpose(
            [fvars.index(v) for v in all_vars if v in fvars]
        )
        # reshape for broadcasting
        new_shape = [ftable_T.shape[axes.index(i)] if all_vars[i] in fvars else 1
                     for i in range(len(all_vars))]
        result = result * ftable_T.reshape(
            [ftable.shape[fvars.index(v)] if v in fvars else 1 for v in all_vars]
        )
    return (all_vars, result)

def variable_elimination(factors, elim_order, query):
    \"\"\"
    Compute P(query) by eliminating variables in elim_order.
    factors: list of (var_tuple, np.ndarray)
    elim_order: list of variable names to eliminate
    query: name of query variable
    Returns: normalized np.array over query domain
    \"\"\"
    pool = list(factors)
    for X in elim_order:
        relevant = [f for f in pool if X in f[0]]
        pool     = [f for f in pool if X not in f[0]]
        if not relevant:
            continue
        joint_vars, joint_table = factor_product(relevant)
        # sum out X along its axis
        ax        = joint_vars.index(X)
        tau_table = joint_table.sum(axis=ax)
        tau_vars  = tuple(v for v in joint_vars if v != X)
        pool.append((tau_vars, tau_table))
    # multiply all remaining factors (should only mention query)
    _, result = factor_product(pool)
    result = result.ravel()
    return result / result.sum()   # normalize -> P(query)

# ── Example: 4-node chain ─────────────────────────────
phi1   = (('X1',), np.array([0.6, 0.4]))
phi12  = (('X1','X2'), np.array([[0.9,0.1],[0.2,0.8]]))
phi23  = (('X2','X3'), np.array([[0.7,0.3],[0.4,0.6]]))
phi34  = (('X3','X4'), np.array([[0.8,0.2],[0.3,0.7]]))

factors     = [phi1, phi12, phi23, phi34]
elim_order  = ['X1','X2','X3']
px4         = variable_elimination(factors, elim_order, 'X4')
print(f"P(X4=0) = {px4[0]:.4f}, P(X4=1) = {px4[1]:.4f}")
# → P(X4=0) = 0.5928, P(X4=1) = 0.4072
"""),

    heading3("6b — From Scratch: Belief Propagation on Tree"),
    code_block("python", """\
import numpy as np

def bp_chain(phi1, phi_pairs):
    \"\"\"
    Exact BP on a chain X1 - X2 - ... - Xn.
    phi1: prior over X1 as np.array shape (k,)
    phi_pairs: list of pairwise factors phi_{i,i+1} shape (k,k)
    Returns: list of marginal arrays, one per variable
    \"\"\"
    n = len(phi_pairs) + 1
    # Forward messages: mu_fwd[i] = message from X_i to X_{i+1} (size k)
    mu_fwd = [None] * n
    mu_fwd[0] = phi1.copy()  # leaf message = prior
    for i in range(n-1):
        # mu_fwd[i+1](x_{i+1}) = sum_{x_i} phi_{i,i+1}(x_i, x_{i+1}) * mu_fwd[i](x_i)
        mu_fwd[i+1] = phi_pairs[i].T @ mu_fwd[i]  # shape (k,)

    # Backward messages: mu_bwd[i] = message from X_i to X_{i-1}
    mu_bwd = [None] * n
    mu_bwd[n-1] = np.ones(phi1.shape[0])  # leaf (X_n) sends uniform
    for i in range(n-2, -1, -1):
        # mu_bwd[i](x_i) = sum_{x_{i+1}} phi_{i,i+1}(x_i,x_{i+1}) * mu_bwd[i+1](x_{i+1})
        mu_bwd[i] = phi_pairs[i] @ mu_bwd[i+1]

    # Beliefs = forward * backward, normalized
    beliefs = []
    for i in range(n):
        b = mu_fwd[i] * mu_bwd[i]
        beliefs.append(b / b.sum())
    return beliefs

phi1   = np.array([0.6, 0.4])
phi12  = np.array([[0.9,0.1],[0.2,0.8]])
phi23  = np.array([[0.7,0.3],[0.4,0.6]])
phi34  = np.array([[0.8,0.2],[0.3,0.7]])

beliefs = bp_chain(phi1, [phi12, phi23, phi34])
for i, b in enumerate(beliefs):
    print(f"P(X{i+1}=0) = {b[0]:.4f}, P(X{i+1}=1) = {b[1]:.4f}")
# All four marginals computed exactly in one pass.
"""),

    heading3("6c — Production: pgmpy Library"),
    code_block("python", """\
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination, BeliefPropagation

# Build network
model = BayesianNetwork([('X1','X2'),('X2','X3'),('X3','X4')])
cpd1  = TabularCPD('X1', 2, [[0.6],[0.4]])
cpd2  = TabularCPD('X2', 2, [[0.9,0.2],[0.1,0.8]], evidence=['X1'], evidence_card=[2])
cpd3  = TabularCPD('X3', 2, [[0.7,0.4],[0.3,0.6]], evidence=['X2'], evidence_card=[2])
cpd4  = TabularCPD('X4', 2, [[0.8,0.3],[0.2,0.7]], evidence=['X3'], evidence_card=[2])
model.add_cpds(cpd1, cpd2, cpd3, cpd4)
assert model.check_model()

# Variable Elimination — single query
ve   = VariableElimination(model)
q    = ve.query(['X4'], show_progress=False)
print(q)  # P(X4=0)≈0.5928, P(X4=1)≈0.4072

# Belief Propagation — all marginals
bp   = BeliefPropagation(model)
bp.calibrate()  # runs junction-tree message passing
m    = bp.query(['X1'], show_progress=False)
print(m)  # Should recover prior P(X1=0)=0.6
"""),
    divider(),

    # ── Section 7: Interview ───────────────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is Variable Elimination?", bold=True)], [
        para(rt("VE computes a marginal by eliminating one variable at a time: collect all factors mentioning the variable, multiply them, sum the variable out, and add the resulting factor back to the pool. Repeat until only the query variable remains; normalize.")),
        para(rt("Complexity: "), eq(r"O(n \cdot k^{w+1})"), rt(" where "), eq(r"k"), rt(" = domain size, "), eq(r"w"), rt(" = treewidth.")),
    ]),
    toggle([rt("Q2 (Easy): How does Belief Propagation differ from VE?", bold=True)], [
        para(rt("BP passes messages along factor-graph edges. On a tree, a two-pass schedule (leaves→root then root→leaves) yields all marginals simultaneously in "), eq(r"O(n\,k^2)"), rt(". VE computes one query; BP computes all. Both are algebraically equivalent — BP on the junction tree IS VE scheduled optimally.")),
    ]),
    toggle([rt("Q3 (Medium): What is treewidth and why does it matter?", bold=True)], [
        para(rt("Treewidth "), eq(r"w^*"), rt(" is the minimum over all elimination orderings of the maximum clique size minus 1 in the induced graph. It determines inference complexity: "), eq(r"O(n\,k^{w^*+1})"), rt(". For a chain/tree, "), eq(r"w^*=1"), rt("; for a grid, "), eq(r"w^* = O(\sqrt{n})"), rt("; for a complete graph, "), eq(r"w^*=n-1"), rt(". Finding the optimal ordering is NP-hard; heuristics like min-fill or min-degree are used.")),
    ]),
    toggle([rt("Q4 (Medium): Why is Loopy BP approximate?", bold=True)], [
        para(rt("On graphs with cycles, messages travel around loops, effectively counting evidence multiple times. A message from "), eq(r"X_j"), rt(" to "), eq(r"X_i"), rt(" should be independent of "), eq(r"X_i"), rt("'s own prior, but in a cycle, "), eq(r"X_i"), rt("'s belief influences "), eq(r"X_j"), rt(" which feeds back. Result: overconfident (under-dispersed) beliefs, no convergence guarantee.")),
    ]),
    toggle([rt("Q5 (Hard): Explain the Junction Tree algorithm.", bold=True)], [
        para(rt("Three steps: (1) Moralization + triangulation — add edges to make the graph chordal (every cycle of length ≥ 4 has a chord). (2) Identify maximal cliques and build a clique tree (junction tree) satisfying the running-intersection property. (3) Run BP on the clique tree — messages now carry joint distributions over cliques, not individual variables. Exact on any graph; cost "), eq(r"O(n\,k^{w^*+1})"), rt(".")),
    ]),
    toggle([rt("Q6 (Hard — PhD): Relate VE/BP to the sum-product semiring.", bold=True)], [
        para(rt("Both algorithms are instances of the sum-product algorithm on a commutative semiring "), eq(r"(\mathbb{R}_{\geq 0},+,\times)"), rt(". The semiring has additive identity 0 and multiplicative identity 1. Substituting "), eq(r"(\max, +)"), rt(" yields max-product / Viterbi (MAP inference). Substituting "), eq(r"(\text{any}, \times)"), rt(" with log-domain transforms gives the log-sum-exp (numerically stable) variant. The same message schedule works for any compatible semiring.")),
    ]),
    toggle([rt("Red Flags (Interviewer Perspective)", bold=True)], [
        bullet(rt("Saying BP is always exact — it's exact only on trees.")),
        bullet(rt("Confusing treewidth with number of nodes.")),
        bullet(rt("Claiming VE and BP are fundamentally different algorithms — they are the same computation.")),
        bullet(rt("Not knowing that finding the optimal elimination ordering is NP-hard.")),
    ]),
    divider(),

    # ── Section 8: Comparison ──────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Algorithm", "Graph Requirement", "Queries", "Complexity", "When to Use"]),
        table_row(["Variable Elimination", "Any (exact)", "One per run", "O(n·k^{w+1})", "Single query, small treewidth"]),
        table_row(["Belief Propagation", "Tree (exact)", "All marginals", "O(n·k^2)", "Tree / junction-tree, all marginals needed"]),
        table_row(["Loopy BP", "Any (approx)", "All marginals", "O(iter·n·k^2)", "Large loopy graphs, approximate OK"]),
        table_row(["MCMC (Gibbs/MH)", "Any (approx)", "Any query", "O(T·n)", "High treewidth, continuous vars"]),
        table_row(["Variational Inference", "Any (approx)", "Any query", "O(iter·n)", "Large-scale, differentiable models"]),
    ),
    callout("🎯", rt("Decision Rule: ", bold=True),
            rt("Use exact inference (VE/BP) when treewidth ≤ ~20 and the graph is known. "
               "Use Loopy BP for large sparse graphs where approximate is acceptable. "
               "Use MCMC / VI when the model is continuous or treewidth is too large.")),
    divider(),

    # ── Section 9: Explainer Embed ────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through Variable Elimination and Belief Propagation simultaneously on a 4-node chain — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Bayesian Networks — conditional independence, d-separation, CPDs.")),
    bullet(rt("Markov Random Fields / factor graphs — undirected graphical models.")),
    bullet(rt("Probability: marginalization, Bayes' theorem, joint distributions.")),
    heading3("What to Learn Next"),
    bullet(rt("Approximate Inference: MCMC (Gibbs sampling, Metropolis-Hastings).")),
    bullet(rt("Variational Inference: mean-field VI, ELBO, black-box VI.")),
    bullet(rt("Loopy Belief Propagation and convergence analysis.")),
    bullet(rt("Expectation Propagation (EP) — a refinement of BP for exponential families.")),
    heading3("Key Papers"),
    bullet(rt("Pearl, J. (1988). ", italic=True), rt('"Probabilistic Reasoning in Intelligent Systems." Morgan Kaufmann. — foundational BP.')),
    bullet(rt("Lauritzen & Spiegelhalter (1988). ", italic=True), rt('"Local Computations with Probabilities on Graphical Structures." JRSS-B. — junction tree.')),
    bullet(rt("Yedidia, Freeman & Weiss (2003). ", italic=True), rt('"Understanding Belief Propagation and Its Generalizations." — Bethe free energy connection.')),
    bullet(rt("Dechter, R. (1999). ", italic=True), rt('"Bucket Elimination: A Unifying Framework for Reasoning." AIJ. — VE formalization.')),
    heading3("Best Resources"),
    bullet(rt("Koller & Friedman, ", italic=True), rt('"Probabilistic Graphical Models" (2009), Chapters 9–10.')),
    bullet(rt("Bishop, PRML (2006), Chapter 8 — Graphical Models.")),
    bullet(rt("pgmpy library: https://pgmpy.org — production-grade PGM inference in Python.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
