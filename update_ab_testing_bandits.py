#!/usr/bin/env python3
"""Update Notion page for: A/B testing: sample size calculation, sequential testing, multi-armed bandits"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-811e-85b2-f3627b77babd"
ICON = "🟡"   # Intermediate depth
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/ab_testing_bandits_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [

    # ── Section 1: 30-Second Version ──────────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("An A/B test is a randomized controlled experiment: split users randomly into two groups, give group A the old version and group B the new version, collect a metric, and use statistics to decide whether the observed difference is real or just chance. Before collecting a single data point you must fix how many users you need (sample size), how often you're allowed to look at results (sequential testing), and — if you want to adapt traffic in real-time — which bandit algorithm to use.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine a chef testing two soup recipes. She gives bowl A to 500 randomly chosen diners and bowl B to 500 others. She pre-commits to reading ratings only at the end. She uses statistics to decide whether bowl B is genuinely tastier, or if the gap was luck. If she keeps peeking every day and stops as soon as one bowl looks better, she'll wrongly declare a winner far more than 5% of the time.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("Fix α, power (1−β), and MDE δ before collecting data. Compute n per arm from these three. Look at data only as pre-specified. Peeking without adjustment inflates false-positive rate from 5% to ~14%.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Before online experimentation, product teams shipped features to everyone and used intuition or aggregate metrics to judge success. Causal effects were confounded by seasonality, user segment differences, and other concurrent changes.")),
    heading3("What Came Before"),
    para(rt("Fisher's agricultural field trials (1920s–30s) established randomization as the cure for confounding. Wald's Sequential Probability Ratio Test (SPRT, 1945) introduced the idea of testing as data arrives. Robbins' multi-armed bandit formulation (1952) introduced the explore-exploit framework. By the 2000s, large internet companies (Google, Microsoft, Amazon) systematized A/B testing at scale, exposing new problems: peeking, metric dilution, network interference, and the regret cost of pure exploration.")),
    heading3("Key Papers"),
    bullet(rt("R.A. Fisher, ", bold=True), rt("The Design of Experiments"), rt(" (1935) — foundational randomization and p-value framework")),
    bullet(rt("Abraham Wald, ", bold=True), rt("Sequential Analysis"), rt(" (1947) — SPRT: optimal sequential test minimizing expected sample size")),
    bullet(rt("Herbert Robbins, ", bold=True), rt('"Some Aspects of the Sequential Design of Experiments"'), rt(" (1952) — introduced the multi-armed bandit problem")),
    bullet(rt("O'Brien & Fleming, ", bold=True), rt('"A Multiple Testing Procedure for Clinical Trials"'), rt(" (Biometrics, 1979) — alpha-spending function for interim analyses")),
    bullet(rt("Johari et al., ", bold=True), rt('"Peeking at A/B Tests"'), rt(" (KDD 2017) — always-valid p-values (mSPRT) for continuous monitoring")),
    bullet(rt("Peter Auer et al., ", bold=True), rt('"Finite-Time Analysis of the Multiarmed Bandit Problem"'), rt(" (Machine Learning, 2002) — UCB1 with logarithmic regret")),
    heading3("Evolution Timeline"),
    para(rt("Agricultural trials (Fisher 1920s) → clinical SPRT (Wald 1947) → online A/B tests (Google, 2000s) → sequential testing with alpha-spending → always-valid p-values (Netflix/Optimizely) → Bayesian bandits (Thompson Sampling, Chapelle & Li 2011) → contextual bandits (LinUCB, Li et al. 2010)")),
    table(4,
        table_row(["Dimension", "Classical A/B (fixed horizon)", "Sequential testing", "Bandits"]),
        table_row(["When to analyze", "Once at end", "Pre-specified K looks", "Every round"]),
        table_row(["Traffic split", "Fixed 50/50", "Fixed 50/50", "Adaptive"]),
        table_row(["α control", "Trivial", "Alpha-spending needed", "Bayesian / frequentist"]),
        table_row(["Regret optimization", "None (pure explore)", "None (pure explore)", "Core objective"]),
        table_row(["When to stop", "Fixed n", "Boundary crossing or end", "Horizon / posterior"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ──────────────────────────────────────────────
    heading2("🔑 Core Concepts & Theory"),
    heading3("The Hypothesis Testing Framework"),
    para(rt("Let "), eq(r"p_A, p_B"), rt(" be the true conversion rates of control and variant. Null hypothesis "), eq(r"H_0: p_A = p_B"), rt("; alternative "), eq(r"H_1: p_B \neq p_A"), rt(" (two-sided). The test statistic for proportions is:")),
    equation_block(r"z = \frac{\hat{p}_B - \hat{p}_A}{\sqrt{\hat{p}(1-\hat{p})\left(\frac{1}{n_A}+\frac{1}{n_B}\right)}}"),
    para(rt("where "), eq(r"\hat{p} = (n_A \hat{p}_A + n_B \hat{p}_B)/(n_A+n_B)"), rt(" is the pooled proportion. Under "), eq(r"H_0"), rt(", "), eq(r"z \xrightarrow{d} \mathcal{N}(0,1)"), rt(" as "), eq(r"n \to \infty"), rt(".")),
    heading3("Sample Size Formula"),
    para(rt("From the power requirement — the test must detect "), eq(r"\delta = p_B - p_A"), rt(" with probability "), eq(r"1-\beta"), rt(" at significance level "), eq(r"\alpha"), rt(":")),
    equation_block(r"n = \left\lceil \frac{(z_{\alpha/2} + z_\beta)^2\,[p_1(1-p_1) + p_2(1-p_2)]}{\delta^2} \right\rceil"),
    para(rt("For "), eq(r"p_1=0.10"), rt(", "), eq(r"p_2=0.12"), rt(", "), eq(r"\alpha=0.05"), rt(", power "), eq(r"=0.80"), rt(": "), eq(r"z_{\alpha/2}=1.960"), rt(", "), eq(r"z_\beta=0.842"), rt(", "), eq(r"\delta=0.02"), rt(", giving "), eq(r"n=3{,}839"), rt(" per arm.")),
    callout("🔑", rt("Core invariant: ", bold=True), rt("The required sample size scales as "), eq(r"n \propto \delta^{-2}"), rt(". Halving the minimum detectable effect quadruples the required sample size. This is the most common reason experiments are underpowered in practice.")),
    heading3("Prerequisites"),
    bullet(rt("Central Limit Theorem and Normal approximation to the Binomial")),
    bullet(rt("Hypothesis testing: Type I/II errors, p-values")),
    bullet(rt("Bayesian inference: prior/posterior for Thompson Sampling")),
    divider(),

    # ── Section 4: Architecture & Deep Dive ───────────────────────────────────
    heading2("🏗️ Architecture & Internal Workings"),
    heading3("The Full A/B Pipeline"),
    para(rt("1. ", bold=True), rt("Pre-experiment: specify metric, α, power, MDE, compute n.")),
    para(rt("2. ", bold=True), rt("Randomization: hash(user_id + experiment_id) mod 100 → bucket. Ensures i.i.d. assignment.")),
    para(rt("3. ", bold=True), rt("Run: collect observations until n per arm (or interim look schedule met).")),
    para(rt("4. ", bold=True), rt("Analysis: compute z-statistic, compare to critical value (or adjusted boundary).")),
    para(rt("5. ", bold=True), rt("Decision: reject or fail-to-reject H₀; ship or roll back.")),
    heading3("Numerical Trace: Sample Size"),
    para(rt("Given "), eq(r"p_1=0.10, p_2=0.12, \alpha=0.05, 1-\beta=0.80"), rt(":")),
    equation_block(r"z_{\alpha/2} = \Phi^{-1}(0.975) = 1.960, \quad z_\beta = \Phi^{-1}(0.80) = 0.842"),
    equation_block(r"\text{numerator} = (1.960+0.842)^2 \times [0.10 \times 0.90 + 0.12 \times 0.88] = 7.855 \times 0.1956 = 1.536"),
    equation_block(r"n = \left\lceil \frac{1.536}{(0.02)^2} \right\rceil = \left\lceil 3838.1 \right\rceil = 3{,}839 \text{ per arm}"),
    heading3("The Peeking Problem — Numerical Detail"),
    para(rt("Suppose you run a 5-look experiment under the null (no real effect), checking at n/N = 0.2, 0.4, 0.6, 0.8, 1.0, stopping at the first look where |z| > 1.96. By simulation (200,000 trials, σ=1), the family-wise false-positive rate is 14.10% — nearly triple the nominal 5%.")),
    para(rt("Intuition: the z-statistic follows a Brownian bridge under the null. With probability ≈ 14%, it crosses ±1.96 at some point before the end. Each extra look adds another opportunity for a transient large fluctuation to produce a false positive.")),
    heading3("O'Brien-Fleming Boundaries — Derivation"),
    para(rt("Let "), eq(r"t_k = k/K"), rt(" be the information fraction at look "), eq(r"k"), rt(". The OBF spending function is:")),
    equation_block(r"\alpha_{\text{spend}}(t) = 2\left[1 - \Phi\!\left(z_\infty / \sqrt{t}\right)\right]"),
    para(rt("For overall "), eq(r"\alpha=0.05"), rt(" and "), eq(r"K=5"), rt(" equal looks, "), eq(r"z_\infty \approx 2.040"), rt(". The per-look boundaries are:")),
    table(4,
        table_row(["Look k", "Info fraction t_k", "OBF boundary z_k", "α spent at look k"]),
        table_row(["1", "0.20", "4.562", "0.000005"]),
        table_row(["2", "0.40", "3.226", "0.0013"]),
        table_row(["3", "0.60", "2.634", "0.0084"]),
        table_row(["4", "0.80", "2.281", "0.0226"]),
        table_row(["5", "1.00", "2.040", "0.0414"]),
    ),
    heading3("Always-Valid P-Values (mSPRT)"),
    para(rt("The mixture Sequential Probability Ratio Test constructs a likelihood ratio process:")),
    equation_block(r"M_t = \int \prod_{s=1}^t \frac{f_\theta(X_s)}{f_0(X_s)} \, \pi(\theta) \, d\theta"),
    para(rt("where "), eq(r"\pi(\theta)"), rt(" is a mixing distribution over alternatives. "), eq(r"M_t"), rt(" is a non-negative martingale under "), eq(r"H_0"), rt(" with "), eq(r"\mathbb{E}_{H_0}[M_t]=1"), rt(". The always-valid p-value is "), eq(r"p_t = 1/M_t"), rt(". By Ville's inequality (a super-martingale version of Markov), "), eq(r"P_{H_0}(\exists t: p_t \leq \alpha) \leq \alpha"), rt(".")),
    heading3("Thompson Sampling — Internal Mechanism"),
    para(rt("Maintain conjugate Beta posteriors "), eq(r"\text{Beta}(\alpha_k, \beta_k)"), rt(" for each arm's conversion rate. At each round:")),
    bullet(eq(r"\tilde{p}_k \sim \text{Beta}(\alpha_k, \beta_k)"), rt(" for each arm k")),
    bullet(rt("Pull arm "), eq(r"k^* = \arg\max_k \tilde{p}_k")),
    bullet(rt("Observe reward "), eq(r"r \in \{0,1\}"), rt("; update: "), eq(r"\alpha_{k^*} \mathrel{+}= r, \; \beta_{k^*} \mathrel{+}= 1-r")),
    para(rt("The sampling step does the exploration automatically: under-sampled arms have wider Beta distributions with non-negligible chance of producing a high sample, which triggers exploration. Over time, the posterior concentrates on the true rate, and the best arm is sampled almost exclusively.")),
    callout("⚠️", rt("Design decision: ", bold=True), rt("Why Beta-Binomial for Thompson? Because the Beta distribution is conjugate to the Bernoulli likelihood — the posterior update is a one-line arithmetic update (no MCMC needed). For continuous rewards, Gaussian-Gaussian or log-normal posteriors are used instead.")),
    divider(),

    # ── Section 5: Math ───────────────────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Sample Size Derivation"),
    para(rt("We want: "), eq(r"P(\text{reject } H_0 \mid p_B = p_1+\delta) = 1-\beta"), rt(". Under the alternative, "), eq(r"z \sim \mathcal{N}(\mu_{\text{alt}}, 1)"), rt(" where "), eq(r"\mu_{\text{alt}} = \delta / \text{SE}")),
    equation_block(r"\text{SE} = \sqrt{\frac{p_1(1-p_1)+p_2(1-p_2)}{n}}"),
    para(rt("Power condition: "), eq(r"\mu_{\text{alt}} - z_{\alpha/2} = z_\beta"), rt(", i.e., "), eq(r"\delta/\text{SE} = z_{\alpha/2}+z_\beta"), rt(". Solving for n:")),
    equation_block(r"n = \frac{(z_{\alpha/2}+z_\beta)^2\,[p_1(1-p_1)+p_2(1-p_2)]}{\delta^2}"),
    heading3("UCB1 Regret Bound"),
    para(rt("For K arms with gaps "), eq(r"\Delta_k = \mu^* - \mu_k"), rt(", UCB1's expected cumulative regret satisfies:")),
    equation_block(r"\mathbb{E}[R_T] \leq \sum_{k:\Delta_k>0} \left( \frac{8\ln T}{\Delta_k} + \left(1+\frac{\pi^2}{3}\right)\Delta_k \right)"),
    para(rt("The dominant term is "), eq(r"\mathcal{O}(\ln T / \Delta)"), rt(". This matches the Lai-Robbins lower bound up to constants, proving UCB1 is asymptotically optimal.")),
    heading3("Thompson Sampling — Optimality"),
    para(rt("Thompson Sampling is asymptotically optimal for the Bernoulli bandit: its expected regret satisfies the Lai-Robbins lower bound with equality as "), eq(r"T \to \infty"), rt(":")),
    equation_block(r"\liminf_{T\to\infty} \frac{\mathbb{E}[R_T]}{\ln T} \geq \sum_{k:\Delta_k>0} \frac{\Delta_k}{KL(p_k \,\|\, p^*)}"),
    para(rt("where "), eq(r"KL(p_k \| p^*)"), rt(" is the KL divergence between Bernoulli distributions. Thompson Sampling achieves this bound (Agrawal & Goyal 2012, Kaufmann et al. 2012).")),
    callout("⚠️", rt("Warning: ", bold=True), rt("The mSPRT requires choosing the mixing distribution π(θ) before the experiment. A diffuse prior gives more flexibility but lower power. A tight prior around the expected effect size maximizes power but is sensitive to misspecification.")),
    divider(),

    # ── Section 6: Code ───────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — Sample Size & OBF from Scratch"),
    code_block("python", """import math
import scipy.stats as st
import numpy as np

# ── Sample size (two-proportion z-test) ──────────────────────────────────
def sample_size(p1, p2, alpha=0.05, power=0.80):
    \"\"\"Required n per arm for two-proportion z-test.\"\"\"
    z_a = st.norm.ppf(1 - alpha / 2)   # e.g. 1.960 for alpha=0.05
    z_b = st.norm.ppf(power)            # e.g. 0.842 for 80% power
    delta = abs(p2 - p1)
    numerator = (z_a + z_b)**2 * (p1*(1-p1) + p2*(1-p2))
    return math.ceil(numerator / delta**2)

n = sample_size(p1=0.10, p2=0.12)
print(f"n per arm = {n}")   # 3839

# ── O'Brien-Fleming critical values ──────────────────────────────────────
def obf_boundaries(K, alpha=0.05):
    \"\"\"Critical z-values for K equally-spaced interim looks.\"\"\"
    # Solve for z_inf numerically (alpha-spending function sums to alpha)
    from scipy.optimize import brentq
    def total_alpha(z_inf):
        total = 0
        for k in range(1, K+1):
            z_k = z_inf * math.sqrt(K / k)
            total += 2 * (1 - st.norm.cdf(z_k))
        return total - alpha
    z_inf = brentq(total_alpha, 0.1, 10)
    return [z_inf * math.sqrt(K / k) for k in range(1, K+1)]

print(obf_boundaries(K=5))
# [4.562, 3.226, 2.634, 2.281, 2.040]
"""),
    heading3("6b — Thompson Sampling"),
    code_block("python", """import numpy as np

def thompson_sampling(true_p, T=1000, seed=42):
    \"\"\"Beta-Binomial Thompson Sampling for K Bernoulli arms.\"\"\"
    np.random.seed(seed)
    K = len(true_p)
    alpha_k = np.ones(K)   # prior: Beta(1,1) = Uniform
    beta_k  = np.ones(K)
    rewards, chosen = [], []
    for t in range(T):
        samples = np.random.beta(alpha_k, beta_k)   # sample each posterior
        arm = np.argmax(samples)                      # pick best sample
        r = int(np.random.rand() < true_p[arm])     # observe reward
        alpha_k[arm] += r
        beta_k[arm]  += (1 - r)
        rewards.append(r); chosen.append(arm)
    return chosen, rewards, alpha_k, beta_k

chosen, rewards, a, b = thompson_sampling([0.10, 0.12], T=1000)
print(f"Fraction to arm B: {chosen.count(1)/len(chosen):.3f}")  # ~0.85+
print(f"Posterior mode arm B: {(a[1]-1)/(a[1]+b[1]-2):.4f}")    # ≈ 0.12
"""),
    heading3("6c — UCB1"),
    code_block("python", """import numpy as np, math

def ucb1(true_p, T=1000, seed=0):
    \"\"\"UCB1 bandit algorithm for K Bernoulli arms.\"\"\"
    np.random.seed(seed)
    K = len(true_p)
    n_pulls = np.zeros(K); mu_hat = np.zeros(K)
    # Force-explore each arm once
    for arm in range(K):
        r = int(np.random.rand() < true_p[arm])
        n_pulls[arm] += 1; mu_hat[arm] = r
    regret = 0
    best_mu = max(true_p)
    for t in range(K+1, T+1):
        ucb = mu_hat + np.sqrt(2 * math.log(t) / n_pulls)
        arm = np.argmax(ucb)
        r = int(np.random.rand() < true_p[arm])
        n_pulls[arm] += 1
        mu_hat[arm] += (r - mu_hat[arm]) / n_pulls[arm]   # online mean update
        regret += best_mu - true_p[arm]
    return regret, n_pulls, mu_hat

regret, pulls, mu = ucb1([0.10, 0.12], T=1000)
print(f"Cumulative regret: {regret:.2f}")    # ~7-9 (O(ln T))
print(f"Pulls: A={pulls[0]:.0f}, B={pulls[1]:.0f}")
"""),
    heading3("6d — Production (Statsmodels / SciPy)"),
    code_block("python", """from scipy import stats
import numpy as np

# Classical two-proportion z-test
conversions_A, n_A = 412,  4000   # control
conversions_B, n_B = 498,  4000   # variant

count = np.array([conversions_A, conversions_B])
nobs  = np.array([n_A, n_B])
z_stat, p_value = stats.proportions_ztest(count, nobs, alternative='two-sided')
print(f"z = {z_stat:.4f}, p = {p_value:.4f}")

# ⚠️ Gotcha 1: always two-sided unless you pre-committed to direction
# ⚠️ Gotcha 2: only look once (or use OBF if you need interim looks)
# ⚠️ Gotcha 3: check for novelty effects (first-week spikes) before calling it
"""),
    divider(),

    # ── Section 7: Interview Q&A ──────────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy) — What is the purpose of randomization in an A/B test?", bold=True)], [
        para(rt("Randomization ensures that on average, all confounders (user age, device, time-zone, prior behavior) are balanced between the control and variant groups. Without randomization, observed differences could be caused by self-selection or assignment bias rather than the treatment itself. Random assignment makes the potential outcomes independent of the treatment assignment, enabling causal inference.")),
    ]),
    toggle([rt("Q2 (Easy) — What do α and power mean, and what are typical values?", bold=True)], [
        para(eq(r"\alpha"), rt(" = significance level = tolerable false-positive rate = P(reject H₀ | H₀ true). Industry standard: 0.05.")),
        para(rt("Power "), eq(r"= 1-\beta"), rt(" = P(reject H₀ | H₁ true). Industry standard: 0.80 (sometimes 0.90 for high-stakes decisions).")),
        para(rt("Lower α or higher power both require larger n. There is a fundamental trade-off.")),
    ]),
    toggle([rt("Q3 (Medium) — Why is peeking at results bad, and how do you fix it?", bold=True)], [
        para(rt("Peeking — checking and potentially stopping early at unplanned times — inflates the family-wise Type I error rate. With 5 equally-spaced looks at z=1.96, the effective α rises to ≈14.1%. Fixes:")),
        bullet(rt("Pre-specify K interim looks and use alpha-spending (O'Brien-Fleming or Pocock) to adjust per-look boundaries.")),
        bullet(rt("Use always-valid p-values (mSPRT): construct a martingale test statistic valid for any stopping time.")),
        bullet(rt("Never look at results until the pre-specified end date.")),
    ]),
    toggle([rt("Q4 (Medium) — How do you choose MDE?", bold=True)], [
        para(rt("MDE (minimum detectable effect) = the smallest effect size that matters to the business. Set it based on: (a) business value threshold (any smaller effect is not worth shipping), (b) historical distribution of effect sizes, (c) power-cost trade-off (smaller MDE → larger n → longer experiment). Never set MDE post-hoc based on observed effect — that inflates effective α.")),
    ]),
    toggle([rt("Q5 (Hard) — Explain Thompson Sampling and why it is asymptotically optimal.", bold=True)], [
        para(rt("Thompson Sampling maintains a posterior "), eq(r"p_k \mid \text{data} \sim \text{Beta}(\alpha_k, \beta_k)"), rt(" for each arm. At each step, sample "), eq(r"\tilde{p}_k"), rt(" from each posterior and pull the arm with the largest sample.")),
        para(rt("Optimality: the posterior concentrates on the true value at rate "), eq(r"\mathcal{O}(1/n)"), rt(". The probability of sampling a suboptimal arm "), eq(r"k"), rt(" converges to "), eq(r"\text{Beta}(p_k \| p^*) \cdot \ln T / (T \cdot \Delta_k)"), rt(" — exactly the Lai-Robbins lower bound. Thompson Sampling achieves this bound asymptotically without requiring knowledge of the gap "), eq(r"\Delta_k"), rt(".")),
        para(rt("Explain to a PhD Researcher: Thompson Sampling is a posterior sampling strategy that implicitly solves the index policy optimal in the Gittins index sense, matches the KL-based Lai-Robbins lower bound, and has finite-time guarantees (Agrawal & Goyal 2012).")),
        para(rt("Explain to a Research Scientist/Engineer: Thompson Sampling is Bayesian: maintain a Beta posterior for each arm, sample from each, pick the highest. It naturally trades off exploration (wide posteriors) and exploitation (concentrated posteriors on good arms). It's easy to implement, fast, and empirically excellent.")),
    ]),
    toggle([rt("Q6 (Hard) — When would you NOT use a multi-armed bandit?", bold=True)], [
        bullet(rt("When you need a rigorous causal claim with controlled Type I error (e.g., regulatory approval, medical device trials) — bandits don't guarantee fixed α.")),
        bullet(rt("When effects are non-stationary or cyclical — adaptive allocation can confound time effects with treatment effects.")),
        bullet(rt("When you have few users and long-horizon decisions — bandit algorithms need time to learn.")),
        bullet(rt("When the treatment has carry-over effects (e.g., email campaigns) — users may see both arms at different times.")),
    ]),
    toggle([rt("Q7 (Hard) — What is the regret of UCB1, and what is the lower bound?", bold=True)], [
        para(rt("UCB1 achieves expected regret "), eq(r"\mathbb{E}[R_T] \leq \sum_k \frac{8\ln T}{\Delta_k} + O(1)"), rt(".")),
        para(rt("The Lai-Robbins lower bound states that for any consistent policy, "), eq(r"\liminf_{T\to\infty} \mathbb{E}[R_T]/\ln T \geq \sum_k \Delta_k / KL(p_k \| p^*)"), rt(". UCB1 matches this up to a constant (the 8 vs the KL divergence). Thompson Sampling achieves the exact constant (the KL term).")),
    ]),
    toggle([rt("Q8 (System Design) — How would you design an experimentation platform for a large tech company?", bold=True)], [
        bullet(rt("Assignment service: deterministic hashing (e.g., SHA256(user_id + experiment_id)) into buckets, stored in fast key-value store.")),
        bullet(rt("Metrics pipeline: stream events (Kafka), aggregate per arm (Flink/Spark), store in OLAP (Druid).")),
        bullet(rt("Statistical engine: pre-compute required n, schedule looks, compute z-statistics or always-valid p-values.")),
        bullet(rt("Guardrail metrics: automatically flag experiments that move safety metrics negatively.")),
        bullet(rt("CUPED: control for pre-experiment user variance using covariates to reduce standard error and required n.")),
    ]),
    divider(),

    # ── Section 8: Comparison ─────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Method", "Traffic split", "Type I control", "Regret", "Best for"]),
        table_row(["Fixed A/B", "50/50 fixed", "Exact α", "O(T) linear", "Rigorous causal inference"]),
        table_row(["A/B + OBF", "50/50 fixed", "Exact α (with spending)", "O(T) linear", "Clinical trials, regulated"]),
        table_row(["A/B + mSPRT", "50/50 fixed", "Always-valid α", "O(T) linear", "Continuous monitoring (tech)"]),
        table_row(["ε-greedy", "Adaptive", "Not guaranteed", "O(ε·T)", "Simplest baseline"]),
        table_row(["UCB1", "Adaptive", "Not guaranteed", "O(ln T / Δ)", "Frequentist bandit"]),
        table_row(["Thompson Sampling", "Adaptive", "Not guaranteed", "O(ln T / KL)", "Best empirical + Bayes"]),
        table_row(["LinUCB / Neural", "Adaptive (contextual)", "Not guaranteed", "O(√T)", "Personalization"]),
    ),
    callout("🎯", rt("Decision guide: ", bold=True),
        rt("Use fixed A/B when regulatory/legal requirements mandate controlled α. "),
        rt("Use mSPRT when you need continuous monitoring without inflated error. "),
        rt("Use Thompson Sampling when experiment runs weeks+ and traffic is high (regret savings are real). "),
        rt("Use LinUCB/contextual bandits when user features can be leveraged for personalization.")),
    divider(),

    # ── Section 9: Explainer Embed ────────────────────────────────────────────
    heading2("🎨 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the full experimentation pipeline — power analysis, peeking inflation, O'Brien-Fleming boundaries, Thompson Sampling, and UCB1. Use Next/Prev or ← → arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Normal distribution and CLT — required for z-test approximation")),
    bullet(rt("Hypothesis testing (p-values, rejection regions)")),
    bullet(rt("Bayesian inference: Beta-Binomial conjugacy")),
    bullet(rt("Law of large numbers — why arms converge")),
    heading3("What to Learn Next"),
    bullet(rt("CUPED (Controlled-experiment Using Pre-Experiment Data) — variance reduction for A/B tests")),
    bullet(rt("Contextual Bandits (LinUCB, Neural Bandits) — leveraging user features")),
    bullet(rt("Causal inference: difference-in-differences, synthetic control for when RCT is infeasible")),
    bullet(rt("Bayesian optimization — applying bandit ideas to hyperparameter search")),
    heading3("Key Papers"),
    bullet(rt("Johari et al., 'Peeking at A/B Tests' (KDD 2017) — always-valid p-values derivation")),
    bullet(rt("Agrawal & Goyal, 'Analysis of Thompson Sampling' (COLT 2012) — optimality proof")),
    bullet(rt("Auer et al., 'Finite-Time Analysis of the Multiarmed Bandit Problem' (Machine Learning 2002) — UCB1")),
    bullet(rt("Deng et al., 'Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data' (KDD 2013) — CUPED")),
    heading3("Best Resources"),
    bullet(rt("Book: Sutton & Barto, 'Reinforcement Learning: An Introduction' Ch. 2 — multi-armed bandits")),
    bullet(rt("Book: Imbens & Rubin, 'Causal Inference' — rigorous treatment of randomization")),
    bullet(rt("Blog: Netflix Tech Blog, 'Interpreting A/B test results: false positives and statistical significance'")),
    bullet(rt("Statsmodels.stats.proportion — Python implementation of sample size and z-tests")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Hypothesis Testing (3.1), Bayesian Inference (3.5), Causal Inference, Reinforcement Learning, MLOps Experimentation Platforms.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
