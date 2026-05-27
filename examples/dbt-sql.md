## META
name: dbt / SQL Analytics Engineering
version: 1.0.0
domain: dbt-sql
description: Data build tool (dbt) and SQL analytics engineering concepts spanning modeling, testing, lineage, materializations, and data warehouse patterns.
nodes: 46
edges: 105
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|dbt|dbt (Data Build Tool)
  |An open-source transformation framework that allows analytics engineers to transform raw data in their warehouse using SELECT statements. dbt handles dependency resolution, testing, documentation, and orchestration of SQL models — bringing software engineering practices to analytics.]

[CONCEPT|dbt_project|dbt Project
  |The root directory structure containing all models, tests, macros, seeds, snapshots, and configuration files for a dbt implementation. Defined by dbt_project.yml which specifies the project name, version, model paths, and default materializations.]

[CONCEPT|dbt_model|dbt Model
  |A single SQL SELECT statement saved as a .sql file that defines a table or view in the data warehouse. Models are the primary unit of work in dbt; each model can reference other models via the ref() function, enabling lineage tracking and ordered execution.]

[CONCEPT|dbt_cloud|dbt Cloud
  |The managed SaaS platform from dbt Labs that provides a browser-based IDE, job scheduling, CI/CD integration, documentation hosting, and team collaboration features on top of dbt Core. Removes the need to manage orchestration infrastructure.]

[CONCEPT|dbt_core|dbt Core
  |The open-source CLI version of dbt, installable via pip. Provides the transformation engine without managed scheduling or UI. Organizations pair dbt Core with orchestrators like Airflow or Prefect and version control via GitHub Actions.]

[CONCEPT|materialization|Materialization
  |The strategy that determines how a dbt model is persisted in the data warehouse — as a table, view, incremental table, or ephemeral CTE. Choosing the right materialization balances query performance, storage cost, and build time.]

[CONCEPT|table_materialization|Table Materialization
  |A dbt materialization that drops and recreates the entire underlying table on every run. Simple and reliable; appropriate for smaller datasets or when downstream consumers need predictable query performance via physical storage.]

[CONCEPT|view_materialization|View Materialization
  |A dbt materialization that creates a database view — a stored SQL query — rather than physically storing data. The view executes at query time, meaning no storage cost but potentially slower downstream queries. Default materialization in dbt.]

[CONCEPT|incremental_model|Incremental Model
  |A dbt materialization strategy that appends or merges only new or changed records into an existing table, rather than rebuilding from scratch. Dramatically reduces build time and warehouse compute cost for large tables with monotonically increasing data.]

[CONCEPT|ephemeral_model|Ephemeral Model
  |A dbt materialization that compiles the model's SQL as a CTE injected into referencing models at compile time, creating no object in the database. Used for intermediate transformation steps that are reused but not queried directly.]

[CONCEPT|ref_function|ref() Function
  |dbt's core dependency declaration function — `{{ ref('model_name') }}` — that compiles to the correct database relation name and registers a dependency edge in the lineage DAG. Enables dbt to run models in topological order and power cross-environment portability.]

[CONCEPT|source_function|source() Function
  |`{{ source('source_name', 'table_name') }}` declares a dependency on a raw data table managed outside dbt. Enables freshness testing, schema documentation, and lineage tracing back to upstream raw data without treating external tables as dbt models.]

[CONCEPT|lineage_dag|Lineage DAG (Directed Acyclic Graph)
  |The dependency graph of all dbt models and sources, automatically constructed from ref() and source() calls. The DAG drives execution order, enables selective re-runs via node selection, and is visualized in dbt Docs as an interactive lineage diagram.]

[CONCEPT|dbt_test|dbt Test
  |An assertion about model data that dbt executes after building models. Tests return a set of failing rows; a test passes when zero rows are returned. dbt tests are the primary mechanism for data quality assurance within the transformation layer.]

[CONCEPT|schema_test|Generic (Schema) Test
  |Built-in dbt tests defined in YAML schema files using a shorthand syntax. The four built-in tests are: not_null, unique, accepted_values, and relationships. Applied per-column across many models without writing custom SQL.]

[CONCEPT|custom_test|Singular (Custom) Test
  |A dbt test defined as a standalone SQL SELECT statement in the tests/ directory. Returns rows that represent test failures. Used for business logic assertions that require joins, aggregations, or complex conditions beyond generic test coverage.]

[CONCEPT|not_null_test|not_null Test
  |A dbt generic test that asserts no row in the specified column contains a NULL value. Fundamental for validating required fields in fact and dimension tables and catching upstream pipeline failures that produce missing values.]

[CONCEPT|unique_test|unique Test
  |A dbt generic test that asserts every value in the specified column appears only once. Critical for validating primary keys and grain definitions; a unique test failure signals a fan-out join or deduplication failure upstream.]

[CONCEPT|dbt_docs|dbt Docs
  |Auto-generated documentation website produced by `dbt docs generate`. Includes model descriptions, column metadata, test coverage, source freshness status, and an interactive lineage DAG visualization. Serves as the living data dictionary for the analytics team.]

[CONCEPT|dbt_seed|dbt Seed
  |A CSV file in the seeds/ directory that dbt loads into the data warehouse as a table. Used for small, static reference datasets — country codes, product categories, cost centers — that change infrequently and benefit from version control.]

[CONCEPT|snapshot|dbt Snapshot
  |A dbt feature that implements Slowly Changing Dimension (SCD) Type 2 history tracking. On each run, dbt compares source data to the snapshot table and inserts new records with valid_from/valid_to timestamps for any changed rows, preserving full history.]

[CONCEPT|scd_type_2|SCD Type 2 (Slowly Changing Dimension Type 2)
  |A data warehousing technique that preserves the full history of changes to a dimension by creating new rows for each change, each with effective_from and effective_to dates and a current_flag. Enables point-in-time reporting on historical states.]

[CONCEPT|macro|dbt Macro
  |A reusable Jinja-templated SQL function defined in the macros/ directory. Called in model SQL or other macros using `{{ macro_name(args) }}`. Macros enable the DRY principle in SQL by abstracting repeated patterns — date spines, surrogate key generation, pivot logic.]

[CONCEPT|jinja_template|Jinja Templating
  |A Python-based templating engine that dbt uses to add dynamic logic — variables, conditionals, loops, and macro calls — to SQL files. Enables environment-aware SQL, conditional logic based on flags, and code generation within dbt models.]

[CONCEPT|dbt_package|dbt Package
  |A collection of reusable dbt models, macros, and tests published on dbt Hub or GitHub. Key packages include dbt-utils (utility macros), dbt-expectations (Great Expectations-style tests), and audit_helper (data diffing). Installed via packages.yml.]

[CONCEPT|profiles_yml|profiles.yml
  |The local configuration file that stores connection details for each dbt target — database host, credentials, schema, warehouse size. Lives outside the dbt project (typically ~/.dbt/) so credentials are never committed to version control.]

[CONCEPT|target_schema|Target Schema
  |The database schema where dbt materializes models during a run. Typically parameterized per environment (dev, staging, prod) via the target.schema variable, so developers build into isolated personal schemas without overwriting production tables.]

[CONCEPT|sql|SQL (Structured Query Language)
  |The declarative language used to define all dbt transformations. dbt extends SQL with Jinja templating but compiles to standard SQL that the target warehouse executes. Analytics engineers need strong SQL skills to build efficient, correct dbt models.]

[CONCEPT|cte|CTE (Common Table Expression)
  |A named temporary result set defined with the WITH clause at the top of a SQL query. CTEs improve readability by breaking complex logic into named steps. dbt models are conventionally structured as chains of CTEs with a final SELECT statement.]

[CONCEPT|window_function|Window Function
  |A SQL function that performs calculations across a set of rows related to the current row, defined by a PARTITION BY and ORDER BY clause. Used for running totals, rankings, lag/lead comparisons, and dense ranking — without collapsing rows like aggregate functions do.]

[CONCEPT|aggregate_function|Aggregate Function
  |A SQL function that computes a single value from a set of rows — SUM, COUNT, AVG, MIN, MAX. Requires GROUP BY to define the grouping grain. The foundation of most fact table metric calculations.]

[CONCEPT|grain|Grain
  |The precise definition of what one row in a table represents — e.g., "one row per order per day per customer." Declaring grain explicitly is the most important design decision in dimensional modeling; grain violations are a primary source of incorrect analytics.]

[CONCEPT|fact_table|Fact Table
  |A central table in a star schema that stores measurable, numeric business events or transactions. Each row represents one occurrence at the defined grain and contains foreign keys to dimension tables plus numeric measures. The primary source of analytical metrics.]

[CONCEPT|dimension_table|Dimension Table
  |A table that provides descriptive context — who, what, where, when, why — for the events recorded in fact tables. Dimensions are denormalized for query performance and updated using SCD techniques when attributes change over time.]

[CONCEPT|star_schema|Star Schema
  |A dimensional modeling pattern where a central fact table is surrounded by denormalized dimension tables connected via foreign keys. Optimized for analytical query performance and BI tool compatibility. Named for its star-shaped entity-relationship diagram.]

[CONCEPT|medallion_architecture|Medallion Architecture
  |A data lakehouse design pattern organizing data into Bronze (raw), Silver (cleaned/conformed), and Gold (aggregated/business-ready) layers. Maps naturally to dbt staging, intermediate, and mart model layers. Common in Databricks and dbt-on-Spark implementations.]

[CONCEPT|idempotency|Idempotency
  |The property that running a dbt model multiple times produces the same result as running it once. Table and incremental (with unique_key) materializations are idempotent; safe reruns after failures are a core dbt design principle.]

[CONCEPT|incremental_strategy|Incremental Strategy
  |The method dbt uses to merge new data into an incremental model. Options include: merge (upsert via unique_key), append (insert-only), and delete+insert (delete matching partitions then reinsert). Strategy choice depends on warehouse capabilities and data patterns.]

[CONCEPT|unique_key|Unique Key
  |A column or combination of columns that uniquely identifies a row in an incremental model, used by the merge and delete+insert strategies to identify records to update or replace. Without a unique_key, dbt can only append rows, risking duplicates.]

[CONCEPT|dry_principle|DRY Principle (Don't Repeat Yourself)
  |Software engineering principle that each piece of logic should be expressed exactly once. In dbt, DRY is achieved by extracting repeated SQL patterns into macros, using packages, and centralizing metric definitions in semantic layer configurations.]

[CONCEPT|slowly_changing_dimension|Slowly Changing Dimension (SCD)
  |A dimension table concept for handling attributes that change over time. SCD Type 1 overwrites old values; SCD Type 2 preserves history with validity timestamps; SCD Type 3 tracks only current and previous values. Snapshots automate SCD Type 2 in dbt.]

[CONCEPT|analytics_engineering|Analytics Engineering
  |The discipline at the intersection of data engineering and data analysis, focused on modeling, testing, and documenting clean, reliable data sets for downstream consumption. Analytics engineers own the transformation layer — from raw source to semantic model.]

[CONCEPT|semantic_layer|Semantic Layer
  |An abstraction layer that defines business metrics, dimensions, and entities centrally so BI tools query consistent definitions rather than raw SQL. dbt's MetricFlow implements a semantic layer above dbt models, ensuring every tool computes revenue the same way.]

[CONCEPT|source_freshness|Source Freshness
  |A dbt feature that checks whether raw source tables have been updated within an expected time window. Configured in sources.yml with warn_after and error_after thresholds. Prevents stale data from flowing undetected into production models.]

[CONCEPT|node_selection|Node Selection
  |dbt's syntax for targeting specific models, tests, or sources in a run. Supports model names, tags, paths, and graph operators (+ for ancestors/descendants, @ for all ancestors). Enables efficient CI/CD by running only models affected by a code change.]

[CONCEPT|environment|dbt Environment
  |A named deployment context (dev, staging, prod) with its own target schema, warehouse credentials, and configuration. dbt Cloud manages environments natively; dbt Core environments are implemented via profiles.yml targets and CI/CD tooling.]

---

## EDGES

dbt                      -[COMPONENT_OF]->           dbt_project
dbt                      -[PRODUCES]->               lineage_dag
dbt                      -[ENABLES]->                analytics_engineering
dbt                      -[INSTANCE_OF]->            dbt_core
dbt                      -[INSTANCE_OF]->            dbt_cloud

dbt_project              -[COMPONENT_OF]->           dbt_model
dbt_project              -[COMPONENT_OF]->           macro
dbt_project              -[COMPONENT_OF]->           dbt_seed
dbt_project              -[COMPONENT_OF]->           snapshot
dbt_project              -[REQUIRES]->               profiles_yml

dbt_model                -[USES]->                   ref_function
dbt_model                -[USES]->                   source_function
dbt_model                -[USES]->                   cte
dbt_model                -[USES]->                   jinja_template
dbt_model                -[DEFINED_BY]->             materialization
dbt_model                -[OUTPUTS]->                target_schema
dbt_model                -[VALIDATED_BY]->           dbt_test

dbt_cloud                -[EXTENDS]->                dbt_core
dbt_cloud                -[MANAGES]->                environment

materialization          -[INSTANCE_OF]->            table_materialization
materialization          -[INSTANCE_OF]->            view_materialization
materialization          -[INSTANCE_OF]->            incremental_model
materialization          -[INSTANCE_OF]->            ephemeral_model

incremental_model        -[REQUIRES]->               unique_key
incremental_model        -[REQUIRES]->               incremental_strategy
incremental_model        -[ENABLES]->                idempotency
incremental_model        -[CONTRASTS_WITH]->         table_materialization

ephemeral_model          -[OUTPUTS]->                cte
ephemeral_model          -[COMPONENT_OF]->           dbt_model

ref_function             -[RESOLVES]->               lineage_dag
ref_function             -[ENABLES]->                node_selection
ref_function             -[PREREQUISITE_FOR]->       idempotency

source_function          -[VALIDATES]->              source_freshness
source_function          -[COMPONENT_OF]->           lineage_dag

lineage_dag              -[VISUALIZED_BY]->          dbt_docs
lineage_dag              -[ENABLES]->                node_selection
lineage_dag              -[DEFINED_BY]->             ref_function

dbt_test                 -[INSTANCE_OF]->            schema_test
dbt_test                 -[INSTANCE_OF]->            custom_test
dbt_test                 -[VALIDATES]->              grain
dbt_test                 -[VALIDATES]->              idempotency

schema_test              -[INSTANCE_OF]->            not_null_test
schema_test              -[INSTANCE_OF]->            unique_test

unique_test              -[VALIDATES]->              grain
unique_test              -[VALIDATES]->              unique_key

not_null_test            -[VALIDATES]->              fact_table
not_null_test            -[VALIDATES]->              dimension_table

dbt_docs                 -[VISUALIZES]->             lineage_dag
dbt_docs                 -[DOCUMENTS]->              dbt_model
dbt_docs                 -[INCLUDES]->               source_freshness

dbt_seed                 -[OUTPUTS]->                dimension_table
dbt_seed                 -[COMPONENT_OF]->           star_schema

snapshot                 -[IMPLEMENTS]->             scd_type_2
snapshot                 -[TRACKS]->                 slowly_changing_dimension
snapshot                 -[REQUIRES]->               unique_key

scd_type_2               -[INSTANCE_OF]->            slowly_changing_dimension
scd_type_2               -[APPLIES_TO]->             dimension_table

macro                    -[USES]->                   jinja_template
macro                    -[ENABLES]->                dry_principle
macro                    -[COMPONENT_OF]->           dbt_package

jinja_template           -[ENABLES]->                dry_principle
jinja_template           -[ENABLES]->                environment

dbt_package              -[EXTENDS]->                macro
dbt_package              -[EXTENDS]->                schema_test

profiles_yml             -[DEFINES]->                environment
profiles_yml             -[DEFINES]->                target_schema

sql                      -[PREREQUISITE_FOR]->       dbt_model
sql                      -[COMPONENT_OF]->           cte
sql                      -[USES]->                   window_function
sql                      -[USES]->                   aggregate_function

cte                      -[ENABLES]->                dry_principle
cte                      -[COMPONENT_OF]->           dbt_model
cte                      -[PREREQUISITE_FOR]->       grain

window_function          -[APPLIES_TO]->             fact_table
window_function          -[CONTRASTS_WITH]->         aggregate_function

aggregate_function       -[DEFINES]->                grain
aggregate_function       -[APPLIES_TO]->             fact_table

grain                    -[DEFINES]->                fact_table
grain                    -[COMPONENT_OF]->           star_schema
grain                    -[VALIDATED_BY]->           unique_test

fact_table               -[COMPONENT_OF]->           star_schema
fact_table               -[COMPONENT_OF]->           medallion_architecture
fact_table               -[REQUIRES]->               dimension_table

dimension_table          -[COMPONENT_OF]->           star_schema
dimension_table          -[IMPLEMENTS]->             slowly_changing_dimension

star_schema              -[INSTANCE_OF]->            medallion_architecture
star_schema              -[ENABLES]->                semantic_layer

medallion_architecture   -[MAPS_TO]->                materialization
medallion_architecture   -[ENABLES]->                analytics_engineering

idempotency              -[REQUIRES]->               unique_key
idempotency              -[ENABLES]->                incremental_strategy

incremental_strategy     -[INSTANCE_OF]->            unique_key
incremental_strategy     -[REQUIRES]->               idempotency

unique_key               -[ENABLES]->                idempotency
unique_key               -[REQUIRED_BY]->            snapshot

dry_principle            -[ENABLES]->                analytics_engineering

slowly_changing_dimension -[IMPLEMENTED_BY]->        scd_type_2
slowly_changing_dimension -[TRACKED_BY]->            snapshot

analytics_engineering    -[REQUIRES]->               sql
analytics_engineering    -[PRODUCES]->               semantic_layer
analytics_engineering    -[USES]->                   dbt

semantic_layer           -[DEFINED_BY]->             grain
semantic_layer           -[BUILT_ON]->               star_schema

source_freshness         -[PREVENTS]->               fact_table
node_selection           -[ENABLES]->                environment
