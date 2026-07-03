#!/usr/bin/env python3
"""Update Notion page for: NDCG (Normalized Discounted Cumulative Gain)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__) or '.')
from notion_template import *

PAGE_ID = "33c93418-809c-81cf-9383-daa6f40e5145"
ICON = "🟡"
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/ndcg_explainer.html"},
}

blocks = [

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1: The 30-Second Version
    # ══════════════════════════════════════════════════════════════════════════

    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("NDCG (Normalized Discounted Cumulative Gain) is a metric that measures how well a system ranks a list of items, where the position of each relevant item matters. A highly relevant result at position 1 contributes far more than the same result at position 10.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine Google search results. If the page you're looking for is the very first result, you're happy — you found it instantly. If it's buried on page 3, you're annoyed. NDCG captures this intuition mathematically: it rewards systems that put the most relevant results at the top, and penalizes those that bury them.")),
    heading3("One-Sentence Summary"),
    para(rt("NDCG divides your system's ranking score (DCG) by the best possible ranking's score (IDCG), producing a [0,1] metric where 1 means perfect ordering.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("NDCG = DCG / IDCG, where DCG rewards relevance discounted by log position — so position 1 counts twice as much as positions 2-3 combined.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: Historical Context
    # ══════════════════════════════════════════════════════════════════════════

    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Early information retrieval metrics (Precision@k, Recall) treated all relevant documents identically — a hit at rank 1 counted the same as a hit at rank 100. This failed to reflect real user behavior: users rarely look beyond the first few results.")),
    heading3("What Came Before"),
    para(rt("Average Precision (AP) and Mean Reciprocal Rank (MRR) assumed binary relevance (relevant / not relevant). Real-world relevance is graded — a Wikipedia article on a topic may be more relevant than a forum post, but both count as 'relevant' under binary schemes.")),
    heading3("The Breakthrough"),
    para(rt("Järvelin & Kekäläinen (2002) introduced DCG and NDCG in 'Cumulated Gain-Based Evaluation of IR Techniques' (SIGIR 2002). Their key insight: combine graded relevance with logarithmic position discount. The normalization step (dividing by IDCG) made the metric comparable across queries with different numbers of relevant documents.")),
    heading3("Before vs After"),
    table(
        4,
        table_row(["Dimension", "Precision@k / MAP", "NDCG"]),
        table_row(["Relevance grades", "Binary (0/1)", "Graded (0,1,2,3...)"]),
        table_row(["Position sensitivity", "Uniform within top-k", "Log discount — position 1 >> position 10"]),
        table_row(["Cross-query comparison", "Raw counts vary by query", "Normalized to [0,1]"]),
        table_row(["Best for", "Classification tasks", "Ranked retrieval, recommendation, LTR"]),
    ),
    heading3("Evolution Timeline"),
    para(rt("Precision/Recall (1950s) → Average Precision (1970s) → MRR (1990s) → DCG/NDCG (2002) → LambdaRank/LambdaMART optimizing NDCG directly (2007) → NDCG as standard LTR benchmark (2010s→present)")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3: Core Concepts & Theory
    # ══════════════════════════════════════════════════════════════════════════

    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Relevance score "), eq(r"rel_i"), rt(" — a non-negative integer grade for the document at rank i (e.g., 0=irrelevant, 1=marginal, 2=relevant, 3=highly relevant)")),
    bullet(rt("Gain — the usefulness of a document: "), eq(r"2^{rel_i} - 1"), rt(" (exponential gain formula) or simply "), eq(r"rel_i"), rt(" (linear gain formula)")),
    bullet(rt("Discount — the positional penalty: "), eq(r"\frac{1}{\log_2(i+1)}"), rt(", which equals 1 at position 1 and decreases logarithmically")),
    bullet(rt("DCG — Discounted Cumulative Gain: sum of discounted gains over the ranked list")),
    bullet(rt("IDCG — Ideal DCG: DCG achieved by the perfect ranking (sorted by relevance descending)")),
    bullet(rt("NDCG — Normalized DCG: "), eq(r"\text{DCG} / \text{IDCG}"), rt(", always in [0,1]")),
    heading3("Core Property"),
    callout("🔑", rt("Key Concept: ", bold=True), rt("NDCG is query-independent — by dividing by IDCG, you can average NDCG across queries with wildly different numbers of relevant documents and get a meaningful aggregate score.")),
    heading3("Prerequisites"),
    para(rt("To understand NDCG fully, you should know: Precision@k and Recall, binary relevance vs graded relevance, logarithms (base 2), and the concept of ranking/ordering in information retrieval.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4: Architecture & Internal Workings
    # ══════════════════════════════════════════════════════════════════════════

    heading2("⚙️ Architecture & Internal Workings"),
    heading3("Step-by-Step Computation"),
    numbered(rt("Collect relevance judgments for your query — a list of (document, relevance_grade) pairs")),
    numbered(rt("Rank documents by your system's predicted score (highest first)")),
    numbered(rt("Extract the relevance grades in ranked order: "), eq(r"[rel_1, rel_2, \ldots, rel_k]")),
    numbered(rt("Compute DCG@k using the exponential gain formula")),
    numbered(rt("Compute IDCG@k by sorting the same relevance grades descending, then applying DCG formula")),
    numbered(rt("NDCG@k = DCG@k / IDCG@k")),
    heading3("Numerical Trace — Worked Example"),
    para(rt("Ranked list relevance scores (positions 1-6): [3, 2, 3, 0, 1, 2]")),
    para(rt("Position discounts "), eq(r"\frac{1}{\log_2(i+1)}"), rt(": [1.000, 0.631, 0.500, 0.431, 0.387, 0.356]")),
    para(rt("Gains "), eq(r"2^{rel_i} - 1"), rt(": [7, 3, 7, 0, 1, 3]")),
    para(rt("Discounted gains (gain × discount): [7.000, 1.893, 3.500, 0.000, 0.387, 1.068]")),
    para(rt("DCG@6 = 7.000 + 1.893 + 3.500 + 0.000 + 0.387 + 1.068 = "), rt("13.848", bold=True)),
    para(rt("Ideal ranking: [3, 3, 2, 2, 1, 0] → gains [7, 7, 3, 3, 1, 0]")),
    para(rt("IDCG@6 = 7.000 + 4.417 + 1.500 + 1.293 + 0.387 + 0.000 = "), rt("14.597", bold=True)),
    equation_block(r"\text{NDCG@6} = \frac{13.848}{14.597} \approx 0.949"),
    heading3("Design Decisions"),
    callout("💭", rt("Why log₂(i+1) and not log₂(i)? ", bold=True), rt("Using i+1 ensures position 1 gets discount 1/log₂(2) = 1.0 (no penalty at the top), while log₂(i) would give log₂(1)=0, causing division by zero.")),
    callout("💭", rt("Why 2^rel - 1 and not just rel? ", bold=True), rt("The exponential gain formula emphasizes highly relevant documents much more than marginally relevant ones. With linear gain, rel=3 is only 3× better than rel=1. With exponential gain, rel=3 is 7× better than rel=1 — matching human perception that perfect results are far more valuable.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5: The Math
    # ══════════════════════════════════════════════════════════════════════════

    heading2("📐 The Math Behind It"),
    heading3("DCG Formula (Exponential Gain — standard)"),
    equation_block(r"\text{DCG@}k = \sum_{i=1}^{k} \frac{2^{rel_i} - 1}{\log_2(i+1)}"),
    heading3("DCG Formula (Linear Gain — original Järvelin 2002)"),
    equation_block(r"\text{DCG@}k = \sum_{i=1}^{k} \frac{rel_i}{\log_2(i+1)}"),
    heading3("Ideal DCG"),
    equation_block(r"\text{IDCG@}k = \sum_{i=1}^{k} \frac{2^{rel_{\pi(i)}} - 1}{\log_2(i+1)}"),
    para(rt("where "), eq(r"\pi"), rt(" is the permutation that sorts documents by relevance descending (i.e., "), eq(r"rel_{\pi(1)} \geq rel_{\pi(2)} \geq \cdots \geq rel_{\pi(k)}"), rt(").")),
    heading3("NDCG"),
    equation_block(r"\text{NDCG@}k = \frac{\text{DCG@}k}{\text{IDCG@}k}"),
    para(rt("NDCG is bounded: "), eq(r"0 \leq \text{NDCG@}k \leq 1"), rt(". It equals 1 iff your ranking is the perfect ideal ordering, and approaches 0 when the most relevant documents are ranked last.")),
    heading3("Position Discount Decay"),
    para(rt("The discount function "), eq(r"d(i) = \frac{1}{\log_2(i+1)}"), rt(" gives:")),
    bullet(rt("Position 1: "), eq(r"d(1) = 1.000")),
    bullet(rt("Position 2: "), eq(r"d(2) = 1/\log_2(3) \approx 0.631")),
    bullet(rt("Position 3: "), eq(r"d(3) = 1/\log_2(4) = 0.500")),
    bullet(rt("Position 10: "), eq(r"d(10) = 1/\log_2(11) \approx 0.289")),
    bullet(rt("Position 100: "), eq(r"d(100) = 1/\log_2(101) \approx 0.151")),
    callout("⚠️", rt("Warning: ", bold=True), rt("NDCG@k is undefined (division by zero) when IDCG@k = 0, which happens when there are no relevant documents at all in the top-k of the ideal ranking. Always handle this edge case in implementation — typically by defining NDCG=1 when both DCG and IDCG are 0, and NDCG=0 when IDCG=0 but DCG>0 (which should be impossible if judgments are consistent).")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6: Code
    # ══════════════════════════════════════════════════════════════════════════

    heading2("💻 Code Implementation"),
    heading3("From Scratch (NumPy)"),
    code_block("python", '''import numpy as np

def dcg_at_k(relevances, k):
    """Compute Discounted Cumulative Gain at k.

    Args:
        relevances: list/array of relevance grades in ranked order
        k: cutoff position
    Returns:
        DCG@k (float) using exponential gain formula
    """
    relevances = np.array(relevances[:k], dtype=float)
    n = len(relevances)
    if n == 0:
        return 0.0
    # Position indices 1-based: positions = [1, 2, 3, ..., n]
    positions = np.arange(1, n + 1)
    # Exponential gain: 2^rel - 1
    gains = np.power(2.0, relevances) - 1.0
    # Logarithmic discount: 1 / log2(i + 1)
    discounts = 1.0 / np.log2(positions + 1)
    return np.sum(gains * discounts)

def ndcg_at_k(relevances, k):
    """Compute NDCG@k.

    Args:
        relevances: list/array of relevance grades in ranked order (your system\'s output)
        k: cutoff position
    Returns:
        NDCG@k in [0, 1], or 1.0 if no relevant documents exist
    """
    dcg = dcg_at_k(relevances, k)
    # Ideal DCG: sort relevances descending
    ideal_relevances = sorted(relevances, reverse=True)
    idcg = dcg_at_k(ideal_relevances, k)
    if idcg == 0.0:
        return 1.0  # Convention: perfect score when nothing is relevant
    return dcg / idcg

# ── Worked example ─────────────────────────────────────────────
relevances = [3, 2, 3, 0, 1, 2]  # your system\'s ranking
k = 6

dcg  = dcg_at_k(relevances, k)   # 13.848
idcg = dcg_at_k(sorted(relevances, reverse=True), k)  # 14.597
ndcg = ndcg_at_k(relevances, k)  # 0.949

print(f"DCG@{k}  = {dcg:.3f}")
print(f"IDCG@{k} = {idcg:.3f}")
print(f"NDCG@{k} = {ndcg:.3f}")
# Output:
# DCG@6  = 13.848
# IDCG@6 = 14.597
# NDCG@6 = 0.949
'''),
    heading3("Production Usage (scikit-learn)"),
    code_block("python", '''from sklearn.metrics import ndcg_score
import numpy as np

# sklearn expects 2D arrays: shape (n_queries, n_documents)
# relevances_true: ground-truth relevance grades
# relevances_pred: predicted scores from your system (higher = more relevant)

# Single query example
relevances_true = np.array([[3, 2, 3, 0, 1, 2]])  # ground truth
relevances_pred = np.array([[0.9, 0.8, 0.7, 0.4, 0.3, 0.2]])  # model scores

# sklearn ranks by relevances_pred descending, then computes NDCG
score = ndcg_score(relevances_true, relevances_pred, k=6)
print(f"NDCG@6 = {score:.4f}")

# ⚠️ Gotcha 1: sklearn\'s ndcg_score uses linear gain by default in some versions.
#    The sklearn implementation uses the exponential formula (2^rel - 1) matching
#    the standard used in LTR benchmarks (LETOR, MS MARCO).

# ⚠️ Gotcha 2: the second argument is SCORES (not relevance grades).
#    sklearn ranks documents by these scores, THEN evaluates against true relevances.
#    Don\'t pass true relevances as both arguments — that always gives NDCG=1!

# Mean NDCG across multiple queries
true_multi = np.array([[3,2,1,0], [2,2,1,1], [3,0,0,0]])
pred_multi = np.array([[0.9,0.7,0.4,0.1], [0.8,0.6,0.5,0.2], [0.95,0.3,0.2,0.1]])
mean_ndcg = ndcg_score(true_multi, pred_multi, k=4)
print(f"Mean NDCG@4 = {mean_ndcg:.4f}")
'''),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 7: Interview Deep-Dive
    # ══════════════════════════════════════════════════════════════════════════

    heading2("🎤 Interview Deep-Dive"),
    toggle(
        [rt("Q1 (Easy): What is NDCG and why is it used in information retrieval?", bold=True)],
        [
            para(rt("NDCG measures the quality of a ranked list by rewarding relevant items at the top. It uses a logarithmic discount so that position 1 is far more valuable than position 10. By dividing by IDCG (the perfect ranking's score), it normalizes to [0,1], enabling comparison across queries with different numbers of relevant documents.")),
            para(rt("Key formula: "), eq(r"\text{NDCG@}k = \frac{\sum_{i=1}^k (2^{rel_i}-1)/\log_2(i+1)}{\text{IDCG@}k}")),
        ],
    ),
    toggle(
        [rt("Q2 (Medium): What is IDCG and why do we need normalization?", bold=True)],
        [
            para(rt("IDCG is the DCG of the ideal ranking — documents sorted by relevance descending. Without normalization, DCG values are incomparable across queries: a query with 10 highly relevant documents will always have higher DCG than a query with 2 relevant documents, regardless of system quality. NDCG = DCG/IDCG fixes this.")),
        ],
    ),
    toggle(
        [rt("Q3 (Medium): What's the difference between linear gain (rel_i) and exponential gain (2^rel_i - 1)?", bold=True)],
        [
            para(rt("Linear gain: "), eq(r"rel_i"), rt(" — each relevance grade contributes proportionally. A grade-3 document contributes 3× a grade-1 document.")),
            para(rt("Exponential gain: "), eq(r"2^{rel_i} - 1"), rt(" — grade 3 contributes 7× a grade 1 document. This better reflects user behavior: a perfect result is disproportionately more valuable than a mediocre one.")),
            para(rt("The exponential variant is now standard (used by LETOR, MS MARCO, Kaggle competitions, and sklearn).")),
        ],
    ),
    toggle(
        [rt("Q4 (Hard): How would you optimize NDCG directly during model training?", bold=True)],
        [
            para(rt("NDCG is non-differentiable (it depends on discrete rankings). LambdaRank (Burges et al., 2007) addresses this by defining pseudo-gradients proportional to |ΔNDCG| — the absolute change in NDCG if two documents swap positions. LambdaMART extends this using gradient-boosted trees, making it the dominant Learning-to-Rank (LTR) algorithm.")),
            para(rt("Specifically, for documents i and j where "), eq(r"s_i > s_j"), rt(" but "), eq(r"rel_j > rel_i"), rt(" (wrong order), the gradient is:")),
            equation_block(r"\lambda_{ij} = \frac{-1}{1 + e^{s_i - s_j}} \cdot |\Delta\text{NDCG}_{ij}|"),
        ],
    ),
    toggle(
        [rt("Q5 (Hard — Follow-up trap): NDCG@k for k < total relevant docs — is this problematic?", bold=True)],
        [
            para(rt("Yes. NDCG@10 on a query with 50 relevant documents means even the perfect system at k=10 can only put 10 of the 50 relevant docs in the window. IDCG@10 uses the top-10 most relevant docs from the pool, so you're comparing against this restricted ideal — not against retrieving all 50. This is correct behavior but means NDCG@10 ≠ NDCG@50.")),
        ],
    ),
    heading3("Explain to a PhD Researcher"),
    para(rt("NDCG is a rank-weighted evaluation functional. Define "), eq(r"\sigma: [n] \to [n]"), rt(" as your system's ranking permutation. Then:")),
    equation_block(r"\text{NDCG@}k(\sigma) = \frac{\sum_{i=1}^k (2^{rel_{\sigma(i)}}-1) / \log_2(i+1)}{\max_{\pi} \sum_{i=1}^k (2^{rel_{\pi(i)}}-1) / \log_2(i+1)}"),
    para(rt("The denominator is achieved by "), eq(r"\pi = \text{argsort}(rel, \text{descending})"), rt(". LambdaRank optimizes a smooth surrogate by defining pair-wise pseudo-gradients "), eq(r"|\Delta\text{NDCG}_{ij}|"), rt(" that approximate the gradient of the expected NDCG under a Plackett-Luce ranking distribution.")),
    heading3("Explain to a Research Scientist/Engineer"),
    para(rt("NDCG@k: score your system's top-k results against an oracle. Use "), eq(r"\text{ndcg\_score}"), rt(" from sklearn for quick evaluation, but implement from scratch when you need query-level aggregation or custom relevance grading schemes. In LTR pipelines (XGBoost with rank:ndcg, LightGBM with lambdarank), the model directly optimizes NDCG — set "), rt("eval_metric='ndcg'", code=True), rt(" and "), rt("label_gain", code=True), rt(" to match your relevance scale.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 8: Comparisons
    # ══════════════════════════════════════════════════════════════════════════

    heading2("⚖️ Comparison & Trade-offs"),
    heading3("NDCG vs Other Ranking Metrics"),
    table(
        5,
        table_row(["Metric", "Relevance Type", "Position Sensitive", "Normalized", "Best For"]),
        table_row(["Precision@k", "Binary", "No (uniform)", "Partially", "Simple retrieval"]),
        table_row(["Recall@k", "Binary", "No", "Yes (by total relevant)", "Coverage tasks"]),
        table_row(["MAP", "Binary", "Yes (AP considers order)", "Yes", "Standard IR benchmark"]),
        table_row(["MRR", "Binary", "Yes (only first hit)", "Yes", "QA / single-answer tasks"]),
        table_row(["NDCG@k", "Graded", "Yes (log discount)", "Yes [0,1]", "Ranked retrieval, LTR, RecSys"]),
        table_row(["ERR", "Graded", "Yes (cascade model)", "Yes [0,1]", "Web search (user stops at first satisfying result)"]),
    ),
    callout("🎯", rt("Decision: ", bold=True), rt("Use NDCG when you have graded relevance labels and care about full-list quality. Use MAP for binary relevance + IR benchmarks. Use MRR for single-answer tasks. Use ERR when the user stops after finding the first satisfying result (click model). Avoid Precision@k for comparing systems on queries with different numbers of relevant docs.")),
    heading3("Advantages"),
    bullet(rt("Handles graded relevance — not just binary relevant/not")),
    bullet(rt("Position-sensitive — rewards top-heavy rankings")),
    bullet(rt("Normalized to [0,1] — comparable across queries and datasets")),
    bullet(rt("Industry standard — used in LETOR, MS MARCO, Yahoo! LTR Challenge, Kaggle")),
    heading3("Disadvantages"),
    bullet(rt("Requires relevance judgments — expensive human annotation")),
    bullet(rt("Non-differentiable — cannot directly backpropagate through NDCG")),
    bullet(rt("Undefined when IDCG=0 — must handle edge case")),
    bullet(rt("Sensitive to k — NDCG@10 and NDCG@100 can tell very different stories")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 9: Explainer Embed
    # ══════════════════════════════════════════════════════════════════════════

    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/ndcg_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10: Related Topics
    # ══════════════════════════════════════════════════════════════════════════

    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Information Retrieval fundamentals (Precision, Recall, F1)")),
    bullet(rt("Ranking and sorting algorithms")),
    bullet(rt("Logarithms and logarithmic decay")),
    bullet(rt("Graded relevance judgments and annotation")),
    heading3("What to Learn Next"),
    bullet(rt("Learning to Rank (LTR) — pointwise, pairwise, listwise approaches")),
    bullet(rt("LambdaRank and LambdaMART — directly optimizing NDCG")),
    bullet(rt("Expected Reciprocal Rank (ERR) — cascade model for web search")),
    bullet(rt("Recommender System evaluation — NDCG in collaborative filtering")),
    bullet(rt("Mean Average Precision (MAP) — the binary-relevance counterpart")),
    heading3("Key Papers"),
    numbered(rt("Järvelin & Kekäläinen (2002). 'Cumulated Gain-Based Evaluation of IR Techniques.' ACM TOIS — introduced DCG/NDCG")),
    numbered(rt("Burges et al. (2007). 'Learning to Rank Using Gradient Descent (RankNet/LambdaRank).' ICML — first practical NDCG optimization")),
    numbered(rt("Wu et al. (2010). 'Adapting Boosting for Information Retrieval Measures.' Information Retrieval — LambdaMART")),
    numbered(rt("Chapelle & Chang (2011). 'Yahoo! Learning to Rank Challenge Overview.' JMLR — industry-scale NDCG benchmarking")),
    heading3("Best Resources"),
    bullet(rt("Manning, Raghavan & Schütze — 'Introduction to Information Retrieval' Ch. 8 (free online)")),
    bullet(rt("YouTube: 'Learning to Rank' by Olivier Chapelle — Google Tech Talk")),
    bullet(rt("sklearn docs: sklearn.metrics.ndcg_score")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Mean Average Precision (MAP), MRR, Learning to Rank, LambdaMART, Recommender Systems Evaluation, Collaborative Filtering, Click Models, BM25")),

]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
