#!/usr/bin/env python3
"""Update Notion page for: Cross-entropy loss for classification (connection to MLE)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from notion_template import *

PAGE_ID = "33c93418-809c-811d-8d57-e0c37edf12e0"
ICON = "🟡"   # Intermediate
SLUG = "cross_entropy_loss_classification"
EXPLAINER_URL = f"https://jayitsaha.github.io/PersonalSkillUp/AI/explainers/{SLUG}_explainer.html"

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
    para(rt("Cross-entropy loss is the standard loss function for training classification models. "
            "Given a predicted probability distribution over classes and the true label, it measures how "
            "surprised the model would be to see that label. Minimizing this loss trains the model to "
            "assign high probability to the correct class.")),
    heading3("Real-World Analogy"),
    para(rt("Imagine a weather forecaster who gives a 90% chance of rain, and it actually rains. "
            "Great — low loss. But if she said 5% chance of rain and it poured, the loss is huge. "
            "Cross-entropy penalizes confident wrong predictions exponentially harder than uncertain ones.")),
    callout("💡", rt("If you remember one thing: ", bold=True),
            rt("Minimizing average cross-entropy over one-hot labels = maximizing log-likelihood (MLE) = "
               "minimizing KL divergence from the empirical label distribution. These are three names for "
               "the same optimization problem. And the gradient is simply "), eq(r"\hat{q} - y"), rt(".")),
    divider(),

    # ── Section 2: Historical Context ─────────────────────────────────────────
    heading2("📜 Why This Exists — Historical Context"),
    heading3("The Problem"),
    para(rt("Early classification models used mean squared error (MSE) on one-hot labels. This creates "
            "a poor loss landscape: the gradient of MSE through softmax saturates when probabilities are "
            "near 0 or 1, causing vanishing gradients and slow learning in the early stages of training.")),
    heading3("What Came Before"),
    para(rt("Perceptron models in the 1950s–1970s used direct threshold decision rules. Logistic regression "
            "(1950s statistics) introduced maximum likelihood estimation for binary classification, producing "
            "the log-loss / binary cross-entropy as a natural byproduct of the MLE framework.")),
    heading3("The Breakthrough"),
    para(rt("Rumelhart, Hinton & Williams (1986) extended backpropagation to multi-layer networks. The "
            "combination of softmax output with cross-entropy loss — popularized in neural network training "
            "by LeCun, Bottou et al. (1989–1998) — replaced MSE for classification because it provides "
            "non-saturating gradients and has a clean probabilistic interpretation.")),
    heading3("Key Papers"),
    bullet(rt("Rumelhart, Hinton & Williams (1986) — Learning representations by back-propagating errors. "
              "Nature 323. Introduced modern backprop.")),
    bullet(rt("LeCun et al. (1989) — Backpropagation Applied to Handwritten Zip Code Recognition. "
              "Established CE + softmax as standard for neural classification.")),
    bullet(rt("Bridle (1990) — Probabilistic Interpretation of Feedforward Classification Network Outputs "
              "with Relationships to Statistical Pattern Recognition. Formalized softmax as MLE.")),
    heading3("Evolution Timeline"),
    para(rt("Perceptron (threshold) → Logistic Regression (sigmoid + BCE) → "
            "Multi-class softmax + CE → Label smoothing + focal loss (2017+) → "
            "Temperature-scaled CE for calibration")),
    table(3,
          table_row(["Dimension", "MSE on One-Hot", "Cross-Entropy Loss"]),
          table_row(["Probabilistic basis", "None (arbitrary distance)", "MLE / KL minimization"]),
          table_row(["Gradient near boundary", "Saturates (vanishing)", "Always non-zero: q-y"]),
          table_row(["Sensitive to confident errors", "Moderate (quadratic)", "High (logarithmic divergence)"]),
          table_row(["Preferred for classification", "No", "Yes (standard)"]),
    ),
    divider(),

    # ── Section 3: Core Concepts ───────────────────────────────────────────────
    heading2("🧩 Core Concepts & Theory"),
    heading3("Key Definitions"),
    para(rt("Let "), eq(r"K"), rt(" be the number of classes, "), eq(r"z \in \mathbb{R}^K"), rt(" be the logit vector "
            "from the final linear layer, "), eq(r"y \in \{0,1\}^K"), rt(" be the one-hot true label with "),
        eq(r"y_{k^*} = 1"), rt(" for true class "), eq(r"k^*"), rt(".")),
    para(rt("The softmax function converts logits to probabilities:")),
    equation_block(r"\hat{q}_k = \text{softmax}(z)_k = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}, \quad k = 1,\ldots,K"),
    para(rt("The cross-entropy loss for one example is:")),
    equation_block(r"\mathcal{L}_{CE} = -\sum_{k=1}^{K} y_k \log \hat{q}_k = -\log \hat{q}_{k^*}"),
    para(rt("The average CE loss over a dataset of "), eq(r"N"), rt(" examples is:")),
    equation_block(r"\mathcal{L} = -\frac{1}{N} \sum_{i=1}^{N} \log \hat{q}_{k_i^*}"),
    heading3("Core Property"),
    callout("🔑", rt("The cross-entropy loss is jointly convex in the softmax probabilities, and the softmax–CE "
                     "combination has gradient "), eq(r"\nabla_z \mathcal{L}_{CE} = \hat{q} - y"),
            rt(" — a clean signal that is zero only at the global optimum.")),
    heading3("Prerequisites"),
    bullet(rt("Shannon entropy: ", bold=True), rt("the average surprise under a distribution")),
    bullet(rt("KL divergence: ", bold=True), rt("asymmetric information-theoretic distance between distributions")),
    bullet(rt("Softmax: ", bold=True), rt("normalizes logits into a probability simplex")),
    bullet(rt("Maximum likelihood estimation: ", bold=True), rt("choose parameters that maximize data probability")),
    divider(),

    # ── Section 4: PhD Deep Dive ───────────────────────────────────────────────
    heading2("🔬 Architecture & Internal Workings (PhD-Level Deep Dive)"),
    heading3("The Full Softmax → CE Pipeline"),
    para(rt("Step 1 — Forward pass: The final linear layer computes "), eq(r"z = W h + b"),
        rt(" where "), eq(r"h"), rt(" is the penultimate representation. Example: "),
        eq(r"z = [2.1,\ 0.8,\ -0.5]"), rt(".")),
    para(rt("Step 2 — Softmax: Subtract "), eq(r"\max(z) = 2.1"), rt(" for numerical stability, then exponentiate:")),
    equation_block(r"e^{z - 2.1} = [e^0,\ e^{-1.3},\ e^{-2.6}] = [1.0000,\ 0.2725,\ 0.0743]"),
    para(rt("Sum: "), eq(r"S = 1.3468"), rt(". Probabilities: "), eq(r"\hat{q} = [0.7425,\ 0.2024,\ 0.0551]"), rt(".")),
    para(rt("Step 3 — Loss (true class = 0):")),
    equation_block(r"\mathcal{L}_{CE} = -\log(0.7425) = 0.2977"),
    para(rt("Step 4 — Gradient w.r.t. logits:")),
    equation_block(r"\nabla_z \mathcal{L}_{CE} = \hat{q} - y = [0.7425 - 1,\ 0.2024 - 0,\ 0.0551 - 0] = [-0.2575,\ +0.2024,\ +0.0551]"),
    heading3("Why the Gradient is q − y: Derivation"),
    para(rt("Define "), eq(r"S = \sum_j e^{z_j}"), rt(". Then "), eq(r"\hat{q}_{k^*} = e^{z_{k^*}} / S"), rt(".")),
    para(rt("Case "), eq(r"k = k^*"), rt(" (true class):")),
    equation_block(r"\frac{\partial \mathcal{L}}{\partial z_{k^*}} = -\frac{\partial}{\partial z_{k^*}} \log \hat{q}_{k^*} = -\frac{1}{\hat{q}_{k^*}} \cdot \frac{e^{z_{k^*}} S - e^{z_{k^*}} e^{z_{k^*}}}{S^2} = -(1 - \hat{q}_{k^*}) = \hat{q}_{k^*} - 1"),
    para(rt("Case "), eq(r"k \neq k^*"), rt(" (non-true class):")),
    equation_block(r"\frac{\partial \mathcal{L}}{\partial z_k} = -\frac{\partial}{\partial z_k} \log \hat{q}_{k^*} = -\frac{1}{\hat{q}_{k^*}} \cdot \frac{-e^{z_{k^*}} e^{z_k}}{S^2} = \hat{q}_k"),
    para(rt("Combined (using one-hot "), eq(r"y_k"), rt("):")),
    equation_block(r"\frac{\partial \mathcal{L}}{\partial z_k} = \hat{q}_k - y_k"),
    heading3("Failure Modes & Edge Cases"),
    bullet(rt("Class imbalance: ", bold=True), rt("If class 0 appears 99% of the time, a model predicting class 0 always "
               "achieves very low CE loss but fails on minority classes. Fix: weighted CE or focal loss.")),
    bullet(rt("Overconfidence: ", bold=True), rt("CE loss can drive probabilities to near 1 on training data (overfitting). "
               "Fix: label smoothing, which replaces hard targets with soft ones.")),
    bullet(rt("Large logit scale: ", bold=True), rt("If logits grow very large, softmax outputs saturate near 0 or 1 and "
               "gradients vanish. Fix: weight decay, batch norm, or logit clipping.")),
    bullet(rt("Numerical underflow: ", bold=True), rt("log(softmax(z)) = z - log-sum-exp(z). Use PyTorch's "
               "F.log_softmax + F.nll_loss (= F.cross_entropy) never softmax then log.")),
    divider(),

    # ── Section 5: The Math Behind It ─────────────────────────────────────────
    heading2("📐 The Math Behind It"),
    heading3("The Three-Way Equivalence"),
    para(rt("We show that minimizing CE = maximizing log-likelihood = minimizing KL from empirical distribution.")),
    heading3("View 1: Cross-Entropy Loss"),
    equation_block(r"\mathcal{L}_{CE}(\theta) = -\frac{1}{N} \sum_{i=1}^{N} \log q_\theta(y_i \mid x_i)"),
    heading3("View 2: Maximum Likelihood"),
    para(rt("Under the categorical model "), eq(r"p(y \mid x; \theta) = q_\theta(y \mid x)"), rt(", the log-likelihood is:")),
    equation_block(r"\ell(\theta) = \frac{1}{N} \sum_{i=1}^{N} \log q_\theta(y_i \mid x_i) = -\mathcal{L}_{CE}"),
    para(rt("Maximizing "), eq(r"\ell(\theta)"), rt(" is identical to minimizing "), eq(r"\mathcal{L}_{CE}"), rt(".")),
    heading3("View 3: KL Divergence from Empirical Distribution"),
    para(rt("Let "), eq(r"\hat{p}"), rt(" be the empirical distribution over "), eq(r"(x, y)"), rt(" pairs: "
            "a uniform mixture of point masses at the training examples. The cross-entropy between "),
        eq(r"\hat{p}"), rt(" and the model "), eq(r"q_\theta"), rt(" is:")),
    equation_block(r"H(\hat{p},\, q_\theta) = -\sum_{x,y} \hat{p}(x,y) \log q_\theta(y \mid x) = -\frac{1}{N}\sum_i \log q_\theta(y_i \mid x_i) = \mathcal{L}_{CE}"),
    para(rt("Using "), eq(r"H(\hat{p}, q_\theta) = H(\hat{p}) + D_{\text{KL}}(\hat{p} \,\|\, q_\theta)"), rt(", and noting "),
        eq(r"H(\hat{p})"), rt(" is constant w.r.t. "), eq(r"\theta"), rt(":")),
    equation_block(r"\underset{\theta}{\min}\; \mathcal{L}_{CE} = \underset{\theta}{\min}\; D_{\text{KL}}(\hat{p} \,\|\, q_\theta)"),
    para(rt("For one-hot labels per example, the empirical entropy "), eq(r"H(\hat{p}) = 0"), rt(", so "),
        eq(r"D_{\text{KL}} = \mathcal{L}_{CE}"), rt(" directly.")),
    heading3("Full Gradient Derivation (Batch)"),
    para(rt("The batch gradient with respect to parameters "), eq(r"W"), rt(" is:")),
    equation_block(r"\frac{\partial \mathcal{L}}{\partial W} = \frac{1}{N} \sum_{i=1}^N (\hat{q}_i - y_i) h_i^\top"),
    para(rt("where "), eq(r"h_i"), rt(" is the penultimate-layer representation and "), eq(r"\hat{q}_i - y_i"),
        rt(" is the per-example error signal.")),
    heading3("Label Smoothing (Regularized Version)"),
    para(rt("Replace one-hot "), eq(r"y"), rt(" with smoothed target "), eq(r"\tilde{y}_k = (1-\varepsilon)y_k + \varepsilon/K"),
        rt(". This replaces minimizing KL to a one-hot with minimizing KL to a softer distribution:")),
    equation_block(r"\mathcal{L}_{LS} = -(1-\varepsilon)\log \hat{q}_{k^*} - \frac{\varepsilon}{K}\sum_{k=1}^K \log \hat{q}_k"),
    callout("⚠️", rt("Common Misconception: ", bold=True),
            rt("A low CE loss does NOT imply a calibrated model. CE loss is minimized when predicted probabilities match "
               "class frequencies in training data, but the model may still be poorly calibrated on the test distribution. "
               "Post-hoc calibration (Platt scaling, temperature scaling) is needed separately.")),
    divider(),

    # ── Section 6: Code ────────────────────────────────────────────────────────
    heading2("💻 Code Implementation"),
    heading3("6a — From Scratch (NumPy)"),
    code_block("python", """\
import numpy as np

def softmax(z):
    \"\"\"Numerically stable softmax.\"\"\"
    z = np.asarray(z, dtype=float)
    z = z - z.max(axis=-1, keepdims=True)   # subtract max for stability
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)

def cross_entropy_loss(logits, labels):
    \"\"\"
    Cross-entropy loss for multi-class classification.

    Args:
        logits: (N, K) array of raw logits
        labels: (N,)  array of integer class indices
    Returns:
        scalar average CE loss
    \"\"\"
    N = logits.shape[0]
    q = softmax(logits)                     # (N, K) probabilities
    # Pick the probability assigned to the true class for each example
    q_true = q[np.arange(N), labels]       # (N,)
    loss = -np.log(np.maximum(q_true, 1e-15))  # clip for safety
    return loss.mean()

def softmax_ce_gradient(logits, labels):
    \"\"\"
    Gradient of CE loss w.r.t. logits: dL/dz = q_hat - y
    This combines the softmax Jacobian and CE gradient analytically.

    Returns: (N, K) gradient array
    \"\"\"
    N, K = logits.shape
    q = softmax(logits)
    # Build one-hot matrix
    y = np.zeros_like(q)
    y[np.arange(N), labels] = 1.0
    return (q - y) / N     # average over batch

# ----- Example -----
logits = np.array([[2.1, 0.8, -0.5],
                   [-0.3, 1.5, 0.2]])
labels = np.array([0, 1])

loss = cross_entropy_loss(logits, labels)
grad = softmax_ce_gradient(logits, labels)

print(f"Loss: {loss:.4f}")          # 0.3304
print(f"Gradient:\\n{grad}")        # [[−0.1288, 0.1012, 0.0276], ...]
\
"""),
    heading3("6b — Production Usage (PyTorch)"),
    code_block("python", """\
import torch
import torch.nn as nn
import torch.nn.functional as F

# ── Standard cross-entropy (CORRECT way) ──────────────────────────────────────
# nn.CrossEntropyLoss = log_softmax + nll_loss in one numerically stable step
loss_fn = nn.CrossEntropyLoss()

logits = torch.tensor([[2.1, 0.8, -0.5],
                        [-0.3, 1.5, 0.2]])
labels = torch.tensor([0, 1])

loss = loss_fn(logits, labels)
print(f"Loss: {loss.item():.4f}")   # 0.3304

# ── ⚠️ GOTCHA: Do NOT softmax before CrossEntropyLoss ────────────────────────
probs = F.softmax(logits, dim=-1)
# loss_fn(probs, labels)  ← WRONG! Applies softmax again on top of probabilities

# ── Label smoothing (PyTorch 1.10+) ─────────────────────────────────────────
loss_fn_smooth = nn.CrossEntropyLoss(label_smoothing=0.1)
loss_smooth = loss_fn_smooth(logits, labels)

# ── Class weights for imbalanced data ────────────────────────────────────────
weights = torch.tensor([1.0, 2.0, 0.5])   # up-weight class 1
loss_fn_weighted = nn.CrossEntropyLoss(weight=weights)
loss_weighted = loss_fn_weighted(logits, labels)

# ── Manual: equivalent to CrossEntropyLoss ───────────────────────────────────
log_probs = F.log_softmax(logits, dim=-1)
loss_manual = F.nll_loss(log_probs, labels)

# ── Binary classification (sigmoid + BCE) ────────────────────────────────────
binary_logits = torch.tensor([1.5, -0.3])
binary_labels = torch.tensor([1.0, 0.0])
bce = F.binary_cross_entropy_with_logits(binary_logits, binary_labels)
\
"""),
    callout("💡", rt("Performance tip: ", bold=True),
            rt("Use F.cross_entropy (functional) or nn.CrossEntropyLoss — both use the log-sum-exp trick internally "
               "and are implemented in C++/CUDA. Never manually compute softmax then log for training losses.")),
    divider(),

    # ── Section 7: Interview Deep-Dive ────────────────────────────────────────
    heading2("🎤 Interview Deep-Dive"),
    heading3("Q1 (Easy): Why do we use cross-entropy loss instead of MSE for classification?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("MSE treats the output as a vector of real numbers. For softmax outputs, MSE gradients saturate "
                "when probabilities are near 0 or 1, producing vanishing learning signals. Cross-entropy loss has "
                "gradient "), eq(r"\hat{q} - y"), rt(", which is non-zero as long as the model is wrong. "
                "Additionally, CE has a direct probabilistic interpretation (MLE under a categorical model) while MSE does not.")),
    ]),
    heading3("Q2 (Easy): What does the CE loss return when the model is perfectly correct?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("If the model assigns probability 1 to the correct class: "), eq(r"\mathcal{L}_{CE} = -\log(1) = 0"), rt(". "
                "In practice, softmax never outputs exactly 1 (it's a ratio of exponentials), so the loss is always slightly positive.")),
    ]),
    heading3("Q3 (Medium): Explain why minimizing CE is equivalent to MLE."),
    toggle([rt("Answer", bold=True)], [
        para(rt("Under a categorical model parameterized by "), eq(r"\theta"), rt(", the probability of observing label "),
            eq(r"y_i"), rt(" given "), eq(r"x_i"), rt(" is "), eq(r"q_\theta(y_i \mid x_i)"), rt(". "
                "The log-likelihood is "), eq(r"\ell = \frac{1}{N}\sum_i \log q_\theta(y_i \mid x_i)"), rt(". "
                "The CE loss is "), eq(r"\mathcal{L}_{CE} = -\ell"), rt(". Minimizing CE is literally maximizing the log-likelihood.")),
    ]),
    heading3("Q4 (Medium): What is the gradient of CE loss w.r.t. logits, and why is it clean?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("The gradient is "), eq(r"\partial \mathcal{L} / \partial z_k = \hat{q}_k - y_k"), rt(". "
                "This is clean because the softmax Jacobian and the CE gradient chain-rule together to cancel terms. "
                "The softmax Jacobian is "), eq(r"J_{ij} = \hat{q}_i(\delta_{ij} - \hat{q}_j)"), rt(", and the CE gradient "
                "w.r.t. probabilities is "), eq(r"-y_k/\hat{q}_k"), rt(". Multiplying them collapses to "), eq(r"\hat{q} - y"), rt(".")),
    ]),
    heading3("Q5 (Hard): What is the connection between CE loss and KL divergence?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Let "), eq(r"\hat{p}"), rt(" be the empirical distribution (uniform mixture of one-hot points). Then "),
            eq(r"\mathcal{L}_{CE} = H(\hat{p}, q_\theta)"), rt(" (cross-entropy). Using the identity "),
            eq(r"H(p,q) = H(p) + D_{\text{KL}}(p \| q)"), rt(": minimizing CE minimizes "),
            eq(r"D_{\text{KL}}(\hat{p} \| q_\theta)"), rt(" because "), eq(r"H(\hat{p})"), rt(" is constant. "
                "For one-hot labels, "), eq(r"H(\hat{p}) = 0"), rt(", so CE = KL directly.")),
    ]),
    heading3("Q6 (Hard): Why does label smoothing help, and what KL does it minimize?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("Hard one-hot labels push CE loss to drive "), eq(r"\hat{q}_{k^*} \to 1"), rt(", making the model "
                "overconfident. Label smoothing replaces the one-hot with "),
            eq(r"\tilde{y}_k = (1-\varepsilon)\delta_{k,k^*} + \varepsilon/K"), rt(". This is equivalent to "
                "minimizing KL to the smoothed distribution rather than the point mass. The model can no longer "
                "achieve zero loss, preventing logit explosion and improving calibration.")),
    ]),
    heading3("Q7 (Hard, PhD): Is cross-entropy consistent? What does it converge to?"),
    toggle([rt("Answer", bold=True)], [
        para(rt("As "), eq(r"N \to \infty"), rt(", minimizing CE over the training set converges to minimizing the "
                "population cross-entropy "), eq(r"H(p^*(y \mid x), q_\theta(y \mid x))"),
            rt(" where "), eq(r"p^*"), rt(" is the true conditional distribution. If "),
            eq(r"q_\theta"), rt(" is correctly specified (true conditional is in the model class), "
                "the MLE estimate is consistent and asymptotically efficient (Cramér-Rao bound is achieved). "
                "In the misspecified case, MLE converges to the minimum-KL-divergence point in the model class.")),
    ]),
    callout("🚩", rt("Red Flags: ", bold=True),
            rt("'CE loss is just for probabilistic outputs' — wrong, it's the standard for any softmax classification. "
               "'MSE is fine for classification' — wrong, saturating gradients. "
               "'CE loss ensures calibration' — wrong, calibration requires additional post-hoc methods.")),
    divider(),

    # ── Section 8: Comparison ─────────────────────────────────────────────────
    heading2("⚖️ Comparison & Trade-offs"),
    table(4,
          table_row(["Loss Function", "When to Use", "Pros", "Cons"]),
          table_row(["CE Loss (softmax)", "Multi-class, 1 label/example", "MLE, clean gradient q-y", "Ignores margin"]),
          table_row(["Focal Loss", "Imbalanced classes (object det.)", "Down-weights easy examples", "Extra hyperparameter gamma"]),
          table_row(["Hinge Loss", "SVM-style classifiers", "Max-margin guarantee", "Not probabilistic; flat far from boundary"]),
          table_row(["MSE on logits", "Regression (not classification)", "Simple", "Saturating gradients for classification"]),
          table_row(["Label Smoothing CE", "Overconfidence concern", "Better calibration", "Slight accuracy trade-off"]),
          table_row(["Binary CE (BCE)", "Binary or multi-label", "MLE for Bernoulli model", "Needs sigmoid not softmax"]),
    ),
    callout("🎯", rt("Decision guide: ", bold=True),
            rt("Multi-class, single label → softmax + CE. "
               "Binary or multi-label → sigmoid + BCE. "
               "Severe class imbalance → focal loss (γ=2) or weighted CE. "
               "Want better calibration → label smoothing (ε=0.1) or post-hoc temperature scaling.")),
    divider(),

    # ── Section 9: Interactive Visual Explainer ────────────────────────────────
    heading2("🎯 Interactive Visual Explainer"),
    embed(EXPLAINER_URL),
    para(rt("Step through the softmax → CE → MLE → KL pipeline visually — use Next/Prev or arrow keys.", italic=True, color="gray")),
    divider(),

    # ── Section 10: Related Topics ─────────────────────────────────────────────
    heading2("🔗 Related Topics & Further Reading"),
    heading3("Prerequisites"),
    bullet(rt("Shannon Entropy — the information-theoretic foundation (Section 4.1)")),
    bullet(rt("KL Divergence — asymmetric divergence CE is built on (Section 4.2)")),
    bullet(rt("Softmax Function — the probability normalizer (Part IV: Neural Networks)")),
    bullet(rt("Maximum Likelihood Estimation — the statistical framework (Part I: Stats)")),
    heading3("What to Learn Next"),
    bullet(rt("Focal Loss — CE variant for class imbalance (Lin et al., 2017)")),
    bullet(rt("Temperature Scaling & Calibration — post-hoc calibration of CE-trained models")),
    bullet(rt("Label Smoothing — regularized CE with softer targets")),
    bullet(rt("Mutual Information — generalizes CE to representations (InfoNCE, CPC)")),
    heading3("Key Papers"),
    bullet(rt("Rumelhart, Hinton & Williams (1986). Learning representations by back-propagating errors. Nature.")),
    bullet(rt("Bridle (1990). Probabilistic Interpretation of Feedforward Network Outputs. NIPS.")),
    bullet(rt("Szegedy et al. (2016). Rethinking Inception (introduced label smoothing). CVPR.")),
    bullet(rt("Lin et al. (2017). Focal Loss for Dense Object Detection. ICCV.")),
    bullet(rt("Guo et al. (2017). On Calibration of Modern Neural Networks. ICML.")),
    heading3("Best Resources"),
    bullet(rt("Bishop, PRML (2006), Chapter 4: Linear Models for Classification — full probabilistic derivation")),
    bullet(rt("Goodfellow, Deep Learning (2016), Chapter 6.2.2.3: Softmax and CE loss")),
    bullet(rt("CS231n Lecture 3 (Karpathy) — loss functions, CE gradient derivation from scratch")),
    bullet(rt("Information Theory, Inference, and Learning Algorithms — MacKay, Chapter 2")),
    callout("🔗", rt("This topic connects to: ", bold=True),
            rt("Shannon Entropy (4.1), KL Divergence (4.2), Logistic Regression, Softmax, "
               "MLE, Bayesian Inference, Focal Loss, Label Smoothing, Temperature Scaling, InfoNCE / CPC.")),
]

update_page(PAGE_ID, ICON, PROPERTIES, blocks)
