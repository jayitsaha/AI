#!/usr/bin/env python3
"""Update Notion page for: Annoy Library"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81f4-8fae-f00e1dad48a4"
ICON = "🟡"  # Intermediate
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/annoy_library_explainer.html"

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Annoy (Approximate Nearest Neighbors Oh Yeah) is a C++ library with Python bindings, created at Spotify, that finds the "), rt("k", code=True), rt(" vectors most similar to a query vector — extremely fast — by trading a tiny bit of accuracy for massive speed and memory efficiency. It works on any dense vector: song embeddings, image features, text embeddings, recommendation latent factors.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine a library with a million books. Finding the most similar book by reading every single one would take forever. Annoy organises the library like a series of independent binary 'choose-your-path' mazes: at each fork, a random question splits books into two groups. Build many such mazes, then at search time walk all mazes simultaneously and merge the candidate lists. You never read every book, but you reliably find the right neighbourhood.")),
    heading3("One-Sentence Summary"),
    para(rt("Annoy builds a forest of random-projection binary trees over a static vector set, memory-maps the index to disk, and answers approximate nearest-neighbor queries by descending all trees in parallel and ranking merged candidates by exact distance.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Annoy = random hyperplane forests + mmap. Each tree splits space with a hyperplane through two random points; more trees → higher recall at linear cost. The index is static and file-backed — multiple processes share it with zero copy.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Spotify needed to serve real-time song recommendations from a catalogue of tens of millions of tracks. The recommendation vectors (from matrix factorisation / collaborative filtering) lived in ℝ^d where d ≈ 40–200. Brute-force nearest-neighbor search is "), eq(r"O(n \cdot d)"), rt(" per query — infeasible at 50 M items and 10 ms latency budgets. Existing solutions (KD-trees, ball-trees) degrade in high dimensions; LSH was hard to tune and lacked multi-metric support; FAISS didn't exist yet.")),
    heading3("What Came Before"),
    para(rt("KD-trees (Bentley, 1975) partition space by axis-aligned hyperplanes — optimal for low dimensions (d ≤ 15–20) but suffer the curse of dimensionality above that. Ball-trees use hypersphere boundaries, slightly better but same fundamental problem. LSH (Indyk & Motwani, 1998) hashes similar vectors to the same bucket — fast but metric-specific and recall is hard to control without parameter tuning.")),
    heading3("The Breakthrough"),
    para(rt("Erik Bernhardsson at Spotify open-sourced Annoy in 2013 (GitHub). The key insights were: (1) random hyperplanes through two random data points are a simple, metric-agnostic partitioning scheme; (2) building "), rt("T", italic=True), rt(" independent trees and merging candidate sets provides a tunable recall knob; (3) serialising the entire forest as a flat binary file enables "), rt("mmap()", code=True), rt(" sharing across processes — a critical production advantage.")),
    heading3("Key Paper"),
    para(rt("Bernhardsson, E. (2013). Annoy: Approximate Nearest Neighbors in C++/Python. GitHub / PyCon SE talk. The original motivation is documented in his blog post 'Nearest Neighbor Methods and Vector Models' (2015).")),
    heading3("Evolution Timeline"),
    para(rt("KD-tree (1975) → Ball-tree (1988) → LSH (1998) → "), rt("Annoy (2013)", bold=True), rt(" → HNSW (2016) → FAISS (2017) → ScaNN (2020) → DiskANN (2019, disk-based HNSW) → modern vector databases (Pinecone, Weaviate, Milvus, Qdrant).")),
    table(5,
        table_row(["Dimension", "KD-tree", "LSH", "Annoy", "HNSW"]),
        table_row(["Algorithm", "Axis-aligned splits", "Random hash families", "Random hyperplane forests", "Small-world graph"]),
        table_row(["Mutable index", "Yes", "Partial", "No (static)", "Yes"]),
        table_row(["High-dim performance", "Poor (d > 20)", "Moderate", "Good (d ≤ 500)", "Excellent"]),
        table_row(["Memory layout", "Tree in RAM", "Hash tables", "mmap binary file", "Graph in RAM"]),
        table_row(["Recall control", "Via k*", "Via hash tables", "Via n_trees", "Via ef_search"]),
        table_row(["Multi-process sharing", "No", "No", "Yes (mmap)", "No"]),
    ),
    divider(),

    # ── Section 3: Core Concepts & Theory ─────────────────────────────────────
    heading2("📐 Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(rt("Approximate Nearest Neighbor (ANN): ", bold=True), rt("Algorithm that returns neighbors within a (1+ε) factor of the true nearest neighbor distance, trading exactness for speed.")),
    bullet(rt("Random Projection Tree: ", bold=True), rt("A binary tree where each internal node splits the data by a hyperplane whose normal is chosen randomly (via two random data points).")),
    bullet(rt("Hyperplane: ", bold=True), rt("An (d-1)-dimensional subspace in ℝ^d. In Annoy, each hyperplane is the perpendicular bisector of the segment between two randomly chosen data points.")),
    bullet(rt("Memory-mapped file (mmap): ", bold=True), rt("OS mechanism mapping a disk file into the process virtual address space. Pages are loaded on-demand; multiple processes share physical pages. Used by Annoy for zero-copy, zero-parse index loading.")),
    bullet(rt("search_k: ", bold=True), rt("The candidate set size — how many leaf-node items are examined before computing exact distances. Higher search_k → higher recall → higher latency.")),
    heading3("Prerequisites"),
    para(rt("To understand Annoy, you should know: vectors and dot products in ℝ^d, the concept of nearest-neighbor search, basic tree data structures, and what approximate means in the ANN context.")),
    callout("🔑", rt("Core Property: ", bold=True), rt("Annoy's recall is monotonically non-decreasing in the number of trees T. For a fixed dataset and metric, doubling T roughly halves the probability that the true nearest neighbor is missed — but at the cost of 2× build time, 2× index size, and 2× query time.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ───────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD Deep Dive)"),
    heading3("Build Phase — Recursive Tree Construction"),
    para(rt("Given "), eq(r"n"), rt(" vectors "), eq(r"\mathbf{x}_1, \ldots, \mathbf{x}_n \in \mathbb{R}^d"), rt(", build "), eq(r"T"), rt(" independent trees:")),
    numbered(rt("Start with all indices "), eq(r"S = \{1, \ldots, n\}")),
    numbered(rt("Pick two random indices "), eq(r"i, j \in S")),
    numbered(rt("Splitting hyperplane: perpendicular bisector of "), eq(r"\overline{\mathbf{x}_i \mathbf{x}_j}")),
    numbered(rt("Normal vector: "), eq(r"\mathbf{v} = \mathbf{x}_i - \mathbf{x}_j")),
    numbered(rt("Midpoint: "), eq(r"\mathbf{m} = (\mathbf{x}_i + \mathbf{x}_j)/2")),
    numbered(rt("A point "), eq(r"\mathbf{x}"), rt(" goes LEFT iff "), eq(r"\mathbf{v}^\top (\mathbf{x} - \mathbf{m}) < 0"), rt(", RIGHT otherwise.")),
    numbered(rt("Recurse on left and right subsets until "), eq(r"|S| \leq K"), rt(" (leaf size, typically 10–50).")),
    numbered(rt("Repeat from step 1 for each of the "), eq(r"T"), rt(" trees.")),
    heading3("Query Phase — Priority Queue Traversal"),
    para(rt("For query "), eq(r"\mathbf{q}")),
    numbered(rt("Initialise a max-priority-queue (by distance-to-hyperplane) with all "), eq(r"T"), rt(" tree roots.")),
    numbered(rt("Pop node "), eq(r"u"), rt(". If leaf, add all items to candidate set "), eq(r"C"), rt(".")),
    numbered(rt("If internal node with hyperplane "), eq(r"(\mathbf{v}, \mathbf{m})"), rt(": compute margin "), eq(r"\mu = \mathbf{v}^\top (\mathbf{q} - \mathbf{m})")),
    numbered(rt("Push BOTH children to priority queue: primary child with priority "), eq(r"0"), rt(", secondary with priority "), eq(r"|\mu|"), rt(". (Smaller priority = explored first.)")),
    numbered(rt("Continue until "), eq(r"|C| \geq \text{search\_k}"), rt(".")),
    numbered(rt("Compute exact distances "), eq(r"\|\mathbf{q} - \mathbf{x}_c\|"), rt(" for all "), eq(r"c \in C"), rt(", return top "), eq(r"k"), rt(".")),
    heading3("Numerical Trace (d=2, n=5, T=1)"),
    para(rt("Dataset: "), eq(r"\mathbf{x}_0=[0.1,0.2], \mathbf{x}_1=[0.8,0.7], \mathbf{x}_2=[0.3,0.6], \mathbf{x}_3=[0.9,0.1], \mathbf{x}_4=[0.5,0.5]")),
    para(rt("Query: "), eq(r"\mathbf{q}=[0.45, 0.48]"), rt(". Leaf size K=3.")),
    para(rt("Step 1: Pick random pair "), eq(r"i=0, j=1"), rt(". Normal: "), eq(r"\mathbf{v}=[0.1-0.8, 0.2-0.7]=[-0.7,-0.5]"), rt(". Mid: "), eq(r"\mathbf{m}=[0.45, 0.45]")),
    para(rt("Step 2: Partition. For "), eq(r"\mathbf{x}_0"), rt(": "), eq(r"\mathbf{v}^\top(\mathbf{x}_0 - \mathbf{m}) = (-0.7)(0.1-0.45)+(-0.5)(0.2-0.45)=(-0.7)(-0.35)+(-0.5)(-0.25)=0.245+0.125=0.37>0"), rt(" → RIGHT.")),
    para(rt("For "), eq(r"\mathbf{x}_2"), rt(": "), eq(r"(-0.7)(0.3-0.45)+(-0.5)(0.6-0.45)=0.105-0.075=0.03>0"), rt(" → RIGHT. Others similarly computed. Left={1,3}, Right={0,2,4}. Both ≤3 → leaves.")),
    para(rt("Step 3: Query margin: "), eq(r"\mu=(-0.7)(0.45-0.45)+(-0.5)(0.48-0.45)=-0.015<0"), rt(" → query goes LEFT. Primary=LEFT leaf {1,3}. |C|=2 < search_k=6, so also explore RIGHT {0,2,4}. |C|=5 ≥ search_k=5.")),
    para(rt("Step 4: Exact distances from "), eq(r"\mathbf{q}=[0.45,0.48]"), rt(": d(x0)=0.502, d(x1)=0.536, d(x2)=0.196, d(x3)=0.621, d(x4)=0.071. Return k=2: {x4, x2}. ✓")),
    heading3("Serialisation & Memory Map"),
    para(rt("After build, Annoy serialises the forest as a flat array of fixed-size node structs: internal nodes store (v, m, left_child_id, right_child_id); leaves store the item list. Total size ≈ "), eq(r"O(T \cdot n)"), rt(" items × (d+2) floats per node. The file is read via "), rt("mmap()", code=True), rt(": the OS provides the entire forest as a pointer with demand-paging.")),
    heading3("Design Decision: Random Hyperplane vs Axis-Aligned"),
    callout("🔍", rt("Why random hyperplanes through two data points, not random axes? ", bold=True), rt("Axis-aligned splits (KD-tree) fail in high dimensions: hyperplanes parallel to axes become 'thin slabs' that don't separate clustered data. Random hyperplanes through actual data points are data-adaptive — they naturally bisect high-density regions. The choice of two random data points ensures the hyperplane passes through the data cloud rather than empty space.")),
    divider(),

    # ── Section 5: The Math ────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Splitting Hyperplane Definition"),
    para(rt("Given two points "), eq(r"\mathbf{p}, \mathbf{q} \in \mathbb{R}^d"), rt(", the perpendicular bisector hyperplane is:")),
    equation_block(r"\mathcal{H} = \left\{ \mathbf{x} \in \mathbb{R}^d \;\middle|\; (\mathbf{p} - \mathbf{q})^\top \!\left(\mathbf{x} - \tfrac{\mathbf{p}+\mathbf{q}}{2}\right) = 0 \right\}"),
    para(rt("This is the locus of points equidistant from "), eq(r"\mathbf{p}"), rt(" and "), eq(r"\mathbf{q}"), rt(". The signed distance from a point "), eq(r"\mathbf{x}"), rt(" to the hyperplane is:")),
    equation_block(r"\text{margin}(\mathbf{x}) = \frac{(\mathbf{p}-\mathbf{q})^\top (\mathbf{x} - \mathbf{m})}{\|\mathbf{p}-\mathbf{q}\|_2}, \quad \mathbf{m} = \tfrac{\mathbf{p}+\mathbf{q}}{2}"),
    heading3("Angular (Cosine) Metric"),
    para(rt("For angular distance, Annoy pre-normalises all vectors to the unit sphere. The splitting hyperplane still passes through the origin (since "), eq(r"\mathbf{m} = 0"), rt(" for unit vectors). The split condition simplifies to:")),
    equation_block(r"(\hat{\mathbf{p}} - \hat{\mathbf{q}})^\top \mathbf{x} \gtrless 0"),
    para(rt("where "), eq(r"\hat{\mathbf{p}} = \mathbf{p}/\|\mathbf{p}\|"), rt(". This is geometrically a great-circle arc on the unit hypersphere.")),
    heading3("Recall Bound"),
    para(rt("Let "), eq(r"r^*"), rt(" be the distance to the true nearest neighbor, and "), eq(r"r_{ann}"), rt(" be the distance returned by Annoy. The probability that Annoy misses the true NN from a single tree is bounded by the probability that the true NN is in a different leaf. With "), eq(r"T"), rt(" independent trees, the miss probability decays geometrically:")),
    equation_block(r"P(\text{miss} | T \text{ trees}) \leq \left(1 - \frac{1}{2^{\lceil \log_2 n/K \rceil}}\right)^T \approx \left(1 - \frac{K}{n}\right)^T"),
    para(rt("As "), eq(r"T \to \infty"), rt(", "), eq(r"P(\text{miss}) \to 0"), rt(". In practice, "), eq(r"T = 10"–"100"), rt(" trees gives recall ≥ 0.9 for most workloads.")),
    heading3("Build and Query Complexity"),
    equation_block(r"\text{Build time: } O\!\left(T \cdot n \log n\right)"),
    equation_block(r"\text{Index size: } O\!\left(T \cdot n \cdot d\right) \text{ bytes}"),
    equation_block(r"\text{Query time: } O\!\left(T \cdot \log n + \text{search\_k} \cdot d\right)"),
    callout("⚠️", rt("Warning: ", bold=True), rt("Annoy's recall guarantee is probabilistic, not deterministic. For identical query/database, two runs with different random seeds will build different trees and may return slightly different results. If you need exact recall = 1.0, use brute-force search or FAISS with IndexFlatL2.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """import numpy as np
from heapq import heappush, heappop

class RPNode:
    __slots__ = ['normal', 'mid', 'left', 'right', 'items']
    def __init__(self, normal=None, mid=None, left=None, right=None, items=None):
        self.normal, self.mid, self.left, self.right, self.items = \
            normal, mid, left, right, items

class AnnoyIndex:
    \"\"\"Minimal Annoy-like index using random-projection binary trees.\"\"\"

    def __init__(self, f, metric='euclidean', n_trees=10, leaf_size=10):
        self.f = f                # embedding dimension
        self.metric = metric
        self.n_trees = n_trees
        self.leaf_size = leaf_size
        self._items = []          # list of vectors (added via add_item)
        self._trees = []          # list of root RPNode

    def add_item(self, i, v):
        \"\"\"Add vector v at index i.\"\"\"
        v = np.asarray(v, dtype=np.float32)
        if self.metric == 'angular':
            norm = np.linalg.norm(v)
            if norm > 0: v = v / norm   # pre-normalise for cosine
        while len(self._items) <= i:
            self._items.append(None)
        self._items[i] = v

    def build(self, n_trees=None):
        \"\"\"Build n_trees independent random-projection trees.\"\"\"
        if n_trees: self.n_trees = n_trees
        X = np.stack(self._items)          # (n, d)
        indices = list(range(len(X)))
        for _ in range(self.n_trees):
            self._trees.append(self._build_tree(X, indices))

    def _build_tree(self, X, indices):
        if len(indices) <= self.leaf_size:
            return RPNode(items=indices)   # LEAF
        # Pick two random points → hyperplane
        i, j = np.random.choice(indices, 2, replace=False)
        normal = X[i] - X[j]              # hyperplane normal
        mid    = (X[i] + X[j]) / 2.0     # midpoint on hyperplane
        # Partition: dot(normal, x - mid) < 0 → left
        dots   = (X[indices] - mid) @ normal
        left   = [idx for idx, d in zip(indices, dots) if d <  0]
        right  = [idx for idx, d in zip(indices, dots) if d >= 0]
        if not left or not right:
            return RPNode(items=indices)   # degenerate → leaf
        return RPNode(
            normal=normal, mid=mid,
            left  = self._build_tree(X, left),
            right = self._build_tree(X, right),
        )

    def get_nns_by_vector(self, v, n, search_k=None):
        \"\"\"Return (indices, distances) of n approximate nearest neighbors.\"\"\"
        v = np.asarray(v, dtype=np.float32)
        if self.metric == 'angular':
            norm = np.linalg.norm(v)
            if norm > 0: v = v / norm
        if search_k is None:
            search_k = self.n_trees * self.leaf_size
        X = np.stack(self._items)
        # Priority queue: (margin, node) — min-heap (lower margin = explore first)
        pq = []
        for root in self._trees:
            heappush(pq, (0.0, root))
        candidates = set()
        while pq and len(candidates) < search_k:
            margin, node = heappop(pq)
            if node.items is not None:          # leaf
                candidates.update(node.items)
                continue
            mu = node.normal @ (v - node.mid)   # signed distance to hyperplane
            # Primary child (same side as query) gets priority 0 (explored first)
            primary   = node.left  if mu < 0 else node.right
            secondary = node.right if mu < 0 else node.left
            heappush(pq, (0.0,      primary))
            heappush(pq, (abs(mu),  secondary))  # explore other side if close
        # Exact distance ranking over candidates
        cands = list(candidates)
        dists = np.linalg.norm(X[cands] - v, axis=1)
        order = np.argsort(dists)[:n]
        return [cands[i] for i in order], dists[order].tolist()
"""),
    heading3("6b — Production (pip install annoy)"),
    code_block("python", """from annoy import AnnoyIndex
import numpy as np

DIM   = 128   # embedding dimension
TREES = 50    # higher → better recall, larger file, slower build

# ── BUILD ──────────────────────────────────────────────────────────────────────
idx = AnnoyIndex(DIM, 'angular')     # metric: 'angular','euclidean','manhattan','dot','hamming'
idx.on_disk_build('items.ann')       # build directly to disk (no RAM spike for large n)

embeddings = np.random.randn(100_000, DIM).astype(np.float32)
for i, vec in enumerate(embeddings):
    idx.add_item(i, vec)

idx.build(TREES)                     # O(T · n log n) — releases GIL in C++
# idx.save('items.ann')              # skip if using on_disk_build

# ── QUERY (another process / worker) ──────────────────────────────────────────
idx2 = AnnoyIndex(DIM, 'angular')
idx2.load('items.ann')               # mmap — instant, shared across workers

query_vec = np.random.randn(DIM).astype(np.float32)
neighbors, distances = idx2.get_nns_by_vector(
    query_vec,
    n=10,                            # return top-10 neighbors
    search_k=TREES * 100,            # candidates examined: higher → better recall
    include_distances=True           # True → returns (list[int], list[float])
)
print(neighbors)    # [idx_of_nearest, idx_of_2nd, ...]
print(distances)    # [0.012, 0.031, ...] (angular distance, not cosine similarity!)

# ── GOTCHAS ────────────────────────────────────────────────────────────────────
# ❌ idx.add_item() AFTER idx.build() → RuntimeError — index is static!
# ❌ angular distance ≠ cosine similarity: dist = sqrt(2*(1 - cos(θ)))
# ❌ Large DIM (>500) needs more trees for same recall
# ✅ Prefork mmap load: load('items.ann') in parent, fork workers — shared pages
# ✅ search_k=TREES*n_candidates controls recall/latency trade-off precisely
"""),
    divider(),

    # ── Section 7: Interview Deep-Dive ─────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is Annoy and what problem does it solve?", bold=True)], [
        para(rt("Annoy is a C++ library (Python bindings) for approximate nearest neighbor search. It solves the problem of finding the k vectors most similar to a query in a large collection too big for brute-force O(n·d) computation. Originally built at Spotify for music recommendation retrieval from millions of song vectors.")),
    ]),
    toggle([rt("Q2 (Easy): What does 'approximate' mean in ANN?", bold=True)], [
        para(rt("Approximate means the returned neighbors are not guaranteed to be the true nearest neighbors — Annoy might miss some. The trade-off is speed: approximate methods can be orders of magnitude faster than exact search. Annoy's approximation quality is controlled by n_trees and search_k.")),
    ]),
    toggle([rt("Q3 (Medium): How does Annoy build its index?", bold=True)], [
        para(rt("Annoy builds T independent binary trees. For each tree: pick two random data points, compute the perpendicular bisector hyperplane, partition all points (left/right of the hyperplane), recurse on each partition until leaf_size is reached. Repeat with different random points for each tree.")),
        para(rt("Split condition: "), eq(r"(\mathbf{p}-\mathbf{q})^\top(\mathbf{x}-\mathbf{m})<0 \Rightarrow \text{left}")),
    ]),
    toggle([rt("Q4 (Medium): How does query work at inference time?", bold=True)], [
        para(rt("Annoy maintains a priority queue initialised with all T tree roots. It pops nodes and descends toward the query, but crucially also enqueues the 'other side' child with priority = |distance to hyperplane|. This allows exploring near misses. Once search_k candidates are gathered, exact distances are computed and top k returned.")),
    ]),
    toggle([rt("Q5 (Medium): What is the mmap advantage?", bold=True)], [
        para(rt("After build, Annoy serialises the forest to a binary file and loads it via mmap(). The OS maps the file into virtual memory without copying. Multiple processes (e.g., gunicorn workers) all point to the same physical memory pages — zero duplication, instant load time. This is unique to Annoy among ANN libraries.")),
    ]),
    toggle([rt("Q6 (Hard): Annoy vs HNSW — when would you pick each?", bold=True)], [
        para(rt("Use Annoy when: index is static, you need mmap multi-process sharing, simplicity matters, n < 10M. Use HNSW (hnswlib/FAISS) when: you need real-time insertions, need higher recall at same latency, dimension > 500, or n > 100M. HNSW consistently outperforms Annoy on ANN benchmarks (ann-benchmarks.com) at high recall but requires the graph in RAM.")),
    ]),
    toggle([rt("Q7 (Hard): Why do random hyperplanes through data points work better than random directions?", bold=True)], [
        para(rt("A random direction in high-dimensional space has high probability of being nearly orthogonal to the data manifold — the resulting hyperplane would barely separate any points meaningfully. Hyperplanes through two data points are data-adaptive: they naturally bisect the data cloud in regions of high density, creating balanced partitions. This is the key algorithmic insight that makes Annoy effective.")),
    ]),
    toggle([rt("Q8 (Hard): How does angular distance differ from cosine similarity, and why does it matter?", bold=True)], [
        para(rt("Cosine similarity: "), eq(r"\cos\theta = \mathbf{x}^\top \mathbf{y}/(\\|\mathbf{x}\\|\\|\mathbf{y}\\|) \in [-1,1]")),
        para(rt("Annoy's angular distance: "), eq(r"d_{ang} = \sqrt{2(1 - \cos\theta)} \in [0, 2]")),
        para(rt("They are monotonically related — sorting by one is equivalent to sorting by the other — but the numeric values differ. Annoy returns angular distance, not cosine similarity. A distance of 0.1 does NOT mean cosine similarity of 0.9.")),
    ]),
    toggle([rt("Q9 (Expert): Explain to a PhD Researcher the theoretical underpinning of Annoy's recall.", bold=True)], [
        para(rt("Annoy belongs to the family of randomised partition tree methods. Each tree is a recursive random hyperplane split — the split point is drawn from the data distribution, making the partition data-adaptive rather than oblivious. The probability that two points "), eq(r"\mathbf{x}, \mathbf{y}"), rt(" land in the same leaf depends on the angle between them and the leaf size K. For angular metric, the probability of separation by a random great-circle is proportional to "), eq(r"\theta(\mathbf{x},\mathbf{y})/\pi"), rt(". With T trees, the probability of co-occurrence (same leaf) decreases geometrically in T. Annoy's recall is therefore a function of T, K, the intrinsic dimensionality of the data, and the query contrast ratio (distance to true NN vs distance to false NN). On clustered data with well-separated manifolds, Annoy achieves high recall with few trees; on uniform distributions in high dimensions, more trees are needed.")),
    ]),
    toggle([rt("Q10 (System Design): How would you use Annoy in a recommendation system at Spotify scale?", bold=True)], [
        para(rt("Offline: Train matrix factorisation (ALS) or two-tower model → 50M item embeddings in ℝ^128. Build Annoy index (TREES=100, metric=angular) → save to shared NFS/S3. Index size ≈ 100 × 50M × 128 × 4 bytes ≈ 2.56 TB (manageable with quantisation). Online: Each recommendation server process mmaps the index file — zero copy, ~1 ms cold start. For a query user embedding, call get_nns_by_vector(user_vec, n=100, search_k=500_000). Recall ~0.95 at ~5 ms latency. Then apply ranking model over 100 candidates.")),
    ]),
    divider(),

    # ── Section 8: Comparisons ─────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(6,
        table_row(["Library", "Algorithm", "Mutable", "GPU", "Recall@10", "Best For"]),
        table_row(["Annoy", "Random-proj trees + mmap", "No", "No", "~0.90", "Static, multi-process, simple"]),
        table_row(["FAISS (HNSW)", "Small-world graphs", "Yes", "No", "~0.99", "High recall, dynamic, production"]),
        table_row(["FAISS (IVF+PQ)", "Inverted file + quantisation", "Partial", "Yes", "~0.95", "Billion-scale, GPU"]),
        table_row(["Hnswlib", "HNSW (pure C++)", "Yes", "No", "~0.99", "Dynamic, simple API"]),
        table_row(["ScaNN", "Anisotropic quantisation", "No", "Partial", "~0.98", "Google-scale cosine"]),
        table_row(["DiskANN", "Graph on disk (Vamana)", "Partial", "No", "~0.99", "Disk-based, large n"]),
        table_row(["KD-tree (sklearn)", "Axis-aligned splits", "Yes", "No", "1.0 (exact)", "d ≤ 20, exact search"]),
        table_row(["Brute force", "Exact scan", "Yes", "Yes", "1.0 (exact)", "n ≤ 100K, GPU available"]),
    ),
    callout("🎯", rt("Decision Guide: ", bold=True),
        rt("Static index + multi-process serving → Annoy. Dynamic insertions needed → HNSW/Hnswlib. Billion-scale + GPU → FAISS. Exact search with d ≤ 20 → KD-tree. Exact search with d > 20 → FAISS IndexFlatL2.")),
    divider(),

    # ── Section 9: Interactive Explainer ──────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ───────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites (know these first)"),
    bullet(rt("Vector spaces and dot products in ℝ^d")),
    bullet(rt("K-Nearest Neighbors (KNN) — brute-force nearest neighbor search")),
    bullet(rt("KD-tree and Ball-tree — exact ANN for low dimensions")),
    bullet(rt("Cosine similarity and angular distance")),
    heading3("What to Learn Next"),
    bullet(rt("HNSW (Hierarchical Navigable Small World) — current state-of-the-art ANN")),
    bullet(rt("FAISS — Facebook's production ANN library (IVF, PQ, IVFPQ)")),
    bullet(rt("ScaNN — Google's anisotropic quantisation ANN")),
    bullet(rt("Product Quantisation (PQ) — lossy vector compression for ANN")),
    bullet(rt("LSH (Locality-Sensitive Hashing) — alternative hashing-based ANN")),
    bullet(rt("Vector Databases — Pinecone, Weaviate, Milvus, Qdrant (use HNSW + mmap internally)")),
    bullet(rt("Two-Tower Retrieval Models — where ANN is the serving backbone")),
    heading3("Key Papers"),
    bullet(rt("Bernhardsson, E. (2013). Annoy: Approximate Nearest Neighbors in C++/Python. Spotify / GitHub.")),
    bullet(rt("Malkov & Yashunin (2018). Efficient and Robust Approximate Nearest Neighbor Search Using HNSW. IEEE TPAMI.")),
    bullet(rt("Johnson, Douze & Jégou (2017). Billion-scale similarity search with GPUs. FAISS. arXiv:1702.08734.")),
    bullet(rt("Indyk & Motwani (1998). Approximate Nearest Neighbors: Towards Removing the Curse of Dimensionality. STOC. (LSH origin paper.)")),
    bullet(rt("Guo et al. (2020). Accelerating Large-Scale Inference with Anisotropic Vector Quantization. ScaNN. ICML 2020.")),
    heading3("Best Resources"),
    bullet(rt("Annoy GitHub: github.com/spotify/annoy (C++ source + Python docs)")),
    bullet(rt("ann-benchmarks.com — live comparison of all ANN libraries on standardised datasets")),
    bullet(rt("Bernhardsson blog: erikbern.com — 'Nearest Neighbor Methods and Vector Models' (2015)")),
    bullet(rt("FAISS wiki: github.com/facebookresearch/faiss/wiki — for comparison context")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("HNSW · FAISS · ScaNN · Product Quantisation · LSH · KD-tree · Ball-tree · Vector Databases · Two-Tower Models · Candidate Generation in RecSys · RAG Retrieval")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
