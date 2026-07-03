"""
Notion page updater for the "No Free Lunch Theorem" topic.
Run with NOTION_API_TOKEN set in environment.
"""

from notion_template import (
    update_page,
    heading2, heading3,
    para, equation_block, callout,
    bullet, numbered, code_block,
    toggle, table, table_row, embed,
    rt, eq,
)

# ── Page Config ────────────────────────────────────────────────────────────────
PAGE_ID = "33c93418-809c-8174-8479-e4b02d572a4d"
ICON = "🟢"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Foundational"}},
    "Interview Priority": {"select": {"name": "Important"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/no_free_lunch_explainer.html"},
}

# ── Blocks ─────────────────────────────────────────────────────────────────────
blocks = [

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1: 30-SECOND VERSION
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Imagine you run a tournament where many different algorithms compete on every conceivable learning problem — from recognising cats in photos to predicting stock prices to classifying random noise. The No Free Lunch (NFL) theorem says that when you tally up the total score across ALL possible problems, every algorithm ties. No algorithm is universally better than any other.")),
    heading3("Real-World Analogy"),
    para(rt("Think of it like a buffet where every dish is equally good on average — but only because the buffet includes things you'd never actually eat (rocks, motor oil, sawdust). If you restrict to food you actually want, suddenly some chefs are clearly better. NFL tells us the 'restriction to real food' is called inductive bias.")),
    callout("💡", rt("If you remember one thing: There is no universally best learning algorithm — performance advantage always comes from matching your algorithm's assumptions (inductive bias) to the structure of your actual problem.")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: HISTORICAL CONTEXT
    # ══════════════════════════════════════════════════════════════════════════
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("In the 1980s and early 1990s, the ML community debated which algorithm was 'best.' Decision trees, neural networks, SVMs, and nearest-neighbours all had enthusiastic proponents claiming universal superiority. NFL settled the debate — not by picking a winner, but by proving no winner can exist.")),
    heading3("Key Papers"),
    para(rt("Wolpert, D. H. (1996). ", bold=True), rt("The Lack of A Priori Distinctions Between Learning Algorithms. "), rt("Neural Computation, 8(7). — Formal proof of NFL for supervised learning.")),
    para(rt("Wolpert, D. H. & Macready, W. G. (1997). ", bold=True), rt("No Free Lunch Theorems for Optimization. "), rt("IEEE Transactions on Evolutionary Computation, 1(1). — Extension to search/optimization.")),
    heading3("Evolution Timeline"),
    bullet(rt("Pre-1996: Algorithm wars — practitioners claim universal bests")),
    bullet(rt("1996: Wolpert proves NFL for supervised learning")),
    bullet(rt("1997: NFL extended to search and optimization (Wolpert & Macready)")),
    bullet(rt("2000s: NFL motivates inductive bias research, Bayesian methods, and ensemble methods")),
    bullet(rt("Today: NFL is foundational to AutoML, NAS, and meta-learning — why we need task-specific priors")),
    heading3("Comparison: Before vs After NFL"),
    table(
        3,
        table_row(["Dimension", "Before NFL", "After NFL"]),
        table_row(["Dominant belief", "One algorithm can be universally best", "No algorithm is universally best"]),
        table_row(["Research goal", "Find the best algorithm", "Find the best algorithm for a given problem class"]),
        table_row(["Practice", "Apply favorite algorithm everywhere", "Match algorithm bias to problem structure"]),
        table_row(["Theory", "Empirical claims of superiority", "Formal impossibility results"]),
        table_row(["Foundation for", "Algorithm advocacy", "Meta-learning, AutoML, Bayesian optimization"]),
    ),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3: CORE CONCEPTS & THEORY
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definition"),
    para(
        rt("Let "),
        eq(r"\mathcal{F}"),
        rt(" be the set of ALL possible target functions "),
        eq(r"f: \mathcal{X} \to \mathcal{Y}"),
        rt(" and let "),
        eq(r"A_1, A_2"),
        rt(" be any two learning algorithms. The NFL theorem states that summed over all "),
        eq(r"f \in \mathcal{F}"),
        rt(" (with uniform probability), both algorithms have identical expected generalization error:"),
    ),
    equation_block(r"\sum_{f \in \mathcal{F}} \mathcal{L}(A_1, f, \mathcal{D}) = \sum_{f \in \mathcal{F}} \mathcal{L}(A_2, f, \mathcal{D})"),
    para(
        rt("where "),
        eq(r"\mathcal{L}(A, f, \mathcal{D})"),
        rt(" is the generalization error of algorithm "),
        eq(r"A"),
        rt(" trained on dataset "),
        eq(r"\mathcal{D}"),
        rt(" and evaluated on target "),
        eq(r"f"),
        rt("."),
    ),
    heading3("Building Blocks"),
    bullet(rt("Target function space 𝓕: ALL possible mappings from inputs to outputs — including completely random ones")),
    bullet(rt("Generalization error ℒ: How well the learned model predicts on unseen data")),
    bullet(rt("Inductive bias: The assumptions an algorithm makes that restrict which hypotheses it prefers")),
    bullet(rt("Problem class: The subset of 𝓕 that actually occurs in a real-world domain")),
    callout("🔑", rt("Key Concept: ", bold=True), rt("NFL holds because for every problem where algorithm A beats B, there is a complementary problem where B beats A by the exact same margin. The wins and losses cancel perfectly.")),
    heading3("Prerequisites"),
    bullet(rt("Probability theory — expectation, distributions over function spaces")),
    bullet(rt("Supervised learning — generalization error, training vs test sets")),
    bullet(rt("Hypothesis spaces — the set of models an algorithm can express")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4: ARCHITECTURE & INTERNAL WORKINGS
    # ══════════════════════════════════════════════════════════════════════════
    heading2("⚙️ Architecture & Internal Workings"),
    heading3("How the Proof Works (Proof Sketch)"),
    para(rt("The proof is elegant. Consider a binary classification problem over a finite input space 𝒳 of size n. There are exactly 2ⁿ possible target functions (each input can map to 0 or 1). The key observation:")),
    numbered(rt("Training on dataset 𝒟 fixes the labels for |𝒟| points. Any algorithm must generalize to the remaining n − |𝒟| points.")),
    numbered(rt("For each unseen point, there are 2^(n−|D|) target functions consistent with 𝒟. Half predict 0, half predict 1.")),
    numbered(rt("Therefore, no matter what the algorithm outputs for unseen points, exactly half the consistent target functions will agree with it and half will disagree.")),
    numbered(rt("This means every algorithm achieves exactly 50% accuracy on unseen data, averaged across all consistent target functions.")),
    para(rt("This is not a coincidence — it's a combinatorial identity. The training data constrains nothing about unseen behavior when you average over all functions.")),
    heading3("Numerical Trace"),
    para(rt("Example with |𝒳| = 3, |𝒟| = 1:", bold=True)),
    para(rt("Suppose 𝒳 = {x₁, x₂, x₃} and our training set contains only (x₁, 1). There are 2² = 4 possible target functions on the unseen points {x₂, x₃}: {(0,0), (0,1), (1,0), (1,1)}. Algorithm A predicts (0, 0) for unseen points. Matches: (0,0) ✓, (0,1) ½ credit, (1,0) ½ credit, (1,1) ✗. Average: 2/4 = 50%. Algorithm B predicts (1, 1). Matches: (0,0) ✗, (0,1) ½, (1,0) ½, (1,1) ✓. Average: 2/4 = 50%. Both score the same.")),
    heading3("Why Inductive Bias Saves Us"),
    para(rt("In practice, we do not care about all possible target functions. Real problems have structure: natural images are smooth, stock prices have momentum, language follows grammar. When we restrict 𝓕 to the actually-occurring subset 𝓕_real, the symmetry of NFL breaks — and algorithms with the right inductive bias for 𝓕_real win.")),
    callout("💡", rt("Design Decision: ", bold=True), rt("This is why deep neural networks dominate vision (they have translation-equivariance bias via convolutions) but struggle on tabular data (where gradient-boosted trees with their piecewise-constant bias win).")),
    heading3("Edge Cases & Failure Modes"),
    bullet(rt("NFL assumes uniform distribution over 𝓕 — unrealistic but mathematically necessary for the theorem")),
    bullet(rt("NFL does NOT say all algorithms perform equally on any specific problem")),
    bullet(rt("NFL applies to exact generalization performance, not computational cost, sample efficiency, or robustness")),
    bullet(rt("In continuous spaces, the theorem requires measure-theoretic care — the finite-space version is the cleanest")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5: THE MATH
    # ══════════════════════════════════════════════════════════════════════════
    heading2("📐 The Math Behind It"),
    heading3("Formal Statement (Wolpert 1996)"),
    para(
        rt("Let "),
        eq(r"\mathcal{X}"),
        rt(" be a finite input space, "),
        eq(r"\mathcal{Y} = \{0,1\}"),
        rt(" be the label space, and "),
        eq(r"\mathcal{F} = \mathcal{Y}^{\mathcal{X}}"),
        rt(" be the set of all Boolean target functions. Let "),
        eq(r"\mathcal{D}"),
        rt(" be any fixed training set of size m, and let "),
        eq(r"\mathcal{L}"),
        rt(" be any loss function. Then for any two algorithms "),
        eq(r"A_1"),
        rt(" and "),
        eq(r"A_2"),
        rt(":"),
    ),
    equation_block(r"\sum_{f \in \mathcal{F}} \mathbb{E}_{\mathcal{D}}\left[\mathcal{L}\left(A_i(\mathcal{D}), f, \mathcal{D}^c\right)\right] = \text{const}, \quad i = 1, 2"),
    para(rt("where 𝒟ᶜ denotes the test set (complement of training inputs).")),
    heading3("Proof Sketch (Combinatorial)"),
    para(
        rt("For a finite input space with "),
        eq(r"|\mathcal{X}| = n"),
        rt(" and "),
        eq(r"|\mathcal{D}| = m"),
        rt(", there are "),
        eq(r"|\mathcal{F}| = 2^n"),
        rt(" target functions. After conditioning on the training data, we must predict on the "),
        eq(r"n - m"),
        rt(" unseen points."),
    ),
    numbered(
        rt("For any unseen point "),
        eq(r"x^*"),
        rt(", exactly half of all target functions predict 0 and half predict 1:"),
    ),
    equation_block(r"\left|\{f \in \mathcal{F} : f(x^*) = 0\}\right| = \left|\{f \in \mathcal{F} : f(x^*) = 1\}\right| = \frac{|\mathcal{F}|}{2}"),
    numbered(
        rt("Any algorithm must pick some prediction for "),
        eq(r"x^*"),
        rt(". Call it "),
        eq(r"\hat{y}"),
        rt(". Then:"),
    ),
    equation_block(r"\sum_{f \in \mathcal{F}} \mathbf{1}\left[A(\mathcal{D})(x^*) \neq f(x^*)\right] = \frac{|\mathcal{F}|}{2}"),
    numbered(rt("Summing over all unseen points and all target functions gives the same total error for every algorithm:")),
    equation_block(r"\sum_{f \in \mathcal{F}} \mathcal{L}(A, f, \mathcal{D}) = \frac{(n-m) \cdot |\mathcal{F}|}{2}"),
    para(rt("This is purely combinatorial — no assumptions about the algorithm structure are needed.")),
    heading3("Implications for PAC Learning"),
    para(
        rt("In PAC learning, we bound "),
        eq(r"\mathcal{L}(A, f, \mathcal{D})"),
        rt(" for a specific function class "),
        eq(r"\mathcal{H} \subset \mathcal{F}"),
        rt(". NFL is consistent with PAC theory — PAC bounds are tight precisely because they assume the target comes from a restricted class, not all of "),
        eq(r"\mathcal{F}"),
        rt("."),
    ),
    callout("⚠️", rt("Warning: ", bold=True), rt("A common misconception is that NFL means 'all algorithms are equally useless.' Wrong. It means equal performance averaged over ALL tasks including adversarial ones. For any specific task distribution, one algorithm can dramatically outperform another.")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6: CODE IMPLEMENTATION
    # ══════════════════════════════════════════════════════════════════════════
    heading2("💻 Code Implementation"),
    heading3("6a — Demonstrating NFL from Scratch"),
    code_block("python", """\
import numpy as np
from itertools import product

def all_target_functions(n_points):
    \"\"\"Generate all 2^n binary target functions over n points.\"\"\"
    for labels in product([0, 1], repeat=n_points):
        yield np.array(labels)

def evaluate_algorithm(predict_fn, train_X, train_y, test_X, target_fn):
    \"\"\"Evaluate a learning algorithm on a specific target function.\"\"\"
    # Train: algorithm sees (train_X, train_y)
    prediction = predict_fn(train_X, train_y, test_X)
    # Test: compare predictions to target function on unseen points
    true_labels = target_fn[test_X]
    return np.mean(prediction != true_labels)  # error rate

# Setup: 4 input points, train on 2, test on 2
n_total = 4
train_idx = np.array([0, 1])
test_idx = np.array([2, 3])

# Algorithm 1: always predict 0 on test set
def always_zero(train_X, train_y, test_X):
    return np.zeros(len(test_X), dtype=int)

# Algorithm 2: always predict 1 on test set
def always_one(train_X, train_y, test_X):
    return np.ones(len(test_X), dtype=int)

# Algorithm 3: majority vote from training labels
def majority_vote(train_X, train_y, test_X):
    majority = int(np.round(np.mean(train_y)))
    return np.full(len(test_X), majority, dtype=int)

algorithms = [always_zero, always_one, majority_vote]
alg_names  = ['Always-0', 'Always-1', 'Majority']
total_errors = {name: 0.0 for name in alg_names}
n_functions = 0

for target in all_target_functions(n_total):
    train_y = target[train_idx]
    for alg, name in zip(algorithms, alg_names):
        err = evaluate_algorithm(alg, train_idx, train_y, test_idx, target)
        total_errors[name] += err
    n_functions += 1

print(f'Total target functions: {n_functions}')
for name, total_err in total_errors.items():
    avg_err = total_err / n_functions
    print(f'{name}: avg error = {avg_err:.4f}')

# Output:
# Total target functions: 16
# Always-0:    avg error = 0.5000   <- ALL THE SAME
# Always-1:    avg error = 0.5000   <- NFL in action
# Majority:    avg error = 0.5000   <- regardless of strategy
"""),
    heading3("6b — Practical Implication: Choosing Biases"),
    code_block("python", """\
from sklearn.datasets import make_classification, make_regression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
import numpy as np

# NFL in practice: no single winner across problem types
results = {}

# Problem 1: Low-dimensional, linearly separable — simple bias wins
X1, y1 = make_classification(n_features=5, n_informative=3, random_state=42)

# Problem 2: High-dimensional, non-linear — complex bias wins
X2, y2 = make_classification(n_features=50, n_informative=20,
                              n_clusters_per_class=3, random_state=42)

algorithms = {
    'Decision Tree': DecisionTreeClassifier(max_depth=5),
    'Neural Net':    MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=500),
    'k-NN':          KNeighborsClassifier(n_neighbors=5),
}

for prob_name, (X, y) in [('Simple', (X1, y1)), ('Complex', (X2, y2))]:
    for alg_name, alg in algorithms.items():
        score = cross_val_score(alg, X, y, cv=5).mean()
        results[(prob_name, alg_name)] = score
        print(f'{prob_name} | {alg_name}: {score:.3f}')

# Key insight: No single algorithm wins on both problems.
# NFL says: if you could create ALL possible problems,
# every algorithm would average to the same score.
# But for YOUR real problems, match bias to structure!
"""),
    callout("⚠️", rt("Gotcha: ", bold=True), rt("Running this code will show one algorithm winning on the simple problem and a different one on the complex problem — NFL in action, even with just 2 problem instances.")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 7: INTERVIEW DEEP-DIVE
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy): What is the No Free Lunch theorem?"),
    toggle(
        [rt("Answer", bold=True)],
        [
            para(rt("The NFL theorem states that averaged over all possible target functions (with uniform distribution), every learning algorithm has the same expected generalization error. No algorithm is universally superior to any other.")),
            callout("⚠️", rt("Follow-up trap: ", bold=True), rt("'So we should just pick algorithms randomly?' No — NFL is about averaging over ALL problems including random ones. For any real problem distribution, algorithms with the right inductive bias win.")),
        ],
    ),
    heading3("Q2 (Medium): What is inductive bias, and why does it matter given NFL?"),
    toggle(
        [rt("Answer", bold=True)],
        [
            para(rt("Inductive bias is the set of assumptions an algorithm makes to generalize beyond training data. NFL says these assumptions can't help universally — but they CAN help on specific problem classes. CNNs have translation-equivariance bias (good for images), decision trees have axis-aligned split bias (good for tabular data), GPs have smoothness bias. The 'free lunch' you get in practice is paid for by matching your bias to your domain.")),
        ],
    ),
    heading3("Q3 (Medium): How does NFL relate to the bias-variance tradeoff?"),
    toggle(
        [rt("Answer", bold=True)],
        [
            para(rt("They are complementary. Bias-variance describes error decomposition for a single problem and algorithm. NFL says you can't escape this tradeoff globally — lowering bias increases variance, and averaged over all problems, your total error stays constant. Choosing a high-bias algorithm that fits your problem class reduces variance without hurting total error across your relevant problem class.")),
        ],
    ),
    heading3("Q4 (Hard): Can you prove the NFL theorem for a simple case?"),
    toggle(
        [rt("Answer", bold=True)],
        [
            para(rt("For binary classification over a finite input space 𝒳 with |𝒳| = n, there are 2ⁿ target functions. After training on m points, any algorithm must predict on the remaining n−m points. For any unseen point x*, exactly half of all 2ⁿ target functions map it to 0 and half to 1. So regardless of what the algorithm predicts, it disagrees with exactly half the target functions at x*. Summing over all unseen points and all target functions, every algorithm achieves total error = (n−m)·2ⁿ/2, the same for all algorithms. QED.")),
        ],
    ),
    heading3("Q5 (Hard): How does NFL affect AutoML and neural architecture search?"),
    toggle(
        [rt("Answer", bold=True)],
        [
            para(rt("NFL implies that no single architecture or hyperparameter configuration can be universally optimal. AutoML and NAS are justified precisely because we need task-specific optimization — the 'best' architecture depends on the problem. This also explains why meta-learning works: it learns the prior over which architectures/algorithms tend to work for which problem classes, effectively encoding inductive bias about the task distribution.")),
        ],
    ),
    heading3("Two-Level Explanation"),
    heading3("Explain to a PhD Researcher"),
    para(rt("NFL is a measure-theoretic impossibility result: for any measurable loss function and any uniform prior over the function space 𝓕 = 𝒴^𝒳, the marginal expected loss is invariant to the choice of learner. The practical escape hatch is that real-world tasks come from a low-measure subset of 𝓕 that is far from uniform — and any learner whose hypothesis class assigns high prior mass to this subset will outperform on it while underperforming on the irrelevant complement.")),
    heading3("Explain to a Research Scientist/Engineer"),
    para(rt("NFL means: if you tested your model on every possible problem including random ones, you'd score the same as a coin flip. But you only care about your actual problem distribution. The key engineering insight: pick an architecture whose structural assumptions (equivariance, sparsity, smoothness) match your data's actual properties. That matching is what buys you performance — there's no free lunch, but you can eat cheaply if you order the right dish.")),
    heading3("Red Flags — Wrong Answers That Get You Rejected"),
    bullet(rt("Saying 'NFL means deep learning is never better than a decision tree' — NFL is about averages over all problems, not specific ones")),
    bullet(rt("Confusing NFL with the bias-variance tradeoff — related but distinct concepts")),
    bullet(rt("Claiming NFL is only about optimization, not learning — both versions exist but the supervised learning version is most relevant in ML")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 8: COMPARISON & TRADE-OFFS
    # ══════════════════════════════════════════════════════════════════════════
    heading2("⚖️ Comparison & Trade-offs"),
    table(
        4,
        table_row(["Concept", "What It Says", "Scope", "Implication"]),
        table_row(["NFL Theorem", "All algorithms equal on average over all problems", "All possible target functions, uniform prior", "No universally best algorithm — must use inductive bias"]),
        table_row(["Bias-Variance Tradeoff", "Error = Bias² + Variance + Noise", "Single problem, single algorithm", "Choose model complexity to balance underfitting/overfitting"]),
        table_row(["Occam's Razor", "Simpler models generalize better", "Restricted to regular/smooth problems", "Prefer simpler hypotheses — an inductive bias itself"]),
        table_row(["PAC Learning", "Bounds on sample complexity for a hypothesis class", "Fixed function class, worst-case target", "Algorithms CAN be provably better within a class"]),
        table_row(["Ugly Duckling Theorem", "All objects are equally similar", "All possible features with uniform prior", "Feature selection requires domain-specific bias"]),
    ),
    heading3("When NFL Applies"),
    bullet(rt("Theoretical analysis comparing algorithm families")),
    bullet(rt("Motivating inductive bias choices in model design")),
    bullet(rt("Understanding why AutoML and NAS are necessary")),
    bullet(rt("Meta-learning: learning which algorithm works for which task class")),
    heading3("When NFL Does NOT Apply (Common Misconception)"),
    bullet(rt("Comparing algorithms on a specific dataset — there can be clear winners")),
    bullet(rt("When problem structure is known — the uniform prior breaks down")),
    bullet(rt("Practical ML engineering — you always have domain knowledge")),
    callout("🎯", rt("Decision: ", bold=True), rt("NFL is a theoretical lens, not a practical constraint. Use it to justify WHY you need domain-specific inductive bias, not as an excuse to avoid choosing algorithms carefully.")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 9: VISUAL EXPLAINER
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/no_free_lunch_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10: RELATED TOPICS
    # ══════════════════════════════════════════════════════════════════════════
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Probability Theory & Statistics — distributions, expectations, uniform priors")),
    bullet(rt("Introduction to Machine Learning — supervised learning, generalization")),
    bullet(rt("Hypothesis Space & Model Complexity — VC dimension, capacity")),
    heading3("What to Learn Next"),
    bullet(rt("Inductive Bias & Regularization — L1/L2, dropout as bias mechanisms")),
    bullet(rt("Bias-Variance Tradeoff — the per-problem complement to NFL")),
    bullet(rt("Bayesian Learning — explicit priors as inductive bias")),
    bullet(rt("Meta-Learning & AutoML — automated inductive bias selection")),
    bullet(rt("PAC Learning — formal sample complexity bounds within hypothesis classes")),
    heading3("Key Papers"),
    bullet(rt("Wolpert (1996)", bold=True), rt(" — The Lack of A Priori Distinctions Between Learning Algorithms. Neural Computation.")),
    bullet(rt("Wolpert & Macready (1997)", bold=True), rt(" — No Free Lunch Theorems for Optimization. IEEE Trans. Evolutionary Computation.")),
    bullet(rt("Mitchell (1980)", bold=True), rt(" — The Need for Biases in Learning Generalizations. Rutgers TR. (pre-NFL motivation)")),
    bullet(rt("Schaffer (1994)", bold=True), rt(" — A Conservation Law for Generalization Performance. ICML. (precursor result)")),
    heading3("Best Resources"),
    bullet(rt("Mitchell, T. Machine Learning (1997) — Chapter 7: Computational Learning Theory")),
    bullet(rt("Shalev-Shwartz & Ben-David, Understanding Machine Learning (2014) — Chapter 5: The Bias-Complexity Tradeoff")),
    bullet(rt("Pedro Domingos, 'A Few Useful Things to Know About Machine Learning' (2012) — best practical NFL discussion")),
    callout("🔗", rt("This topic connects to: Inductive Bias · Bias-Variance Tradeoff · PAC Learning · Bayesian Learning · Meta-Learning · AutoML · VC Dimension · Occam's Razor · Regularization")),
]

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    update_page(PAGE_ID, ICON, PROPERTIES, blocks)
