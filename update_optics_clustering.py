#!/usr/bin/env python3
"""Update Notion page for: OPTICS (Ordering Points To Identify Clustering Structure)
   Corrected: minPts=2 used in numerical trace (cd = distance to 2nd nearest neighbor).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81fa-81c4-fdb1f17a67b5"
ICON = "🟡"  # Intermediate depth
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/optics_clustering_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: The 30-Second Version ──────────────────────────────
    heading2("The 30-Second Version"),
    heading3("What is this?"),
    para(rt("OPTICS (Ordering Points To Identify the Clustering Structure) is a density-based clustering algorithm that arranges data points into a special order that reveals cluster structure at multiple density scales simultaneously — without requiring you to pick a specific neighborhood radius (epsilon). Its signature output is a reachability plot: a bar chart where valleys correspond to clusters.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine scanning a city from satellite and building an elevation profile of population density. Dense downtown blocks sit in deep valleys; sparse suburbs sit at modest heights; isolated farmhouses spike to towering heights. You can slice horizontally at any density threshold to reveal the corresponding neighborhood structure. OPTICS builds exactly this density-elevation profile for your data.")),
    heading3("One-Sentence Summary"),
    para(rt("OPTICS orders data points by density-reachability so that clusters appear as consecutive valleys in a reachability plot, generalizing DBSCAN across all epsilon simultaneously.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("OPTICS produces a reachability plot where valleys = clusters. Deeper valleys = denser clusters. Choose any slope threshold xi to extract clusters — it replaces the brittle epsilon parameter of DBSCAN.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────
    heading2("Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("DBSCAN (1996) was a breakthrough: it found arbitrary-shaped clusters and handled noise, requiring only two parameters — epsilon (radius) and minPts. But DBSCAN has a fundamental weakness: it uses a single global epsilon. Real-world datasets often contain clusters of widely different densities. A tight city-centre cluster and a loose suburban cluster cannot both be found by a single epsilon — tighten epsilon and you miss the sparse cluster; loosen epsilon and the dense clusters merge.")),
    heading3("What Came Before"),
    para(rt("DBSCAN (Ester et al., 1996) required setting epsilon manually. Single-linkage hierarchical clustering handles multi-scale density but runs in O(n^3) and produces dendrograms requiring manual cutting. K-Means requires spherical clusters and a fixed k.")),
    heading3("The Breakthrough"),
    para(rt("Ankerst, Breunig, Kriegel, and Sander published 'OPTICS: Ordering Points To Identify the Clustering Structure' at SIGMOD 1999. The key insight: instead of extracting clusters at one epsilon, produce a reachability ordering of all points. Two new quantities — the core distance and the reachability distance — encode the local density. Points belonging to the same cluster appear consecutively with low reachability values (valleys), while inter-cluster transitions create spikes.")),
    heading3("Evolution Timeline"),
    bullet(rt("1996: DBSCAN — density clustering, fixed epsilon, minPts")),
    bullet(rt("1999: OPTICS — reachability ordering, generalizes DBSCAN for all epsilon")),
    bullet(rt("2013: HDBSCAN (Campello et al.) — same hierarchy more efficiently, adds soft cluster probabilities")),
    bullet(rt("2017+: HDBSCAN adopted into sklearn; becomes standard over OPTICS for large data")),
    heading3("Before vs After Comparison"),
    table(4,
        table_row(["Dimension", "DBSCAN (Before)", "OPTICS (After)", "Improvement"]),
        table_row(["Multi-scale density", "Single epsilon only", "All epsilon simultaneously", "No re-running needed"]),
        table_row(["Parameter sensitivity", "Very sensitive to epsilon", "Robust — xi post-hoc", "Easier to tune"]),
        table_row(["Output", "Hard cluster labels", "Reachability plot", "Visual interpretability"]),
        table_row(["Varying-density clusters", "Misses sparse clusters", "Detects both", "Core advantage"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────
    heading2("Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Let "), eq(r"\mathcal{D}"), rt(" be a dataset with distance function "), eq(r"\text{dist}: \mathcal{D} \times \mathcal{D} \to \mathbb{R}_{\geq 0}"), rt(". Fix "), eq(r"\text{minPts} \in \mathbb{N}"), rt(".")),
    heading3("Core Distance"),
    para(rt("The "), rt("core distance", bold=True), rt(" of a point "), eq(r"p"), rt(" is the distance to its minPts-th nearest neighbor:")),
    equation_block(r"\text{cd}_{\text{minPts}}(p) = \text{dist}(p,\; o_{\text{minPts}})"),
    para(rt("where "), eq(r"o_{\text{minPts}}"), rt(" is the minPts-th nearest neighbor of "), eq(r"p"), rt(". Unlike DBSCAN, no global epsilon is fixed — core distance is simply the distance to the minPts-th nearest neighbor in the full dataset.")),
    heading3("Reachability Distance"),
    para(rt("The "), rt("reachability distance", bold=True), rt(" from point "), eq(r"p"), rt(" with respect to core point "), eq(r"o"), rt(" is:")),
    equation_block(r"\text{rd}_{\text{minPts}}(p, o) = \max\!\left(\text{cd}_{\text{minPts}}(o),\; \text{dist}(p, o)\right)"),
    para(rt("The max() ensures that within a core point's dense neighborhood, all reachability distances are floored to at least the core distance — preventing false merging of clusters at sub-core-distance scales.")),
    heading3("The Core Property"),
    callout("🔑", rt("Key Invariant: ", bold=True), rt("Points within the same dense cluster appear consecutively in the OPTICS ordering with low reachability distances. Inter-cluster transitions and noise points appear with high reachability distances. The reachability plot is a topology-preserving projection of the dataset's density structure.")),
    heading3("Prerequisites"),
    bullet(rt("Euclidean distance and k-nearest neighbor queries")),
    bullet(rt("DBSCAN concepts: epsilon-neighborhood, core points, density connectivity")),
    bullet(rt("Priority queues (min-heap) for efficient seed management")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ────────────────────
    heading2("Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("Algorithm Structure"),
    para(rt("OPTICS processes each point exactly once. It maintains an ordered list of processed points and a priority queue (the 'seeds' or 'OrderSeeds') of candidate points sorted by their current best reachability distance.")),
    numbered(rt("Compute pairwise distances (or use k-d tree / ball tree for scalability)")),
    numbered(rt("Compute core distance for every point: distance to minPts-th nearest neighbor")),
    numbered(rt("Initialize: all reachability distances = infinity, all points unprocessed")),
    numbered(rt("For each unprocessed point p (outer loop): output p with rd=infinity (cluster boundary marker); if p is a core point, call update(p)")),
    numbered(rt("update(p): for each unprocessed point q, compute new_rd = max(cd(p), dist(p,q)). If new_rd < current_rd(q), update and insert q into seeds")),
    numbered(rt("Inner loop: extract minimum-rd point q from seeds, output it, call update(q)")),
    numbered(rt("Repeat until all points are processed")),
    heading3("Numerical Trace (7 Points, minPts=2)"),
    para(rt("Dataset: A=(1,2), B=(2,2), C=(2,3), D=(8,7), E=(8,8), F=(7,8), N=(25,80). With minPts=2 (core distance = distance to 2nd nearest neighbor):")),
    para(rt("Core distances:")),
    bullet(rt("cd(A) = dist(A, 2nd-nearest=C) = sqrt((1-2)^2+(2-3)^2) = sqrt(2) = 1.414")),
    bullet(rt("cd(B) = dist(B, 2nd-nearest=A or C) = 1.000")),
    bullet(rt("cd(C) = dist(C, 2nd-nearest=A) = sqrt(2) = 1.414")),
    bullet(rt("cd(D) = 1.414, cd(E) = 1.000, cd(F) = 1.414")),
    bullet(rt("cd(N) = dist(N, 2nd-nearest=F) = 74.216 (isolated noise point)")),
    para(rt("OPTICS ordering starting from A:")),
    table(4,
        table_row(["Order", "Point", "rd (reachability)", "Explanation"]),
        table_row(["1", "A", "infinity", "Start of run — cluster boundary marker"]),
        table_row(["2", "B", "1.414", "max(cd(A)=1.414, dist(A,B)=1.0) = 1.414"]),
        table_row(["3", "C", "1.000", "max(cd(B)=1.0, dist(B,C)=1.0) = 1.000"]),
        table_row(["4", "F", "7.071", "max(cd(C)=1.414, dist(C,F)=7.071) = 7.071 (inter-cluster spike)"]),
        table_row(["5", "D", "1.414", "max(cd(F)=1.414, dist(F,D)=1.414) = 1.414"]),
        table_row(["6", "E", "1.414", "max(cd(D)=1.414, dist(D,E)=1.0) = 1.414"]),
        table_row(["7", "N", "73.980", "max(cd(E)=1.0, dist(E,N)=73.98) = 73.98 (noise spike)"]),
    ),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("High dimensions: distance concentrations degrade neighborhood structure (use dimensionality reduction first)")),
    bullet(rt("Very different cluster sizes: minPts must be small enough to capture sparse clusters but large enough to avoid noise sensitivity")),
    bullet(rt("Equal-distance ties: implementation-dependent ordering may cause minor variation (use stable sort)")),
    bullet(rt("Disconnected seeds: if core distances are very large, the priority queue may be empty before all points are processed — the outer loop correctly handles this by starting new cluster runs")),
    divider(),

    # ── Section 5: The Math ────────────────────────────────────────────
    heading2("The Math Behind OPTICS"),
    heading3("Complete Formal Definitions"),
    para(rt("Given "), eq(r"\mathcal{D}"), rt(", distance function "), eq(r"d"), rt(", and "), eq(r"\text{minPts}"), rt(":")),
    equation_block(r"\text{cd}_{\text{minPts}}(p) = d\!\left(p,\; N_{\text{minPts}}(p)\right)"),
    para(rt("where "), eq(r"N_{\text{minPts}}(p)"), rt(" is the minPts-th nearest neighbor (by sorted distance). For the reachability distance:")),
    equation_block(r"\text{rd}_{\text{minPts}}(p, o) = \max\!\left(\text{cd}_{\text{minPts}}(o),\; d(p, o)\right)"),
    heading3("Why max() Is Necessary — Proof Sketch"),
    para(rt("Suppose two clusters "), eq(r"C_1"), rt(" (dense, characteristic radius "), eq(r"r_1"), rt(") and "), eq(r"C_2"), rt(" (less dense, radius "), eq(r"r_2 > r_1"), rt(") share a bridging point "), eq(r"b"), rt(" between them. Without max(), a point "), eq(r"q \in C_2"), rt(" close to "), eq(r"b"), rt(" could have "), eq(r"\text{rd}(q, b) = d(q, b) < r_1"), rt(", placing "), eq(r"q"), rt(" inside "), eq(r"C_1"), rt("'s valley. The max() floors this to at least "), eq(r"\text{cd}(b) = r_2"), rt(", correctly placing "), eq(r"q"), rt(" in the higher-reachability region between the clusters.")),
    heading3("The Xi Cluster Extraction Method"),
    para(rt("Given the reachability sequence "), eq(r"(rd_1, rd_2, \ldots, rd_n)"), rt(", define steep downward and upward steps:")),
    equation_block(r"\text{steep\_drop}(i): \quad \frac{rd_i - rd_{i+1}}{rd_i} \geq \xi"),
    equation_block(r"\text{steep\_rise}(i): \quad \frac{rd_{i+1} - rd_i}{rd_{i+1}} \geq \xi"),
    para(rt("A cluster "), eq(r"C = \{p_s, \ldots, p_e\}"), rt(" is valid if bracketed by a steep drop on the left and a steep rise on the right:")),
    equation_block(r"\max_{k \in [s,e]} rd_k \leq \max(rd_s, rd_e) \cdot (1 - \xi)"),
    heading3("Relationship to DBSCAN"),
    para(rt("Theorem (Ankerst et al., 1999): For any "), eq(r"\varepsilon' \leq \varepsilon_{\max}"), rt(", the clusters obtained by running DBSCAN with parameters "), eq(r"(\varepsilon', \text{minPts})"), rt(" are equivalent to the clusters extracted from the OPTICS reachability plot with a horizontal threshold at "), eq(r"\varepsilon'"), rt(". Point "), eq(r"p"), rt(" is a core point in DBSCAN iff "), eq(r"\text{cd}(p) \leq \varepsilon'"), rt(".")),
    callout("⚠️", rt("Common Misconception: ", bold=True), rt("OPTICS does NOT produce DBSCAN clusters directly. OPTICS produces an ordering. To extract DBSCAN-equivalent clusters, apply a threshold to the reachability plot. The xi method is NOT equivalent to any single DBSCAN run — it can find nested clusters of different densities.")),
    heading3("Complexity"),
    equation_block(r"T(n) = O(n^2) \text{ (naive)}, \quad O(n \log n) \text{ (with spatial index)}"),
    para(rt("Space complexity is "), eq(r"O(n)"), rt(" for the reachability and order arrays.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────
    heading2("Code Implementation"),
    heading3("6a — From Scratch (NumPy/SciPy)"),
    code_block("python", """import numpy as np
from scipy.spatial.distance import cdist

def optics(X, min_pts=5):
    \"\"\"OPTICS from scratch. Returns (order, reachability_dists, core_dists).\"\"\"
    n = len(X)
    D = cdist(X, X)  # O(n^2) pairwise distances

    # Core distances: dist to min_pts-th nearest neighbor
    # sorted ascending, exclude self (dist=0 at index 0)
    sorted_D = np.sort(D, axis=1)
    core_dists = sorted_D[:, min_pts]  # index min_pts = (min_pts+1)-th column incl self

    reach_dists = np.full(n, np.inf)
    processed = np.zeros(n, dtype=bool)
    order = []
    seeds = {}  # {point_index: reachability_dist}

    def update(idx):
        cd = core_dists[idx]
        if cd == np.inf:
            return
        for j in range(n):
            if processed[j]: continue
            new_rd = max(cd, D[idx, j])
            if new_rd < reach_dists[j]:
                reach_dists[j] = new_rd
                seeds[j] = new_rd

    for start in range(n):
        if processed[start]: continue
        processed[start] = True
        order.append(start)
        update(start)
        while seeds:
            q = min(seeds, key=seeds.get)
            del seeds[q]
            processed[q] = True
            order.append(q)
            update(q)

    reach_plot = [reach_dists[i] for i in order]
    return order, reach_plot, core_dists


def extract_clusters_threshold(order, reach_plot, eps):
    \"\"\"DBSCAN-equivalent extraction using eps threshold.\"\"\"
    labels = np.full(len(order), -1)
    cluster_id = -1
    for i, pt in enumerate(order):
        if reach_plot[i] > eps:
            cluster_id += 1
        labels[pt] = cluster_id
    return labels"""),
    heading3("6b — Production Usage (sklearn)"),
    code_block("python", """from sklearn.cluster import OPTICS
import numpy as np

# xi method (recommended)
clust = OPTICS(
    min_samples=5,           # minPts
    xi=0.05,                 # steepness threshold (0.01-0.1 typical)
    min_cluster_size=0.05,   # minimum cluster size as fraction of n
    metric='euclidean',
    algorithm='auto',        # 'ball_tree' for Euclidean, 'kd_tree' for low-dim
    n_jobs=-1,
)
clust.fit(X)

labels        = clust.labels_        # -1 = noise
reachability  = clust.reachability_  # reachability distances (by original index)
ordering      = clust.ordering_      # point indices in OPTICS order

# Visualize reachability plot
import matplotlib.pyplot as plt
plt.bar(range(len(X)), clust.reachability_[clust.ordering_],
        color='steelblue', width=1)
plt.xlabel('OPTICS Order'); plt.ylabel('Reachability Distance')
plt.title('OPTICS Reachability Plot — Valleys = Clusters')
plt.tight_layout(); plt.show()

# DBSCAN-equivalent extraction
clust2 = OPTICS(min_samples=5, cluster_method='dbscan', eps=0.5)
clust2.fit(X)

# Gotcha: reachability_ is indexed by ORIGINAL point index, not ordering.
# Always use reachability_[ordering_] to get the plot in visit order.
# Gotcha: xi method may find zero clusters if xi is too large or
#         min_cluster_size is too big — reduce both."""),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────
    heading2("Interview Deep-Dive"),
    heading3("Q1 (Easy): What is the reachability distance and why does it use max()?"),
    para(rt("The reachability distance rd(p, o) = max(cd(o), dist(p, o)) from point p to core point o measures how hard it is to reach p from o. The max() prevents reachability from being smaller than the core distance of the source — this ensures that within a dense cluster, all transitions are at least as large as the cluster's local density scale. Without max(), two tight clusters connected by a single short-distance bridge could appear to merge in the reachability plot.")),
    heading3("Q2 (Medium): How does OPTICS generalize DBSCAN?"),
    para(rt("DBSCAN runs with a fixed epsilon and reports clusters at that density level. OPTICS produces a reachability ordering that encodes the DBSCAN clustering for ALL values of epsilon simultaneously. Applying a horizontal threshold at height epsilon' to the OPTICS reachability plot yields exactly the DBSCAN clustering with parameter epsilon'. This means running OPTICS once avoids the need to re-run DBSCAN for different epsilon values during parameter exploration.")),
    heading3("Q3 (Hard): Explain the xi method vs threshold cut."),
    para(rt("A threshold cut applies a fixed horizontal line at height epsilon — any bar below epsilon is in a cluster. This is equivalent to a single DBSCAN run. The xi method detects steep downward and upward gradients in the reachability sequence. A cluster is formed between a steep drop (reachability falls by factor >= xi) and a matching steep rise. This enables detecting nested clusters of different densities that no single epsilon can capture — the fundamental advantage over DBSCAN.")),
    heading3("Q4 (Hard): OPTICS vs HDBSCAN tradeoffs?"),
    para(rt("Both build the same density reachability hierarchy. OPTICS uses a priority-queue sweep, running in O(n^2) naive or O(n log n) with spatial indexing. HDBSCAN builds the full minimum spanning tree over the mutual reachability graph first, then extracts the cluster hierarchy via single-linkage condensation. HDBSCAN scales better (O(n log n)) and also provides soft membership probabilities per point. The resulting hierarchical clusters are equivalent, but HDBSCAN is preferred for production on large datasets.")),
    heading3("Multi-Level Explanations"),
    heading3("Explain to a PhD Researcher:"),
    para(rt("OPTICS constructs a reachability ordering over the dataset by iteratively expanding the minimum mutual reachability distance in a priority queue. The resulting reachability sequence is monotonically related to the 1-linkage distance of the density-connected components at each epsilon. The xi extraction corresponds to finding maximal intervals where the slope satisfies the steepness condition — a form of scale-space blob detection on the 1D reachability signal. The theoretical guarantees (Lemma 2, Ankerst 1999) show that density-connected sets in DBSCAN(epsilon) are exactly the intervals with max rd <= epsilon.")),
    heading3("Explain to a Research Scientist/Engineer:"),
    para(rt("Think of OPTICS as building a dendrogram via a greedy nearest-neighbor sweep. It's a priority queue algorithm: always expand to the closest reachable unvisited point. The reachability plot is a 1D projection of the cluster hierarchy. For production, use HDBSCAN instead — same theory, faster implementation, and you get cluster membership probabilities. OPTICS is most useful when you need the reachability plot for visual inspection or when exploring multiple epsilon thresholds.")),
    heading3("System Design Angle"),
    para(rt("In an ML pipeline, OPTICS fits into exploratory data analysis and customer segmentation. Run OPTICS once on a subsample to produce the reachability plot; inspect it to pick epsilon or xi; then run DBSCAN with that epsilon on the full dataset for efficiency. For streaming data, OPTICS does not naturally extend — use microcluster-based methods like DenStream instead.")),
    callout("🚩", rt("Red Flags: ", bold=True), rt("Saying OPTICS is 'DBSCAN with a different parameter' — OPTICS finds clusters at ALL densities simultaneously. Confusing the reachability ordering index with the original data index. Forgetting that infinity reachability marks the START of a new cluster run, not noise.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────
    heading2("Comparison & Trade-offs"),
    table(6,
        table_row(["Dimension","OPTICS","DBSCAN","K-Means","HDBSCAN","Agglomerative"]),
        table_row(["Cluster shapes","Arbitrary","Arbitrary","Spherical","Arbitrary","Arbitrary"]),
        table_row(["Number of clusters","Auto","Auto","Fixed k","Auto","Fixed k or auto"]),
        table_row(["Multi-scale density","Yes (all epsilon)","No (single epsilon)","No","Yes (hierarchical)","Partial"]),
        table_row(["Handles noise","Yes","Yes","No","Yes (soft)","No"]),
        table_row(["Key parameter","minPts + xi","epsilon + minPts","k","minPts + min_cluster_size","linkage + distance"]),
        table_row(["Time complexity","O(n^2) naive","O(n^2) naive","O(nki)","O(n log n)","O(n^2 log n)"]),
        table_row(["Output","Reachability plot + labels","Labels","Labels","Labels + probabilities","Dendrogram + labels"]),
        table_row(["Best for","Varying density, exploration","Known epsilon, large n","Spherical equal-density","Varying density, production","Hierarchical structure"]),
    ),
    heading3("When to Use OPTICS"),
    bullet(rt("Clusters of widely different densities (the canonical use case)")),
    bullet(rt("Exploratory analysis — inspect the reachability plot before committing to parameters")),
    bullet(rt("Arbitrary cluster shapes with noise/outliers")),
    bullet(rt("Moderate-sized datasets (< 100k points without spatial indexing)")),
    heading3("When NOT to Use OPTICS"),
    bullet(rt("Very large datasets (> 1M points) — prefer HDBSCAN")),
    bullet(rt("High dimensions (> 50) without prior dimensionality reduction")),
    bullet(rt("When cluster probabilities/soft assignments are needed")),
    bullet(rt("When clusters are known to be roughly spherical and equal-density — K-Means is faster")),
    callout("🎯", rt("Decision: ", bold=True), rt("Use OPTICS when exploring multi-density datasets and you want visual insight via the reachability plot. Use HDBSCAN in production for the same problem. Use DBSCAN when you already know a good epsilon. Use K-Means when clusters are spherical and k is known.")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ────────────────────────
    heading2("Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through OPTICS point-by-point and watch the reachability plot build — valleys reveal the two dense clusters. Use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ─────────────────────────────────────
    heading2("Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("DBSCAN — OPTICS is a direct generalization; understand epsilon-neighborhoods and core points first")),
    bullet(rt("Distance metrics (Euclidean, Manhattan, Minkowski)")),
    bullet(rt("K-Nearest Neighbor search and spatial data structures (k-d trees, ball trees)")),
    bullet(rt("Priority queues / min-heaps")),
    heading3("What to Learn Next"),
    bullet(rt("HDBSCAN — production-ready successor with soft memberships and O(n log n) complexity")),
    bullet(rt("Hierarchical Clustering (Agglomerative) — related hierarchical structure, different merging")),
    bullet(rt("Density estimation (KDE) — the statistical foundation of density-based clustering")),
    bullet(rt("Silhouette score and DBCV — evaluation metrics for density-based clustering")),
    heading3("Key Papers"),
    bullet(rt("Ankerst M., Breunig M., Kriegel H.-P., Sander J. (1999). 'OPTICS: Ordering Points To Identify the Clustering Structure.' SIGMOD. — Original paper introducing OPTICS.")),
    bullet(rt("Ester M., Kriegel H.-P., Sander J., Xu X. (1996). 'A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise.' KDD. — DBSCAN predecessor.")),
    bullet(rt("Campello R.J.G.B., Moulavi D., Sander J. (2013). 'Density-Based Clustering Based on Hierarchical Density Estimates.' PAKDD. — HDBSCAN, the modern successor.")),
    bullet(rt("Schubert E. et al. (2017). 'DBSCAN Revisited, Revisited.' ACM TODS. — Practical guidance on density-based clustering parameter selection.")),
    heading3("Best Resources"),
    bullet(rt("scikit-learn documentation: sklearn.cluster.OPTICS — includes excellent reachability plot examples")),
    bullet(rt("Ankerst et al. (1999) original paper — clearly explains the priority queue mechanics")),
    bullet(rt("hdbscan Python package documentation — for understanding the modern successor")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("DBSCAN, HDBSCAN, Mean-Shift Clustering, Hierarchical Clustering, Density Estimation (KDE), Silhouette Score, Cluster Validation Metrics")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
