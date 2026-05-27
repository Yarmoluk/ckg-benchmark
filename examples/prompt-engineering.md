## META
name: Prompt Engineering
version: 1.0.0
domain: prompt-engineering
description: The craft and science of designing inputs to LLMs that reliably produce accurate, useful, and safe outputs.
nodes: 54
edges: 73
source: McCreary Intelligent Textbook Corpus (MIT)
license: MIT

---

## NODES

[CONCEPT|large_language_model|Large Language Model
  |Neural network trained on massive text corpora to predict and generate tokens. The system being prompted — understanding its architecture explains why prompt structure matters.]

[CONCEPT|transformer_architecture|Transformer Architecture
  |Self-attention-based neural network architecture underlying all modern LLMs. Attention heads allow the model to relate tokens across long distances, which makes context window position meaningful.]

[CONCEPT|token|Token
  |Atomic unit of text processed by an LLM — roughly a word fragment. Models think in tokens, not words, so token choice and count directly affect cost, context capacity, and output quality.]

[CONCEPT|tokenization|Tokenization
  |Process of splitting raw text into tokens using a learned vocabulary (e.g., BPE). Affects how the model perceives punctuation, code, multilingual text, and numerical values.]

[CONCEPT|context_window|Context Window
  |Fixed-size token budget available to the model for input + output in a single inference call. Every prompt element consumes context; trade-offs between instruction length and available response space are real.]

[CONCEPT|inference|Inference
  |The forward pass of a trained model to generate output from a given input prompt. Temperature, sampling strategy, and prompt structure are tunable only at inference time.]

[CONCEPT|foundation_model|Foundation Model
  |Large model pre-trained on broad data and adapted to many tasks. Prompt engineering is the primary interface for directing foundation models without retraining.]

[CONCEPT|fine_tuning|Fine-Tuning
  |Updating a pre-trained model's weights on a narrower dataset for a specific task. When prompt engineering alone cannot reliably shape behavior, fine-tuning is the next intervention.]

[CONCEPT|prompt|Prompt
  |The complete text input passed to an LLM at inference time, comprising instructions, context, examples, and constraints. The single most controllable variable in a deployed LLM system.]

[CONCEPT|prompt_engineering|Prompt Engineering
  |Iterative discipline of designing, testing, and refining prompts to maximize LLM output quality for a given task. Combines linguistic intuition with empirical evaluation.]

[CONCEPT|system_prompt|System Prompt
  |Instruction block injected before user input, typically by the application developer. Sets model role, tone, constraints, and task framing — invisible to end users but high-leverage.]

[CONCEPT|user_prompt|User Prompt
  |The runtime input from the end user within an ongoing interaction. Shaped by but separate from the system prompt; together they form the full context the model reasons over.]

[CONCEPT|prompt_structure|Prompt Structure
  |Deliberate arrangement of components: role assignment, task description, examples, constraints, and output format. Structure guides the model's attention allocation across the context window.]

[CONCEPT|instruction_clarity|Instruction Clarity
  |Degree to which a prompt leaves no ambiguity about what the model should do. Vague instructions produce high output variance; precise instructions narrow the distribution toward desired outputs.]

[CONCEPT|specificity|Specificity
  |Concreteness of constraints and expected outputs in a prompt. "Write a 3-sentence summary for a non-expert reader" is more specific than "summarize this." Specificity reduces unwanted model creativity.]

[CONCEPT|task_decomposition|Task Decomposition
  |Breaking a complex task into ordered subtasks, either in a single prompt or across a chain. Models perform better on tractable sub-problems than on monolithic instructions.]

[CONCEPT|prompt_length|Prompt Length
  |Token count consumed by a prompt, trading off against available response tokens. Long prompts with redundant context can dilute attention on key instructions.]

[CONCEPT|prompt_iteration|Prompt Iteration
  |Systematic cycle of writing a prompt, observing outputs, diagnosing failure modes, and revising. Rarely is a first-draft prompt production-ready.]

[CONCEPT|prompt_testing|Prompt Testing
  |Running a prompt against a diverse set of inputs and measuring output quality against defined criteria. Distinguishes accidental correctness from reliable behavior.]

[CONCEPT|response_quality|Response Quality
  |Multi-dimensional assessment of LLM output: accuracy, coherence, relevance, format compliance, and safety. The target variable prompt engineering attempts to maximize.]

[CONCEPT|tone_control|Tone Control
  |Explicit instruction to the model about register — formal, casual, empathetic, concise. Tone is learnable from examples or directly specified; leaving it unspecified risks mismatch with audience expectations.]

[CONCEPT|audience_adaptation|Audience Adaptation
  |Calibrating vocabulary, assumed knowledge, and explanation depth to a target reader. A prompt that specifies "explain to a high school student" yields systematically different outputs than one targeting domain experts.]

[CONCEPT|zero_shot_prompting|Zero-Shot Prompting
  |Asking the model to perform a task with only instructions and no examples. Relies entirely on knowledge encoded during pre-training. Fails predictably on tasks with unusual output formats.]

[CONCEPT|few_shot_prompting|Few-Shot Prompting
  |Including a small number of input-output examples in the prompt to demonstrate the desired pattern. Especially powerful for format conformance and stylistic consistency.]

[CONCEPT|example_selection|Example Selection
  |Choosing which examples to include in a few-shot prompt. High-quality, diverse examples that span edge cases outperform random selection. Bad examples can actively mislead the model.]

[CONCEPT|chain_of_thought_prompting|Chain-of-Thought Prompting
  |Eliciting explicit intermediate reasoning steps before a final answer. Models that "show their work" make fewer logical errors, particularly on math, logic, and multi-step inference tasks.]

[CONCEPT|step_by_step_reasoning|Step-by-Step Reasoning
  |Intermediate reasoning structure produced by chain-of-thought prompting. Each step constrains the next, reducing error propagation compared to direct answer generation.]

[CONCEPT|self_consistency|Self-Consistency
  |Sampling multiple chain-of-thought outputs from the same prompt and selecting the most frequent final answer. Improves reliability without fine-tuning by averaging out stochastic errors.]

[CONCEPT|tree_of_thoughts|Tree of Thoughts
  |Extends chain-of-thought into a search tree where the model explores multiple reasoning branches and backtracks from dead ends. Effective for planning and combinatorial problems.]

[CONCEPT|prompt_chaining|Prompt Chaining
  |Passing the output of one prompt as the input to the next in a sequence. Enables complex workflows that exceed what any single prompt can accomplish within a context window.]

[CONCEPT|prompt_templates|Prompt Templates
  |Parameterized prompt structures with variable slots filled at runtime. Enable consistent, maintainable prompts across many use cases while reducing per-call engineering effort.]

[CONCEPT|role_assignment|Role Assignment
  |Instructing the model to adopt a specific professional or character persona. "You are a senior security engineer" shifts the model's prior toward domain-appropriate vocabulary and reasoning patterns.]

[CONCEPT|persona_prompting|Persona Prompting
  |Assigning a detailed character description — name, background, communication style — to shape model behavior beyond task role. Useful for consistent brand voice in product applications.]

[CONCEPT|constraint_setting|Constraint Setting
  |Explicit restrictions in a prompt: word limits, prohibited topics, required format, scope boundaries. Without constraints, models optimize for plausibility, not usefulness.]

[CONCEPT|negative_prompting|Negative Prompting
  |Specifying what the model should NOT do or produce. Reduces false positives from underspecified positive constraints. "Do not include caveats or disclaimers" is a well-known productivity pattern.]

[CONCEPT|delimiter_usage|Delimiter Usage
  |Using clear separators (triple backticks, XML tags, dashes) to segment prompt regions. Prevents the model from treating user-supplied content as instruction — a core defense against prompt injection.]

[CONCEPT|contextual_priming|Contextual Priming
  |Providing background information in the prompt that shifts the model's interpretive frame. A model primed with a clinical context interprets ambiguous terms differently than one primed with consumer context.]

[CONCEPT|meta_prompting|Meta-Prompting
  |Using a prompt to generate or improve another prompt. Enables automated prompt optimization, though the generated prompt still requires human validation before deployment.]

[CONCEPT|prompt_compression|Prompt Compression
  |Reducing token count while preserving semantic content. Techniques include paraphrasing, removing redundancy, and using structured formats. Critical for long-context tasks approaching window limits.]

[CONCEPT|temperature_setting|Temperature Setting
  |Inference parameter controlling output randomness. Temperature 0 gives near-deterministic, highest-probability outputs. Higher values increase diversity but risk incoherence. A key dial for creative vs. factual tasks.]

[CONCEPT|top_p_sampling|Top-P Sampling
  |Nucleus sampling: the model samples only from tokens whose cumulative probability exceeds threshold P. Interacts with temperature — both should be tuned together, not independently.]

[CONCEPT|max_tokens|Max Tokens Setting
  |Hard upper bound on output token count. Prevents runaway generation costs and forces the model to be concise. Set too low, it truncates answers mid-sentence.]

[CONCEPT|output_format_specification|Output Format Specification
  |Explicit instruction about the structure of the desired output: list, table, JSON, prose paragraph. LLMs conform well when format requirements are stated early in the prompt.]

[CONCEPT|json_output|JSON Output
  |Requesting structured JSON from the model. Enables programmatic downstream consumption. Most models support JSON mode natively; without it, schema-guided prompting improves reliability.]

[CONCEPT|schema_guided_output|Schema-Guided Output
  |Providing a target JSON schema or template in the prompt so the model fills in values rather than inventing structure. Dramatically reduces output parsing errors in production pipelines.]

[CONCEPT|context_management|Context Management
  |Strategy for what to include in the context window given finite token budgets: conversation history pruning, document chunking, summarization of prior turns.]

[CONCEPT|retrieval_augmented_generation|Retrieval-Augmented Generation
  |Injecting retrieved external documents into the prompt at inference time to ground model outputs in current or domain-specific knowledge. Reduces hallucination on factual queries.]

[CONCEPT|hallucination|Hallucination
  |Model assertion of false or fabricated information presented with apparent confidence. Caused by gaps between training data and query scope. Retrieval and constraint-setting are primary mitigations.]

[CONCEPT|factual_accuracy|Factual Accuracy
  |Proportion of model claims in an output that are verifiably correct. The primary quality dimension for informational tasks; trades off against creativity for generative tasks.]

[CONCEPT|prompt_injection|Prompt Injection
  |Attack where adversarial content in user input or retrieved documents overrides the system prompt's instructions. A structural vulnerability when system and user content are not clearly separated.]

[CONCEPT|guardrails|Guardrails
  |Hard constraints enforced at the system prompt or infrastructure layer to prevent the model from producing harmful, off-topic, or policy-violating outputs. First line of defense in production deployments.]

[CONCEPT|prompt_evaluation|Prompt Evaluation
  |Systematic measurement of prompt performance across a test set. Moves prompt engineering from intuition-driven to evidence-driven. Required before any prompt reaches production.]

[CONCEPT|token_efficiency|Token Efficiency
  |Ratio of task-relevant information to total tokens consumed. High token efficiency means the model gets signal, not noise. Tracked as RDS in the CKG benchmark.]

[CONCEPT|cost_optimization|Cost Optimization
  |Minimizing API spend per unit of output quality. Achieved through prompt compression, caching, model tiering, and batching. Token efficiency is the primary lever.]

---

## EDGES

large_language_model       -[PREREQUISITE_FOR]->     prompt_engineering
transformer_architecture   -[ENABLES]->              context_window
transformer_architecture   -[COMPONENT_OF]->         large_language_model
token                      -[DEFINED_BY]->            tokenization
token                      -[COMPONENT_OF]->          context_window
tokenization               -[PREREQUISITE_FOR]->      prompt_length
context_window             -[CONSTRAINS]->            prompt_length
context_window             -[CONSTRAINS]->            context_management
inference                  -[REQUIRES]->              large_language_model
inference                  -[CONTROLLED_BY]->         temperature_setting
foundation_model           -[INSTANCE_OF]->           large_language_model
fine_tuning                -[IMPROVES_ON]->           zero_shot_prompting
fine_tuning                -[BUILDS_ON]->             foundation_model
prompt                     -[INSTANCE_OF]->           user_prompt
prompt                     -[COMPONENT_OF]->          prompt_structure
prompt_engineering         -[PRODUCES]->              prompt
prompt_engineering         -[REQUIRES]->              prompt_iteration
prompt_engineering         -[USES]->                  prompt_evaluation
system_prompt              -[COMPONENT_OF]->          prompt_structure
system_prompt              -[ENABLES]->               role_assignment
system_prompt              -[ENABLES]->               guardrails
system_prompt              -[MITIGATES]->             prompt_injection
user_prompt                -[COMPONENT_OF]->          prompt_structure
prompt_structure           -[DETERMINES]->            response_quality
instruction_clarity        -[IMPROVES_ON]->           response_quality
specificity                -[BUILDS_ON]->             instruction_clarity
specificity                -[COMPONENT_OF]->          constraint_setting
task_decomposition         -[ENABLES]->               prompt_chaining
task_decomposition         -[PREREQUISITE_FOR]->      chain_of_thought_prompting
prompt_length              -[TRADES_OFF_WITH]->       context_window
prompt_iteration           -[REQUIRES]->              prompt_testing
prompt_iteration           -[PRODUCES]->              response_quality
prompt_testing             -[INSTANCE_OF]->           prompt_evaluation
response_quality           -[MEASURED_BY]->           prompt_evaluation
tone_control               -[COMPONENT_OF]->          prompt_structure
audience_adaptation        -[BUILDS_ON]->             tone_control
zero_shot_prompting        -[PREREQUISITE_FOR]->      few_shot_prompting
few_shot_prompting         -[REQUIRES]->              example_selection
few_shot_prompting         -[IMPROVES_ON]->           zero_shot_prompting
chain_of_thought_prompting -[BUILDS_ON]->             few_shot_prompting
chain_of_thought_prompting -[ENABLES]->               step_by_step_reasoning
step_by_step_reasoning     -[PREREQUISITE_FOR]->      self_consistency
self_consistency           -[IMPROVES_ON]->           chain_of_thought_prompting
tree_of_thoughts           -[EXTENDS]->               chain_of_thought_prompting
tree_of_thoughts           -[BUILDS_ON]->             self_consistency
prompt_chaining            -[USES]->                  prompt_templates
prompt_chaining            -[ENABLES]->               meta_prompting
prompt_templates           -[IMPLEMENTS]->            prompt_structure
role_assignment            -[USES]->                  persona_prompting
constraint_setting         -[COMPONENT_OF]->          prompt_structure
negative_prompting         -[INSTANCE_OF]->           constraint_setting
delimiter_usage            -[MITIGATES]->             prompt_injection
delimiter_usage            -[COMPONENT_OF]->          prompt_structure
contextual_priming         -[BUILDS_ON]->             system_prompt
meta_prompting             -[BUILDS_ON]->             prompt_chaining
prompt_compression         -[IMPROVES_ON]->           token_efficiency
prompt_compression         -[REQUIRES]->              context_management
temperature_setting        -[COMPONENT_OF]->          inference
top_p_sampling             -[COMPONENT_OF]->          inference
top_p_sampling             -[INTERACTS_WITH]->        temperature_setting
max_tokens                 -[CONSTRAINS]->            response_quality
output_format_specification -[COMPONENT_OF]->         prompt_structure
json_output                -[INSTANCE_OF]->           output_format_specification
schema_guided_output       -[EXTENDS]->               json_output
context_management         -[ENABLES]->               retrieval_augmented_generation
retrieval_augmented_generation -[MITIGATES]->         hallucination
hallucination              -[CONTRASTS_WITH]->        factual_accuracy
factual_accuracy           -[REQUIRES]->              retrieval_augmented_generation
prompt_injection           -[THREATENS]->             system_prompt
guardrails                 -[MITIGATES]->             hallucination
prompt_evaluation          -[PRODUCES]->              token_efficiency
token_efficiency           -[ENABLES]->               cost_optimization
cost_optimization          -[REQUIRES]->              prompt_compression
