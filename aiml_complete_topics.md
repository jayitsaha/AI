# AI / ML / Data Science — Complete Topic Compendium

> **Merged from:** `ai_ml_roadmap.docx` and `aiml_mastery_bible.docx`
>
> | Source | Topic Count |
> |---|---|
> | AI/ML Roadmap | **1305** |
> | AI/ML Mastery Bible | **1229** |
> | **Merged (deduplicated)** | **2040** |
> | Duplicates removed | 494 |

---

## Table of Contents

1. [PART I: MATHEMATICAL & STATISTICAL FOUNDATIONS](#part-i-mathematical-statistical-foundations) — 280 topics
2. [PART II: PROGRAMMING, DATA & SOFTWARE ENGINEERING](#part-ii-programming-data-software-engineering) — 67 topics
3. [PART III: CLASSICAL MACHINE LEARNING](#part-iii-classical-machine-learning) — 268 topics
4. [PART IV: DEEP LEARNING FOUNDATIONS](#part-iv-deep-learning-foundations) — 91 topics
5. [PART V: CONVOLUTIONAL NEURAL NETWORKS & COMPUTER VISION](#part-v-convolutional-neural-networks-computer-vision) — 157 topics
6. [PART VI: SEQUENCE MODELS, TRANSFORMERS & NLP](#part-vi-sequence-models-transformers-nlp) — 170 topics
7. [PART VII: GENERATIVE MODELS](#part-vii-generative-models) — 78 topics
8. [PART VIII: LARGE LANGUAGE MODELS & GENERATIVE AI](#part-viii-large-language-models-generative-ai) — 169 topics
9. [PART IX: MULTIMODAL AI](#part-ix-multimodal-ai) — 94 topics
10. [PART X: RECOMMENDATION SYSTEMS](#part-x-recommendation-systems) — 123 topics
11. [PART XI: REINFORCEMENT LEARNING](#part-xi-reinforcement-learning) — 71 topics
12. [PART XII: GRAPH NEURAL NETWORKS](#part-xii-graph-neural-networks) — 34 topics
13. [PART XIII: TIME SERIES & FORECASTING](#part-xiii-time-series-forecasting) — 28 topics
14. [PART XIV: PROBABILISTIC ML & BAYESIAN METHODS](#part-xiv-probabilistic-ml-bayesian-methods) — 25 topics
15. [PART XV: SPEECH, AUDIO & MULTIMODAL](#part-xv-speech-audio-multimodal) — 25 topics
16. [PART XVI: MLOps & PRODUCTION ML](#part-xvi-mlops-production-ml) — 86 topics
17. [PART XVII: ML SYSTEM DESIGN](#part-xvii-ml-system-design) — 45 topics
18. [PART XVIII: RESPONSIBLE AI, SAFETY & ETHICS](#part-xviii-responsible-ai-safety-ethics) — 63 topics
19. [PART XIX: SPECIALIZED & EMERGING TOPICS](#part-xix-specialized-emerging-topics) — 152 topics
20. [PART XX: ROBOTICS & EMBODIED AI (Overview)](#part-xx-robotics-embodied-ai-overview) — 14 topics

---

## PART I: MATHEMATICAL & STATISTICAL FOUNDATIONS

### 1. Linear Algebra

#### 1.1 Scalars, Vectors, Matrices & Tensors

- [ ] Scalar operations & fields (real, complex)
- [ ] Vector spaces, subspaces, span & basis
- [ ] Linear independence & dimension
- [ ] Matrix types: square, symmetric, diagonal, identity, orthogonal, unitary, Hermitian, positive-definite, positive-semidefinite, sparse, Toeplitz, Hankel, Vandermonde, band matrices
- [ ] Tensor notation & order (0th–Nth order tensors)
- [ ] Einstein summation convention
- [ ] Outer product, Kronecker product, Hadamard (element-wise) product
- [ ] Tensor contraction & reshaping
- [ ] Block matrices & Schur complement

#### 1.2 Matrix Operations & Properties

- [ ] Matrix addition, scalar multiplication, transposition
- [ ] Matrix multiplication & computational complexity (O(n³), Strassen O(n^2.807))
- [ ] Trace: properties, cyclic permutation, relation to eigenvalues
- [ ] Determinant: cofactor expansion, geometric interpretation (signed volume), properties
- [ ] Matrix inverse: existence conditions, computation via Gauss-Jordan, adjugate method
- [ ] Pseudo-inverse (Moore-Penrose): definition, computation, applications in least squares
- [ ] Matrix rank: row rank, column rank, rank-nullity theorem
- [ ] Null space (kernel) & column space (range/image)
- [ ] Row echelon form, reduced row echelon form (RREF)
- [ ] LU decomposition, LDL decomposition
- [ ] Cholesky decomposition (for positive-definite matrices)
- [ ] QR decomposition (Gram-Schmidt, Householder, Givens rotations)
- [ ] Matrix norms: Frobenius, spectral (operator), nuclear, L1, L∞
- [ ] Condition number & numerical stability

#### 1.3 Eigendecomposition & Spectral Theory

- [ ] Eigenvalues & eigenvectors: definition, characteristic polynomial
- [ ] Eigendecomposition: A = PDP⁻¹
- [ ] Spectral theorem for symmetric/Hermitian matrices
- [ ] Diagonalization: conditions, geometric vs algebraic multiplicity
- [ ] Power method for dominant eigenvalue
- [ ] Rayleigh quotient
- [ ] Gershgorin circle theorem
- [ ] Eigenvalue perturbation theory
- [ ] Applications: PCA, PageRank, Markov chains, vibrational modes

#### 1.4 Singular Value Decomposition (SVD)

- [ ] Full SVD: A = UΣVᵀ
- [ ] Compact/truncated/economy SVD
- [ ] Relationship between SVD & eigendecomposition (AᵀA, AAᵀ)
- [ ] Low-rank approximation & Eckart-Young theorem
- [ ] Applications: dimensionality reduction, matrix completion, image compression, latent semantic analysis, pseudoinverse computation
- [ ] Numerical computation of SVD (Golub-Kahan bidiagonalization)
- [ ] Randomized SVD for large matrices

#### 1.5 Vector Calculus & Matrix Calculus

- [ ] Gradient of scalar functions w.r.t. vectors
- [ ] Jacobian matrix: definition, chain rule for vector-valued functions
- [ ] Hessian matrix: second-order derivatives, role in optimization
- [ ] Matrix derivatives: ∂(Ax)/∂x, ∂(xᵀAx)/∂x, ∂tr(AB)/∂A
- [ ] Vector-Jacobian products (VJP) & Jacobian-vector products (JVP)
- [ ] Automatic differentiation: forward mode vs reverse mode (backprop)
- [ ] Kronecker product in matrix calculus
- [ ] Taylor expansion in matrix form

#### 1.6 Advanced Linear Algebra for ML

- [ ] Positive-definite matrices: tests, Cholesky, kernel matrices
- [ ] Matrix exponential & logarithm
- [ ] Cayley-Hamilton theorem
- [ ] Jordan normal form
- [ ] Linear transformations: rotation, reflection, projection, shear
- [ ] Projection matrices & orthogonal projections
- [ ] Gram matrices & kernel trick connection
- [ ] Rayleigh-Ritz method
- [ ] Nonnegative matrix factorization (NMF)
- [ ] Tensor decompositions: CP (CANDECOMP/PARAFAC), Tucker, tensor-train
- [ ] Random matrix theory basics (Marchenko-Pastur distribution)

### 2. Calculus & Analysis

#### 2.1 Single-Variable Calculus

- [ ] Limits, continuity, differentiability
- [ ] Derivatives: product rule, quotient rule, chain rule
- [ ] Common derivatives: polynomials, exponentials, logarithms, trigonometric, hyperbolic (tanh, sigmoid)
- [ ] Mean value theorem, L'Hôpital's rule
- [ ] Taylor series & Maclaurin series, remainder terms
- [ ] Integration: Riemann, fundamental theorem of calculus
- [ ] Integration techniques: substitution, by parts, partial fractions
- [ ] Improper integrals & convergence

#### 2.2 Multivariable Calculus

- [ ] Partial derivatives & total derivative
- [ ] Gradient: direction of steepest ascent, gradient fields
- [ ] Directional derivatives
- [ ] Hessian matrix & second derivative test for local extrema
- [ ] Chain rule for multivariable functions
- [ ] Implicit function theorem
- [ ] Multiple integrals (double, triple), change of variables (Jacobian determinant)
- [ ] Line integrals, surface integrals
- [ ] Divergence, curl, Laplacian
- [ ] Green's theorem, Stokes' theorem, Divergence theorem (overview)

#### 2.3 Optimization-Relevant Calculus

- [ ] Convexity of functions: definition, first-order & second-order conditions
- [ ] Constrained optimization: Lagrange multipliers, KKT conditions
- [ ] Saddle points & how they affect optimization in high dimensions
- [ ] Lipschitz continuity & smoothness
- [ ] Functional derivatives (variational calculus basics)

#### 2.4 Integral Transforms & Special Functions

- [ ] Fourier transform & inverse Fourier transform
- [ ] Discrete Fourier Transform (DFT) & Fast Fourier Transform (FFT)
- [ ] Laplace transform (overview for control theory / RL)
- [ ] Convolution theorem
- [ ] Gamma function, Beta function
- [ ] Softmax function as a continuous approximation of argmax

### 3. Probability & Statistics

#### 3.1 Probability Foundations

- [ ] Sample space, events, axioms of probability (Kolmogorov)
- [ ] Conditional probability & Bayes' theorem
- [ ] Law of total probability
- [ ] Independence & conditional independence
- [ ] Combinatorics: permutations, combinations, multinomial coefficients
- [ ] Inclusion-exclusion principle

#### 3.2 Random Variables & Distributions

- [ ] Discrete random variables: PMF, CDF
- [ ] Continuous random variables: PDF, CDF
- [ ] Joint distributions, marginal distributions, conditional distributions
- [ ] Discrete distributions: Bernoulli, Binomial, Multinomial, Poisson, Geometric, Negative Binomial, Hypergeometric, Categorical
- [ ] Continuous distributions: Uniform, Gaussian (Normal), Multivariate Normal, Exponential, Gamma, Beta, Chi-squared, Student's t, F-distribution, Cauchy, Laplace, Log-normal, Weibull, Pareto, Dirichlet
- [ ] Mixture distributions & Gaussian mixture models
- [ ] Exponential family of distributions: canonical form, sufficient statistics, natural parameters
- [ ] Conjugate priors

#### 3.3 Expectation, Variance & Moments

- [ ] Expected value: linearity, law of the unconscious statistician (LOTUS)
- [ ] Variance, standard deviation, covariance, correlation
- [ ] Covariance matrix & its properties
- [ ] Moment generating functions (MGF) & characteristic functions
- [ ] Skewness & kurtosis
- [ ] Conditional expectation & law of iterated expectations (tower property)

#### 3.4 Limit Theorems & Convergence

- [ ] Law of large numbers (weak & strong)
- [ ] Central limit theorem (CLT) & its variants
- [ ] Convergence: in probability, in distribution, almost sure, in Lp
- [ ] Delta method
- [ ] Hoeffding's inequality, Chebyshev's inequality, Markov's inequality
- [ ] Concentration inequalities (McDiarmid, Bernstein, Chernoff bounds)

#### 3.5 Statistical Estimation

- [ ] Point estimation: bias, variance, MSE, consistency, efficiency
- [ ] Maximum Likelihood Estimation (MLE): derivation, properties, asymptotic normality
- [ ] Maximum A Posteriori (MAP) estimation
- [ ] Method of moments
- [ ] Sufficient statistics & Fisher-Neyman factorization
- [ ] Cramér-Rao lower bound & Fisher information
- [ ] Rao-Blackwell theorem
- [ ] EM algorithm: E-step, M-step, convergence, applications (GMM, missing data)

#### 3.6 Hypothesis Testing & Confidence Intervals

- [ ] Null & alternative hypotheses, test statistic, p-value
- [ ] Type I error (α), Type II error (β), power of a test
- [ ] z-test, t-test (one-sample, two-sample, paired)
- [ ] Chi-squared test (goodness of fit, independence)
- [ ] F-test, ANOVA (one-way, two-way)
- [ ] Multiple comparisons problem: Bonferroni correction, Holm-Bonferroni, Benjamini-Hochberg (FDR)
- [ ] Likelihood ratio test, Wald test, Score test
- [ ] Non-parametric tests: Mann-Whitney U, Wilcoxon signed-rank, Kruskal-Wallis, Kolmogorov-Smirnov, permutation tests
- [ ] Confidence intervals: construction, interpretation, bootstrap CI
- [ ] A/B testing: sample size calculation, sequential testing, multi-armed bandits for experimentation

#### 3.7 Bayesian Statistics

- [ ] Prior, likelihood, posterior, evidence (marginal likelihood)
- [ ] Conjugate priors for common distributions
- [ ] Bayesian updating & sequential analysis
- [ ] Credible intervals vs confidence intervals
- [ ] Bayesian model comparison: Bayes factors, BIC
- [ ] Empirical Bayes
- [ ] Hierarchical / multilevel Bayesian models
- [ ] Non-informative & weakly informative priors (Jeffreys prior)

#### 3.8 Stochastic Processes (Foundations)

- [ ] Markov chains: transition matrix, stationary distribution, ergodicity, detailed balance
- [ ] Poisson process
- [ ] Random walks
- [ ] Martingales (basic definition)
- [ ] Brownian motion / Wiener process (overview)
- [ ] Hidden Markov Models (HMMs): forward-backward algorithm, Viterbi, Baum-Welch

### 4. Information Theory

#### 4.1 Core Concepts

- [ ] Entropy: Shannon entropy H(X), interpretation as uncertainty/information content
- [ ] Joint entropy H(X,Y), conditional entropy H(X|Y)
- [ ] Chain rule of entropy
- [ ] Mutual information I(X;Y): definition, properties, relation to entropy
- [ ] Conditional mutual information
- [ ] KL divergence (relative entropy): definition, asymmetry, non-negativity (Gibbs' inequality)
- [ ] Forward KL vs reverse KL: mode-covering vs mode-seeking behaviour
- [ ] Cross-entropy: definition, relation to KL divergence, use as loss function
- [ ] Jensen-Shannon divergence (JSD)
- [ ] f-divergences (general family)

#### 4.2 Information Theory in ML

- [ ] Cross-entropy loss for classification (connection to MLE)
- [ ] Mutual information in feature selection & representation learning
- [ ] Information bottleneck method
- [ ] Minimum description length (MDL) principle
- [ ] Data processing inequality
- [ ] Rate-distortion theory (overview)
- [ ] Variational bounds & ELBO (connection to VAEs)
- [ ] Entropy regularization in RL (SAC, maximum entropy RL)
- [ ] Bits-back coding & compression-based ML

### 5. Optimization Theory

#### 5.1 Convex Optimization

- [ ] Convex sets, convex functions, strict/strong convexity
- [ ] First-order conditions (gradient = 0), second-order conditions (Hessian PSD)
- [ ] Local vs global optima in convex vs non-convex settings
- [ ] Linear programming (LP): simplex method, duality
- [ ] Quadratic programming (QP)
- [ ] Semidefinite programming (SDP)
- [ ] Conic optimization
- [ ] Lagrangian duality: weak duality, strong duality, Slater's condition
- [ ] KKT conditions: primal feasibility, dual feasibility, complementary slackness

#### 5.2 Gradient-Based Optimization

- [ ] Gradient descent: batch, mini-batch, stochastic (SGD)
- [ ] Learning rate: fixed, decaying, warmup, cyclical, cosine annealing, 1cycle
- [ ] Momentum: classical momentum, Nesterov accelerated gradient (NAG)
- [ ] Adaptive learning rate methods: AdaGrad, RMSProp, AdaDelta, Adam, AdamW, Nadam, RAdam, LAMB, LARS
- [ ] Weight decay vs L2 regularization (decoupled weight decay)
- [ ] Gradient clipping: by value, by norm
- [ ] Learning rate warmup strategies
- [ ] Polyak averaging / exponential moving average (EMA) of weights
- [ ] Lookahead optimizer
- [ ] Sharpness-Aware Minimization (SAM)
- [ ] Lion optimizer

#### 5.3 Second-Order & Advanced Methods

- [ ] Newton's method & quasi-Newton methods (BFGS, L-BFGS)
- [ ] Natural gradient descent & Fisher information matrix
- [ ] Conjugate gradient method
- [ ] Proximal gradient methods (ISTA, FISTA)
- [ ] Mirror descent
- [ ] Frank-Wolfe (conditional gradient) method
- [ ] ADMM (Alternating Direction Method of Multipliers)

#### 5.4 Non-Convex Optimization in Deep Learning

- [ ] Loss landscape of neural networks: saddle points, local minima, plateaus
- [ ] Sharp vs flat minima & generalization
- [ ] Batch size effects on optimization & generalization
- [ ] Gradient noise as implicit regularization
- [ ] Loss surface visualization techniques
- [ ] Lottery ticket hypothesis
- [ ] Mode connectivity & loss landscape topology

#### 5.5 Constrained & Black-Box Optimization

- [ ] Penalty methods, barrier methods, augmented Lagrangian
- [ ] Projected gradient descent
- [ ] Gradient-free / derivative-free optimization: Nelder-Mead, CMA-ES, simulated annealing
- [ ] Evolutionary algorithms: genetic algorithms, differential evolution
- [ ] Bayesian optimization: surrogate models (GP), acquisition functions (EI, UCB, PI, Thompson sampling)
- [ ] Multi-objective optimization: Pareto front, NSGA-II

### 6. Discrete Mathematics & Graph Theory

#### 6.1 Discrete Math Essentials

- [ ] Set theory, relations, functions
- [ ] Logic: propositional, first-order (relevant to neuro-symbolic AI)
- [ ] Combinatorics for counting arguments in ML
- [ ] Computational complexity: O, Ω, Θ, P, NP, NP-hard (relevant to algorithm selection)

#### 6.2 Graph Theory

- [ ] Graphs: directed, undirected, weighted, bipartite, DAG
- [ ] Adjacency matrix, Laplacian matrix, incidence matrix
- [ ] Graph traversal: BFS, DFS
- [ ] Shortest paths: Dijkstra, Bellman-Ford
- [ ] Minimum spanning tree: Kruskal, Prim
- [ ] Graph connectivity, components, cliques
- [ ] Spectral graph theory: graph Laplacian eigenvalues, Cheeger inequality, spectral clustering connection
- [ ] Random graphs: Erdős-Rényi, Barabási-Albert (scale-free), small-world networks
- [ ] PageRank algorithm
- [ ] Graph isomorphism & the Weisfeiler-Leman test (WL test for GNNs)

### 0.1 Linear Algebra

#### 0.1.1 Vectors & Vector Spaces

- [ ] Vector definition, notation, geometric interpretation
- [ ] Cross product (geometric meaning)
- [ ] Norms: L0, L1, L2, L∞ and their ML implications
- [ ] Subspaces, column space, null space, row space
- [ ] Orthogonality, orthonormal basis

#### 0.1.2 Matrices

- [ ] Matrix operations: addition, multiplication, transpose
- [ ] Matrix rank, invertibility, determinant

#### 0.1.3 Eigendecomposition & Spectral Theory

- [ ] Eigenvalues & eigenvectors — definition and geometric intuition
- [ ] Power iteration method
- [ ] Applications: PCA, graph Laplacians, Markov chains

#### 0.1.4 Singular Value Decomposition (SVD)

- [ ] Full SVD, economy SVD
- [ ] SVD in recommendation systems (matrix factorization)
- [ ] Truncated SVD for dimensionality reduction

#### 0.1.5 Matrix Calculus

- [ ] Gradient w.r.t. matrix parameters
- [ ] Backpropagation as matrix calculus
- [ ] Numerator vs denominator layout conventions

#### 0.1.6 Tensors

- [ ] Tensor definition and rank
- [ ] Tensor operations: contraction, outer product
- [ ] Einstein summation notation
- [ ] Broadcasting semantics
- [ ] Applications in deep learning (weight tensors)

### 0.2 Calculus & Optimization

#### 0.2.1 Multivariable Calculus

- [ ] Partial derivatives, gradient
- [ ] Taylor series expansion (scalar and vector forms)

#### 0.2.2 Convexity

- [ ] Jensen's inequality
- [ ] Quasiconvex, strongly convex functions
- [ ] Convex optimization: global optima guarantee
- [ ] Non-convex landscapes in deep learning
- [ ] Saddle points, local minima, flat regions

#### 0.2.3 Gradient Descent Family

- [ ] Gradient descent (GD): update rule, convergence
- [ ] Mini-batch SGD: batch size trade-offs
- [ ] AdaGrad: per-parameter learning rates
- [ ] RMSProp: exponential moving average of squared gradients
- [ ] Adam: adaptive moment estimation, β1, β2, ε
- [ ] Adadelta, Nadam, Lion, Sophia
- [ ] Convergence rates: O(1/k) vs O(1/k²)

#### 0.2.4 Second-Order Methods

- [ ] Newton's method and Hessian computation
- [ ] K-FAC (Kronecker-factored approximate curvature)

#### 0.2.5 Lagrangian & Constrained Optimization

- [ ] Primal and dual problems
- [ ] Applications: SVM dual formulation

### 0.3 Probability & Statistics

#### 0.3.1 Probability Theory

- [ ] Probability density functions (PDF) and cumulative distribution functions (CDF)

#### 0.3.2 Key Distributions

- [ ] Poisson distribution
- [ ] Gaussian (Normal): properties, MGF
- [ ] Multivariate Gaussian: mean vector, covariance matrix, Mahalanobis distance
- [ ] Beta distribution (conjugate prior for Bernoulli)
- [ ] Dirichlet distribution (conjugate prior for Multinomial)
- [ ] Categorical distribution

#### 0.3.3 Expectation & Moments

- [ ] Chernoff bounds, Hoeffding's inequality

#### 0.3.4 Information Theory

- [ ] Entropy (Shannon entropy): definition and intuition
- [ ] Kullback-Leibler (KL) divergence: non-symmetry, uses in ML
- [ ] Differential entropy (continuous distributions)

#### 0.3.5 Bayesian Statistics

- [ ] Bayesian inference vs frequentist

#### 0.3.6 Hypothesis Testing & Statistical Inference

- [ ] Null hypothesis, alternative hypothesis
- [ ] p-value definition and misinterpretation
- [ ] ANOVA
- [ ] Multiple testing: Bonferroni correction, FDR, BH procedure
- [ ] A/B testing design: sample size, significance, effect size

### 0.4 Information & Complexity Theory

- [ ] Big-O notation, asymptotic analysis
- [ ] Time and space complexity
- [ ] NP-hardness, NP-completeness
- [ ] VC dimension and PAC learnability
- [ ] Rademacher complexity
- [ ] Bias-complexity trade-off

---

## PART II: PROGRAMMING, DATA & SOFTWARE ENGINEERING

### 7. Python for Data Science & ML

#### 7.1 Core Python

- [ ] Data types, control flow, functions, classes, decorators, generators, iterators
- [ ] List comprehensions, dictionary comprehensions, lambda functions
- [ ] Exception handling, context managers
- [ ] Type hints & static analysis (mypy)
- [ ] Concurrency: threading, multiprocessing, asyncio
- [ ] Memory management: garbage collection, reference counting, weak references
- [ ] Profiling & optimization: cProfile, line_profiler, memory_profiler

#### 7.2 Scientific Python Stack

- [ ] NumPy: ndarray, broadcasting, vectorization, ufuncs, structured arrays, memory layout (C vs Fortran order), advanced indexing
- [ ] Pandas: DataFrame, Series, groupby, merge/join, pivot tables, window functions, categorical data, MultiIndex, method chaining, .pipe()
- [ ] SciPy: sparse matrices, optimization (minimize), interpolation, signal processing, spatial (KD-tree)
- [ ] Matplotlib & Seaborn: figure/axes model, customization, statistical plots
- [ ] Plotly & interactive visualization

#### 7.3 ML/DL Frameworks

- [ ] Scikit-learn: estimator API, pipelines, custom transformers, ColumnTransformer, cross-validation strategies, grid/random search
- [ ] PyTorch: tensors, autograd, nn.Module, DataLoader, custom datasets, hooks, mixed precision (AMP), distributed training (DDP, FSDP), TorchScript, torch.compile
- [ ] TensorFlow / Keras: tf.data, tf.function, SavedModel, TF Lite, TF Serving
- [ ] JAX: functional transformations (jit, grad, vmap, pmap), Flax/Haiku
- [ ] Hugging Face ecosystem: transformers, datasets, tokenizers, accelerate, PEFT, TRL

#### 7.4 Software Engineering for ML

- [ ] Version control: Git, branching strategies, Git LFS for large files
- [ ] Testing: unit tests (pytest), integration tests, property-based testing (Hypothesis)
- [ ] Code quality: linting (ruff, flake8), formatting (black), type checking
- [ ] Documentation: docstrings (NumPy/Google style), Sphinx
- [ ] Package management: pip, conda, poetry, virtual environments
- [ ] Design patterns relevant to ML: strategy, factory, observer, decorator
- [ ] Reproducibility: random seeds, deterministic algorithms, environment pinning

### 8. Data Engineering & Preprocessing

#### 8.1 Data Collection & Storage

- [ ] Data sources: APIs, web scraping (BeautifulSoup, Scrapy), databases, data lakes
- [ ] SQL fundamentals: joins, aggregations, window functions, CTEs, query optimization
- [ ] NoSQL databases: document (MongoDB), key-value (Redis), column-family (Cassandra), graph (Neo4j)
- [ ] Data warehousing concepts: star schema, snowflake schema, OLAP vs OLTP
- [ ] Data formats: CSV, JSON, Parquet, Avro, ORC, HDF5, Arrow/Feather
- [ ] Distributed storage: HDFS, S3, GCS
- [ ] Data versioning: DVC, LakeFS, Delta Lake

#### 8.2 Exploratory Data Analysis (EDA)

- [ ] Descriptive statistics: central tendency, dispersion, shape
- [ ] Distribution analysis: histograms, KDE, Q-Q plots, box plots, violin plots
- [ ] Correlation analysis: Pearson, Spearman, Kendall, point-biserial, phi coefficient
- [ ] Multivariate EDA: pair plots, heatmaps, parallel coordinates
- [ ] Outlier detection: IQR, z-score, Mahalanobis distance, isolation forest, LOF
- [ ] Data profiling: pandas-profiling / ydata-profiling, Great Expectations

#### 8.3 Data Cleaning & Quality

- [ ] Missing data mechanisms: MCAR, MAR, MNAR
- [ ] Imputation: mean/median/mode, KNN imputation, MICE (multivariate imputation by chained equations), matrix completion, deep learning imputation
- [ ] Duplicate detection & deduplication
- [ ] Data type conversion & parsing
- [ ] String cleaning: regex, fuzzy matching (Levenshtein distance)
- [ ] Data validation frameworks: Great Expectations, Pandera, pydantic

#### 8.4 Feature Engineering

- [ ] Numerical features: scaling (StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler), log/Box-Cox/Yeo-Johnson transforms, binning, polynomial features, interaction features
- [ ] Categorical features: one-hot, label, ordinal, binary, target (mean) encoding, frequency encoding, leave-one-out encoding, CatBoost encoding, entity embeddings
- [ ] Text features: bag-of-words, TF-IDF, n-grams, character n-grams, text length, readability scores
- [ ] Date/time features: cyclical encoding (sin/cos), time since event, day-of-week, holiday flags
- [ ] Geospatial features: haversine distance, geohashing, spatial clustering
- [ ] Feature crosses & interaction terms
- [ ] Automated feature engineering: Featuretools, tsfresh (time series)

#### 8.5 Feature Selection

- [ ] Filter methods: variance threshold, correlation, chi-squared, mutual information, ANOVA F-value
- [ ] Wrapper methods: forward selection, backward elimination, recursive feature elimination (RFE)
- [ ] Embedded methods: L1 (Lasso) regularization, tree-based importance, SHAP-based selection
- [ ] Dimensionality reduction as feature extraction (PCA, autoencoders)
- [ ] Feature importance: permutation importance, drop-column importance, SHAP values
- [ ] Multicollinearity: VIF (Variance Inflation Factor)

#### 8.6 Handling Imbalanced Data

- [ ] Oversampling: random, SMOTE, ADASYN, borderline-SMOTE
- [ ] Undersampling: random, Tomek links, edited nearest neighbours, NearMiss
- [ ] Hybrid methods: SMOTE + Tomek, SMOTE + ENN
- [ ] Class-weighted loss functions
- [ ] Anomaly detection framing
- [ ] Evaluation with imbalanced data: precision-recall curve, F1, AUC-PR, MCC
- [ ] Threshold tuning: PR curve, ROC analysis, cost-sensitive thresholds

#### 8.7 Data Augmentation

- [ ] Image augmentation: flipping, rotation, cropping, color jitter, CutOut, MixUp, CutMix, RandAugment, AutoAugment, AugMax, trivial augment
- [ ] Text augmentation: synonym replacement, back-translation, random insertion/deletion/swap, contextual augmentation (LLM-based), EDA (Easy Data Augmentation)
- [ ] Audio augmentation: time stretching, pitch shifting, noise injection, SpecAugment
- [ ] Tabular augmentation: SMOTE variants, noise injection, generative (CTGAN)

---

## PART III: CLASSICAL MACHINE LEARNING

### 9. Supervised Learning — Regression

#### 9.1 Linear Regression

- [ ] Simple linear regression: OLS derivation (closed-form & gradient descent)
- [ ] Multiple linear regression: matrix formulation (β = (XᵀX)⁻¹Xᵀy)
- [ ] Assumptions: linearity, independence, homoscedasticity, normality of residuals, no multicollinearity
- [ ] Diagnostic plots: residual vs fitted, Q-Q, scale-location, Cook's distance
- [ ] Coefficient of determination R², adjusted R²
- [ ] Feature significance: t-tests on coefficients, F-test for overall model
- [ ] Weighted least squares (WLS) for heteroscedastic data
- [ ] Generalized least squares (GLS)

#### 9.2 Regularized Regression

- [ ] Ridge regression (L2): shrinkage, bias-variance tradeoff, closed-form solution, ridge trace
- [ ] Lasso regression (L1): sparsity, feature selection, no closed-form, coordinate descent
- [ ] Elastic Net: L1 + L2, mixing parameter α
- [ ] Regularization path & cross-validation for λ selection
- [ ] Bayesian interpretation: Ridge = Gaussian prior, Lasso = Laplace prior

#### 9.3 Polynomial & Nonlinear Regression

- [ ] Polynomial features & overfitting
- [ ] Basis function regression (radial basis, Fourier)
- [ ] Splines: linear, cubic, natural cubic splines, B-splines
- [ ] Generalized Additive Models (GAMs)
- [ ] Kernel regression (Nadaraya-Watson)
- [ ] Isotonic regression

#### 9.4 Generalized Linear Models (GLMs)

- [ ] Exponential family, link functions, canonical links
- [ ] Logistic regression as GLM (covered in classification)
- [ ] Poisson regression for count data
- [ ] Negative binomial regression (overdispersion)
- [ ] Gamma regression
- [ ] Quasi-likelihood methods
- [ ] Deviance, AIC, BIC for model selection

### 10. Supervised Learning — Classification

#### 10.1 Logistic Regression

- [ ] Sigmoid function, decision boundary (linear)
- [ ] Binary logistic regression: MLE, gradient derivation, iteratively reweighted least squares (IRLS)
- [ ] Multinomial logistic regression (softmax regression)
- [ ] Ordinal logistic regression
- [ ] Regularized logistic regression (L1, L2, elastic net)
- [ ] Calibration of predicted probabilities: Platt scaling, isotonic regression

#### 10.2 Support Vector Machines (SVMs)

- [ ] Hard-margin SVM: maximum margin hyperplane, support vectors
- [ ] Soft-margin SVM: slack variables, C parameter, hinge loss
- [ ] Dual formulation & quadratic programming
- [ ] Kernel trick: polynomial kernel, RBF (Gaussian) kernel, sigmoid kernel, string kernels
- [ ] Kernel properties: Mercer's theorem, positive semi-definiteness
- [ ] Multi-class SVM: one-vs-one, one-vs-rest (OVR)
- [ ] SVR (Support Vector Regression): ε-insensitive loss
- [ ] Computational complexity & scalability: SMO algorithm, kernel approximations (Random Fourier Features, Nyström method)

#### 10.3 K-Nearest Neighbours (KNN)

- [ ] Distance metrics: Euclidean, Manhattan, Minkowski, cosine similarity, Mahalanobis
- [ ] Choosing K: elbow method, cross-validation
- [ ] Weighted KNN (distance-weighted)
- [ ] Curse of dimensionality & KNN
- [ ] Efficient search: KD-trees, ball trees, locality-sensitive hashing (LSH)
- [ ] KNN for regression

#### 10.4 Naive Bayes

- [ ] Bayes' theorem applied to classification
- [ ] Naive independence assumption
- [ ] Gaussian Naive Bayes, Multinomial Naive Bayes, Bernoulli Naive Bayes, Complement Naive Bayes
- [ ] Laplace smoothing
- [ ] When Naive Bayes works well (high-dimensional sparse data, text)

#### 10.5 Decision Trees

- [ ] Splitting criteria: Gini impurity, entropy (information gain), gain ratio, variance reduction (regression)
- [ ] Tree construction: ID3, C4.5, CART
- [ ] Pruning: pre-pruning (early stopping), post-pruning (cost-complexity / minimal cost-complexity)
- [ ] Handling continuous features, missing values, multi-output
- [ ] Feature importance from trees
- [ ] Advantages: interpretability, no feature scaling needed, handles mixed types
- [ ] Disadvantages: high variance, axis-aligned splits, instability

#### 10.6 Discriminant Analysis

- [ ] Linear Discriminant Analysis (LDA): Fisher's criterion, assumptions
- [ ] Quadratic Discriminant Analysis (QDA)
- [ ] Regularized discriminant analysis
- [ ] LDA for dimensionality reduction (supervised)

### 11. Ensemble Methods

#### 11.1 Bagging

- [ ] Bootstrap aggregating: variance reduction
- [ ] Random Forest: random subspace method, feature bagging, out-of-bag (OOB) error, feature importance (MDI, MDA)
- [ ] Extremely Randomized Trees (Extra-Trees)
- [ ] Bagging for regression & classification

#### 11.2 Boosting

- [ ] AdaBoost: weight updates, exponential loss, weak learner requirement
- [ ] Gradient Boosting Machines (GBM): functional gradient descent, shrinkage, subsampling
- [ ] XGBoost: regularized objective, approximate splits (histogram-based), column subsampling, handling missing values, sparsity-aware algorithm, cache-aware block structure
- [ ] LightGBM: leaf-wise growth, GOSS (Gradient-based One-Side Sampling), EFB (Exclusive Feature Bundling), histogram-based splits, categorical feature handling
- [ ] CatBoost: ordered target encoding, oblivious decision trees, GPU training
- [ ] Histogram-based Gradient Boosting (scikit-learn HistGradientBoosting)
- [ ] Hyperparameter tuning: n_estimators, learning_rate, max_depth, min_child_weight, subsample, colsample, reg_alpha, reg_lambda
- [ ] Early stopping strategies

#### 11.3 Stacking & Blending

- [ ] Stacking (stacked generalization): base learners, meta-learner, cross-validation stacking
- [ ] Blending: holdout-based stacking
- [ ] Multi-level stacking
- [ ] Practical considerations: diversity of base learners, overfitting in stacking

#### 11.4 Voting & Averaging

- [ ] Hard voting vs soft voting
- [ ] Weighted averaging
- [ ] Bayesian model averaging

### 12. Unsupervised Learning

#### 12.1 Clustering

- [ ] K-Means: Lloyd's algorithm, K-Means++, mini-batch K-Means, elbow method, silhouette analysis
- [ ] K-Medoids (PAM)
- [ ] Hierarchical clustering: agglomerative (single/complete/average/Ward linkage), divisive, dendrogram, cophenetic correlation
- [ ] DBSCAN: ε-neighbourhood, minPts, core/border/noise points, limitations with varying density
- [ ] HDBSCAN: hierarchical density-based, cluster stability, soft clustering
- [ ] OPTICS (Ordering Points To Identify Clustering Structure)
- [ ] Gaussian Mixture Models (GMM): EM algorithm, BIC/AIC for component selection, covariance types (full, tied, diagonal, spherical)
- [ ] Spectral clustering: graph Laplacian, normalized cuts, Shi-Malik, Ng-Jordan-Weiss
- [ ] Mean shift clustering
- [ ] Affinity propagation
- [ ] BIRCH (Balanced Iterative Reducing and Clustering using Hierarchies)
- [ ] Self-Organizing Maps (SOM / Kohonen maps)
- [ ] Clustering evaluation: silhouette score, Calinski-Harabasz, Davies-Bouldin, adjusted Rand index (ARI), normalized mutual information (NMI), V-measure

#### 12.2 Dimensionality Reduction

- [ ] PCA: covariance matrix method, SVD method, explained variance ratio, scree plot, biplot
- [ ] Kernel PCA: non-linear extension, kernel selection
- [ ] Incremental PCA for large datasets
- [ ] Sparse PCA, Robust PCA
- [ ] Independent Component Analysis (ICA): cocktail party problem, FastICA
- [ ] Factor Analysis: latent factors, factor loadings, rotation (varimax, promax)
- [ ] t-SNE: perplexity, Barnes-Hut approximation, limitations (non-parametric, non-convex)
- [ ] UMAP: fuzzy simplicial sets, preserves global structure better than t-SNE, parametric UMAP
- [ ] Multidimensional Scaling (MDS): classical, non-metric
- [ ] Isomap: geodesic distances, k-nearest-neighbour graph
- [ ] Locally Linear Embedding (LLE)
- [ ] Laplacian eigenmaps
- [ ] Random projection: Johnson-Lindenstrauss lemma, Gaussian & sparse random projections
- [ ] Autoencoders for dimensionality reduction (see Deep Learning section)

#### 12.3 Anomaly / Outlier Detection

- [ ] Statistical methods: z-score, Grubbs' test, IQR
- [ ] Distance-based: KNN distance, Local Outlier Factor (LOF)
- [ ] Density-based: DBSCAN-based
- [ ] Isolation Forest: random partitioning, anomaly score
- [ ] One-Class SVM
- [ ] Autoencoder-based anomaly detection (reconstruction error)
- [ ] Elliptic Envelope (Gaussian assumption)
- [ ] Angle-based outlier detection (ABOD)

#### 12.4 Association Rule Mining

- [ ] Support, confidence, lift, conviction
- [ ] Apriori algorithm
- [ ] FP-Growth algorithm
- [ ] Applications: market basket analysis, recommendation pre-filtering

### 13. Model Evaluation & Selection

#### 13.1 Classification Metrics

- [ ] Confusion matrix: TP, TN, FP, FN
- [ ] Accuracy, precision, recall (sensitivity), specificity, F1-score, Fβ-score
- [ ] Matthews Correlation Coefficient (MCC)
- [ ] ROC curve & AUC-ROC: interpretation, multi-class extension (one-vs-rest)
- [ ] Precision-Recall curve & AUC-PR (preferred for imbalanced data)
- [ ] Log loss (cross-entropy loss)
- [ ] Cohen's Kappa
- [ ] Balanced accuracy
- [ ] Multi-class: macro, micro, weighted averaging
- [ ] Multi-label metrics: Hamming loss, subset accuracy, label-ranking average precision

#### 13.2 Regression Metrics

- [ ] Mean Squared Error (MSE), Root MSE (RMSE)
- [ ] Mean Absolute Error (MAE)
- [ ] Mean Absolute Percentage Error (MAPE), Symmetric MAPE (sMAPE)
- [ ] R² (coefficient of determination), adjusted R²
- [ ] Explained variance score
- [ ] Huber loss (robust regression metric)
- [ ] Quantile loss (pinball loss)

#### 13.3 Cross-Validation Strategies

- [ ] K-fold cross-validation
- [ ] Stratified K-fold (for classification)
- [ ] Leave-One-Out (LOO) cross-validation
- [ ] Repeated K-fold
- [ ] Group K-fold (for grouped data)
- [ ] Time series cross-validation: expanding window, sliding window
- [ ] Nested cross-validation for hyperparameter tuning + evaluation

#### 13.4 Hyperparameter Tuning

- [ ] Grid search, random search (Bergstra & Bengio)
- [ ] Bayesian optimization: Gaussian process surrogate, Tree-structured Parzen Estimator (TPE / Optuna)
- [ ] Hyperband & successive halving
- [ ] BOHB (Bayesian Optimization + HyperBand)
- [ ] Population-based training (PBT)
- [ ] Tools: Optuna, Ray Tune, Weights & Biases sweeps

#### 13.5 Bias-Variance Tradeoff & Model Selection

- [ ] Bias-variance decomposition of MSE
- [ ] Underfitting vs overfitting: learning curves, validation curves
- [ ] Model complexity vs generalization
- [ ] AIC, BIC, MDL for model selection
- [ ] Statistical comparison of models: paired t-test, Wilcoxon, McNemar's test, 5×2 cv paired t-test

#### 13.6 Calibration

- [ ] Reliability diagrams (calibration plots)
- [ ] Expected Calibration Error (ECE)
- [ ] Platt scaling (logistic calibration)
- [ ] Isotonic regression calibration
- [ ] Temperature scaling (for neural networks)
- [ ] Calibration in multi-class settings

### 14. Semi-Supervised, Self-Supervised & Weakly Supervised Learning (Classical)

#### 14.1 Semi-Supervised Learning

- [ ] Self-training (pseudo-labeling)
- [ ] Co-training
- [ ] Label propagation & label spreading (graph-based)
- [ ] Transductive SVM (TSVM)
- [ ] Generative models for semi-supervised learning
- [ ] Assumptions: smoothness, cluster, manifold, low-density separation

#### 14.2 Weak Supervision

- [ ] Data programming & Snorkel: labeling functions, noise-aware models
- [ ] Distant supervision (knowledge-base-guided labeling)
- [ ] Active learning: uncertainty sampling, query-by-committee, expected model change, batch-mode active learning

### 1.1 Learning Theory Fundamentals

- [ ] Supervised, unsupervised, semi-supervised, self-supervised, reinforcement learning
- [ ] Training, validation, test sets — why and how to split
- [ ] Generalization error, empirical risk minimization (ERM)
- [ ] Occam's razor, model complexity
- [ ] No Free Lunch theorem
- [ ] Data distributions: i.i.d. assumption, covariate shift, concept drift
- [ ] Online learning vs batch learning

### 1.2 Evaluation Metrics

#### 1.2.1 Classification Metrics

- [ ] Accuracy, when it fails (class imbalance)
- [ ] Brier score

#### 1.2.2 Regression Metrics

- [ ] R-squared, adjusted R-squared
- [ ] Huber loss (robustness to outliers)

#### 1.2.3 Ranking Metrics

- [ ] NDCG (Normalized Discounted Cumulative Gain)
- [ ] MRR (Mean Reciprocal Rank)

### 1.3 Data Preprocessing & Feature Engineering

#### 1.3.1 Data Cleaning

- [ ] Duplicate handling
- [ ] Data type inconsistencies

#### 1.3.2 Feature Scaling

- [ ] Min-Max normalization
- [ ] Z-score standardization
- [ ] Robust scaling (IQR-based)
- [ ] When scaling matters and when it doesn't

#### 1.3.3 Encoding Categorical Variables

- [ ] Target/Mean Encoding (and leakage risks)
- [ ] Frequency/Count Encoding
- [ ] Embedding (entity embeddings for deep learning)
- [ ] Binary Encoding, Hash Encoding

#### 1.3.4 Feature Transformation

- [ ] Binning / discretization
- [ ] Text feature extraction (TF-IDF, n-grams)

#### 1.3.6 Handling Class Imbalance

- [ ] Combined: SMOTEENN, SMOTETomek
- [ ] Ensemble approaches (BalancedBaggingClassifier)

### 1.4 Linear Models

#### 1.4.1 Linear Regression

- [ ] OLS derivation (normal equations)
- [ ] Gauss-Markov theorem (BLUE)
- [ ] Multicollinearity: VIF, condition number
- [ ] Ridge Regression (L2): closed form, regularization path
- [ ] Bayesian linear regression

#### 1.4.2 Logistic Regression

- [ ] Sigmoid function, log-odds interpretation
- [ ] Why logistic regression is a linear classifier despite sigmoid
- [ ] Multi-class: one-vs-rest, softmax regression
- [ ] Regularization in logistic regression
- [ ] Convergence guarantees, solvers: lbfgs, saga, newton-cg

#### 1.4.3 Generalized Linear Models (GLM)

- [ ] Probit model

### 1.5 Support Vector Machines (SVM)

- [ ] Hard-margin SVM: primal formulation
- [ ] Dual formulation derivation via Lagrangian
- [ ] KKT conditions in SVM context
- [ ] Support vectors — what they are and why they matter
- [ ] Kernel trick: kernel matrix, Mercer's theorem
- [ ] Kernel selection and hyperparameter tuning
- [ ] Computational complexity: O(n²) to O(n³) training
- [ ] Practical solvers: libSVM, LIBLINEAR

### 1.6 Tree-Based Methods

#### 1.6.1 Decision Trees

- [ ] CART algorithm
- [ ] Pre-pruning (max_depth, min_samples_split), post-pruning (cost-complexity)

#### 1.6.2 Random Forests

- [ ] Bootstrap aggregation (Bagging)
- [ ] Feature subsampling at each split (max_features)
- [ ] Variance reduction via averaging
- [ ] Extrapolation failure

#### 1.6.3 Gradient Boosting

- [ ] Boosting concept: sequential, error-correcting
- [ ] AdaBoost: sample reweighting, exponential loss
- [ ] Friedman's GBM: stagewise additive modeling
- [ ] XGBoost: second-order gradients, regularization, column subsampling, sparsity-aware
- [ ] XGBoost: weighted quantile sketch, histogram-based splits
- [ ] CatBoost: ordered boosting, native categorical support

#### 1.6.4 Ensemble Theory

- [ ] Bagging vs boosting vs stacking
- [ ] Stacking (meta-learning): level-0 and level-1 models
- [ ] Blending

### 1.7 Distance-Based Methods

#### 1.7.1 K-Nearest Neighbors (KNN)

- [ ] Lazy learning, non-parametric
- [ ] KD-tree, Ball-tree for approximate nearest neighbor (ANN)

#### 1.7.2 Approximate Nearest Neighbor (ANN)

- [ ] HNSW (Hierarchical Navigable Small World graphs)
- [ ] FAISS library (IVF, PQ, IVFPQ)
- [ ] Annoy library
- [ ] ScaNN
- [ ] Trade-off: recall vs latency vs memory

### 1.8 Probabilistic Graphical Models

#### 1.8.1 Naive Bayes

- [ ] Bayes theorem application

#### 1.8.2 Bayesian Networks

- [ ] DAG structure, joint probability factorization
- [ ] Parameter learning (MLE, MAP)
- [ ] Structure learning (score-based, constraint-based)
- [ ] Exact inference: variable elimination, belief propagation
- [ ] Approximate inference: loopy belief propagation, sampling

#### 1.8.3 Hidden Markov Models (HMM)

- [ ] States, observations, transition and emission probabilities
- [ ] Viterbi algorithm (decoding)
- [ ] Baum-Welch (EM for HMM)

#### 1.8.4 Conditional Random Fields (CRF)

- [ ] Undirected graphical models
- [ ] Linear-chain CRF for sequence labeling
- [ ] CRF vs HMM: global normalization
- [ ] Applications: NER, POS tagging

### 1.9 Unsupervised Learning

#### 1.9.1 Clustering

- [ ] K-Means: algorithm, convergence, k-means++ initialization
- [ ] K-Means limitations: non-convex shapes, outliers, k selection
- [ ] GMM vs K-Means: soft assignments, covariance types
- [ ] BIRCH, OPTICS

#### 1.9.2 Dimensionality Reduction

- [ ] PCA: variance maximization, reconstruction, explained variance ratio
- [ ] t-SNE: perplexity, crowding problem, non-linear
- [ ] UMAP: topology-preserving, faster, better global structure
- [ ] LDA (Linear Discriminant Analysis): supervised, class separability

#### 1.9.3 Anomaly Detection

- [ ] ECOD, PyOD library

#### 1.9.4 Topic Modeling

- [ ] LDA (Latent Dirichlet Allocation): generative model
- [ ] LDA parameter inference: variational EM, Gibbs sampling
- [ ] LSA/LSI (Latent Semantic Analysis via SVD)
- [ ] Neural topic models (ProdLDA, NTM)
- [ ] BERTopic

### 1.10 Cross-Validation & Hyperparameter Tuning

- [ ] Time-series CV: walk-forward validation
- [ ] Nested CV (for unbiased evaluation)
- [ ] Hyperband, ASHA

---

## PART IV: DEEP LEARNING FOUNDATIONS

### 15. Neural Network Fundamentals

#### 15.1 Perceptrons & Multi-Layer Perceptrons (MLPs)

- [ ] Single perceptron: linear classifier, perceptron learning rule
- [ ] Universal approximation theorem
- [ ] Multi-layer perceptron architecture: input, hidden, output layers
- [ ] Width vs depth tradeoffs
- [ ] Representation capacity & expressiveness

#### 15.2 Activation Functions

- [ ] Sigmoid: properties, vanishing gradient problem
- [ ] Tanh: zero-centered, vanishing gradient
- [ ] ReLU: sparsity, dying ReLU problem
- [ ] Leaky ReLU, Parametric ReLU (PReLU)
- [ ] ELU, SELU (self-normalizing property)
- [ ] GELU (Gaussian Error Linear Unit) — used in transformers
- [ ] Swish / SiLU (Sigmoid Linear Unit)
- [ ] Mish activation
- [ ] Softmax: multi-class output, temperature scaling
- [ ] Hardswish, Hardtanh (mobile-efficient activations)
- [ ] Choosing activations: hidden layers vs output layers

#### 15.3 Loss Functions

- [ ] Regression losses: MSE (L2), MAE (L1), Huber (smooth L1), log-cosh
- [ ] Classification losses: binary cross-entropy (BCE), categorical cross-entropy, focal loss, hinge loss
- [ ] Contrastive losses: triplet loss, NT-Xent (InfoNCE), supervised contrastive loss
- [ ] Ranking losses: margin ranking loss, pairwise/listwise ranking losses
- [ ] Reconstruction losses: MSE, BCE, perceptual loss, SSIM loss
- [ ] KL divergence loss (VAEs)
- [ ] CTC loss (Connectionist Temporal Classification — speech, OCR)
- [ ] Label smoothing: soft targets, reducing overconfidence
- [ ] Mixup & CutMix loss formulation

#### 15.4 Backpropagation & Computational Graphs

- [ ] Forward pass & computational graph construction
- [ ] Backward pass: chain rule, reverse-mode automatic differentiation
- [ ] Gradient flow through common operations
- [ ] Vanishing & exploding gradients
- [ ] Gradient checking (numerical gradient verification)
- [ ] Higher-order gradients (Hessian-vector products)
- [ ] Autograd in PyTorch / TensorFlow: tape-based vs graph-based
- [ ] Stop-gradient / detach operations

#### 15.5 Weight Initialization

- [ ] Zero initialization (why it fails — symmetry breaking)
- [ ] Random initialization: small random, uniform, normal
- [ ] Xavier / Glorot initialization (for sigmoid/tanh)
- [ ] He / Kaiming initialization (for ReLU family)
- [ ] Orthogonal initialization
- [ ] LSUV (Layer-Sequential Unit-Variance)
- [ ] Fixup initialization (residual networks without normalization)
- [ ] Data-dependent initialization

#### 15.6 Regularization Techniques

- [ ] L1 & L2 regularization (weight decay)
- [ ] Dropout: standard, spatial dropout, DropConnect, DropBlock
- [ ] Batch Normalization: internal covariate shift, training vs inference mode, learnable affine parameters
- [ ] Layer Normalization, Instance Normalization, Group Normalization, RMS Normalization
- [ ] Weight normalization
- [ ] Spectral normalization
- [ ] Data augmentation as regularization
- [ ] Early stopping
- [ ] Max-norm constraint
- [ ] Noise injection: input noise, weight noise, gradient noise
- [ ] Stochastic depth (layer dropout)
- [ ] Mixup, CutMix, Manifold Mixup
- [ ] R-Drop (regularized dropout)

#### 15.7 Training Techniques

- [ ] Mini-batch training: batch size selection, gradient accumulation
- [ ] Learning rate scheduling: step decay, exponential decay, cosine annealing, warmup + decay, cyclical learning rates, OneCycleLR
- [ ] Mixed precision training: FP16, BF16, loss scaling, dynamic loss scaling
- [ ] Gradient clipping: by value, by global norm
- [ ] Gradient accumulation for effective larger batch sizes
- [ ] Curriculum learning: easy-to-hard ordering
- [ ] Training diagnostics: loss curves, gradient norms, activation statistics, dead neuron detection

### 2.1 Neural Network Fundamentals

#### 2.1.1 Perceptron & MLP

- [ ] Biological neuron analogy
- [ ] McCulloch-Pitts neuron
- [ ] Perceptron learning rule, convergence theorem
- [ ] Feedforward pass
- [ ] Capacity, depth vs width

#### 2.1.2 Activation Functions

- [ ] Tanh: zero-centered, still saturates
- [ ] Swish (x·sigmoid(x))
- [ ] Mish
- [ ] Softmax: numerical stability, log-sum-exp trick
- [ ] Softplus

#### 2.1.3 Loss Functions

- [ ] Triplet loss (metric learning)
- [ ] Contrastive loss (SimCLR)
- [ ] ELBO loss

#### 2.1.4 Backpropagation

- [ ] Chain rule derivation through computational graph
- [ ] Forward pass vs backward pass
- [ ] Manual gradient computation (understanding autograd)
- [ ] Exploding gradient problem
- [ ] Gradient flow through skip connections

### 2.2 Regularization Techniques

- [ ] L1 regularization: sparsity effect
- [ ] Dropout: training vs inference (scale by 1-p)
- [ ] DropConnect
- [ ] Inverted Dropout
- [ ] Spatial Dropout (for CNNs)
- [ ] DropPath / Stochastic Depth

### 2.3 Normalization Techniques

- [ ] Batch Normalization: internal covariate shift, training vs inference, momentum, γ and β
- [ ] Layer Normalization: NLP-friendly, sequence-length independent
- [ ] Instance Normalization (style transfer)
- [ ] RMS Norm (LLaMA)
- [ ] Pre-LN vs Post-LN transformers: stability differences

### 2.4 Weight Initialization

- [ ] Zero initialization pitfall

---

## PART V: CONVOLUTIONAL NEURAL NETWORKS & COMPUTER VISION

### 16. CNN Foundations

#### 16.1 Convolution Operations

- [ ] 1D, 2D, 3D convolution
- [ ] Kernel / filter, stride, padding (valid, same, full)
- [ ] Output size calculation
- [ ] Receptive field
- [ ] Depthwise separable convolution (MobileNet)
- [ ] Dilated / atrous convolution (DeepLab)
- [ ] Transposed convolution (deconvolution) for upsampling
- [ ] Grouped convolution (AlexNet, ResNeXt)
- [ ] Deformable convolution
- [ ] 1×1 convolution (Network in Network, dimensionality reduction)

#### 16.2 Pooling & Downsampling

- [ ] Max pooling, average pooling, global average pooling (GAP)
- [ ] Strided convolution as alternative to pooling
- [ ] Adaptive pooling
- [ ] Spatial pyramid pooling (SPPNet)

#### 16.3 CNN Architectures (Evolution)

- [ ] LeNet-5 (1998): pioneering CNN for digits
- [ ] AlexNet (2012): deep CNN, ReLU, dropout, GPU training
- [ ] VGGNet (2014): depth with small 3×3 filters
- [ ] GoogLeNet / Inception v1-v4 (2014-2017): inception modules, factorized convolutions, auxiliary classifiers
- [ ] ResNet (2015): residual connections / skip connections, identity mapping, ResNet-50/101/152
- [ ] ResNeXt (2017): cardinality dimension, grouped convolutions
- [ ] DenseNet (2017): dense connectivity, feature reuse
- [ ] Squeeze-and-Excitation Networks (SENet, 2018): channel attention
- [ ] MobileNet v1/v2/v3: depthwise separable convolutions, inverted residuals, squeeze-excite, neural architecture search
- [ ] ShuffleNet v1/v2: channel shuffle, efficient group convolution
- [ ] EfficientNet (2019): compound scaling (width, depth, resolution), NAS-derived base
- [ ] EfficientNetV2: progressive learning, Fused-MBConv
- [ ] NFNets: normalizer-free networks, AGC (adaptive gradient clipping)
- [ ] RegNet: design spaces for network architecture
- [ ] ConvNeXt (2022): modernized ConvNet competing with ViT
- [ ] RepVGG: re-parameterization for inference efficiency

### 17. Object Detection

#### 17.1 Two-Stage Detectors

- [ ] R-CNN: region proposals (selective search), CNN feature extraction, SVM classification
- [ ] Fast R-CNN: RoI pooling, multi-task loss
- [ ] Faster R-CNN: Region Proposal Network (RPN), anchor boxes
- [ ] Feature Pyramid Network (FPN): multi-scale feature maps
- [ ] Cascade R-CNN: multi-stage detection with increasing IoU thresholds

#### 17.2 One-Stage Detectors

- [ ] SSD (Single Shot MultiBox Detector)
- [ ] YOLO family: YOLOv1 through YOLOv10+, architecture evolution, anchor-free designs
- [ ] RetinaNet: focal loss for class imbalance
- [ ] CenterNet: keypoint-based detection (objects as center points)
- [ ] CornerNet: corner-based detection
- [ ] FCOS: fully convolutional one-stage, anchor-free

#### 17.3 Transformer-Based Detection

- [ ] DETR (Detection Transformer): set prediction, bipartite matching, no NMS/anchors
- [ ] Deformable DETR: deformable attention for faster convergence
- [ ] DINO: improved DETR with denoising anchor boxes
- [ ] Co-DETR
- [ ] RT-DETR: real-time DETR
- [ ] Grounding DINO: open-set object detection with text

#### 17.4 Detection Concepts

- [ ] Intersection over Union (IoU), GIoU, DIoU, CIoU
- [ ] Non-Maximum Suppression (NMS), Soft-NMS, DIoU-NMS
- [ ] Anchor boxes: aspect ratios, scales, anchor-free alternatives
- [ ] Multi-scale detection: FPN, PANet, BiFPN, NAS-FPN
- [ ] Evaluation: mAP (mean Average Precision), COCO metrics (AP@[.5:.95]), PASCAL VOC metrics

### 18. Image Segmentation

#### 18.1 Semantic Segmentation

- [ ] Fully Convolutional Network (FCN): replacing FC layers with conv
- [ ] U-Net: encoder-decoder with skip connections (medical imaging)
- [ ] SegNet: encoder-decoder with pooling indices
- [ ] DeepLab v1-v3+: atrous convolutions, ASPP (Atrous Spatial Pyramid Pooling), CRF post-processing, encoder-decoder with atrous separable convolution
- [ ] PSPNet: Pyramid Pooling Module
- [ ] HRNet: high-resolution representations throughout
- [ ] Transformer-based: SegFormer, SETR, Mask2Former

#### 18.2 Instance & Panoptic Segmentation

- [ ] Mask R-CNN: RoIAlign, mask head
- [ ] YOLACT: real-time instance segmentation
- [ ] PointRend: point-based refinement
- [ ] Panoptic segmentation: stuff + things, Panoptic FPN
- [ ] Mask2Former: unified architecture for all segmentation tasks
- [ ] SAM (Segment Anything Model): promptable segmentation, zero-shot transfer

#### 18.3 Segmentation Losses & Metrics

- [ ] Pixel-wise cross-entropy, weighted cross-entropy
- [ ] Dice loss, Tversky loss
- [ ] Lovász-Softmax loss (IoU surrogate)
- [ ] Boundary losses
- [ ] mIoU (mean Intersection over Union), pixel accuracy, Dice coefficient

### 19. Advanced Computer Vision Tasks

#### 19.1 Pose Estimation

- [ ] 2D human pose estimation: heatmap-based (Stacked Hourglass, HRNet, SimpleBaseline), regression-based
- [ ] Top-down vs bottom-up approaches (OpenPose)
- [ ] 3D pose estimation: lifting 2D to 3D, direct 3D prediction
- [ ] Hand pose estimation, face landmark detection

#### 19.2 Image Generation & Synthesis

- [ ] Neural style transfer: Gram matrix, content & style loss
- [ ] Super-resolution: SRCNN, ESRGAN, Real-ESRGAN
- [ ] Image inpainting: contextual attention, LaMa
- [ ] Image-to-image translation: Pix2Pix, CycleGAN, SPADE
- [ ] NeRF (Neural Radiance Fields): novel view synthesis, 3D-aware generation
- [ ] 3D Gaussian Splatting

#### 19.3 Video Understanding

- [ ] Action recognition: two-stream networks, I3D, SlowFast, TimeSformer, VideoMAE
- [ ] Temporal action detection & localization
- [ ] Video object detection & tracking
- [ ] Object tracking: SORT, DeepSORT, ByteTrack, OC-SORT
- [ ] Optical flow: FlowNet, RAFT, PWC-Net
- [ ] Video segmentation: VOS, video instance segmentation

#### 19.4 3D Vision

- [ ] Depth estimation: monocular (MiDaS, DPT), stereo
- [ ] Point cloud processing: PointNet, PointNet++, Point Transformer
- [ ] 3D object detection: VoxelNet, PointPillars, CenterPoint
- [ ] Multi-view geometry, structure from motion (SfM), SLAM
- [ ] Mesh reconstruction, occupancy networks

#### 19.5 Face & Biometrics

- [ ] Face detection: MTCNN, RetinaFace
- [ ] Face recognition: FaceNet (triplet loss), ArcFace (additive angular margin), CosFace
- [ ] Face verification vs identification
- [ ] Face anti-spoofing / liveness detection
- [ ] Deepfake detection

#### 19.6 OCR & Document Understanding

- [ ] Text detection: EAST, CRAFT, DBNet
- [ ] Text recognition: CRNN, attention-based (ABINet), TrOCR
- [ ] Scene text (in-the-wild): end-to-end (PaddleOCR, EasyOCR)
- [ ] Document layout analysis, table detection & extraction
- [ ] Document AI: LayoutLM, LayoutLMv3, Donut

#### 19.7 Medical Imaging

- [ ] Modalities: X-ray, CT, MRI, ultrasound, pathology (whole slide images)
- [ ] U-Net & nnU-Net for medical segmentation
- [ ] Transfer learning from ImageNet to medical domains
- [ ] Self-supervised pretraining for medical data
- [ ] Class imbalance & small dataset challenges
- [ ] Radiology report generation

### 2.5 Convolutional Neural Networks (CNNs)

#### 2.5.1 Core Convolution Operations

- [ ] Convolution vs cross-correlation
- [ ] Stride, dilation (atrous convolution)
- [ ] Pointwise (1×1) convolution: channel mixing

#### 2.5.2 CNN Architectures (Know Each Evolution)

- [ ] AlexNet: ReLU, dropout, data augmentation
- [ ] VGGNet: depth through 3×3 convolutions
- [ ] InceptionNet / GoogLeNet: inception module, auxiliary classifiers
- [ ] Wide ResNet
- [ ] MobileNetV2: inverted residuals, linear bottlenecks
- [ ] RegNet
- [ ] ConvNeXt: modernizing CNN with transformer design choices

#### 2.5.3 Object Detection

- [ ] R-CNN family: R-CNN, Fast R-CNN, Faster R-CNN
- [ ] YOLO family: YOLOv1-YOLOv9, anchor boxes, grid prediction
- [ ] RetinaNet: Focal Loss for dense detectors
- [ ] Anchor-free detectors: FCOS, CenterPoint
- [ ] mAP evaluation for detection

#### 2.5.4 Semantic & Instance Segmentation

- [ ] Mask R-CNN: RoI Align, instance masks

### 4.1 Image Fundamentals

- [ ] Image representation: pixels, channels (RGB, RGBA, HSV, LAB)
- [ ] Image histograms
- [ ] Convolution and correlation in signal processing
- [ ] Fourier transform for images
- [ ] Image filtering: Gaussian, Sobel, Laplacian of Gaussian
- [ ] Edge detection: Canny, LoG
- [ ] Feature descriptors: SIFT, SURF, HOG, ORB

### 4.2 Vision Transformers (ViT)

- [ ] Patch embedding: image → sequence of patches
- [ ] Learnable positional embeddings
- [ ] Scaling: ViT-S, B, L, H
- [ ] Data requirements vs CNNs
- [ ] Swin Transformer: hierarchical, shifted windows, local attention
- [ ] Swin V2
- [ ] BEiT: BERT-style pre-training for ViT
- [ ] CLIP vision encoder

### 4.3 Image Generation (Advanced)

- [ ] ControlNet: additional conditioning
- [ ] SDXL, SD 3, FLUX
- [ ] DALL-E 3, Imagen 3
- [ ] Edit: InstructPix2Pix, instruct-based editing
- [ ] Inpainting, outpainting

### 4.4 Video Understanding

- [ ] 3D convolutions (C3D, I3D)
- [ ] Two-stream networks: spatial + temporal
- [ ] Optical flow: Lucas-Kanade, Farneback, RAFT
- [ ] Temporal segments, SlowFast networks
- [ ] Video Transformers: TimeSformer, VideoMAE
- [ ] Video generation: Sora, CogVideoX, Wan2.1
- [ ] Action recognition, activity detection
- [ ] Video question answering

### 4.5 3D Vision & Scene Understanding

- [ ] NeRF (Neural Radiance Fields): volumetric rendering
- [ ] Stereo matching

### 4.6 Medical & Specialized Imaging

- [ ] CT, MRI, X-Ray specific challenges
- [ ] Histopathology with transformers
- [ ] Domain shift in medical imaging
- [ ] Class imbalance (lesion detection)

---

## PART VI: SEQUENCE MODELS, TRANSFORMERS & NLP

### 20. Recurrent Neural Networks

#### 20.1 RNN Foundations

- [ ] Vanilla RNN: architecture, hidden state, unfolding in time
- [ ] Backpropagation Through Time (BPTT): truncated BPTT
- [ ] Vanishing & exploding gradients in RNNs
- [ ] Bidirectional RNNs
- [ ] Deep (stacked) RNNs

#### 20.2 Gated Architectures

- [ ] LSTM: forget gate, input gate, output gate, cell state, peephole connections
- [ ] GRU: update gate, reset gate, comparison with LSTM
- [ ] Highway networks

#### 20.3 Sequence-to-Sequence Models

- [ ] Encoder-decoder framework
- [ ] Attention mechanism (Bahdanau attention): additive attention, alignment scores
- [ ] Luong attention: dot-product, general, concat
- [ ] Teacher forcing vs scheduled sampling
- [ ] Beam search decoding: beam width, length normalization, coverage penalty
- [ ] Greedy decoding, top-k sampling, top-p (nucleus) sampling, temperature

### 21. Transformer Architecture

#### 21.1 Core Transformer Mechanics

- [ ] Self-attention: query, key, value matrices, scaled dot-product attention
- [ ] Multi-head attention: multiple attention heads, concatenation, projection
- [ ] Positional encoding: sinusoidal, learned, relative (RPE), RoPE (Rotary Position Embeddings), ALiBi
- [ ] Layer normalization: Pre-LN vs Post-LN, RMSNorm
- [ ] Feed-forward network (FFN): position-wise, expansion ratio
- [ ] Residual connections in transformers
- [ ] Encoder-decoder architecture (original Transformer — Vaswani et al., 2017)
- [ ] Encoder-only (BERT family), Decoder-only (GPT family), Encoder-Decoder (T5, BART)
- [ ] Causal masking / autoregressive mask
- [ ] Cross-attention in encoder-decoder models

#### 21.2 Efficient & Long-Context Transformers

- [ ] Computational complexity of attention: O(n²) problem
- [ ] Sparse attention: local, strided, BigBird, Longformer (sliding window + global)
- [ ] Linear attention: Performer (FAVOR+), Random Feature Attention
- [ ] Linformer: low-rank approximation of attention matrix
- [ ] FlashAttention & FlashAttention-2: IO-aware, tiling, kernel fusion
- [ ] Multi-Query Attention (MQA) & Grouped-Query Attention (GQA)
- [ ] Sliding window attention (Mistral)
- [ ] Ring Attention for distributed long-context
- [ ] State-space models: S4, Mamba (selective state spaces), linear RNNs
- [ ] RWKV: RNN-Transformer hybrid
- [ ] Hyena: convolution-based attention replacement
- [ ] Mixture of Experts (MoE) in transformers: top-k routing, load balancing, Switch Transformer, GShard, Mixtral

#### 21.3 Vision Transformers

- [ ] ViT (Vision Transformer): patch embedding, cls token, positional embedding
- [ ] DeiT: data-efficient training, distillation token
- [ ] Swin Transformer: shifted windows, hierarchical feature maps
- [ ] PVT, CvT, CoAtNet: hybrid CNN-Transformer
- [ ] MAE (Masked Autoencoder): self-supervised pretraining for vision
- [ ] DINO & DINOv2: self-supervised ViT with self-distillation
- [ ] BEiT: BERT-style pretraining for vision
- [ ] EVA, EVA-02: scaling ViTs
- [ ] SAM (Segment Anything): ViT-based foundation model for segmentation

### 22. Natural Language Processing

#### 22.1 Text Preprocessing & Tokenization

- [ ] Text normalization: lowercasing, punctuation removal, stemming, lemmatization
- [ ] Tokenization: word-level, character-level, subword
- [ ] Subword tokenization algorithms: BPE (Byte Pair Encoding), WordPiece, Unigram (SentencePiece), Byte-level BPE
- [ ] Vocabulary construction & special tokens ([CLS], [SEP], [MASK], [PAD], [UNK])
- [ ] Detokenization & token-to-character alignment
- [ ] Multilingual tokenization challenges

#### 22.2 Word Embeddings

- [ ] One-hot encoding limitations
- [ ] Word2Vec: Skip-gram, CBOW, negative sampling, hierarchical softmax
- [ ] GloVe: global co-occurrence matrix, weighted least squares
- [ ] FastText: subword (character n-gram) embeddings, handling OOV words
- [ ] Embedding evaluation: word analogies, similarity benchmarks, intrinsic vs extrinsic evaluation
- [ ] Contextual embeddings (ELMo): bidirectional LSTM-based, layer-wise representations

#### 22.3 Pre-trained Language Models

- [ ] BERT: masked language modeling (MLM), next sentence prediction (NSP), [CLS] token, fine-tuning
- [ ] RoBERTa: removing NSP, dynamic masking, larger batches, more data
- [ ] ALBERT: factorized embedding, cross-layer parameter sharing, sentence order prediction
- [ ] DistilBERT: knowledge distillation for smaller BERT
- [ ] ELECTRA: replaced token detection (discriminator-generator)
- [ ] DeBERTa: disentangled attention, enhanced mask decoder
- [ ] XLNet: permutation language modeling, Transformer-XL with relative positional encoding
- [ ] GPT-1, GPT-2, GPT-3: autoregressive language modeling, scaling, in-context learning
- [ ] T5 (Text-to-Text Transfer Transformer): unifying NLP tasks as text generation
- [ ] BART: denoising autoencoder, encoder-decoder pretraining
- [ ] mBERT, XLM-R: multilingual models, cross-lingual transfer

#### 22.4 NLP Tasks & Techniques

- [ ] Text classification: sentiment analysis, topic classification, intent detection
- [ ] Named Entity Recognition (NER): BIO/IOB tagging, CRF layer, span-based NER
- [ ] Part-of-Speech (POS) tagging
- [ ] Dependency parsing, constituency parsing
- [ ] Semantic Role Labeling (SRL)
- [ ] Coreference resolution
- [ ] Relation extraction
- [ ] Machine translation: statistical MT (phrase-based), neural MT (seq2seq + attention, Transformer-based), evaluation (BLEU, METEOR, chrF, COMET)
- [ ] Text summarization: extractive (TextRank, BertSumExt) vs abstractive (BART, Pegasus, T5)
- [ ] Question answering: extractive (SQuAD-style, span extraction), generative, open-domain QA (retriever + reader)
- [ ] Natural language inference (NLI) / textual entailment: SNLI, MultiNLI
- [ ] Semantic textual similarity (STS): sentence embeddings, Sentence-BERT
- [ ] Information extraction: open information extraction, event extraction
- [ ] Information retrieval: BM25, TF-IDF, dense retrieval (DPR, ColBERT), re-ranking
- [ ] Dialogue systems: task-oriented (DST, policy, NLG), open-domain (retrieval-based, generative)
- [ ] Topic modeling: LDA (Latent Dirichlet Allocation), NMF, BERTopic
- [ ] Keyword extraction: RAKE, YAKE, KeyBERT
- [ ] Text generation: language model decoding strategies, controllable generation, CTRL, PPLM

### 2.6 Recurrent Neural Networks (RNNs)

#### 2.6.1 Vanilla RNN

- [ ] Hidden state, recurrence equation

#### 2.6.2 LSTM

- [ ] Gradient highway (LSTM's solution to vanishing gradient)
- [ ] Stacked LSTM

#### 2.6.3 GRU (Gated Recurrent Unit)

- [ ] GRU vs LSTM: fewer parameters, similar performance

#### 2.6.4 Sequence-to-Sequence Models

- [ ] Attention in Seq2Seq (Bahdanau attention)
- [ ] Coverage mechanism

### 2.7 Attention Mechanisms

#### 2.7.1 Classic Attention

- [ ] Attention as soft alignment

#### 2.7.2 Scaled Dot-Product Attention

- [ ] Q, K, V formulation
- [ ] Scaling factor √d_k and why it's needed
- [ ] Softmax normalization, attention weights
- [ ] Attention complexity: O(n²) in sequence length

#### 2.7.3 Multi-Head Attention

- [ ] Parallel attention heads
- [ ] Head dimensionality: d_model / n_heads
- [ ] Concatenation and linear projection
- [ ] Different heads capture different relationships

#### 2.7.4 Self-Attention vs Cross-Attention

- [ ] Padding mask

#### 2.7.5 Efficient Attention Variants

- [ ] Linear attention: kernel approximation
- [ ] FlashAttention: IO-aware exact attention (fused CUDA kernel)
- [ ] FlashAttention-2, FlashAttention-3
- [ ] Multi-Query Attention (MQA): shared K/V heads
- [ ] Grouped Query Attention (GQA): Llama 2/3
- [ ] Ring Attention (for very long sequences)

### 2.8 Transformer Architecture

#### 2.8.1 Original Transformer (Vaswani 2017)

- [ ] Encoder stack: multi-head self-attention + FFN + residuals + layer norm
- [ ] Decoder stack: masked self-attention + cross-attention + FFN
- [ ] Position-wise FFN: two linear layers with ReLU
- [ ] Residual connections and why they help
- [ ] Layer normalization placement

#### 2.8.2 Positional Encoding

- [ ] Sinusoidal positional encoding (original transformer)
- [ ] Learned positional embeddings (BERT, GPT)
- [ ] Relative positional encoding (Shaw et al.)
- [ ] ALiBi (Attention with Linear Biases)
- [ ] RoPE (Rotary Position Embedding): complex number rotation
- [ ] RoPE for context length extension
- [ ] YaRN, LongRoPE

#### 2.8.3 Transformer Variants by Architecture

- [ ] Decoder-only: GPT family (generative, autoregressive)
- [ ] State Space Models: Mamba, Mamba-2 (alternative to attention)
- [ ] Hybrid architectures: Jamba (Mamba + attention)

#### 2.8.4 Training Dynamics

- [ ] Gradient clipping in transformers
- [ ] Weight tying (input embedding = output embedding)
- [ ] Initialization for transformers
- [ ] Training instability causes and remedies

### 3.1 Classic NLP

#### 3.1.1 Text Preprocessing

- [ ] Sentence segmentation
- [ ] Stop word removal
- [ ] Stemming (Porter, Snowball) vs Lemmatization
- [ ] Case normalization
- [ ] Regex for text cleaning

#### 3.1.2 Text Representation

- [ ] Bag of Words (BoW)
- [ ] TF-IDF: term frequency, inverse document frequency
- [ ] N-gram language models
- [ ] Perplexity as language model evaluation metric

#### 3.1.3 Word Embeddings

- [ ] Analogy reasoning: king - man + woman = queen
- [ ] Bias in word embeddings
- [ ] Retrofitting for downstream tasks

#### 3.1.4 Sequence Labeling

- [ ] Chunking
- [ ] BIO, BIOES tagging scheme

#### 3.1.5 Traditional NLP Tasks

- [ ] Sentiment analysis: lexicon-based vs ML-based
- [ ] Machine translation (statistical: IBM models, phrase-based)

### 3.2 Transformer-Based NLP Models

#### 3.2.1 BERT & Encoder Models

- [ ] Masked Language Modeling (MLM): 15% token masking
- [ ] BERT tokenizer: WordPiece
- [ ] [CLS] token for classification, [SEP] separator
- [ ] Fine-tuning BERT for downstream tasks
- [ ] ALBERT: cross-layer parameter sharing, SOP task

#### 3.2.2 GPT Family (Decoder Models)

- [ ] GPT-1: language model pre-training
- [ ] GPT-2: zero-shot task transfer
- [ ] GPT-3: few-shot in-context learning, scaling
- [ ] InstructGPT: RLHF alignment
- [ ] GPT-4: multimodal, longer context
- [ ] GPT-4o, GPT-o1, GPT-o3

#### 3.2.3 T5, BART & Encoder-Decoder Models

- [ ] T5: text-to-text framework, span corruption
- [ ] BART: denoising pre-training (text infilling, shuffling)
- [ ] mT5, mBART: multilingual
- [ ] Pegasus: gap sentence generation

#### 3.2.4 Open-Source LLM Families

- [ ] Mixtral 8x7B: sparse MoE
- [ ] Qwen family
- [ ] Gemma, Gemma 2
- [ ] Phi-1/2/3: small but capable (data quality focus)
- [ ] DeepSeek-V2, DeepSeek-V3, DeepSeek-R1
- [ ] Command R, Falcon
- [ ] Comparison: architecture differences, training strategies

### 3.3 Tokenization

- [ ] BPE (Byte Pair Encoding): iterative merging
- [ ] SentencePiece: language-agnostic
- [ ] Tiktoken (GPT-4)
- [ ] Unigram Language Model tokenizer
- [ ] Byte-level BPE (GPT-2, RoBERTa)

---

## PART VII: GENERATIVE MODELS

### 23. Autoencoders

#### 23.1 Autoencoder Variants

- [ ] Vanilla autoencoder: encoder, bottleneck, decoder, reconstruction loss
- [ ] Denoising autoencoder (DAE): adding input noise
- [ ] Sparse autoencoder: L1 penalty on activations, KL divergence sparsity
- [ ] Contractive autoencoder: Frobenius norm of Jacobian
- [ ] Variational Autoencoder (VAE): latent space, reparameterization trick, ELBO, KL divergence term, posterior collapse
- [ ] β-VAE: disentangled representations, β hyperparameter
- [ ] VQ-VAE (Vector Quantized VAE): discrete latent codes, codebook, straight-through estimator
- [ ] VQ-VAE-2: hierarchical latents
- [ ] Conditional VAE (CVAE)
- [ ] Adversarial autoencoders (AAE)
- [ ] WAE (Wasserstein Autoencoder)

### 24. Generative Adversarial Networks (GANs)

#### 24.1 GAN Foundations & Variants

- [ ] Vanilla GAN: generator, discriminator, minimax game, JS divergence
- [ ] Training challenges: mode collapse, training instability, vanishing gradients
- [ ] DCGAN: architectural guidelines (BatchNorm, strided convolutions, LeakyReLU)
- [ ] WGAN: Wasserstein distance, weight clipping
- [ ] WGAN-GP: gradient penalty for Lipschitz constraint
- [ ] Spectral Normalization GAN (SN-GAN)
- [ ] Progressive GAN: growing resolution during training
- [ ] StyleGAN, StyleGAN2, StyleGAN3: style-based generator, mapping network, AdaIN, equivariance
- [ ] BigGAN: large-scale class-conditional generation, truncation trick
- [ ] Conditional GAN (cGAN): class-conditional generation, projection discriminator
- [ ] Pix2Pix: paired image-to-image translation, PatchGAN discriminator
- [ ] CycleGAN: unpaired image translation, cycle consistency loss
- [ ] StarGAN: multi-domain translation
- [ ] GAN evaluation metrics: FID (Fréchet Inception Distance), IS (Inception Score), KID, precision/recall, LPIPS

### 25. Diffusion Models

#### 25.1 Diffusion Model Foundations

- [ ] Forward process: gradual noise addition, noise schedule (linear, cosine)
- [ ] Reverse process: learning to denoise, denoising network (U-Net)
- [ ] DDPM (Denoising Diffusion Probabilistic Models): training objective, simplified loss, variational lower bound
- [ ] DDIM (Denoising Diffusion Implicit Models): deterministic sampling, accelerated generation
- [ ] Score-based models: score matching, Langevin dynamics, noise-conditional score networks (NCSN)
- [ ] Score SDE framework: unified view (Song et al.)
- [ ] Classifier guidance & classifier-free guidance (CFG): guidance scale
- [ ] Latent Diffusion Models (LDM): encoding to latent space, VQ-VAE / VAE encoder
- [ ] Stable Diffusion: architecture (VAE + U-Net + CLIP text encoder), conditioning mechanism, cross-attention
- [ ] SDXL, Stable Diffusion 3: improved architectures, DiT backbone
- [ ] DiT (Diffusion Transformer): replacing U-Net with Transformer
- [ ] Consistency models: single-step generation
- [ ] Rectified flow / flow matching
- [ ] ControlNet: adding spatial conditioning (pose, edges, depth)
- [ ] IP-Adapter: image prompt conditioning
- [ ] DreamBooth: subject-driven fine-tuning with few images
- [ ] LoRA for diffusion models
- [ ] Sampling acceleration: DPM-Solver, PNDM, UniPC
- [ ] Cascaded diffusion: low-res → high-res (Imagen, DALL-E 2)

### 26. Other Generative Models

#### 26.1 Normalizing Flows

- [ ] Change of variables formula, Jacobian determinant
- [ ] Coupling layers: NICE, RealNVP, Glow
- [ ] Autoregressive flows: MAF, IAF
- [ ] Continuous normalizing flows (Neural ODE)
- [ ] Flow matching (a bridge between flows and diffusion)

#### 26.2 Energy-Based Models (EBMs)

- [ ] Energy function, Boltzmann distribution
- [ ] Training: contrastive divergence, score matching, noise contrastive estimation (NCE)
- [ ] Restricted Boltzmann Machines (RBMs) — historical
- [ ] Modern EBMs & connections to diffusion models

#### 26.3 Autoregressive Models

- [ ] PixelRNN, PixelCNN, Gated PixelCNN
- [ ] WaveNet for audio generation
- [ ] Autoregressive image models: VQGAN + Transformer (taming transformers)
- [ ] Connections to language models as autoregressive generators

### 2.9 Generative Models

#### 2.9.1 Variational Autoencoders (VAE)

- [ ] Encoder: q(z|x), reparameterization trick
- [ ] Decoder: p(x|z)
- [ ] KL annealing, β-VAE
- [ ] VQ-VAE: discrete latent space, codebook learning
- [ ] Posterior collapse and remedies

#### 2.9.2 Generative Adversarial Networks (GANs)

- [ ] Wasserstein GAN (WGAN): Earth Mover's distance, Lipschitz constraint
- [ ] DCGAN: convolutional generator/discriminator
- [ ] Progressive GAN (ProGAN)
- [ ] BigGAN: class-conditional, batch normalization tricks

#### 2.9.3 Normalizing Flows

- [ ] Bijective transformations, change of variables
- [ ] Glow: 1×1 invertible convolutions
- [ ] Neural ODE connection

#### 2.9.4 Diffusion Models

- [ ] Forward process: Markov chain adding Gaussian noise (β schedule)
- [ ] DDPM: score matching, ε-prediction
- [ ] DDIM: deterministic sampling, fewer steps
- [ ] Noise schedules: linear, cosine, sigmoid
- [ ] Text-to-image: DALL-E 2, Stable Diffusion, Imagen
- [ ] Flow Matching (Stable Diffusion 3, Flux): straight trajectories
- [ ] Distillation for fast sampling
- [ ] Video diffusion: Sora, CogVideo, Wan
- [ ] 3D generation: DreamFusion, Zero123

---

## PART VIII: LARGE LANGUAGE MODELS & GENERATIVE AI

### 27. LLM Pretraining

#### 27.1 Pretraining Objectives & Data

- [ ] Autoregressive language modeling (next-token prediction)
- [ ] Masked language modeling (MLM — BERT-style)
- [ ] Prefix language modeling, span corruption (T5)
- [ ] Pretraining data: web crawl (Common Crawl, C4, The Pile, RedPajama, FineWeb), books, code, curation & filtering, deduplication (MinHash, SimHash, exact dedup)
- [ ] Data quality: filtering heuristics, perplexity filtering, toxicity filtering, PII removal
- [ ] Data mixing strategies: domain proportions, sampling weights
- [ ] Tokenizer training: BPE on pretraining corpus, vocabulary size tradeoffs

#### 27.2 Scaling Laws & Architecture Decisions

- [ ] Scaling laws: Kaplan et al. (2020), Chinchilla (Hoffmann et al., 2022) — compute-optimal training
- [ ] Model size vs dataset size vs compute budget
- [ ] Architecture choices: decoder-only dominance, layer count vs width, FFN ratio
- [ ] Vocabulary size effects on performance
- [ ] Context length: training for long context, position interpolation, YaRN, NTK-aware scaling
- [ ] Training infrastructure: data parallelism, tensor parallelism, pipeline parallelism, 3D parallelism, ZeRO (DeepSpeed), FSDP (PyTorch), Megatron-LM

#### 27.3 Notable LLM Families

- [ ] GPT series: GPT-1, GPT-2, GPT-3, GPT-3.5, GPT-4, GPT-4o
- [ ] LLaMA family: LLaMA, LLaMA 2, LLaMA 3, LLaMA 3.1
- [ ] Mistral, Mixtral (MoE)
- [ ] Gemini / PaLM family (Google)
- [ ] Claude family (Anthropic)
- [ ] Qwen, Yi, DeepSeek, Phi series (small efficient models)
- [ ] Falcon, MPT, BLOOM (open models)
- [ ] Command R (Cohere), Grok (xAI)

### 28. LLM Fine-Tuning & Alignment

#### 28.1 Supervised Fine-Tuning (SFT)

- [ ] Instruction tuning: instruction-response pairs, formatting (Alpaca, ShareGPT, ChatML)
- [ ] Full fine-tuning vs parameter-efficient fine-tuning
- [ ] Data quality for SFT: LIMA ('Less Is More for Alignment'), Orca, WizardLM
- [ ] Multi-task fine-tuning (FLAN, T0)
- [ ] Catastrophic forgetting & mitigation

#### 28.2 Parameter-Efficient Fine-Tuning (PEFT)

- [ ] LoRA (Low-Rank Adaptation): rank decomposition, α scaling, target modules
- [ ] QLoRA: quantized base model + LoRA adapters, NormalFloat (NF4) quantization, double quantization, paged optimizers
- [ ] DoRA (Weight-Decomposed Low-Rank Adaptation)
- [ ] Adapter layers (Houlsby et al.): bottleneck adapters
- [ ] Prefix tuning & prompt tuning (soft prompts)
- [ ] IA³ (Infused Adapter by Inhibiting and Amplifying Inner Activations)
- [ ] (LoRA variants: LoRA+, AdaLoRA, rsLoRA, LoRA-FA, VeRA, GaLore)

#### 28.3 RLHF & Preference Optimization

- [ ] Reinforcement Learning from Human Feedback (RLHF) pipeline: SFT → Reward Model → RL (PPO)
- [ ] Reward modeling: Bradley-Terry model, pairwise comparisons, reward hacking
- [ ] PPO for language models: clipping, KL penalty from reference policy
- [ ] Direct Preference Optimization (DPO): implicit reward model, reference-free variant
- [ ] ORPO, SimPO, KTO, IPO: alternative preference optimization methods
- [ ] Constitutional AI (CAI): self-critique, revision, RLAIF
- [ ] Rejection sampling fine-tuning (Best-of-N)
- [ ] SPIN (Self-Play Fine-Tuning)
- [ ] Online vs offline preference optimization

#### 28.4 Model Merging & Composition

- [ ] Model averaging, SLERP (Spherical Linear Interpolation)
- [ ] Task arithmetic: adding/subtracting task vectors
- [ ] TIES-Merging, DARE
- [ ] MoE from merged experts
- [ ] Model soups

### 29. LLM Inference & Deployment

#### 29.1 Quantization

- [ ] Weight quantization: INT8, INT4, FP8, NF4
- [ ] Post-training quantization (PTQ): GPTQ, AWQ, SqueezeLLM, QuIP
- [ ] Quantization-aware training (QAT)
- [ ] Activation quantization: SmoothQuant, LLM.int8() (mixed-precision decomposition)
- [ ] GGUF / GGML format (llama.cpp ecosystem)
- [ ] Quantization evaluation: perplexity degradation, task-specific benchmarks

#### 29.2 Inference Optimization

- [ ] KV-cache: memory management, paged attention (vLLM)
- [ ] Speculative decoding: draft model + verification
- [ ] Continuous batching / dynamic batching
- [ ] Tensor parallelism for inference
- [ ] Model distillation for smaller deployment models
- [ ] Pruning: unstructured, structured, SparseGPT, Wanda
- [ ] Inference frameworks: vLLM, TGI (Text Generation Inference), TensorRT-LLM, llama.cpp, Ollama, MLC-LLM
- [ ] Serving: throughput vs latency tradeoffs, SLOs, autoscaling

#### 29.3 Decoding Strategies

- [ ] Greedy decoding
- [ ] Beam search: beam width, length penalty
- [ ] Temperature scaling
- [ ] Top-k sampling, top-p (nucleus) sampling, min-p sampling
- [ ] Typical sampling, eta sampling, mirostat
- [ ] Repetition penalty, presence penalty, frequency penalty
- [ ] Structured/constrained decoding: JSON mode, grammar-based (GBNF)
- [ ] Watermarking LLM outputs

### 30. Prompt Engineering & In-Context Learning

#### 30.1 Prompting Techniques

- [ ] Zero-shot prompting
- [ ] Few-shot prompting: example selection, ordering effects
- [ ] Chain-of-Thought (CoT) prompting: step-by-step reasoning
- [ ] Zero-shot CoT ('Let's think step by step')
- [ ] Self-Consistency: multiple CoT paths + majority voting
- [ ] Tree of Thoughts (ToT): branching reasoning paths
- [ ] Graph of Thoughts
- [ ] ReAct (Reasoning + Acting): interleaving thought & tool use
- [ ] Automatic prompt optimization: APE, DSPy, OPRO
- [ ] System prompts & persona prompting
- [ ] Role prompting & context setting
- [ ] Prompt chaining & decomposition

#### 30.2 Retrieval-Augmented Generation (RAG)

- [ ] RAG pipeline: retrieve → augment → generate
- [ ] Document chunking strategies: fixed-size, semantic, recursive, sentence-based, parent-child
- [ ] Embedding models: OpenAI embeddings, Sentence-BERT, E5, BGE, GTE, Jina, Cohere Embed
- [ ] Vector databases: Pinecone, Weaviate, Qdrant, Milvus, Chroma, FAISS, pgvector
- [ ] Similarity search: cosine similarity, L2 distance, inner product, HNSW, IVF
- [ ] Hybrid search: dense + sparse (BM25) + reranking
- [ ] Reranking: cross-encoders, ColBERT, Cohere Rerank
- [ ] Advanced RAG: query transformation (HyDE, step-back prompting), multi-hop retrieval, iterative retrieval, self-RAG, CRAG (Corrective RAG)
- [ ] Evaluation: faithfulness, relevance, context precision/recall (RAGAS framework)
- [ ] GraphRAG: knowledge-graph-augmented retrieval
- [ ] Agentic RAG: routing, query planning, tool selection

#### 30.3 LLM Evaluation & Benchmarks

- [ ] Perplexity as intrinsic metric
- [ ] Task benchmarks: MMLU, HellaSwag, ARC, TruthfulQA, GSM8K, MATH, HumanEval, MBPP, BBH
- [ ] Chat/instruction benchmarks: MT-Bench, AlpacaEval, Chatbot Arena (Elo rating)
- [ ] Safety benchmarks: ToxiGen, RealToxicityPrompts, BBQ (bias), HarmBench
- [ ] LLM-as-judge evaluation: G-Eval, pairwise comparison
- [ ] Human evaluation: Likert scales, pairwise preference, inter-annotator agreement (Kappa, Krippendorff's alpha)
- [ ] Contamination / data leakage in benchmarks

### 31. AI Agents & Tool Use

#### 31.1 LLM Agents

- [ ] Agent frameworks: LangChain, LlamaIndex, CrewAI, AutoGen, Semantic Kernel
- [ ] Tool use / function calling: JSON schema, structured output
- [ ] Planning: task decomposition, plan-and-solve, hierarchical planning
- [ ] Memory: short-term (context window), long-term (vector store), episodic, working memory
- [ ] Reflection & self-correction: Reflexion, self-refine
- [ ] Multi-agent systems: debate, collaboration, specialization
- [ ] Code generation agents: code interpreter, sandboxed execution
- [ ] Web browsing agents
- [ ] MCP (Model Context Protocol): tool integration standard

#### 31.2 Advanced Agent Patterns

- [ ] ReAct pattern: reasoning traces + actions
- [ ] Plan-Execute-Reflect loop
- [ ] Autonomous agents: AutoGPT, BabyAGI, Voyager (Minecraft)
- [ ] Agent evaluation: success rate, efficiency, safety
- [ ] Guardrails & safety in agent systems
- [ ] Human-in-the-loop agent workflows

### 3.4 Large Language Model (LLM) Training

#### 3.4.1 Pre-Training

- [ ] Chinchilla scaling laws: tokens = 20x parameters
- [ ] Distributed training strategies (see MLOps section)
- [ ] Gradient checkpointing
- [ ] Loss spikes, recovery techniques

#### 3.4.2 Instruction Fine-Tuning (SFT)

- [ ] Supervised fine-tuning on instruction datasets
- [ ] FLAN, Alpaca, Vicuna, OpenHermes
- [ ] Multi-task instruction following
- [ ] Chat format, system prompts

#### 3.4.3 Alignment: RLHF

- [ ] Step 1: SFT on high-quality prompts
- [ ] Step 2: Reward Model training from human preferences
- [ ] Step 3: PPO (Proximal Policy Optimization) fine-tuning
- [ ] PPO clip objective, value function
- [ ] InstructGPT RLHF pipeline
- [ ] Reward hacking, overoptimization

#### 3.4.4 Alignment: RLAIF and Alternatives

- [ ] DPO derivation from RLHF
- [ ] RLAIF: AI feedback instead of human

### 3.5 Parameter-Efficient Fine-Tuning (PEFT)

- [ ] LoRA (Low-Rank Adaptation): A and B matrices, rank r
- [ ] LoRA math: W = W_0 + AB, where A∈R^{d×r}, B∈R^{r×k}
- [ ] LoRA rank selection, alpha scaling
- [ ] QLoRA: LoRA on 4-bit quantized model
- [ ] LoRA+, AdaLoRA, Flora
- [ ] Prefix Tuning: virtual tokens prepended
- [ ] P-Tuning v2
- [ ] BitFit: only bias terms

### 3.6 LLM Inference & Serving

#### 3.6.1 Decoding Strategies

- [ ] Contrastive search
- [ ] Medusa: parallel decoding heads

#### 3.6.2 KV Cache

- [ ] Key-Value cache for autoregressive generation
- [ ] Memory footprint: 2 × n_layers × n_heads × d_head × seq_len × 2 bytes
- [ ] Prefix caching
- [ ] RadixAttention

#### 3.6.3 Quantization

- [ ] GGUF / llama.cpp quantization formats
- [ ] Activation quantization challenges
- [ ] SmoothQuant: migrating outliers

#### 3.6.4 Serving Systems

- [ ] vLLM: paged attention, high throughput
- [ ] Throughput vs latency trade-offs

### 3.7 Prompt Engineering & Context Learning

- [ ] Program-Aided Language models (PAL)
- [ ] Prompt sensitivity and robustness
- [ ] Prompt injection attacks

### 3.8 RAG (Retrieval-Augmented Generation)

- [ ] Motivation: reduce hallucination, knowledge cutoff
- [ ] Naive RAG: retrieve → chunk → embed → generate
- [ ] Advanced RAG: hybrid retrieval, re-ranking
- [ ] Modular RAG: routing, fusion, adaptive
- [ ] Sparse retrieval: BM25
- [ ] Hybrid: RRF (Reciprocal Rank Fusion)
- [ ] Re-ranking: cross-encoder vs bi-encoder
- [ ] HyDE (Hypothetical Document Embedding)
- [ ] Contextual retrieval (Anthropic)
- [ ] Evaluation: RAGAS metrics

### 3.9 LLM Agents & Tool Use

- [ ] ReAct agent loop: thought → action → observation
- [ ] Planning: sequential, parallel, hierarchical
- [ ] Memory: episodic, semantic, procedural
- [ ] Agent evaluation: trajectory, task success rate
- [ ] Safety in agents: tool restrictions, guardrails

### 3.10 LLM Evaluation

- [ ] BIG-Bench, BIG-Bench Hard
- [ ] Hallucination benchmarks: TruthfulQA, FActScorE

---

## PART IX: MULTIMODAL AI

### 32. Vision-Language Models

#### 32.1 Contrastive Vision-Language Pretraining

- [ ] CLIP: contrastive learning of image-text pairs, zero-shot transfer, prompt engineering for CLIP
- [ ] ALIGN: scaling noisy image-text pairs
- [ ] SigLIP: sigmoid loss for language-image pretraining
- [ ] OpenCLIP: open-source CLIP variants
- [ ] EVA-CLIP: scaling CLIP with EVA ViTs

#### 32.2 Generative Vision-Language Models

- [ ] Flamingo: visual language model with gated cross-attention, few-shot visual reasoning
- [ ] BLIP, BLIP-2: bootstrapping language-image pretraining, Q-Former
- [ ] LLaVA (Large Language and Vision Assistant): visual instruction tuning, projection layer
- [ ] LLaVA-NeXT, LLaVA-OneVision
- [ ] GPT-4V / GPT-4o: multimodal capabilities
- [ ] Gemini: native multimodal training
- [ ] Claude vision capabilities
- [ ] InternVL, Qwen-VL, CogVLM
- [ ] PaLI, PaLI-X: pathways language and image model

#### 32.3 Tasks & Applications

- [ ] Image captioning: COCO Captions, show-and-tell, CIDEr/SPICE metrics
- [ ] Visual Question Answering (VQA): VQAv2, OK-VQA, GQA
- [ ] Visual grounding / referring expression comprehension
- [ ] Visual reasoning: NLVR, Winoground
- [ ] Image-text retrieval: zero-shot, fine-tuned
- [ ] Text-to-image generation (see Diffusion Models)
- [ ] Multimodal document understanding: charts, infographics, screenshots

### 33. Text-to-Image, Video & Audio

#### 33.1 Text-to-Image Generation

- [ ] DALL-E, DALL-E 2 (unCLIP): CLIP text embedding + prior + decoder
- [ ] DALL-E 3: improved prompt following with synthetic captions
- [ ] Stable Diffusion: open-source latent diffusion
- [ ] Imagen: large T5 text encoder + cascaded diffusion
- [ ] Midjourney architecture insights
- [ ] FLUX models
- [ ] Evaluation: FID, CLIPScore, human preference (Pick-a-Pic, HPS)

#### 33.2 Text-to-Video

- [ ] Video diffusion models: temporal layers, 3D U-Net, temporal attention
- [ ] Sora (OpenAI): spacetime patches, long-form coherent video
- [ ] Runway Gen-2/Gen-3, Pika, Kling, Hailuo
- [ ] AnimateDiff: animating text-to-image models
- [ ] Video editing: InstructPix2Pix for video, TokenFlow

#### 33.3 Multimodal Fusion Strategies

- [ ] Early fusion: concatenation at input level
- [ ] Late fusion: separate encoders, combined at decision level
- [ ] Cross-modal attention / cross-attention fusion
- [ ] Bottleneck fusion: Perceiver, Q-Former
- [ ] Modality dropout for robustness
- [ ] Alignment: contrastive alignment (CLIP-style), generative alignment

### 5.1 Contrastive Multimodal Learning

#### 5.1.1 CLIP (Contrastive Language-Image Pre-Training)

- [ ] Dual encoder: image encoder (ViT/ResNet) + text encoder (Transformer)
- [ ] InfoNCE contrastive loss on (image, text) pairs
- [ ] Zero-shot classification via text prompts
- [ ] 400M image-text pairs from internet
- [ ] Temperature parameter in CLIP
- [ ] Applications: zero-shot, image search, text-to-image conditioning

#### 5.1.2 CLIP Variants

- [ ] ALIGN: noise-resistant contrastive training at scale
- [ ] FLAVA: foundational language-and-vision alignment
- [ ] DeCLIP, SLIP, YCLIP
- [ ] ImageBind: binding 6 modalities in one space
- [ ] AudioCLIP

### 5.2 Vision-Language Models (VLMs)

#### 5.2.1 Architecture Patterns

- [ ] Dual stream: separate vision + language encoders
- [ ] Single stream: joint processing
- [ ] Q-Former (Querying Transformer) — BLIP-2
- [ ] MLP projector (LLaVA)
- [ ] Learnable query tokens (Flamingo)

#### 5.2.2 Key VLM Models

- [ ] Flamingo: interleaved image-text, few-shot
- [ ] BLIP: bootstrapped language-image pre-training
- [ ] BLIP-2: Q-Former between frozen vision encoder and frozen LLM
- [ ] InstructBLIP: instruction tuning for VQA
- [ ] LLaVA 1.5, LLaVA-NeXT: AnyRes, higher resolution
- [ ] GPT-4V: closed-source MLLM
- [ ] InternVL, InternLM-XComposer
- [ ] Qwen-VL, Qwen2-VL
- [ ] PaliGemma, PaliGemma 2

#### 5.2.3 VLM Tasks

- [ ] Visual commonsense reasoning
- [ ] Text-rich document understanding (DocVQA)
- [ ] Chart/diagram QA (ChartQA)
- [ ] OCR and document parsing
- [ ] Medical image VQA

### 5.3 Multimodal Training

- [ ] Vision-language alignment pre-training
- [ ] Instruction tuning with image-text pairs
- [ ] Mixed training (text-only + multimodal batches)
- [ ] Dynamic resolution: handling various aspect ratios
- [ ] M-RoPE (multi-dimensional rotary position embeddings)
- [ ] Pixel shuffle for feature compression
- [ ] AnyRes: adaptive image slicing
- [ ] Interleaved multimodal sequences

### 5.4 Audio & Speech

- [ ] Speech representation: MFCC, log mel spectrogram
- [ ] Whisper: weakly supervised speech recognition
- [ ] HuBERT: hidden unit BERT for speech
- [ ] Speech Synthesis: Tacotron 2, FastSpeech 2
- [ ] Neural vocoder: WaveNet, HiFi-GAN
- [ ] Audio generation: AudioGen, MusicGen, AudioLDM
- [ ] Multimodal with audio: AV-HuBERT, AudioCLIP

### 5.5 Video-Language Models

- [ ] Video captioning, VideoQA
- [ ] Video retrieval
- [ ] Video-LLaVA, VideoChat, MiniGPT4-Video
- [ ] Long video understanding: streaming attention
- [ ] Temporal grounding

### 5.6 Multimodal Evaluation

- [ ] VQAv2, GQA, TextVQA, MMBench
- [ ] MME, MMMU (massive multitask)
- [ ] SeedBench, MMStar
- [ ] HallusionBench (hallucination)
- [ ] POPE (object hallucination)

---

## PART X: RECOMMENDATION SYSTEMS

### 34. Recommendation Systems

#### 34.1 Foundations & Classical Methods

- [ ] Content-based filtering: item features, user profiles, TF-IDF for items, cosine similarity
- [ ] Collaborative filtering: user-based CF, item-based CF, neighborhood methods
- [ ] Matrix factorization: SVD, ALS (Alternating Least Squares), SVD++, NMF
- [ ] Implicit feedback: clicks, views, purchases vs explicit ratings
- [ ] BPR (Bayesian Personalized Ranking): pairwise optimization for implicit feedback
- [ ] Hybrid methods: weighted, switching, cascade, feature augmentation
- [ ] Cold start problem: for new users, new items, solutions (side information, content-based fallback, popularity-based)

#### 34.2 Deep Learning for RecSys

- [ ] Neural Collaborative Filtering (NCF): MLP replacing inner product
- [ ] Autoencoders for CF: AutoRec, Mult-VAE, EASE^R
- [ ] Wide & Deep: memorization (wide) + generalization (deep)
- [ ] DeepFM: factorization machines + deep neural network
- [ ] DCN (Deep & Cross Network): explicit feature crosses
- [ ] DIN (Deep Interest Network): attention over user behavior sequence
- [ ] DIEN (Deep Interest Evolution Network): interest evolution with GRU
- [ ] BST (Behavior Sequence Transformer): Transformer for user sequence
- [ ] SASRec: self-attentive sequential recommendation
- [ ] BERT4Rec: bidirectional model for sequential recommendation
- [ ] GNN-based recommendations: PinSage, LightGCN, NGCF
- [ ] Two-tower model: separate user & item encoders, approximate nearest neighbour retrieval

#### 34.3 Industrial RecSys Pipeline

- [ ] Multi-stage architecture: candidate generation → pre-ranking → ranking → re-ranking
- [ ] Candidate generation: approximate nearest neighbour (ANN), HNSW, FAISS, ScaNN
- [ ] Feature engineering for RecSys: user features, item features, context features, cross features
- [ ] Click-Through Rate (CTR) prediction: logistic regression, GBDT, DNN, multi-task models
- [ ] Multi-task learning in RecSys: ESMM (Entire Space Multi-Task Model), MMOE (Multi-gate Mixture-of-Experts), PLE
- [ ] Position bias & debiasing: inverse propensity weighting, position features
- [ ] Diversity & novelty in recommendations: MMR (Maximal Marginal Relevance), DPP (Determinantal Point Processes)
- [ ] Exploration vs exploitation: ε-greedy, Thompson sampling, UCB, contextual bandits (LinUCB)
- [ ] Real-time recommendation: online learning, feature freshness
- [ ] Session-based recommendations: GRU4Rec, SR-GNN

#### 34.4 Evaluation & Metrics

- [ ] Offline metrics: Precision@K, Recall@K, F1@K, Hit Rate@K, NDCG@K, MAP, MRR, AUC, log loss, coverage, diversity, novelty, serendipity
- [ ] Online metrics: CTR, conversion rate, revenue per impression, engagement time, retention
- [ ] A/B testing for RecSys: interleaving experiments, long-term effects
- [ ] Bias in offline evaluation: popularity bias, selection bias

#### 34.5 LLM-Enhanced Recommendations

- [ ] LLMs as recommenders: prompt-based ranking, in-context recommendation
- [ ] LLMs for feature enrichment: generating item descriptions, user intent extraction
- [ ] Conversational recommendation systems
- [ ] Knowledge-graph-enhanced recommendations

### 6.1 Foundational Concepts

- [ ] Collaborative Filtering (CF) vs Content-Based Filtering vs Hybrid
- [ ] Cold start problem: user cold start, item cold start
- [ ] Popularity bias, filter bubble, echo chamber
- [ ] User-item interaction matrix: sparsity
- [ ] Long-tail distribution of items
- [ ] Evaluation: offline (NDCG, MRR, HR@k) vs online (CTR, GMV)
- [ ] Position bias in implicit feedback

### 6.2 Memory-Based Collaborative Filtering

- [ ] User-based CF: find similar users, recommend their items
- [ ] Item-based CF: find similar items based on co-interaction
- [ ] Similarity metrics: cosine, Pearson, Jaccard
- [ ] Neighborhood size selection
- [ ] Sparsity problem, scalability

### 6.3 Matrix Factorization

- [ ] Basic MF: P × Q^T ≈ R (user × factor, item × factor)
- [ ] Regularized MF with SGD
- [ ] ALS (Alternating Least Squares): parallelizable, implicit feedback
- [ ] Weighted ALS for implicit feedback (hu et al. 2008)
- [ ] SVD++: incorporating implicit feedback as side information
- [ ] PMF (Probabilistic Matrix Factorization): Bayesian
- [ ] NMF (Non-negative MF)
- [ ] TimeSVD++: temporal dynamics
- [ ] Factorization Machines (FM): feature interaction
- [ ] Field-aware FM (FFM)

### 6.4 Deep Learning for RecSys

#### 6.4.1 Neural Collaborative Filtering

- [ ] NCF: GMF + MLP branches combined (NeuMF)
- [ ] Deep MF: deep feature learning
- [ ] AutoRec: autoencoder for CF
- [ ] CDAE (Collaborative Denoising Autoencoder)
- [ ] EASE: embarrassingly shallow autoencoder

#### 6.4.2 Session-Based & Sequential Recommendation

- [ ] GRU4Rec: RNN for session-based recommendation
- [ ] NARM: attention-based GRU
- [ ] S3-Rec: self-supervised pre-training
- [ ] Position-aware attention

#### 6.4.3 Two-Tower Models

- [ ] User tower: user features → user embedding
- [ ] Training: in-batch negatives, hard negatives
- [ ] Hard negative mining
- [ ] Feature engineering for each tower
- [ ] DSSM, YoutubeNet
- [ ] Serving: FAISS ANN search

#### 6.4.4 Wide & Deep Learning

- [ ] Wide component: memorization (cross-product features)
- [ ] Deep component: generalization
- [ ] Google Play recommendation
- [ ] DCN v2: improved cross network
- [ ] xDeepFM: CIN (Compressed Interaction Network)
- [ ] AutoInt: self-attention for feature interaction
- [ ] DLRM (Deep Learning Recommendation Model — Meta)

#### 6.4.5 CTR Prediction Models

- [ ] LR → FM → DeepFM → DCN → DIEN
- [ ] DeepFM: FM + deep component
- [ ] DIN (Deep Interest Network): adaptive activation
- [ ] Target attention for user behavior modeling

### 6.5 Multi-Stage Recommendation Pipeline

- [ ] Stage 1: Candidate Generation / Retrieval (millions → thousands)
- [ ] Stage 2: Rough Ranking / Pre-ranking (thousands → hundreds)
- [ ] Stage 3: Fine Ranking (hundreds → dozens)
- [ ] Stage 4: Re-ranking, filtering, diversity injection
- [ ] Calibration between stages

### 6.6 Learning to Rank

- [ ] Pointwise: regression/classification per item
- [ ] Pairwise: BPR, RankNet, LambdaRank
- [ ] Listwise: ListNet, LambdaMART, NDCG optimization
- [ ] LambdaMART: gradient boosting for ranking
- [ ] Direct NDCG optimization challenges (non-differentiable)

### 6.7 Knowledge Graph for RecSys

- [ ] KG-based CF: RippleNet, KGCN, KGNN-LS
- [ ] Entity and relation embeddings
- [ ] Path-based reasoning
- [ ] KGAT: knowledge graph attention network

### 6.8 Graph Neural Networks for RecSys

- [ ] PinSage: GraphSAGE for Pinterest
- [ ] NGCF: high-order connectivity
- [ ] LightGCN: simplified GCN (no feature transformation)
- [ ] DGCF: disentangled graph CF
- [ ] Bipartite graph: users and items

### 6.9 Context-Aware & Bandit-Based RecSys

- [ ] Context: time, location, device, session
- [ ] CARS (Context-Aware Recommender Systems)
- [ ] Multi-Armed Bandit (MAB): ε-greedy, UCB, Thompson Sampling
- [ ] Explore-exploit in news/ad recommendation
- [ ] Off-policy evaluation: IPS (Inverse Propensity Scoring)
- [ ] Counterfactual learning

### 6.10 Multi-Task Learning in RecSys

- [ ] Shared bottom architecture
- [ ] PLE (Progressive Layered Extraction)
- [ ] Objectives: CTR, CVR, dwell time, satisfaction
- [ ] Task weighting strategies

### 6.11 LLMs for Recommendation

- [ ] P5: prompting for recommendation as text generation
- [ ] TALLRec: text alignment for LLM recommendation
- [ ] BIGRec, LLaRA
- [ ] Semantic IDs (indexing items for LLMs)

### 6.12 Feature Stores & Real-Time Serving

- [ ] Online vs offline features
- [ ] Feature store: Feast, Tecton, Vertex AI Feature Store
- [ ] Near-real-time feature computation
- [ ] Feature freshness trade-offs
- [ ] Embeddings storage and retrieval at scale

---

## PART XI: REINFORCEMENT LEARNING

### 35. Reinforcement Learning

#### 35.1 Foundations

- [ ] Markov Decision Process (MDP): states, actions, transition probabilities, rewards, discount factor γ
- [ ] Partially Observable MDP (POMDP)
- [ ] Return, value function V(s), action-value function Q(s,a)
- [ ] Bellman expectation equation, Bellman optimality equation
- [ ] Policy: deterministic vs stochastic
- [ ] Exploration vs exploitation: ε-greedy, Boltzmann (softmax), UCB, optimism in the face of uncertainty

#### 35.2 Tabular Methods

- [ ] Dynamic programming: policy evaluation, policy iteration, value iteration
- [ ] Monte Carlo methods: first-visit, every-visit, off-policy with importance sampling
- [ ] Temporal Difference (TD) learning: TD(0), TD(λ), eligibility traces
- [ ] Q-learning: off-policy TD control, convergence guarantees
- [ ] SARSA: on-policy TD control
- [ ] n-step methods

#### 35.3 Deep Reinforcement Learning

- [ ] DQN (Deep Q-Network): experience replay, target network, Huber loss
- [ ] Double DQN: overestimation bias correction
- [ ] Dueling DQN: separate value & advantage streams
- [ ] Prioritized experience replay
- [ ] Rainbow DQN: combining multiple improvements
- [ ] C51 / QR-DQN: distributional RL
- [ ] Noisy Networks: parametric noise for exploration

#### 35.4 Policy Gradient Methods

- [ ] REINFORCE algorithm: likelihood ratio gradient, baseline subtraction
- [ ] Actor-Critic methods: separate policy (actor) & value (critic) networks
- [ ] A2C (Advantage Actor-Critic), A3C (Asynchronous A3C)
- [ ] GAE (Generalized Advantage Estimation): λ-weighted advantage
- [ ] PPO (Proximal Policy Optimization): clipped surrogate objective, trust region alternative
- [ ] TRPO (Trust Region Policy Optimization): KL divergence constraint, conjugate gradient
- [ ] SAC (Soft Actor-Critic): maximum entropy RL, temperature α, continuous action spaces
- [ ] TD3 (Twin Delayed DDPG): clipped double Q, delayed policy updates, target smoothing
- [ ] DDPG (Deep Deterministic Policy Gradient): continuous actions, actor-critic

#### 35.5 Model-Based RL

- [ ] World models: learning dynamics models, Dreamer (v1, v2, v3)
- [ ] Dyna architecture: model-based data augmentation
- [ ] MBPO (Model-Based Policy Optimization)
- [ ] MuZero: learned model without explicit state representation
- [ ] Planning with learned models: Monte Carlo Tree Search (MCTS)

#### 35.6 Advanced RL Topics

- [ ] Multi-agent RL: cooperative, competitive, mixed, MAPPO, QMIX
- [ ] Inverse RL: learning reward functions from expert demonstrations
- [ ] Imitation learning: behavioral cloning, DAgger (Dataset Aggregation)
- [ ] Offline RL: learning from fixed datasets, CQL (Conservative Q-Learning), IQL, Decision Transformer
- [ ] Hierarchical RL: options framework, feudal networks, goal-conditioned RL
- [ ] Reward shaping: potential-based shaping
- [ ] Curriculum learning in RL: automatic curriculum
- [ ] Meta-RL: learning to learn, MAML for RL, RL²
- [ ] Sim-to-real transfer: domain randomization, system identification
- [ ] RLHF (connection to LLM alignment — see Section 28)
- [ ] Safe RL: constrained MDPs, risk-sensitive RL

### 7.1 RL Foundations

- [ ] Agent, environment, state, action, reward, policy
- [ ] Markov Decision Process (MDP): (S, A, P, R, γ)
- [ ] Markov property
- [ ] Return: discounted cumulative reward
- [ ] Discount factor γ and horizon trade-offs
- [ ] Optimal policy, Bellman equation
- [ ] Policy evaluation, policy improvement

### 7.2 Model-Free Methods

#### 7.2.1 Temporal Difference Learning

- [ ] TD(0) update rule
- [ ] Expected SARSA

#### 7.2.2 Deep Q-Networks (DQN)

- [ ] Experience replay buffer
- [ ] Target network: fixed for stability
- [ ] Epsilon-greedy exploration
- [ ] Double DQN: decouple selection and evaluation
- [ ] Dueling DQN: V(s) + A(s,a)

### 7.3 Policy Gradient Methods

- [ ] REINFORCE algorithm: gradient of log π
- [ ] Baseline subtraction for variance reduction

### 7.4 Model-Based RL

- [ ] Dyna-Q: planning with learned model
- [ ] World models: RSSM, DreamerV3
- [ ] MuZero: planning without dynamics model
- [ ] AlphaZero: MCTS + neural network

### 7.5 Multi-Agent RL (MARL)

- [ ] CTDE (Centralized Training, Decentralized Execution)
- [ ] QMIX, VDN: value decomposition
- [ ] MADDPG: multi-agent DDPG

### 7.6 Offline RL

- [ ] Learning from fixed dataset (no environment interaction)
- [ ] Distribution shift problem
- [ ] Decision Transformer: RL as sequence modeling
- [ ] Trajectory Transformer

---

## PART XII: GRAPH NEURAL NETWORKS

### 36. Graph Neural Networks

#### 36.1 Foundations

- [ ] Graph representations: adjacency matrix, adjacency list, edge list
- [ ] Node features, edge features, graph-level features
- [ ] Message passing framework: aggregate, update, readout
- [ ] Over-smoothing & over-squashing problems

#### 36.2 GNN Architectures

- [ ] GCN (Graph Convolutional Network): spectral motivation, normalized adjacency
- [ ] GraphSAGE: sampling & aggregation (mean, LSTM, pooling)
- [ ] GAT (Graph Attention Network): attention coefficients for neighbours
- [ ] GIN (Graph Isomorphism Network): WL test connection, sum aggregation
- [ ] GatedGCN, PNA (Principal Neighbourhood Aggregation)
- [ ] Graph Transformers: Graphormer, GPS (General Powerful Scalable)
- [ ] Heterogeneous GNNs: R-GCN (Relational GCN), HAN (Heterogeneous Attention Network)
- [ ] Temporal/dynamic GNNs: TGAT, TGN

#### 36.3 Tasks & Applications

- [ ] Node classification: semi-supervised setting (Cora, Citeseer, PubMed)
- [ ] Link prediction: knowledge graph completion, recommendation
- [ ] Graph classification: molecular property prediction, social network analysis
- [ ] Graph generation: GraphRNN, molecular generation (GCPN, MolGAN, DiGress)
- [ ] Community detection with GNNs
- [ ] Traffic prediction, fraud detection on graphs

#### 36.4 Knowledge Graphs

- [ ] Knowledge graph structure: entities, relations, triples (h, r, t)
- [ ] Knowledge graph embeddings: TransE, TransR, DistMult, ComplEx, RotatE
- [ ] Knowledge graph completion (link prediction)
- [ ] Knowledge-grounded NLP: ERNIE, K-BERT, KGAT
- [ ] Ontology learning & reasoning

### 2.12 Graph Neural Networks (GNNs)

#### 2.12.1 Foundations

- [ ] Graph representation: nodes, edges, adjacency matrix, degree matrix
- [ ] Spectral graph convolution
- [ ] Spatial graph convolution

#### 2.12.2 GNN Architectures

- [ ] GAT (Graph Attention Network): attention-weighted aggregation
- [ ] GIN (Graph Isomorphism Network): Weisfeiler-Lehman test
- [ ] MPNN (Message Passing Neural Network)
- [ ] Edge convolution (DGCNN)

#### 2.12.3 Applications & Challenges

- [ ] Node classification, link prediction, graph classification
- [ ] Oversmoothing problem
- [ ] Scalability: mini-batch graph training
- [ ] Heterogeneous graphs

---

## PART XIII: TIME SERIES & FORECASTING

### 37. Time Series Analysis

#### 37.1 Classical Methods

- [ ] Time series components: trend, seasonality, cyclic, residual
- [ ] Decomposition: additive vs multiplicative, STL decomposition
- [ ] Stationarity: ADF test (Augmented Dickey-Fuller), KPSS test, differencing
- [ ] Autocorrelation (ACF) & partial autocorrelation (PACF)
- [ ] AR (AutoRegressive), MA (Moving Average), ARMA, ARIMA, SARIMA
- [ ] Exponential smoothing: simple, Holt (trend), Holt-Winters (trend + seasonality), ETS framework
- [ ] VAR (Vector AutoRegression) for multivariate time series
- [ ] GARCH models: volatility modeling in finance
- [ ] Prophet (Facebook/Meta): additive model, changepoints, holidays, Fourier terms

#### 37.2 Deep Learning for Time Series

- [ ] RNN/LSTM/GRU for time series (see Section 20)
- [ ] Temporal Convolutional Networks (TCN): causal convolutions, dilated convolutions
- [ ] WaveNet architecture
- [ ] DeepAR: autoregressive probabilistic forecasting
- [ ] N-BEATS: basis expansion, interpretable stacks
- [ ] N-HiTS: hierarchical interpolation
- [ ] Temporal Fusion Transformers (TFT): multi-horizon, variable selection, interpretable attention
- [ ] Informer, Autoformer, FEDformer, PatchTST: Transformer variants for long-horizon forecasting
- [ ] TimesNet: temporal 2D-variation modeling
- [ ] TimeGPT, Chronos, Moirai: foundation models for time series

#### 37.3 Anomaly Detection in Time Series

- [ ] Statistical methods: z-score, moving average deviation, control charts
- [ ] Machine learning: Isolation Forest on rolling features, autoencoder reconstruction error
- [ ] Deep learning: LSTM-based anomaly detection, Transformer-based (Anomaly Transformer)
- [ ] Change point detection: PELT, Bayesian online changepoint detection, ruptures library

#### 37.4 Evaluation & Practical Considerations

- [ ] Metrics: MAE, RMSE, MAPE, sMAPE, MASE, weighted quantile loss (WQL)
- [ ] Backtesting: expanding window, sliding window, purged cross-validation
- [ ] Probabilistic forecasting: prediction intervals, quantile regression, conformal prediction
- [ ] Multi-step forecasting: direct, recursive, MIMO strategies
- [ ] Feature engineering for time series: lag features, rolling statistics, date features, Fourier features

---

## PART XIV: PROBABILISTIC ML & BAYESIAN METHODS

### 38. Probabilistic Machine Learning

#### 38.1 Bayesian Inference

- [ ] Exact inference: conjugate models, analytical posterior
- [ ] Approximate inference: Laplace approximation, variational inference (VI), MCMC
- [ ] Variational inference: ELBO, mean-field approximation, amortized VI
- [ ] MCMC: Metropolis-Hastings, Gibbs sampling, Hamiltonian Monte Carlo (HMC), NUTS (No-U-Turn Sampler)
- [ ] Diagnostics: trace plots, R-hat, effective sample size, divergences

#### 38.2 Gaussian Processes (GPs)

- [ ] GP definition: mean function, covariance (kernel) function
- [ ] Common kernels: RBF/SE, Matérn, periodic, linear, polynomial, spectral mixture
- [ ] GP regression: posterior predictive distribution, marginal likelihood
- [ ] GP classification: Laplace approximation, variational inference
- [ ] Sparse GPs: inducing points, FITC, SVGP
- [ ] Scalable GPs: random Fourier features, Kronecker structure, GPyTorch
- [ ] Deep Gaussian Processes
- [ ] GPs for Bayesian optimization (see Section 5.5)

#### 38.3 Bayesian Neural Networks (BNNs)

- [ ] Weight uncertainty: prior over weights, posterior inference
- [ ] Bayes by Backprop (variational inference for NNs)
- [ ] MC-Dropout: dropout as approximate Bayesian inference
- [ ] Deep ensembles as approximate Bayesian methods
- [ ] Stochastic Weight Averaging - Gaussian (SWAG)
- [ ] Laplace approximation for neural networks
- [ ] Uncertainty quantification: aleatoric vs epistemic uncertainty

#### 38.4 Probabilistic Programming

- [ ] PyMC / PyMC3: model specification, inference, posterior analysis
- [ ] Stan: HMC/NUTS, PyStan, CmdStan
- [ ] NumPyro / Pyro: probabilistic programming on JAX/PyTorch
- [ ] TensorFlow Probability
- [ ] Edward2

---

## PART XV: SPEECH, AUDIO & MULTIMODAL

### 39. Speech & Audio Processing

#### 39.1 Audio Fundamentals

- [ ] Digital audio: sampling rate, bit depth, waveforms
- [ ] Feature extraction: MFCCs (Mel-Frequency Cepstral Coefficients), mel spectrograms, log-mel spectrograms, filter banks
- [ ] Short-Time Fourier Transform (STFT), spectrogram
- [ ] Audio preprocessing: noise reduction, VAD (Voice Activity Detection), normalization

#### 39.2 Automatic Speech Recognition (ASR)

- [ ] Traditional pipeline: acoustic model, language model, decoder
- [ ] End-to-end ASR: CTC-based (DeepSpeech, QuartzNet), attention-based (LAS - Listen Attend Spell)
- [ ] Conformer: CNN + Transformer hybrid for speech
- [ ] Wav2Vec 2.0: self-supervised pretraining, contrastive learning + masking
- [ ] HuBERT: self-supervised with pseudo-labels
- [ ] Whisper (OpenAI): large-scale weakly supervised, multilingual, multitask
- [ ] Streaming / online ASR: RNN-T (RNN Transducer), fast conformer
- [ ] Language model integration: shallow fusion, deep fusion
- [ ] Evaluation: WER (Word Error Rate), CER (Character Error Rate)

#### 39.3 Text-to-Speech (TTS)

- [ ] Traditional: concatenative synthesis, parametric synthesis (HMM-based)
- [ ] Neural TTS: Tacotron, Tacotron 2 (spectrogram prediction + vocoder)
- [ ] Vocoders: WaveNet, WaveRNN, WaveGlow, HiFi-GAN, Vocos
- [ ] Non-autoregressive TTS: FastSpeech, FastSpeech 2, VITS
- [ ] Zero-shot TTS / voice cloning: VALL-E, Bark, XTTS, StyleTTS 2
- [ ] Evaluation: MOS (Mean Opinion Score), PESQ, STOI, speaker similarity

#### 39.4 Other Audio Tasks

- [ ] Speaker verification / identification: speaker embeddings, x-vectors, ECAPA-TDNN
- [ ] Speaker diarization: who spoke when, EEND, clustering-based
- [ ] Audio classification: environmental sounds, AudioSet, PANNs, AST (Audio Spectrogram Transformer)
- [ ] Music generation: Jukebox, MusicLM, MusicGen, Stable Audio
- [ ] Audio-language models: CLAP (contrastive language-audio pretraining)
- [ ] Sound event detection & localization

---

## PART XVI: MLOps & PRODUCTION ML

### 40. MLOps

#### 40.1 Experiment Tracking & Model Registry

- [ ] MLflow: tracking, projects, models, registry
- [ ] Weights & Biases (W&B): experiments, sweeps, artifacts, reports
- [ ] Neptune.ai, Comet ML, ClearML
- [ ] Model versioning & lineage tracking
- [ ] Artifact management: datasets, models, checkpoints

#### 40.2 ML Pipelines & Orchestration

- [ ] Pipeline concepts: DAGs, steps, artifacts, caching
- [ ] Apache Airflow: DAGs, operators, sensors, scheduling
- [ ] Kubeflow Pipelines: Kubernetes-native, components, experiments
- [ ] Prefect, Dagster: modern orchestrators
- [ ] Vertex AI Pipelines (GCP), SageMaker Pipelines (AWS), Azure ML Pipelines
- [ ] ZenML: MLOps framework integration
- [ ] Feature stores: Feast, Tecton, Hopsworks — offline & online serving, feature consistency

#### 40.3 Model Serving & Deployment

- [ ] Serving frameworks: TensorFlow Serving, TorchServe, Triton Inference Server, BentoML, Seldon Core, KServe
- [ ] REST API serving: Flask, FastAPI, Django
- [ ] gRPC for low-latency serving
- [ ] Batch vs real-time inference
- [ ] Edge deployment: TF Lite, ONNX Runtime, CoreML, TensorRT, OpenVINO
- [ ] Model format conversion: ONNX as interchange format
- [ ] A/B testing, canary deployments, shadow deployments, blue-green deployments
- [ ] Feature flags for ML models

#### 40.4 Containerization & Infrastructure

- [ ] Docker: images, containers, Dockerfile, multi-stage builds, GPU support (nvidia-docker)
- [ ] Kubernetes: pods, services, deployments, horizontal pod autoscaling, GPU scheduling
- [ ] Helm charts for ML deployments
- [ ] Infrastructure as Code: Terraform, Pulumi
- [ ] Cloud ML platforms: AWS SageMaker, GCP Vertex AI, Azure ML, Databricks
- [ ] GPU cluster management: SLURM, Ray cluster

#### 40.5 Monitoring & Observability

- [ ] Data drift detection: statistical tests (KS, PSI, chi-squared), monitoring dashboards
- [ ] Concept drift: sudden, gradual, incremental, recurring
- [ ] Model performance monitoring: accuracy degradation, latency, throughput
- [ ] Prediction logging & auditing
- [ ] Tools: Evidently AI, WhyLabs, Arize, Fiddler, NannyML
- [ ] Alerting & automated retraining triggers

#### 40.6 Data Versioning & Reproducibility

- [ ] DVC (Data Version Control): data & model versioning, remotes, pipelines
- [ ] LakeFS: git-like data versioning for data lakes
- [ ] Delta Lake: ACID transactions on data lakes
- [ ] Reproducibility checklist: random seeds, environment pinning, deterministic operations, config files (Hydra, OmegaConf)

#### 40.7 CI/CD for ML

- [ ] Continuous integration: automated testing (unit, integration, model validation)
- [ ] Continuous delivery: automated model deployment pipeline
- [ ] Model validation gates: performance thresholds, fairness checks, latency checks
- [ ] GitHub Actions, GitLab CI, Jenkins for ML
- [ ] Testing ML code: data validation tests, model performance tests, integration tests, smoke tests

### 8.1 ML System Design

- [ ] Requirements gathering: latency, throughput, accuracy, fairness
- [ ] Data pipeline design
- [ ] Feedback loop design
- [ ] Failure mode analysis
- [ ] Chip Huyen's ML system design framework

### 8.2 Distributed Training

#### 8.2.1 Data Parallelism

- [ ] DDP (Distributed Data Parallel): gradients all-reduce
- [ ] FSDP (Fully Sharded Data Parallel): shards params, grads, optimizer states
- [ ] ZeRO (DeepSpeed): Stage 1, 2, 3

#### 8.2.2 Model Parallelism

- [ ] Tensor Parallelism: split layer matrices across devices (Megatron-LM)
- [ ] Pipeline Parallelism: split layers across devices, micro-batches
- [ ] GPipe, PipeDream, Chimera
- [ ] Expert Parallelism for MoE models
- [ ] 3D parallelism: DP + TP + PP

#### 8.2.3 Communication Primitives

- [ ] All-Reduce, All-Gather, Reduce-Scatter
- [ ] NCCL, GLOO backends
- [ ] Ring-AllReduce
- [ ] NVLink, InfiniBand

### 8.3 Model Compression

- [ ] Magnitude pruning, gradient-based pruning
- [ ] Knowledge Distillation: soft labels, teacher-student
- [ ] Self-distillation, online distillation
- [ ] Quantization (see LLM Inference section)
- [ ] Low-rank factorization of weight matrices

### 8.4 Experiment Tracking & Versioning

- [ ] Experiment tracking: MLflow, Weights & Biases, Comet ML
- [ ] Logging metrics, hyperparameters, artifacts
- [ ] Model registry

### 8.5 Model Deployment

- [ ] ONNX export for cross-framework deployment
- [ ] Batching strategies: static, dynamic, adaptive
- [ ] Blue-green deployment, canary releases
- [ ] Shadow deployment
- [ ] A/B testing for ML models

### 8.6 Feature Stores & Data Infrastructure

- [ ] Lambda architecture: batch + streaming
- [ ] Kappa architecture: streaming only
- [ ] Kafka for real-time feature pipelines
- [ ] Spark for large-scale feature computation

### 8.7 Model Monitoring & Observability

- [ ] Data drift detection: KS test, PSI (Population Stability Index)
- [ ] Concept drift detection: DDM, ADWIN
- [ ] Feature importance drift
- [ ] Alerting and SLOs

### 8.8 CI/CD for ML

- [ ] ML pipelines: Kubeflow, MLflow Pipelines, Airflow
- [ ] Testing: unit tests for transforms, model training tests
- [ ] Model governance and approval workflows

### 8.9 Compute Infrastructure

- [ ] GPU memory management: activations, parameters, gradients, optimizer states
- [ ] Kubernetes for ML workloads
- [ ] Spot instances and preemption handling
- [ ] Training cost estimation

---

## PART XVII: ML SYSTEM DESIGN

### 41. ML System Design (Interview Framework)

#### 41.1 Design Framework

- [ ] Step 1: Problem formulation — clarify requirements, define ML task type, specify constraints (latency, throughput, budget)
- [ ] Step 2: Metrics — offline metrics vs online metrics, guardrail metrics, counter-metrics
- [ ] Step 3: Data — data sources, labeling strategy, data pipeline, storage, freshness requirements
- [ ] Step 4: Feature engineering — user features, item features, context features, cross features, real-time vs batch features
- [ ] Step 5: Model selection — baseline model, iteration plan, tradeoffs (complexity vs latency vs interpretability)
- [ ] Step 6: Training — loss function, training data construction (positive/negative sampling), training infrastructure
- [ ] Step 7: Evaluation — offline evaluation, online evaluation (A/B testing), slice analysis
- [ ] Step 8: Deployment — serving infrastructure, batch vs online, model updates, rollback strategy
- [ ] Step 9: Monitoring — data drift, model drift, feedback loops, retraining cadence

#### 41.2 Common ML System Design Problems

- [ ] Search ranking system (Google, Bing)
- [ ] Ads click-through rate (CTR) prediction
- [ ] News feed / content ranking (Facebook, Twitter / X, TikTok)
- [ ] E-commerce product recommendation
- [ ] Video recommendation (YouTube, Netflix)
- [ ] Ride matching / ETA prediction (Uber, Lyft)
- [ ] Fraud detection system (payments, transactions)
- [ ] Spam / harmful content detection
- [ ] Autocomplete / query suggestion
- [ ] Notification delivery optimization
- [ ] People You May Know (PYMK) / friend suggestion
- [ ] Job recommendation (LinkedIn)
- [ ] Image search / visual search
- [ ] Chatbot / conversational AI system
- [ ] Review quality / helpfulness prediction
- [ ] Content moderation pipeline (text, image, video)
- [ ] Dynamic pricing / surge pricing

### 11.1 Design Framework

- [ ] 3. Data collection and annotation
- [ ] 6. Offline evaluation metrics
- [ ] 7. Online serving architecture

### 11.2 Classic Design Problems

#### Recommendation Systems

- [ ] Instagram Feed Ranking
- [ ] Music recommendation (Spotify)

#### Search & Ranking

- [ ] Web search ranking
- [ ] E-commerce search (semantic + keyword)
- [ ] Pinterest visual search
- [ ] Ad ranking / auction

#### NLP Systems

- [ ] Spam classifier
- [ ] Sentiment analysis at scale
- [ ] Document classification
- [ ] Machine translation system
- [ ] QA system

#### Computer Vision Systems

- [ ] OCR pipeline
- [ ] Medical image diagnosis

#### Abuse & Trust & Safety

- [ ] Bot detection
- [ ] Fake news / misinformation detection

### 11.3 Key Trade-offs to Always Address

- [ ] Precision vs Recall (and which matters more for the product)

---

## PART XVIII: RESPONSIBLE AI, SAFETY & ETHICS

### 42. Responsible AI

#### 42.1 Fairness & Bias

- [ ] Types of bias: historical, representation, measurement, aggregation, evaluation, deployment
- [ ] Fairness definitions: demographic parity, equalized odds, equality of opportunity, individual fairness, counterfactual fairness
- [ ] Impossibility theorem: incompatibility of fairness criteria
- [ ] Bias detection: disparate impact analysis, fairness metrics by subgroup
- [ ] Bias mitigation: pre-processing (resampling, reweighting), in-processing (adversarial debiasing, fairness constraints), post-processing (threshold adjustment)
- [ ] Tools: AI Fairness 360 (AIF360), Fairlearn, What-If Tool

#### 42.2 Explainability & Interpretability

- [ ] Model-agnostic methods: LIME (Local Interpretable Model-Agnostic Explanations), SHAP (SHapley Additive exPlanations), partial dependence plots (PDP), accumulated local effects (ALE), permutation importance
- [ ] Model-specific: attention visualization, gradient-based methods (saliency maps, Grad-CAM, Integrated Gradients), concept-based explanations (TCAV)
- [ ] Rule extraction from neural networks
- [ ] Counterfactual explanations
- [ ] SHAP: Kernel SHAP, Tree SHAP, Deep SHAP, interaction values
- [ ] Global vs local explanations
- [ ] Inherently interpretable models: decision trees, rule lists, GAMs (EBM / Explainable Boosting Machine)

#### 42.3 Privacy

- [ ] Differential privacy: ε-differential privacy, DP-SGD, privacy budget, composition theorems
- [ ] Federated learning: FedAvg, FedProx, communication efficiency, non-IID data challenges, privacy guarantees
- [ ] Secure multi-party computation (SMPC)
- [ ] Homomorphic encryption for ML
- [ ] Data anonymization: k-anonymity, l-diversity, t-closeness
- [ ] Model inversion attacks, membership inference attacks
- [ ] Machine unlearning

#### 42.4 Adversarial Robustness

- [ ] Adversarial examples: FGSM, PGD, C&W attack, AutoAttack
- [ ] Adversarial training: PGD-AT, TRADES
- [ ] Certified robustness: randomized smoothing, interval bound propagation
- [ ] Backdoor attacks & defenses
- [ ] Data poisoning attacks
- [ ] Robustness evaluation: robust accuracy, certified radius

#### 42.5 AI Safety & Alignment

- [ ] Alignment problem: outer alignment, inner alignment, mesa-optimization
- [ ] Reward hacking / reward misspecification
- [ ] Scalable oversight: RLHF, debate, recursive reward modeling
- [ ] Constitutional AI
- [ ] Red teaming LLMs: manual, automated, adversarial prompting
- [ ] Prompt injection: direct, indirect, jailbreaking
- [ ] Guardrails: input/output filtering, Llama Guard, NeMo Guardrails
- [ ] AI governance: EU AI Act, NIST AI RMF, risk categories
- [ ] Hallucination detection & mitigation in LLMs

### 9.1 Fairness & Bias

- [ ] Sources of bias: data, label, measurement, historical
- [ ] Impossibility results: mutual exclusivity of fairness criteria
- [ ] Individual vs group fairness
- [ ] Debiasing word embeddings

### 9.2 Interpretability & Explainability (XAI)

- [ ] SHAP values: Shapley values from game theory, TreeSHAP, DeepSHAP
- [ ] LIME: local linear approximation
- [ ] Global interpretability: feature importance, partial dependence plots (PDP)
- [ ] ICE (Individual Conditional Expectation) plots
- [ ] Attention visualization (caution: not ground truth)
- [ ] Probing classifiers for LLMs
- [ ] Mechanistic interpretability: circuits, superposition
- [ ] Saliency maps, GradCAM for CNNs

### 9.3 Robustness & Adversarial ML

- [ ] Adversarial training: min-max optimization
- [ ] Model evasion attacks
- [ ] Backdoor attacks, trojan models
- [ ] Robustness to distribution shift

### 9.4 Privacy

- [ ] Differential Privacy (DP): ε-DP, δ-DP, Gaussian mechanism
- [ ] DP-SGD: training with privacy guarantees
- [ ] Federated Learning: local training + aggregation
- [ ] FedAvg algorithm
- [ ] Homomorphic encryption (theoretical)

### 9.5 Alignment

- [ ] Alignment problem: AI systems doing what we want
- [ ] Reward hacking, Goodhart's law
- [ ] Specification gaming
- [ ] RLHF as alignment technique
- [ ] Debate as alignment strategy
- [ ] Interpretability for alignment
- [ ] AI safety research landscape: MIRI, Anthropic, ARC

---

## PART XIX: SPECIALIZED & EMERGING TOPICS

### 43. Self-Supervised & Contrastive Learning

#### 43.1 Self-Supervised Learning Paradigms

- [ ] Pretext tasks: rotation prediction, jigsaw puzzle, colorization, inpainting
- [ ] Contrastive learning: positive/negative pairs, InfoNCE loss, temperature
- [ ] SimCLR: augmentation-based, large batch, projection head
- [ ] MoCo (Momentum Contrast): momentum encoder, queue of negatives
- [ ] BYOL (Bootstrap Your Own Latent): no negative pairs, exponential moving average target
- [ ] SwAV: online clustering, multi-crop strategy
- [ ] Barlow Twins: cross-correlation, redundancy reduction
- [ ] VICReg: variance-invariance-covariance regularization
- [ ] DINO: self-distillation with no labels, ViT features
- [ ] Masked image modeling: BEiT, MAE, SimMIM, data2vec
- [ ] Joint-embedding predictive architectures (JEPA): I-JEPA, V-JEPA

### 44. Transfer Learning & Domain Adaptation

#### 44.1 Transfer Learning

- [ ] Feature extraction: using pretrained features as fixed representations
- [ ] Fine-tuning: full model, head-only, gradual unfreezing, discriminative learning rates
- [ ] Domain shift: covariate shift, label shift, concept drift
- [ ] When transfer learning helps vs hurts (negative transfer)

#### 44.2 Domain Adaptation

- [ ] Unsupervised domain adaptation: DANN (Domain-Adversarial Neural Network), gradient reversal layer
- [ ] Maximum Mean Discrepancy (MMD) for distribution alignment
- [ ] Self-training for domain adaptation
- [ ] Test-time adaptation / test-time training (TTT, TENT)
- [ ] Source-free domain adaptation

### 45. Meta-Learning & Few-Shot Learning

#### 45.1 Meta-Learning

- [ ] Learning to learn: task distribution, inner loop, outer loop
- [ ] MAML (Model-Agnostic Meta-Learning): second-order gradients, first-order approximations (FOMAML, Reptile)
- [ ] Prototypical Networks: class prototypes, embedding space, distance-based classification
- [ ] Matching Networks: attention over support set
- [ ] Relation Networks: learned comparison function
- [ ] Meta-learning for hyperparameter optimization
- [ ] Meta-learning for architecture search

#### 45.2 Few-Shot & Zero-Shot Learning

- [ ] N-way K-shot classification: support set, query set, episodes
- [ ] Zero-shot learning: attribute-based, semantic embeddings, generalized zero-shot learning
- [ ] In-context learning in LLMs as meta-learning
- [ ] Prompt-based few-shot with LLMs

### 46. Model Compression & Efficient ML

#### 46.1 Knowledge Distillation

- [ ] Hinton et al.: teacher-student framework, soft targets, temperature
- [ ] Feature-based distillation: FitNets, attention transfer
- [ ] Self-distillation: Born-Again Networks
- [ ] Online distillation: Deep Mutual Learning
- [ ] Task-specific distillation: DistilBERT, TinyBERT

#### 46.2 Pruning

- [ ] Unstructured pruning: magnitude pruning, lottery ticket hypothesis, iterative magnitude pruning (IMP)
- [ ] Structured pruning: filter pruning, channel pruning, layer removal
- [ ] Pruning at initialization: SNIP, GraSP
- [ ] Dynamic pruning / conditional computation
- [ ] SparseGPT, Wanda for LLM pruning

#### 46.3 Quantization (General)

- [ ] Post-training quantization (PTQ): symmetric vs asymmetric, per-tensor vs per-channel
- [ ] Quantization-aware training (QAT): fake quantization, straight-through estimator
- [ ] Mixed-precision: FP32, FP16, BF16, INT8, INT4
- [ ] Dynamic quantization
- [ ] (LLM-specific quantization covered in Section 29.1)

#### 46.4 Neural Architecture Search (NAS)

- [ ] Search space design: cell-based, macro-based
- [ ] Search strategies: reinforcement learning-based (Zoph & Le), evolutionary, differentiable (DARTS), one-shot (supernet, weight sharing)
- [ ] Efficiency-aware NAS: FBNet, EfficientNet, MnasNet, hardware-aware NAS
- [ ] Once-for-all (OFA) networks

#### 46.5 Efficient Inference

- [ ] Operator fusion, graph optimization
- [ ] Flash Attention & memory-efficient attention
- [ ] Speculative decoding (see Section 29.2)
- [ ] Token merging / token pruning for ViTs
- [ ] Early exit / adaptive computation

### 47. Continual, Curriculum & Active Learning

#### 47.1 Continual / Lifelong Learning

- [ ] Catastrophic forgetting: causes, measurement
- [ ] Regularization-based: EWC (Elastic Weight Consolidation), SI (Synaptic Intelligence), LwF (Learning without Forgetting)
- [ ] Replay-based: experience replay, generative replay
- [ ] Architecture-based: progressive neural networks, PackNet
- [ ] Task-incremental vs class-incremental vs domain-incremental settings

#### 47.2 Curriculum Learning

- [ ] Manual curriculum design: easy-to-hard ordering
- [ ] Self-paced learning: automatic difficulty-based weighting
- [ ] Anti-curriculum & hard example mining
- [ ] Competence-based curriculum

#### 47.3 Active Learning

- [ ] Query strategies: uncertainty sampling (entropy, margin, least confidence), query-by-committee, expected model change, diversity sampling, Bayesian active learning (BALD)
- [ ] Batch-mode active learning
- [ ] Active learning for NLP, CV, structured prediction
- [ ] Human-in-the-loop ML pipelines

### 48. Neuro-Symbolic AI & Emerging Paradigms

#### 48.1 Neuro-Symbolic AI

- [ ] Neural theorem provers
- [ ] Differentiable programming with logic: DeepProbLog, NeurASP
- [ ] Neural module networks
- [ ] Concept bottleneck models
- [ ] Symbol grounding problem

#### 48.2 Foundation Models & Scaling

- [ ] Foundation model concept: pretrain once, adapt everywhere
- [ ] Emergent abilities: in-context learning, chain-of-thought reasoning, tool use
- [ ] Scaling laws: power-law relationships (loss vs compute, data, parameters)
- [ ] Chinchilla optimal: compute-optimal data-parameter ratio
- [ ] Multi-modal foundation models: unified architectures

#### 48.3 Other Emerging Topics

- [ ] Test-time compute scaling: using more inference compute for harder problems
- [ ] Mixture of Experts (MoE): sparse gating, top-k routing, load balancing, expert specialization
- [ ] State-space models: S4, Mamba, H3, selective state spaces
- [ ] Geometric deep learning: equivariant neural networks, group theory, symmetry-preserving architectures
- [ ] Neural ODEs: continuous-depth networks, adjoint method
- [ ] Kolmogorov-Arnold Networks (KANs)
- [ ] Retrieval-augmented pretraining: RETRO
- [ ] Instruction-following & constitutional AI
- [ ] AI for science: protein folding (AlphaFold), drug discovery, materials science, weather forecasting (GraphCast, Pangu-Weather)
- [ ] World models for robotics & planning

### 2.10 Self-Supervised & Contrastive Learning

#### 2.10.1 Pretext Tasks

- [ ] Colorization
- [ ] Patch ordering (jigsaw)
- [ ] Next frame prediction

#### 2.10.2 Contrastive Learning

- [ ] SimCLR: augmentation-based pairs, NT-Xent loss
- [ ] MoCo v2, v3
- [ ] BYOL: no negative pairs, stop gradient
- [ ] SimSiam: collapse prevention without negatives
- [ ] VICReg
- [ ] Temperature parameter in InfoNCE
- [ ] Batch size effects on contrastive learning

#### 2.10.3 Masked Autoencoders (MAE)

- [ ] High masking ratio (75%) for images
- [ ] Asymmetric encoder-decoder
- [ ] Patch embedding, masked tokens
- [ ] Data2Vec: masked prediction across modalities
- [ ] I-JEPA: latent space prediction

### 2.11 Transfer Learning & Fine-Tuning

- [ ] Pre-training on large corpus, fine-tuning on downstream task
- [ ] Feature extraction (frozen backbone)
- [ ] Linear probing vs full fine-tuning comparison
- [ ] Few-shot learning: Prototypical Networks, Matching Networks, MAML
- [ ] Zero-shot learning: attribute-based, class embedding

### 10.1 Scaling Laws

- [ ] Kaplan et al. (2020): compute, data, parameters power laws
- [ ] Emergent abilities at scale
- [ ] Scaling laws for fine-tuning
- [ ] Data scaling: quality > quantity
- [ ] Debate: scaling hypothesis vs architectural innovations

### 10.2 Test-Time Compute (Inference Scaling)

- [ ] Chain-of-Thought as test-time compute
- [ ] Self-consistency: sampling + majority vote
- [ ] Process Reward Models (PRM) vs Outcome Reward Models (ORM)
- [ ] MCTS for LLM reasoning
- [ ] OpenAI o1, o3: hidden chain-of-thought
- [ ] DeepSeek-R1: RL-based reasoning
- [ ] Scaling inference: trade compute at test time for accuracy

### 10.3 Mixture of Experts (MoE)

- [ ] Top-k routing: select k experts per token
- [ ] Switch Transformer: k=1, auxiliary loss
- [ ] GShard, GLaM
- [ ] DeepSeek-MoE: fine-grained expert partitioning
- [ ] Expert parallelism for training
- [ ] Dead expert problem

### 10.4 State Space Models

- [ ] S4 (Structured State Spaces): HiPPO, LSSL
- [ ] Mamba: selective SSM, hardware-aware algorithm
- [ ] Mamba-2: SSD framework, connections to attention
- [ ] RWKV: linear attention via RNN formulation
- [ ] RetNet: retention mechanism
- [ ] Hybrid models: Jamba, Zamba
- [ ] SSMs vs attention: efficiency vs expressiveness

### 10.5 Long Context & Memory

- [ ] Context window: 8K → 128K → 1M tokens
- [ ] Retrieval augmented long context
- [ ] Streaming LLM: attention sink
- [ ] External memory: MemGPT
- [ ] Infinite context: InfLLM, InfiniteAttention

### 10.6 Multimodal Generation Frontier

- [ ] Any-to-any models: text, image, audio, video unified
- [ ] Unified tokenization of all modalities
- [ ] Show-o, Janus: understanding + generation in one model
- [ ] GPT-4o real-time audio
- [ ] Gemini 2.0 Flash: natively multimodal generation

### 10.7 AI for Science

- [ ] AlphaFold2, AlphaFold3: protein structure prediction
- [ ] Drug discovery with ML
- [ ] Graph neural networks for molecular property prediction
- [ ] Climate modeling with ML
- [ ] Materials science: crystal property prediction
- [ ] Genomics: DNA language models

### 10.8 Robotics & Embodied AI

- [ ] RT-2, RT-X: vision-language-action models
- [ ] Diffusion Policy
- [ ] SLAM and navigation

---

## PART XX: ROBOTICS & EMBODIED AI (Overview)

### 49. Robotics & Embodied AI

#### 49.1 Perception

- [ ] Sensor fusion: LiDAR, cameras, radar, IMU
- [ ] 3D object detection: point cloud methods (PointPillars, CenterPoint), BEV (Bird's Eye View) methods (BEVFormer)
- [ ] SLAM: Simultaneous Localization and Mapping (visual SLAM, LiDAR SLAM)
- [ ] Occupancy prediction

#### 49.2 Planning & Control

- [ ] Motion planning: RRT, A*, PRM, trajectory optimization
- [ ] Model Predictive Control (MPC)
- [ ] End-to-end learning for autonomous driving
- [ ] Behaviour cloning & imitation learning for robotics
- [ ] Sim-to-real transfer: domain randomization, progressive nets

#### 49.3 Robot Learning

- [ ] Learning from demonstrations (LfD)
- [ ] Reward learning for robots
- [ ] Manipulation: grasping, dexterous manipulation
- [ ] Foundation models for robotics: RT-1, RT-2, SayCan, PaLM-E, VIMA
- [ ] Language-conditioned policies

---
