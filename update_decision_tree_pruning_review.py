#!/usr/bin/env python3
"""Update Notion page for: Pre-pruning & Post-pruning (Cost-Complexity) — Decision Tree Pruning"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8108-93d3-d7a98ecae88f"
ICON = "🟡"  # Intermediate
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/decision_tree_pruning_review_explainer.html"},
}

blocks = [
    # ── Section 1: 30-Second Version ──
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("A decision tree grown without constraints memorises training data — every leaf holds one or two samples. Pruning controls how much the tree grows. Two strategies exist: pre-pruning stops growth early via hard thresholds; post-pruning grows the full tree then collapses the weakest subtrees.")),
    heading3("Real-World Analogy"),
    para(rt("Pre-pruning: telling a sculptor 'stop after 5 chisels per session.' Post-pruning: letting the sculptor finish, then removing every detail whose visual impact is smaller than the effort to carve it. Both produce a cleaner statue — they just intervene at different times.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Pre-pruning stops growth early via hard constraints (max_depth, min_samples_split). Post-pruning grows fully then collapses subtrees whose per-leaf error gain is less than a regularisation constant "), eq(r"\alpha"), rt(". Cross-validation selects the optimal "), eq(r"\alpha^*"), rt(".")),
    divider(),

    # ── Section 2: Historical Context ──
    heading2("📜 Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Early decision tree algorithms (ID3, 1979; C4.5, 1993; CART, 1984) produced trees that fit training data perfectly — a phenomenon Quinlan called 'overfitting'. A depth-10 binary tree has up to 1024 leaves; with limited training data each leaf holds one example and has 0% training error, 50%+ test error.")),
    heading3("Key Papers"),
    bullet(rt("Breiman, Friedman, Olshen, Stone — ", bold=True), rt("Classification and Regression Trees (CART), 1984. Introduced cost-complexity pruning as a principled regularisation framework.")),
    bullet(rt("Quinlan — ", bold=True), rt("C4.5: Programs for Machine Learning, 1993. Introduced error-based pruning as a post-pruning alternative.")),
    bullet(rt("Mingers (1987) — ", bold=True), rt("An empirical comparison of pruning methods for decision tree induction. Machine Learning. Early systematic evaluation.")),
    heading3("Evolution"),
    para(rt("1979: ID3 (no pruning) → 1984: CART (cost-complexity post-pruning) → 1986: Reduced Error Pruning → 1993: C4.5 error-based pruning → 1990s: Pre-pruning hyperparameters become standard (sklearn defaults today).")),
    table(4,
        table_row(["Dimension", "No Pruning", "Pre-Pruning", "Post-Pruning (CC)"]),
        table_row(["When to intervene", "Never", "During growth", "After full build"]),
        table_row(["Overfitting control", "None", "Hard thresholds", "Penalty parameter α"]),
        table_row(["Computation", "O(n log n) per split", "Same, stops early", "Full tree + pruning pass"]),
        table_row(["Flexibility", "Max (bad)", "Limited by greedy choices", "Global view; can keep deep sparse subtrees"]),
        table_row(["Tuning complexity", "None", "Interpretable hyperparams", "Single α; needs CV"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ──
    heading2("📐 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Node "), eq(r"t"), rt(": a decision point in the tree. Contains "), eq(r"|t|"), rt(" training samples.")),
    bullet(rt("Leaf "), eq(r"\ell"), rt(": terminal node; its prediction is the majority class (classification) or mean (regression).")),
    bullet(rt("Impurity "), eq(r"i(t)"), rt(": Gini = "), eq(r"1 - \sum_k p_k^2"), rt(" or Entropy = "), eq(r"-\sum_k p_k \log p_k"), rt(", where "), eq(r"p_k"), rt(" = fraction of class "), eq(r"k"), rt(" at node "), eq(r"t"), rt(".")),
    bullet(rt("Resubstitution error "), eq(r"R(T)"), rt(" = weighted sum of leaf errors: "), eq(r"\sum_{\ell \in \tilde{T}} p(\ell)\,e(\ell)"), rt(", where "), eq(r"p(\ell)"), rt(" = fraction of samples reaching leaf "), eq(r"\ell"), rt(" and "), eq(r"e(\ell)"), rt(" = leaf error rate.")),
    callout("📌", rt("Key Property: ", bold=True), rt("Cost-complexity pruning guarantees a nested sequence of trees "), eq(r"T_0 \supset T_1 \supset \cdots \supset \{t_1\}"), rt(" (root). Each step minimises "), eq(r"R_\alpha(T)"), rt(" for its alpha range — no combinatorial search needed.")),
    divider(),

    # ── Section 4: PhD Architecture Deep-Dive ──
    heading2("🔬 Architecture & Internal Workings"),
    heading3("Pre-Pruning: Parameter-by-Parameter"),
    para(rt("Pre-pruning wraps the tree-growing algorithm with stopping conditions checked before each split.")),
    heading3("max_depth"),
    para(rt("A node at depth "), eq(r"d = \texttt{max\_depth}"), rt(" becomes a leaf immediately. Effect: a balanced binary tree of depth "), eq(r"d"), rt(" has "), eq(r"2^d"), rt(" leaves; "), rt("max_depth=5"), rt(" caps at 32 leaves. Reduces model complexity exponentially.")),
    heading3("min_samples_split"),
    para(rt("Node "), eq(r"t"), rt(" is split only if "), eq(r"|t| \geq n_{\min}"), rt(". Guards against learning from statistically insignificant groups. Typical defaults: sklearn uses 2 (no guard), practitioners often use 10–20.")),
    heading3("min_impurity_decrease (δ)"),
    para(rt("A split is allowed only if the weighted impurity decrease exceeds "), eq(r"\delta"), rt(":")),
    equation_block(r"\Delta i(t) = i(t) - \frac{|t_L|}{|t|}\,i(t_L) - \frac{|t_R|}{|t|}\,i(t_R) \geq \delta"),
    heading3("Post-Pruning: Cost-Complexity (CART Algorithm)"),
    para(rt("Step 1: Grow the full tree "), eq(r"T_0"), rt(" (with only leaf purity as stopping condition, or tiny min_samples_leaf).")),
    para(rt("Step 2: For each internal node "), eq(r"t"), rt(", compute the effective pruning threshold:")),
    equation_block(r"\alpha_{\text{eff}}(t) = \frac{R(t) - R(T_t)}{|\tilde{T}_t| - 1}"),
    para(rt("where "), eq(r"R(t)"), rt(" = error if "), eq(r"t"), rt(" were a leaf, "), eq(r"R(T_t)"), rt(" = error of the full subtree rooted at "), eq(r"t"), rt(", "), eq(r"|\tilde{T}_t|"), rt(" = number of leaves in "), eq(r"T_t"), rt(". The denominator counts leaves removed by pruning.")),
    para(rt("Step 3: Prune the node with smallest "), eq(r"\alpha_{\text{eff}}"), rt(" to get "), eq(r"T_1"), rt(". Repeat to build the sequence "), eq(r"T_0 \supset T_1 \supset \cdots \supset T_k"), rt(".")),
    para(rt("Step 4: CV each "), eq(r"T_i"), rt(" on held-out data; select "), eq(r"T^*"), rt(" = best generalisation.")),
    heading3("Numerical Trace"),
    para(rt("Suppose a subtree "), eq(r"T_{n3}"), rt(" has 2 leaves. Leaf errors: "), eq(r"e(L_1) = 0.05,\; e(L_2) = 0.08"), rt(". Sample fractions: "), eq(r"p(L_1) = 0.14,\; p(L_2) = 0.14"), rt(". Error of subtree:")),
    equation_block(r"R(T_{n3}) = 0.14 \times 0.05 + 0.14 \times 0.08 = 0.0070 + 0.0112 = 0.0182"),
    para(rt("Error of node "), eq(r"n3"), rt(" as a leaf (error rate 10%, fraction 28%): "), eq(r"R(n3) = 0.28 \times 0.10 = 0.0280"), rt(". Effective alpha:")),
    equation_block(r"\alpha_{\text{eff}}(n3) = \frac{0.0280 - 0.0182}{2 - 1} = \frac{0.0098}{1} = 0.0098"),
    para(rt("This is the smallest "), eq(r"\alpha_{\text{eff}}"), rt(" in the tree — prune "), eq(r"n3"), rt(" first. If a competing node has "), eq(r"\alpha_{\text{eff}} = 0.0240"), rt(", it is pruned in the next step.")),
    divider(),

    # ── Section 5: Math ──
    heading2("📐 The Math Behind It"),
    heading3("Cost-Complexity Criterion"),
    para(rt("Define the cost-complexity of tree "), eq(r"T"), rt(" with regularisation parameter "), eq(r"\alpha \geq 0"), rt(":")),
    equation_block(r"R_\alpha(T) = R(T) + \alpha\,|\tilde{T}|"),
    para(rt("where "), eq(r"|\tilde{T}|"), rt(" is the number of leaves. As "), eq(r"\alpha"), rt(" increases, smaller trees (fewer leaves) are preferred.")),
    heading3("Optimal Subtree Property"),
    para(rt("For any "), eq(r"\alpha"), rt(", there exists a unique smallest optimal subtree "), eq(r"T(\alpha) \subseteq T_0"), rt(" that minimises "), eq(r"R_\alpha(T)"), rt(". Breiman et al. (1984) proved this via the following: if "), eq(r"T_1, T_2"), rt(" both minimise "), eq(r"R_\alpha"), rt(" then their intersection also minimises it — so a unique minimal element exists.")),
    heading3("Effective Alpha Derivation"),
    para(rt("At what "), eq(r"\alpha"), rt(" does pruning subtree "), eq(r"T_t"), rt(" become beneficial? We need "), eq(r"R_\alpha(\text{pruned}) \leq R_\alpha(\text{original})"), rt(":")),
    equation_block(r"R(t) + \alpha \cdot 1 \leq R(T_t) + \alpha\,|\tilde{T}_t|"),
    equation_block(r"R(t) - R(T_t) \leq \alpha\,(|\tilde{T}_t| - 1)"),
    equation_block(r"\alpha \geq \frac{R(t) - R(T_t)}{|\tilde{T}_t| - 1} = \alpha_{\text{eff}}(t)"),
    para(rt("So for any "), eq(r"\alpha \geq \alpha_{\text{eff}}(t)"), rt(", pruning "), eq(r"T_t"), rt(" at "), eq(r"t"), rt(" reduces "), eq(r"R_\alpha"), rt(". The greedy algorithm prunes the node with the smallest "), eq(r"\alpha_{\text{eff}}"), rt(" at each step, producing the sequence of optimal subtrees.")),
    heading3("Impurity Decrease Derivation (Pre-pruning)"),
    para(rt("For the Gini criterion, the impurity decrease for a split "), eq(r"s"), rt(" at node "), eq(r"t"), rt(":")),
    equation_block(r"\Delta i(s, t) = i(t) - p_L\,i(t_L) - p_R\,i(t_R), \quad p_L = \frac{|t_L|}{|t|}, \; p_R = \frac{|t_R|}{|t|}"),
    para(rt("For Gini: "), eq(r"i(t) = 1 - \sum_k \hat{p}_k^2"), rt(". For entropy: "), eq(r"i(t) = -\sum_k \hat{p}_k \log_2 \hat{p}_k"), rt(". The split is blocked if "), eq(r"\Delta i(s, t) < \delta"), rt(".")),
    callout("⚠️", rt("Common Misconception: ", bold=True), rt("The cost-complexity criterion R(T) uses resubstitution (training) error, NOT CV error. CV is used only to select among the sequence of trees T0 ⊃ T1 ⊃ … produced by the pruning algorithm. Do not confuse the pruning criterion with the model selection criterion.")),
    divider(),

    # ── Section 6: Code ──
    heading2("💻 Code Implementation"),
    heading3("6a — Pre-Pruning (sklearn)"),
    code_block("python", """\
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
import numpy as np

X, y = make_classification(n_samples=300, n_features=10, random_state=42)

# Pre-pruning: stop early via hard constraints
clf_pre = DecisionTreeClassifier(
    max_depth=4,              # max levels from root to leaf
    min_samples_split=20,     # split only if node has >= 20 samples
    min_impurity_decrease=0.01,  # split only if Gini gain >= delta
    random_state=42
)
clf_pre.fit(X, y)
print("Pre-pruned leaves:", clf_pre.get_n_leaves())  # e.g., 12
print("Pre-pruned depth:", clf_pre.get_depth())
"""),
    heading3("6b — Post-Pruning via Cost-Complexity (sklearn)"),
    code_block("python", """\
# Step 1: Get the pruning path (all candidate alphas)
full_tree = DecisionTreeClassifier(random_state=42)
path = full_tree.cost_complexity_pruning_path(X, y)
ccp_alphas = path.ccp_alphas[:-1]  # drop last: collapses to root

# Step 2: CV over alpha values
best_alpha, best_score = 0, 0
for alpha in ccp_alphas:
    clf = DecisionTreeClassifier(ccp_alpha=alpha, random_state=42)
    score = cross_val_score(clf, X, y, cv=5, scoring='accuracy').mean()
    if score > best_score:
        best_score, best_alpha = score, alpha

# Step 3: Retrain with best alpha
clf_post = DecisionTreeClassifier(ccp_alpha=best_alpha, random_state=42)
clf_post.fit(X, y)
print(f"Best alpha: {best_alpha:.4f}")
print(f"Post-pruned leaves: {clf_post.get_n_leaves()}")
print(f"CV accuracy: {best_score:.4f}")
"""),
    heading3("6c — From Scratch: Effective Alpha Computation"),
    code_block("python", """\
import numpy as np

def effective_alpha(tree, node_id, X, y):
    \"\"\"Compute alpha_eff for a given internal node.
    Uses the sklearn tree structure attributes.\"\"\"
    left = tree.children_left[node_id]
    right = tree.children_right[node_id]
    n_total = tree.n_node_samples[0]

    # R(t): resubstitution error if node_id were a leaf
    p_t = tree.n_node_samples[node_id] / n_total
    e_t = 1.0 - tree.value[node_id][0].max() / tree.n_node_samples[node_id]
    R_t = p_t * e_t

    # R(T_t): error of the subtree (sum over leaves in subtree)
    def subtree_error(nid):
        l, r = tree.children_left[nid], tree.children_right[nid]
        if l == -1:  # leaf
            p_l = tree.n_node_samples[nid] / n_total
            e_l = 1.0 - tree.value[nid][0].max() / tree.n_node_samples[nid]
            return p_l * e_l, 1
        err_l, nl = subtree_error(l)
        err_r, nr = subtree_error(r)
        return err_l + err_r, nl + nr

    R_Tt, n_leaves = subtree_error(node_id)
    if n_leaves <= 1:
        return float('inf')  # leaf: can't prune further
    return (R_t - R_Tt) / (n_leaves - 1)

# Usage:
clf_full = DecisionTreeClassifier(random_state=42).fit(X, y)
t = clf_full.tree_
for nid in range(t.node_count):
    if t.children_left[nid] != -1:  # internal node
        alpha = effective_alpha(t, nid, X, y)
        print(f"Node {nid}: alpha_eff = {alpha:.4f}")
"""),
    divider(),

    # ── Section 7: Interview Deep-Dive ──
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy): What is the difference between pre-pruning and post-pruning?"),
    para(rt("Pre-pruning imposes constraints during tree growth (max_depth, min_samples_split) that prevent overly specific splits from being created. Post-pruning (e.g., cost-complexity pruning) first grows the full tree, then systematically removes subtrees whose complexity cost outweighs their accuracy gain. Pre-pruning is faster; post-pruning can produce globally better trees.")),
    heading3("Q2 (Easy): What happens to a decision tree if you set max_depth=1?"),
    para(rt("The tree becomes a 'decision stump' — a single split with two leaves. Maximum simplicity, minimum capacity. Useful as a weak learner in boosting (AdaBoost uses stumps), but too simple for most standalone tasks.")),
    heading3("Q3 (Medium): How does cost-complexity pruning work? Walk me through it."),
    para(rt("1. Grow the full tree T0. 2. For each internal node t, compute the effective alpha: the ratio of error increase to leaves removed if we prune the subtree at t. 3. Prune the node with the smallest effective alpha to get T1. 4. Repeat to get the sequence T0 ⊃ T1 ⊃ … ⊃ Troot. 5. Cross-validate to select the tree in this sequence with the best generalisation. The key insight: this greedy algorithm is provably optimal — it produces the same sequence as optimising the cost-complexity criterion for each alpha.")),
    heading3("Q4 (Medium): Why is the denominator (|T_t| - 1) in the effective alpha formula?"),
    para(rt("Pruning the subtree at t replaces |T_t| leaves with 1 leaf — the net leaf reduction is |T_t| - 1. The effective alpha is the error increase per leaf removed. If a subtree has 5 leaves and collapsing it to a single leaf increases error by 0.04, the effective alpha is 0.04 / 4 = 0.01. This normalises across subtrees of different sizes.")),
    heading3("Q5 (Hard): What theoretical guarantee does CART's pruning sequence provide?"),
    para(rt("Breiman et al. (1984) proved: for each α ≥ 0, the algorithm's greedy pruning step produces the unique smallest optimal subtree T(α) — the tree with fewest leaves that minimises R_α(T). Furthermore, the sequence is nested and finite. This means cross-validating over the finite set of candidate trees is provably equivalent to searching over all α ∈ [0, ∞). The proof uses the fact that the set of optimal subtrees forms a chain under the subset relation.")),
    heading3("Q6 (Hard): Explain to a PhD Researcher — what is the relationship between CART pruning and regularisation in neural networks?"),
    para(rt("CART's cost-complexity criterion R_α(T) = R(T) + α|T̃| is structurally analogous to L1 regularisation on neural networks: R(θ) + λ||θ||₁. In both cases, a penalty term discourages complexity (leaf count vs parameter magnitude) and a scalar (α vs λ) controls the bias-variance tradeoff. The key difference: in CART the 'complexity measure' is discrete (leaf count) and the optimal solution at each α is found exactly via the greedy algorithm, whereas in neural nets the L1 problem requires iterative optimisation. CART's discrete structure enables the provably optimal nested sequence, which is unavailable in continuous parameter spaces.")),
    heading3("Red Flags in Interviews"),
    bullet(rt("Saying 'post-pruning uses validation error to prune' — no, it uses resubstitution error for the pruning sequence; CV is only used for model selection (picking α*).")),
    bullet(rt("Confusing min_samples_split (minimum to split) with min_samples_leaf (minimum per leaf) — distinct parameters.")),
    bullet(rt("Claiming min_impurity_decrease uses absolute impurity — it uses the weighted decrease, accounting for child sizes.")),
    divider(),

    # ── Section 8: Comparison ──
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Method", "Speed", "Global View?", "Tuning", "sklearn Param"]),
        table_row(["max_depth", "Fastest", "No", "Grid search integer", "max_depth"]),
        table_row(["min_samples_split", "Fast", "No", "Grid search integer", "min_samples_split"]),
        table_row(["min_impurity_decrease", "Fast", "No", "Continuous δ ≥ 0", "min_impurity_decrease"]),
        table_row(["Cost-complexity (CART)", "Slower", "Yes — full tree first", "CV over alpha path", "ccp_alpha"]),
        table_row(["Reduced Error Pruning", "Moderate", "Yes", "Validation set", "Not in sklearn"]),
        table_row(["Error-Based (C4.5)", "Moderate", "Yes", "Significance level", "Not in sklearn"]),
    ),
    callout("🎯", rt("Decision: ", bold=True), rt("Use pre-pruning (max_depth + min_samples_split) for large datasets, fast training, and interpretability. Use cost-complexity pruning (ccp_alpha + CV) when test generalisation is the priority and you can afford extra computation. Combine both: set modest max_depth as a hard guard and tune ccp_alpha for fine-grained control.")),
    divider(),

    # ── Section 9: Explainer Embed ──
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/decision_tree_pruning_review_explainer.html"),
    para(rt("Step through pre-pruning constraints and post-pruning cost-complexity with a numerically accurate tree — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ──
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Decision Tree Induction (ID3, C4.5, CART) — how splits are chosen")),
    bullet(rt("Gini Impurity & Information Gain — the impurity measures used in Δi(t)")),
    bullet(rt("Bias-Variance Tradeoff — the fundamental reason pruning is necessary")),
    bullet(rt("Cross-Validation — needed to select α* in post-pruning")),
    heading3("What to Learn Next"),
    bullet(rt("Random Forests — ensemble of pruned trees; bagging reduces variance further")),
    bullet(rt("Gradient Boosted Trees (XGBoost, LightGBM) — also prune via min_child_weight and max_depth")),
    bullet(rt("Feature Importance — Gini importance and permutation importance from fitted trees")),
    heading3("Key Papers"),
    bullet(rt("Breiman, Friedman, Olshen, Stone (1984) — ", bold=True), rt("Classification and Regression Trees. Chapman & Hall. The definitive CART reference.")),
    bullet(rt("Quinlan (1993) — ", bold=True), rt("C4.5: Programs for Machine Learning. Introduces error-based pruning.")),
    bullet(rt("Mingers (1987) — ", bold=True), rt("An empirical comparison of pruning methods. Machine Learning 2(3). First systematic comparison.")),
    heading3("Best Resources"),
    bullet(rt("ESL Ch 9.2 — Tree-Based Methods (Hastie, Tibshirani, Friedman) — rigorous treatment")),
    bullet(rt("sklearn docs: Decision Tree — cost_complexity_pruning_path() example")),
    bullet(rt("CART original monograph (Breiman et al.) — appendix proves the nested sequence theorem")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Decision Trees (CART/C4.5) · Ensemble Methods (Random Forest, Gradient Boosting) · Bias-Variance Tradeoff · Cross-Validation · Regularisation")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
