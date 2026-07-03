#!/usr/bin/env python3
"""Update Notion page for: Clustering evaluation: silhouette score, Calinski-Harabasz,
Davies-Bouldin, adjusted Rand index (ARI), normalized mutual information (NMI), V-measure"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81db-9da2-d9cb5d632737"
ICON = "🟡"   # Intermediate depth
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/clustering_evaluation_explainer.html"},
}

blocks = [

    # ══════════════════════════════════════════════════════════════════
    # SECTION 1: THE 30-SECOND VERSION
    # ══════════════════════════════════════════════════════════════════
    heading2("🎯 The 30-Second Version"),

    heading3("What is this?"),
    para(rt("When a clustering algorithm groups your data, how do you know if it did a good job? Clustering evaluation metrics answer this question. Unlike supervised learning where you compare predictions to known labels, clustering is unsupervised — you often don't have 'right answers.' So we have two families of metrics: internal metrics (judge quality using only the data itself — how tight and separated are the clusters?) and external metrics (compare to ground-truth labels when they exist).")),

    heading3("Real-World Analogy"),
    para(rt("Imagine sorting a pile of mixed fruit into groups by eye. Internal evaluation is like checking your result yourself: 'Are all the apples together? Are the groups clearly separated from each other?' External evaluation is like showing your sorted piles to an expert who knows the true varieties and says 'You got 87% of them right.' Both are useful, but they measure different things.")),

    heading3("One-Sentence Summary"),
    para(rt("Clustering evaluation metrics quantify how well a clustering algorithm has partitioned data — internally via cluster compactness and separation, externally via agreement with ground-truth labels.")),

    callout("💡", rt("If you remember one thing: ", bold=True), rt("Internal metrics (silhouette, CH, DB) need no labels and measure geometric quality; external metrics (ARI, NMI, V-measure) require ground truth and measure label agreement. Silhouette ∈ [−1,1] (higher=better), CH (higher=better), DB (lower=better), ARI/NMI/V ∈ [0,1] (higher=better).")),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 2: HISTORICAL CONTEXT
    # ══════════════════════════════════════════════════════════════════
    heading2("📜 Why This Exists — Historical Context & Motivation"),

    heading3("The Problem"),
    para(rt("Early clustering algorithms (k-means appeared in the 1950s–60s via Steinhaus 1957, MacQueen 1967) had no principled way to compare outputs. Practitioners would visually inspect results or use inertia (within-cluster sum of squares) — but inertia always decreases with more clusters, making it useless for selecting k. A principled, parameter-free way to assess cluster structure was urgently needed.")),

    heading3("What Came Before"),
    para(rt("Before dedicated clustering metrics, researchers used: (1) inertia/WCSS — monotonically decreasing with k, so not helpful; (2) manual visual inspection — not scalable; (3) ad hoc domain-specific rules. The gap was a reliable, interpretable scalar score that could compare any two clustering solutions.")),

    heading3("Key Papers & Timeline"),
    para(rt("The major contributions in chronological order:")),
    numbered(rt("Caliński & Harabász (1974) — "), rt("'A dendrite method for cluster analysis,' ", italic=True), rt("Comm. in Statistics. Introduced the Calinski-Harabasz (CH) index as the ratio of between-cluster to within-cluster dispersion.")),
    numbered(rt("Davies & Bouldin (1979) — "), rt("'A cluster separation measure,' ", italic=True), rt("IEEE PAMI. Introduced the Davies-Bouldin index penalizing clusters that are large and close together.")),
    numbered(rt("Rousseeuw (1987) — "), rt("'Silhouettes: a graphical aid to the interpretation and validation of cluster analysis,' ", italic=True), rt("J. Computational & Applied Mathematics. Introduced silhouette scores — the most widely used internal metric today.")),
    numbered(rt("Hubert & Arabie (1985) — "), rt("'Comparing partitions,' ", italic=True), rt("J. Classification. Introduced the Adjusted Rand Index (ARI) correcting the Rand Index for chance agreement.")),
    numbered(rt("Vinh, Epps & Bailey (2010) — "), rt("'Information theoretic measures for clusterings comparison,' ", italic=True), rt("JMLR. Unified NMI variants and showed adjusted-for-chance formulations matter.")),
    numbered(rt("Rosenberg & Hirschberg (2007) — "), rt("'V-measure: A conditional entropy-based external cluster evaluation measure,' ", italic=True), rt("EMNLP. Introduced V-measure via homogeneity and completeness.")),

    heading3("Before vs After: The Landscape Change"),
    table(
        4,
        table_row(["Dimension", "Before (pre-1974)", "After (1974–2010)", "Modern Practice"]),
        table_row(["Internal eval", "Inertia (k-dependent)", "CH, DB, Silhouette", "Silhouette + CH combo"]),
        table_row(["External eval", "Raw Rand Index (biased)", "ARI (chance-corrected)", "ARI or NMI standard"]),
        table_row(["Interpretability", "No normalized range", "CH: no bound, DB: ≥0, Sil: [−1,1]", "Silhouette most intuitive"]),
        table_row(["Cluster count selection", "Elbow on inertia (vague)", "Silhouette plot, CH elbow", "Silhouette avg + CH"]),
        table_row(["Random baseline", "Not accounted for", "ARI corrects for chance", "ARI preferred over RI"]),
    ),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 3: CORE CONCEPTS & THEORY
    # ══════════════════════════════════════════════════════════════════
    heading2("🧠 Core Concepts & Theory"),

    heading3("Prerequisites"),
    callout("📋", rt("To understand this fully, you should know: ", bold=True), rt("(1) K-means and hierarchical clustering algorithms; (2) Distance metrics (Euclidean, cosine); (3) Entropy and mutual information (for NMI/V-measure); (4) Contingency tables (for ARI); (5) Basic probability — expected value.")),

    heading3("The Two Families"),
    para(rt("All clustering evaluation metrics fall into one of two categories:")),
    bullet(rt("Internal metrics", bold=True), rt(": Use only the data and cluster assignments. Measure geometric properties — how compact each cluster is (low intra-cluster distance) and how separated clusters are from each other (high inter-cluster distance). No ground-truth labels needed. Used when you have no labels, or to select k.")),
    bullet(rt("External metrics", bold=True), rt(": Compare predicted cluster assignments to known ground-truth labels. Treat clustering as a classification problem and measure agreement. Used in research/benchmarking when labels exist but were hidden during clustering.")),

    heading3("Key Definitions"),
    para(rt("Let "), eq(r"X = \{x_1, \ldots, x_n\}"), rt(" be "), eq(r"n"), rt(" data points. A clustering "), eq(r"C = \{C_1, \ldots, C_k\}"), rt(" partitions "), eq(r"X"), rt(" into "), eq(r"k"), rt(" disjoint clusters. Let "), eq(r"d(x,y)"), rt(" denote a distance metric (typically Euclidean).")),

    callout("🔑", rt("Key Invariant: ", bold=True), rt("A good clustering maximizes intra-cluster similarity (points within a cluster are close) and maximizes inter-cluster dissimilarity (clusters are far from each other). All internal metrics operationalize this principle differently.")),

    heading3("Metric Taxonomy at a Glance"),
    table(
        5,
        table_row(["Metric", "Family", "Range", "Direction", "Sensitive to k?"]),
        table_row(["Silhouette", "Internal", "[−1, 1]", "Higher = better", "No"]),
        table_row(["Calinski-Harabász (CH)", "Internal", "[0, ∞)", "Higher = better", "Yes (penalizes more k)"]),
        table_row(["Davies-Bouldin (DB)", "Internal", "[0, ∞)", "Lower = better", "Slight"]),
        table_row(["Adjusted Rand Index (ARI)", "External", "[−1, 1]*", "Higher = better", "No"]),
        table_row(["Normalized Mutual Info (NMI)", "External", "[0, 1]", "Higher = better", "No"]),
        table_row(["V-measure", "External", "[0, 1]", "Higher = better", "No"]),
    ),
    para(rt("*ARI can be slightly negative for random clusterings (corrects for chance), but practically lives in [0, 1] for meaningful clusterings.", italic=True)),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 4: ARCHITECTURE & INTERNAL WORKINGS — PhD DEEP DIVE
    # ══════════════════════════════════════════════════════════════════
    heading2("🔬 Architecture & Internal Workings — PhD-Level Deep Dive"),

    heading3("4.1 Silhouette Score"),
    para(rt("For each point "), eq(r"x_i"), rt(" in cluster "), eq(r"C_j"), rt(":")),
    bullet(rt("Compute "), eq(r"a(i)"), rt(" = mean distance from "), eq(r"x_i"), rt(" to all other points in the same cluster "), eq(r"C_j"), rt(". This measures intra-cluster cohesion.")),
    bullet(rt("Compute "), eq(r"b(i)"), rt(" = "), eq(r"\min_{C_\ell \neq C_j} \frac{1}{|C_\ell|}\sum_{x_m \in C_\ell} d(x_i, x_m)"), rt(". This is the mean distance to points in the nearest other cluster. Measures separation.")),
    bullet(rt("The silhouette of point "), eq(r"i"), rt(": "), eq(r"s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}")),

    para(rt("The overall silhouette score is the mean over all points: "), eq(r"\bar{s} = \frac{1}{n}\sum_{i=1}^n s(i)")),

    para(rt("Interpretation of "), eq(r"s(i)"), rt(":")),
    bullet(rt("s(i) ≈ +1: Point is well inside its cluster, far from others. Correctly assigned.")),
    bullet(rt("s(i) ≈ 0: Point is near the boundary between two clusters. Ambiguous.")),
    bullet(rt("s(i) ≈ −1: Point is closer to a neighboring cluster than its own. Likely misassigned.")),

    para(rt("Numerical trace — 3 points, 2 clusters (A={p1,p2}, B={p3}):")),
    para(rt("p1=(0,0), p2=(1,0), p3=(5,0)")),
    para(rt("For p1: a(1)=d(p1,p2)=1.0. b(1)=d(p1,p3)=5.0. s(1)=(5−1)/max(5,1)=4/5=0.80.")),
    para(rt("For p2: a(2)=d(p2,p1)=1.0. b(2)=d(p2,p3)=4.0. s(2)=(4−1)/4=0.75.")),
    para(rt("For p3 (singleton): a(3)=0 (no other points). Convention: s(3)=0.")),
    para(rt("Mean silhouette = (0.80+0.75+0.00)/3 = 0.517.")),

    callout("⚠️", rt("Design Decision — Singleton clusters: ", bold=True), rt("By convention s(i)=0 for singletons (no intra-cluster comparison possible). This is a weakness: a single-point cluster gets a neutral score rather than being penalized. Some implementations skip singletons entirely.")),

    callout("⚠️", rt("Computational cost: ", bold=True), rt("O(n²) pairwise distances. For large n (>10,000), use approximate silhouette or sample-based variants. sklearn has sample_size parameter for this.")),

    heading3("4.2 Calinski-Harabász (CH) Index — Variance Ratio Criterion"),
    para(rt("The CH index measures the ratio of between-cluster dispersion to within-cluster dispersion:")),
    equation_block(r"\text{CH}(k) = \frac{\text{SSB}/(k-1)}{\text{SSW}/(n-k)}"),
    para(rt("Where:")),
    bullet(eq(r"\text{SSB} = \sum_{j=1}^{k} |C_j| \cdot \|m_j - m\|^2"), rt(" = between-cluster sum of squares (m_j = centroid of cluster j, m = global centroid)")),
    bullet(eq(r"\text{SSW} = \sum_{j=1}^{k} \sum_{x_i \in C_j} \|x_i - m_j\|^2"), rt(" = within-cluster sum of squares")),

    para(rt("Intuition: SSB measures how far clusters are from each other (good when large). SSW measures how spread points are within clusters (good when small). Dividing by degrees of freedom (k−1) and (n−k) normalizes for the number of clusters.")),

    para(rt("Numerical trace with 6 points (2 features), 2 clusters:")),
    para(rt("A={(-2,0),(-1,0),(0,0)}, B={(3,0),(4,0),(5,0)}")),
    para(rt("m_A=(-1,0), m_B=(4,0), m_global=(1.5,0)")),
    para(rt("SSB = 3*||(-1,0)-(1.5,0)||² + 3*||(4,0)-(1.5,0)||² = 3*6.25 + 3*6.25 = 37.5")),
    para(rt("SSW = (1+0+1) + (1+0+1) = 4.0")),
    para(rt("CH = (37.5/1) / (4.0/4) = 37.5 / 1.0 = 37.5")),

    callout("⚠️", rt("Key weakness: ", bold=True), rt("CH assumes convex, equally-sized clusters. It can mislead for non-convex shapes (moons, rings) or highly imbalanced cluster sizes. It also increases monotonically with k for some datasets — the maximum is not always at the true k.")),

    heading3("4.3 Davies-Bouldin (DB) Index"),
    para(rt("For each cluster "), eq(r"C_j"), rt(", define the within-cluster scatter "), eq(r"s_j = \frac{1}{|C_j|}\sum_{x_i \in C_j} d(x_i, m_j)"), rt(" (mean distance from centroid).")),
    para(rt("The separation between clusters j and ℓ is "), eq(r"d_{j\ell} = d(m_j, m_\ell)"), rt(" (distance between centroids).")),
    para(rt("The Davies-Bouldin index is:")),
    equation_block(r"\text{DB} = \frac{1}{k}\sum_{j=1}^{k} \max_{\ell \neq j} \frac{s_j + s_\ell}{d_{j\ell}}"),
    para(rt("Intuition: For each cluster, find the worst-case neighbor — the one that has large scatter relative to how far away it is. Average this worst case over all clusters. Lower DB = better clustering.")),

    para(rt("Numerical trace (same 6 points):")),
    para(rt("s_A = mean(2,1,0) = 1.0. s_B = mean(1,0,1) = 0.667.")),
    para(rt("d(m_A, m_B) = d((-1,0),(4,0)) = 5.0.")),
    para(rt("R(A,B) = (s_A + s_B) / d(m_A,m_B) = (1.0+0.667)/5.0 = 0.333.")),
    para(rt("Since k=2: DB = (0.333 + 0.333)/2 = 0.333.")),

    callout("⚠️", rt("Design Decision — centroid vs other definitions: ", bold=True), rt("sklearn uses centroid-based scatter by default. The original paper allows any distance-based scatter. The centroid version is most common but breaks for non-Euclidean geometries.")),

    heading3("4.4 Adjusted Rand Index (ARI)"),
    para(rt("Given true labels "), eq(r"U = \{U_1,\ldots,U_r\}"), rt(" and predicted clusters "), eq(r"V = \{V_1,\ldots,V_s\}"), rt(", build the contingency table "), eq(r"n_{ij} = |U_i \cap V_j|"), rt(".")),
    para(rt("The raw Rand Index counts pairs of points that are in the same cluster in both U and V, or different clusters in both:")),
    equation_block(r"\text{RI} = \frac{a + b}{\binom{n}{2}}"),
    para(rt("where a = pairs in same group in both U and V, b = pairs in different groups in both.")),
    para(rt("The ARI corrects for chance using the hypergeometric model:")),
    equation_block(r"\text{ARI} = \frac{\sum_{ij}\binom{n_{ij}}{2} - \left[\sum_i \binom{a_i}{2}\sum_j\binom{b_j}{2}\right] / \binom{n}{2}}{\frac{1}{2}\left[\sum_i\binom{a_i}{2} + \sum_j\binom{b_j}{2}\right] - \left[\sum_i\binom{a_i}{2}\sum_j\binom{b_j}{2}\right] / \binom{n}{2}}"),
    para(rt("where "), eq(r"a_i = \sum_j n_{ij}"), rt(" (row sums) and "), eq(r"b_j = \sum_i n_{ij}"), rt(" (column sums).")),

    para(rt("Why adjust for chance? The raw RI is biased — random clusterings can achieve non-zero RI. The ARI subtracts the expected RI under a random partition model (hypergeometric null) and normalizes to [0,1] for perfect agreement. ARI=0 means performance no better than chance; ARI=1 means perfect agreement; ARI<0 means worse than random.")),

    para(rt("Numerical trace (n=6, true labels=[A,A,A,B,B,B], predicted=[X,X,Y,Y,B,B]):")),
    para(rt("Contingency table: n_AX=2, n_AY=1, n_BX=0, n_BY=1, n_BB=2.")),
    para(rt("C(2,2)+C(1,2)+C(2,2) = 1+0+1 = 2. Row sums: a=[3,3], b=[2,2,2]. C(3,2)+C(3,2)=3+3=6. C(2,2)+C(2,2)+C(2,2)=3. E[index]=(6*3)/C(6,2)=18/15=1.2.")),
    para(rt("ARI = (2 - 1.2) / ((6+3)/2 - 1.2) = 0.8/3.3 ≈ 0.24. (Rough sketch — precise computation involves all terms.)")),

    heading3("4.5 Normalized Mutual Information (NMI)"),
    para(rt("NMI is grounded in information theory. Given true labels "), eq(r"Y"), rt(" and cluster assignments "), eq(r"C"), rt(":")),
    equation_block(r"I(Y;C) = \sum_{y}\sum_{c} P(y,c)\log\frac{P(y,c)}{P(y)P(c)}"),
    equation_block(r"\text{NMI}(Y,C) = \frac{2 \cdot I(Y;C)}{H(Y) + H(C)}"),
    para(rt("where "), eq(r"H(Y) = -\sum_y P(y)\log P(y)"), rt(" is the Shannon entropy of the true label distribution and "), eq(r"H(C)"), rt(" similarly for clusters.")),

    para(rt("Intuition: Mutual information I(Y;C) measures how much knowing the cluster assignment tells you about the true label (and vice versa). Dividing by the average entropy normalizes to [0,1]. NMI=1 means perfect correspondence; NMI=0 means knowing cluster tells you nothing about true label.")),

    callout("⚠️", rt("Important: ", bold=True), rt("NMI is NOT adjusted for chance — it can overestimate quality for large k with many small clusters. sklearn's adjusted_mutual_info_score implements AMI (Adjusted Mutual Information) which corrects this. For fair comparisons across different k, use AMI instead of NMI.")),

    heading3("4.6 V-Measure"),
    para(rt("V-measure decomposes clustering quality into two complementary properties:")),
    bullet(rt("Homogeneity h"), rt(": Each cluster contains only members of a single class. "), eq(r"h = 1 - \frac{H(C|Y)}{H(C)}")),
    bullet(rt("Completeness c"), rt(": All members of a class are assigned to the same cluster. "), eq(r"c = 1 - \frac{H(Y|C)}{H(Y)}")),
    para(rt("V-measure is their harmonic mean (F1-style):")),
    equation_block(r"V_\beta = \frac{(1+\beta^2) \cdot h \cdot c}{\beta^2 \cdot h + c}"),
    para(rt("The default "), eq(r"\beta=1"), rt(" weights homogeneity and completeness equally. "), eq(r"\beta < 1"), rt(" favors homogeneity; "), eq(r"\beta > 1"), rt(" favors completeness.")),

    para(rt("Intuition analogy: Homogeneity = precision (each cluster is 'pure'), Completeness = recall (each true class is 'captured'). V-measure = F1 of clustering. High homogeneity but low completeness = algorithm created many small pure clusters but split true classes. High completeness but low homogeneity = algorithm put everything in few clusters containing many classes.")),

    callout("⚠️", rt("Relationship to NMI: ", bold=True), rt("V-measure with β=1 is mathematically equivalent to NMI when using log base 2. They are the same quantity derived from different first principles. This unification was shown by Rosenberg & Hirschberg (2007).")),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 5: THE MATH
    # ══════════════════════════════════════════════════════════════════
    heading2("📐 The Math Behind It"),

    heading3("5.1 Silhouette — Full Derivation"),
    equation_block(r"a(i) = \frac{1}{|C_{k(i)}| - 1} \sum_{j \in C_{k(i)}, j \neq i} d(x_i, x_j)"),
    equation_block(r"b(i) = \min_{\ell \neq k(i)} \frac{1}{|C_\ell|} \sum_{j \in C_\ell} d(x_i, x_j)"),
    equation_block(r"s(i) = \frac{b(i) - a(i)}{\max\{a(i), b(i)\}} = \begin{cases} 1 - a(i)/b(i) & \text{if } a(i) < b(i) \\ 0 & \text{if } a(i) = b(i) \\ b(i)/a(i) - 1 & \text{if } a(i) > b(i) \end{cases}"),
    para(rt("The three-case form makes clear that "), eq(r"s(i) \in [-1, 1]"), rt(" always. When "), eq(r"a(i) = 0"), rt(" (point exactly at centroid with unique position), "), eq(r"s(i) = 1"), rt(".")),
    para(rt("The overall score: "), eq(r"\bar{s} = \frac{1}{n}\sum_{i=1}^n s(i)"), rt(". Cluster-level silhouette: "), eq(r"\bar{s}_{C_k} = \frac{1}{|C_k|}\sum_{i \in C_k} s(i)"), rt(".")),

    heading3("5.2 Calinski-Harabász — Decomposition of Variance"),
    para(rt("The total sum of squares decomposes as "), eq(r"\text{SST} = \text{SSB} + \text{SSW}"), rt(". Defining global mean "), eq(r"m = \frac{1}{n}\sum_{i=1}^n x_i"), rt(":")),
    equation_block(r"\text{SSB} = \sum_{k=1}^{K} n_k \|m_k - m\|^2, \quad \text{SSW} = \sum_{k=1}^{K}\sum_{i \in C_k} \|x_i - m_k\|^2"),
    equation_block(r"\text{CH}(K) = \frac{n-K}{K-1} \cdot \frac{\text{SSB}}{\text{SSW}}"),
    para(rt("This is analogous to the F-statistic in ANOVA: large CH means between-group variance dominates within-group variance, i.e., clusters are well-separated relative to their internal spread.")),

    callout("📐", rt("Mathematical note: ", bold=True), rt("For K=n (each point is its own cluster): SSW=0 → CH=∞. For K=1: SSB=0 → CH=0. The maximum of CH over K provides one heuristic for choosing k.")),

    heading3("5.3 Davies-Bouldin — Formal Derivation"),
    equation_block(r"R_{ij} = \frac{s_i + s_j}{d(m_i, m_j)}, \quad D_i = \max_{j \neq i} R_{ij}"),
    equation_block(r"\text{DB} = \frac{1}{K} \sum_{i=1}^K D_i"),
    para(rt("Here "), eq(r"s_i"), rt(" can be any within-cluster measure (mean distance to centroid by default). "), eq(r"d(m_i, m_j)"), rt(" is centroid separation. The ratio "), eq(r"R_{ij}"), rt(" is high when clusters i and j are internally large (big scatter) but externally close (small separation). DB averages the worst-case ratio for each cluster.")),

    heading3("5.4 Adjusted Rand Index — Combinatorial Derivation"),
    para(rt("With contingency matrix "), eq(r"\{n_{ij}\}"), rt(", row sums "), eq(r"a_i = \sum_j n_{ij}"), rt(", column sums "), eq(r"b_j = \sum_i n_{ij}"), rt(":")),
    equation_block(r"\text{Index} = \sum_{ij}\binom{n_{ij}}{2}"),
    equation_block(r"\text{Expected Index} = \frac{\sum_i\binom{a_i}{2}\cdot\sum_j\binom{b_j}{2}}{\binom{n}{2}}"),
    equation_block(r"\text{Max Index} = \frac{\sum_i\binom{a_i}{2} + \sum_j\binom{b_j}{2}}{2}"),
    equation_block(r"\text{ARI} = \frac{\text{Index} - \text{Expected Index}}{\text{Max Index} - \text{Expected Index}}"),
    para(rt("The expected index under the hypergeometric model (random partition with fixed cluster sizes) is subtracted. This makes ARI=0 in expectation for random clusterings, regardless of n or k.")),

    callout("⚠️", rt("Common Misconception: ", bold=True), rt("ARI is symmetric: ARI(U,V)=ARI(V,U). It doesn't matter which is 'true' and which is 'predicted.' This is unlike precision/recall which are asymmetric.")),

    heading3("5.5 NMI — Information-Theoretic Foundation"),
    para(rt("Probabilities are estimated empirically: "), eq(r"P(Y=y_i) = |U_i|/n"), rt(", "), eq(r"P(C=c_j) = |V_j|/n"), rt(", "), eq(r"P(Y=y_i, C=c_j) = n_{ij}/n"), rt(".")),
    equation_block(r"H(Y) = -\sum_{i} \frac{|U_i|}{n}\log\frac{|U_i|}{n}"),
    equation_block(r"I(Y;C) = \sum_{i}\sum_{j} \frac{n_{ij}}{n}\log\frac{n \cdot n_{ij}}{|U_i||V_j|}"),
    equation_block(r"\text{NMI} = \frac{2I(Y;C)}{H(Y)+H(C)}"),
    para(rt("The data processing inequality guarantees "), eq(r"I(Y;C) \leq \min(H(Y),H(C))"), rt(", so "), eq(r"\text{NMI} \leq 1"), rt(" always. NMI=1 iff Y and C are in 1-to-1 correspondence.")),

    heading3("5.6 V-Measure — Conditional Entropy Formulation"),
    equation_block(r"h = \begin{cases} 1 & \text{if } H(C,Y)=0 \\ 1 - \frac{H(C|Y)}{H(C)} & \text{otherwise}\end{cases}"),
    equation_block(r"c = \begin{cases} 1 & \text{if } H(C,Y)=0 \\ 1 - \frac{H(Y|C)}{H(Y)} & \text{otherwise}\end{cases}"),
    equation_block(r"v = \frac{2 \cdot h \cdot c}{h + c}"),
    para(rt("Conditional entropy "), eq(r"H(C|Y) = 0"), rt(" iff knowing the true class Y completely determines the cluster assignment (perfect homogeneity). Similarly "), eq(r"H(Y|C) = 0"), rt(" iff knowing the cluster determines the true class (perfect completeness).")),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 6: CODE
    # ══════════════════════════════════════════════════════════════════
    heading2("💻 Code Implementation"),

    heading3("6a — From Scratch (NumPy)"),
    code_block("python", '''import numpy as np
from itertools import combinations
from scipy.special import comb

# ─── Silhouette Score ─────────────────────────────────────────────
def silhouette_score_scratch(X, labels):
    """
    Compute mean silhouette score from scratch.
    X: (n, d) array of data points
    labels: (n,) array of cluster assignments (integers)
    """
    n = len(X)
    unique_labels = np.unique(labels)
    k = len(unique_labels)

    # Compute full pairwise distance matrix: O(n^2 * d)
    dist = np.linalg.norm(X[:, None] - X[None, :], axis=-1)  # (n, n)

    scores = []
    for i in range(n):
        ci = labels[i]
        same_mask = (labels == ci)
        same_mask[i] = False  # exclude self

        # a(i): mean intra-cluster distance
        if same_mask.sum() == 0:
            scores.append(0.0)  # singleton cluster
            continue
        a = dist[i, same_mask].mean()

        # b(i): mean distance to nearest other cluster
        b = np.inf
        for cl in unique_labels:
            if cl == ci:
                continue
            other_mask = (labels == cl)
            mean_dist = dist[i, other_mask].mean()
            b = min(b, mean_dist)

        # s(i)
        if np.isinf(b):  # only one cluster total
            s = 0.0
        else:
            s = (b - a) / max(a, b)
        scores.append(s)

    return np.mean(scores)


# ─── Calinski-Harabász Index ──────────────────────────────────────
def calinski_harabasz_scratch(X, labels):
    """
    CH index = (SSB / (k-1)) / (SSW / (n-k))
    """
    n, d = X.shape
    unique_labels = np.unique(labels)
    k = len(unique_labels)

    global_mean = X.mean(axis=0)

    SSW = 0.0
    SSB = 0.0
    for cl in unique_labels:
        mask = (labels == cl)
        Xk = X[mask]
        nk = mask.sum()
        centroid = Xk.mean(axis=0)

        # Within-cluster SS: sum of squared distances to centroid
        SSW += ((Xk - centroid) ** 2).sum()

        # Between-cluster SS: weighted distance of centroid from global mean
        SSB += nk * ((centroid - global_mean) ** 2).sum()

    if SSW == 0:
        return np.inf  # perfect clustering

    return (SSB / (k - 1)) / (SSW / (n - k))


# ─── Davies-Bouldin Index ─────────────────────────────────────────
def davies_bouldin_scratch(X, labels):
    """
    DB = (1/k) * sum_i max_{j≠i} (s_i + s_j) / d(m_i, m_j)
    """
    unique_labels = np.unique(labels)
    k = len(unique_labels)

    centroids = []
    scatters = []
    for cl in unique_labels:
        mask = (labels == cl)
        Xk = X[mask]
        centroid = Xk.mean(axis=0)
        scatter = np.linalg.norm(Xk - centroid, axis=1).mean()
        centroids.append(centroid)
        scatters.append(scatter)
    centroids = np.array(centroids)

    DB_sum = 0.0
    for i in range(k):
        worst = -np.inf
        for j in range(k):
            if i == j:
                continue
            d_ij = np.linalg.norm(centroids[i] - centroids[j])
            if d_ij == 0:
                r = np.inf
            else:
                r = (scatters[i] + scatters[j]) / d_ij
            worst = max(worst, r)
        DB_sum += worst

    return DB_sum / k


# ─── Adjusted Rand Index ──────────────────────────────────────────
def adjusted_rand_index_scratch(true_labels, pred_labels):
    """
    ARI = (Index - Expected) / (Max - Expected)
    Uses contingency table combinatorics.
    """
    n = len(true_labels)
    true_classes = np.unique(true_labels)
    pred_classes = np.unique(pred_labels)

    # Build contingency table
    contingency = np.zeros((len(true_classes), len(pred_classes)), dtype=int)
    true_idx = {v: i for i, v in enumerate(true_classes)}
    pred_idx = {v: i for i, v in enumerate(pred_classes)}
    for t, p in zip(true_labels, pred_labels):
        contingency[true_idx[t], pred_idx[p]] += 1

    # C(n,2) combinations
    def c2(x):
        return x * (x - 1) / 2

    # Sum of C(n_ij, 2) over all cells
    sum_cij = c2(contingency).sum()

    # Row and column sums
    row_sums = contingency.sum(axis=1)
    col_sums = contingency.sum(axis=0)

    sum_ai = c2(row_sums).sum()   # sum of C(a_i, 2)
    sum_bj = c2(col_sums).sum()   # sum of C(b_j, 2)

    expected = (sum_ai * sum_bj) / c2(n)
    max_index = (sum_ai + sum_bj) / 2

    if max_index == expected:
        return 1.0  # perfect or degenerate case

    return (sum_cij - expected) / (max_index - expected)


# ─── NMI ──────────────────────────────────────────────────────────
def nmi_scratch(true_labels, pred_labels):
    """
    NMI = 2 * I(Y;C) / (H(Y) + H(C))
    """
    n = len(true_labels)
    true_classes = np.unique(true_labels)
    pred_classes = np.unique(pred_labels)

    # Contingency table
    contingency = np.zeros((len(true_classes), len(pred_classes)))
    true_idx = {v: i for i, v in enumerate(true_classes)}
    pred_idx = {v: i for i, v in enumerate(pred_classes)}
    for t, p in zip(true_labels, pred_labels):
        contingency[true_idx[t], pred_idx[p]] += 1

    P_yc = contingency / n
    P_y = P_yc.sum(axis=1, keepdims=True)
    P_c = P_yc.sum(axis=0, keepdims=True)

    # Mutual information: sum P(y,c) * log(P(y,c) / (P(y)*P(c)))
    mask = P_yc > 0
    MI = (P_yc[mask] * np.log(P_yc[mask] / (P_y * P_c)[mask])).sum()

    # Entropies
    H_y = -(P_y[P_y > 0] * np.log(P_y[P_y > 0])).sum()
    H_c = -(P_c[P_c > 0] * np.log(P_c[P_c > 0])).sum()

    if H_y + H_c == 0:
        return 1.0

    return 2 * MI / (H_y + H_c)


# ─── V-Measure ────────────────────────────────────────────────────
def v_measure_scratch(true_labels, pred_labels, beta=1.0):
    """
    V = (1+beta²)*h*c / (beta²*h + c)
    """
    n = len(true_labels)
    true_classes = np.unique(true_labels)
    pred_classes = np.unique(pred_labels)

    contingency = np.zeros((len(true_classes), len(pred_classes)))
    true_idx = {v: i for i, v in enumerate(true_classes)}
    pred_idx = {v: i for i, v in enumerate(pred_classes)}
    for t, p in zip(true_labels, pred_labels):
        contingency[true_idx[t], pred_idx[p]] += 1

    P_yc = contingency / n
    P_y = P_yc.sum(axis=1)
    P_c = P_yc.sum(axis=0)

    def entropy(probs):
        p = probs[probs > 0]
        return -(p * np.log(p)).sum()

    H_C = entropy(P_c)
    H_Y = entropy(P_y)

    # H(C|Y): conditional entropy of clusters given true labels
    H_CgY = 0.0
    for i, py in enumerate(P_y):
        if py > 0:
            row = P_yc[i] / py
            H_CgY += py * entropy(row)

    # H(Y|C): conditional entropy of true labels given clusters
    H_YgC = 0.0
    for j, pc in enumerate(P_c):
        if pc > 0:
            col = P_yc[:, j] / pc
            H_YgC += pc * entropy(col)

    h = 1 - H_CgY / H_C if H_C > 0 else 1.0
    c = 1 - H_YgC / H_Y if H_Y > 0 else 1.0

    if h + c == 0:
        return 0.0

    return (1 + beta**2) * h * c / (beta**2 * h + c)


# ─── Quick test ───────────────────────────────────────────────────
if __name__ == "__main__":
    np.random.seed(42)
    from sklearn.datasets import make_blobs
    X, y_true = make_blobs(n_samples=150, centers=3, random_state=42)

    # Perfect clustering (use true labels)
    print("=== Perfect clustering (true labels) ===")
    print(f"Silhouette:  {silhouette_score_scratch(X, y_true):.4f}")  # ~0.80
    print(f"CH Index:    {calinski_harabasz_scratch(X, y_true):.2f}")  # ~700+
    print(f"DB Index:    {davies_bouldin_scratch(X, y_true):.4f}")    # ~0.3
    print(f"ARI:         {adjusted_rand_index_scratch(y_true, y_true):.4f}")  # 1.00
    print(f"NMI:         {nmi_scratch(y_true, y_true):.4f}")           # 1.00
    print(f"V-measure:   {v_measure_scratch(y_true, y_true):.4f}")     # 1.00
'''),

    heading3("6b — Production Usage (sklearn)"),
    code_block("python", '''from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import (
    silhouette_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    adjusted_rand_score,
    normalized_mutual_info_score,
    v_measure_score,
    homogeneity_score,
    completeness_score,
)
from sklearn.datasets import make_blobs
import numpy as np

# ─── Generate data ────────────────────────────────────────────────
X, y_true = make_blobs(n_samples=300, centers=4, random_state=42)

# ─── Cluster with K-Means ─────────────────────────────────────────
km = KMeans(n_clusters=4, random_state=42, n_init=10)
y_pred = km.fit_predict(X)

# ─── Internal Metrics (no ground truth needed) ────────────────────
sil = silhouette_score(X, y_pred)
ch  = calinski_harabasz_score(X, y_pred)
db  = davies_bouldin_score(X, y_pred)
print(f"Silhouette:          {sil:.4f}  (range: [-1,1], higher=better)")
print(f"Calinski-Harabász:   {ch:.2f}   (range: [0,∞), higher=better)")
print(f"Davies-Bouldin:      {db:.4f}  (range: [0,∞), lower=better)")

# ─── External Metrics (need ground truth) ─────────────────────────
ari = adjusted_rand_score(y_true, y_pred)
nmi = normalized_mutual_info_score(y_true, y_pred, average_method="arithmetic")
vm  = v_measure_score(y_true, y_pred, beta=1.0)
h   = homogeneity_score(y_true, y_pred)
c   = completeness_score(y_true, y_pred)
print(f"ARI:                 {ari:.4f}  (range: [-1,1], higher=better)")
print(f"NMI:                 {nmi:.4f}  (range: [0,1],  higher=better)")
print(f"V-measure:           {vm:.4f}  (range: [0,1],  higher=better)")
print(f"  Homogeneity:       {h:.4f}")
print(f"  Completeness:      {c:.4f}")

# ─── Choosing k with silhouette ───────────────────────────────────
print("\\n=== Silhouette analysis to choose k ===")
for k in range(2, 7):
    km_k = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_k = km_k.fit_predict(X)
    if len(np.unique(labels_k)) < 2:
        continue
    s = silhouette_score(X, labels_k)
    ch_k = calinski_harabasz_score(X, labels_k)
    print(f"k={k}: Silhouette={s:.4f}  CH={ch_k:.1f}")
# k=4 will have the highest silhouette and CH (matching true structure)

# ─── Gotcha 1: silhouette_score requires >= 2 clusters ────────────
# sklearn will raise ValueError if labels has only 1 unique value
try:
    silhouette_score(X, np.zeros(len(X)))
except ValueError as e:
    print(f"\\nGotcha: {e}")

# ─── Gotcha 2: NMI average_method matters ─────────────────────────
# "arithmetic" is standard; "geometric" or "min" give different (often higher) values
nmi_arith    = normalized_mutual_info_score(y_true, y_pred, average_method="arithmetic")
nmi_geometric = normalized_mutual_info_score(y_true, y_pred, average_method="geometric")
print(f"\\nNMI arithmetic:  {nmi_arith:.4f}")
print(f"NMI geometric:   {nmi_geometric:.4f}  (can differ significantly)")

# ─── Gotcha 3: Large n → use sample_size for silhouette ──────────
# For n>10000, silhouette_score is O(n^2); use:
# silhouette_score(X, labels, sample_size=2000, random_state=42)
'''),

    callout("⚠️", rt("Gotcha — NMI average_method: ", bold=True), rt("sklearn's normalized_mutual_info_score has an average_method parameter ('arithmetic', 'geometric', 'min', 'max'). The Vinh et al. (2010) paper recommends 'arithmetic' for most purposes. Different choices can give substantially different values — always report which you used.")),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 7: INTERVIEW DEEP-DIVE
    # ══════════════════════════════════════════════════════════════════
    heading2("🎤 Interview Deep-Dive"),

    heading3("Questions — Easy to Hard"),

    toggle([rt("Q1 (Easy): What is the silhouette score and what does a value near −1 mean?", bold=True)], [
        para(rt("The silhouette score s(i) measures how similar a point is to its own cluster vs. the nearest other cluster. s(i) = (b(i) − a(i)) / max(a(i), b(i)), where a(i) is mean intra-cluster distance and b(i) is mean distance to nearest other cluster.")),
        para(rt("s(i) ≈ −1 means the point is much closer to a neighboring cluster than to its own cluster — it is likely misassigned. A score near +1 means the point is well-embedded in its cluster and far from others. A score near 0 means the point is on the border between two clusters.")),
    ]),

    toggle([rt("Q2 (Easy): When would you use an internal metric vs an external metric?", bold=True)], [
        para(rt("Use internal metrics (silhouette, CH, DB) when you have no ground-truth labels — the typical real-world case where clustering is exploratory. They are also used for hyperparameter tuning (selecting k) without labels.")),
        para(rt("Use external metrics (ARI, NMI, V-measure) when you DO have ground-truth labels but are testing a clustering algorithm in a research/benchmark setting. You cluster without the labels, then evaluate against them. In production with no labels, external metrics cannot be computed.")),
    ]),

    toggle([rt("Q3 (Medium): Why does the Rand Index need to be 'adjusted'? What does ARI correct for?", bold=True)], [
        para(rt("The raw Rand Index (RI) counts the fraction of point pairs that are consistently grouped (both same or both different in U and V). The problem: even random cluster assignments achieve non-zero RI. Specifically, if both clusterings have k clusters of equal size, RI can be substantially above 0 by chance.")),
        para(rt("ARI corrects by subtracting the expected RI under a null model (hypergeometric distribution — random partition with fixed cluster sizes). After correction, ARI = 0 in expectation for random clusterings, making it a fair comparison metric across different k and n.")),
        para(rt("Follow-up: 'What's the null model?' The hypergeometric model assumes random assignment of n points to clusters such that cluster sizes match the observed ones in U and V. This is the natural maximum-entropy null for clusterings with fixed cluster sizes.")),
    ]),

    toggle([rt("Q4 (Medium): What is the difference between NMI and V-measure? When do they disagree?", bold=True)], [
        para(rt("Mathematically, V-measure with β=1 equals NMI (both are 2*I(Y;C)/(H(Y)+H(C))). They were derived independently but converge to the same formula.")),
        para(rt("The key difference is interpretability: V-measure explicitly decomposes into homogeneity (each cluster is pure) and completeness (each true class is captured), which is actionable. NMI provides a single number with an information-theoretic interpretation.")),
        para(rt("They can differ when β ≠ 1 in V-measure (weighting homogeneity vs completeness differently) or when using Adjusted Mutual Information (AMI) instead of NMI. For large k with small clusters, NMI can be artificially high (not adjusted for chance); AMI corrects this while NMI does not.")),
    ]),

    toggle([rt("Q5 (Medium): Describe a scenario where silhouette is high but the clustering is 'wrong.'", bold=True)], [
        para(rt("Classic case: non-convex or ring-shaped data. If the true structure consists of two concentric rings, a 2-cluster solution by k-means will produce two half-moons (geometrically separated convex clusters), giving a high silhouette. But this is geometrically clean while semantically wrong — the true 'inner ring' and 'outer ring' clusters aren't captured.")),
        para(rt("Another case: heavily imbalanced data. If one true cluster has 10,000 points and another has 10, k-means may split the large cluster into 2 and merge the small one, producing geometrically tight clusters with high silhouette but wrong membership.")),
    ]),

    toggle([rt("Q6 (Hard): Walk me through the full computation of ARI for a specific example.", bold=True)], [
        para(rt("True labels: [A,A,B,B,C,C]. Predicted: [1,1,1,2,2,2].")),
        para(rt("Contingency table:")),
        table(4, table_row(["", "Pred 1", "Pred 2", "Row sum"]),
              table_row(["True A", "2", "0", "2"]),
              table_row(["True B", "1", "1", "2"]),
              table_row(["True C", "0", "2", "2"]),
              table_row(["Col sum", "3", "3", "6"])),
        para(rt("Index = C(2,2)+C(0,2)+C(1,2)+C(1,2)+C(0,2)+C(2,2) = 1+0+0+0+0+1 = 2.")),
        para(rt("sum_ai = C(2,2)+C(2,2)+C(2,2) = 1+1+1 = 3.")),
        para(rt("sum_bj = C(3,2)+C(3,2) = 3+3 = 6.")),
        para(rt("Expected = (3 × 6) / C(6,2) = 18/15 = 1.2.")),
        para(rt("Max = (3+6)/2 = 4.5.")),
        para(rt("ARI = (2 − 1.2)/(4.5 − 1.2) = 0.8/3.3 ≈ 0.242.")),
        para(rt("The clustering partially recovers A and C but muddles B.")),
    ]),

    toggle([rt("Q7 (Hard): How do you evaluate clustering quality when n > 1 million points?", bold=True)], [
        para(rt("Silhouette at O(n²) is infeasible. Options:")),
        para(rt("1. Sampling: Compute silhouette on a random subsample of 10,000 points. sklearn supports sample_size parameter. Variance can be high — use multiple samples and average.")),
        para(rt("2. Mini-batch silhouette: Compute a(i) and b(i) using only a sample of same-cluster and neighbor-cluster points.")),
        para(rt("3. CH index: Only requires centroids and SSW/SSB — O(n) once centroids are known. Excellent for large n.")),
        para(rt("4. DB index: Also O(n) after centroids computed. Good scalability.")),
        para(rt("5. External metrics (ARI, NMI): O(n) computation from contingency table — scale well.")),
        para(rt("6. Inertia with elbow heuristic: O(n*k*d), fast but less informative than silhouette.")),
        para(rt("Recommendation: Use CH index as the primary internal metric for large-scale, use ARI/NMI when ground truth is available.")),
    ]),

    heading3("2-Level Explanations"),
    heading3("For a PhD Researcher"),
    para(rt("Internal metrics operationalize different geometric notions of cluster structure. Silhouette maximizes inter/intra distance ratios at the point level, making it invariant to absolute scale but sensitive to cluster shape assumptions (it implicitly assumes convex clusters since it uses Euclidean distance). The CH index is equivalent to the F-statistic in MANOVA — maximizing CH is equivalent to finding the partition that maximizes the variance explained by cluster membership under a Gaussian spherical noise model.")),
    para(rt("ARI's hypergeometric null model assumes fixed marginals (cluster sizes fixed), which is the natural exchangeability model. However, when cluster sizes are unequal, ARI can be biased toward partitions with many small clusters. Fowlkes & Mallows (1983) index is an alternative with different null assumptions. For external metrics, the information-theoretic family (NMI, AMI) has stronger connections to MDL (minimum description length) — a clustering with high NMI is one where knowing cluster labels provides maximal compression of the true label distribution.")),

    heading3("For a Research Scientist/Engineer"),
    para(rt("In practice, always compute multiple metrics. Silhouette catches bad cluster shapes that CH misses (CH favors equal-sized round clusters). DB is complementary — it penalizes situations where two clusters are close together even if individually tight. Use silhouette plots (per-cluster and per-point) not just the mean — a high mean can hide one cluster with all negative values.")),
    para(rt("For external metrics: ARI is the standard in papers (chance-corrected, symmetric, simple to explain). NMI is used in NLP/IR tasks where one cares about information-theoretic matching. V-measure is useful when you want to separately communicate how homogeneous your clusters are vs. how complete your class capture is.")),
    para(rt("Red flags in interviews: saying 'I use inertia/WCSS to evaluate clustering' without mentioning its limitation (monotone in k). Or saying 'Rand Index' without mentioning it's biased — always say ARI.")),

    heading3("System Design Angle"),
    para(rt("In an ML system that clusters user behavior for personalization: you'd monitor silhouette or DB over time to detect cluster drift (as user behaviors shift, cluster quality degrades). You'd use ARI between consecutive weeks' clusterings to measure cluster stability (a suddenly low ARI means the segment structure changed dramatically — trigger re-training). CH is useful for automated k-selection in a pipeline where k can drift.")),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 8: COMPARISON & TRADE-OFFS
    # ══════════════════════════════════════════════════════════════════
    heading2("⚖️ Comparison & Trade-offs"),

    heading3("Comprehensive Comparison Table"),
    table(
        7,
        table_row(["Metric", "Family", "Range", "Assumes convex clusters?", "Chance-corrected?", "Computation", "Best use case"]),
        table_row(["Silhouette", "Internal", "[−1, 1]", "Implicitly (Euclidean)", "N/A", "O(n²)", "Interpretable point-level diagnostics"]),
        table_row(["Calinski-Harabász", "Internal", "[0, ∞)", "Yes (spherical)", "N/A", "O(n·k)", "Fast, large-scale k selection"]),
        table_row(["Davies-Bouldin", "Internal", "[0, ∞)", "Partially (centroid-based)", "N/A", "O(n·k + k²)", "Finding worst-case cluster pairs"]),
        table_row(["Rand Index", "External", "[0, 1]", "No", "No — biased!", "O(n²)", "Avoid — use ARI instead"]),
        table_row(["ARI", "External", "[−1, 1]", "No", "Yes", "O(n)", "Standard external metric in papers"]),
        table_row(["NMI", "External", "[0, 1]", "No", "No*", "O(n)", "Information-theoretic tasks, NLP"]),
        table_row(["AMI", "External", "[−1, 1]", "No", "Yes", "O(n)", "Fair NMI when k varies"]),
        table_row(["V-measure", "External", "[0, 1]", "No", "No*", "O(n)", "Communicating homogeneity vs completeness"]),
    ),
    para(rt("*NMI and V-measure are not adjusted for chance — AMI is the adjusted version.", italic=True)),

    heading3("When to Use Which"),
    callout("🎯", rt("Decision Guide: ", bold=True),
        rt("No labels? → Silhouette (interpretable) + CH (fast). "),
        rt("Labels available? → ARI (standard), NMI (information-theoretic). "),
        rt("Want to explain to stakeholders? → Silhouette (−1 to +1 everyone understands) + V-measure (homogeneity/completeness analogy to precision/recall). "),
        rt("Large n (>100k)? → CH or DB (O(nk)) over silhouette (O(n²)). "),
        rt("Comparing clusterings with different k? → ARI or AMI (chance-corrected). "),
        rt("Non-convex clusters? → Silhouette with non-Euclidean distance, or switch to density-based metrics.")),

    heading3("Advantages & Disadvantages"),
    heading3("Silhouette"),
    bullet(rt("✅ Intuitive, bounded [−1,1], can plot per-point and per-cluster")),
    bullet(rt("✅ Works with any distance metric (not just Euclidean)")),
    bullet(rt("❌ O(n²) — expensive for large datasets")),
    bullet(rt("❌ Biased toward convex cluster shapes")),
    bullet(rt("❌ Can give misleading results for DBSCAN (noise points)")),

    heading3("Calinski-Harabász"),
    bullet(rt("✅ O(n) after centroid computation — scales well")),
    bullet(rt("✅ Directly related to variance explained (MANOVA F-statistic)")),
    bullet(rt("❌ Strongly assumes spherical, equal-size clusters")),
    bullet(rt("❌ No upper bound — hard to interpret absolute value")),

    heading3("ARI"),
    bullet(rt("✅ Chance-corrected — ARI=0 for random, regardless of k")),
    bullet(rt("✅ Symmetric — doesn't depend on which is 'true' vs 'predicted'")),
    bullet(rt("✅ O(n) computation")),
    bullet(rt("❌ Requires ground-truth labels")),
    bullet(rt("❌ Slightly biased toward partitions with many clusters of equal size")),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 9: INTERACTIVE VISUAL EXPLAINER
    # ══════════════════════════════════════════════════════════════════
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/clustering_evaluation_explainer.html"),
    para(rt("Step through the concept visually — watch all 6 metrics update as cluster quality degrades from perfect to random. Use ← → arrow keys to navigate.", italic=True, color="gray")),

    divider(),

    # ══════════════════════════════════════════════════════════════════
    # SECTION 10: RELATED TOPICS & FURTHER READING
    # ══════════════════════════════════════════════════════════════════
    heading2("🔗 Related Topics & Further Reading"),

    heading3("Prerequisites (should know first)"),
    bullet(rt("K-Means clustering (Lloyd's algorithm, K-Means++, elbow method)")),
    bullet(rt("Hierarchical clustering (linkage methods, dendrograms)")),
    bullet(rt("Distance metrics (Euclidean, cosine, Mahalanobis)")),
    bullet(rt("Shannon entropy and mutual information")),
    bullet(rt("Contingency tables and combinatorics")),

    heading3("What to Learn Next"),
    bullet(rt("DBSCAN and density-based clustering — how to evaluate clusters with noise points")),
    bullet(rt("Gaussian Mixture Models (GMM) — BIC/AIC for model selection in soft clustering")),
    bullet(rt("Spectral clustering — evaluation when clusters are non-convex")),
    bullet(rt("Cluster stability analysis — bootstrap-based evaluation")),
    bullet(rt("Topic models (LDA) — extensions of NMI/V-measure to soft assignments")),

    heading3("Key Papers"),
    numbered(rt("Rousseeuw, P.J. (1987). 'Silhouettes: a graphical aid to the interpretation and validation of cluster analysis.' J. Computational and Applied Mathematics, 20, 53–65. "), rt("— The original silhouette paper, still the definitive reference.", italic=True)),
    numbered(rt("Hubert, L. & Arabie, P. (1985). 'Comparing partitions.' J. Classification, 2(1), 193–218. "), rt("— Introduced ARI. Essential for any clustering evaluation pipeline.", italic=True)),
    numbered(rt("Caliński, T. & Harabász, J. (1974). 'A dendrite method for cluster analysis.' Communications in Statistics, 3(1), 1–27. "), rt("— Original CH index.", italic=True)),
    numbered(rt("Davies, D.L. & Bouldin, D.W. (1979). 'A cluster separation measure.' IEEE Transactions on PAMI, 1(2), 224–227. "), rt("— Original DB index.", italic=True)),
    numbered(rt("Vinh, N.X., Epps, J. & Bailey, J. (2010). 'Information theoretic measures for clusterings comparison.' JMLR, 11, 2837–2854. "), rt("— Unified framework for NMI variants; introduced AMI.", italic=True)),
    numbered(rt("Rosenberg, A. & Hirschberg, J. (2007). 'V-measure: A conditional entropy-based external cluster evaluation measure.' EMNLP 2007. "), rt("— V-measure paper; shows equivalence with NMI.", italic=True)),

    heading3("Best Resources"),
    bullet(rt("sklearn Clustering Evaluation docs — comprehensive, with worked examples for all metrics")),
    bullet(rt("'Cluster Analysis: Basic Concepts and Algorithms' — Chapter in 'Introduction to Data Mining' (Tan, Steinbach, Kumar) — excellent coverage")),
    bullet(rt("Rousseeuw's original silhouette paper (1987) — worth reading for the graphical interpretation (silhouette plots)")),

    callout("🔗", rt("This topic connects to: ", bold=True), rt("K-Means clustering, GMM (soft clustering evaluation via BIC), DBSCAN (density reachability), Dimensionality Reduction (PCA for pre-clustering), Information Theory (mutual information, entropy), Unsupervised Learning section generally.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
