#!/usr/bin/env python3
"""Update Notion page for: States, observations, transition and emission probabilities (HMM)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-8146-b17e-d73cefba309a"
ICON = "🟡"  # Intermediate
EXPLAINER_URL = "https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/hmm_states_emissions_explainer.html"

PROPERTIES = {
    "Status": {"select": {"name": "Completed"}},
    "Depth": {"select": {"name": "Intermediate"}},
    "Interview Priority": {"select": {"name": "Must Know"}},
    "Has Explainer": {"checkbox": True},
    "Explainer URL": {"url": EXPLAINER_URL},
}

blocks = [
    # ── Section 1: The 30-Second Version ──────────────────────────────────────
    heading2("🎯 The 30-Second Version"),
    heading3("What is this?"),
    para(rt("A Hidden Markov Model (HMM) is a statistical machine that generates sequences of observable symbols while secretly jumping between hidden states you cannot see. Each hidden state has its own probability of producing each observable symbol, and the transitions between hidden states follow fixed probabilities.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine you're watching a friend from behind a curtain. You can't see the weather outside, but you can see whether they carry an umbrella, wear sunglasses, or bring a raincoat. The weather is the hidden state; their accessories are the observations. An HMM models exactly this: hidden causes producing visible effects.")),
    para(rt("One-sentence summary: An HMM is a probabilistic model with a hidden Markov chain (governed by transition matrix A) whose states emit observable symbols (governed by emission matrix B), starting from an initial distribution π.")),
    callout("💡", rt("If you remember one thing: ", bold=True), rt("λ = (A, B, π) fully defines an HMM. A controls where the hidden state goes next; B controls what you see; π controls where you start.")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context & Motivation"),
    heading3("The Problem"),
    para(rt("In the 1960s, speech researchers faced a key challenge: the acoustic signal of a spoken word varies enormously between speakers, speeds, and contexts. There was no principled way to decode the underlying phoneme sequence from noisy observations.")),
    heading3("What Came Before"),
    para(rt("Markov chains modelled state sequences, but assumed states were directly observable — useless for speech where phonemes are inferred, not measured. Template matching (DTW) existed but had no probabilistic semantics.")),
    heading3("The Breakthrough"),
    para(rt("Leonard Baum and colleagues at the Institute for Defense Analyses developed the mathematical framework for HMMs in the late 1960s (published 1966–1972). The key insight: treat the hidden state sequence as a latent variable and maximise observed-data likelihood via the Forward-Backward (Baum-Welch) EM algorithm.")),
    heading3("Key Papers"),
    bullet(rt("Baum & Petrie (1966) — "Statistical Inference for Probabilistic Functions of Finite State Markov Chains" — foundational HMM paper")),
    bullet(rt("Baum et al. (1970) — "A Maximization Technique in the Statistical Analysis of Probabilistic Functions of Markov Chains" — Baum-Welch algorithm")),
    bullet(rt("Rabiner (1989) — "A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition" IEEE Proc. — the definitive reference; 20 000+ citations")),
    heading3("Evolution Timeline"),
    para(rt("Markov chains (1906) → HMMs for speech (Baum 1966) → Viterbi algorithm adopted (1967) → Applied to speech recognition at IBM (1975–1985) → Became dominant ASR paradigm (1990s) → CRFs augment HMMs (2001) → Deep learning replaces in ASR (2012+) → Still core in bioinformatics, finance, NLP POS tagging")),
    heading3("Before vs After"),
    table(4,
        table_row(["Dimension", "Markov Chains (Before)", "HMMs (After)", "CRFs / Deep Models (After))"]),
        table_row(["State visibility", "States directly observed", "States hidden / latent", "Labels predicted discriminatively"]),
        table_row(["Observations", "States ARE observations", "States emit observations", "Observations condition labels"]),
        table_row(["Parameter learning", "Count co-occurrences", "Baum-Welch EM", "Gradient descent"]),
        table_row(["Long-range deps", "Limited by order", "Limited by Markov order", "Arbitrary (CRF, Transformer)"]),
        table_row(["Best for", "Ergodic sequences", "Speech, NLP POS, genomics", "NER, structured prediction"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("The Five Components"),
    para(rt("An HMM is defined by:")),
    numbered(rt("Hidden states "), eq(r"S = \{s_1, \ldots, s_N\}"), rt(" — unobservable process with N states")),
    numbered(rt("Observation vocabulary "), eq(r"V = \{v_1, \ldots, v_M\}"), rt(" — M distinct observable symbols")),
    numbered(eq(r"\pi"), rt(" — initial state distribution: "), eq(r"\pi_i = P(q_1 = s_i)")),
    numbered(eq(r"A"), rt(" — transition matrix: "), eq(r"a_{ij} = P(q_{t+1}=s_j \mid q_t=s_i)")),
    numbered(eq(r"B"), rt(" — emission matrix: "), eq(r"b_j(k) = P(o_t=v_k \mid q_t=s_j)")),
    heading3("Markov Assumptions"),
    callout("🔑", rt("First-order Markov property: ", bold=True), eq(r"P(q_t \mid q_{t-1}, q_{t-2}, \ldots) = P(q_t \mid q_{t-1})"), rt(" — future state depends only on present state, not full history.")),
    callout("🔑", rt("Output independence: ", bold=True), eq(r"P(o_t \mid q_1,\ldots,q_T,o_1,\ldots,o_{t-1}) = P(o_t \mid q_t)"), rt(" — emission depends only on current hidden state.")),
    heading3("Stochasticity Constraints"),
    para(rt("Every row of A and B must be a valid probability distribution:")),
    equation_block(r"\sum_{j=1}^N a_{ij} = 1 \quad \forall i, \qquad \sum_{k=1}^M b_j(k) = 1 \quad \forall j, \qquad \sum_{i=1}^N \pi_i = 1"),
    heading3("The Three Classic Problems"),
    table(3,
        table_row(["Problem", "Question", "Algorithm"]),
        table_row(["Evaluation", "P(O | λ) — how likely is this observation sequence?", "Forward algorithm"]),
        table_row(["Decoding", "Q* = argmax P(Q,O|λ) — best hidden state path?", "Viterbi algorithm"]),
        table_row(["Learning", "λ* = argmax P(O|λ) — fit model to data?", "Baum-Welch (EM)"]),
    ),
    divider(),

    # ── Section 4: Architecture & Internal Workings ────────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD Deep Dive)"),
    heading3("The Trellis Structure"),
    para(rt("Unrolling an HMM over time produces a ", bold=False), rt("trellis", bold=True), rt(": a grid of N × T nodes. Node (i, t) represents being in state s_i at time t. Edges carry transition probabilities a_ij; each column of nodes 'emits' the observation o_t via b_i(o_t).")),
    heading3("Forward Algorithm — Full Internal Walkthrough"),
    para(rt("Define the forward variable:")),
    equation_block(r"\alpha_t(i) = P(o_1, o_2, \ldots, o_t,\; q_t = s_i \mid \lambda)"),
    para(rt("Initialisation (t=1):")),
    equation_block(r"\alpha_1(i) = \pi_i \cdot b_i(o_1)"),
    para(rt("Induction (t → t+1): sum over all predecessor states:")),
    equation_block(r"\alpha_{t+1}(j) = \left[\sum_{i=1}^{N} \alpha_t(i) \cdot a_{ij}\right] \cdot b_j(o_{t+1})"),
    para(rt("Termination:")),
    equation_block(r"P(O \mid \lambda) = \sum_{i=1}^N \alpha_T(i)"),
    heading3("Viterbi Algorithm — Numerical Trace"),
    para(rt("Example: N=2 states {Sunny, Rainy}, M=3 observations {Walk, Shop, Clean}.")),
    para(rt("Parameters: π=[0.6, 0.4], A=[[0.7,0.3],[0.4,0.6]], B=[[0.6,0.3,0.1],[0.1,0.4,0.5]].")),
    para(rt("Observation sequence: Walk, Shop, Clean.")),
    para(rt("Step 1 — Initialisation (observe Walk):")),
    equation_block(r"\delta_1(S) = \pi_S \cdot b_S(\text{Walk}) = 0.6 \times 0.6 = 0.360"),
    equation_block(r"\delta_1(R) = \pi_R \cdot b_R(\text{Walk}) = 0.4 \times 0.1 = 0.040"),
    para(rt("Step 2 — Recursion (observe Shop):")),
    equation_block(r"\delta_2(S) = \max\{0.360 \times 0.7,\; 0.040 \times 0.4\} \times b_S(\text{Shop}) = 0.252 \times 0.3 = 0.0756"),
    equation_block(r"\delta_2(R) = \max\{0.360 \times 0.3,\; 0.040 \times 0.6\} \times b_R(\text{Shop}) = 0.108 \times 0.4 = 0.0432"),
    para(rt("Backpointers: ψ₂(S)=Sunny, ψ₂(R)=Sunny.")),
    para(rt("Step 3 — Recursion (observe Clean):")),
    equation_block(r"\delta_3(S) = \max\{0.0756 \times 0.7,\; 0.0432 \times 0.4\} \times 0.1 = 0.05292 \times 0.1 = 0.005292"),
    equation_block(r"\delta_3(R) = \max\{0.0756 \times 0.3,\; 0.0432 \times 0.6\} \times 0.5 = 0.02592 \times 0.5 = 0.012960"),
    para(rt("Best final state: Rainy (0.01296 > 0.005292). Backtrack via ψ:")),
    para(rt("ψ₃(R)=Sunny → ψ₂(S)=Sunny → start. Optimal path: Sunny → Sunny → Rainy.")),
    heading3("Why Max vs Sum?"),
    callout("🔍", rt("Forward uses ", bold=False), rt("sum ", bold=True), rt("over predecessors (marginalises over all paths) giving P(O|λ). Viterbi uses "), rt("max ", bold=True), rt("(finds the single best path). The two algorithms share identical recursion structure but different aggregation operators.")),
    heading3("Numerical Stability — Log Domain"),
    para(rt("For long sequences, products of probabilities underflow to zero in floating point. Standard practice is to work in log space:")),
    equation_block(r"\log \delta_t(j) = \log b_j(o_t) + \max_{i}\{\log \delta_{t-1}(i) + \log a_{ij}\}"),
    divider(),

    # ── Section 5: The Math Behind It ─────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("Joint Probability of Sequence and Path"),
    equation_block(r"P(O, Q \mid \lambda) = \pi_{q_1} \cdot \prod_{t=1}^{T-1} a_{q_t q_{t+1}} \cdot \prod_{t=1}^{T} b_{q_t}(o_t)"),
    heading3("Marginal Likelihood via Forward Algorithm"),
    para(rt("Summing over all possible hidden paths Q:")),
    equation_block(r"P(O \mid \lambda) = \sum_{Q} P(O, Q \mid \lambda) = \sum_{i=1}^N \alpha_T(i)"),
    para(rt("Naïve summation costs "), eq(r"\mathcal{O}(N^T \cdot T)"), rt("; Forward reduces this to "), eq(r"\mathcal{O}(N^2 T)")),
    heading3("Backward Variable"),
    para(rt("Complementary to α, the backward variable "), eq(r"\beta_t(i)"), rt(" captures the probability of the future:")),
    equation_block(r"\beta_t(i) = P(o_{t+1}, \ldots, o_T \mid q_t = s_i, \lambda)"),
    equation_block(r"\beta_T(i) = 1, \qquad \beta_t(i) = \sum_{j=1}^N a_{ij} \cdot b_j(o_{t+1}) \cdot \beta_{t+1}(j)"),
    heading3("State Occupation Probabilities (for Baum-Welch)"),
    para(rt("Probability of being in state i at time t:")),
    equation_block(r"\gamma_t(i) = \frac{\alpha_t(i)\,\beta_t(i)}{\sum_{j=1}^N \alpha_t(j)\,\beta_t(j)}"),
    para(rt("Probability of transitioning from i to j at time t:")),
    equation_block(r"\xi_t(i,j) = \frac{\alpha_t(i)\, a_{ij}\, b_j(o_{t+1})\, \beta_{t+1}(j)}{\sum_{i'}\sum_{j'} \alpha_t(i')\, a_{i'j'}\, b_{j'}(o_{t+1})\, \beta_{t+1}(j')}"),
    heading3("M-Step Re-estimation (Baum-Welch)"),
    equation_block(r"\hat{\pi}_i = \gamma_1(i)"),
    equation_block(r"\hat{a}_{ij} = \frac{\sum_{t=1}^{T-1} \xi_t(i,j)}{\sum_{t=1}^{T-1} \gamma_t(i)}"),
    equation_block(r"\hat{b}_j(k) = \frac{\sum_{t=1,\, o_t=v_k}^{T} \gamma_t(j)}{\sum_{t=1}^{T} \gamma_t(j)}"),
    callout("⚠️", rt("Warning: ", bold=True), rt("Baum-Welch is an EM algorithm and converges to a local optimum only. It is sensitive to initialisation. Multiple random restarts are standard practice. Also, it assumes the number of hidden states N is known — model selection for N requires BIC, AIC, or cross-validation.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("From Scratch — NumPy Viterbi"),
    code_block("python", """import numpy as np

# HMM parameters
pi = np.array([0.6, 0.4])           # initial distribution [Sunny, Rainy]
A  = np.array([[0.7, 0.3],          # transition matrix (row = from state)
               [0.4, 0.6]])
B  = np.array([[0.6, 0.3, 0.1],     # emission matrix (row = state, col = obs)
               [0.1, 0.4, 0.5]])
# States: 0=Sunny, 1=Rainy | Observations: 0=Walk, 1=Shop, 2=Clean

obs = np.array([0, 1, 2])  # Walk, Shop, Clean

def viterbi(obs, pi, A, B):
    T, N = len(obs), len(pi)
    delta = np.zeros((T, N))   # max-prob up to t in state i
    psi   = np.zeros((T, N), dtype=int)  # backpointers

    # Initialisation
    delta[0] = pi * B[:, obs[0]]

    # Recursion
    for t in range(1, T):
        for j in range(N):
            # best previous state * transition * emission
            scores      = delta[t-1] * A[:, j] * B[j, obs[t]]
            psi[t, j]   = np.argmax(scores)
            delta[t, j] = np.max(scores)

    # Traceback
    q_star = np.zeros(T, dtype=int)
    q_star[-1] = np.argmax(delta[-1])
    for t in range(T-2, -1, -1):
        q_star[t] = psi[t+1, q_star[t+1]]

    return q_star, delta

q_star, delta = viterbi(obs, pi, A, B)
print([['Sunny','Rainy'][s] for s in q_star])  # ['Sunny', 'Sunny', 'Rainy']
print(np.round(delta, 6))
# [[0.36    0.04   ]
#  [0.0756  0.0432 ]
#  [0.005292 0.01296]]
"""),
    heading3("Log-Domain Viterbi (Numerically Stable)"),
    code_block("python", """def viterbi_log(obs, pi, A, B):
    \"\"\"Viterbi in log domain to avoid floating-point underflow.\"\"\"
    T, N = len(obs), len(pi)
    log_A = np.log(A + 1e-300)
    log_B = np.log(B + 1e-300)
    log_delta = np.zeros((T, N))
    psi = np.zeros((T, N), dtype=int)

    log_delta[0] = np.log(pi + 1e-300) + log_B[:, obs[0]]
    for t in range(1, T):
        for j in range(N):
            scores = log_delta[t-1] + log_A[:, j] + log_B[j, obs[t]]
            psi[t, j] = np.argmax(scores)
            log_delta[t, j] = np.max(scores)

    q_star = np.zeros(T, dtype=int)
    q_star[-1] = np.argmax(log_delta[-1])
    for t in range(T-2, -1, -1):
        q_star[t] = psi[t+1, q_star[t+1]]
    return q_star, np.exp(log_delta)
"""),
    heading3("Production — hmmlearn"),
    code_block("python", """from hmmlearn import hmm
import numpy as np

model = hmm.CategoricalHMM(n_components=2, n_features=3)
model.startprob_     = np.array([0.6, 0.4])
model.transmat_      = np.array([[0.7, 0.3],[0.4, 0.6]])
model.emissionprob_  = np.array([[0.6,0.3,0.1],[0.1,0.4,0.5]])

obs_seq = np.array([[0],[1],[2]])  # shape (T, 1) for discrete HMM
log_prob, states = model.decode(obs_seq, algorithm="viterbi")
print(f"Log-likelihood: {log_prob:.4f}")  # ln(0.01296) ≈ -4.344
print(f"State sequence: {states}")         # [0 0 1]

# Fitting from data (Baum-Welch)
model_fit = hmm.CategoricalHMM(n_components=2, n_iter=100, tol=1e-4)
model_fit.fit(obs_seq)  # obs_seq is (T,1) array of integer observations
"""),
    callout("⚠️", rt("Gotcha: ", bold=True), rt("hmmlearn's CategoricalHMM expects a 2D array of shape (T, 1) for single-feature discrete obs. Pass lengths=[T1,T2,...] when fitting multiple sequences. Always use the log-domain for sequences T > 50 to avoid underflow.")),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎯 Interview Deep-Dive"),
    toggle([rt("Q1 (Easy): What are the three matrices in an HMM and what do they represent?", bold=True)], [
        para(rt("A: λ = (A, B, π). A is the N×N transition matrix where a_ij = P(next state = j | current = i). B is the N×M emission matrix where b_j(k) = P(observe symbol k | in state j). π is the N-vector initial state distribution. All rows of A and B, and the vector π, must sum to 1.")),
    ]),
    toggle([rt("Q2 (Easy): What is the Markov assumption and why is it useful?", bold=True)], [
        para(rt("A: The first-order Markov property states that P(q_t | q_{t-1}, ..., q_1) = P(q_t | q_{t-1}). This memoryless property makes the joint probability factorise into a product of local terms, enabling efficient dynamic programming algorithms like Forward and Viterbi that run in O(N²T) rather than O(N^T).")),
    ]),
    toggle([rt("Q3 (Medium): Explain the difference between the Forward algorithm and the Viterbi algorithm.", bold=True)], [
        para(rt("A: Both are DP algorithms on the trellis. Forward computes α_t(i) = P(o_1,...,o_t, q_t=i) by summing over predecessor states (marginalising). It answers: P(O|λ). Viterbi computes δ_t(i) = max P(q_1,...,q_{t-1}, q_t=i, o_1,...,o_t) by taking the max over predecessors. It answers: what is the single most probable hidden state sequence?")),
        para(rt("Both have identical O(N²T) complexity; the only difference is sum vs max.")),
    ]),
    toggle([rt("Q4 (Medium): Why do we work in log space for HMMs?", bold=True)], [
        para(rt("A: Viterbi and Forward compute products of many probabilities (each < 1). For T=100 and N=5, a product of 100 terms like 0.1^100 = 10^-100 underflows IEEE 754 double precision (min ~10^-308). In log space, products become sums: log(δ_t(j)) = log(b_j(o_t)) + max_i{log(δ_{t-1}(i)) + log(a_{ij})}. Addition never underflows.")),
    ]),
    toggle([rt("Q5 (Hard): How does Baum-Welch work and what are its limitations?", bold=True)], [
        para(rt("A: Baum-Welch is the EM algorithm for HMMs. E-step: compute γ_t(i) and ξ_t(i,j) using forward (α) and backward (β) variables. M-step: re-estimate π, A, B as expected-count ratios. It provably increases P(O|λ) monotonically but converges to a local maximum, not global. Issues: (1) sensitive to random init — use k-means or domain-priors to initialise; (2) N (number of states) is a hyperparameter — select via BIC; (3) can degenerate if a state gets zero occupation probability.")),
    ]),
    toggle([rt("Q6 (Hard): How does an HMM relate to a Kalman filter?", bold=True)], [
        para(rt("A: A Kalman filter is a Gaussian HMM with continuous hidden state and linear Gaussian transitions/emissions. HMM (discrete): q_t ∈ {1,...,N}, emission P(o|q) is categorical. Kalman filter: q_t ∈ R^n, state equation q_t = F q_{t-1} + w_t (w_t ~ N(0,Q)), observation y_t = H q_t + v_t (v_t ~ N(0,R)). The Forward algorithm corresponds to Kalman predict+update; Viterbi corresponds to Kalman smoothing. Both are special cases of belief propagation on a chain-structured graphical model.")),
    ]),
    toggle([rt("Q7 (System Design): How would you use HMMs in a speech recognition pipeline?", bold=True)], [
        para(rt("A: Classic ASR: (1) Extract MFCC features from audio (39-dim every 10ms). (2) Each phoneme gets a left-to-right HMM with 3-5 states and Gaussian (or GMM) emissions. (3) Word = concatenation of phoneme HMMs; language model adds P(word sequence). (4) Viterbi decoding finds best phoneme/word sequence. Key design choices: number of states per phoneme, GMM components vs DNN acoustic model, beam search for efficiency. Modern systems replace GMM emissions with DNN acoustic models (CD-DNN-HMM) or end-to-end CTC/attention, but the HMM trellis structure persists in forced-alignment tasks.")),
    ]),
    callout("🚩", rt("Red flags in interviews: ", bold=True), rt("(1) Saying 'Viterbi gives P(O|λ)' — Viterbi gives the most probable path, not the likelihood. (2) Forgetting that rows of A and B must sum to 1. (3) Confusing forward (α) with backward (β) variables.")),
    divider(),

    # ── Section 8: Comparison & Trade-offs ────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(5,
        table_row(["Dimension", "HMM", "CRF (Linear-Chain)", "RNN/LSTM", "Transformer"]),
        table_row(["Model type", "Generative P(O,Q)", "Discriminative P(Q|O)", "Discriminative", "Discriminative"]),
        table_row(["Training", "Baum-Welch (EM)", "Gradient descent", "Gradient descent", "Gradient descent"]),
        table_row(["Long-range deps", "Weak (Markov order)", "Feature-engineered", "LSTM ~100 steps", "Arbitrary via attention"]),
        table_row(["Interpretability", "High (A,B explicit)", "Medium (weights)", "Low", "Low"]),
        table_row(["Inference cost", "O(N²T)", "O(N²T) Viterbi", "O(NT)", "O(T²N)"]),
        table_row(["Labelled data needed?", "No (unsupervised EM)", "Yes", "Yes", "Yes"]),
        table_row(["Best use case", "Small state space, seq labelling, bioinformatics", "NER, POS (with features)", "Speech, LM", "NLP, CV, everything"]),
    ),
    callout("🎯", rt("Decision guide: ", bold=True), rt("Use HMMs when you need (a) interpretable hidden states with probabilistic semantics, (b) unsupervised learning (Baum-Welch), or (c) a generative model of sequences. Use CRFs for discriminative sequence labelling with rich features. Use LSTMs/Transformers when you have enough labelled data and need maximum accuracy.")),
    heading3("Advantages"),
    bullet(rt("Fully probabilistic — outputs likelihoods, handles uncertainty")),
    bullet(rt("Can learn unsupervised (no labels needed for Baum-Welch)")),
    bullet(rt("Interpretable hidden states and parameter matrices")),
    bullet(rt("Efficient O(N²T) inference via DP")),
    bullet(rt("Well-understood theoretical guarantees")),
    heading3("Disadvantages"),
    bullet(rt("Markov assumption is often violated (long-range dependencies ignored)")),
    bullet(rt("Number of hidden states N must be chosen manually")),
    bullet(rt("Baum-Welch finds local optima only; sensitive to init")),
    bullet(rt("Discrete emission assumption — requires feature engineering for continuous data")),
    bullet(rt("Scales poorly with N (O(N²) transition parameters)")),
    divider(),

    # ── Section 9: Interactive Explainer ──────────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the concept visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Markov Chains & Markov Property — the backbone of HMM transitions")),
    bullet(rt("Probability Distributions & Bayes' Theorem")),
    bullet(rt("Expectation-Maximisation (EM) Algorithm — for understanding Baum-Welch")),
    bullet(rt("Dynamic Programming — Forward and Viterbi are DP on a DAG")),
    heading3("What to Learn Next"),
    bullet(rt("Forward-Backward Algorithm (full derivation) & Baum-Welch EM")),
    bullet(rt("Gaussian HMMs & Continuous Emissions")),
    bullet(rt("Conditional Random Fields (CRF) — discriminative generalization")),
    bullet(rt("Speech Recognition & Acoustic Modelling")),
    bullet(rt("CpG Island Detection (HMMs in bioinformatics)")),
    heading3("Key Papers"),
    bullet(rt("Baum et al. (1970) — Baum-Welch EM algorithm — the foundational learning paper")),
    bullet(rt("Viterbi (1967) — 'Error bounds for convolutional codes…' — original Viterbi algorithm")),
    bullet(rt("Rabiner (1989) — 'A Tutorial on HMMs…' IEEE Proc. — best entry-level deep dive")),
    bullet(rt("Lafferty et al. (2001) — 'Conditional Random Fields…' — CRF extends HMMs discriminatively")),
    heading3("Best Resources"),
    bullet(rt("Rabiner 1989 tutorial (IEEE Proc.) — 40 pages of rigorous but readable exposition")),
    bullet(rt("Manning & Schütze 'Foundations of Statistical NLP' Chapter 9")),
    bullet(rt("CS229 Stanford Notes on HMMs (free online)")),
    bullet(rt("hmmlearn Python library — clean NumPy implementation to study")),
    callout("🔗", rt("This topic connects to: ", bold=True), rt("Viterbi Algorithm, Baum-Welch EM, Kalman Filter, Conditional Random Fields, Markov Chain Monte Carlo, Gaussian Mixture Models, Speech Acoustic Modelling")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
