## META
name: RPG and IBM i Platform Intelligence
version: 1.0.0
domain: rpg-ibm-i
description: Compact knowledge graph of RPG language evolution, IBM i platform architecture, ILE concepts, data access patterns, and modernization blockers for legacy system migration.
nodes: 50
edges: 77
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|rpg|RPG Language
  |Report Program Generator, an IBM programming language introduced in 1959 originally designed for punched-card business report processing and later evolved into a general-purpose application language on IBM midrange systems.]

[CONCEPT|rpg_ii|RPG II
  |Second generation of RPG introduced with the System/3 and System/38, adding cycle indicators, array support, and structured file access while retaining fixed-column specification format.]

[CONCEPT|rpg_iii|RPG III
  |Third generation of RPG introduced on the System/38 and AS/400, adding structured programming constructs (IF/ELSE/ENDIF, DO loops) and eliminating some reliance on the implicit program cycle.]

[CONCEPT|rpg_iv|RPG IV
  |Fourth generation of RPG introduced in 1994 on the AS/400, extending to 10-character names, free-form expressions, built-in functions, and full ILE support, also called ILE RPG or RPGLE.]

[CONCEPT|ile_rpg|ILE RPG
  |The ILE-compatible version of RPG IV that compiles to modules, supports service programs and binding directories, enables procedure calls across languages, and is the current strategic RPG dialect.]

[CONCEPT|free_form_rpg|Free-Form RPG
  |A coding style introduced in RPG IV (fully supported from V7.1) that abandons fixed-column specification positions, allowing C-style syntax and eliminating the need for spec-type codes in the C-spec area.]

[CONCEPT|fixed_form_rpg|Fixed-Form RPG
  |The traditional RPG coding style where each source line is divided into fixed-column fields for spec type, factor 1, operation, factor 2, and result, inherited from punched-card conventions and still prevalent in legacy code.]

[CONCEPT|f_spec|F-Spec (File Description)
  |A fixed-form RPG specification line beginning with F in column 6 that declares every file used by the program, specifying file type, processing mode, record length, and device type.]

[CONCEPT|d_spec|D-Spec (Definition)
  |A fixed-form RPG specification line beginning with D in column 6 that declares standalone variables, data structures, constants, and prototypes, replaced in free-form by DCL-S, DCL-DS, and DCL-PR.]

[CONCEPT|c_spec|C-Spec (Calculation)
  |A fixed-form RPG specification line beginning with C in column 6 containing program logic operations, including conditioning indicators, factor 1, operation code, factor 2, result field, and resulting indicators.]

[CONCEPT|o_spec|O-Spec (Output)
  |A fixed-form RPG specification line beginning with O in column 6 that controls printed or display output, specifying fields, edit codes, and conditioning, largely superseded by display files and printer files.]

[CONCEPT|rpg_cycle|RPG Program Cycle
  |A hardwired read-process-write loop implicitly embedded in every RPG program that automatically reads the primary file, performs calculations conditioned by indicators, writes output, and repeats until Last Record (LR) is set. Predates structured programming and has no equivalent in modern languages, causing automated migration tools to fail.]

[CONCEPT|indicator|RPG Indicator
  |A two-digit (01–99) boolean flag used in fixed-form RPG to condition calculations and output, set by file operations, comparison results, or explicit SETOF/SETON operations; a major readability and migration obstacle.]

[CONCEPT|lr_indicator|LR Indicator
  |Last Record indicator (LR) that when set causes the RPG program cycle to perform final totals processing and end program execution; the primary mechanism for terminating the implicit RPG cycle.]

[CONCEPT|ibm_i|IBM i
  |IBM's integrated operating system and platform (formerly OS/400) running on IBM Power Systems hardware, providing an integrated database, security, and job management environment optimized for business applications.]

[CONCEPT|as400|AS/400
  |IBM's Application System/400 midrange computer introduced in 1988, the predecessor to IBM i, combining hardware and OS in a tightly integrated system with a single-level store architecture and integrated relational database.]

[CONCEPT|cl_program|CL Program
  |A Control Language program compiled on IBM i that executes CL commands to manage jobs, files, libraries, and system resources, commonly used to orchestrate RPG program calls and set up the library list.]

[CONCEPT|cl_command|CL Command
  |A named IBM i command (e.g., CALL, CRTPF, OVRDBF) with keyword parameters that performs a discrete system operation, usable interactively, in CL programs, or from job control.]

[CONCEPT|display_file|Display File
  |An IBM i externally described file that defines screen formats for interactive applications, used by RPG programs via the WORKSTN device type to present and collect data through 5250 terminal emulation.]

[CONCEPT|printer_file|Printer File
  |An IBM i externally described file that defines report layouts and spool attributes used by RPG programs via the PRINTER device type to produce formatted printed output routed to the output queue.]

[CONCEPT|dds|Data Description Specifications
  |IBM i source member format used to externally describe the fields, keys, and attributes of physical files, logical files, display files, and printer files, decoupling data structure from program code.]

[CONCEPT|physical_file|Physical File
  |An IBM i database object that stores actual data records in a flat table structure, analogous to a base table in SQL, defined via DDS or SQL CREATE TABLE and accessed by RPG and CL programs.]

[CONCEPT|logical_file|Logical File
  |An IBM i database object that provides a keyed or subset view over one or more physical files, analogous to an SQL view or index, defined via DDS to present data in an alternate sequence or with record selection.]

[CONCEPT|db2_for_i|DB2 for IBM i
  |The integrated relational database management system embedded in IBM i, storing all data as IBM i objects and accessible via SQL, RPG embedded SQL, or native file I/O without a separate database server.]

[CONCEPT|embedded_sql|Embedded SQL
  |SQL statements coded directly within RPG (or other ILE language) source using the EXEC SQL prefix and precompiled by the SQL precompiler, enabling set-based data access and replacing procedural file operations.]

[CONCEPT|opnqryf|OPNQRYF Command
  |Open Query File CL command that dynamically applies record selection, join, and ordering to a database file access path at runtime, historically used to implement query logic before embedded SQL was practical; a modernization obstacle.]

[CONCEPT|libl|Library List
  |An ordered list of IBM i libraries searched when resolving object references by name, analogous to a PATH variable; set per job and manipulated by CL programs to control which version of a program or file is used.]

[CONCEPT|library_object|IBM i Library Object
  |An IBM i container object (*LIB) that groups related programs, files, data areas, and other objects, functioning as a namespace and the primary unit of deployment and authority management.]

[CONCEPT|ile|Integrated Language Environment
  |IBM i's bindable program model that allows modules compiled from RPG, C, COBOL, and CL to be bound together into programs or service programs, enabling modular design and cross-language procedure calls.]

[CONCEPT|service_program|Service Program
  |An ILE object (*SRVPGM) containing exported procedures that can be called by multiple programs without copying code, analogous to a shared library or DLL, activated within an activation group.]

[CONCEPT|binding_directory|Binding Directory
  |An IBM i object (*BNDDIR) that lists service programs and modules to be searched during the bind step when creating an ILE program or service program, simplifying dependency management.]

[CONCEPT|activation_group|Activation Group
  |A runtime scoping construct within an IBM i job that groups ILE programs and service programs sharing storage, commitment control scope, and error handling, controlling resource lifetime and isolation.]

[CONCEPT|subfile|Subfile
  |A special display file record format on IBM i that holds multiple records for list-style screen presentation, allowing RPG programs to load a page of records and display them in a scrollable grid on a 5250 screen.]

[CONCEPT|message_queue|Message Queue
  |An IBM i object (*MSGQ) that holds messages sent between jobs, users, or programs, used for asynchronous inter-process communication and operator notifications.]

[CONCEPT|data_queue|Data Queue
  |An IBM i object (*DTAQ) that provides a high-performance FIFO or LIFO queue for passing data between jobs without file I/O overhead, commonly used for trigger-based and real-time integration patterns.]

[CONCEPT|job_queue|Job Queue
  |An IBM i object (*JOBQ) that holds submitted batch jobs waiting to be selected by a subsystem for execution, controlling job throughput and scheduling priority.]

[CONCEPT|batch_job_ibmi|IBM i Batch Job
  |A non-interactive job submitted to a job queue on IBM i that executes RPG or CL programs in the background, managed by subsystem descriptions and subject to job scheduling and resource limits.]

[CONCEPT|journal|Journal
  |An IBM i object (*JRN) that records before and after images of database changes to journal receivers, providing the foundation for commitment control, replication, and audit trails.]

[CONCEPT|journal_receiver|Journal Receiver
  |An IBM i object (*JRNRCV) that physically stores the journal entries written by the journal, detached and archived periodically to manage disk space while preserving the audit trail.]

[CONCEPT|commitment_control|Commitment Control
  |An IBM i transaction management facility that groups database changes into atomic units of work that can be committed or rolled back, requiring journaling to be active on all files involved in the transaction.]

[CONCEPT|module_object|ILE Module
  |An intermediate compiled object (*MODULE) produced by compiling an ILE RPG, C, COBOL, or CL source member, not directly executable but bound into programs or service programs during the bind step.]

[CONCEPT|program_object|IBM i Program Object
  |A bound ILE executable object (*PGM) created by binding one or more modules and optionally service programs, the deployable and callable unit of execution on IBM i.]

[CONCEPT|data_area|Data Area
  |An IBM i object (*DTAARA) that stores a small amount of data accessible to any job on the system without file I/O, used for global configuration values, job-to-job communication, and lock coordination.]

[CONCEPT|spool_file_ibmi|IBM i Spool File
  |A temporary file in an output queue (*OUTQ) holding formatted printer output generated by RPG or system commands, pending printing or online viewing via IBM i output management.]

[CONCEPT|override_command|OVRDBF / Override Command
  |A CL command (e.g., OVRDBF, OVRDSPF) that redirects file references at runtime, allowing a single RPG program to access different physical or logical files without recompilation.]

[CONCEPT|rpg_modernization|RPG Modernization
  |The process of migrating fixed-form RPG programs with cycle logic and indicator usage to free-form ILE RPG, embedded SQL, web services, or off-platform languages, blocked primarily by implicit cycle dependencies and indicator proliferation.]

[CONCEPT|code_for_ibm_i|Code for IBM i
  |A Visual Studio Code extension and set of IBM i development tools providing modern IDE capabilities, remote source editing, and debugging for RPG, CL, and COBOL programs on IBM i.]

[CONCEPT|lansa|LANSA
  |A cross-platform rapid application development framework for IBM i and web that abstracts RPG and DDS complexity, providing a proprietary 4GL and code generation engine for building modernized business applications.]

[CONCEPT|sqlrpgle|SQLRPGLE
  |An ILE RPG source type that embeds SQL statements precompiled by the SQL precompiler, enabling set-based database access within RPG programs and representing the primary modernization path for file I/O replacement.]

---

## EDGES

rpg                      -[EVOLVED_INTO]->            rpg_ii
rpg_ii                   -[EVOLVED_INTO]->            rpg_iii
rpg_iii                  -[EVOLVED_INTO]->            rpg_iv
rpg_iv                   -[INSTANCE_OF]->             ile_rpg
ile_rpg                  -[SUPPORTS]->                free_form_rpg
ile_rpg                  -[COMPILES_TO]->             module_object
module_object            -[BOUND_INTO]->              program_object
module_object            -[BOUND_INTO]->              service_program
fixed_form_rpg           -[USES]->                    f_spec
fixed_form_rpg           -[USES]->                    d_spec
fixed_form_rpg           -[USES]->                    c_spec
fixed_form_rpg           -[USES]->                    o_spec
fixed_form_rpg           -[CONTAINS]->                rpg_cycle
rpg_cycle                -[USES]->                    indicator
rpg_cycle                -[USES]->                    lr_indicator
lr_indicator             -[TERMINATES]->              rpg_cycle
rpg_cycle                -[PREVENTS]->                rpg_modernization
indicator                -[PREVENTS]->                rpg_modernization
opnqryf                  -[PREVENTS]->                rpg_modernization
rpg                      -[RUNS_ON]->                 ibm_i
ile_rpg                  -[RUNS_ON]->                 ibm_i
ibm_i                    -[EVOLVED_FROM]->            as400
cl_program               -[CALLS]->                   rpg
cl_program               -[EXECUTES]->                cl_command
cl_program               -[MANAGES]->                 libl
cl_command               -[RESOLVES_OBJECTS_VIA]->    libl
libl                     -[SEARCHES]->                library_object
library_object           -[CONTAINS]->                program_object
library_object           -[CONTAINS]->                service_program
library_object           -[CONTAINS]->                physical_file
display_file             -[USES]->                    dds
printer_file             -[USES]->                    dds
physical_file            -[USES]->                    dds
logical_file             -[USES]->                    dds
logical_file             -[VIEWS]->                   physical_file
db2_for_i                -[STORES]->                  physical_file
db2_for_i                -[EXPOSES]->                 logical_file
embedded_sql             -[REPLACES]->                opnqryf
embedded_sql             -[ACCESSES]->                db2_for_i
opnqryf                  -[ACCESSES]->                physical_file
ile                      -[USES]->                    service_program
ile                      -[USES]->                    binding_directory
ile                      -[USES]->                    activation_group
service_program          -[REQUIRES]->                binding_directory
service_program          -[ACTIVATED_IN]->            activation_group
program_object           -[ACTIVATED_IN]->            activation_group
display_file             -[USES]->                    subfile
subfile                  -[LOADED_BY]->               program_object
cl_command               -[ROUTES_JOBS_TO]->          job_queue
job_queue                -[SUBMITS]->                 batch_job_ibmi
batch_job_ibmi           -[CALLS]->                   program_object
batch_job_ibmi           -[USES]->                    data_queue
cl_program               -[APPLIES]->                 override_command
override_command         -[REDIRECTS]->               physical_file
override_command         -[REDIRECTS]->               logical_file
journal                  -[CONTAINS]->                journal_receiver
commitment_control       -[REQUIRES]->                journal
commitment_control       -[SCOPED_TO]->               activation_group
db2_for_i                -[JOURNALED_BY]->            journal
program_object           -[WRITES_TO]->               spool_file_ibmi
printer_file             -[ROUTES_TO]->               spool_file_ibmi
cl_program               -[READS_FROM]->              data_area
cl_program               -[SENDS_TO]->                message_queue
batch_job_ibmi           -[SENDS_TO]->                message_queue
data_queue               -[DECOUPLES]->               batch_job_ibmi
sqlrpgle                 -[COMBINES]->                ile_rpg
sqlrpgle                 -[USES]->                    embedded_sql
sqlrpgle                 -[ACCESSES]->                db2_for_i
rpg_modernization        -[USES]->                    code_for_ibm_i
rpg_modernization        -[USES]->                    lansa
rpg_modernization        -[TARGETS]->                 sqlrpgle
rpg_modernization        -[TARGETS]->                 free_form_rpg
lansa                    -[GENERATES]->               program_object
code_for_ibm_i           -[EDITS]->                   ile_rpg
