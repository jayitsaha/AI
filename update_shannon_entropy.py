#!/usr/bin/env python3
"""Update Notion page for: Entropy: Shannon entropy H(X), interpretation as uncertainty/information content"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81d1-9916-d704b303f4dd"
ICON = "🟢"  # Foundational
PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Foundational"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/shannon_entropy_explainer.html"},
}

blocks = [
    # ── Section 1: The 30-Second Version ──
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(
        rt("Shannon entropy "),
        eq(r"H(X)"),
        rt(" is a single number that measures how uncertain or unpredictable a random variable is. "
           "If you already know what will happen (a coin that always lands heads), entropy is 0 — no surprise. "
           "If you have no idea (a fair coin), entropy is 1 bit — maximum uncertainty for a binary choice.")
    ),
    heading3("Real-World Analogy"),
    para(
        rt("Imagine a weather forecaster in two cities. City A: a desert where it never rains — the forecast "
           "\"no rain\" tells you nothing new (entropy ≈ 0). City B: an unpredictable coastal city where rain "
           "is equally likely any day — each forecast genuinely informs you (entropy is high). "
           "Shannon entropy quantifies exactly this: how much information, on average, does each outcome give you?")
    ),
    callout("💡", rt("If you remember one thing: ", bold=True),
            rt("Entropy is the average surprise. Each outcome "),
            eq(r"x_i"),
            rt(" with probability "),
            eq(r"p_i"),
            rt(" carries surprise "),
            eq(r"-\log_2 p_i"),
            rt(" bits. Entropy is the expectation of this surprise: "),
            eq(r"H(X) = -\sum_i p_i \log_2 p_i")),
    divider(),

    # ── Section 2: Historical Context ──
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("Before 1948, information had no formal mathematical definition. Engineers designing "
            "telegraph and telephone systems needed to know: how efficiently can a message be compressed? "
            "What is the maximum rate at which a noisy channel can transmit data reliably? These questions "
            "had no rigorous answers.")),
    heading3("The Breakthrough"),
    para(rt("Claude Shannon's 1948 paper \"A Mathematical Theory of Communication\" (Bell System Technical Journal) "
            "introduced the entropy formula and proved two landmark theorems: the source coding theorem "
            "(entropy = minimum average bits per symbol for lossless compression) and the channel capacity theorem "
            "(noisy channels have a definite bit-rate limit). This single paper founded the entire field of "
            "information theory.")),
    heading3("Evolution Timeline"),
    bullet(rt("1948 — Shannon introduces entropy, mutual information, channel capacity")),
    bullet(rt("1952 — Huffman coding: a practical algorithm achieving entropy limit")),
    bullet(rt("1965 — Kolmogorov complexity: algorithmic entropy for individual strings")),
    bullet(rt("1990s — Entropy adopted in ML: decision trees (ID3, C4.5), maximum entropy models")),
    bullet(rt("2000s–present — Cross-entropy becomes the dominant loss function in deep learning")),
    heading3("Before vs After Shannon"),
    table(3,
        table_row(["Dimension", "Before Shannon (1948)", "After Shannon"]),
        table_row(["Information", "Vague intuition", "Mathematically defined as −log p"]),
        table_row(["Compression", "Ad hoc coding", "Proven lower bound: H(X) bits/symbol"]),
        table_row(["Channel capacity", "Unknown", "C = max I(X;Y) bits/channel use"]),
        table_row(["ML losses", "Mean squared error", "Cross-entropy grounded in entropy theory"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ──
    heading2("🔑 Core Concepts & Theory"),
    heading3("Self-information (surprise)"),
    para(rt("The self-information (or surprisal) of a single event "),
         eq(r"x_i"),
         rt(" with probability "),
         eq(r"p_i"),
         rt(" is:")),
    equation_block(r"I(x_i) = -\log_2 p_i \text{ bits}"),
    para(rt("Three axioms uniquely determine this form: (1) non-negativity, (2) certain events give 0 surprise, "
            "(3) surprise of two independent events adds. The logarithm is the only function satisfying all three.")),
    heading3("Shannon Entropy"),
    para(rt("Entropy is the expected self-information over the distribution:")),
    equation_block(r"H(X) = \mathbb{E}[-\log_2 p(X)] = -\sum_{i=1}^{n} p_i \log_2 p_i"),
    para(rt("Convention: "),
         eq(r"0 \log_2 0 = 0"),
         rt(" (since "),
         eq(r"\lim_{p \to 0^+} p \log p = 0"),
         rt("). Units: bits (base 2), nats (base "),
         eq(r"e"),
         rt("), or hartleys (base 10).")),
    heading3("Binary Entropy Function"),
    para(rt("For a Bernoulli variable with "),
         eq(r"P(\text{success}) = p"),
         rt(":")),
    equation_block(r"H_b(p) = -p\log_2 p - (1-p)\log_2(1-p)"),
    para(rt("This bell curve peaks at "),
         eq(r"p = 0.5"),
         rt(" (1 bit) and reaches 0 at the endpoints. Key values: "
            "H_b(0.5)=1.000, H_b(0.9)=H_b(0.1)=0.469, H_b(0.2)=H_b(0.8)=0.722 bits.")),
    callout("🔑",
            rt("Key Property: ", bold=True),
            rt("Entropy is maximised by the uniform distribution, achieving "),
            eq(r"H_{\max} = \log_2 n"),
            rt(" bits for "),
            eq(r"n"),
            rt(" outcomes. Any concentration of probability reduces entropy.")),
    divider(),

    # ── Section 4: Architecture & Internal Workings ──
    heading2("🏗️ Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("Step-by-step computation: distribution [0.7, 0.2, 0.1]"),
    para(rt("Step 1: Assign self-information to each outcome:")),
    equation_block(r"I(A) = -\log_2 0.7 = 0.5146 \text{ bits}"),
    equation_block(r"I(B) = -\log_2 0.2 = 2.3219 \text{ bits}"),
    equation_block(r"I(C) = -\log_2 0.1 = 3.3219 \text{ bits}"),
    para(rt("Step 2: Weight each surprise by its probability (expected value):")),
    equation_block(r"H = 0.7 \times 0.5146 + 0.2 \times 2.3219 + 0.1 \times 3.3219 = 1.1568 \text{ bits}"),
    para(rt("Compare: uniform 3-way distribution has "),
         eq(r"\log_2 3 = 1.5850"),
         rt(" bits — 37% more entropy.")),
    heading3("Why the formula is an average"),
    para(rt("Entropy answers: \"if I draw many symbols from this distribution and encode them optimally, "
            "how many bits do I need per symbol on average?\" Rare events (large "),
         eq(r"-\log_2 p"),
         rt(") need long codes; common events (small "),
         eq(r"-\log_2 p"),
         rt(") get short codes. Weighting by "),
         eq(r"p_i"),
         rt(" gives the average.")),
    heading3("Design decision: why −log and not another function?"),
    para(rt("Shannon proved that any 'uncertainty measure' satisfying four axioms "
            "(continuity, symmetry, maximum at uniformity, grouping/additivity) must equal "
            "−K Σ p_i log p_i for some constant K. The log is not a design choice — it is forced.")),
    heading3("Edge cases and failure modes"),
    bullet(rt("p=0 terms: by convention 0·log(0)=0, handled by filtering p>0 before summing")),
    bullet(rt("Continuous distributions: differential entropy h(X)=−∫p(x)log p(x)dx, which can be negative")),
    bullet(rt("Entropy of a Dirac delta (certain): h→−∞ in continuous case; H=0 in discrete")),
    bullet(rt("Numerical stability: use log(p+ε) in code; or filter zeros before computing")),
    divider(),

    # ── Section 5: The Math ──
    heading2("📐 The Math Behind It"),
    heading3("Full Derivation: Why H = −Σ p log p?"),
    para(rt("Shannon (1948) imposed four axioms on any measure of uncertainty "),
         eq(r"H(p_1, \ldots, p_n)"),
         rt(":")),
    numbered(rt("Continuity: H is continuous in the "),
              eq(r"p_i")),
    numbered(rt("Maximum at uniformity: for fixed n, H is maximised when all "),
              eq(r"p_i = 1/n")),
    numbered(rt("Normalisation: "),
              eq(r"H(1/2, 1/2) = 1"),
              rt(" (1 bit for a fair coin)")),
    numbered(rt("Grouping (additivity): H is consistent when outcomes are grouped: "
                "H(p_1,...,p_n) = H(p_1+p_2, p_3,...)+（p_1+p_2)H(p_1/(p_1+p_2), p_2/(p_1+p_2))")),
    para(rt("The unique solution (Khinchin 1957, formalising Shannon) is:")),
    equation_block(r"H(p_1, \ldots, p_n) = -K \sum_{i=1}^n p_i \log p_i, \quad K > 0"),
    para(rt("With base-2 logarithm, K=1 and units are bits.")),
    heading3("Key Properties with Proofs"),
    para(rt("Non-negativity: "), eq(r"H(X) \geq 0")),
    para(rt("Proof: each term "), eq(r"-p_i \log_2 p_i \geq 0"), rt(" since "), eq(r"0 \leq p_i \leq 1 \Rightarrow \log_2 p_i \leq 0")),
    equation_block(r"H(X) \leq \log_2 n \text{ (maximum entropy)}"),
    para(rt("Proof via Jensen's inequality: since "), eq(r"\log"), rt(" is concave,")),
    equation_block(r"H = \mathbb{E}\!\left[\log \frac{1}{p(X)}\right] \leq \log\!\left(\mathbb{E}\!\left[\frac{1}{p(X)}\right]\right) = \log n"),
    heading3("Chain Rule"),
    equation_block(r"H(X, Y) = H(X) + H(Y \mid X)"),
    para(rt("Entropy of a joint distribution equals entropy of X plus the residual uncertainty in Y given X. "
            "This factorises the joint entropy into a sequence of conditional terms:")),
    equation_block(r"H(X_1, \ldots, X_n) = \sum_{i=1}^n H(X_i \mid X_1, \ldots, X_{i-1})"),
    heading3("Cross-Entropy and KL Divergence"),
    equation_block(r"H(q, p) = H(q) + D_{\mathrm{KL}}(q \| p) = -\sum_i q_i \log p_i"),
    para(rt("where "), eq(r"D_{\mathrm{KL}}(q \| p) = \sum_i q_i \log \frac{q_i}{p_i} \geq 0"),
         rt(" (Gibbs' inequality). Minimising cross-entropy loss is equivalent to minimising KL divergence, "
            "since "), eq(r"H(q)"), rt(" is fixed for a given dataset.")),
    callout("⚠️",
            rt("Common pitfall: ", bold=True),
            rt("PyTorch's cross_entropy uses natural log (nats). Multiply by "),
            eq(r"\log_2 e \approx 1.4427"),
            rt(" to convert to bits. Always check the log base when comparing values across sources.")),
    divider(),

    # ── Section 6: Code ──
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """\
import numpy as np

def surprise(p: float) -> float:
    \"\"\"Self-information of a single event (bits).\"\"\"
    if p <= 0 or p > 1:
        raise ValueError("Probability must be in (0, 1]")
    return -np.log2(p)

def entropy(probs) -> float:
    \"\"\"Shannon entropy of a discrete distribution (bits).
    Handles p=0 by convention (0 * log 0 = 0).
    \"\"\"
    probs = np.asarray(probs, dtype=float)
    assert np.isclose(probs.sum(), 1.0, atol=1e-6), "Probabilities must sum to 1"
    # Filter zeros: 0 * log(0) = 0 by convention
    nonzero = probs[probs > 0]
    return float(-np.sum(nonzero * np.log2(nonzero)))

def binary_entropy(p: float) -> float:
    \"\"\"Binary entropy function H_b(p).\"\"\"
    if p <= 0 or p >= 1:
        return 0.0
    return -p * np.log2(p) - (1 - p) * np.log2(1 - p)

# Examples
print(entropy([0.5, 0.5]))           # 1.0000 bits  (fair coin)
print(entropy([0.7, 0.2, 0.1]))      # 1.1568 bits
print(entropy([0.25] * 4))           # 2.0000 bits  (uniform 4-way)
print(entropy([1.0]))                # 0.0000 bits  (certain)
print(binary_entropy(0.5))          # 1.0000 bits
print(binary_entropy(0.9))          # 0.4690 bits

def cross_entropy(q_true, p_pred) -> float:
    \"\"\"Cross-entropy H(q, p) in bits.\"\"\"
    q = np.asarray(q_true); p = np.asarray(p_pred)
    return float(-np.sum(q * np.log2(p + 1e-12)))

# H(q) = 1.157, H(q,p) = 1.280, KL = 0.123
q, p = [0.7, 0.2, 0.1], [0.5, 0.3, 0.2]
print(f"H(q)={entropy(q):.4f}  H(q,p)={cross_entropy(q,p):.4f}  KL={cross_entropy(q,p)-entropy(q):.4f}")
"""),
    heading3("6b — Production Usage (PyTorch, sklearn)"),
    code_block("python", """\
import torch
import torch.nn.functional as F
from sklearn.metrics import log_loss

# ── PyTorch cross-entropy loss (nats) ──
logits = torch.tensor([[2.0, 1.0, 0.1]])   # shape (batch=1, classes=3)
target = torch.tensor([0])                  # true class index

# F.cross_entropy = log_softmax + NLLLoss (numerically stable)
loss = F.cross_entropy(logits, target)
# Nats → bits: multiply by log2(e)
print(f"CE loss: {loss.item():.4f} nats = {loss.item()*1.4427:.4f} bits")

# ── Entropy of model predictions ──
probs = F.softmax(logits, dim=-1)           # [0.576, 0.212, 0.212] approx
logprobs = torch.log2(probs + 1e-12)
H = -(probs * logprobs).sum(dim=-1)        # entropy per sample
print(f"Prediction entropy: {H.item():.4f} bits")

# ── sklearn: log_loss ≡ cross-entropy in nats ──
y_true = [0, 1, 2]
y_pred = [[0.9, 0.05, 0.05], [0.05, 0.9, 0.05], [0.05, 0.05, 0.9]]
print(f"sklearn log_loss: {log_loss(y_true, y_pred):.4f} nats")

# ── Entropy regularization in RL (e.g. SAC) ──
# Objective: J = E[r] + alpha * H(pi)
# High entropy -> diverse policy -> better exploration
alpha = 0.2  # entropy temperature coefficient
policy_entropy = H.mean()
objective = expected_reward + alpha * policy_entropy   # noqa
"""),
    callout("⚠️",
            rt("Gotcha: ", bold=True),
            rt("In PyTorch, nn.CrossEntropyLoss expects raw logits (not softmax outputs). "
               "Passing softmax probabilities leads to double-softmax and incorrect loss values. "
               "Also, do_sample=True is required in HuggingFace generate() for temperature to take effect.")),
    divider(),

    # ── Section 7: Interview Deep-Dive ──
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy): What is Shannon entropy and what does it measure?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Shannon entropy "),
             eq(r"H(X) = -\sum_i p_i \log_2 p_i"),
             rt(" measures the average uncertainty or information content of a random variable. "
                "High entropy = unpredictable distribution (many bits needed to encode outcomes); "
                "low entropy = concentrated distribution (few bits needed). It equals the minimum average "
                "number of yes/no questions needed to determine the outcome.")),
    ]),
    heading3("Q2 (Easy): What is the entropy of a fair coin? Of a biased coin (p=0.9)?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Fair coin: "),
             eq(r"H = -0.5\log_2 0.5 - 0.5\log_2 0.5 = 1"),
             rt(" bit. Biased coin (p=0.9): "),
             eq(r"H = -0.9\log_2 0.9 - 0.1\log_2 0.1 = 0.137 + 0.332 = 0.469"),
             rt(" bits. The biased coin is more predictable — less uncertainty, less information per toss.")),
    ]),
    heading3("Q3 (Medium): How is entropy related to cross-entropy loss in neural networks?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Cross-entropy loss is "),
             eq(r"\mathcal{L} = H(q, p) = -\sum_i q_i \log p_i"),
             rt(" where "),
             eq(r"q"),
             rt(" is the true label distribution (one-hot in classification) and "),
             eq(r"p"),
             rt(" is the model's softmax output. By the decomposition "),
             eq(r"H(q,p) = H(q) + D_{\mathrm{KL}}(q \| p)"),
             rt(", minimising cross-entropy is equivalent to minimising KL divergence, since "),
             eq(r"H(q)"),
             rt(" is constant for a fixed dataset.")),
    ]),
    heading3("Q4 (Medium): What is information gain in decision trees?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Information gain of a split on feature "),
             eq(r"F"),
             rt(" is:")),
        para(eq(r"IG(S, F) = H(S) - \sum_{v} \frac{|S_v|}{|S|} H(S_v)"),
             rt(" where "),
             eq(r"S_v"),
             rt(" is the subset of samples where "),
             eq(r"F = v"),
             rt(". We pick the split that maximises IG — i.e., reduces entropy (uncertainty about labels) the most. "
                "ID3 and C4.5 algorithms use this directly; CART uses Gini impurity as an approximation.")),
    ]),
    heading3("Q5 (Hard): What is the source coding theorem and why does it matter?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Shannon's source coding theorem states: for a stationary ergodic source with entropy "),
             eq(r"H(X)"),
             rt(" bits/symbol, any lossless code requires at least "),
             eq(r"H(X)"),
             rt(" bits/symbol on average, and codes achieving this limit exist (e.g., Huffman, arithmetic coding). "
                "This is important because it defines the fundamental limit of lossless compression — no algorithm "
                "can compress below entropy without loss. In ML, it explains why cross-entropy is the natural "
                "loss: minimising it maximises the likelihood of the data under the model, which is equivalent to "
                "finding the most efficient code for the data.")),
    ]),
    heading3("Q6 (Hard): What is entropy regularization and why is it used in RL?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("In reinforcement learning, adding an entropy bonus to the objective: "),
             eq(r"J(\pi) = \mathbb{E}[r] + \alpha H(\pi(\cdot|s))"),
             rt(" encourages the policy to remain stochastic and explore broadly. Without it, the policy can "
                "collapse to a deterministic strategy that exploits but fails to explore suboptimal actions. "
                "Soft Actor-Critic (SAC) and MaxEntRL maximise this augmented objective. The temperature "),
             eq(r"\alpha"),
             rt(" trades off reward maximisation vs exploration. Entropy regularization prevents mode collapse "
                "and leads to more robust, transferable policies.")),
    ]),
    heading3("Follow-up traps"),
    bullet(rt("\"Can entropy be negative?\" — For discrete distributions: never. For continuous differential entropy: yes (e.g., a very narrow Gaussian can have h → −∞).")),
    bullet(rt("\"Is high model output entropy always bad?\" — No. For uncertain inputs (out-of-distribution), high entropy is the correct honest response.")),
    bullet(rt("\"Does entropy equal information?\" — Entropy measures average information per observation. A single drawn outcome carries self-information −log p_i, not H(X).")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ──
    heading2("⚖️ Comparison & Trade-offs"),
    heading3("Entropy vs Related Measures"),
    table(4,
        table_row(["Measure", "Formula", "When to use", "Notes"]),
        table_row(["Shannon entropy H(X)", "-Σ p log p", "Uncertainty of a single variable", "Always ≥ 0 for discrete"]),
        table_row(["Joint entropy H(X,Y)", "-Σ p(x,y) log p(x,y)", "Uncertainty of two variables together", "H(X,Y) ≤ H(X)+H(Y)"]),
        table_row(["Conditional entropy H(Y|X)", "H(X,Y)−H(X)", "Residual uncertainty in Y given X", "≥ 0; = 0 iff Y determined by X"]),
        table_row(["Mutual information I(X;Y)", "H(X)−H(X|Y)", "Shared information / feature relevance", "Symmetric, always ≥ 0"]),
        table_row(["KL divergence D_KL(p‖q)", "Σ p log(p/q)", "Distribution mismatch (asymmetric)", "Not a metric; can be ∞"]),
        table_row(["Cross-entropy H(p,q)", "−Σ p log q", "Training loss in classification", "H(p)+KL(p‖q)"]),
        table_row(["Differential entropy h(X)", "−∫ f log f dx", "Continuous distributions", "Can be negative"]),
    ),
    heading3("Decision guide"),
    callout("🎯",
            rt("Use entropy when: ", bold=True),
            rt("measuring uncertainty of a distribution, choosing decision tree splits (information gain), "
               "regularizing policies in RL, or measuring label noise in datasets.\n"),
            rt("Use cross-entropy when: ", bold=True),
            rt("training classifiers (it is the correct log-likelihood loss).\n"),
            rt("Use KL divergence when: ", bold=True),
            rt("comparing two distributions (VAE latent loss, knowledge distillation, fine-tuning regularization).\n"),
            rt("Use mutual information when: ", bold=True),
            rt("measuring feature relevance or statistical dependence between variables.")),
    divider(),

    # ── Section 9: Interactive Explainer ──
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/shannon_entropy_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys. "
            "Card 4 includes live sliders to reshape a distribution and watch entropy update in real time.",
            italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics & Further Reading ──
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Probability theory: discrete distributions, expectation, conditional probability")),
    bullet(rt("Logarithm properties: log rules, change of base, limit of p log p as p→0")),
    heading3("What to learn next"),
    bullet(rt("KL Divergence — the directed distance between two distributions")),
    bullet(rt("Mutual Information — shared information between two random variables")),
    bullet(rt("Cross-Entropy Loss — the ML training loss derived from entropy")),
    bullet(rt("Huffman Coding — practical algorithm achieving the entropy bound")),
    bullet(rt("Maximum Entropy Principle — choosing distributions by maximizing entropy")),
    bullet(rt("Differential Entropy — entropy of continuous distributions")),
    heading3("Key Papers"),
    bullet(rt("Shannon, C.E. (1948). \"A Mathematical Theory of Communication.\" Bell System Technical Journal. — The founding paper; introduces entropy, channel capacity, source coding theorem.")),
    bullet(rt("Cover, T.M. & Thomas, J.A. (2006). \"Elements of Information Theory.\" 2nd ed. — The definitive graduate textbook.")),
    bullet(rt("Khinchin, A.I. (1957). \"Mathematical Foundations of Information Theory.\" — Rigorous axiomatic derivation of entropy.")),
    heading3("Best Resources"),
    bullet(rt("3Blue1Brown: \"Entropy in Compression\" (YouTube) — visual intuition for entropy as compression")),
    bullet(rt("Cover & Thomas, Chapters 2-3 — authoritative treatment of entropy and its properties")),
    bullet(rt("Stanford CS229 Notes on Information Theory — concise ML-oriented derivations")),
    callout("🔗",
            rt("This topic connects to: ", bold=True),
            rt("KL Divergence · Mutual Information · Cross-Entropy Loss · Huffman Coding · "
               "Maximum Entropy Models · Decision Trees (Information Gain) · Soft Actor-Critic (SAC) · "
               "Variational Autoencoders (ELBO) · Bayesian Information Criterion (BIC)")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
