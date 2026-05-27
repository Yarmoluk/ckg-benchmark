## META
name: Legacy Code Intelligence
version: 1.1.0
domain: legacy-code-intelligence
description: Schema and methodology for building a navigable knowledge graph of any legacy codebase — COBOL, Fortran, PL/I, RPG, or old Java monoliths. Covers risk analysis, copybook dependency mapping, batch job architecture, and COBOL-to-Java migration.
nodes: 70
edges: 127
source: Graphify.md; IBM mainframe documentation; ADM literature; Strangler Fig (Fowler 2004)
license: MIT

---

## NODES

[CONCEPT|legacy_system|Legacy System
  |Production software system that is difficult to modify, poorly documented, and critical to business operations. Defined not by age but by the cost and risk of change. ~220 billion lines of COBOL alone remain in production as of 2026.]

[CONCEPT|cobol_program|COBOL Program
  |A compilation unit in COBOL consisting of four divisions: IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE. The atomic deployable unit on IBM mainframe and mid-range systems. A large bank may have 50,000+ of these.]

[CONCEPT|identification_division|IDENTIFICATION DIVISION
  |First COBOL division — declares the program name and author. Contains metadata, not logic. The only part that tells you what the program is supposed to do.]

[CONCEPT|data_division|DATA DIVISION
  |COBOL division that declares all data structures: FILE SECTION (I/O records), WORKING-STORAGE (memory variables), LINKAGE SECTION (passed parameters). Understanding data division is prerequisite to understanding any logic.]

[CONCEPT|procedure_division|PROCEDURE DIVISION
  |COBOL division containing all executable logic: paragraphs, sections, PERFORM calls, IF/EVALUATE, COMPUTE. Business rules live here. This is where the knowledge is buried.]

[CONCEPT|copybook|Copybook
  |Reusable COBOL data definition file included via COPY statement. Equivalent to a shared header. A single copybook can be used by hundreds of programs — changing one field propagates breakage system-wide.]

[CONCEPT|working_storage|WORKING-STORAGE
  |COBOL section for in-memory variables that persist for the duration of program execution. Business state — accumulators, flags, intermediate values — lives here. Often thousands of lines in older programs.]

[CONCEPT|linkage_section|LINKAGE SECTION
  |COBOL section defining parameters passed to the program by a CALL statement. The interface contract between programs. Undocumented linkage sections are the primary source of integration failures during modernization.]

[CONCEPT|batch_job|Batch Job
  |Scheduled non-interactive program that processes large volumes of records. The backbone of banking, insurance, and payroll. Runs nightly/weekly; a single job may chain 100+ programs. JCL controls execution order.]

[CONCEPT|jcl|JCL (Job Control Language)
  |IBM scripting language that defines batch job execution: which programs run, in what order, with which input/output files. JCL is the orchestration layer above COBOL — rarely documented, frequently tribal knowledge.]

[CONCEPT|vsam_file|VSAM File
  |Virtual Storage Access Method — the dominant file structure in mainframe COBOL. KSDS (keyed), ESDS (sequential), RRDS (relative) variants. VSAM files are the persistent state layer most COBOL programs read and write.]

[CONCEPT|db2_table|DB2 Table
  |IBM relational database table accessed from COBOL via embedded SQL (EXEC SQL ... END-EXEC). Programs that mix COBOL logic with DB2 access are among the hardest to extract business rules from.]

[CONCEPT|subprogram|Subprogram
  |COBOL program invoked via CALL statement. Receives parameters via LINKAGE SECTION. The called program may itself call others — forming the call graph that must be fully mapped before any change.]

[CONCEPT|call_graph|Call Graph
  |Directed graph of CALL relationships between programs. The most critical artifact in legacy modernization: a node is a program, an edge is a CALL. Without this map, change impact is unknowable.]

[CONCEPT|business_rule|Business Rule
  |Domain logic encoded in PROCEDURE DIVISION: interest rate calculations, eligibility thresholds, compliance checks, exception conditions. The highest-value content in any legacy system — survives every hardware migration.]

[CONCEPT|embedded_rule|Embedded Business Rule
  |A business rule with no separation from the code implementing it. No comment, no documentation, no test. The rule is only discoverable by reading the COMPUTE or IF statement and reverse-engineering the intent.]

[CONCEPT|tribal_knowledge|Tribal Knowledge
  |Undocumented system understanding held by engineers who built or maintained it. Exists only in human memory. Lost permanently when those engineers retire. The primary risk in legacy modernization.]

[CONCEPT|technical_debt|Technical Debt
  |Accumulated shortcuts, workarounds, and deferred refactoring that increase the cost of every future change. Legacy systems carry decades of technical debt; some changes require understanding 30 years of layered patches.]

[CONCEPT|change_propagation|Change Propagation
  |The spread of a modification through dependent components. Changing a copybook field propagates to every program that uses it. Changing a VSAM record layout propagates to every program that reads or writes it.]

[CONCEPT|impact_analysis|Impact Analysis
  |Pre-change analysis of which components will be affected by a proposed modification. Impossible without a complete call graph and data dependency map. CKG traversal makes this a graph query.]

[CONCEPT|dead_code|Dead Code
  |Paragraphs, sections, or entire programs that are never CALLed and never executed. Common in legacy systems after years of partial rewrites. Removing it risks removing something referenced by a path no one knew existed.]

[CONCEPT|documentation_gap|Documentation Gap
  |The difference between what a system does and what its documentation says it does. In legacy systems, documentation is typically 20-30 years out of date. The CKG is the living documentation.]

[CONCEPT|ckg_schema|CKG Schema for Legacy Code
  |The set of node types and edge types used to map a legacy codebase as a knowledge graph. Nodes: PROGRAM, COPYBOOK, VSAM_FILE, DB2_TABLE, BATCH_JOB, BUSINESS_RULE, JCL_STEP. Edges: CALLS, COPIES, READS, WRITES, IMPLEMENTS_RULE, INVOKES.]

[CONCEPT|ast_extraction|AST Extraction
  |Parsing legacy source code into an Abstract Syntax Tree to identify CALL statements, COPY statements, data references, and logic patterns. The automated first step in building a legacy CKG.]

[CONCEPT|call_chain|Call Chain
  |A traversal path through the call graph: JOB → JCL_STEP → PROGRAM_A → CALLS → PROGRAM_B → CALLS → PROGRAM_C. The path that must be traced to understand the full execution context of any business rule.]

[CONCEPT|data_lineage|Data Lineage
  |Tracking which programs read, transform, and write which data fields across the system. Required to answer "what populates this field" and "what does changing this field break."]

[CONCEPT|legacy_ckg|Legacy System CKG
  |A CKG built from a specific legacy codebase. Nodes are programs, copybooks, files, rules. Edges are CALLS, COPIES, READS, WRITES. An agent with this CKG can answer impact analysis queries with zero hallucination.]

[CONCEPT|modernization|Legacy Modernization
  |The process of replacing or wrapping legacy systems with modern equivalents while preserving business logic. Estimated $300B annual spend globally. Most large rewrites fail due to incomplete business rule extraction.]

[CONCEPT|strangler_fig|Strangler Fig Pattern
  |Modernization approach (Fowler 2004): build new functionality alongside the legacy system, gradually divert traffic to the new system until the legacy can be decommissioned. Minimizes big-bang rewrite risk.]

[CONCEPT|api_wrapper|API Wrapper
  |Thin modern API layer placed in front of a legacy program. Exposes COBOL functionality as REST/gRPC without rewriting it. Extends legacy life while enabling modern consumption.]

[CONCEPT|event_interception|Event Interception
  |Modernization pattern: intercept transactions at the boundary, publish to an event stream, and process in a modern system in parallel with the legacy. Enables gradual migration without stopping the legacy.]

[CONCEPT|big_bang_rewrite|Big Bang Rewrite
  |Attempting to replace an entire legacy system at once. Historically fails: the rewrite takes years, the legacy keeps evolving, and the new system never matches all the embedded business rules. Highest-risk modernization path.]

[CONCEPT|business_rule_extraction|Business Rule Extraction
  |The process of identifying, naming, and documenting business rules embedded in legacy code. The most labor-intensive step in modernization. CKG encodes the output: BUSINESS_RULE nodes with named edges to implementing programs.]

[CONCEPT|regression_risk|Regression Risk
  |The probability that a change to the legacy system breaks existing functionality. Proportional to undocumented dependencies. CKG traversal reduces this by making impact analysis precise before any change is made.]

[CONCEPT|mainframe|IBM Mainframe
  |IBM z/Series hardware platform running z/OS. Still executes the majority of global financial transactions. COBOL programs run on mainframes. Migration off mainframe is the most common legacy modernization trigger.]

[CONCEPT|rpg_program|RPG Program
  |Report Program Generator — IBM mid-range (AS/400/iSeries/IBM i) equivalent of COBOL. Millions of lines in manufacturing, distribution, and mid-market ERP systems. Same modernization challenges as COBOL.]

[CONCEPT|pl1_program|PL/I Program
  |Programming Language One — IBM systems language between COBOL and C. Used in insurance and scientific computing. Smaller installed base than COBOL but same tribal knowledge and documentation problems.]

[CONCEPT|jcl_step|JCL Step
  |A single program execution within a JCL job. A job consists of multiple steps; each step runs one program with specified input/output. JCL steps are the control flow nodes in the batch execution graph.]

[CONCEPT|file_dependency|File Dependency
  |The relationship between a program and the data files it reads or writes. Two programs sharing a VSAM file are implicitly coupled — a schema change to the file affects both, even if they never CALL each other.]

[CONCEPT|paragraph|COBOL Paragraph
  |Named section of PROCEDURE DIVISION code. The unit of logic organization in COBOL. A large program may have hundreds of paragraphs. PERFORMed paragraphs are the subroutines of COBOL — internal call graph nodes.]

[CONCEPT|perform_statement|PERFORM Statement
  |COBOL statement that executes a paragraph. The internal equivalent of a function call. Internal call graphs (PERFORM chains) are as important as external call graphs (CALL chains) for understanding program logic.]

[CONCEPT|redefines|REDEFINES Clause
  |COBOL data declaration that maps multiple data structures to the same memory location. Used for union types and data conversion. One of the most common sources of hidden complexity — two names for the same bytes.]

[CONCEPT|occurs_clause|OCCURS Clause
  |COBOL declaration for fixed-length arrays (tables). Programs subscript into these with VARYING loops. A table definition in a copybook drives array processing logic in dozens of programs.]

[CONCEPT|pic_clause|PIC Clause
  |COBOL data declaration defining a field's type and size: PIC 9(18) = 18-digit number, PIC X(n) = string, PIC S9(7)V99 = signed decimal with 2 implied decimal places. Wrong PIC clause = silent data corruption — no exception thrown, wrong value silently stored.]

[CONCEPT|comp_3_packed_decimal|COMP-3 Packed Decimal
  |IBM mainframe binary-coded decimal format that stores two digits per byte. Mainframe-native: moving COMP-3 data to Java or any non-mainframe platform requires explicit conversion to BigDecimal. The most common source of silent precision loss in COBOL migrations.]

[CONCEPT|88_level_condition|88-Level Condition
  |COBOL boolean flag defined as a named value of a data field. Example: 88 ACCOUNT-ACTIVE VALUE 'A'. The business meaning of 'A' exists only in the 88-level declaration — and in tribal knowledge. Hundreds of business rules are encoded this way invisibly.]

[CONCEPT|alter_statement|ALTER Statement
  |COBOL statement that modifies GOTO destinations at runtime. Makes static call graph analysis structurally impossible — you cannot know at parse time where control will flow. Its presence in a program is a hard blocker for automated AST extraction.]

[CONCEPT|go_to_statement|GOTO Statement
  |Unconditional branch that transfers control to a named paragraph. Creates non-structured spaghetti control flow. Programs with extensive GOTO use cannot be refactored paragraph-by-paragraph — the entire PROCEDURE DIVISION must be analyzed as a unit.]

[CONCEPT|date_field|Legacy Date Field
  |Two-digit year date fields (PIC 99 for year) still present in post-Y2K systems that received patches but were never fully remediated. Y2K fixes often added windowing logic in obscure utility programs — not in the date fields themselves.]

[CONCEPT|numeric_overflow|Numeric Overflow
  |Silent truncation when a computed value exceeds the declared PIC field size. COBOL does not throw an exception — it silently drops the high-order digits. A PIC 9(5) field receiving a 6-digit result stores the wrong number without warning.]

[CONCEPT|shared_copybook|Shared Copybook
  |A copybook used by 10+ programs across multiple subsystems. The blast radius of any field change is proportional to the usage count. A shared copybook in a large bank may be referenced by 500+ programs across payroll, lending, and compliance subsystems simultaneously.]

[CONCEPT|copybook_dependency_map|Copybook Dependency Map
  |Complete graph of which programs use which copybooks, including transitive dependencies through nested COPYs. Prerequisite for any safe copybook modification. Without this map, impact analysis is guesswork.]

[CONCEPT|impact_radius|Impact Radius
  |The count of programs directly and transitively affected by a change to a single copybook or VSAM record layout. Quantifies change risk before any modification is made. A shared copybook with impact_radius=500 requires a coordinated release across 500 programs.]

[CONCEPT|copybook_version_drift|Copybook Version Drift
  |The same logical copybook exists in slightly-different versions across different subsystems — one field added here, one renamed there. Common in systems assembled through acquisitions. Programs in different subsystems think they share a record layout but don't.]

[CONCEPT|nested_copybook|Nested Copybook
  |A copybook that COPYs other copybooks internally. Creates transitive dependency chains: changing the inner copybook propagates through every outer copybook to every program that uses the outer. Multiplies effective impact_radius.]

[CONCEPT|job_step_dependency|Job Step Dependency
  |Ordering constraint between JCL steps where Step N+1 reads the output file written by Step N. Changing the output format of Step N silently breaks Step N+1 — no compile error, only a runtime failure or wrong data at the next batch run.]

[CONCEPT|job_scheduler|Enterprise Job Scheduler
  |External scheduler (IBM TWS/IWS, CA7, Control-M) that triggers batch jobs on calendars, dependencies, and events. The orchestration layer above JCL. Job dependencies encoded in the scheduler are often undocumented and separate from the JCL itself.]

[CONCEPT|checkpoint_restart|Checkpoint/Restart
  |COBOL batch capability to restart a failed job from an intermediate checkpoint rather than the beginning. Critical for jobs that process millions of records — a restart-from-zero would take hours and corrupt partially-committed data. Must be preserved or re-implemented during migration.]

[CONCEPT|sort_step|SORT Step
  |JCL utility step that sorts an input file before the next program reads it. Not a COBOL program — commonly overlooked in migrations because it has no source to parse. The receiving program implicitly depends on sort order; remove the sort step and get wrong results silently.]

[CONCEPT|cobol_to_java|COBOL-to-Java Migration
  |The most common COBOL modernization target. Involves: data type mapping (PIC → Java types), control flow restructuring (GOTO elimination), runtime replacement (z/OS → JVM), and interface migration (CICS → REST, JCL → Spring Batch). Typically takes 3-7 years for a major bank.]

[CONCEPT|transpilation|Transpilation
  |Automated source-to-source conversion of COBOL to Java (Micro Focus, Blu Age, TSRI). Fast: converts 1M lines in weeks. Produces Java that structurally mirrors COBOL — GOTO becomes labeled loops, PERFORM becomes method calls. Result is running but unmaintainable. Preferred by teams that want to decommission the mainframe, not modernize the code.]

[CONCEPT|data_type_mapping|Data Type Mapping
  |Systematic translation from COBOL PIC clauses to Java/modern types: PIC 9(18) → BigDecimal, PIC X(n) → String, COMP-3 → BigDecimal with explicit scale, PIC S9(7)V99 → BigDecimal(scale=2). Missing or wrong mappings are the primary source of silent calculation errors post-migration.]

[CONCEPT|vsam_to_rdbms|VSAM-to-RDBMS Migration
  |Converting VSAM flat record files to relational database tables. Key decisions: KSDS key → primary key, REDEFINES → nullable columns or separate tables, variable-length records → nullable fields or child tables. Often reveals that the "flat" file was actually a denormalized relational model.]

[CONCEPT|cics_to_rest|CICS-to-REST Migration
  |Replacing CICS online transaction programs with REST APIs. CICS COMMAREA (parameter block) maps to REST request/response body. Transaction ID maps to API endpoint. The hardest part: CICS state management (pseudo-conversational transactions) has no direct REST equivalent.]

[CONCEPT|batch_to_spring_batch|Batch-to-Spring-Batch Migration
  |Converting COBOL batch jobs to Spring Batch (Java). JCL step → Spring Batch Step, VSAM input file → ItemReader, VSAM output file → ItemWriter, SORT step → custom comparator. Checkpoint/restart maps to Spring Batch's built-in job repository.]

[CONCEPT|jcl_to_pipeline|JCL-to-Pipeline Migration
  |Converting JCL job stream definitions to modern pipeline orchestration (Apache Airflow, Jenkins, Control-M for distributed). Preserves job dependency logic in a form that DevOps teams can manage. The scheduler dependency graph must be reverse-engineered before migration.]

[CONCEPT|golden_record_testing|Golden Record Testing
  |Running old and new systems in parallel and comparing outputs byte-by-byte. The only reliable way to validate migration fidelity for financial calculations. Legacy system output = golden record; new system must match exactly. Differences reveal data type mapping errors and embedded rule omissions.]

[CONCEPT|pre_action_grounding|Pre-Action Grounding
  |Pattern: AI agent queries the legacy CKG before generating a code change, migration plan, or impact analysis. The CKG constrains generation to known program relationships — wrong programs don't exist in the graph.]

[CONCEPT|sovereign_deployment|Sovereign Deployment
  |Running the legacy CKG locally on bank or insurer infrastructure, never uploading source code or business rules to a vendor. Required for regulated industries. CKG .md format enables this — no external API needed.]

[CONCEPT|mcp_delivery|MCP Delivery
  |Exposing the legacy CKG via ckg-mcp so Claude Desktop, Cursor, or LangGraph agents can query it as a tool. Enables "what calls this program?" as a first-class agent capability against the live graph.]

---

## EDGES

legacy_system           -[CONTAINS]->           cobol_program
legacy_system           -[CONTAINS]->           batch_job
legacy_system           -[CONTAINS]->           vsam_file
legacy_system           -[CONTAINS]->           jcl
legacy_system           -[ACCUMULATES]->        technical_debt
legacy_system           -[SUFFERS_FROM]->       documentation_gap
legacy_system           -[SUFFERS_FROM]->       tribal_knowledge

cobol_program           -[COMPONENT_OF]->       identification_division
cobol_program           -[COMPONENT_OF]->       data_division
cobol_program           -[COMPONENT_OF]->       procedure_division
cobol_program           -[CALLS]->              subprogram
cobol_program           -[COPIES]->             copybook
cobol_program           -[READS]->              vsam_file
cobol_program           -[WRITES]->             vsam_file
cobol_program           -[READS]->              db2_table
cobol_program           -[CONTAINS]->           business_rule
cobol_program           -[CONTAINS]->           paragraph
cobol_program           -[CONTAINS]->           dead_code

data_division           -[CONTAINS]->           working_storage
data_division           -[CONTAINS]->           linkage_section
procedure_division      -[CONTAINS]->           paragraph
procedure_division      -[CONTAINS]->           perform_statement
procedure_division      -[IMPLEMENTS]->         business_rule

copybook                -[DEFINES]->            working_storage
copybook                -[CAUSES]->             change_propagation
redefines               -[COMPONENT_OF]->       data_division
occurs_clause           -[COMPONENT_OF]->       data_division

subprogram              -[RECEIVES_VIA]->       linkage_section
call_graph              -[COMPOSED_OF]->        cobol_program
call_graph              -[EDGE_TYPE_IS]->       subprogram
call_chain              -[TRAVERSES]->          call_graph

batch_job               -[CONTROLLED_BY]->      jcl
batch_job               -[INVOKES]->            cobol_program
jcl                     -[COMPOSED_OF]->        jcl_step
jcl_step                -[RUNS]->               cobol_program

business_rule           -[INSTANCE_OF]->        embedded_rule
embedded_rule           -[CAUSES]->             documentation_gap
tribal_knowledge        -[ENCODES]->            embedded_rule
tribal_knowledge        -[LOST_WITH]->          documentation_gap

file_dependency         -[COUPLES]->            cobol_program
vsam_file               -[CREATES]->            file_dependency
db2_table               -[CREATES]->            file_dependency

change_propagation      -[REQUIRES]->           impact_analysis
impact_analysis         -[TRAVERSES]->          call_graph
impact_analysis         -[TRAVERSES]->          file_dependency
impact_analysis         -[QUANTIFIES]->         regression_risk

ast_extraction          -[PRODUCES]->           call_graph
ast_extraction          -[PRODUCES]->           data_lineage
ast_extraction          -[BUILDS]->             legacy_ckg
business_rule_extraction -[PRODUCES]->          business_rule
business_rule_extraction -[REQUIRES]->          ast_extraction
business_rule_extraction -[REDUCES]->           tribal_knowledge

legacy_ckg              -[ENCODES]->            call_graph
legacy_ckg              -[ENCODES]->            business_rule
legacy_ckg              -[ENCODES]->            file_dependency
legacy_ckg              -[ENABLES]->            impact_analysis
legacy_ckg              -[ENABLES]->            pre_action_grounding
legacy_ckg              -[REDUCES]->            documentation_gap
legacy_ckg              -[REDUCES]->            regression_risk
legacy_ckg              -[DELIVERED_VIA]->      mcp_delivery
legacy_ckg              -[REQUIRES]->           sovereign_deployment

ckg_schema              -[DEFINES_TYPES_FOR]->  legacy_ckg
ckg_schema              -[PRODUCED_BY]->        ast_extraction

modernization           -[REQUIRES]->           business_rule_extraction
modernization           -[REQUIRES]->           impact_analysis
modernization           -[RISKS]->              big_bang_rewrite

strangler_fig           -[CONTRASTS_WITH]->     big_bang_rewrite
strangler_fig           -[REQUIRES]->           call_graph
api_wrapper             -[WRAPS]->              cobol_program
api_wrapper             -[EXTENDS_LIFE_OF]->    legacy_system
event_interception      -[ENABLES]->            modernization

mainframe               -[RUNS]->               cobol_program
rpg_program             -[SIMILAR_TO]->         cobol_program
pl1_program             -[SIMILAR_TO]->         cobol_program

pre_action_grounding    -[PREVENTS]->           regression_risk
sovereign_deployment    -[REQUIRED_BY]->        mainframe

pic_clause              -[COMPONENT_OF]->       data_division
pic_clause              -[CAUSES]->             numeric_overflow
comp_3_packed_decimal   -[INSTANCE_OF]->        pic_clause
comp_3_packed_decimal   -[REQUIRES]->           data_type_mapping
comp_3_packed_decimal   -[CAUSES]->             regression_risk
88_level_condition      -[COMPONENT_OF]->       data_division
88_level_condition      -[ENCODES]->            embedded_rule
88_level_condition      -[CAUSES]->             documentation_gap
alter_statement         -[PREVENTS]->           ast_extraction
alter_statement         -[CAUSES]->             regression_risk
go_to_statement         -[CAUSES]->             regression_risk
go_to_statement         -[COMPLICATES]->        business_rule_extraction
date_field              -[INSTANCE_OF]->        pic_clause
date_field              -[CAUSES]->             regression_risk
numeric_overflow        -[CAUSED_BY]->          pic_clause
numeric_overflow        -[CAUSES]->             regression_risk

shared_copybook         -[INSTANCE_OF]->        copybook
shared_copybook         -[QUANTIFIED_BY]->      impact_radius
shared_copybook         -[CAUSES]->             change_propagation
copybook_dependency_map -[MAPS]->               shared_copybook
copybook_dependency_map -[ENABLES]->            impact_analysis
copybook_dependency_map -[REQUIRED_BY]->        cobol_to_java
impact_radius           -[DETERMINES]->         regression_risk
impact_radius           -[QUANTIFIES]->         change_propagation
copybook_version_drift  -[INSTANCE_OF]->        technical_debt
copybook_version_drift  -[CAUSES]->             documentation_gap
copybook_version_drift  -[COMPLICATES]->        copybook_dependency_map
nested_copybook         -[INSTANCE_OF]->        copybook
nested_copybook         -[MULTIPLIES]->         impact_radius
legacy_ckg              -[ENCODES]->            copybook_dependency_map

job_step_dependency     -[COMPONENT_OF]->       jcl
job_step_dependency     -[CAUSES]->             change_propagation
job_step_dependency     -[REQUIRES]->           impact_analysis
job_scheduler           -[INVOKES]->            batch_job
job_scheduler           -[CONTAINS]->           job_step_dependency
checkpoint_restart      -[COMPONENT_OF]->       batch_job
checkpoint_restart      -[REQUIRED_BY]->        batch_to_spring_batch
sort_step               -[COMPONENT_OF]->       jcl
sort_step               -[CREATES]->            file_dependency
sort_step               -[CAUSES]->             regression_risk

cobol_to_java           -[INSTANCE_OF]->        modernization
cobol_to_java           -[REQUIRES]->           data_type_mapping
cobol_to_java           -[REQUIRES]->           copybook_dependency_map
cobol_to_java           -[REQUIRES]->           business_rule_extraction
cobol_to_java           -[REQUIRES]->           golden_record_testing
transpilation           -[INSTANCE_OF]->        cobol_to_java
transpilation           -[REQUIRES]->           ast_extraction
transpilation           -[CONTRASTS_WITH]->     strangler_fig
data_type_mapping       -[HANDLES]->            comp_3_packed_decimal
data_type_mapping       -[HANDLES]->            pic_clause
vsam_to_rdbms           -[COMPONENT_OF]->       cobol_to_java
vsam_to_rdbms           -[REQUIRES]->           data_lineage
cics_to_rest            -[COMPONENT_OF]->       cobol_to_java
batch_to_spring_batch   -[COMPONENT_OF]->       cobol_to_java
batch_to_spring_batch   -[HANDLES]->            checkpoint_restart
jcl_to_pipeline         -[COMPONENT_OF]->       cobol_to_java
jcl_to_pipeline         -[REQUIRES]->           job_scheduler
golden_record_testing   -[VALIDATES]->          cobol_to_java
golden_record_testing   -[REQUIRES]->           legacy_ckg
