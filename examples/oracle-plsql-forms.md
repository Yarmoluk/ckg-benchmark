## META
name: Oracle PL/SQL and Oracle Forms Legacy Intelligence
version: 1.0.0
domain: oracle-plsql-forms
description: Oracle PL/SQL language constructs, Oracle Forms and Reports components, Oracle-specific SQL patterns, and migration blockers for legacy Oracle application modernization.
nodes: 50
edges: 85
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|plsql|PL/SQL
  |Oracle's procedural extension to SQL, adding variables, control flow, cursors, exception handling, and modular programming constructs to the relational query language. PL/SQL code runs inside the Oracle database engine, enabling server-side business logic colocated with data.]

[CONCEPT|plsql_package|PL/SQL Package
  |A named schema object that groups related PL/SQL types, variables, constants, cursors, exceptions, procedures, and functions into a single unit. Packages have a specification (public interface) and a body (private implementation), providing encapsulation and performance benefits via session-level caching.]

[CONCEPT|plsql_package_body|PL/SQL Package Body
  |The implementation half of a PL/SQL package containing the executable code for all procedures and functions declared in the package specification. Package bodies can define private subprograms invisible outside the package. Recompiling the body does not invalidate dependent objects referencing the specification.]

[CONCEPT|plsql_procedure|PL/SQL Procedure
  |A named PL/SQL subprogram that performs an action and does not return a value. Procedures accept IN, OUT, and IN OUT parameters and can contain DML, control flow, exception handling, and calls to other subprograms. The primary unit of reusable server-side logic in Oracle applications.]

[CONCEPT|plsql_function|PL/SQL Function
  |A named PL/SQL subprogram that performs a computation and returns a single value. Functions can be called from SQL expressions when they meet purity constraints. Functions declared DETERMINISTIC or PARALLEL_ENABLE integrate with the Oracle query optimizer.]

[CONCEPT|plsql_trigger|PL/SQL Trigger
  |A PL/SQL subprogram automatically invoked by the database engine in response to DML events (INSERT, UPDATE, DELETE) on a table, schema events, or system events. Triggers enforce business rules at the data layer but create invisible dependencies that complicate migration and testing.]

[CONCEPT|plsql_type|PL/SQL Type
  |A user-defined data type declared with CREATE TYPE or within a package, allowing structured data (objects, collections, nested tables, varrays) to be passed between PL/SQL subprograms and stored in Oracle tables. Oracle-specific object types have no direct equivalent in standard SQL databases.]

[CONCEPT|plsql_cursor|PL/SQL Cursor
  |A named pointer to the result set of a SELECT statement that enables row-by-row processing within PL/SQL. Explicit cursors give fine-grained control over fetch loops; implicit cursors are created automatically for DML and single-row SELECT INTO statements.]

[CONCEPT|ref_cursor|REF CURSOR
  |A PL/SQL cursor variable that holds a reference to a query result set rather than the result set itself. REF CURSORs can be passed as parameters between subprograms and returned to client applications, enabling dynamic and parameterized query result passing. SYS_REFCURSOR is the weakly typed Oracle built-in.]

[CONCEPT|bulk_collect|BULK COLLECT
  |A PL/SQL clause that fetches multiple rows from a cursor or SELECT statement into a collection variable in a single context switch between the SQL and PL/SQL engines. Dramatically reduces per-row context-switch overhead, often yielding 10-100× speedups over row-by-row cursor loops.]

[CONCEPT|forall_statement|FORALL Statement
  |A PL/SQL bulk DML construct that sends an entire collection of DML statements to the SQL engine in a single round trip. Used with BULK COLLECT to implement the fetch-process-write pattern with minimal SQL/PL/SQL engine context switches.]

[CONCEPT|exception_handler|PL/SQL Exception Handler
  |A WHEN clause in a PL/SQL EXCEPTION block that catches and handles named or user-defined errors. Oracle provides predefined exceptions (NO_DATA_FOUND, TOO_MANY_ROWS) and allows RAISE_APPLICATION_ERROR for custom codes. Improper handlers that silently swallow errors are a major maintenance hazard.]

[CONCEPT|autonomous_transaction_pragma|PRAGMA AUTONOMOUS_TRANSACTION
  |A compiler directive that makes a PL/SQL subprogram run in its own independent transaction, allowing it to commit or roll back without affecting the caller's transaction. Widespread misuse creates invisible partial commits that bypass normal transaction boundaries. Migration tools cannot detect the side effects without executing the code.]

[CONCEPT|dynamic_sql|Dynamic SQL
  |SQL statements constructed and executed at runtime rather than compile time, enabling flexible query generation based on variable conditions. In PL/SQL, dynamic SQL is executed via EXECUTE IMMEDIATE or the DBMS_SQL package. Dynamic SQL bypasses compile-time dependency tracking and complicates static analysis.]

[CONCEPT|execute_immediate|EXECUTE IMMEDIATE
  |The PL/SQL statement that parses and executes a SQL string or anonymous PL/SQL block at runtime. Supports bind variables via USING clause and retrieves results via INTO or BULK COLLECT INTO. Dynamic table or column names cannot use bind variables and require string concatenation, creating SQL injection risk.]

[CONCEPT|oracle_db|Oracle Database
  |Oracle Corporation's relational database management system with integrated procedural extensions, native object types, advanced replication, partitioning, and fine-grained auditing. The platform on which all Oracle-specific features — PL/SQL, Forms, Reports, Scheduler — depend. Migrating off Oracle requires replacing all proprietary features.]

[CONCEPT|oracle_sequence|Oracle Sequence
  |A schema object that generates unique numeric values independent of any table, used to produce surrogate primary keys. Oracle sequences are stand-alone objects shared across sessions; they differ from ANSI IDENTITY columns and PostgreSQL sequences in syntax and behavior. Sequences must be rewritten during migration.]

[CONCEPT|oracle_synonym|Oracle Synonym
  |A schema object that creates an alias for another database object — table, view, procedure, or database link. Public synonyms provide location transparency across schemas. Synonyms can mask the true location of objects, making dependency analysis and migration difficult.]

[CONCEPT|oracle_directory|Oracle Directory
  |A schema object that maps an alias name to a physical filesystem directory on the database server. Used by UTL_FILE and external table access to read and write OS files. Directory objects tie the database to server-specific filesystem paths, creating infrastructure coupling that blocks migration.]

[CONCEPT|db_link|Database Link
  |An Oracle schema object that defines a connection from one Oracle database to another, enabling cross-database SQL queries and DML using the @ syntax. Database links create hidden inter-database dependencies that are difficult to detect statically and have no equivalent in non-Oracle databases.]

[CONCEPT|materialized_view|Materialized View
  |A database object that stores the precomputed result of a query as a physical table, refreshed on demand or automatically. Oracle's materialized view fast refresh and query rewrite features use advanced log-based change tracking not available in all target migration databases.]

[CONCEPT|oracle_scheduler|Oracle Scheduler
  |The built-in Oracle job scheduling framework (DBMS_SCHEDULER package) that manages recurring and one-time database jobs, job chains, calendaring expressions, and resource consumer groups. Scheduler jobs that execute PL/SQL must be converted when migrating to a non-Oracle platform.]

[CONCEPT|oracle_job|Oracle Scheduler Job
  |A single scheduled task managed by Oracle Scheduler, defined with a name, action (PL/SQL block, stored procedure, or external script), schedule, and enabled state. Jobs are the atomic unit of work in Oracle Scheduler and must be recreated in the target platform's scheduler during migration.]

[CONCEPT|oracle_forms|Oracle Forms
  |Oracle's proprietary RAD framework for building character-mode and then GUI client/server and web data-entry applications connected directly to an Oracle database. Forms applications are defined in binary FMB files and run on a dedicated Forms Runtime or web-deployed Forms Servlet. No open-source equivalent exists.]

[CONCEPT|fmb_file|FMB File (Forms Binary Module)
  |The compiled binary file format that stores an Oracle Forms application — all triggers, items, blocks, parameters, and layout. FMB files are not human-readable; the source-equivalent FMX is generated at compile time. Migration requires Oracle Forms conversion tools or complete manual rewrite.]

[CONCEPT|form_trigger|Oracle Forms Trigger
  |PL/SQL code blocks embedded in an Oracle Forms application that execute in response to user interface events such as WHEN-BUTTON-PRESSED, WHEN-NEW-ITEM-INSTANCE, or KEY-NEXT-ITEM. Triggers contain business logic tightly coupled to the Forms runtime, making them the primary migration challenge in Forms modernization.]

[CONCEPT|form_item|Oracle Forms Item
  |The atomic UI element in an Oracle Forms block — a text field, button, checkbox, list, or image item. Items have built-in database binding properties that automatically fetch and post values to the connected Oracle table without explicit SQL. This auto-binding has no equivalent in modern web frameworks.]

[CONCEPT|form_block|Oracle Forms Block
  |A logical grouping of related form items that corresponds to a database table or view. Data blocks provide automatic query, insert, update, and delete functionality tied to the base table. Control blocks hold items not bound to a database table. The block-to-table coupling is the deepest architectural dependency in Oracle Forms.]

[CONCEPT|forms_runtime|Oracle Forms Runtime
  |The server-side process or web application component that interprets compiled FMX files and renders Oracle Forms applications to client terminals or browsers via the Forms Servlet / Java plugin. Oracle ended mainstream support for Forms 12c in 2023, making runtime obsolescence a key migration driver.]

[CONCEPT|webutil|Oracle Forms WebUtil
  |A client-side Java library integrated with Oracle Forms that provides web-tier functionality — file upload/download, client filesystem access, printer control, and registry access — previously handled by C-language DLL calls in client/server Forms. WebUtil dependencies complicate Forms-to-web migration.]

[CONCEPT|oracle_reports|Oracle Reports
  |Oracle's proprietary report generation tool for producing pixel-perfect columnar, matrix, and master-detail reports from Oracle database queries. Reports are defined in binary RDF files and executed on a Reports Server. Oracle ended active development around Oracle 12c, leaving legacy reports as a modernization target.]

[CONCEPT|rdf_file|RDF File (Reports Definition File)
  |The binary file format storing an Oracle Reports definition — queries, layout, parameters, and format triggers. Like FMB files, RDF files are not human-readable and require Oracle Reports Builder to edit. Migration requires extracting query logic and recreating layout in a modern reporting tool.]

[CONCEPT|reports_server|Oracle Reports Server
  |The middleware component that receives report execution requests, runs Oracle Reports definitions against the database, and returns output in PDF, HTML, or XML format. Reports Server dependencies on Oracle-specific infrastructure block cloud migration without replacing both the report definitions and the serving infrastructure.]

[CONCEPT|rownum|ROWNUM Pseudocolumn
  |An Oracle pseudocolumn that assigns a sequential integer to each row returned by a query, used to implement top-N queries (WHERE ROWNUM <= N). ROWNUM is assigned before ORDER BY is applied, requiring a subquery wrapper for correct ordered top-N results. The ANSI equivalent is FETCH FIRST N ROWS ONLY or ROW_NUMBER() OVER().]

[CONCEPT|connect_by|CONNECT BY (Hierarchical Query)
  |Oracle's proprietary SQL clause for tree and hierarchy traversal — START WITH defines the root condition, CONNECT BY PRIOR defines the parent-child relationship. Produces SYS_CONNECT_BY_PATH, CONNECT_BY_ROOT, and LEVEL pseudocolumns. The ANSI equivalent is a recursive CTE (WITH RECURSIVE), requiring full query rewrites during migration.]

[CONCEPT|merge_statement|MERGE Statement
  |Oracle's implementation of the SQL MERGE (upsert) statement that conditionally inserts, updates, or deletes rows in a target table based on matching rows in a source. Oracle's MERGE syntax predates ANSI SQL:2003 and includes Oracle-specific extensions such as conditional DELETE in the WHEN MATCHED clause.]

[CONCEPT|flashback_query|Flashback Query
  |Oracle's capability to query historical data as it existed at a past point in time using the AS OF TIMESTAMP or AS OF SCN clause. Built on Oracle's Undo tablespace retention. Flashback Query has no standard SQL equivalent; migrating applications that depend on it requires implementing temporal tables in the target database.]

[CONCEPT|oracle_hint|Oracle Query Hint
  |Directives embedded in SQL comments (/*+ HINT */) that instruct the Oracle optimizer to use a specific execution plan — index choice, join method, or parallel degree. Hints are Oracle-proprietary and must be removed or rewritten during migration; incorrect hint removal can cause severe query plan regressions.]

[CONCEPT|dbms_output|DBMS_OUTPUT Package
  |The Oracle built-in package that provides a server-side text buffer readable by SQL*Plus and IDE tools after a PL/SQL block completes. Used ubiquitously for debugging and logging in legacy PL/SQL code. DBMS_OUTPUT has no runtime equivalent in PostgreSQL or other databases; logging must be reimplemented during migration.]

[CONCEPT|utl_file|UTL_FILE Package
  |The Oracle built-in package that allows PL/SQL programs to read and write operating system text files on the database server through Oracle Directory objects. UTL_FILE is frequently used for legacy flat-file ETL and reporting. It has no cross-database equivalent and must be replaced with application-tier file I/O during migration.]

[CONCEPT|dbms_scheduler|DBMS_SCHEDULER Package
  |The PL/SQL API for creating, managing, and monitoring Oracle Scheduler jobs, chains, programs, and schedules. Provides fine-grained scheduling (calendar expressions), job dependencies, and notifications. DBMS_SCHEDULER calls embedded in application code must be replaced with target-platform equivalents during migration.]

[CONCEPT|oracle_migration|Oracle Migration
  |The technical and organizational process of moving an Oracle application stack — PL/SQL logic, Forms, Reports, schemas, and data — to a different database platform. Blocked by the accumulation of Oracle-specific features that have no direct equivalents: dynamic SQL patterns, Forms runtime dependencies, database links, and proprietary SQL syntax.]

[CONCEPT|open_source_db|Open-Source Database
  |A non-Oracle relational database — PostgreSQL, MySQL, MariaDB — targeted during Oracle modernization projects to reduce licensing costs. Open-source databases support ANSI SQL but lack Oracle-proprietary features, requiring application changes proportional to the density of Oracle-specific code in the migrated system.]

[CONCEPT|plsql_to_java|PL/SQL to Java Migration
  |The architectural pattern of moving business logic from Oracle PL/SQL stored procedures into Java (or another JVM language) application-tier services during Oracle modernization. Eliminates server-side procedural logic from the database layer but requires careful transactional boundary redesign.]

[CONCEPT|forms_modernization|Oracle Forms Modernization
  |The process of replacing Oracle Forms applications with modern web or mobile UI frameworks — Angular, React, Oracle APEX, or custom REST APIs. Forms modernization is the most labor-intensive part of Oracle legacy migration because Forms triggers contain interleaved UI and business logic with no clean separation of concerns.]

[CONCEPT|liquibase|Liquibase
  |An open-source database schema change management tool that tracks, versions, and applies database migrations via XML, YAML, JSON, or SQL changelogs. Supports Oracle and open-source databases, enabling controlled schema evolution during Oracle migration projects.]

[CONCEPT|flyway|Flyway
  |An open-source database migration tool that applies versioned SQL migration scripts in order, tracking applied migrations in a schema history table. Simpler than Liquibase; favored for SQL-centric teams. Supports Oracle as a source and most open-source databases as targets during migration.]

[CONCEPT|oracle_apex|Oracle APEX
  |Oracle Application Express — Oracle's low-code web application development platform built on top of the Oracle database. Often used as a modernization path for Oracle Forms, preserving the Oracle database dependency while replacing the Forms runtime with a browser-based UI. Avoids full re-architecture but remains Oracle-locked.]

[CONCEPT|sql_plus|SQL*Plus
  |Oracle's command-line interface for executing SQL and PL/SQL statements, running scripts, and producing formatted reports. SQL*Plus-specific formatting commands (COLUMN, BREAK, TTITLE) and script directives (@, @@, SPOOL) are not portable to other database CLIs and must be replaced during migration.]

[CONCEPT|oracle_lob|Oracle LOB (Large Object)
  |Oracle's native storage type for large binary (BLOB) and character (CLOB, NCLOB) data, managed through the DBMS_LOB package. Oracle LOB semantics — temporary LOBs, LOB locators, and SecureFile LOB storage — differ from the large object handling in PostgreSQL and other open-source databases, requiring data-type mapping during migration.]

---

## EDGES

plsql                         -[RUNS_ON]->                oracle_db
plsql                         -[CONTAINS]->               plsql_package
plsql                         -[CONTAINS]->               plsql_procedure
plsql                         -[CONTAINS]->               plsql_function
plsql                         -[CONTAINS]->               plsql_trigger
plsql                         -[CONTAINS]->               plsql_type
plsql                         -[CONTAINS]->               plsql_cursor

plsql_package                 -[CONTAINS]->               plsql_procedure
plsql_package                 -[CONTAINS]->               plsql_function
plsql_package                 -[IMPLEMENTED_BY]->         plsql_package_body
plsql_package                 -[USES]->                   plsql_type

plsql_package_body            -[IMPLEMENTS]->             plsql_package
plsql_package_body            -[CONTAINS]->               exception_handler

plsql_procedure               -[USES]->                   exception_handler
plsql_procedure               -[USES]->                   plsql_cursor
plsql_procedure               -[USES]->                   dynamic_sql

plsql_function                -[USES]->                   exception_handler
plsql_function                -[USES]->                   plsql_cursor

plsql_trigger                 -[USES]->                   autonomous_transaction_pragma
plsql_trigger                 -[USES]->                   dynamic_sql
plsql_trigger                 -[RUNS_ON]->                oracle_db

plsql_cursor                  -[USES]->                   bulk_collect
plsql_cursor                  -[INSTANCE_OF]->            ref_cursor

bulk_collect                  -[USED_WITH]->              forall_statement

dynamic_sql                   -[USES]->                   execute_immediate
dynamic_sql                   -[PREVENTS]->               oracle_migration

autonomous_transaction_pragma -[BYPASSES]->               plsql_trigger
autonomous_transaction_pragma -[PREVENTS]->               oracle_migration

execute_immediate             -[RUNS_ON]->                oracle_db

dbms_output                   -[USED_IN]->                plsql_procedure
dbms_output                   -[PREVENTS]->               oracle_migration

utl_file                      -[ACCESSES]->               oracle_directory
utl_file                      -[PREVENTS]->               oracle_migration

oracle_directory              -[PREVENTS]->               oracle_migration
oracle_directory              -[USED_BY]->                oracle_db

oracle_db                     -[CONTAINS]->               oracle_sequence
oracle_db                     -[CONTAINS]->               oracle_synonym
oracle_db                     -[CONTAINS]->               materialized_view
oracle_db                     -[CONTAINS]->               oracle_scheduler

db_link                       -[CONNECTS]->               oracle_db
db_link                       -[PREVENTS]->               oracle_migration

oracle_sequence               -[PREVENTS]->               oracle_migration

oracle_synonym                -[PREVENTS]->               oracle_migration

materialized_view             -[USES]->                   oracle_hint
materialized_view             -[PREVENTS]->               oracle_migration

oracle_scheduler              -[USES]->                   oracle_job
oracle_scheduler              -[USES]->                   dbms_scheduler

dbms_scheduler                -[PREVENTS]->               oracle_migration

flashback_query               -[REQUIRES]->               oracle_db
flashback_query               -[PREVENTS]->               oracle_migration

rownum                        -[PREVENTS]->               oracle_migration

connect_by                    -[PREVENTS]->               oracle_migration

merge_statement               -[USES]->                   oracle_db

oracle_hint                   -[USED_IN]->                merge_statement
oracle_hint                   -[PREVENTS]->               oracle_migration

oracle_forms                  -[DEFINED_BY]->             fmb_file
oracle_forms                  -[USES]->                   form_trigger
oracle_forms                  -[USES]->                   form_item
oracle_forms                  -[USES]->                   form_block
oracle_forms                  -[RUNS_ON]->                forms_runtime
oracle_forms                  -[USES]->                   webutil
oracle_forms                  -[RUNS_ON]->                oracle_db
oracle_forms                  -[PREVENTS]->               oracle_migration

form_trigger                  -[USES]->                   plsql
form_trigger                  -[PREVENTS]->               oracle_migration

form_block                    -[CONTAINS]->               form_item
form_block                    -[USES]->                   oracle_db

oracle_reports                -[DEFINED_BY]->             rdf_file
oracle_reports                -[RUNS_ON]->                reports_server
oracle_reports                -[RUNS_ON]->                oracle_db
oracle_reports                -[PREVENTS]->               oracle_migration

oracle_migration              -[TARGETS]->                open_source_db
oracle_migration              -[USES]->                   liquibase
oracle_migration              -[USES]->                   flyway

liquibase                     -[MANAGES]->                oracle_db
flyway                        -[MANAGES]->                oracle_db

plsql_to_java                 -[REPLACES]->               plsql_package

forms_modernization           -[REPLACES]->               oracle_forms
forms_modernization           -[USES]->                   oracle_apex

oracle_apex                   -[RUNS_ON]->                oracle_db
oracle_apex                   -[REPLACES]->               forms_runtime

sql_plus                      -[RUNS_ON]->                oracle_db
sql_plus                      -[PREVENTS]->               oracle_migration

oracle_lob                    -[MANAGED_BY]->             oracle_db
oracle_lob                    -[PREVENTS]->               oracle_migration
