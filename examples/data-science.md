## META
name: Data Science
version: 1.0.0
domain: data-science
description: End-to-end data science workflow covering statistics, Python tooling, data preparation, modeling, and responsible practice.
nodes: 60
edges: 76
source: McCreary Intelligent Textbook Corpus (MIT)
license: MIT

---

## NODES

[CONCEPT|data_science|Data Science
  |Interdisciplinary field combining statistics, programming, and domain knowledge to extract actionable insights from data. Spans the full pipeline from raw data collection to deployed models and communicated findings.]

[CONCEPT|python_programming|Python Programming
  |General-purpose language that has become the lingua franca of data science. Its ecosystem (NumPy, Pandas, Scikit-learn, PyTorch) covers every stage of the data science workflow.]

[CONCEPT|data|Data
  |Raw recorded observations about the world. The fundamental input to every data science task; data quality, representativeness, and volume determine the ceiling on what any model can achieve.]

[CONCEPT|numerical_data|Numerical Data
  |Data expressed as numbers that support arithmetic operations. Subdivided into continuous (real-valued) and discrete (integer-valued). Processed directly by most statistical and ML algorithms.]

[CONCEPT|categorical_data|Categorical Data
  |Data that takes values from a finite set of named categories, e.g., blood type or product color. Must be encoded numerically before use with most algorithms.]

[CONCEPT|dataset|Dataset
  |A structured collection of observations organized into rows (instances) and columns (features or variables). The standard unit of analysis in data science.]

[CONCEPT|observation|Observation
  |A single data point or record — one row of a dataset. Represents one measured instance of the phenomenon under study.]

[CONCEPT|feature|Feature
  |A single measured variable or attribute of each observation. Also called a predictor or independent variable. Feature choice is the primary driver of model quality.]

[CONCEPT|target_variable|Target Variable
  |The outcome a model is trained to predict or explain. Also called the dependent variable, label, or response. Defines the supervised learning task.]

[CONCEPT|data_science_workflow|Data Science Workflow
  |End-to-end process: problem definition → data collection → cleaning → exploration → modeling → evaluation → deployment → communication. Each stage gates the next.]

[CONCEPT|problem_definition|Problem Definition
  |Translating a business or research question into a precise, measurable ML or statistical task. Poorly defined problems are the most common cause of failed data science projects.]

[CONCEPT|data_collection|Data Collection
  |Process of gathering raw data from sources such as databases, APIs, sensors, surveys, or web scraping. Volume, freshness, and ethical provenance all matter.]

[CONCEPT|pandas_library|Pandas Library
  |Python library providing the DataFrame and Series data structures for tabular data manipulation. The primary tool for data loading, cleaning, transformation, and exploratory analysis in Python.]

[CONCEPT|dataframe|DataFrame
  |Two-dimensional labeled data structure with columns of potentially different types, analogous to a spreadsheet or SQL table. The central data structure in Pandas-based workflows.]

[CONCEPT|numpy_library|NumPy Library
  |Python library providing fast n-dimensional arrays and vectorized mathematical operations. The numerical backbone underlying Pandas, Scikit-learn, and most scientific Python packages.]

[CONCEPT|numpy_array|NumPy Array
  |Fixed-type, contiguous-memory n-dimensional array. Enables vectorized operations that are orders of magnitude faster than Python loops. The standard container for numerical computation.]

[CONCEPT|missing_values|Missing Values
  |Data points absent from a dataset, represented as NaN or NULL. Present in virtually all real-world datasets; require explicit handling before modeling to avoid biased or broken pipelines.]

[CONCEPT|imputation|Imputation
  |Strategy for filling missing values with estimated replacements — common choices include mean, median, mode, or model-based predictions. Choice depends on the missingness mechanism and downstream task.]

[CONCEPT|outliers|Outliers
  |Observations that lie far from the bulk of the data distribution. May indicate data entry errors, rare genuine phenomena, or distribution shift. Impact on models varies by algorithm.]

[CONCEPT|outlier_detection|Outlier Detection
  |Process of identifying anomalous observations using statistical tests (z-score, IQR) or algorithmic methods (Isolation Forest, DBSCAN). A prerequisite for robust downstream analysis.]

[CONCEPT|data_transformation|Data Transformation
  |Systematic modification of raw feature values to improve model compatibility or performance. Includes scaling, encoding, log-transforms, and derived feature creation.]

[CONCEPT|feature_scaling|Feature Scaling
  |Normalizing feature ranges so no single feature dominates distance or gradient computations. Min-max scaling and standardization (z-score) are the two standard approaches.]

[CONCEPT|data_visualization|Data Visualization
  |Graphical representation of data to reveal patterns, distributions, and relationships that are difficult to perceive in tabular form. Essential for EDA and communicating results to stakeholders.]

[CONCEPT|matplotlib_library|Matplotlib Library
  |Foundational Python plotting library offering fine-grained control over figure composition. Most other Python visualization tools (Seaborn, Pandas plots) are built on top of Matplotlib.]

[CONCEPT|seaborn_library|Seaborn Library
  |Statistical visualization library built on Matplotlib. Provides high-level interfaces for common statistical plots (distribution plots, regression plots, heatmaps) with attractive defaults.]

[CONCEPT|descriptive_statistics|Descriptive Statistics
  |Numerical summaries that characterize a dataset's central tendency, spread, and shape without inferring to a population. The first analytical step in any EDA.]

[CONCEPT|mean|Mean
  |Arithmetic average of a numeric variable: sum divided by count. Sensitive to outliers; complements the median for understanding central tendency.]

[CONCEPT|median|Median
  |Middle value of a sorted dataset. Robust to outliers and skewed distributions; preferred over the mean when data contain extreme values.]

[CONCEPT|variance|Variance
  |Average squared deviation of observations from the mean. Measures spread; forms the basis for standard deviation, linear regression, and many statistical tests.]

[CONCEPT|standard_deviation|Standard Deviation
  |Square root of variance, in the same units as the data. The most interpretable measure of spread; used in z-score normalization and confidence intervals.]

[CONCEPT|distribution|Distribution
  |Mathematical description of the probability or frequency of values a variable takes. Understanding the distribution guides choice of summary statistics, tests, and models.]

[CONCEPT|normal_distribution|Normal Distribution
  |Symmetric bell-shaped distribution characterized by mean μ and standard deviation σ. Central to classical statistics; many phenomena are approximately normal by the Central Limit Theorem.]

[CONCEPT|probability|Probability
  |Numerical measure of the likelihood of an event, ranging from 0 (impossible) to 1 (certain). The mathematical language underlying all statistical inference and probabilistic modeling.]

[CONCEPT|central_limit_theorem|Central Limit Theorem
  |Theorem stating that the sampling distribution of the mean approaches a normal distribution as sample size grows, regardless of the population distribution. Justifies many inferential procedures.]

[CONCEPT|confidence_interval|Confidence Interval
  |Range of values within which the true population parameter is expected to fall with a specified probability (e.g., 95%). Quantifies estimation uncertainty; wider intervals reflect less data or more variability.]

[CONCEPT|hypothesis_testing|Hypothesis Testing
  |Formal statistical procedure for deciding whether observed data are consistent with a null hypothesis. Produces a p-value used to accept or reject the null at a chosen significance level.]

[CONCEPT|p_value|P-Value
  |Probability of observing a test statistic as extreme as the data, assuming the null hypothesis is true. Does not measure effect size or practical significance; routinely misinterpreted.]

[CONCEPT|correlation|Correlation
  |Statistical measure of the linear association between two numeric variables, ranging from −1 to +1. Correlation does not imply causation.]

[CONCEPT|pearson_correlation|Pearson Correlation
  |Standardized measure of linear correlation between two variables: r = cov(X,Y) / (σ_X · σ_Y). Assumes both variables are numeric and approximately normally distributed.]

[CONCEPT|regression_analysis|Regression Analysis
  |Statistical modeling approach for estimating the relationship between a numeric target variable and one or more predictors. Enables prediction and causal inference.]

[CONCEPT|linear_regression|Linear Regression
  |Regression model that assumes a linear relationship between predictors and the target. Parameters estimated by minimizing sum of squared residuals (OLS). Interpretable and efficient.]

[CONCEPT|ordinary_least_squares|Ordinary Least Squares
  |Closed-form method for estimating linear regression coefficients by minimizing the sum of squared residuals. Optimal under Gauss-Markov assumptions (homoscedasticity, no multicollinearity).]

[CONCEPT|scikit_learn|Scikit-learn Library
  |Python machine learning library with a unified API for classification, regression, clustering, preprocessing, and model selection. The standard toolkit for applied ML in Python.]

[CONCEPT|train_test_split|Train-Test Split
  |Partition of a dataset into non-overlapping training and test subsets before any modeling. The test set is reserved for final evaluation only, preventing information leakage.]

[CONCEPT|r_squared|R-Squared
  |Proportion of variance in the target variable explained by the regression model, ranging from 0 to 1. Measures goodness of fit; does not penalize model complexity.]

[CONCEPT|mean_squared_error|Mean Squared Error
  |Average squared difference between predictions and true values. The dominant regression loss function; penalizes large errors quadratically. Units are squared units of the target.]

[CONCEPT|overfitting|Overfitting
  |Condition where a model fits training data so closely that it fails to generalize to new data. Evidenced by a large gap between training and validation/test performance.]

[CONCEPT|bias_variance_tradeoff|Bias-Variance Tradeoff
  |Fundamental tension: simple models have high bias (systematic error) but low variance; complex models have low bias but high variance (sensitivity to training data). Optimal models balance both.]

[CONCEPT|cross_validation|Cross-Validation
  |Resampling procedure that evaluates model generalization by training and testing on multiple complementary data splits. Produces a more reliable performance estimate than a single train-test split.]

[CONCEPT|feature_selection|Feature Selection
  |Process of identifying the subset of features most relevant to the target variable. Reduces dimensionality, training time, and overfitting risk; improves model interpretability.]

[CONCEPT|feature_engineering|Feature Engineering
  |Domain-guided creation of new informative features from raw data. Often the highest-leverage activity in a data science project; good features can make a simple model outperform a complex one.]

[CONCEPT|machine_learning|Machine Learning
  |Subfield of AI and data science in which models learn patterns from data rather than from hand-coded rules. Builds on statistical foundations and is applied via libraries like Scikit-learn.]

[CONCEPT|gradient_descent|Gradient Descent
  |Iterative optimization algorithm that adjusts model parameters in the direction of steepest loss reduction. Underpins training of neural networks and many other parameterized models.]

[CONCEPT|neural_networks|Neural Networks
  |Layered computational models loosely inspired by biological neurons. Excel at learning complex nonlinear patterns from large datasets; the foundation of modern deep learning.]

[CONCEPT|deep_learning|Deep Learning
  |Machine learning with neural networks containing many layers. Enables automatic feature extraction from raw inputs (images, text, audio) without manual feature engineering.]

[CONCEPT|explainable_ai|Explainable AI
  |Set of techniques and principles that make model predictions understandable to humans. Critical for high-stakes domains (healthcare, finance, legal) where accountability is required.]

[CONCEPT|model_interpretability|Model Interpretability
  |Degree to which a human can understand and predict a model's behavior. Intrinsically interpretable models (linear regression, decision trees) differ from post-hoc explainability methods.]

[CONCEPT|shap_values|SHAP Values
  |Game-theoretic approach (SHapley Additive exPlanations) that assigns each feature a contribution score for each prediction. Model-agnostic; provides locally faithful and globally consistent explanations.]

[CONCEPT|reproducibility|Reproducibility
  |Ability of an independent researcher to obtain the same results using the same data and code. Requires fixed random seeds, version-pinned dependencies, and documented pipelines.]

[CONCEPT|data_ethics|Data Ethics
  |Principles governing responsible data collection, use, and model deployment. Addresses privacy, consent, fairness, bias, and accountability. Increasingly codified in regulation (GDPR, EU AI Act).]

---

## EDGES

data_science             -[REQUIRES]->            python_programming
data_science             -[REQUIRES]->            data
data_science             -[DEFINED_BY]->          data_science_workflow
data_science             -[BUILDS_ON]->           descriptive_statistics
data_science             -[ENABLES]->             machine_learning

data_science_workflow    -[COMPONENT_OF]->        problem_definition
data_science_workflow    -[COMPONENT_OF]->        data_collection
data_science_workflow    -[COMPONENT_OF]->        data_visualization
problem_definition       -[PREREQUISITE_FOR]->    data_collection
data_collection          -[PRODUCES]->            dataset

dataset                  -[COMPONENT_OF]->        observation
dataset                  -[COMPONENT_OF]->        feature
dataset                  -[COMPONENT_OF]->        target_variable
dataset                  -[REQUIRES]->            train_test_split

data                     -[INSTANCE_OF]->         numerical_data
data                     -[INSTANCE_OF]->         categorical_data
numerical_data           -[USES]->                feature_scaling
categorical_data         -[REQUIRES]->            feature_engineering

python_programming       -[ENABLES]->             pandas_library
python_programming       -[ENABLES]->             numpy_library
python_programming       -[ENABLES]->             scikit_learn
python_programming       -[ENABLES]->             matplotlib_library

numpy_library            -[PREREQUISITE_FOR]->    pandas_library
numpy_library            -[PRODUCES]->            numpy_array
pandas_library           -[PRODUCES]->            dataframe
dataframe                -[USES]->                numpy_array

dataframe                -[COMPONENT_OF]->        missing_values
dataframe                -[COMPONENT_OF]->        outliers
missing_values           -[SOLVES]->              imputation
outliers                 -[MEASURED_BY]->         outlier_detection

data_transformation      -[COMPONENT_OF]->        feature_scaling
data_transformation      -[ENABLES]->             feature_engineering
feature_scaling          -[PREREQUISITE_FOR]->    machine_learning
feature_engineering      -[ENABLES]->             feature_selection

matplotlib_library       -[PREREQUISITE_FOR]->    seaborn_library
matplotlib_library       -[ENABLES]->             data_visualization
seaborn_library          -[ENABLES]->             data_visualization
data_visualization       -[USES]->                descriptive_statistics

descriptive_statistics   -[COMPONENT_OF]->        mean
descriptive_statistics   -[COMPONENT_OF]->        median
descriptive_statistics   -[COMPONENT_OF]->        variance
descriptive_statistics   -[COMPONENT_OF]->        standard_deviation
variance                 -[PRODUCES]->            standard_deviation
mean                     -[COMPONENT_OF]->        normal_distribution
standard_deviation       -[COMPONENT_OF]->        normal_distribution

distribution             -[INSTANCE_OF]->         normal_distribution
normal_distribution      -[ENABLES]->             central_limit_theorem
central_limit_theorem    -[ENABLES]->             confidence_interval
confidence_interval      -[PREREQUISITE_FOR]->    hypothesis_testing
hypothesis_testing       -[PRODUCES]->            p_value
probability              -[DEFINED_BY]->          distribution

correlation              -[INSTANCE_OF]->         pearson_correlation
correlation              -[PREREQUISITE_FOR]->    regression_analysis
correlation              -[CONTRASTS_WITH]->      p_value

regression_analysis      -[INSTANCE_OF]->         linear_regression
linear_regression        -[USES]->                ordinary_least_squares
linear_regression        -[MEASURED_BY]->         r_squared
linear_regression        -[MEASURED_BY]->         mean_squared_error

scikit_learn             -[IMPLEMENTS]->          linear_regression
scikit_learn             -[IMPLEMENTS]->          cross_validation
scikit_learn             -[IMPLEMENTS]->          feature_selection
train_test_split         -[PREREQUISITE_FOR]->    cross_validation
cross_validation         -[PREVENTS]->            overfitting

overfitting              -[DEFINED_BY]->          bias_variance_tradeoff
overfitting              -[CONTRASTS_WITH]->      r_squared

machine_learning         -[REQUIRES]->            feature_engineering
machine_learning         -[REQUIRES]->            gradient_descent
machine_learning         -[ENABLES]->             neural_networks
neural_networks          -[ENABLES]->             deep_learning
gradient_descent         -[PREREQUISITE_FOR]->    neural_networks

explainable_ai           -[ENABLES]->             model_interpretability
explainable_ai           -[USES]->                shap_values
model_interpretability   -[APPLIED_VIA]->         shap_values
data_ethics              -[REQUIRES]->            explainable_ai
data_ethics              -[REQUIRES]->            reproducibility
reproducibility          -[REQUIRES]->            python_programming
