#!/usr/bin/env python3
"""Update Notion page for: Bayesian Updating & Sequential Analysis"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8145-bdbc-e8d25483befc"
ICON = "🟡"   # Intermediate
PROPERTIES = {
    "Status":            {"select": {"name": "Completed"}},
    "Depth":             {"select": {"name": "Intermediate"}},
    "Interview Priority":{"select": {"name": "Must Know"}},
    "Has Explainer":     {"checkbox": True},
    "Explainer URL":     {"url": "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/bayesian_updating_sequential_explainer.html"},
}

blocks = [

    # Section 1: 30-Second Version
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("Bayesian updating is the mathematically correct way to change your beliefs when new evidence arrives. You start with a "), rt("prior", bold=True), rt(" (what you believe before data), observe something, and produce a "), rt("posterior", bold=True), rt(" (your updated belief). The key insight: today's posterior is tomorrow's prior. Do this for each new observation and you have sequential Bayesian inference.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine you're estimating whether a coin is fair. Before any flips, you're uncertain. After 5 heads in a row, you update toward 'biased coin.' After a tails, you adjust back down slightly. Each flip resharpens your belief. Sequential analysis adds: 'Stop flipping once I'm confident enough.'")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Bayes' rule applied repeatedly: posterior ← likelihood × prior / evidence. Because today's posterior becomes tomorrow's prior, the final posterior is the same regardless of order ("), rt("order-invariance", italic=True), rt("). For Beta-Binomial: seeing k heads in n flips gives Beta("), eq(r"\alpha_0+k"), rt(", "), eq(r"\beta_0+n-k"), rt(") regardless of order.")),
    divider(),

    # Section 2: Historical Context
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Classical frequentist statistics required fixing the sample size "), eq(r"n"), rt(" before collecting any data. This was wasteful: if a drug effect was enormous, you still had to wait for all 1000 patients. And peeking at data mid-experiment inflated Type I error rates catastrophically.")),
    heading3("What Came Before"),
    para(rt("The Neyman-Pearson framework (1933) formalized hypothesis testing with fixed "), eq(r"n"), rt(". Bayesian ideas existed since Bayes (1763) and Laplace (1774-1812) but were largely dormant for a century.")),
    heading3("The Breakthrough"),
    para(rt("Two parallel revolutions: (1) Abraham Wald's SPRT (1945) — derived during WWII for munitions quality control, proved sequential testing minimizes expected sample size. (2) Revival of Bayesian inference (1950s-1970s) through de Finetti, Savage, and eventually MCMC (1990s) making Bayesian methods computationally practical.")),
    heading3("Key Papers"),
    bullet(rt("Bayes, T. (1763). An Essay Towards Solving a Problem in the Doctrine of Chances. Phil. Trans. Royal Society.")),
    bullet(rt("Wald, A. (1945). Sequential Tests of Statistical Hypotheses. Ann. Math. Stat. Proved SPRT minimizes E[N].")),
    bullet(rt("Wald, A. & Wolfowitz, J. (1948). Optimum Character of the Sequential Probability Ratio Test. Ann. Math. Stat.")),
    heading3("Before vs. After Comparison"),
    table(3,
        table_row(["Dimension", "Fixed-Sample Testing", "Sequential / Bayesian"]),
        table_row(["Sample size", "Fixed in advance", "Stops as soon as sufficient evidence"]),
        table_row(["Mid-experiment peek", "Inflates Type I error", "Valid at every stopping time (SPRT)"]),
        table_row(["Output", "p-value + binary decision", "Full posterior distribution"]),
        table_row(["Prior knowledge", "Ignored", "Encoded explicitly"]),
        table_row(["Efficiency", "Fixed n (often over-samples)", "~50-70% fewer samples typically"]),
    ),
    divider(),

    # Section 3: Core Concepts
    heading2("🔑 Core Concepts & Theory"),
    heading3("Bayes' Rule"),
    equation_block(r"P(\theta \mid x) = \frac{P(x \mid \theta)\, P(\theta)}{P(x)} \propto \underbrace{P(x \mid \theta)}_{\text{likelihood}} \cdot \underbrace{P(\theta)}_{\text{prior}}"),
    heading3("Key Definitions"),
    bullet(rt("Prior "), eq(r"P(\theta)"), rt(": Belief about parameter before observing data")),
    bullet(rt("Likelihood "), eq(r"P(x \mid \theta)"), rt(": Probability of observed data given parameter (NOT a distribution over "), eq(r"\theta"), rt(")")),
    bullet(rt("Posterior "), eq(r"P(\theta \mid x)"), rt(": Updated belief after observing data")),
    bullet(rt("Conjugate prior: prior whose functional form is preserved under Bayesian update")),
    heading3("Beta-Binomial Conjugacy"),
    para(rt("Prior: "), eq(r"p \sim \text{Beta}(\alpha, \beta)"), rt(". After observing "), eq(r"k"), rt(" heads in "), eq(r"n"), rt(" flips:")),
    equation_block(r"p \mid X_{1:n} \sim \text{Beta}(\alpha + k,\; \beta + n - k)"),
    para(rt("Update rule: "), rt("heads add 1 to alpha; tails add 1 to beta", bold=True), rt(". Distribution moments:")),
    equation_block(r"\text{Mean} = \frac{\alpha}{\alpha+\beta}, \quad \text{Mode} = \frac{\alpha-1}{\alpha+\beta-2}, \quad \text{Var} = \frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}"),
    heading3("SPRT Boundaries (Wald)"),
    equation_block(r"\log A = \log\frac{1-\beta}{\alpha} \quad\text{(upper: accept }H_1), \qquad \log B = \log\frac{\beta}{1-\alpha} \quad\text{(lower: accept }H_0)"),
    callout("🔑", rt("Order Invariance: ", bold=True), rt("Beta("), eq(r"\alpha_0+k"), rt(", "), eq(r"\beta_0+n-k"), rt(") depends only on "), eq(r"k"), rt(" and "), eq(r"n"), rt(", not on order. This is because the count "), eq(r"(k,n)"), rt(" is a sufficient statistic for the Bernoulli likelihood — it captures all information about "), eq(r"p"), rt(" in the data.")),
    divider(),

    # Section 4: Architecture / Deep Dive
    heading2("🔬 Architecture & Internal Workings"),
    heading3("Numerical Trace: 14 Flips, true p=0.7, prior Beta(1,1)"),
    table(5,
        table_row(["Step", "Flip", "Posterior Beta(α,β)", "Mean", "Variance"]),
        table_row(["0 (prior)", "—",   "Beta(1,1)",   "0.500", "0.0833"]),
        table_row(["1",        "H",   "Beta(2,1)",   "0.667", "0.0556"]),
        table_row(["2",        "H",   "Beta(3,1)",   "0.750", "0.0375"]),
        table_row(["3",        "T",   "Beta(3,2)",   "0.600", "0.0400"]),
        table_row(["5",        "H",   "Beta(5,2)",   "0.714", "0.0255"]),
        table_row(["10",       "H",   "Beta(10,2)",  "0.833", "0.0112"]),
        table_row(["12",       "T",   "Beta(11,3)",  "0.786", "0.0099"]),
        table_row(["14",       "H",   "Beta(13,3)",  "0.812", "0.0081"]),
    ),
    heading3("SPRT Trace for Same Sequence"),
    para(rt("Per-flip log-LR increments: head = "), eq(r"\log(0.7/0.5) \approx +0.336"), rt(", tail = "), eq(r"\log(0.3/0.5) \approx -0.511")),
    table(4,
        table_row(["Obs", "Flip", "Cumulative log-LR", "Status"]),
        table_row(["1",  "H", "0.336",  "continue"]),
        table_row(["2",  "H", "0.673",  "continue"]),
        table_row(["3",  "T", "0.162",  "continue"]),
        table_row(["11", "H", "2.854",  "continue (just below 2.944)"]),
        table_row(["12", "T", "2.343",  "continue (drops back)"]),
        table_row(["14", "H", "3.016",  "ACCEPT H1 (>= log A = 2.944)"]),
    ),
    heading3("Expected Sample Size (SPRT vs. Fixed)"),
    equation_block(r"\mathbb{E}_1[N] \approx \frac{(1-\beta)\log A + \beta \log B}{p_1\log\frac{p_1}{p_0} + (1-p_1)\log\frac{1-p_1}{1-p_0}} = \frac{0.8(2.944) + 0.2(-1.558)}{0.7(0.336) + 0.3(-0.511)} \approx 14.3"),
    para(rt("Fixed-sample test for same "), eq(r"(\alpha=0.05,\beta=0.20,p_0=0.5,p_1=0.7)"), rt(" requires "), eq(r"n \approx 50"), rt(" — 3.5x more observations than the SPRT.")),
    heading3("Design Decision: Conjugate vs. MCMC"),
    para(rt("Conjugate priors give exact, O(1) sequential updates. The trade-off: conjugacy only exists for exponential family likelihoods. For logistic regression, neural networks, or non-standard likelihoods, use MCMC (exact but expensive) or variational inference (fast but approximate).")),
    divider(),

    # Section 5: The Math
    heading2("📐 The Math Behind It"),
    heading3("Derivation of Beta-Binomial Update"),
    para(rt("Prior: "), eq(r"P(p) \propto p^{\alpha-1}(1-p)^{\beta-1}")),
    para(rt("Bernoulli likelihood for one observation "), eq(r"x \in \{0,1\}"), rt(":")),
    equation_block(r"P(x \mid p) = p^x (1-p)^{1-x}"),
    para(rt("Posterior (unnormalized):")),
    equation_block(r"P(p \mid x) \propto p^{(\alpha+x)-1}(1-p)^{(\beta+1-x)-1} \equiv \text{Beta}(\alpha+x,\; \beta+1-x)"),
    para(rt("After "), eq(r"n"), rt(" i.i.d. observations with "), eq(r"k = \sum x_i"), rt(" heads — because the exponents simply accumulate:")),
    equation_block(r"P(p \mid x_{1:n}) = \text{Beta}(\alpha_0+k,\; \beta_0+n-k)"),
    heading3("Normalizing Constant"),
    equation_block(r"P(x_{1:n}) = \binom{n}{k} \frac{B(\alpha_0+k,\;\beta_0+n-k)}{B(\alpha_0,\;\beta_0)}, \quad B(\alpha,\beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}"),
    heading3("SPRT Error Guarantees (Wald's Inequalities)"),
    equation_block(r"P_{H_0}(\text{accept }H_1) \leq \frac{B}{1-B} \leq \alpha"),
    equation_block(r"P_{H_1}(\text{accept }H_0) \leq \frac{1-A}{A} \cdot \frac{1}{1} \leq \beta"),
    para(rt("These are "), rt("exact", bold=True), rt(" inequalities valid for any stopping time — not asymptotic approximations.")),
    heading3("Why SPRT Is Optimal — Sketch"),
    para(rt("The SPRT log-LR "), eq(r"\Lambda_n"), rt(" is a martingale under "), eq(r"H_0"), rt(" (since "), eq(r"\mathbb{E}_0[e^{\Lambda_n}] = 1"), rt(" — it is an exponential martingale). By the optional stopping theorem, "), eq(r"\mathbb{E}_0[\Lambda_{N}] \approx \log B \cdot P_0(\text{accept }H_0) + \log A \cdot P_0(\text{accept }H_1)"), rt(". This pins down the expected sample size uniquely, and no other test can achieve smaller "), eq(r"\mathbb{E}[N]"), rt(" under both hypotheses simultaneously.")),
    callout("⚠️", rt("Warning: SPRT Requires No Adaptive Boundaries: ", bold=True), rt("The error guarantees hold only if boundaries are fixed before data collection. Adapting boundaries mid-experiment (even 'conservatively') destroys the guarantee. For adaptive stopping, use e-values (Johari et al. 2022) which are valid under optional stopping by construction.")),
    divider(),

    # Section 6: Code
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (Pure Python/NumPy)"),
    code_block("python", "import numpy as np\nfrom scipy.stats import beta as beta_dist\n\ndef bayesian_coin_update(flips, alpha0=1, beta0=1):\n    \"\"\"\n    Sequential Bayesian updating for coin bias estimation.\n    O(1) per step due to Beta-Binomial conjugacy.\n    \"\"\"\n    alpha, beta = alpha0, beta0\n    history = [(alpha, beta, alpha/(alpha+beta))]\n\n    for x in flips:\n        alpha += x          # head: increment alpha\n        beta  += (1 - x)   # tail: increment beta\n        mean  = alpha / (alpha + beta)\n        history.append((alpha, beta, mean))\n\n    return history\n\n# 14 flips with true p=0.7\nflips = [1,1,0,1,1,1,1,1,1,1,1,0,1,1]\nhist  = bayesian_coin_update(flips)\n\nfor i, (a, b, m) in enumerate(hist):\n    flip_info = f'flip={flips[i-1]}' if i > 0 else 'prior'\n    print(f'Step {i:2d} ({flip_info}): Beta({a},{b})  mean={m:.4f}')\n\n# 95% credible interval at final step\nalpha_n, beta_n = hist[-1][0], hist[-1][1]\nci_lo = beta_dist.ppf(0.025, alpha_n, beta_n)\nci_hi = beta_dist.ppf(0.975, alpha_n, beta_n)\nprint(f'95% CI: [{ci_lo:.3f}, {ci_hi:.3f}]')"),
    heading3("6b — SPRT from Scratch"),
    code_block("python", "def sprt(observations, p0, p1, alpha=0.05, beta=0.20):\n    \"\"\"\n    Wald Sequential Probability Ratio Test for Bernoulli trials.\n    Guaranteed: P(Type I error) <= alpha, P(Type II error) <= beta.\n    \"\"\"\n    log_A = np.log((1 - beta) / alpha)   # upper: accept H1\n    log_B = np.log(beta / (1 - alpha))   # lower: accept H0\n\n    log_lr_head = np.log(p1 / p0)\n    log_lr_tail = np.log((1 - p1) / (1 - p0))\n\n    log_lr = 0.0\n    for n, x in enumerate(observations, 1):\n        log_lr += log_lr_head if x == 1 else log_lr_tail\n        if log_lr >= log_A:\n            return 'H1', n\n        elif log_lr <= log_B:\n            return 'H0', n\n    return 'inconclusive', n\n\nflips = [1,1,0,1,1,1,1,1,1,1,1,0,1,1]\ndecision, n = sprt(flips, p0=0.5, p1=0.7)\nprint(f'Decision: {decision} after {n} observations')  # H1 after 14\n\n# Estimate expected sample size via simulation\nimport numpy as np\nnp.random.seed(0)\nns = [sprt(np.random.binomial(1, 0.7, 100), 0.5, 0.7)[1] for _ in range(10000)]\nprint(f'Mean sample size under H1: {np.mean(ns):.1f}')  # ~ 14.3"),
    heading3("6c — Production (scipy + PyMC)"),
    code_block("python", "# For complex likelihoods: PyMC with online approximation\nimport pymc as pm\nimport numpy as np\n\nwith pm.Model() as coin_model:\n    p = pm.Beta('p', alpha=1, beta=1)            # prior\n    obs = pm.Bernoulli('obs', p=p, observed=[1,1,0,1,1,1,1,1,1,1,1,0,1,1])\n    idata = pm.sample(1000, tune=500, chains=2, progressbar=False)\n\nprint(pm.summary(idata, var_names=['p']))\n# For Beta-Binomial, this is overkill — use analytic update!\n# PyMC is needed for: logistic models, hierarchical priors, custom likelihoods\n\n# GOTCHA: always check model.check_test_point() before sampling"),
    divider(),

    # Section 7: Interview
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What is prior, likelihood, and posterior?", bold=True)], [
        para(rt("Prior "), eq(r"P(\theta)"), rt(": belief before data. Likelihood "), eq(r"P(x|\theta)"), rt(": probability of observed data given parameter (NOT a dist. over "), eq(r"\theta"), rt("). Posterior "), eq(r"P(\theta|x) \propto P(x|\theta)P(\theta)"), rt(": updated belief.")),
        callout("⚠️", rt("Follow-up trap: 'Is the likelihood a probability distribution over theta?' ", bold=True), rt("No! It does NOT integrate to 1 over "), eq(r"\theta")),
    ]),
    toggle([rt("Q2 (Easy): Why is Beta conjugate to Bernoulli?", bold=True)], [
        para(rt("Both have form "), eq(r"p^a (1-p)^b"), rt(". Their product stays in the Beta family — new parameters just add the exponents. No integration needed.")),
    ]),
    toggle([rt("Q3 (Medium): How does Bayesian mean differ from MLE?", bold=True)], [
        para(rt("MLE: "), eq(r"\hat{p}_{MLE} = k/n"), rt(". Bayesian mean: "), eq(r"\hat{p}_{Bayes} = (\alpha_0+k)/(\alpha_0+\beta_0+n)"), rt(". Bayesian shrinks toward prior mean. As "), eq(r"n \to \infty"), rt(", both converge. MLE can be 0 or 1 with extreme data; Bayes stays in interior.")),
    ]),
    toggle([rt("Q4 (Medium): What is SPRT and why is it optimal?", bold=True)], [
        para(rt("Accumulates "), eq(r"\Lambda_n = \sum \log(P(x_i|H_1)/P(x_i|H_0))"), rt(", stops when it crosses Wald boundaries. Optimal: Wald-Wolfowitz proved no other sequential test with same "), eq(r"(\alpha,\beta)"), rt(" bounds has smaller expected sample size under both "), eq(r"H_0"), rt(" and "), eq(r"H_1"), rt(".")),
    ]),
    toggle([rt("Q5 (Hard): Why can't you use classical p-values for sequential testing?", bold=True)], [
        para(rt("Fixed-n p-values assume n chosen before peeking. Sequential peeking with stop-when-p<0.05 inflates Type I error to ~30% because you run many correlated tests. The SPRT avoids this by calibrating boundaries to maintain guaranteed error rates at any stopping time.")),
        callout("⚠️", rt("Red flag: ", bold=True), rt("'I just use a stricter threshold like p<0.001.' That corrects for independent multiple tests, not sequential data-peeking.")),
    ]),
    toggle([rt("Q6 (Hard): Explain e-values to a PhD Researcher.", bold=True)], [
        para(rt("An e-value "), eq(r"E"), rt(" satisfies "), eq(r"\mathbb{E}_{H_0}[E] \leq 1"), rt(". By Markov: "), eq(r"P_{H_0}(E \geq 1/\alpha) \leq \alpha"), rt(" at any stopping time. The SPRT likelihood ratio (not log) is an e-process. E-values compose multiplicatively. This enables always-valid inference: peek continuously, stop anytime, adjust for covariates — no correction needed.")),
    ]),
    toggle([rt("Q7 (Hard): When does conjugacy break down and what do you do?", bold=True)], [
        para(rt("Conjugacy only exists for exponential family likelihoods. For logistic regression, neural networks: (1) MCMC (exact asymptotically, expensive), (2) Variational inference (fast, biased), (3) Laplace approximation (Gaussian at MAP, fast but local), (4) Assumed Density Filtering for sequential streaming data.")),
    ]),
    divider(),

    # Section 8: Comparison
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Method", "Output", "Stopping Rule", "Prior Required", "Complexity"]),
        table_row(["Fixed-sample frequentist", "p-value", "Pre-specified n", "No", "O(n)"]),
        table_row(["Bayesian updating (conjugate)", "Full posterior", "Any (posterior-based)", "Yes", "O(1)/step"]),
        table_row(["SPRT", "H0 or H1", "Optimal Wald boundaries", "No", "O(1)/step"]),
        table_row(["Bayes Factor", "BF ratio", "When BF > threshold", "Yes", "Varies"]),
        table_row(["E-values", "e-value", "Any time", "No", "O(1)/step"]),
        table_row(["Thompson Sampling", "Action", "Online (no fixed end)", "Yes (bandit)", "O(1)/step"]),
    ),
    callout("🎯", rt("Decision framework: ", bold=True), rt("Full uncertainty at every step? → Bayesian updating. Two specific point hypotheses, optimal stopping? → SPRT. Maximum flexibility, continuous monitoring? → E-values. Have prior knowledge to encode? → Bayesian. Prior controversial? → Frequentist with correction.")),
    divider(),

    # Section 9: Explainer Embed
    heading2("🎯 Interactive Visual Explainer"),
    embed("https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/bayesian_updating_sequential_explainer.html"),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys. Watch the Beta posterior sharpen as coin flips arrive and track the SPRT log-likelihood ratio racing toward its acceptance boundary.", italic=True, color="gray")),
    divider(),

    # Section 10: Related Topics
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Probability Axioms & Kolmogorov (3.1)")),
    bullet(rt("Conditional Probability & Bayes (3.3)")),
    bullet(rt("Prior, Likelihood, Posterior, Evidence (3.8)")),
    bullet(rt("Beta/Gamma Distributions (continuous distributions section)")),
    bullet(rt("Hypothesis Testing & p-values (3.7)")),
    heading3("What to Learn Next"),
    bullet(rt("Conjugate Priors Catalog (3.9)")),
    bullet(rt("Bayesian Model Comparison / Bayes Factors (3.11)")),
    bullet(rt("MCMC & Variational Inference — for non-conjugate posteriors")),
    bullet(rt("Thompson Sampling & Bayesian Bandits")),
    bullet(rt("Empirical Bayes — estimating hyperparameters from data")),
    heading3("Key Papers"),
    bullet(rt("Wald, A. (1945). Sequential Tests of Statistical Hypotheses. Ann. Math. Stat.")),
    bullet(rt("Wald, A. & Wolfowitz, J. (1948). Optimum Character of the SPRT. Ann. Math. Stat.")),
    bullet(rt("Johari, R. et al. (2022). Always Valid Inference. Management Science. — E-values for continuous monitoring.")),
    bullet(rt("Shafer, G. & Vovk, V. (2019). Game-Theoretic Foundations for Probability and Finance.")),
    heading3("Best Resources"),
    bullet(rt("Gelman et al., Bayesian Data Analysis (3rd ed.) — Ch. 2-3 for conjugate models")),
    bullet(rt("Wald, A. (1947). Sequential Analysis (book) — Original comprehensive treatment")),
    bullet(rt("Evan Miller's blog: 'How Not to Run an A/B Test' — Classic article on sequential testing pitfalls")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Conjugate Priors Catalog, MAP Estimation, Bayesian Model Comparison, Credible vs. Confidence Intervals, Thompson Sampling, Hidden Markov Models (forward algorithm = sequential Bayesian update for hidden states)")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
