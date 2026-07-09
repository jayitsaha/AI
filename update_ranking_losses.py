#!/usr/bin/env python3
"""Update Notion page for: Ranking losses (margin ranking, pairwise/listwise)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8198-9fff-ffa9875a857f"
ICON = "🟠"  # Advanced
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/AI/explainers/ranking_losses_explainer.html"},
}

blocks = [
    # ── Section 1: The 30-Second Version ──
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt(
        "Ranking losses are training objectives that teach a model to put items in the "
        "RIGHT ORDER, not to predict the exact right number. Instead of asking \"is this "
        "score 4.7 or 4.8?\", they ask \"should item A score higher than item B?\" — because "
        "for search, recommendations, and ads, what the user sees is a sorted list, and only "
        "the relative order matters."
    )),
    heading3("Real-World Analogy"),
    para(rt(
        "Imagine judging a diving competition. You don't need judges to agree on the exact "
        "number of points (9.3 vs 9.4) — you need them to agree on who dove better than whom. "
        "A margin ranking loss is like a judge saying \"diver A must clear diver B by at least "
        "0.5 points, or I'm unhappy.\" A listwise loss is like grading the ENTIRE podium order "
        "at once, not just pairwise comparisons."
    )),
    para(rt(
        "Summary: Ranking losses (margin ranking, RankNet pairwise loss, ListNet/LambdaRank "
        "listwise losses) optimize the relative ORDER of scored items rather than their "
        "absolute values, because ranking quality — not raw score accuracy — is what search, "
        "recsys, and ads systems are ultimately judged on."
    )),
    callout("💡", rt("If you remember one thing: ", bold=True), rt(
        "Ranking losses penalize an incorrectly ORDERED pair (or list), not an incorrectly "
        "VALUED score — a model can be \"wrong\" in absolute terms and still have zero ranking loss "
        "as long as relevant items score above irrelevant ones."
    )),
    divider(),

    # ── Section 2: Historical Context ──
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt(
        "Early \"learning to rank\" attempts trained a plain regressor or classifier per "
        "document — a pointwise approach (e.g., regress relevance grade with MSE, or classify "
        "relevant/irrelevant with logistic loss). Pointwise losses treat each document "
        "independently and are blind to the fact that the final product is a SORTED LIST. "
        "A model can achieve low MSE overall while still misordering the top results — the "
        "exact place users look."
    )),
    heading3("What Came Before"),
    para(rt(
        "Pointwise regression/classification (e.g., PRank, McRank) minimized per-document "
        "error. It ignored inter-document dependencies: getting the top-2 documents swapped "
        "hurts a search engine far more than a small score error on a document ranked #50, "
        "but pointwise losses weight every document equally."
    )),
    heading3("The Breakthrough"),
    para(rt(
        "Burges et al. (2005) introduced RankNet: reframe the problem as classifying PAIRS "
        "of documents — \"is document i more relevant than document j?\" — using a "
        "cross-entropy loss over a sigmoid of the score difference. This directly optimizes "
        "the thing that matters: relative order. Cao et al. (2007, ListNet) then generalized "
        "this from pairs to full permutations (listwise), and Burges (2010, LambdaRank / "
        "LambdaMART) fixed RankNet's biggest flaw — that it didn't know the loss function "
        "(like NDCG) even existed — by directly weighting each pairwise gradient by how much "
        "swapping that pair would change NDCG."
    )),
    heading3("Key Papers"),
    bullet(rt("Burges et al., ", bold=True), rt("\"Learning to Rank using Gradient Descent\" — ICML 2005. Introduced RankNet (pairwise, neural net + cross-entropy).")),
    bullet(rt("Cao, Qin, Liu, Tsai, Li, ", bold=True), rt("\"Learning to Rank: From Pairwise Approach to Listwise Approach\" — ICML 2007. Introduced ListNet (Plackett-Luce listwise loss).")),
    bullet(rt("Burges, ", bold=True), rt("\"From RankNet to LambdaRank to LambdaMART: An Overview\" — MSR-TR 2010. Introduced λ-gradients weighted by |ΔNDCG|.")),
    bullet(rt("Wu, Burges, Svore, Gao, ", bold=True), rt("\"Adapting Boosting for Information Retrieval Measures\" — 2010. LambdaMART = LambdaRank gradients + MART (gradient boosted trees).")),
    heading3("Evolution Timeline"),
    para(rt("Pointwise regression/classification  →  Pairwise (Margin Ranking Loss, RankNet)  →  Listwise (ListNet, ListMLE)  →  Metric-aware (LambdaRank, LambdaMART, SoftRank)  →  Neural listwise (ApproxNDCG, TF-Ranking, differentiable sort losses).")),
    table(4,
        table_row(["Dimension", "Pointwise (Before)", "Pairwise/Listwise (After)"]),
        table_row(["Optimizes", "Per-item score accuracy", "Relative order / whole-list order"]),
        table_row(["Loss signal", "MSE / cross-entropy on label", "Preference violations between items"]),
        table_row(["Sensitivity to top-of-list errors", "Uniform across all items", "Can be weighted toward top ranks (LambdaRank)"]),
        table_row(["Correlates with NDCG/MRR", "Weakly", "Directly (esp. LambdaRank)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ──
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Given a query "), eq(r"q"), rt(", a set of documents "), eq(r"\{d_1,\dots,d_n\}"),
         rt(" with relevance grades "), eq(r"y_i \in \{0,1,\dots,R\}"), rt(" and model scores "),
         eq(r"s_i = f(q, d_i;\theta)"), rt(", a ranking loss is a function of the SCORES and "
            "the RELATIVE preference order implied by the relevance grades — not of "
            "\\(s_i\\) and \\(y_i\\) in isolation.")),
    heading3("The Three Families"),
    bullet(rt("Pointwise: ", bold=True), rt("loss decomposes over individual documents, e.g. "), eq(r"\sum_i \ell(s_i, y_i)"), rt(" (regression/classification).")),
    bullet(rt("Pairwise: ", bold=True), rt("loss decomposes over ordered pairs "), eq(r"(i,j)"), rt(" where "), eq(r"y_i > y_j"), rt(", e.g. "), eq(r"\sum_{(i,j)} \ell(s_i - s_j)"), rt(" — Margin Ranking Loss and RankNet live here.")),
    bullet(rt("Listwise: ", bold=True), rt("loss is a function of the entire score vector "), eq(r"\mathbf{s}"), rt(" and full permutation/relevance vector at once — ListNet, ListMLE, LambdaRank, ApproxNDCG.")),
    heading3("Core Property / Invariant"),
    para(rt("All ranking losses share "), rt("translation invariance", bold=True), rt(": adding a constant "), eq(r"c"), rt(" to every score "), eq(r"s_i \to s_i + c"), rt(" leaves the loss unchanged, because only score DIFFERENCES (pairwise) or score-induced ORDERINGS (listwise) matter — never absolute magnitude.")),
    callout("🔑", rt("Key Concept: ", bold=True), rt(
        "A ranking loss is invariant to any monotonic transform that preserves order for "
        "pointwise evaluation, but pairwise/listwise losses are strictly more informative "
        "because they encode WHICH orderings are preferred, directly matching how ranking "
        "quality (NDCG, MRR, MAP) is measured at inference time."
    )),
    heading3("Prerequisites Check"),
    para(rt("To understand this, you should know: binary cross-entropy loss, gradient descent, sigmoid/softmax, and the definition of NDCG (Normalized Discounted Cumulative Gain).")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ──
    heading2("🏗️ Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("Pipeline"),
    para(rt("Query+Doc features → Scoring function "), eq(r"f_\theta"), rt(" (linear model / GBDT / neural net) → raw scores "), eq(r"s_i"), rt(" → Ranking loss (pairwise or listwise, computed over all documents for a query) → gradient w.r.t. "), eq(r"s_i"), rt(" → backprop/boosting update of "), eq(r"\theta"), rt(".")),
    heading3("1. Margin Ranking Loss — the simplest pairwise loss"),
    para(rt("Given a preferred document with score "), eq(r"s^+"), rt(" and a less-preferred one with score "), eq(r"s^-"), rt(", and target "), eq(r"y=1"), rt(":")),
    equation_block(r"L(s^+, s^-) = \max\big(0,\; -y\cdot(s^+ - s^-) + m\big) = \max(0,\, m - (s^+ - s^-))"),
    para(rt("This is EXACTLY hinge loss applied to a score difference. It only produces gradient when the margin "), eq(r"m"), rt(" is violated: "), eq(r"s^+ - s^- < m"), rt(". Once "), eq(r"s^+"), rt(" beats "), eq(r"s^-"), rt(" by at least "), eq(r"m"), rt(", the pair contributes ZERO loss and zero gradient — the model stops \"caring\" about already-correctly-separated pairs and focuses capacity on violated ones.")),
    heading3("2. RankNet — probabilistic pairwise loss"),
    para(rt("RankNet converts the score difference into a probability that "), eq(r"i"), rt(" ranks above "), eq(r"j"), rt(" via a sigmoid, then applies cross-entropy against the TRUE preference:")),
    equation_block(r"P_{ij} = \sigma(s_i - s_j) = \frac{1}{1+e^{-\sigma_0(s_i-s_j)}}, \qquad \bar{P}_{ij} = \frac{1}{2}(1+S_{ij}),\ \ S_{ij}\in\{-1,0,1\}"),
    equation_block(r"C_{ij} = -\bar{P}_{ij}\log P_{ij} - (1-\bar{P}_{ij})\log(1-P_{ij})"),
    para(rt("Unlike margin ranking loss's hard cutoff, RankNet's loss is smooth and NEVER exactly zero — it always pulls "), eq(r"s_i"), rt(" and "), eq(r"s_j"), rt(" further apart, just with vanishing gradient as separation grows.")),
    heading3("3. ListNet — listwise via Plackett-Luce top-one probability"),
    para(rt("Instead of pairs, ListNet compares two PROBABILITY DISTRIBUTIONS over \"which document is ranked #1\", one derived from true relevance, one from predicted scores, both via softmax (Plackett-Luce top-1 model):")),
    equation_block(r"P_s(j) = \frac{\exp(s_j)}{\sum_{k=1}^n \exp(s_k)}, \qquad L_{\text{ListNet}} = -\sum_{j=1}^n P_y(j)\,\log P_s(j)"),
    para(rt("This is cross-entropy between the TRUE top-1 distribution "), eq(r"P_y"), rt(" (softmax of relevance grades) and the PREDICTED top-1 distribution "), eq(r"P_s"), rt(" — it considers all documents jointly in one loss term, not pair-by-pair.")),
    heading3("4. LambdaRank — metric-aware pairwise gradients"),
    para(rt("RankNet's gradient magnitude for a pair doesn't know whether that pair sits at rank 1-2 (huge NDCG impact) or rank 49-50 (negligible impact). LambdaRank fixes this by literally MULTIPLYING the RankNet gradient by "), eq(r"|\Delta \text{NDCG}_{ij}|"), rt(" — the change in NDCG if ranks "), eq(r"i"), rt(" and "), eq(r"j"), rt(" were swapped in the CURRENT ranked list:")),
    equation_block(r"\lambda_{ij} = \frac{\partial C_{ij}}{\partial s_i} = -\frac{\sigma_0}{1+e^{\sigma_0(s_i-s_j)}}\,\big|\Delta \text{NDCG}_{ij}\big|"),
    para(rt("No explicit loss function "), eq(r"C"), rt(" needs to be differentiable for this — "), eq(r"\lambda_{ij}"), rt(" IS the gradient, defined directly, which is why LambdaRank can optimize non-differentiable metrics like NDCG or MAP.")),
    heading3("Numerical Trace"),
    para(rt("Query with 4 documents, true relevance "), eq(r"y=[3,2,1,0]"), rt(" for "), eq(r"[A,B,C,D]"), rt(", untrained model scores "), eq(r"s=[0.2, 0.9, 0.5, 0.7]"), rt(" (badly ordered — D outscores A despite being irrelevant):")),
    bullet(rt("Margin loss on pair (A,D), m=1: "), eq(r"L=\max(0, 1-(0.2-0.7))=\max(0,1.5)=1.5"), rt(" — heavily penalized.")),
    bullet(rt("RankNet on pair (A,D): "), eq(r"P_{AD}=\sigma(0.2-0.7)=\sigma(-0.5)=0.3775"), rt(", target "), eq(r"\bar P=1"), rt(", cross-entropy "), eq(r"C=-\log(0.3775)=0.974"), rt(".")),
    bullet(rt("ListNet: predicted "), eq(r"P_s=[0.166,0.335,0.224,0.274]"), rt(", target "), eq(r"P_y=[0.644,0.237,0.087,0.032]"), rt(" (softmax of relevance grades), "), eq(r"L=-\sum P_y \log P_s \approx 1.586"), rt(".")),
    bullet(rt("LambdaRank on (A,D): current ranking B,D,C,A gives NDCG@4=0.6935; swapping A,D gives NDCG@4=0.8428, so "), eq(r"|\Delta\text{NDCG}|=0.1493"), rt(", giving "), eq(r"\lambda_{AD}=-\frac{1}{1+e^{-0.5}}\times 0.1493\approx -0.093"), rt(" — a strong pull compared to a low-impact pair like (B,C) which barely changes NDCG.")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("Ties ("), eq(r"y_i=y_j"), rt("): pairwise losses should SKIP these pairs (or use "), eq(r"S_{ij}=0"), rt(") — including them injects noise since there's no ground-truth preference.")),
    bullet(rt("Margin ranking loss with a too-large margin "), eq(r"m"), rt(": forces even confidently-correct pairs to keep producing gradient, distorting the score scale.")),
    bullet(rt("Class imbalance in relevance grades: a query with 1 relevant + 99 irrelevant docs produces 99 pairs dominated by the same easy comparisons — needs pair sampling/weighting.")),
    bullet(rt("Listwise cost: naive listwise losses over full permutations are "), eq(r"O(n!)"), rt("; ListNet's top-one relaxation reduces this to "), eq(r"O(n)"), rt(", which is why it's tractable.")),
    callout("⚙️", rt("Design Decision: ", bold=True), rt(
        "Why weight gradients by |ΔNDCG| (LambdaRank) instead of directly differentiating NDCG? "
        "NDCG is a function of RANK POSITIONS (via sort), which is piecewise-constant and has "
        "zero gradient almost everywhere. LambdaRank sidesteps this by defining a heuristic "
        "gradient directly, rather than trying to backprop through an argsort."
    )),
    divider(),

    # ── Section 5: The Math Behind It ──
    heading2("📐 The Math Behind It"),
    heading3("Margin Ranking Loss — Gradient"),
    para(rt("For an active pair (loss > 0), the subgradient is piecewise constant:")),
    equation_block(r"\frac{\partial L}{\partial s^+} = \begin{cases}-1 & \text{if } m-(s^+-s^-) > 0\\ 0 & \text{otherwise}\end{cases}, \qquad \frac{\partial L}{\partial s^-} = -\frac{\partial L}{\partial s^+}"),
    para(rt("The gradient magnitude is constant (1) regardless of how badly the pair is misordered — every violated pair gets an equal-strength push, which is the hinge loss's defining trait.")),
    heading3("RankNet — Full Derivation"),
    para(rt("Start from binary cross-entropy on "), eq(r"P_{ij}=\sigma(s_i-s_j)"), rt(":")),
    equation_block(r"C_{ij} = -\bar P_{ij}\log P_{ij} - (1-\bar P_{ij})\log(1-P_{ij})"),
    para(rt("Substituting "), eq(r"\bar P_{ij}=1"), rt(" (i truly preferred over j) simplifies to the familiar logistic loss on the score gap:")),
    equation_block(r"C_{ij} = \log\big(1+e^{-\sigma_0(s_i-s_j)}\big)"),
    para(rt("Differentiating w.r.t. "), eq(r"s_i"), rt(":")),
    equation_block(r"\frac{\partial C_{ij}}{\partial s_i} = -\sigma_0\left(1 - \sigma(s_i-s_j)\right) = -\sigma_0\big(1-P_{ij}\big) = \sigma_0\left(\bar P_{ij}-P_{ij}\right)\text{(general }\bar P\text{ case)}"),
    para(rt("This is the gradient "), eq(r"\lambda_{ij}"), rt(" that LambdaRank later reuses and reweights by "), eq(r"|\Delta\text{NDCG}_{ij}|"), rt(".")),
    heading3("ListNet — Cross-Entropy over Top-One Distributions"),
    equation_block(r"L_{\text{ListNet}}(\mathbf{y},\mathbf{s}) = -\sum_{j=1}^n \frac{e^{y_j}}{\sum_k e^{y_k}}\,\log\frac{e^{s_j}}{\sum_k e^{s_k}}"),
    para(rt("Gradient w.r.t. "), eq(r"s_j"), rt(" (standard softmax cross-entropy gradient):")),
    equation_block(r"\frac{\partial L_{\text{ListNet}}}{\partial s_j} = P_s(j) - P_y(j)"),
    heading3("NDCG — the metric these losses approximate"),
    equation_block(r"\text{DCG}@k = \sum_{i=1}^k \frac{2^{y_i}-1}{\log_2(i+1)}, \qquad \text{NDCG}@k = \frac{\text{DCG}@k}{\text{IDCG}@k}"),
    para(rt("where IDCG is the DCG of the IDEAL (perfectly sorted-by-relevance) ranking, making NDCG "), eq(r"\in [0,1]"), rt(".")),
    callout("⚠️", rt("Common Misconception: ", bold=True), rt(
        "\"Minimizing pairwise loss automatically maximizes NDCG.\" False in general — RankNet/margin "
        "ranking loss weight ALL pairs equally, so a model can perfectly satisfy thousands of "
        "low-rank pairs while still misordering the top-2 (which dominates NDCG due to its "
        "log-discount). This is precisely the gap LambdaRank closes by weighting each pair's "
        "gradient by its actual NDCG impact."
    )),
    heading3("Proof Sketch — Why RankNet's C_ij is convex in (s_i − s_j)"),
    para(rt("Let "), eq(r"z=s_i-s_j"), rt(". Then "), eq(r"C(z)=\log(1+e^{-\sigma_0 z})"), rt(" is the softplus of "), eq(r"-\sigma_0 z"), rt(", and softplus is convex (its second derivative "), eq(r"\sigma(z)(1-\sigma(z))\sigma_0^2 \geq 0"), rt(" everywhere), so "), eq(r"C"), rt(" is convex in the score gap — gradient descent on a single pair is well-behaved, though the SUM over many pairs sharing documents is not jointly convex in "), eq(r"\theta"), rt(" for a nonlinear "), eq(r"f_\theta"), rt(".")),
    divider(),

    # ── Section 6: Code Implementation ──
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """import numpy as np

def margin_ranking_loss(s_pos, s_neg, margin=1.0):
    \"\"\"Hinge loss on a score gap. s_pos, s_neg: (batch,) arrays.\"\"\"
    diff = s_pos - s_neg
    loss = np.maximum(0.0, margin - diff)
    # gradient is -1 for active (violated) pairs, 0 otherwise
    active = (loss > 0).astype(np.float64)
    grad_pos = -active
    grad_neg = active
    return loss.mean(), grad_pos, grad_neg


def ranknet_loss(s_i, s_j, S_ij, sigma=1.0):
    \"\"\"Pairwise probabilistic loss (RankNet).
    S_ij: +1 if i truly preferred, -1 if j preferred, 0 if tie.
    \"\"\"
    P_bar = 0.5 * (1.0 + S_ij)                       # target probability
    diff = sigma * (s_i - s_j)
    # numerically stable log(1+exp(-diff))
    C = np.log1p(np.exp(-np.abs(diff))) + np.maximum(-diff, 0) - np.maximum(-diff, 0)
    C = P_bar * np.log1p(np.exp(-diff)) + (1 - P_bar) * (diff + np.log1p(np.exp(-diff)))
    grad_i = sigma * (P_bar - 1.0 / (1.0 + np.exp(-diff)))  # dC/ds_i
    return C.mean(), grad_i, -grad_i


def listnet_loss(scores, relevances):
    \"\"\"Listwise top-one cross-entropy (ListNet). scores/relevances: (n,)\"\"\"
    def softmax(x):
        x = x - x.max()
        e = np.exp(x)
        return e / e.sum()
    P_s = softmax(scores)
    P_y = softmax(relevances.astype(np.float64))
    loss = -np.sum(P_y * np.log(P_s + 1e-12))
    grad = P_s - P_y                                  # dL/ds_j
    return loss, grad


def ndcg_at_k(relevances_in_rank_order, k=None):
    \"\"\"relevances_in_rank_order: relevance grades sorted by predicted rank.\"\"\"
    rel = np.array(relevances_in_rank_order, dtype=np.float64)
    k = len(rel) if k is None else k
    discounts = 1.0 / np.log2(np.arange(2, k + 2))
    dcg = np.sum((2 ** rel[:k] - 1) * discounts)
    ideal = np.sort(rel)[::-1]
    idcg = np.sum((2 ** ideal[:k] - 1) * discounts)
    return dcg / idcg if idcg > 0 else 0.0


def lambda_gradient(s_i, s_j, delta_ndcg, sigma=1.0):
    \"\"\"LambdaRank pairwise gradient, scaled by |ΔNDCG| if pair i,j swapped.\"\"\"
    return -sigma * abs(delta_ndcg) / (1.0 + np.exp(sigma * (s_i - s_j)))
"""),
    heading3("6b — Production Usage (PyTorch / LightGBM)"),
    code_block("python", """import torch
import torch.nn as nn

# Margin Ranking Loss — built into PyTorch
loss_fn = nn.MarginRankingLoss(margin=1.0)
s_pos = torch.tensor([0.9, 0.6])   # relevant doc scores
s_neg = torch.tensor([0.3, 0.5])   # irrelevant doc scores
target = torch.ones_like(s_pos)     # +1 means s_pos should exceed s_neg
loss = loss_fn(s_pos, s_neg, target)
# ⚠️ Gotcha: target=1 means arg1 should rank ABOVE arg2 — flipping args silently
# reverses "preferred" without an error.

# LambdaMART in production: LightGBM's built-in "lambdarank" objective
import lightgbm as lgb
train_data = lgb.Dataset(
    X_train, label=y_train,
    group=group_sizes,          # number of docs per query, MUST sum to len(X_train)
)
params = {
    "objective": "lambdarank",
    "metric": "ndcg",
    "ndcg_eval_at": [5, 10],
    "lambdarank_truncation_level": 30,  # cap pairs per query for speed
}
model = lgb.train(params, train_data, num_boost_round=200)
# ⚠️ Gotcha: `group` must exactly partition the rows in query order — a mismatch
# silently corrupts which documents get paired together.
"""),
    callout("⚠️", rt("Gotcha: ", bold=True), rt(
        "Pairwise/listwise losses need query GROUPING — documents from different queries must "
        "never be paired together. Forgetting to pass `group`/`qid` is the #1 bug in learning-"
        "to-rank pipelines and silently produces a nonsensical (but numerically valid) loss."
    )),
    divider(),

    # ── Section 7: Interview Deep-Dive ──
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q&A (Easy → Hard)"),
    numbered(rt("Q (Easy): ", bold=True), rt("Why not just use MSE regression on relevance grades for ranking? "), rt("A: MSE treats every document independently and penalizes score-magnitude errors uniformly, but ranking quality only depends on RELATIVE order — MSE can be low while the top-1 position is wrong, which is what users actually see.")),
    numbered(rt("Q (Easy): ", bold=True), rt("What does Margin Ranking Loss compute? "), rt("A: Hinge loss on the score gap between a preferred and non-preferred item: "), eq(r"\max(0, m-(s^+-s^-))"), rt(" — zero once separation exceeds the margin.")),
    numbered(rt("Q (Medium): ", bold=True), rt("How does RankNet differ from Margin Ranking Loss? "), rt("A: RankNet uses a smooth, probabilistic cross-entropy loss (via sigmoid of the score gap) that never fully saturates to zero, whereas margin loss is a hard hinge that zeroes out once the margin is satisfied.")),
    numbered(rt("Q (Medium): ", bold=True), rt("What's the core limitation of RankNet that LambdaRank fixes? "), rt("A: RankNet weighs every pair equally regardless of its position in the ranked list, so it doesn't correlate tightly with NDCG (which is dominated by top-rank errors). LambdaRank multiplies each pair's gradient by "), eq(r"|\Delta\text{NDCG}|"), rt(" if that pair were swapped.")),
    numbered(rt("Q (Hard): ", bold=True), rt("How can LambdaRank optimize NDCG if NDCG isn't differentiable? "), rt("A: It never differentiates NDCG. It DEFINES a gradient-like quantity "), eq(r"\lambda_{ij}"), rt(" directly as the RankNet gradient scaled by "), eq(r"|\Delta\text{NDCG}_{ij}|"), rt(", proven (empirically/via Donmez et al.) to locally optimize NDCG at convergence.")),
    numbered(rt("Q (Hard): ", bold=True), rt("Why does ListNet use only the TOP-ONE Plackett-Luce probability instead of full permutation probability? "), rt("A: Full permutation probability requires "), eq(r"O(n!)"), rt(" terms; the top-one marginal reduces this to "), eq(r"O(n)"), rt(" while remaining a valid probability distribution, trading some listwise fidelity for tractability.")),
    numbered(rt("Q (Hard): ", bold=True), rt("What is LambdaMART, and why do search engines use it more than neural rankers? "), rt("A: LambdaMART = LambdaRank's λ-gradients used as pseudo-residuals fit by gradient-boosted regression trees (MART) instead of a neural net. GBDTs handle heterogeneous, sparse, tabular ranking features (BM25 scores, click features, etc.) better than dense neural nets and remain a strong, fast, interpretable baseline — this combo won multiple Yahoo/Microsoft LTR challenges.")),
    heading3("Follow-up Traps"),
    callout("🚨", rt("\"So pairwise losses are strictly worse than listwise?\" ", bold=True), rt(
        "No — pairwise losses (esp. LambdaMART) remain the industry standard because they're "
        "cheaper, work naturally with GBDTs, and LambdaRank's NDCG-weighting closes most of the "
        "gap to listwise methods. Pure listwise losses (ListNet, ApproxNDCG) are more common in "
        "neural, end-to-end differentiable pipelines."
    )),
    heading3("Explain to a PhD Researcher"),
    para(rt(
        "Ranking losses can be unified as approximations to Bayes-optimal ranking under 0/1 "
        "pairwise disagreement loss (pairwise) or the expected reciprocal rank / NDCG risk "
        "(listwise). RankNet's cross-entropy is a convex surrogate for pairwise misranking; "
        "LambdaRank's λ-gradients are a heuristic but empirically strong local approximation "
        "to the true (non-differentiable, piecewise-constant) NDCG gradient, later formalized "
        "via the LambdaLoss framework (Wang et al. 2018) as optimizing a valid, metric-driven "
        "upper bound."
    )),
    heading3("Explain to a Research Scientist / Engineer"),
    para(rt(
        "In practice: start with LambdaMART (LightGBM/XGBoost `rank:pairwise` or "
        "`lambdarank` objective) for tabular ranking features — it's fast, robust, and "
        "directly optimizes NDCG. Move to neural listwise losses (ListNet/ApproxNDCG/"
        "softmax cross-entropy over the list) only when you need end-to-end feature "
        "learning (e.g., from raw text/embeddings) that GBDTs can't do."
    )),
    heading3("System Design Angle"),
    para(rt(
        "In a search/recsys pipeline, ranking losses train the SECOND-stage ranker (after a "
        "cheap first-stage retrieval/candidate-generation step). Training data comes from "
        "click logs or human relevance judgments, grouped by query, with position bias "
        "correction often applied (e.g., via IPS weighting) before the pairwise/listwise loss "
        "is computed — otherwise the model learns to prefer whatever was shown in position 1, "
        "not what's actually most relevant."
    )),
    heading3("Red Flags"),
    bullet(rt("Saying \"just use MSE, it's simpler\" without acknowledging the order-vs-magnitude distinction.")),
    bullet(rt("Forgetting that pairs/lists must be grouped by query — mixing documents across queries.")),
    bullet(rt("Claiming LambdaRank differentiates NDCG directly — it doesn't; it defines a heuristic gradient.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ──
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Dimension", "Pointwise (MSE)", "Margin Ranking / RankNet (Pairwise)", "ListNet (Listwise)", "LambdaRank / LambdaMART"]),
        table_row(["Optimizes", "Absolute score error", "Pairwise order", "Full-list top-1 distribution", "Pairwise order, NDCG-weighted"]),
        table_row(["NDCG correlation", "Weak", "Moderate", "Good", "Strongest (directly metric-aware)"]),
        table_row(["Compute cost / query", "O(n)", "O(n²) pairs (often subsampled)", "O(n)", "O(n²) pairs, but prunable"]),
        table_row(["Common implementation", "sklearn regressors", "PyTorch MarginRankingLoss, RankNet", "TF-Ranking, custom softmax-CE", "LightGBM/XGBoost lambdarank, LambdaMART"]),
        table_row(["Handles non-differentiable metrics", "No", "No", "No (approximates via top-1 CE)", "Yes (heuristic λ-gradient)"]),
    ),
    heading3("When to Use"),
    bullet(rt("Margin Ranking Loss: ", bold=True), rt("simple binary preference data (e.g., \"A clicked over B\"), small feature sets, quick baselines, or metric-learning/embedding tasks (e.g., face verification, RLHF reward models).")),
    bullet(rt("RankNet: ", bold=True), rt("when you need a smooth, probabilistic pairwise signal — historically used before LambdaRank existed, still useful as a stepping stone.")),
    bullet(rt("ListNet: ", bold=True), rt("neural, end-to-end rankers where you want full-list context per training step and mild NDCG awareness.")),
    bullet(rt("LambdaRank / LambdaMART: ", bold=True), rt("production search/ads/recsys ranking with tabular features — the default strong baseline (LightGBM/XGBoost).")),
    heading3("When NOT to Use"),
    bullet(rt("Any pairwise/listwise loss when you have NO relative preference signal (only absolute labels with no comparison structure) — pointwise is simpler and sufficient.")),
    bullet(rt("Naive full listwise (ListMLE, full permutation probability) at large "), eq(r"n"), rt(" per query — factorial blowup.")),
    heading3("Advantages / Disadvantages"),
    bullet(rt("Pairwise pros: ", bold=True), rt("simple, well-understood, works with any base model (linear, tree, neural); cons: ignores list-level context, equal weight per pair unless reweighted.")),
    bullet(rt("Listwise pros: ", bold=True), rt("captures full-list structure in one loss term, most metric-aligned; cons: more expensive, harder to implement/debug, ListNet's top-1 approximation loses some full-order information.")),
    callout("🎯", rt("Decision: ", bold=True), rt(
        "Tabular features + need production speed → LambdaMART (GBDT). Need end-to-end neural "
        "feature learning + strong NDCG alignment → neural listwise (ApproxNDCG/ListNet/"
        "LambdaLoss). Quick baseline or embedding/metric learning → Margin Ranking Loss."
    )),
    divider(),

    # ── Section 9: Explainer Embed ──
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/AI/explainers/ranking_losses_explainer.html"),
    para(rt("Step through pointwise → margin ranking → RankNet → ListNet → LambdaRank, with real numbers and NDCG, using Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Binary Cross-Entropy Loss")),
    bullet(rt("Sigmoid & Softmax Functions")),
    bullet(rt("Gradient Boosted Trees (GBDT) / MART")),
    bullet(rt("Evaluation Metrics: NDCG, MRR, MAP")),
    heading3("What to Learn Next"),
    bullet(rt("LambdaLoss framework (metric-driven loss unification)")),
    bullet(rt("Two-tower retrieval models & contrastive/triplet losses")),
    bullet(rt("Position bias correction & counterfactual learning to rank (IPS)")),
    bullet(rt("Neural re-ranking (BERT cross-encoders, TF-Ranking)")),
    heading3("Key Papers"),
    bullet(rt("Burges et al. (2005) — \"Learning to Rank using Gradient Descent\" (RankNet), ICML.")),
    bullet(rt("Cao et al. (2007) — \"Learning to Rank: From Pairwise Approach to Listwise Approach\" (ListNet), ICML.")),
    bullet(rt("Burges (2010) — \"From RankNet to LambdaRank to LambdaMART: An Overview\", MSR-TR.")),
    bullet(rt("Wang et al. (2018) — \"The LambdaLoss Framework for Ranking Metric Optimization\", CIKM.")),
    bullet(rt("Joachims et al. (2017) — \"Unbiased Learning-to-Rank with Biased Feedback\" (position bias / IPS), WSDM.")),
    heading3("Best Resources"),
    bullet(rt("Microsoft Research: \"From RankNet to LambdaRank to LambdaMART\" technical report (definitive reference).")),
    bullet(rt("LightGBM & XGBoost official docs: `lambdarank` / `rank:pairwise` / `rank:ndcg` objectives.")),
    bullet(rt("TensorFlow Ranking (TF-Ranking) library docs and tutorials for neural listwise losses.")),
    callout("🕸️", rt("This topic connects to: ", bold=True), rt(
        "Search & Information Retrieval, Recommender Systems, RLHF reward modeling (pairwise "
        "preference losses), Metric/Contrastive Learning, and Gradient Boosted Trees."
    )),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
print("SUCCESS: ranking_losses Notion page updated.")
