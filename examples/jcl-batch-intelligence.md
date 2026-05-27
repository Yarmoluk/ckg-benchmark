## META
name: JCL and IBM Mainframe Batch Processing
version: 1.0.0
domain: jcl-batch-intelligence
description: Compact knowledge graph of IBM JCL syntax, JES subsystems, dataset management, utilities, security, execution control, and batch modernization concepts for mainframe environments.
nodes: 53
edges: 71
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|jcl|Job Control Language
  |IBM mainframe scripting language used to define batch job steps, resource allocations, and execution parameters for z/OS workloads.]

[CONCEPT|job_statement|JOB Statement
  |The first statement in every JCL job that identifies the job to JES, specifying accounting, class, priority, and notification parameters.]

[CONCEPT|exec_statement|EXEC Statement
  |JCL statement that invokes a program or cataloged procedure as a job step, optionally passing parameters and overriding symbolic values.]

[CONCEPT|dd_statement|DD Statement
  |Data Definition statement that describes a dataset or I/O resource used by a job step, including allocation, disposition, and space parameters.]

[CONCEPT|proc_statement|PROC Statement
  |JCL statement that marks the start of an inline or cataloged procedure and optionally declares symbolic parameter defaults.]

[CONCEPT|cataloged_proc|Cataloged Procedure
  |A reusable set of JCL statements stored in a procedure library that can be invoked by name from any job, reducing redundancy and standardizing step sequences.]

[CONCEPT|jcllib|JCLLIB Statement
  |JCL statement that specifies libraries to search for cataloged procedures before the system procedure libraries are checked.]

[CONCEPT|steplib|STEPLIB DD
  |A DD statement within a job step that directs the system to search specified load libraries for programs before the system link list.]

[CONCEPT|symbolic_parameter|Symbolic Parameter
  |A variable placeholder defined in a procedure using the &NAME convention that gets substituted with actual values when the procedure is invoked.]

[CONCEPT|instream_data|Instream Data
  |Data embedded directly within the JCL job stream following a DD * or DD DATA statement, used to supply program input without a separate dataset.]

[CONCEPT|sysin|SYSIN DD
  |A DD statement conventionally named SYSIN that provides control statements or input data to a utility or program from the job stream or a dataset.]

[CONCEPT|sysout|SYSOUT DD
  |A DD statement that directs program output to the JES spool for printing or online viewing, specifying an output class.]

[CONCEPT|sysprint|SYSPRINT DD
  |A DD statement conventionally named SYSPRINT used by IBM utilities to write diagnostic messages, reports, and summary output to the spool.]

[CONCEPT|jcl_comment|JCL Comment Statement
  |A non-executing JCL statement beginning with //* used to document job logic, step purpose, or maintenance history within the job stream.]

[CONCEPT|jcl_override|JCL Override
  |A technique for modifying DD statements or symbolic parameters within a cataloged procedure invocation to customize behavior for a specific job run.]

[CONCEPT|job_class|Job Class
  |A single-character attribute on the JOB statement that routes the job to an initiator configured to run jobs of that class, controlling resource consumption.]

[CONCEPT|message_class|Message Class
  |An attribute on the JOB statement that controls where JES routes system messages and job log output for printing or spool retention.]

[CONCEPT|output_class|Output Class
  |A spool routing class assigned to SYSOUT datasets that determines which printer or output device processes the spooled output.]

[CONCEPT|initiator|Initiator
  |A z/OS address space managed by JES that selects jobs from the input queue based on job class and executes them, controlling parallelism.]

[CONCEPT|jes2|JES2
  |IBM Job Entry Subsystem 2, the most common JES implementation, managing job input, scheduling, spool, and output in a single-system or Sysplex environment.]

[CONCEPT|jes3|JES3
  |IBM Job Entry Subsystem 3, an alternative to JES2 providing centralized job scheduling and setup across multiple processors in a complex.]

[CONCEPT|spool|JES Spool
  |Disk space managed by JES that temporarily stores JCL, job logs, and SYSOUT datasets from job submission through output processing.]

[CONCEPT|gdg|Generation Data Group
  |IBM mainframe file versioning construct that maintains a chronological series of dataset generations accessed via relative notation (+1, 0, -1). Has no equivalent in modern systems and is a primary modernization blocker.]

[CONCEPT|gdg_base|GDG Base
  |A catalog entry that defines a Generation Data Group, specifying the maximum number of generations to retain, scratch behavior, and NOEMPTY/EMPTY policy.]

[CONCEPT|gdg_generation|GDG Generation
  |An individual versioned dataset within a GDG, identified by a relative generation number at runtime and an absolute generation and version (GnnnnVnn) in the catalog.]

[CONCEPT|vsam_cluster|VSAM Cluster
  |A Virtual Storage Access Method dataset organization combining data and index components, used for keyed, sequential, or relative-record access in mainframe batch and online applications.]

[CONCEPT|sms|Storage Management Subsystem
  |IBM z/OS facility that automates dataset placement, migration, backup, and deletion by matching datasets to storage classes, data classes, and management classes.]

[CONCEPT|sms_storage_class|SMS Storage Class
  |An SMS construct that specifies performance and availability requirements for a dataset, directing the system to appropriate storage hardware.]

[CONCEPT|sms_data_class|SMS Data Class
  |An SMS construct that supplies default dataset attributes such as record format, block size, and space, reducing the need to code them explicitly in JCL.]

[CONCEPT|sms_management_class|SMS Management Class
  |An SMS construct that defines retention, migration, and backup policies for a dataset, controlling its lifecycle from creation to expiration.]

[CONCEPT|disposition|DISP Parameter
  |A DD statement parameter with three sub-parameters specifying the dataset's initial status, normal-end action, and abnormal-end action.]

[CONCEPT|allocation|Space Allocation
  |JCL parameters on a DD statement that reserve primary and secondary disk space in tracks, cylinders, or blocks for a new dataset.]

[CONCEPT|tape_unit|Tape Unit
  |A hardware device or esoteric unit name referenced in JCL to direct dataset I/O to magnetic tape, still used in mainframe archival and large sequential workloads.]

[CONCEPT|dataset_catalog|Dataset Catalog
  |An IBM mainframe index structure (ICF catalog) that maps dataset names to their volume and DASD location, required for dataset retrieval without explicit volume specification.]

[CONCEPT|idcams|IDCAMS Utility
  |IBM Access Method Services utility used to define, delete, copy, list, and alter VSAM clusters, GDG bases, and catalog entries.]

[CONCEPT|dfsort|DFSORT Utility
  |IBM high-performance sort, merge, and copy utility that processes sequential and VSAM datasets with powerful statement-driven transformation capabilities.]

[CONCEPT|icetool|ICETOOL
  |An extended control interface for DFSORT that provides high-level operators for counting, selecting, statistics, and multi-operation dataset processing without custom program code.]

[CONCEPT|racf|RACF
  |IBM Resource Access Control Facility, the primary security manager on z/OS that authenticates users and controls access to datasets, programs, and system resources via profiles.]

[CONCEPT|racf_dataset_profile|RACF Dataset Profile
  |A RACF security definition that governs read, update, alter, and control access to one or more datasets matched by a generic or discrete profile name.]

[CONCEPT|return_code|Return Code
  |A numeric value (typically 0, 4, 8, or higher) set by a program or utility at step completion that communicates success, warning, or error status to JCL condition processing.]

[CONCEPT|cond_parameter|COND Parameter
  |A JCL parameter on the EXEC or JOB statement that conditionally bypasses job steps based on return codes from prior steps, implementing rudimentary flow control.]

[CONCEPT|restart_step|Restart Step
  |The step name specified on the JOB statement RESTART parameter that directs JES to resume a failed job from a specific step rather than from the beginning.]

[CONCEPT|abend|Abnormal End
  |An unplanned termination of a job step caused by a program exception, system error, or resource failure, producing an abend code and optional dump.]

[CONCEPT|abend_code|Abend Code
  |A system (Sxxx) or user (Uxxx) code produced when a step abends that identifies the failure type and guides diagnosis and recovery.]

[CONCEPT|checkpoint_restart|Checkpoint Restart
  |A facility that saves job progress at defined intervals so that a failed batch job can be restarted from the last checkpoint rather than from step or job beginning.]

[CONCEPT|wto_message|WTO Message
  |A Write To Operator message issued by a batch job or system component to the z/OS console, used for status notification and operator intervention requests.]

[CONCEPT|notify_statement|NOTIFY Parameter
  |A JOB statement parameter that sends a TSO message to a specified user ID when the job completes, providing job-end notification without console monitoring.]

[CONCEPT|batch_window|Batch Window
  |The scheduled time period, typically overnight, during which batch jobs must complete before online systems resume, creating a hard deadline constraint for job stream design.]

[CONCEPT|job_stream|Job Stream
  |An ordered sequence of interdependent JCL jobs submitted to run as a logical unit of work, often managed by an external workload scheduler.]

[CONCEPT|job_dependency_net|Job Dependency Network
  |A directed graph of job predecessor and successor relationships maintained by a workload scheduler that ensures jobs execute in the correct order and trigger downstream work on completion.]

[CONCEPT|ca_7|CA 7 Workload Automation
  |Broadcom CA 7 (formerly Computer Associates) enterprise mainframe workload scheduler that manages job scheduling, dependency resolution, and SLA tracking.]

[CONCEPT|twc|Tivoli Workload Scheduler
  |IBM Tivoli Workload Composer/Scheduler, an enterprise job scheduling platform managing mainframe and distributed batch workloads with cross-platform dependency tracking.]

[CONCEPT|batch_modernization|Batch Modernization
  |The process of migrating mainframe JCL batch workloads to modern platforms such as cloud-native containers, Apache Spark, or microservices, requiring resolution of GDG, VSAM, and JES-specific constructs.]

---

## EDGES

jcl                      -[CONSISTS_OF]->             job_statement
jcl                      -[CONSISTS_OF]->             exec_statement
jcl                      -[CONSISTS_OF]->             dd_statement
jcl                      -[CONSISTS_OF]->             proc_statement
jcl                      -[CONSISTS_OF]->             jcl_comment
jcl                      -[SUBMITTED_TO]->            jes2
jcl                      -[SUBMITTED_TO]->            jes3
job_statement            -[SPECIFIES]->               job_class
job_statement            -[SPECIFIES]->               message_class
job_statement            -[CONTAINS]->                notify_statement
exec_statement           -[INVOKES]->                 cataloged_proc
exec_statement           -[REFERENCES]->              steplib
exec_statement           -[USES]->                    cond_parameter
exec_statement           -[USES]->                    symbolic_parameter
dd_statement             -[SPECIFIES]->               disposition
dd_statement             -[SPECIFIES]->               allocation
dd_statement             -[REFERENCES]->              tape_unit
dd_statement             -[ROUTES_OUTPUT_TO]->        sysout
dd_statement             -[PROVIDES_INPUT_VIA]->      sysin
dd_statement             -[WRITES_MESSAGES_TO]->      sysprint
sysout                   -[ROUTES_TO]->               output_class
output_class             -[MANAGED_BY]->              jes2
initiator                -[SELECTS_BY]->              job_class
initiator                -[MANAGED_BY]->              jes2
cataloged_proc           -[STORED_IN]->               jcllib
cataloged_proc           -[DECLARES]->                symbolic_parameter
cataloged_proc           -[ACCEPTS]->                 jcl_override
jcllib                   -[SEARCHED_BEFORE]->         steplib
instream_data            -[SUPPLIED_VIA]->            sysin
proc_statement           -[DEFINES]->                 cataloged_proc
gdg                      -[CONSISTS_OF]->             gdg_base
gdg                      -[CONSISTS_OF]->             gdg_generation
gdg_generation           -[REQUIRES]->                gdg_base
gdg_base                 -[REGISTERED_IN]->           dataset_catalog
gdg_generation           -[REGISTERED_IN]->           dataset_catalog
gdg                      -[BLOCKS]->                  batch_modernization
vsam_cluster             -[REGISTERED_IN]->           dataset_catalog
idcams                   -[MANAGES]->                 vsam_cluster
idcams                   -[MANAGES]->                 gdg_base
idcams                   -[READS_CONTROL_FROM]->      sysin
idcams                   -[WRITES_REPORT_TO]->        sysprint
racf                     -[PROTECTS]->                vsam_cluster
racf                     -[PROTECTS]->                gdg_base
racf                     -[USES]->                    racf_dataset_profile
racf_dataset_profile     -[GOVERNS_ACCESS_TO]->       dataset_catalog
sms                      -[MANAGES]->                 sms_storage_class
sms                      -[MANAGES]->                 sms_data_class
sms                      -[MANAGES]->                 sms_management_class
sms_storage_class        -[APPLIED_TO]->              vsam_cluster
sms_data_class           -[SUPPLIES_DEFAULTS_FOR]->   dd_statement
sms_management_class     -[CONTROLS_LIFECYCLE_OF]->   gdg_generation
dfsort                   -[USES]->                    icetool
dfsort                   -[READS_CONTROL_FROM]->      sysin
dfsort                   -[WRITES_REPORT_TO]->        sysprint
return_code              -[TRIGGERS]->                cond_parameter
cond_parameter           -[CONTROLS]->                exec_statement
abend                    -[PRODUCES]->                abend_code
abend                    -[GENERATES]->               wto_message
checkpoint_restart       -[RECOVERS_FROM]->           abend
checkpoint_restart       -[RESUMES_AT]->              restart_step
jes2                     -[MANAGES]->                 spool
jes3                     -[MANAGES]->                 spool
jes2                     -[ROUTES_TO]->               initiator
spool                    -[STORES]->                  sysout
ca_7                     -[ORCHESTRATES]->            job_dependency_net
twc                      -[ORCHESTRATES]->            job_dependency_net
job_dependency_net       -[SEQUENCES]->               job_stream
job_stream               -[MUST_COMPLETE_IN]->        batch_window
batch_modernization      -[REPLACES]->                job_stream
batch_modernization      -[RESOLVES]->                gdg
batch_modernization      -[RESOLVES]->                vsam_cluster
