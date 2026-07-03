#!/usr/bin/env python3
"""Update Notion page for: FP-Growth Algorithm"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8112-a154-c29f1e62fe2b"
ICON = "🟠"
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/fp_growth_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Advanced"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [

    # ══════════════════════════════════════════════════════════════════════
    # Section 1: The 30-Second Version
    # ══════════════════════════════════════════════════════════════════════
    heading2("The 30-Second Version"),
    heading3("What is this?"),
    para(rt("FP-Growth (Frequent Pattern Growth) mines frequent itemsets from transaction databases using a compressed prefix tree called an FP-tree. No candidate generation is needed — the algorithm encodes the entire database in two passes and extracts all frequent patterns directly from the tree via recursive divide-and-conquer.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine a library that tracks which books are borrowed together. Instead of checking every possible book combination (as Apriori does), FP-Growth builds a compact \"borrowing pattern tree\" in 2 database scans and reads patterns directly from it. Common books sit near the root and are shared by many paths; rare books appear only on isolated branches. Mining is like reading off all the shared-path combinations — no guessing required.")),
    heading3("One-Sentence Summary"),
    para(rt("FP-Growth compresses a transaction database into an FP-tree then recursively mines it via conditional pattern bases — finding all frequent itemsets in exactly 2 database passes.")),
    callout("💡", rt("Remember one thing: ", bold=True), rt("FP-Growth achieves completeness without candidate generation by encoding all frequency information in a prefix tree, then mining it top-down via conditional FP-trees.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 2: Historical Context
    # ══════════════════════════════════════════════════════════════════════
    heading2("Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Apriori (1994) was the first practical frequent itemset mining algorithm. It works by generating candidate itemsets of increasing size and pruning those below minimum support. However, it requires "), rt("O(2^|I|)", code=True), rt(" candidate itemsets in the worst case — exponential in the number of items. Worse, it needs one full database scan per itemset size, making it extremely slow on dense datasets or with a low minimum-support threshold.")),
    heading3("What Came Before"),
    para(rt("Apriori algorithm by Agrawal & Srikant (1994) generates candidates then prunes using the anti-monotone property: any superset of an infrequent itemset is also infrequent. While elegant, this still results in enormous candidate spaces and repeated I/O.")),
    heading3("The Breakthrough"),
    para(rt("Jiawei Han, Jian Pei, and Yiwen Yin published \"Mining Frequent Patterns without Candidate Generation\" at SIGMOD 2000. The key insight: store the entire database (projected onto frequent items) into a compact prefix tree (FP-tree); then mine using divide-and-conquer on conditional sub-databases. No candidate generation is ever performed.")),
    heading3("Evolution Timeline"),
    bullet(rt("1994: Apriori (Agrawal & Srikant) — candidate generation + anti-monotone pruning")),
    bullet(rt("2000: FP-Growth (Han, Pei & Yin) — compact FP-tree, zero candidates, 2 DB scans")),
    bullet(rt("2001: PrefixSpan (Pei et al.) — extends FP-style mining to sequential patterns")),
    bullet(rt("2000: ECLAT (Zaki) — vertical tid-list format, intersection-based mining")),
    bullet(rt("2004+: FP-Growth* and other variants — optimized node representation, parallelism")),
    bullet(rt("2008: PFP-Growth (Li et al.) — parallel FP-Growth across MapReduce clusters")),
    heading3("Apriori vs FP-Growth Comparison"),
    table(3,
        table_row(["Dimension", "Apriori", "FP-Growth"]),
        table_row(["DB Scans", "2·k (one per itemset size k)", "Exactly 2"]),
        table_row(["Candidates", "Exponential O(2^|I|)", "None"]),
        table_row(["Memory", "Low (iterative)", "Moderate (FP-tree)"]),
        table_row(["Speed (dense DB)", "Very slow", "Fast"]),
        table_row(["Speed (sparse DB)", "OK", "Can be slower (large tree)"]),
        table_row(["Key innovation", "Anti-monotone pruning", "Compressed prefix tree"]),
    ),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 3: Core Concepts & Theory
    # ══════════════════════════════════════════════════════════════════════
    heading2("Core Concepts & Theory"),
    heading3("Key Definitions"),
    bullet(
        rt("Transaction database: "), eq(r"\mathcal{D} = \{T_1, \ldots, T_n\}"),
        rt(", where each "), eq(r"T_i \subseteq \mathcal{I}"), rt(" (a set of items from item universe "), eq(r"\mathcal{I}"), rt(")")
    ),
    bullet(
        rt("Support of itemset "), eq(r"X"), rt(":"),
    ),
    equation_block(r"\text{support}(X, \mathcal{D}) = \frac{|\{T \in \mathcal{D} : X \subseteq T\}|}{|\mathcal{D}|}"),
    bullet(rt("Frequent itemset: an itemset "), eq(r"X"), rt(" such that "), eq(r"\text{support}(X) \geq \text{min\_sup}")),
    bullet(rt("Anti-monotone property: "), eq(r"\text{support}(X \cup Y) \leq \text{support}(X)"), rt(" for all "), eq(r"X, Y")),
    bullet(rt("FP-tree: a compact prefix tree where each root-to-leaf path represents a transaction (shared prefixes merged). Each node stores: (item label, count, parent-link, child-links, node-link to next same-item node).")),
    bullet(rt("Header table: maps each frequent item to its total support count and the head of a linked list of all FP-tree nodes containing that item.")),
    bullet(rt("Conditional pattern base of item "), eq(r"x"), rt(": the set of all prefix paths ending at each "), eq(r"x"), rt("-node in the FP-tree, weighted by that node's count.")),
    bullet(rt("Conditional FP-tree of item "), eq(r"x"), rt(": the FP-tree built from "), eq(r"x"), rt("'s conditional pattern base using the same min_sup threshold.")),
    callout("🔑", rt("Key Invariant: ", bold=True), rt("The FP-tree is a lossless compression of all frequent pattern information. The header table + node-links allow traversal of all occurrences of each item without scanning the original database again.")),
    heading3("Prerequisites"),
    bullet(rt("Itemset, support, confidence, lift")),
    bullet(rt("Apriori algorithm and anti-monotone property")),
    bullet(rt("Tree data structures: prefix trees (tries), linked lists")),
    bullet(rt("Recursive divide-and-conquer algorithms")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 4: Architecture & Internal Workings (PhD-Level)
    # ══════════════════════════════════════════════════════════════════════
    heading2("Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("PHASE 1 — Build the FP-tree (2 database scans)"),
    numbered(rt("Scan 1: Count all item frequencies across all transactions. Discard any item below min_sup. Sort remaining frequent items by frequency descending (ties broken lexicographically) to form the F-list.")),
    numbered(rt("Scan 2: For each transaction T:")),
    bullet(rt("Filter T to keep only frequent items")),
    bullet(rt("Sort filtered items by F-list order (most frequent first)")),
    bullet(rt("Insert sorted transaction into FP-tree: walk from root, follow matching child if it exists (increment count), else create new child node with count=1; update header table node-links at each new node")),
    heading3("PHASE 2 — FP-Growth (recursive divide-and-conquer)"),
    para(rt("For each frequent item "), eq(r"x_i"), rt(" in reverse F-list order (ascending frequency, i.e., rarest first):")),
    numbered(rt("Output {x_i} as a frequent itemset with support = x_i's count in the header table")),
    numbered(rt("Collect conditional pattern base: follow each node-link for x_i; for each such node, record its prefix path (all ancestor items above x_i) weighted by x_i's count at that node")),
    numbered(rt("Build the conditional FP-tree from the conditional pattern base, applying min_sup filtering to the prefix items")),
    numbered(rt("If conditional FP-tree is non-empty: recurse on it, prepending x_i to each result pattern")),
    numbered(rt("All patterns from the recursive call, plus x_i itself, are patterns containing x_i")),
    heading3("Numerical Trace (Classic 5-Transaction Example, min_sup=2)"),
    para(rt("Raw transactions (before filtering):")),
    table(2,
        table_row(["TID", "Items"]),
        table_row(["T1", "{f, a, c, d, g, i, m, p}"]),
        table_row(["T2", "{a, b, c, f, l, m, o}"]),
        table_row(["T3", "{b, f, h, j, o}"]),
        table_row(["T4", "{b, c, k, s, p}"]),
        table_row(["T5", "{a, f, c, e, l, p, m, n}"]),
    ),
    para(rt("Scan 1 — item frequencies: f:4, c:4, a:3, b:3, m:3, p:3. Items d, g, i, l, o, h, j, k, s, e, n all have frequency 1 and are discarded.")),
    para(rt("F-list (descending frequency): f:4, c:4, a:3, b:3, m:3, p:3")),
    para(rt("Scan 2 — filtered, sorted transactions:")),
    table(2,
        table_row(["TID", "Filtered & Sorted Transaction"]),
        table_row(["T1", "{f, c, a, m, p}"]),
        table_row(["T2", "{f, c, a, b, m}"]),
        table_row(["T3", "{f, b}"]),
        table_row(["T4", "{c, b, p}"]),
        table_row(["T5", "{f, c, a, m, p}"]),
    ),
    para(rt("FP-tree structure after inserting all 5 transactions:")),
    bullet(rt("root → f:4 → c:3 → a:3 → m:2 → p:2  (T1+T5 share path f→c→a→m→p)")),
    bullet(rt("root → f:4 → c:3 → a:3 → b:1 → m:1  (T2: diverges at b after a)")),
    bullet(rt("root → f:4 → b:1  (T3: f→b, no c)")),
    bullet(rt("root → c:1 → b:1 → p:1  (T4: starts with c not f)")),
    para(rt("Header table (item → support, first node-link):")),
    table(2,
        table_row(["Item", "Total Support"]),
        table_row(["f", "4"]),
        table_row(["c", "4"]),
        table_row(["a", "3"]),
        table_row(["b", "3"]),
        table_row(["m", "3"]),
        table_row(["p", "3"]),
    ),
    heading3("Mining Item p (ascending order — rarest processed first)"),
    para(rt("Follow node-links for p — two nodes exist:")),
    bullet(rt("Node p:2 on path root→f→c→a→m→p: prefix = {f:2, c:2, a:2, m:2}")),
    bullet(rt("Node p:1 on path root→c→b→p: prefix = {c:1, b:1}")),
    para(rt("Conditional pattern base for p: { {f,c,a,m}:2,  {c,b}:1 }")),
    para(rt("Count items in conditional pattern base: f:2, c:3, a:2, m:2, b:1. With min_sup=2: keep f:2, c:3, a:2, m:2 (drop b:1).")),
    para(rt("Conditional FP-tree for p: root→c:3→f:2→a:2→m:2  (and root→c:3 has a single-path branch c:1 from the second pattern, contributing to c's count)")),
    para(rt("Frequent patterns with p (all subsets from this conditional tree + p):")),
    bullet(rt("{p}: support=3")),
    bullet(rt("{c,p}: support=3")),
    bullet(rt("{f,p}: support=2, {a,p}: support=2, {m,p}: support=2")),
    bullet(rt("{f,c,p}: support=2, {f,a,p}: support=2, {c,a,p}: support=2, {c,m,p}: support=2, {f,m,p}: support=2, {a,m,p}: support=2")),
    bullet(rt("{f,c,a,p}: support=2, {f,c,m,p}: support=2, {f,a,m,p}: support=2, {c,a,m,p}: support=2")),
    bullet(rt("{f,c,a,m,p}: support=2")),
    heading3("Edge Cases"),
    bullet(rt("Single-path FP-tree: if the conditional FP-tree is a single path (no branching), enumerate all 2^k subsets of the path items directly — no recursion needed.")),
    bullet(rt("Empty conditional FP-tree: only {x_i} itself is frequent from that branch — stop recursion.")),
    bullet(rt("Equal-frequency items: must break ties consistently (e.g., lexicographic) to ensure the same F-list order across all sub-problems.")),
    callout("🎯", rt("Design Decision: ", bold=True), rt("Why sort by descending frequency? Maximum prefix sharing — the most common items (appearing in many transactions) are placed near the root, so more paths share prefixes, compressing the tree most efficiently.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 5: The Math Behind It
    # ══════════════════════════════════════════════════════════════════════
    heading2("The Math Behind FP-Growth"),
    heading3("Support Definition"),
    equation_block(r"\text{support}(X, \mathcal{D}) = \frac{|\{T \in \mathcal{D} : X \subseteq T\}|}{|\mathcal{D}|}"),
    heading3("Anti-Monotone Property (Foundation of Correctness)"),
    equation_block(r"\forall X \subseteq Y: \quad \text{support}(Y) \leq \text{support}(X)"),
    para(rt("This guarantees that if any subset of "), eq(r"X"), rt(" is infrequent, "), eq(r"X"), rt(" itself is infrequent — enabling safe pruning at every level of the conditional FP-tree.")),
    heading3("FP-Tree Completeness Theorem"),
    para(rt("Theorem (Han et al., 2000): The FP-tree "), eq(r"\mathcal{T}(\mathcal{D}, \text{min\_sup})"), rt(" contains all information necessary to mine all frequent itemsets from "), eq(r"\mathcal{D}"), rt(" without accessing "), eq(r"\mathcal{D}"), rt(" again. Every frequent itemset can be reconstructed from paths in "), eq(r"\mathcal{T}"), rt(" via the header table node-links.")),
    heading3("Conditional Pattern Base (Formal Definition)"),
    equation_block(r"\text{CPB}(x, \mathcal{T}) = \left\{(\alpha,\, c_i) \;\middle|\; \text{path}(\text{node}_i^x) = \alpha \cdot x,\;\; c_i = \text{count}(\text{node}_i^x)\right\}"),
    para(rt("where "), eq(r"\alpha"), rt(" is the sequence of ancestor items above "), eq(r"\text{node}_i^x"), rt(" (the "), eq(r"i"), rt("-th FP-tree node labeled "), eq(r"x"), rt(").")),
    heading3("Pattern Generation Theorem"),
    para(rt("Every frequent itemset "), eq(r"X = \{x_1, \ldots, x_k\}"), rt(" (in F-list order, "), eq(r"x_k"), rt(" is the lowest-frequency item) is generated "), rt("exactly once", bold=True), rt(" during mining of "), eq(r"x_k"), rt("'s conditional FP-tree, with prefix "), eq(r"\{x_1, \ldots, x_{k-1}\}"), rt(". No duplicate counting occurs.")),
    heading3("Time Complexity"),
    equation_block(r"O\!\left(n \cdot \bar{L} + |\mathcal{T}| + \sum_{x \in \mathcal{F}} |\text{CPB}(x)|\right)"),
    para(rt("where "), eq(r"n = |\mathcal{D}|"), rt(" (number of transactions), "), eq(r"\bar{L}"), rt(" = average filtered transaction length, "), eq(r"\mathcal{T}"), rt(" = FP-tree size, and "), eq(r"\mathcal{F}"), rt(" = set of frequent items.")),
    heading3("Space Complexity"),
    equation_block(r"O\!\left(|\mathcal{F}| \cdot \bar{L}\right)"),
    para(rt("In the worst case (no prefix sharing — fully sparse database): "), eq(r"O(n \cdot \bar{L})"), rt(". In the best case (star topology — one item dominates all paths): "), eq(r"O(|\mathcal{F}|)"), rt(".")),
    callout("⚠️", rt("Complexity Warning: ", bold=True), rt("FP-Growth's advantage over Apriori breaks down for very sparse datasets where min_sup is very low, because the FP-tree grows nearly as large as the original database and conditional FP-trees remain large at each recursive level.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 6: Code Implementation
    # ══════════════════════════════════════════════════════════════════════
    heading2("Code Implementation"),
    heading3("6a — From Scratch (Pure Python, No Libraries)"),
    code_block("python",
"""from collections import defaultdict

class FPNode:
    \"\"\"Node in an FP-tree.\"\"\"
    def __init__(self, item, count, parent):
        self.item = item        # item label (None for root)
        self.count = count      # occurrence count
        self.parent = parent    # parent FPNode
        self.children = {}      # item -> FPNode
        self.node_link = None   # next node with same item (for header table)


class FPTree:
    def __init__(self, transactions, min_sup):
        self.min_sup = min_sup
        self.header_table = {}  # item -> [count, first_node]
        self.root = FPNode(None, 0, None)

        # Pass 1: count frequencies
        freq = defaultdict(int)
        for trans in transactions:
            for item in trans:
                freq[item] += 1

        # Filter & sort items by descending frequency (F-list)
        self.f_list = sorted(
            [item for item, cnt in freq.items() if cnt >= min_sup],
            key=lambda x: (-freq[x], x)  # desc freq, then lex for ties
        )
        freq_rank = {item: i for i, item in enumerate(self.f_list)}

        # Initialize header table
        for item in self.f_list:
            self.header_table[item] = [freq[item], None]

        # Pass 2: insert filtered, sorted transactions
        for trans in transactions:
            filtered = sorted(
                [item for item in trans if item in freq_rank],
                key=lambda x: freq_rank[x]
            )
            if filtered:
                self._insert(filtered, self.root)

    def _insert(self, items, node):
        \"\"\"Recursively insert items into tree starting at node.\"\"\"
        if not items:
            return
        item = items[0]
        if item in node.children:
            node.children[item].count += 1
        else:
            child = FPNode(item, 1, node)
            node.children[item] = child
            # Update header table node-link chain
            if self.header_table[item][1] is None:
                self.header_table[item][1] = child
            else:
                curr = self.header_table[item][1]
                while curr.node_link:
                    curr = curr.node_link
                curr.node_link = child
        self._insert(items[1:], node.children[item])

    def conditional_pattern_base(self, item):
        \"\"\"Collect conditional pattern base for an item via node-links.\"\"\"
        patterns = []
        node = self.header_table[item][1]
        while node:
            count = node.count
            prefix = []
            parent = node.parent
            while parent.item is not None:   # stop at root
                prefix.append(parent.item)
                parent = parent.parent
            prefix.reverse()
            if prefix:
                patterns.append((prefix, count))
            node = node.node_link
        return patterns


def fp_growth(transactions, min_sup, prefix=None):
    \"\"\"Mine all frequent itemsets using FP-Growth.

    Returns list of (frozenset, support_count).
    \"\"\"
    if prefix is None:
        prefix = []

    tree = FPTree(transactions, min_sup)
    frequent_itemsets = []

    # Mine each item in reverse F-list order (ascending frequency)
    for item in reversed(tree.f_list):
        support = tree.header_table[item][0]
        new_itemset = prefix + [item]
        frequent_itemsets.append((frozenset(new_itemset), support))

        # Build conditional transactions from pattern base
        cpb = tree.conditional_pattern_base(item)
        cond_transactions = []
        for path, count in cpb:
            # Expand: repeat the path 'count' times to preserve weights
            cond_transactions.extend([path] * count)

        if cond_transactions:
            sub_itemsets = fp_growth(cond_transactions, min_sup, new_itemset)
            frequent_itemsets.extend(sub_itemsets)

    return frequent_itemsets


# ── Example usage ──────────────────────────────────────────────────────
transactions = [
    ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
    ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
    ['b', 'f', 'h', 'j', 'o'],
    ['b', 'c', 'k', 's', 'p'],
    ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n'],
]

results = fp_growth(transactions, min_sup=2)
print(f"Found {len(results)} frequent itemsets:")
for itemset, sup in sorted(results, key=lambda x: (-len(x[0]), sorted(x[0]))):
    print(f"  {set(itemset)}: support={sup}")

# Gotcha: cond_transactions uses [path]*count — correct but memory-heavy.
# For large datasets, use a weighted FPTree that accepts (transaction, weight) pairs.
# Gotcha: recursion depth can exceed Python's limit for deeply nested trees;
#         increase sys.setrecursionlimit() or convert to iterative form.
"""),
    heading3("6b — Production Usage (mlxtend)"),
    code_block("python",
"""from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

dataset = [
    ['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
    ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
    ['b', 'f', 'h', 'j', 'o'],
    ['b', 'c', 'k', 's', 'p'],
    ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n'],
]

# Step 1: Encode as one-hot boolean DataFrame
te = TransactionEncoder()
te_array = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_array, columns=te.columns_)

# Step 2: Mine frequent itemsets (min_support is a fraction 0.0–1.0)
freq_items = fpgrowth(df, min_support=0.4, use_colnames=True)
print(freq_items.sort_values('support', ascending=False).to_string())

# Step 3: Derive association rules
rules = association_rules(freq_items, metric="confidence", min_threshold=0.6)
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# ── Gotchas ────────────────────────────────────────────────────────────
# Gotcha 1: min_support is a fraction (0.0–1.0), NOT an integer count.
#            Use min_support=2/5 to express count-2 on a 5-transaction DB.
# Gotcha 2: Without use_colnames=True, itemsets use integer column indices.
# Gotcha 3: fpgrowth() is faster than apriori() on dense datasets (fewer
#            columns with True values), but apriori may win on very sparse ones.
# Gotcha 4: association_rules() requires at least one frequent itemset of
#            size >= 2; if none exist (min_support too high), it will error.
"""),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 7: Interview Deep Dive
    # ══════════════════════════════════════════════════════════════════════
    heading2("Interview Deep-Dive"),
    heading3("Q1 (Easy): What is the FP-Growth algorithm and how does it differ from Apriori?"),
    para(rt("FP-Growth mines frequent itemsets by first compressing the transaction database into a prefix tree (FP-tree) in two scans, then recursively extracting patterns via conditional pattern bases — without ever generating candidates. Apriori iteratively generates candidate itemsets of size k+1 from frequent k-itemsets, requiring a full database scan per itemset size. FP-Growth avoids both candidate generation and repeated scans, making it dramatically faster on dense datasets.")),
    heading3("Q2 (Easy): What is an FP-tree? What does each node contain?"),
    para(rt("An FP-tree is a compact prefix tree where each root-to-leaf path encodes a transaction (filtered to frequent items, sorted by descending frequency). Shared prefixes across transactions are merged into shared paths, with counts incremented. Each node contains: item label, count (number of transactions passing through this node), parent pointer, child pointers (one per distinct child item), and a node-link pointer to the next FP-tree node with the same item label (forming a linked list threaded through the header table).")),
    heading3("Q3 (Medium): Walk me through how you'd build an FP-tree from scratch."),
    para(rt("Step 1 (Scan 1): Iterate over all transactions, count each item's frequency, discard items below min_sup. Sort the remaining frequent items by descending frequency to get the F-list. Step 2 (Scan 2): For each transaction, filter to frequent items only, sort them by F-list order, then insert the sequence into the FP-tree starting at the root. At each level, if a child with that item exists, increment its count; otherwise, create a new child node with count=1 and update the header table's node-link chain for that item. After all insertions, the tree and header table are complete.")),
    heading3("Q4 (Medium): What is a conditional pattern base? Why is it needed?"),
    para(rt("The conditional pattern base (CPB) for item x is the collection of all prefix paths in the FP-tree that end at an x-node, each weighted by x's count at that node. It is needed because it defines the sub-database relevant to mining patterns that contain x — essentially the projected database D|x. Instead of re-scanning the original database, we use node-links from the header table to traverse only the x-nodes and collect their prefixes. The CPB is then used to build a smaller conditional FP-tree, enabling recursive sub-problem decomposition.")),
    heading3("Q5 (Medium): What is a conditional FP-tree? How do you build one?"),
    para(rt("A conditional FP-tree for item x is an FP-tree built from x's conditional pattern base, applying the same min_sup threshold. To build it: treat each (prefix_path, count) pair in the CPB as a weighted transaction; count item frequencies across all such weighted transactions; discard items below min_sup; sort remaining items by descending frequency; insert the weighted transactions into a new FP-tree. Recursive mining of this conditional FP-tree finds all frequent patterns that contain x as a suffix.")),
    heading3("Q6 (Hard): Prove that FP-Growth is complete — i.e., it finds ALL frequent itemsets."),
    para(rt("By the conditional FP-tree theorem, every frequent pattern "), rt("X = {x_1, ..., x_k}", code=True), rt(" (in F-list order, x_k is the last/lowest-frequency item) is generated exactly once during mining of x_k's conditional FP-tree. The conditional pattern base for x_k captures all transactions containing x_k, along with their prefix items — precisely the co-occurrence information needed to find {x_1,...,x_{k-1}} as frequent in CPB(x_k). The anti-monotone property guarantees no frequent pattern is pruned during min_sup filtering of the CPB (since all subsets of a frequent itemset are frequent). Every item x_k is processed exactly once (header table is exhausted), and the recursion terminates when no frequent items remain. Therefore all frequent itemsets are generated, and none more than once.")),
    heading3("Q7 (Hard): When would you prefer Apriori over FP-Growth?"),
    para(rt("Apriori may be preferred when: (1) The dataset is very sparse — the FP-tree provides little compression benefit and may consume more memory than Apriori's iterative candidate approach. (2) Memory is severely constrained — FP-tree requires O(|F|·L̄) RAM which can be large. (3) Max itemset size is very small (k=2 or k=3) — Apriori with optimized data structures can be faster for just counting pairs/triples. (4) Interpretability of the candidate generation process matters for auditing or compliance. (5) The min_sup threshold is high — few candidates, Apriori terminates quickly.")),
    heading3("Q8 (Hard): How does FP-Growth handle a database that doesn't fit in memory?"),
    para(rt("For disk-resident databases: Partition the database D into k chunks {D_1,...,D_k} that fit in memory. For each partition D_i, build a local FP-tree and mine local frequent itemsets with threshold (min_sup·|D_i|). Merge all local frequent itemsets into a candidate global set. Make a second pass over all partitions to count global supports and discard those below global min_sup·|D|. This is the partition algorithm (Savasere et al., 1995), applicable to FP-Growth. Alternatively, use PFP-Growth (Li et al., 2008) which partitions by item group across a MapReduce cluster.")),
    heading3("Q9 (Expert): Describe FP-Growth's time/space complexity and when it degrades."),
    para(rt("Time: "), eq(r"O\!\left(n \cdot \bar{L} + |\mathcal{T}| + \sum_{x \in \mathcal{F}} |\text{CPB}(x)|\right)"), rt(". In the best case (dense, high min_sup), tree is tiny and CPBs are small. In the worst case (low min_sup, sparse data), the tree is O(n·L̄) and each CPB is nearly as large as D. Space: O(|F|·L̄) for the FP-tree; worst case O(n·L̄). Degradation conditions: (a) very low min_sup — exponentially many frequent patterns and large trees, (b) sparse high-dimensional data — little prefix sharing, (c) very long average transaction length — deep trees with many conditional levels.")),
    heading3("Q10 (Expert): How would you parallelize FP-Growth across multiple machines?"),
    para(rt("PFP-Growth (Li et al., RecSys 2008): (1) Parallel counting — each machine counts item frequencies on its shard; merge to get global F-list. (2) Group assignment — partition F-list items into g groups. (3) Parallel FP-Growth — each machine processes the transactions relevant to its assigned item groups (map phase: emit (group_id, transaction) for each relevant group; reduce phase: each reducer builds a local FP-tree for its group and mines it). (4) Collect results — union all frequent itemsets. This achieves linear speedup with number of machines while maintaining correctness because each item group's patterns are mined independently (no cross-group dependencies within a single mining step).")),
    heading3("Multi-Level Explanations"),
    heading3("PhD Researcher Explanation"),
    para(rt("FP-Growth is a divide-and-conquer algorithm on the projected database lattice. It constructs a compressed suffix-tree representation (FP-tree) using frequency-ordered prefixes, achieving maximum prefix-sharing. Mining proceeds by conditional prefix projection — factoring the search space into independent sub-problems: {X ∪ {x_i}} for each x_i, where the conditional FP-tree precisely encodes the projected database D|x_i. The algorithm is complete by the theorem that every frequent pattern is uniquely associated with its lowest-ranked item in the F-list ordering and is captured in exactly that item's conditional FP-tree. The FP-tree structure is isomorphic to a trie over frequency-sorted transactions; the header table provides O(1) access to any item's node chain.")),
    heading3("Research Scientist / Engineer Explanation"),
    para(rt("FP-Growth does two passes over the data. First pass builds the header table (item frequencies). Second pass inserts each transaction (filtered to frequent items, sorted by frequency) into a prefix tree. To mine, for each item x_i bottom-up in frequency order: follow its node-links to collect all tree paths ending at x_i nodes, creating the conditional pattern base. Build a new FP-tree from those paths, recurse. Each recursive call solves a sub-problem — 'find all patterns containing x_i.' No candidates are ever generated.")),
    heading3("System Design Angle"),
    para(rt("FP-Growth in production recommendation systems: mine frequent co-purchases for collaborative filtering seeds. Challenges at scale: database too large for in-memory FP-tree → partition by first item (PFP-Growth), run local FP-Growth per partition, merge results. In e-commerce, the association rules derived (antecedent → consequent, confidence ≥ threshold) power 'frequently bought together' widgets. Used in: market basket analysis, web clickstream mining, bioinformatics (frequent gene expression co-regulation patterns), network intrusion detection (frequent syscall sequences).")),
    callout("🚩", rt("Red Flags: ", bold=True), rt("Saying 'FP-Growth is always faster than Apriori' (false for sparse/low-density data). Confusing the conditional pattern BASE (prefix paths) with the conditional FP-TREE (the new tree built from those paths). Not knowing that item ordering in the FP-tree MUST follow F-list order — reordering breaks prefix-sharing correctness. Claiming FP-Growth needs more than 2 database scans.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 8: Comparison & Trade-offs
    # ══════════════════════════════════════════════════════════════════════
    heading2("Comparison & Trade-offs"),
    table(5,
        table_row(["Dimension", "Apriori", "FP-Growth", "ECLAT", "PrefixSpan"]),
        table_row(["DB Scans", "2k (one per itemset size)", "2", "1 (vertical format)", "1"]),
        table_row(["Candidates", "Exponential", "None", "None", "None"]),
        table_row(["Data format", "Horizontal", "Horizontal", "Vertical (tid-lists)", "Horizontal"]),
        table_row(["Memory", "Low", "Moderate", "High (tid-lists)", "Low"]),
        table_row(["Dense DB", "Very slow", "Fast", "Moderate", "Fast"]),
        table_row(["Sparse DB", "OK", "Slower", "Faster", "Fast"]),
        table_row(["Sequential patterns", "No", "No", "No", "Yes"]),
        table_row(["Implementation", "Simple", "Moderate", "Simple", "Moderate"]),
    ),
    heading3("When to Use FP-Growth"),
    bullet(rt("Dense transaction databases (average transaction length > 10 items)")),
    bullet(rt("min_sup not extremely low — tree stays manageable in memory")),
    bullet(rt("Sufficient RAM available for FP-tree (fits in memory)")),
    bullet(rt("Need all frequent itemsets (not just top-k)")),
    bullet(rt("Batch mining on a static snapshot of the database")),
    heading3("When NOT to Use FP-Growth"),
    bullet(rt("Very sparse databases — FP-tree offers little compression; use ECLAT or Apriori")),
    bullet(rt("Streaming data — FP-tree must be rebuilt on updates; use stream mining algorithms")),
    bullet(rt("Distributed setting with very large data — use PFP-Growth or YAFIM (MapReduce)")),
    bullet(rt("Memory-constrained environments — use Apriori (iterative, low RAM) or disk-based partition algorithm")),
    bullet(rt("Sequential pattern mining required — use PrefixSpan or GSP")),
    callout("🎯", rt("Decision: ", bold=True), rt("Use FP-Growth for dense datasets with moderate min_sup and sufficient RAM. Use ECLAT for sparse datasets with few frequent items and abundant memory. Use Apriori when simplicity and low memory matter more than speed. Use PrefixSpan for sequential (ordered) patterns.")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 9: Interactive Visual Explainer
    # ══════════════════════════════════════════════════════════════════════
    heading2("Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through FP-tree construction and pattern mining — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ══════════════════════════════════════════════════════════════════════
    # Section 10: Related Topics & Further Reading
    # ══════════════════════════════════════════════════════════════════════
    heading2("Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Apriori algorithm — FP-Growth is a direct replacement; understand candidate generation and anti-monotone property first")),
    bullet(rt("Itemset mining basics: support, confidence, lift, conviction")),
    bullet(rt("Tree data structures: prefix trees (tries) and linked lists")),
    bullet(rt("Support/confidence/lift metrics for association rules")),
    heading3("What to Learn Next"),
    bullet(rt("Association rules: confidence, lift, conviction, leverage — build rules from frequent itemsets")),
    bullet(rt("Sequential pattern mining: PrefixSpan, GSP — extend to ordered sequences")),
    bullet(rt("ECLAT algorithm: vertical tid-list format, intersection-based support counting")),
    bullet(rt("Market basket analysis applications: recommendation engines, cross-selling, shelf placement")),
    bullet(rt("PFP-Growth: parallel FP-Growth across MapReduce for web-scale mining")),
    heading3("Key Papers"),
    numbered(rt("Han, J., Pei, J., & Yin, Y. (2000). \"Mining Frequent Patterns without Candidate Generation.\" SIGMOD 2000. — Original FP-Growth paper.")),
    numbered(rt("Agrawal, R. & Srikant, R. (1994). \"Fast algorithms for mining association rules.\" VLDB 1994. — Apriori, the predecessor.")),
    numbered(rt("Li, H., Wang, Y., Zhang, D., Zhang, M., & Chang, E. Y. (2008). \"PFP: Parallel FP-Growth for Query Recommendation.\" RecSys 2008. — Distributed FP-Growth.")),
    numbered(rt("Zaki, M. J. (2000). \"Scalable algorithms for association mining.\" IEEE TKDE 2000. — ECLAT (vertical format alternative).")),
    heading3("Best Resources"),
    bullet(rt("Han, Kamber & Pei \"Data Mining: Concepts and Techniques\" 3rd ed., Chapter 6 — canonical textbook treatment")),
    bullet(rt("Coursera: \"Pattern Discovery in Data Mining\" (University of Illinois) — covers FP-Growth with visual walkthroughs")),
    bullet(rt("mlxtend library documentation for fpgrowth() — production-ready implementation with pandas integration")),
    bullet(rt("Original SIGMOD 2000 paper (Han et al.) — 9 pages, very readable, includes full proofs")),
    callout("🔗", rt("FP-Growth connects to: ", bold=True), rt("Apriori Algorithm, ECLAT, Sequential Pattern Mining (PrefixSpan), Market Basket Analysis, Recommendation Systems (collaborative filtering), Bioinformatics (gene expression co-regulation patterns), Web Clickstream Mining")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
