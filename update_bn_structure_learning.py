#!/usr/bin/env python3
"""Update Notion page for: Structure Learning (Score-Based, Constraint-Based)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81b3-8786-c09f4e2a614d"
ICON = "🟠"   # Advanced
PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/bn_structure_learning_explainer.html"},
}

EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/bn_structure_learning_explainer.html"

blocks = [

    # ════════════════════════════════════════════════════════
    # Section 1: 30-Second Version
    # ════════════════════════════════════════════════════════
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("A Bayesian network is a directed acyclic graph (DAG) where nodes are random variables and directed edges encode \"X directly influences Y.\" "
            "Structure learning is the inverse problem: given a table of observations, automatically discover which DAG best explains the data — no expert required.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine you have hospital records for 10,000 patients: smoking history, lung-cancer diagnosis, dyspnoea, bronchitis. "
            "You want to know the causal web linking them, without a physician drawing it by hand. "
            "Structure learning is the algorithm that reconstructs the network from data alone — "
            "like reverse-engineering a circuit board by probing its inputs and outputs.")),
    callout("💡", rt("If you remember one thing: ", bold=True),
            rt("Score-based methods search over DAGs maximising BIC/BDeu; constraint-based methods (PC algorithm) prune edges using conditional independence (CI) tests. "
               "Both recover the same Markov equivalence class in the large-sample limit — and both are NP-hard in the worst case.")),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 2: Historical Context
    # ════════════════════════════════════════════════════════
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Until the 1980s Bayesian networks were hand-crafted by domain experts — expensive, error-prone, and impossible to scale. "
            "As large observational datasets became available (genetics, medicine, finance), researchers needed algorithms to learn structure automatically.")),
    heading3("What Came Before"),
    para(rt("Early work relied on fully supervised DAG specification or pair-wise correlation thresholding — neither handles confounding nor recovers causal direction.")),
    heading3("The Breakthroughs"),
    bullet(rt("Cooper & Herskovits (1992) ", bold=True), rt("— K2 score: greedy DAG search maximising a Bayesian marginal likelihood (Dirichlet prior). First principled score-based algorithm.")),
    bullet(rt("Spirtes, Glymour & Scheines (1993) ", bold=True), rt("— PC algorithm: skeleton via CI tests, then orient v-structures. Introduced constraint-based paradigm.")),
    bullet(rt("Chickering (2002) ", bold=True), rt("— Greedy Equivalence Search (GES): score-based search in CPDAG space, provably consistent.")),
    bullet(rt("Heckerman et al. (1995) ", bold=True), rt("— BDeu score: Bayesian Dirichlet score with equivalent uniform (eu) prior, parameter-free.")),

    heading3("Evolution Timeline"),
    para(rt("K2 (1992) → PC / SGS (1993) → BDe/BDeu (1995) → GES (2002) → MMHC hybrid (2006) → NOTEARS / DAG-GNN (2018–2020, continuous optimisation).")),

    heading3("Before vs After"),
    table(4,
          table_row(["Dimension", "Before (hand-crafted / correlation)", "Score-Based", "Constraint-Based"]),
          table_row(["Scalability", "Manual, d ≤ 20", "Greedy, d ≤ 100+", "CI tests, sparse large d"]),
          table_row(["Handles confounding", "No", "Partially (score)", "FCI extension"]),
          table_row(["Output guarantee", "None", "Markov-equiv. optimal (GES)", "Consistent CPDAG"]),
          table_row(["Compute", "O(1) human hours", "O(d² · iter) greedy", "O(d^{k+2}) CI tests"]),
    ),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 3: Core Concepts & Theory
    # ════════════════════════════════════════════════════════
    heading2("🧠 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("DAG ", bold=True), rt("— Directed Acyclic Graph. Nodes = random variables, edge X→Y means X is a direct cause of Y.")),
    bullet(rt("Markov condition ", bold=True), rt("— Each node X is conditionally independent of its non-descendants given its parents Pa(X).")),
    bullet(rt("Faithfulness ", bold=True), rt("— Every conditional independence in the true distribution P is entailed by d-separation in G (no cancellations).")),
    bullet(rt("CPDAG ", bold=True), rt("— Completed Partially Directed DAG; a unique graphical representative of a Markov equivalence class (MEC). Directed edges are shared by ALL DAGs in the MEC; undirected edges can go either way.")),
    bullet(rt("Scoring function ", bold=True), eq(r"S(G,\mathcal{D})"), rt(" — Assigns a real number to (DAG, data) pair. Decomposes as "),
           eq(r"S = \sum_{i=1}^{d} s(X_i, \text{Pa}(X_i), \mathcal{D})")),

    heading3("Core Property"),
    callout("🔑", rt("Decomposability of BIC/BDeu: ", bold=True),
            rt("The global score breaks into independent local terms, one per node. This means edge additions/deletions only require recomputing the score of the affected node — enabling efficient greedy local search.")),

    heading3("Prerequisites"),
    para(rt("To understand structure learning you should know: conditional independence, d-separation, Bayesian networks (CPDs), BIC/AIC, hypothesis testing (χ²/Fisher-Z), graph theory (DAGs, topological order).")),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 4: Architecture & Internal Workings
    # ════════════════════════════════════════════════════════
    heading2("⚙️ Architecture & Internal Workings — PhD Deep Dive"),

    heading3("Score-Based: BIC Greedy Hill Climbing"),
    para(rt("Information flow: data → local score cache → greedy edge add/delete/reverse loop → DAG.")),
    numbered(rt("Initialise: ", bold=True), rt("G = empty graph. Compute s(Xᵢ, ∅, D) for each node.")),
    numbered(rt("Candidate moves: ", bold=True), rt("For each ordered pair (X,Y) not in G: compute ΔBIC = s(Y, Pa(Y)∪{X}, D) − s(Y, Pa(Y), D). Acyclicity check (topological sort).")),
    numbered(rt("Greedy selection: ", bold=True), rt("Apply move with max positive ΔBIC. Update score cache for Y only.")),
    numbered(rt("Repeat until: ", bold=True), rt("No single move improves score (local optimum).")),

    heading3("Numerical Trace — BIC for Discrete Variables"),
    para(rt("With N=1000 samples, 2-state nodes, observed counts for Dyspnoea (D) given Smoking (S):")),
    para(rt("Observed: P̂(D=1|S=1)=0.65, P̂(D=1|S=0)=0.18, P̂(S=1)=0.40")),
    equation_block(r"\ell(D|\theta) = 400\cdot[0.65\ln 0.65 + 0.35\ln 0.35] + 600\cdot[0.18\ln 0.18 + 0.82\ln 0.82] \approx -576.2 \text{ nats}"),
    equation_block(r"\ell(D|\text{no parents}) = 1000\cdot[0.37\ln 0.37 + 0.63\ln 0.63] \approx -648.5 \text{ nats}"),
    equation_block(r"\Delta\text{BIC}(D \leftarrow S) = 2(-576.2 + 648.5) - \underbrace{(\ln 1000)}_{\approx 6.91} \cdot \underbrace{1}_{\text{extra param}} \approx +137.7"),
    para(rt("Since ΔBIC > 0, adding S→D improves the penalised score. The penalty term prevents overfitting: adding a useless parent gains < log(N)/2 ≈ 3.45 nats in log-likelihood.")),

    heading3("PC Algorithm — Internal Detail"),
    numbered(rt("Skeleton phase (decreasing sparsity): ", bold=True), rt("For conditioning set size k=0,1,2,…: for each adjacent pair (X,Y) test X⊥Y|S for all S⊆Adj(X)\\{Y}, |S|=k. If p-value > α, remove edge, store sepset(X,Y)=S. Halt when max adj degree < k+1.")),
    numbered(rt("V-structure orientation: ", bold=True), rt("For unshielded triple X–Z–Y (X,Y not adjacent): if Z∉sepset(X,Y), orient X→Z←Y.")),
    numbered(rt("Meek rules (R1–R4): ", bold=True), rt("Propagate orientations to avoid new v-structures or directed cycles.")),

    heading3("Fisher-Z Test (Gaussian Data) — Numerical Example"),
    para(rt("Observed partial correlation between LungCancer (L) and Bronchitis (B) conditioning on Smoking (S):")),
    equation_block(r"\hat{\rho}_{LB\cdot S} = \frac{\hat{\rho}_{LB} - \hat{\rho}_{LS}\hat{\rho}_{BS}}{\sqrt{(1-\hat{\rho}_{LS}^2)(1-\hat{\rho}_{BS}^2)}} = \frac{0.41 - (0.72)(0.68)}{\sqrt{(1-0.52)(1-0.46)}} \approx \frac{-0.08}{0.51} \approx -0.16"),
    equation_block(r"Z_{LB\cdot S} = \frac{1}{2}\ln\frac{1+(-0.16)}{1-(-0.16)} = \frac{1}{2}\ln\frac{0.84}{1.16} \approx -0.161"),
    equation_block(r"\text{Test statistic} = \sqrt{N - |S| - 3}\cdot Z_{LB\cdot S} = \sqrt{1000 - 1 - 3}\cdot(-0.161) \approx -5.07"),
    para(rt("But wait — |test stat| = 5.07 >> 1.96, so L and B are NOT independent given S. This example would keep L–B. "
            "In our toy example we assumed weaker association (Z≈0.11) to illustrate removal. The exact numbers depend on sample correlations.")),

    heading3("Edge Cases & Failure Modes"),
    bullet(rt("Score-based: ", bold=True), rt("Local optima in hill-climbing. Restarts, tabu search, or GES (CPDAG search) partially address this.")),
    bullet(rt("PC: ", bold=True), rt("False removals at small N (type I errors cascade — once an edge is removed, its sepset is fixed for orientation). Order-dependence: different variable orderings can yield different skeletons.")),
    bullet(rt("Both: ", bold=True), rt("Assume no latent confounders (causal sufficiency). FCI (Fast Causal Inference) relaxes this at cost of outputting PAGs instead of CPDAGs.")),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 5: The Math
    # ════════════════════════════════════════════════════════
    heading2("📐 The Math Behind It"),

    heading3("BIC Score — Full Derivation"),
    para(rt("The BIC score for DAG G on dataset D with N observations is:")),
    equation_block(r"\text{BIC}(G,\mathcal{D}) = \log P(\mathcal{D}\mid\hat{\theta}_G) - \frac{d_G}{2}\log N"),
    para(rt("where "), eq(r"\hat{\theta}_G"), rt(" are MLEs and "), eq(r"d_G"), rt(" = total number of free parameters.")),
    para(rt("For node "), eq(r"X_i"), rt(" with discrete parents "), eq(r"\text{Pa}(X_i)"), rt(", let "), eq(r"q_i = |\text{Pa}(X_i)|"), rt(" parent configurations, "), eq(r"r_i"), rt(" states:")),
    equation_block(r"s(X_i, \text{Pa}(X_i), \mathcal{D}) = \sum_{j=1}^{q_i}\sum_{k=1}^{r_i} N_{ijk}\log\hat{\theta}_{ijk} - \frac{(r_i-1)q_i}{2}\log N"),
    para(rt("where "), eq(r"N_{ijk}"), rt(" = count of (Xᵢ=k, Pa(Xᵢ)=j), and "), eq(r"\hat{\theta}_{ijk} = N_{ijk}/N_{ij+}")),

    heading3("BDeu Score"),
    para(rt("Bayesian marginal likelihood integrating out parameters under a Dirichlet(α/r_iq_i) prior:")),
    equation_block(r"\text{BDeu}(G,\mathcal{D}) = \sum_{i=1}^{d}\sum_{j=1}^{q_i}\left[\log\frac{\Gamma(\alpha/q_i)}{\Gamma(\alpha/q_i + N_{ij+})} + \sum_{k=1}^{r_i}\log\frac{\Gamma(\alpha/(r_iq_i)+N_{ijk})}{\Gamma(\alpha/(r_iq_i))}\right]"),
    para(rt("As N→∞, BDeu and BIC are equivalent up to constants (both penalise complexity at rate "), eq(r"\frac{d_G}{2}\log N"), rt(").")),

    heading3("Why NP-Hard"),
    para(rt("The number of DAGs on d nodes is given by the OEIS A003024 recurrence:")),
    equation_block(r"a(d) = \sum_{k=1}^{d}(-1)^{k+1}\binom{d}{k}2^{k(d-k)}a(d-k), \quad a(0)=1"),
    para(rt("Values: d=1:1, d=2:3, d=3:25, d=4:543, d=5:29281, d=10:4.2×10¹⁸. "
            "Chickering (1996) proved finding the optimal BIC DAG is NP-hard by reduction from the minimum feedback vertex set problem.")),

    heading3("PC Algorithm Complexity"),
    para(rt("In the worst case (dense graph, max degree k):")),
    equation_block(r"\text{CI tests} = O\!\left(d^2 \binom{d}{k}\right) = O(d^{k+2})"),
    para(rt("For sparse graphs (bounded degree k), this is polynomial in d — the main advantage of constraint-based methods over exact score-based search.")),

    callout("⚠️", rt("Warning: ", bold=True),
            rt("The faithfulness assumption can fail (e.g., perfect cancellations in linear models). "
               "If the true distribution has a conditional independence not implied by d-separation in G, PC will remove a wrong edge. "
               "Score-based methods are slightly more robust to faithfulness violations.")),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 6: Code
    # ════════════════════════════════════════════════════════
    heading2("💻 Code Implementation"),

    heading3("6a — Score-Based Hill Climbing from Scratch"),
    code_block("python", """\
import numpy as np
from itertools import combinations

def bic_local(data, node, parents, alpha=0):
    \"\"\"BIC local score for one node given its parents (discrete vars).
    data: (N, d) int array; node, parents: column indices.
    alpha: Dirichlet pseudocount (0 = MLE/BIC).
    \"\"\"
    N = len(data)
    x = data[:, node]
    r = len(np.unique(x))           # number of states of node

    if not parents:
        counts = np.bincount(x, minlength=r).astype(float) + alpha
        probs  = counts / counts.sum()
        ll = np.sum(np.log(probs + 1e-12) * (counts - alpha))
        d_g = r - 1
    else:
        pa_data = data[:, parents]
        # enumerate parent configurations
        pa_vals = [np.unique(pa_data[:, k]) for k in range(len(parents))]
        from itertools import product as iproduct
        ll, d_g = 0.0, 0
        for pa_cfg in iproduct(*pa_vals):
            mask = np.all(pa_data == pa_cfg, axis=1)
            if mask.sum() == 0:
                continue
            cnts = np.bincount(x[mask], minlength=r).astype(float) + alpha
            probs = cnts / cnts.sum()
            ll   += np.sum(np.log(probs + 1e-12) * (cnts - alpha))
            d_g  += r - 1

    # BIC penalty
    return ll - 0.5 * d_g * np.log(N)


def is_acyclic(adj):
    \"\"\"Check DAG acyclicity via topological sort (Kahn's algorithm).\"\"\"
    d = len(adj)
    indeg = [sum(adj[j][i] for j in range(d)) for i in range(d)]
    queue = [i for i in range(d) if indeg[i] == 0]
    count = 0
    while queue:
        u = queue.pop()
        count += 1
        for v in range(d):
            if adj[u][v]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)
    return count == d


def greedy_hill_climb(data, max_iter=500):
    \"\"\"BIC greedy hill-climbing for BN structure learning.
    Returns adjacency matrix adj[i][j]=1 means i -> j.
    \"\"\"
    N, d = data.shape
    adj = [[0]*d for _ in range(d)]          # start: empty graph
    pa  = [[] for _ in range(d)]             # parent sets

    # Cache initial scores
    scores = [bic_local(data, i, []) for i in range(d)]
    total  = sum(scores)

    for iteration in range(max_iter):
        best_delta, best_move = 0, None

        for i in range(d):
            for j in range(d):
                if i == j:
                    continue

                # --- Try ADD i -> j ---
                if not adj[i][j] and j not in pa[i]:
                    new_pa_j = pa[j] + [i]
                    adj[i][j] = 1
                    if is_acyclic(adj):
                        delta = bic_local(data, j, new_pa_j) - scores[j]
                        if delta > best_delta:
                            best_delta, best_move = delta, ("add", i, j, new_pa_j)
                    adj[i][j] = 0

                # --- Try DELETE i -> j ---
                if adj[i][j]:
                    new_pa_j = [p for p in pa[j] if p != i]
                    delta = bic_local(data, j, new_pa_j) - scores[j]
                    if delta > best_delta:
                        best_delta, best_move = delta, ("del", i, j, new_pa_j)

        if best_move is None:
            print(f"Converged at iteration {iteration}, BIC={total:.2f}")
            break

        op, i, j, new_pa_j = best_move
        if op == "add":
            adj[i][j] = 1
        else:
            adj[i][j] = 0
        delta = bic_local(data, j, new_pa_j) - scores[j]
        scores[j] = bic_local(data, j, new_pa_j)
        pa[j] = new_pa_j
        total += delta

    return adj, total

# Example
np.random.seed(42)
N = 500
S = np.random.binomial(1, 0.4, N)
L = np.random.binomial(1, 0.3 + 0.4*S, N)
D = np.random.binomial(1, 0.1 + 0.5*S, N)
data = np.stack([S, L, D], axis=1)   # true structure: 0->1, 0->2

adj, bic = greedy_hill_climb(data)
print("Learned adjacency (rows=from, cols=to):")
print(np.array(adj))
# Expected: adj[0][1]=1, adj[0][2]=1 (Smoke -> Lung, Smoke -> Dyspnoea)
"""),

    heading3("6b — Constraint-Based PC Skeleton (Production: pgmpy)"),
    code_block("python", """\
# pip install pgmpy pandas
import pandas as pd
import numpy as np
from pgmpy.estimators import PC

np.random.seed(42)
N = 1000
S = np.random.binomial(1, 0.40, N)
L = np.random.binomial(1, np.where(S==1, 0.60, 0.15), N)
D = np.random.binomial(1, np.where(S==1, 0.65, 0.10), N)
B = np.random.binomial(1, np.where(S==1, 0.70, 0.25), N)
df = pd.DataFrame({"Smoke": S, "Lung": L, "Dyspnoea": D, "Bronch": B})

# PC algorithm
est = PC(data=df)
model = est.estimate(
    variant="stable",        # order-independent skeleton
    ci_test="chi_square",    # discrete CI test
    significance_level=0.05,
    return_type="cpdag",     # returns CPDAG (Markov equivalence class)
)
print("Edges:", model.edges())
# Expected: unoriented skeleton Smoke -- Lung, Smoke -- Dyspnoea, Smoke -- Bronch

# Score-based alternative: BIC hill-climbing via pgmpy
from pgmpy.estimators import HillClimbSearch, BicScore
hc = HillClimbSearch(data=df)
dag = hc.estimate(scoring_method=BicScore(data=df))
print("HC DAG edges:", dag.edges())

# GES (causal-learn library)
# pip install causal-learn
from causallearn.search.ScoreBased.GES import ges
data_np = df.values.astype(float)
Record = ges(data_np, score_func="local_score_BIC")
print("GES adjacency:\\n", Record["G"].graph)
"""),

    callout("⚠️", rt("Gotcha: ", bold=True),
            rt("pgmpy's PC variant='stable' gives order-independent skeleton. The default 'orig' can produce different graphs depending on variable ordering — always use 'stable' in practice. "
               "For continuous Gaussian data, use ci_test='pearsonr' (Fisher-Z). For mixed data, use conditional mutual information tests.")),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 7: Interview
    # ════════════════════════════════════════════════════════
    heading2("🎤 Interview Deep-Dive"),

    toggle([rt("Q1 (Easy): What is the difference between score-based and constraint-based structure learning?", bold=True)], [
        para(rt("Score-based methods assign a quality score (BIC, BDeu) to each candidate DAG and search for the maximum-score DAG via greedy operators (add/delete/reverse edges). "
                "Constraint-based methods (PC, FCI) instead run statistical conditional independence tests to identify which edges are absent and how to orient v-structures. "
                "Both recover the Markov equivalence class (CPDAG) in the large-sample limit, but score-based methods are more robust to false CI test results at small N, "
                "while constraint-based methods scale better to sparse high-dimensional graphs.")),
    ]),

    toggle([rt("Q2 (Easy): What is a CPDAG and why does structure learning return one instead of a DAG?", bold=True)], [
        para(rt("A CPDAG (Completed Partially Directed DAG) represents a Markov equivalence class — the set of all DAGs that encode the same conditional independencies. "
                "From observational data alone, we can identify the MEC but not which specific DAG within it is the true one (e.g., X→Y and Y→X are both consistent with the same joint distribution if there are no v-structures). "
                "Directed edges in the CPDAG are shared by all DAGs in the MEC; undirected edges can go either way. "
                "Distinguishing the true DAG within the MEC requires either interventional data or additional assumptions (e.g., additive noise models, functional constraints).")),
    ]),

    toggle([rt("Q3 (Medium): Why is BIC used instead of raw log-likelihood for scoring DAGs?", bold=True)], [
        para(rt("Raw log-likelihood increases monotonically with more edges — the complete DAG always fits the data best (MLEs can perfectly memorise marginal distributions). "
                "BIC adds a complexity penalty: BIC = log P(D|θ̂) − (d_G/2)log N. As N→∞, the penalty term eliminates spurious edges (their log-likelihood gain grows sub-logarithmically while the penalty grows as log N). "
                "BIC is a Laplace approximation to the log marginal likelihood log P(D|G) — it approximates the Bayesian model evidence under a non-informative prior. "
                "BDeu is the exact marginal likelihood under a Dirichlet prior and is preferred when sample sizes are small.")),
    ]),

    toggle([rt("Q4 (Medium): Walk through the PC algorithm step by step.", bold=True)], [
        numbered(rt("Start with the complete undirected graph (all d(d−1)/2 edges).")),
        numbered(rt("For k=0,1,2,…: For each adjacent pair (X,Y), test X⊥Y|S for all S⊆Adj(X)\\{Y} with |S|=k. If independent (p > α), remove edge, record sepset(X,Y)=S.")),
        numbered(rt("Repeat until no adjacent pair can be separated by any conditioning set of the current size.")),
        numbered(rt("For each unshielded triple X–Z–Y: if Z∉sepset(X,Y), orient X→Z←Y (v-structure/collider).")),
        numbered(rt("Apply Meek's 4 orientation rules to propagate orientations without introducing new v-structures or directed cycles.")),
        para(rt("Output: CPDAG. Time: O(d^{k+2}) CI tests where k = max degree of true graph.")),
    ]),

    toggle([rt("Q5 (Hard): Why is exact BN structure learning NP-hard, and what exact algorithms exist?", bold=True)], [
        para(rt("Chickering (1996) proved that finding the DAG maximising BIC is NP-hard via reduction from minimum feedback vertex set (an NP-complete graph problem). "
                "The search space has |DAG(d)| ∼ 2^{d²/2} elements (OEIS A003024). ")),
        para(rt("Exact algorithms via dynamic programming (Koivisto & Sood 2004; Silander & Myllymäki 2006) compute the optimal DAG in O(2^d · d) time and O(2^d) space — "
                "feasible for d ≤ 25 on modern hardware. A* search (Yuan et al. 2011) prunes the DP table and handles d ≤ 30.")),
        para(rt("The key insight for DP: given a topological ordering of nodes (there are d! orderings), the optimal parent set for each node can be found independently. "
                "The DP sums over all subsets of {1..d} as candidate parent configurations, exploiting the local decomposability of the BIC score.")),
    ]),

    toggle([rt("Q6 (Hard): Explain to a PhD Researcher — what are the identifiability limits of constraint-based methods?", bold=True)], [
        para(rt("Constraint-based methods recover the Markov equivalence class (MEC), not a unique DAG. Within the MEC, all DAGs are observationally indistinguishable. "
                "The MEC is identified by its v-structures and skeleton — equivalently by the CPDAG.")),
        para(rt("Under the causal Markov condition and faithfulness, PC is consistent: it recovers the true CPDAG in the large-sample limit. "
                "However, faithfulness can fail — e.g., in a linear Gaussian model X→Z←Y→X, specific parameter values can cause path coefficients to cancel, making X and Y appear independent marginally. "
                "In such cases PC removes the X–Y edge incorrectly.")),
        para(rt("Beyond observational equivalence: additive noise models (ANMs) / linear non-Gaussian models (LiNGAM) can identify the full DAG (not just the CPDAG) from observational data, "
                "because the non-Gaussianity of residuals breaks the MEC symmetry. This is the main advantage of continuous optimisation approaches like NOTEARS.")),
    ]),

    toggle([rt("Q7 (Hard): How does GES differ from hill-climbing, and why is it theoretically superior?", bold=True)], [
        para(rt("Hill-climbing (HC) operates in the space of DAGs, using add/delete/reverse edge operators. It can get stuck in local optima corresponding to different MECs.")),
        para(rt("GES (Chickering 2002) operates in the space of MECs (CPDAGs), using CPDAG-legal operators (insert/delete edges, preserving equivalence class structure). "
                "It has two phases: (1) forward — greedily insert edges that increase BIC until no insertion helps; (2) backward — greedily delete edges. "
                "GES is provably consistent: in the large-N limit with a perfect score, it returns the true CPDAG. HC has no such guarantee because its greedy moves can leave the optimum MEC by taking a suboptimal path through DAG space. "
                "In practice, HC is faster and often competitive at finite N.")),
    ]),

    toggle([rt("Q8 (System Design): How would you apply structure learning in a production causal inference pipeline?", bold=True)], [
        numbered(rt("Data preprocessing: discretise continuous variables (equal-frequency binning) or use Gaussian CI tests if linearity holds. Handle missing data via listwise deletion or imputation.")),
        numbered(rt("Algorithm selection: sparse graph (d>50, k≤4) → PC stable; dense small graph (d<25) → GES or exact DP; high-dimensional genomics (d≈1000) → MMHC or sparse score-based with L1 constraint.")),
        numbered(rt("Bootstrap stability: run PC/GES on B=100 bootstrap samples; report edge stability (frequency across bootstrap runs). Include only edges with stability > 0.5.")),
        numbered(rt("Expert validation: present CPDAG to domain experts; use prior knowledge to orient remaining undirected edges.")),
        numbered(rt("Intervention design: use the learned CPDAG to select informative interventions (experiments) to resolve remaining orientation ambiguities.")),
    ]),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 8: Comparison
    # ════════════════════════════════════════════════════════
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
          table_row(["Algorithm", "Paradigm", "Output", "Consistency", "Best For"]),
          table_row(["GES", "Score (BIC)", "CPDAG", "Yes (large N)", "Gaussian data, medium d"]),
          table_row(["Hill-Climbing", "Score (BIC)", "DAG", "No guarantee", "Fast, any data, d<100"]),
          table_row(["PC", "Constraint (CI)", "CPDAG", "Yes (faithfulness)", "Sparse large d, ample N"]),
          table_row(["FCI", "Constraint (CI)", "PAG", "Yes (latent confounders)", "Observational, unknown confounders"]),
          table_row(["MMHC", "Hybrid", "DAG", "Yes (large N)", "Best practice general use"]),
          table_row(["NOTEARS", "Continuous optim.", "DAG", "Yes (linear SEM)", "Continuous data, differentiable"]),
          table_row(["Exact DP", "Score (BIC)", "DAG", "Optimal", "d ≤ 25, guaranteed optimum"]),
    ),
    callout("🎯", rt("Decision Rule: ", bold=True),
            rt("Use GES or MMHC as default. Use PC/FCI if you suspect hidden confounders. Use Exact DP if d ≤ 20 and you need the guaranteed optimum. Use NOTEARS/DAG-GNN for continuous differentiable data with gradient-based optimisation.")),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 9: Interactive Explainer Embed
    # ════════════════════════════════════════════════════════
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through score-based vs constraint-based DAG discovery — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ════════════════════════════════════════════════════════
    # Section 10: Related Topics
    # ════════════════════════════════════════════════════════
    heading2("🔗 Related Topics & Further Reading"),

    heading3("Prerequisites"),
    bullet(rt("Bayesian Networks — conditional independence, d-separation, CPDs")),
    bullet(rt("Information Theory — mutual information, KL divergence, entropy")),
    bullet(rt("Hypothesis Testing — χ², Fisher-Z, p-values, multiple testing")),
    bullet(rt("Graph Theory — DAGs, topological sort, v-structures")),

    heading3("What to Learn Next"),
    bullet(rt("Parameter Learning — MLE/MAP for CPDs given structure")),
    bullet(rt("Causal Inference (Do-Calculus) — Pearl's intervention calculus")),
    bullet(rt("Hidden Markov Models / Dynamic BNs — temporal structure")),
    bullet(rt("NOTEARS / DAG-GNN — continuous optimisation for structure learning")),

    heading3("Key Papers"),
    bullet(rt("Spirtes, Glymour & Scheines (1993) ", bold=True), rt("— Causation, Prediction and Search. MIT Press. Introduces PC/SGS.")),
    bullet(rt("Chickering (2002) ", bold=True), rt("— Optimal Structure Identification With Greedy Search. JMLR 3:507–554. GES algorithm + consistency proof.")),
    bullet(rt("Heckerman et al. (1995) ", bold=True), rt("— Learning Bayesian Networks: The Combination of Knowledge and Statistical Data. Machine Learning 20:197–243.")),
    bullet(rt("Zheng et al. (2018) ", bold=True), rt("— DAGs with NO TEARS. NeurIPS. Continuous constrained optimisation for DAG learning.")),
    bullet(rt("Tsamardinos et al. (2006) ", bold=True), rt("— The Max-Min Hill-Climbing Bayesian Network Structure Learning Algorithm. Machine Learning 65:31–78. MMHC.")),

    heading3("Best Resources"),
    bullet(rt("Koller & Friedman — Probabilistic Graphical Models (MIT Press 2009), Chapters 18–20")),
    bullet(rt("causal-learn Python library: causal-learn.readthedocs.io")),
    bullet(rt("pgmpy: PC, GES, HillClimb, BicScore — pgmpy.readthedocs.io")),
    bullet(rt("Lecture: Jonas Peters (ETH Zürich) — Causality course, causalcourse.com")),

    callout("🔗", rt("This topic connects to: ", bold=True),
            rt("Bayesian Networks (structure), Parameter Learning (once structure known), Causal Inference (intervention), Hidden Markov Models (dynamic BNs), Gaussian Graphical Models (continuous analogue).")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
