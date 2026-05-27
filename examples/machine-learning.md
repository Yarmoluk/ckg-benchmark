## META
name: Machine Learning
version: 1.0.0
domain: machine-learning
description: Core concepts, algorithms, and evaluation methods in supervised and unsupervised machine learning.
nodes: 68
edges: 89
source: McCreary Intelligent Textbook Corpus (MIT)
license: MIT

---

## NODES

[CONCEPT|machine_learning|Machine Learning
  |Field of study that gives computers the ability to learn from data without being explicitly programmed. Encompasses supervised, unsupervised, and reinforcement learning paradigms.]

[CONCEPT|supervised_learning|Supervised Learning
  |Learning paradigm in which a model is trained on labeled input-output pairs. The goal is to learn a mapping from features to labels that generalizes to unseen examples.]

[CONCEPT|unsupervised_learning|Unsupervised Learning
  |Learning paradigm in which no labels are provided. The model discovers latent structure — clusters, manifolds, or generative factors — directly from the raw input distribution.]

[CONCEPT|classification|Classification
  |Supervised task that assigns a discrete class label to each input. Examples: spam detection, image recognition, medical diagnosis. Output is a categorical prediction.]

[CONCEPT|regression|Regression
  |Supervised task that predicts a continuous numeric output. Examples: house price estimation, demand forecasting. Evaluated with squared-error or absolute-error metrics.]

[CONCEPT|training_data|Training Data
  |The labeled (or unlabeled) dataset used to fit model parameters. Quality, size, and representativeness of training data are the dominant factors in model performance.]

[CONCEPT|test_data|Test Data
  |Held-out dataset used only for final performance estimation. Must never influence model design or hyperparameter choices — contamination leads to optimistic bias.]

[CONCEPT|validation_data|Validation Data
  |Dataset used during development to tune hyperparameters and detect overfitting. Separate from test data; contact with validation data is permitted during model selection.]

[CONCEPT|feature|Feature
  |A single measurable property of an observation. The choice of features determines what information is available to the model; irrelevant features increase noise and training cost.]

[CONCEPT|label|Label
  |The ground-truth output associated with a training example in supervised learning. Also called the target, response variable, or dependent variable.]

[CONCEPT|feature_vector|Feature Vector
  |A fixed-length numerical representation of one observation, encoding all features as an ordered tuple. The standard input format for most ML algorithms.]

[CONCEPT|model|Model
  |A learned mathematical function mapping inputs to predictions. A model is defined by its architecture (structure) and its parameters (learned from data).]

[CONCEPT|algorithm|Algorithm
  |A step-by-step procedure for fitting model parameters to data. The algorithm determines how the model searches for the best solution, e.g., iterative gradient updates or recursive partitioning.]

[CONCEPT|hyperparameter|Hyperparameter
  |A configuration value set before training that controls the learning process itself, such as learning rate, depth limit, or regularization strength. Not learned from data — must be tuned separately.]

[CONCEPT|k_nearest_neighbors|K-Nearest Neighbors
  |Non-parametric classification and regression algorithm that predicts by majority vote or average of the k training examples closest to the query point. Simple, interpretable, but expensive at inference time.]

[CONCEPT|distance_metric|Distance Metric
  |A function measuring similarity between two feature vectors. Common choices include Euclidean distance, Manhattan distance, and cosine similarity. The metric strongly affects KNN accuracy.]

[CONCEPT|decision_tree|Decision Tree
  |Tree-structured model that partitions the feature space using axis-aligned splits. Each leaf holds a class prediction or numeric value; paths from root to leaf are human-readable rules.]

[CONCEPT|splitting_criterion|Splitting Criterion
  |The objective function used to choose which feature and threshold to split on at each node of a decision tree. Gini impurity and entropy are common criteria for classification.]

[CONCEPT|entropy|Entropy
  |Measure of label disorder in a node, borrowed from information theory. A pure node (all one class) has entropy zero; maximum entropy occurs when classes are equally distributed.]

[CONCEPT|information_gain|Information Gain
  |Reduction in entropy achieved by a candidate split. Decision tree inducers choose the split that maximizes information gain, greedily building the tree top-down.]

[CONCEPT|overfitting|Overfitting
  |Model error mode in which the model memorizes training data idiosyncrasies rather than learning generalizable patterns. Manifests as low training error but high test error.]

[CONCEPT|underfitting|Underfitting
  |Model error mode in which the model is too simple to capture the true structure of the data. Manifests as high training error and high test error. Remedied by increasing model capacity.]

[CONCEPT|logistic_regression|Logistic Regression
  |Linear classification model that applies the sigmoid function to a linear combination of features. Produces calibrated class probabilities; efficient, regularizable, and interpretable.]

[CONCEPT|sigmoid_function|Sigmoid Function
  |S-shaped function σ(z) = 1 / (1 + e^−z) that squashes any real number to the (0, 1) interval. Used in logistic regression to convert a linear score to a class probability.]

[CONCEPT|regularization|Regularization
  |Technique that penalizes model complexity during training to reduce overfitting. Adds a penalty term to the loss function, discouraging large parameter values or complex structures.]

[CONCEPT|l1_regularization|L1 Regularization (Lasso)
  |Adds the sum of absolute parameter values to the loss. Produces sparse models by driving irrelevant feature weights exactly to zero — effectively performing feature selection.]

[CONCEPT|l2_regularization|L2 Regularization (Ridge)
  |Adds the sum of squared parameter values to the loss. Shrinks all weights toward zero smoothly without producing exact sparsity. Preferred when all features carry some signal.]

[CONCEPT|support_vector_machine|Support Vector Machine
  |Classifier that finds the maximum-margin hyperplane separating classes. Robust in high-dimensional spaces; the kernel trick extends it to nonlinear boundaries.]

[CONCEPT|kernel_trick|Kernel Trick
  |Mathematical device that implicitly maps inputs to a high-dimensional feature space by computing inner products via a kernel function, enabling SVMs to learn nonlinear boundaries at low cost.]

[CONCEPT|k_means_clustering|K-Means Clustering
  |Unsupervised algorithm that partitions n observations into k clusters by alternately assigning points to their nearest centroid and recomputing centroids. Simple and scalable; sensitive to initialization.]

[CONCEPT|elbow_method|Elbow Method
  |Heuristic for selecting k in K-Means: plot within-cluster sum of squares against k and choose the k at the "elbow" where marginal improvement levels off.]

[CONCEPT|silhouette_score|Silhouette Score
  |Cluster quality metric ranging from −1 to 1 that measures how similar each point is to its own cluster versus the next nearest cluster. Higher is better; near 0 indicates overlapping clusters.]

[CONCEPT|neural_network|Neural Network
  |Layered composition of artificial neurons. Each layer learns increasingly abstract representations of the input. Universal function approximators when sufficiently deep and wide.]

[CONCEPT|artificial_neuron|Artificial Neuron
  |Basic computational unit: computes a weighted sum of its inputs, adds a bias, then applies a nonlinear activation function. The building block of every neural network layer.]

[CONCEPT|activation_function|Activation Function
  |Nonlinear function applied to each neuron's weighted sum. Without nonlinearity, stacking layers collapses to a single linear transformation. Common choices: ReLU, sigmoid, tanh.]

[CONCEPT|relu|ReLU (Rectified Linear Unit)
  |Activation function f(x) = max(0, x). Computationally cheap, avoids vanishing gradients, and produces sparse activations. Default activation for hidden layers in most modern networks.]

[CONCEPT|backpropagation|Backpropagation
  |Algorithm that efficiently computes gradients of the loss with respect to every parameter by applying the chain rule layer by layer in reverse order. Makes training deep networks tractable.]

[CONCEPT|gradient_descent|Gradient Descent
  |Iterative optimization algorithm that updates parameters in the direction of the negative gradient of the loss. Stochastic and mini-batch variants are standard in neural network training.]

[CONCEPT|learning_rate|Learning Rate
  |Hyperparameter controlling the step size in gradient descent. Too large causes divergence; too small causes slow convergence. Typically scheduled to decay during training.]

[CONCEPT|loss_function|Loss Function
  |Scalar function measuring the discrepancy between predictions and ground truth. Minimizing the loss over training data is the objective of the learning algorithm.]

[CONCEPT|mean_squared_error|Mean Squared Error
  |Loss function for regression: average of squared differences between predictions and targets. Penalizes large errors quadratically; sensitive to outliers.]

[CONCEPT|cross_entropy_loss|Cross-Entropy Loss
  |Loss function for classification: negative log-likelihood of the true class under the predicted probability distribution. Standard for logistic regression and softmax classifiers.]

[CONCEPT|deep_learning|Deep Learning
  |Subfield of machine learning using neural networks with many layers (depth). Enables automatic feature learning from raw inputs, eliminating manual feature engineering for vision, audio, and text.]

[CONCEPT|convolutional_neural_network|Convolutional Neural Network
  |Deep learning architecture designed for grid-structured data (images, time series). Uses shared-weight convolution filters to detect local patterns regardless of position.]

[CONCEPT|pooling_layer|Pooling Layer
  |CNN component that down-samples feature maps by aggregating nearby values (max or average). Reduces spatial resolution, builds translation invariance, and controls computational cost.]

[CONCEPT|transfer_learning|Transfer Learning
  |Technique that reuses parameters learned on a large source task as initialization for a smaller target task. Dramatically reduces data and compute requirements for new domains.]

[CONCEPT|fine_tuning|Fine-Tuning
  |Transfer learning strategy that continues training a pre-trained model on target-task data, typically with a small learning rate. Adapts high-level representations while preserving low-level features.]

[CONCEPT|bias_variance_tradeoff|Bias-Variance Tradeoff
  |Decomposition of generalization error into bias (systematic error from underfitting) and variance (sensitivity to training data fluctuations from overfitting). Reducing one tends to increase the other.]

[CONCEPT|cross_validation|Cross-Validation
  |Model evaluation technique that partitions data into complementary subsets, training and evaluating multiple times. Produces a low-variance estimate of generalization performance.]

[CONCEPT|k_fold_cross_validation|K-Fold Cross-Validation
  |Cross-validation variant that splits data into k equally-sized folds, using each fold as the validation set once. Common choices: k=5 or k=10. Standard practice for hyperparameter tuning.]

[CONCEPT|confusion_matrix|Confusion Matrix
  |Square table comparing predicted versus actual class labels across all classes. Entry (i, j) is the count of examples of class i predicted as class j. Foundation for all classification metrics.]

[CONCEPT|precision|Precision
  |Fraction of positive predictions that are actually positive. Precision = TP / (TP + FP). High precision matters when false positives are costly, e.g., spam filtering.]

[CONCEPT|recall|Recall
  |Fraction of actual positives that were correctly predicted. Recall = TP / (TP + FN). High recall matters when false negatives are costly, e.g., disease screening.]

[CONCEPT|f1_score|F1 Score
  |Harmonic mean of precision and recall: 2 · (P · R) / (P + R). Balances both metrics; preferred over accuracy when classes are imbalanced.]

[CONCEPT|roc_curve|ROC Curve
  |Receiver Operating Characteristic curve plotting true positive rate vs. false positive rate at all classification thresholds. Shows the full precision-recall tradeoff of a classifier.]

[CONCEPT|auc|AUC (Area Under the ROC Curve)
  |Single scalar summary of ROC curve quality. AUC = 1.0 is perfect; AUC = 0.5 is random. Threshold-independent measure of discriminative power.]

[CONCEPT|data_preprocessing|Data Preprocessing
  |Pipeline of transformations applied to raw data before model training. Includes normalization, encoding, imputation, and outlier handling. Critical for algorithm convergence and fairness.]

[CONCEPT|normalization|Normalization
  |Rescaling features to a standard range or distribution (e.g., [0,1] or zero mean and unit variance). Prevents features with large magnitudes from dominating distance-based and gradient-based algorithms.]

[CONCEPT|one_hot_encoding|One-Hot Encoding
  |Converts a categorical feature with k levels into k binary indicator features. Eliminates spurious ordinal relationships that would arise from integer encoding.]

[CONCEPT|feature_engineering|Feature Engineering
  |Process of creating informative input representations from raw data using domain knowledge. Often the highest-leverage activity in an ML project; good features can compensate for simple models.]

[CONCEPT|feature_selection|Feature Selection
  |Process of identifying and retaining only the most predictive features. Reduces dimensionality, improves interpretability, and can increase generalization by removing noise.]

[CONCEPT|dimensionality_reduction|Dimensionality Reduction
  |Transformation of high-dimensional data into a lower-dimensional representation that preserves key structure. Addresses the curse of dimensionality; aids visualization and downstream learning.]

[CONCEPT|optimizer|Optimizer
  |Algorithm that updates model parameters to minimize the loss function. Extends basic gradient descent with mechanisms for adaptive step sizes, momentum, or second-order information.]

[CONCEPT|adam_optimizer|Adam Optimizer
  |Adaptive gradient optimizer combining momentum and per-parameter learning rates. Robust default choice for training deep networks; converges reliably across a wide range of architectures.]

[CONCEPT|dropout|Dropout
  |Regularization technique that randomly zeros a fraction of neuron activations during each training forward pass. Forces the network to learn redundant representations, reducing co-adaptation and overfitting.]

[CONCEPT|model_evaluation|Model Evaluation
  |Systematic process of measuring how well a trained model generalizes to new data using held-out datasets and appropriate metrics. The basis for comparing models and detecting overfitting.]

[CONCEPT|model_selection|Model Selection
  |Process of choosing among competing model architectures, algorithms, or hyperparameter configurations based on validation performance. Requires careful separation of validation and test sets.]

[CONCEPT|hyperparameter_tuning|Hyperparameter Tuning
  |Optimization over the hyperparameter space to find configurations that minimize validation error. Methods include grid search, random search, and Bayesian optimization.]

---

## EDGES

machine_learning         -[PREREQUISITE_FOR]->    supervised_learning
machine_learning         -[PREREQUISITE_FOR]->    unsupervised_learning
machine_learning         -[REQUIRES]->            training_data
machine_learning         -[PRODUCES]->            model

supervised_learning      -[ENABLES]->             classification
supervised_learning      -[ENABLES]->             regression
supervised_learning      -[REQUIRES]->            label
supervised_learning      -[IMPLEMENTS]->          k_nearest_neighbors
supervised_learning      -[IMPLEMENTS]->          logistic_regression
supervised_learning      -[IMPLEMENTS]->          support_vector_machine
supervised_learning      -[IMPLEMENTS]->          decision_tree

unsupervised_learning    -[IMPLEMENTS]->          k_means_clustering
unsupervised_learning    -[ENABLES]->             dimensionality_reduction

training_data            -[PRODUCES]->            validation_data
training_data            -[PRODUCES]->            test_data
training_data            -[COMPONENT_OF]->        feature_vector
training_data            -[CAUSES]->              overfitting

feature                  -[COMPONENT_OF]->        feature_vector
feature_vector           -[REQUIRES]->            feature
feature_vector           -[USES]->                normalization

model                    -[DEFINED_BY]->          algorithm
model                    -[DEFINED_BY]->          hyperparameter
model                    -[MEASURED_BY]->         model_evaluation
model                    -[REQUIRES]->            loss_function

algorithm                -[USES]->                gradient_descent
algorithm                -[USES]->                optimizer

hyperparameter           -[QUANTIFIED_BY]->       hyperparameter_tuning
hyperparameter           -[INSTANCE_OF]->         learning_rate

decision_tree            -[USES]->                splitting_criterion
decision_tree            -[CAUSES]->              overfitting
splitting_criterion      -[USES]->                entropy
entropy                  -[DEFINED_BY]->          information_gain

logistic_regression      -[USES]->                sigmoid_function
logistic_regression      -[REQUIRES]->            regularization
logistic_regression      -[OUTPUTS]->             classification

support_vector_machine   -[EXTENDS]->             kernel_trick
support_vector_machine   -[REQUIRES]->            regularization

k_nearest_neighbors      -[REQUIRES]->            distance_metric
k_nearest_neighbors      -[USES]->                feature_vector

k_means_clustering       -[MEASURED_BY]->         silhouette_score
k_means_clustering       -[USES]->                elbow_method
k_means_clustering       -[REQUIRES]->            hyperparameter

overfitting              -[CONTRASTS_WITH]->      underfitting
overfitting              -[PREVENTED_BY]->        regularization
overfitting              -[PREVENTED_BY]->        dropout
overfitting              -[QUANTIFIED_BY]->       bias_variance_tradeoff

regularization           -[INSTANCE_OF]->         l1_regularization
regularization           -[INSTANCE_OF]->         l2_regularization

neural_network           -[COMPONENT_OF]->        artificial_neuron
neural_network           -[REQUIRES]->            activation_function
neural_network           -[TRAINED_BY]->          backpropagation
neural_network           -[CAUSES]->              overfitting
neural_network           -[EXTENDS]->             deep_learning

artificial_neuron        -[USES]->                activation_function
activation_function      -[INSTANCE_OF]->         relu
activation_function      -[INSTANCE_OF]->         sigmoid_function

backpropagation          -[REQUIRES]->            loss_function
backpropagation          -[USES]->                gradient_descent
gradient_descent         -[REQUIRES]->            learning_rate
gradient_descent         -[USES]->                optimizer
optimizer                -[INSTANCE_OF]->         adam_optimizer

loss_function            -[INSTANCE_OF]->         mean_squared_error
loss_function            -[INSTANCE_OF]->         cross_entropy_loss
mean_squared_error       -[APPLIED_VIA]->         regression
cross_entropy_loss       -[APPLIED_VIA]->         classification

deep_learning            -[IMPLEMENTS]->          convolutional_neural_network
convolutional_neural_network -[COMPONENT_OF]->    pooling_layer
convolutional_neural_network -[ENABLES]->         transfer_learning
transfer_learning        -[APPLIED_VIA]->         fine_tuning

data_preprocessing       -[ENABLES]->             feature_engineering
data_preprocessing       -[COMPONENT_OF]->        normalization
data_preprocessing       -[COMPONENT_OF]->        one_hot_encoding
feature_engineering      -[ENABLES]->             feature_selection
feature_selection        -[ENABLES]->             dimensionality_reduction

cross_validation         -[INSTANCE_OF]->         k_fold_cross_validation
cross_validation         -[REQUIRES]->            validation_data
cross_validation         -[ENABLES]->             model_selection

model_evaluation         -[REQUIRES]->            test_data
model_evaluation         -[USES]->                confusion_matrix
confusion_matrix         -[PRODUCES]->            precision
confusion_matrix         -[PRODUCES]->            recall
precision                -[COMPONENT_OF]->        f1_score
recall                   -[COMPONENT_OF]->        f1_score
model_evaluation         -[USES]->                roc_curve
roc_curve                -[QUANTIFIED_BY]->       auc

model_selection          -[REQUIRES]->            cross_validation
model_selection          -[REQUIRES]->            hyperparameter_tuning
bias_variance_tradeoff   -[DEFINED_BY]->          overfitting
bias_variance_tradeoff   -[DEFINED_BY]->          underfitting
