#!/usr/bin/env python3
"""Update Notion page for: Bayes Theorem Application"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-81a4-bbf1-c264b014e5ff"
ICON = "🟡"
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/bayes_theorem_application_explainer.html"

PROPERTIES = {
    "Status":             {"select": {"name": "Completed"}},
    "Depth":              {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer":      {"checkbox": True},
    "Explainer URL":      {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: 30-Second Version ───────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Bayes' theorem is the mathematical rule for updating a belief when you see evidence. "
            "It answers: given that I observed X, how should I revise my probability that Y is true? "
            "It's the engine behind spam filters, medical diagnostics, and Bayesian ML models.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine you test positive for a rare disease. The test is '99% accurate.' Should you panic? "
            "Bayes says no — if the disease affects only 1 in 1000 people, "
            "even a positive result means only ~9% chance you actually have it. "
            "The rarity (prior) overwhelms the test's accuracy.")),
    callout("💡", rt("If you remember one thing: ", bold=True),
            rt("Posterior ∝ Likelihood × Prior. Ignoring the base rate (prior) is the base-rate fallacy "
               "— Bayes' theorem mathematically prevents it.")),
    divider(),

    # ── Section 2: Historical Context ──────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Before Bayes, probability was purely frequentist — you could only assign probabilities to "
            "repeatable experiments. There was no principled way to update beliefs given partial evidence, "
            "or to reason about one-off events like 'is this patient sick?'")),
    heading3("The Breakthrough"),
    para(rt("Thomas Bayes (1701–1761) wrote 'An Essay towards solving a Problem in the Doctrine of Chances,' "
            "published posthumously by Richard Price in 1763. Pierre-Simon Laplace independently rediscovered "
            "and generalized the theorem in 1812. It was largely ignored for a century in favor of frequentism, "
            "then revived in the 20th century as computers made Bayesian computation tractable.")),
    table(3,
        table_row(["Dimension", "Frequentist (Before)", "Bayesian (After)"]),
        table_row(["Probability of", "Long-run frequency", "Degree of belief"]),
        table_row(["Prior knowledge", "Not used", "Encoded as prior P(H)"]),
        table_row(["Output", "p-value (reject/fail)", "Full posterior distribution"]),
        table_row(["Rare events", "Requires many samples", "Handles via prior"]),
        table_row(["Interpretation", "95% CI ≠ 95% probability", "Credible interval is literal probability"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ────────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("The Three Components"),
    bullet(rt("Prior "), eq(r"P(H)"), rt(" — your belief about hypothesis H before observing evidence")),
    bullet(rt("Likelihood "), eq(r"P(E \mid H)"), rt(" — probability of observing evidence E if H is true")),
    bullet(rt("Posterior "), eq(r"P(H \mid E)"), rt(" — updated belief after observing E; what we actually want")),
    para(rt("The normalizing constant "), eq(r"P(E) = \sum_i P(E \mid H_i) P(H_i)"),
         rt(" ensures the posterior is a valid probability distribution summing to 1.")),
    callout("🔑", rt("Key Property: ", bold=True),
            rt("Posterior ∝ Likelihood × Prior. The normalizer just rescales. "
               "When comparing two hypotheses, their ratio (Bayes factor) tells you which is better supported.")),
    heading3("Bayes Factor"),
    para(rt("The Bayes factor "), eq(r"BF = \frac{P(E \mid H_1)}{P(E \mid H_0)}"),
         rt(" measures how much more likely the evidence is under H₁ vs H₀. "
            "BF > 10 is strong evidence, BF > 100 is decisive (Jeffreys scale).")),
    divider(),

    # ── Section 4: PhD Deep Dive ─────────────────────────────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD Deep Dive)"),
    heading3("Full Derivation from First Principles"),
    para(rt("Start from the definition of conditional probability:")),
    equation_block(r"P(A \mid B) = \frac{P(A \cap B)}{P(B)}"),
    para(rt("By symmetry, "), eq(r"P(A \cap B) = P(B \mid A) \cdot P(A)"), rt(". Substituting:")),
    equation_block(r"P(A \mid B) = \frac{P(B \mid A) \cdot P(A)}{P(B)}"),
    para(rt("For a discrete hypothesis space "), eq(r"\{H_1, \ldots, H_k\}"), rt(","
            " the law of total probability gives:")),
    equation_block(r"P(B) = \sum_{i=1}^{k} P(B \mid H_i) \cdot P(H_i)"),
    heading3("Numerical Trace: Medical Test"),
    para(rt("Let D = disease, + = positive test. Given:")),
    bullet(eq(r"P(D) = 0.001")),
    bullet(eq(r"P(+ \mid D) = 0.99") , rt("  (sensitivity)")),
    bullet(eq(r"P(+ \mid \neg D) = 0.01"), rt("  (false-positive rate)")),
    para(rt("Step 1 — Compute joint probabilities:")),
    equation_block(r"P(+ \cap D) = 0.99 \times 0.001 = 0.00099"),
    equation_block(r"P(+ \cap \neg D) = 0.01 \times 0.999 = 0.00999"),
    para(rt("Step 2 — Marginal "), eq(r"P(+)"), rt(":")),
    equation_block(r"P(+) = 0.00099 + 0.00999 = 0.01098"),
    para(rt("Step 3 — Posterior:")),
    equation_block(r"P(D \mid +) = \frac{0.00099}{0.01098} \approx 0.0901 = 9.01\%"),
    para(rt("In a population of 100,000: 99 true positives, 999 false positives. "
            "The test positive pool is 1,098 people. Only 99/1,098 ≈ 9% are genuinely sick.")),
    heading3("Continuous Extension: Beta-Binomial"),
    para(rt("For continuous parameters "), eq(r"\theta"), rt(","
            " Bayes generalizes to densities. Classic example: estimating a coin's bias. "
            "With Beta prior "), eq(r"P(\theta) = \mathrm{Beta}(\alpha, \beta)"),
         rt(" and binomial likelihood "), eq(r"P(k \mid \theta, n) = \binom{n}{k} \theta^k (1-\theta)^{n-k}"),
         rt(":")),
    equation_block(r"P(\theta \mid k, n) = \mathrm{Beta}(\alpha + k,\; \beta + n - k)"),
    para(rt("The Beta distribution is the conjugate prior for the binomial — the posterior is "
            "analytically tractable. After observing k heads in n flips, "
            "we simply add counts to the prior hyperparameters.")),
    divider(),

    # ── Section 5: The Math ──────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Spam Filter: Naïve Bayes"),
    para(rt("Naïve Bayes applies Bayes' theorem to classification by assuming conditional independence of features:")),
    equation_block(r"P(C \mid w_1, \ldots, w_n) \propto P(C) \cdot \prod_{i=1}^{n} P(w_i \mid C)"),
    para(rt("For a new email containing 'free' and 'meeting', with priors P(Spam)=0.4, P(Ham)=0.6:")),
    equation_block(r"P(\text{Spam} \mid \text{free, meeting}) \propto 0.4 \times 0.8 \times 0.1 = 0.032"),
    equation_block(r"P(\text{Ham} \mid \text{free, meeting}) \propto 0.6 \times 0.05 \times 0.6 = 0.018"),
    equation_block(r"P(\text{Spam} \mid \text{free, meeting}) = \frac{0.032}{0.032 + 0.018} = 0.64"),
    heading3("Log-Space for Numerical Stability"),
    para(rt("With many words, products underflow to 0. Use log-sum:")),
    equation_block(r"\log P(C \mid \mathbf{w}) = \log P(C) + \sum_{i=1}^{n} \log P(w_i \mid C) - \log P(\mathbf{w})"),
    heading3("Bayesian Sequential Updating"),
    para(rt("Posterior from step t becomes the prior for step t+1:")),
    equation_block(r"P(\theta \mid x_1, \ldots, x_t) \propto P(x_t \mid \theta) \cdot P(\theta \mid x_1, \ldots, x_{t-1})"),
    callout("⚠️", rt("Common Mistake: ", bold=True),
            rt("Confusing P(+|D) with P(D|+). P(+|D) = 0.99 (sensitivity) does NOT mean "
               "P(D|+) = 0.99. These differ by factors of the prior and marginal. "
               "This confusion is called the prosecutor's fallacy in legal contexts.")),
    divider(),

    # ── Section 6: Code ──────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch: Bayesian Inference"),
    code_block("python", """import numpy as np

def bayes_update(prior: float, likelihood_pos: float, likelihood_neg: float) -> float:
    \"\"\"
    Compute posterior P(H | E) given:
      prior          = P(H)       — prior belief in hypothesis
      likelihood_pos = P(E | H)   — probability of evidence if H is true
      likelihood_neg = P(E | ¬H)  — probability of evidence if H is false
    Returns: P(H | E)
    \"\"\"
    p_evidence = likelihood_pos * prior + likelihood_neg * (1 - prior)
    if p_evidence == 0:
        raise ValueError("P(Evidence) = 0; evidence is impossible under all hypotheses")
    return (likelihood_pos * prior) / p_evidence

# Medical test example
prior       = 0.001   # P(Disease): 1 in 1000
sensitivity = 0.99    # P(+|Disease)
fpr         = 0.01    # P(+|No Disease)

posterior = bayes_update(prior, sensitivity, fpr)
print(f"P(Disease | Positive) = {posterior:.4f} = {posterior*100:.2f}%")
# → 0.0901 = 9.01%

# Sequential update: run the test again on the same person
posterior2 = bayes_update(posterior, sensitivity, fpr)
print(f"P(Disease | 2 Positives) = {posterior2:.4f} = {posterior2*100:.2f}%")
# → 0.5058 = 50.58%  — two positive tests cross the 50% threshold!


def naive_bayes_classify(word_probs: dict, prior_spam: float, email_words: list) -> dict:
    \"\"\"
    Naïve Bayes spam classifier.
    word_probs: {word: (P(word|Spam), P(word|Ham))}
    Returns: {'spam': p_spam, 'ham': p_ham}
    \"\"\"
    log_spam = np.log(prior_spam)
    log_ham  = np.log(1 - prior_spam)
    for w in email_words:
        if w in word_probs:
            ps, ph = word_probs[w]
            log_spam += np.log(ps + 1e-10)   # Laplace smoothing
            log_ham  += np.log(ph + 1e-10)
    # Softmax-style normalization in log space
    max_log = max(log_spam, log_ham)
    p_spam = np.exp(log_spam - max_log)
    p_ham  = np.exp(log_ham  - max_log)
    total  = p_spam + p_ham
    return {'spam': p_spam/total, 'ham': p_ham/total}

word_probs = {
    'free':    (0.80, 0.05),
    'meeting': (0.10, 0.60),
}
result = naive_bayes_classify(word_probs, prior_spam=0.4, email_words=['free', 'meeting'])
print(f"Spam: {result['spam']:.3f}, Ham: {result['ham']:.3f}")
# → Spam: 0.640, Ham: 0.360
"""),
    heading3("6b — Production: sklearn Naïve Bayes"),
    code_block("python", """from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

# Text classification pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=50000)),
    ('clf',   MultinomialNB(alpha=1.0)),   # alpha = Laplace smoothing
])

# Fit
pipeline.fit(X_train, y_train)          # X_train: list of strings
probs = pipeline.predict_proba(X_test)  # Returns P(class | text) per sample

# ⚠️ Gotcha: MultinomialNB expects non-negative features (counts/TF-IDF works).
#            BernoulliNB is better for binary features (word present/absent).
#            GaussianNB handles continuous features (assumes Gaussian likelihood).

# Prior class probabilities (check what Naive Bayes learned)
print(pipeline.named_steps['clf'].class_log_prior_)

# Laplace smoothing alpha:
#   alpha=0 → maximum likelihood (can underflow with unseen words)
#   alpha=1 → Laplace (standard choice)
#   alpha>1 → stronger smoothing, more weight to uniform prior
"""),
    divider(),

    # ── Section 7: Interview ──────────────────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): State Bayes' theorem and name its components.", bold=True)], [
        para(rt("A: "), eq(r"P(H \mid E) = \frac{P(E \mid H) \cdot P(H)}{P(E)}")),
        para(rt("Prior P(H): belief before evidence. Likelihood P(E|H): probability of evidence given hypothesis. "
                "Posterior P(H|E): updated belief. Normalizer P(E) = Σ P(E|Hᵢ)P(Hᵢ).")),
    ]),
    toggle([rt("Q2 (Medium): A disease has 0.1% prevalence. A test is 99% sensitive and 99% specific. "
               "What is P(disease | positive)?", bold=True)], [
        equation_block(r"P(D \mid +) = \frac{0.99 \times 0.001}{0.99 \times 0.001 + 0.01 \times 0.999} = \frac{0.00099}{0.01098} \approx 9\%"),
        para(rt("The low prevalence dominates — most positives are false alarms. "
                "This is the base-rate effect and a classic interview trap.")),
    ]),
    toggle([rt("Q3 (Medium): Why does Naïve Bayes work well despite the independence assumption being wrong?", bold=True)], [
        para(rt("Because classification only requires the correct rank order of class probabilities, not calibrated values. "
                "Even with correlations, the MAP class label is usually correct. "
                "Naïve Bayes is a generative model optimizing joint probability, which is a different objective "
                "than minimizing classification error — this often provides better regularization on small data.")),
    ]),
    toggle([rt("Q4 (Hard): What is a conjugate prior? Why does it matter?", bold=True)], [
        para(rt("A prior "), eq(r"P(\theta)"), rt(" is conjugate to a likelihood "), eq(r"P(x|\theta)"),
             rt(" if the posterior "), eq(r"P(\theta|x)"), rt(" belongs to the same family as the prior. "
                "This matters because it gives closed-form posteriors — no MCMC needed.")),
        para(rt("Examples: Beta-Binomial (coin flips), Dirichlet-Multinomial (Naïve Bayes word probs), "
                "Normal-Normal (known variance), Gamma-Poisson (event rates).")),
    ]),
    toggle([rt("Q5 (Hard): Explain to a PhD Researcher: What is the relationship between MAP estimation "
               "and regularized MLE?", bold=True)], [
        para(rt("MAP (Maximum A Posteriori) maximizes "), eq(r"\log P(\theta \mid X) = \log P(X \mid \theta) + \log P(\theta) + \text{const}")),
        para(rt("With a Gaussian prior "), eq(r"P(\theta) \propto \exp(-\lambda \|\theta\|_2^2)"),
             rt(", log prior = "), eq(r"-\lambda \|\theta\|_2^2"), rt(", so MAP = MLE + L2 regularization (Ridge). "
                "With a Laplace prior, MAP = MLE + L1 (Lasso). "
                "Regularization strength = inverse prior variance. This unifies Bayesian and frequentist frameworks.")),
    ]),
    toggle([rt("Q6 (Hard): When does Bayesian inference fail in practice?", bold=True)], [
        bullet(rt("Misspecified prior: garbage prior → garbage posterior. Strong incorrect prior resists updating.")),
        bullet(rt("Model misspecification: likelihood P(E|H) is wrong (e.g., Gaussian on heavy-tailed data).")),
        bullet(rt("Computational intractability: exact posterior requires summing over exponentially many hypotheses. "
                  "Requires MCMC or variational inference.")),
        bullet(rt("Prior elicitation: subjective priors are hard to specify in high dimensions.")),
    ]),
    divider(),

    # ── Section 8: Comparison ────────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(4,
        table_row(["Approach", "Prior", "Output", "Best For"]),
        table_row(["Bayesian (exact)", "Required", "Full posterior P(θ|X)", "Small hypothesis space, diagnostic reasoning"]),
        table_row(["MAP estimation", "Required", "Single point estimate", "Regularized regression, NLP (add priors as regularizers)"]),
        table_row(["MLE (frequentist)", "None", "Point estimate", "Large data, no prior knowledge"]),
        table_row(["Naïve Bayes classifier", "Class prior P(C)", "P(C|features)", "Text classification, spam, fast baseline"]),
        table_row(["MCMC / VI", "Required", "Approximate posterior", "Complex models, continuous parameters"]),
    ),
    callout("🎯", rt("Decision: ", bold=True),
            rt("Use Bayes' theorem (exact) for small discrete problems and diagnostic reasoning. "
               "Use Naïve Bayes for text classification. Use MCMC/VI when the posterior is intractable. "
               "Use MLE/frequentist when you genuinely have no prior and data is plentiful.")),
    divider(),

    # ── Section 9: Explainer Embed ───────────────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the medical-test calculation visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ───────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Probability theory: conditional probability, joint distributions")),
    bullet(rt("Frequentist statistics: p-values, maximum likelihood estimation")),
    heading3("What to Learn Next"),
    bullet(rt("Naïve Bayes Classifier — direct application to text classification")),
    bullet(rt("Bayesian Networks — extends Bayes to structured graphical models")),
    bullet(rt("MCMC / Variational Inference — computing intractable posteriors")),
    bullet(rt("Gaussian Processes — Bayesian non-parametric regression")),
    heading3("Key Papers"),
    bullet(rt("Bayes, T. (1763). 'An Essay towards solving a Problem in the Doctrine of Chances.' "
              "Philosophical Transactions of the Royal Society. — The original theorem.")),
    bullet(rt("Zhang, H. (2004). 'The Optimality of Naïve Bayes.' FLAIRS 2004. "
              "— Why Naïve Bayes works despite independence violations.")),
    bullet(rt("Efron, B. (2012). 'Bayesian Inference and the Parametric Bootstrap.' — Modern view of Bayesian vs frequentist.")),
    heading3("Best Resources"),
    bullet(rt("'Bayesian Reasoning and Machine Learning' — Barber (free PDF): comprehensive treatment")),
    bullet(rt("'Pattern Recognition and Machine Learning' Ch. 1-2 — Bishop: classic probabilistic ML")),
    bullet(rt("3Blue1Brown: 'Bayes theorem' and 'The medical test paradox' on YouTube — best visual intuition")),
    callout("🔗", rt("This topic connects to: ", bold=True),
            rt("Maximum Likelihood Estimation, Prior & Posterior Distributions, "
               "Naïve Bayes Classifier, Bayesian Networks, Gaussian Processes, MCMC")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
