## META
name: Fortran Scientific and High-Performance Computing Intelligence
version: 1.0.0
domain: fortran-scientific
description: Fortran language evolution from FORTRAN 77 legacy patterns through modern Fortran 2018, HPC parallelism models, scientific math libraries, compilers, and modernization migration paths.
nodes: 52
edges: 77
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|fortran|Fortran
  |The oldest high-level programming language still in widespread scientific use, originally designed for formula translation on IBM mainframes. Fortran dominates numerical computing and HPC because decades of optimized math libraries, compiler maturity, and array-first syntax produce machine code with near-peak hardware efficiency.]

[CONCEPT|fortran_77|FORTRAN 77
  |The 1977 ANSI standard for Fortran, introducing structured IF-THEN-ELSE constructs but retaining fixed-format source code, COMMON blocks, EQUIVALENCE statements, and implicit typing. FORTRAN 77 codebases remain active in climate, aerospace, and finance because their correctness is trusted after decades of validation.]

[CONCEPT|fortran_90|Fortran 90
  |The 1990 ISO standard that modernized Fortran with free-form source, modules, derived types, allocatable arrays, array syntax, explicit interfaces, and pointer variables. Fortran 90 made FORTRAN 77's dangerous patterns avoidable without requiring a full rewrite, enabling incremental modernization.]

[CONCEPT|fortran_95|Fortran 95
  |A minor 1997 revision to Fortran 90 that added FORALL and PURE/ELEMENTAL procedure attributes, deprecated several FORTRAN 77 features (arithmetic IF, PAUSE), and refined array syntax. Fortran 95 compilers are the minimum standard assumed by most modern scientific libraries.]

[CONCEPT|fortran_2003|Fortran 2003
  |The 2004 ISO standard that introduced full object-oriented programming support — type extension, polymorphism, type-bound procedures, and abstract types — plus IEEE arithmetic exception handling, C interoperability via ISO_C_BINDING, and stream I/O. Fortran 2003 enabled Python-Fortran interoperability through standardized C ABI.]

[CONCEPT|fortran_2008|Fortran 2008
  |The 2010 ISO standard that added coarrays as a native parallel programming model, DO CONCURRENT for data-parallel loops, submodules for separate compilation, and the BLOCK construct for local scoping. Fortran 2008 made intra-language parallelism expressible without external libraries for the first time.]

[CONCEPT|fortran_2018|Fortran 2018
  |The 2018 ISO standard that enhanced coarray parallelism (teams, events, failed images), added further C interoperability improvements, and incorporated select technical features from TS 29113 for assumed-type and assumed-rank dummy arguments. Fortran 2018 narrows the gap between native Fortran parallelism and MPI's explicit message passing.]

[CONCEPT|common_block|COMMON Block
  |A FORTRAN 77 mechanism for sharing global memory across subroutines by physical memory address layout rather than by name. The same memory region can be referenced under different variable names in different subroutines. No modern language has an equivalent construct. Automated refactoring tools cannot safely transform COMMON block usage without full program-wide analysis.]

[CONCEPT|implicit_typing|Implicit Typing
  |A FORTRAN 77 rule that automatically assigns data types to variables based on the first letter of their name — variables starting with I through N are INTEGER, all others are REAL — unless overridden by an explicit type declaration. Implicit typing causes silent type errors and makes static analysis and migration impossible without full execution semantics.]

[CONCEPT|fixed_form_source|Fixed-Form Source
  |The punch-card-derived Fortran source format in which statement type is determined by column position: columns 1-5 for labels, column 6 for continuation, columns 7-72 for code, columns 73-80 ignored. Fixed-form source prevents use of identifiers longer than 6 characters in FORTRAN 77 and requires column-sensitive editors.]

[CONCEPT|format_statement|FORMAT Statement
  |A Fortran I/O control statement that specifies field widths, data types, and layout for formatted READ and WRITE operations using a descriptor language (A, F, I, E, X, /) embedded in parentheses. FORMAT statements are referenced by statement labels and are difficult to read, maintain, or replace with modern I/O libraries.]

[CONCEPT|equivalence_statement|EQUIVALENCE Statement
  |A FORTRAN 77 statement that maps two or more variables to the same memory address, allowing integer and floating-point views of the same bit pattern or array aliasing across different variable names. EQUIVALENCE creates aliasing that defeats compiler optimizations and makes data-flow analysis intractable for refactoring tools.]

[CONCEPT|goto_statement_f|GOTO Statement
  |An unconditional branch to a labeled statement, used in FORTRAN 77 for loop control, error handling, and state machine logic before structured constructs were available. Excessive GOTO creates spaghetti control flow that is difficult to follow, test, or refactor into modern structured equivalents.]

[CONCEPT|computed_goto|Computed GOTO
  |A multi-way branch statement — GOTO (L1, L2, L3), I — that transfers control to the label at position I in the list. The historical precursor to SELECT CASE. Computed GOTO is non-structured and prevents automated control-flow lifting into switch-equivalent constructs during modernization.]

[CONCEPT|arithmetic_if|Arithmetic IF
  |A three-way conditional branch — IF (expr) L1, L2, L3 — that jumps to L1 if expr is negative, L2 if zero, L3 if positive. The arithmetic IF has been deleted from Fortran 2018 and has no equivalent in any modern language. Its presence requires manual conversion to IF-THEN-ELSE or SELECT CASE constructs.]

[CONCEPT|hollerith_constant|Hollerith Constant
  |A character literal syntax from FORTRAN 66 — nHstring — where n is the character count and the string follows immediately. Used for text output before the CHARACTER data type existed. Hollerith constants are deleted from the Fortran standard and are not recognized by modern compilers without legacy compatibility flags.]

[CONCEPT|free_form_source|Free-Form Source
  |The Fortran 90 source format that eliminates column-position significance, allows identifiers up to 31 characters (later 63 in Fortran 2003), supports inline comments with !, and uses & for line continuation. Free-form source enables modern editors, linters, and IDEs to process Fortran without column-aware heuristics.]

[CONCEPT|module_system|Fortran Module System
  |A Fortran 90 construct that provides explicit scoping, encapsulation, and namespace control. Modules replace COMMON blocks as the mechanism for sharing data and procedures across program units, exposing only USE-associated names. Modules enable separate compilation with interface checking, which COMMON blocks cannot provide.]

[CONCEPT|derived_type|Derived Type
  |A Fortran 90 user-defined composite data structure analogous to a C struct or a class without methods. Derived types allow grouping of related variables under a named type, enabling structured data to be passed between subprograms as a single argument. Fortran 2003 extended derived types with type-bound procedures for full OOP.]

[CONCEPT|allocatable_array|Allocatable Array
  |A Fortran 90 array whose size is determined and memory allocated at runtime using the ALLOCATE statement, and freed with DEALLOCATE. Allocatable arrays replace fixed-size arrays and COMMON block size assumptions, enabling dynamic data structures without manual pointer arithmetic.]

[CONCEPT|pointer_f|Fortran Pointer
  |A Fortran 90 variable that holds the address of a target variable declared with the TARGET attribute, enabling dynamic data structures, aliasing, and deferred allocation. Fortran pointers are more restricted than C pointers — they can only point to Fortran objects with compatible type and rank — providing safety while enabling dynamic programming.]

[CONCEPT|interface_block|Interface Block
  |An explicit Fortran 90 declaration of a procedure's argument types, kinds, and intents, placed in a calling scope or module. Interface blocks enable compile-time type checking of procedure calls, catch argument mismatches that implicit interfaces silently ignore, and are required for optional, keyword, and assumed-shape array arguments.]

[CONCEPT|pure_function|PURE Procedure
  |A Fortran 95 procedure declared with the PURE attribute, guaranteeing no side effects — no I/O, no SAVE variables, no modifications to global state. The PURE attribute enables the compiler to perform aggressive optimization including loop parallelization, vectorization, and safe reordering of calls.]

[CONCEPT|elemental_function|ELEMENTAL Procedure
  |A Fortran 95 PURE procedure that operates on scalar arguments but can be applied element-wise to arrays of any rank and shape by the runtime, producing an output array of the same shape. ELEMENTAL procedures enable data-parallel programming without explicit loops and are a building block for array-level scientific computation.]

[CONCEPT|assumed_shape_array|Assumed-Shape Array
  |A Fortran 90 dummy argument declaration — REAL :: A(:,:) — that receives the shape of the actual array argument from the caller via an array descriptor rather than requiring the caller to pass explicit dimension sizes. Assumed-shape arrays eliminate the size-mismatch bugs common in FORTRAN 77 array passing and require explicit interface blocks.]

[CONCEPT|do_concurrent|DO CONCURRENT
  |A Fortran 2008 loop construct that asserts all iterations are independent, allowing compilers and runtimes to execute them in parallel using SIMD, threads, or GPU offload. DO CONCURRENT provides a language-standard path to data parallelism without requiring OpenMP pragmas or manual vectorization.]

[CONCEPT|object_oriented_fortran|Object-Oriented Fortran
  |The set of Fortran 2003 features — type extension (inheritance), polymorphism, deferred bindings (virtual methods), and CLASS dummy arguments — that enable object-oriented design patterns in Fortran. OOP Fortran allows legacy scientific codes to adopt abstraction layers without migrating to C++ or Python.]

[CONCEPT|namelists|Fortran NAMELIST
  |A Fortran I/O feature that reads and writes named groups of variables using a keyword=value text format, supporting selective parameter override without recompiling. NAMELIST is widely used in climate models and simulation codes for runtime configuration. NAMELIST I/O syntax is non-standard and not supported in Python or C without custom parsers.]

[CONCEPT|mpi|MPI (Message Passing Interface)
  |The de facto standard library specification for distributed-memory parallel programming, enabling processes on separate compute nodes to exchange data through explicit send, receive, broadcast, and collective operations. MPI is the primary parallelism mechanism in large-scale HPC scientific applications.]

[CONCEPT|openmp|OpenMP
  |A shared-memory parallel programming API based on compiler directives (!$OMP PARALLEL DO), runtime library routines, and environment variables. OpenMP enables thread-level parallelism on multi-core CPUs with minimal code changes to sequential Fortran loops and is widely used in finite element and CFD codes.]

[CONCEPT|coarray|Coarray Fortran
  |Native Fortran 2008 parallel programming syntax where each image (parallel process) has its own local data, and remote data is accessed using bracket notation — A[k] refers to variable A on image k. Coarrays are the only parallel mechanism built into the Fortran standard, enabling parallelism without MPI.]

[CONCEPT|cuda_fortran|CUDA Fortran
  |An extension of Fortran provided by NVIDIA's nvfortran compiler that adds GPU kernel launch syntax, device data management attributes (DEVICE, MANAGED), and GPU-specific intrinsics. CUDA Fortran enables GPU acceleration of scientific Fortran code while preserving the Fortran programming model.]

[CONCEPT|openacc|OpenACC
  |A directive-based GPU and accelerator offloading API for Fortran and C, similar in style to OpenMP. Developers annotate compute loops with !$ACC PARALLEL DO directives; the compiler generates GPU kernel code. OpenACC is portable across NVIDIA, AMD, and multicore CPUs and is widely used in climate and weather models.]

[CONCEPT|blas|BLAS (Basic Linear Algebra Subprograms)
  |A specification and reference implementation of fundamental dense linear algebra operations: level 1 (vector-vector), level 2 (matrix-vector), and level 3 (matrix-matrix). BLAS is the universal performance substrate; all vendor-optimized libraries (MKL, OpenBLAS, cuBLAS) implement the BLAS interface for Fortran and C callers.]

[CONCEPT|lapack|LAPACK (Linear Algebra PACKage)
  |A Fortran library for solving systems of linear equations, eigenvalue problems, and singular value decompositions, built on BLAS level 3 operations. LAPACK is the reference implementation for numerical linear algebra in scientific computing and is wrapped by NumPy, SciPy, MATLAB, and Julia.]

[CONCEPT|scalapack|ScaLAPACK
  |A distributed-memory parallel version of LAPACK that uses MPI for inter-process communication and PBLAS (parallel BLAS) for distributed matrix operations. ScaLAPACK enables eigenvalue and linear solve computations that exceed single-node memory capacity in large-scale scientific simulations.]

[CONCEPT|fftw|FFTW (Fastest Fourier Transform in the West)
  |A self-optimizing Fortran/C library for computing discrete Fourier transforms of arbitrary size and dimension. FFTW plans the optimal transform algorithm at runtime based on problem size and hardware. It is the standard FFT library in CFD, signal processing, and climate modeling codes.]

[CONCEPT|netcdf|NetCDF (Network Common Data Form)
  |A machine-independent data format and library for storing array-oriented scientific data such as gridded climate variables, atmospheric fields, and ocean temperatures. NetCDF's self-describing format with named dimensions, variables, and attributes is the standard data exchange format in atmospheric and ocean science.]

[CONCEPT|hdf5|HDF5 (Hierarchical Data Format 5)
  |A portable binary data format and library for storing large, complex, hierarchical scientific datasets. HDF5 supports parallel I/O via MPI, chunked storage, compression, and arbitrary metadata. Widely used in quantum chemistry, particle physics, and materials science for simulation checkpoint and analysis files.]

[CONCEPT|gfortran|GFortran
  |The GNU Compiler Collection's open-source Fortran compiler, supporting Fortran 77 through Fortran 2018 with good standard conformance. GFortran is the default Fortran compiler on Linux and macOS and is widely used for open-source scientific software development and benchmark testing.]

[CONCEPT|ifort|Intel Fortran Compiler (ifort / ifx)
  |Intel's proprietary Fortran compiler, historically known for generating the highest-performing code on Intel x86 processors through auto-vectorization, OpenMP support, and aggressive interprocedural optimization. ifort is the production compiler of choice for weather forecasting and large-scale HPC applications on Intel clusters.]

[CONCEPT|flang|Flang
  |An open-source Fortran front end for the LLVM compiler infrastructure, developed by AMD and the broader LLVM community. Flang aims to provide a fully standard-conforming, community-maintained alternative to ifort on AMD and ARM hardware, and serves as the compiler backend for NVIDIA's nvfortran on CPU.]

[CONCEPT|nvfortran|NVIDIA Fortran Compiler (nvfortran)
  |NVIDIA's Fortran compiler (formerly PGI Fortran) that supports CUDA Fortran extensions, OpenACC GPU directives, and standard Fortran 2003/2008 for GPU-accelerated scientific computing on NVIDIA hardware. nvfortran is the primary path for porting Fortran HPC codes to GPU clusters.]

[CONCEPT|cfd_simulation|CFD Simulation
  |Computational fluid dynamics — the numerical simulation of fluid flow, heat transfer, and turbulence using finite difference, finite volume, or finite element methods on structured or unstructured grids. CFD codes such as OpenFOAM (C++) and legacy NASA codes (Fortran) represent some of the largest and most computationally demanding scientific applications.]

[CONCEPT|climate_model|Climate Model
  |A numerical model that simulates Earth's atmosphere, ocean, land surface, and sea ice using systems of partial differential equations discretized on global grids. Climate models (CESM, WRF, NEMO) are predominantly written in Fortran and require petascale parallel computing, driving adoption of MPI, OpenMP, and NetCDF.]

[CONCEPT|quantum_chemistry|Quantum Chemistry Code
  |Scientific software for computing molecular electronic structure using methods such as Hartree-Fock, DFT, MP2, and CCSD(T). Codes such as Gaussian, ORCA, and NWChem are heavily Fortran-based, relying on BLAS/LAPACK for matrix operations and HDF5 for checkpoint storage of multi-terabyte integral files.]

[CONCEPT|finite_element|Finite Element Analysis
  |A numerical method for solving structural mechanics, heat transfer, and electromagnetics problems by discretizing a domain into elements and assembling a global stiffness matrix. Legacy FEA codes (ABAQUS solvers, OpenSees) use Fortran for their computational kernels, relying on LAPACK for sparse system solution.]

[CONCEPT|quant_finance_fortran|Quantitative Finance Fortran
  |Legacy Fortran codebases in investment banks and risk systems that implement Monte Carlo simulation, bond pricing, and options valuation. These codes persist because their numerical precision and performance have been validated over decades. BLAS-optimized matrix operations underpin portfolio risk factor computations.]

[CONCEPT|fortran_modernization|Fortran Modernization
  |The process of refactoring legacy FORTRAN 77 codebases to use modern Fortran 90+ features — replacing COMMON blocks with modules, implicit typing with IMPLICIT NONE, fixed-form with free-form source, and GOTOs with structured control flow. Full modernization is often blocked by COMMON blocks and EQUIVALENCE statements that require whole-program analysis.]

[CONCEPT|f2py|f2py (Fortran to Python Interface Generator)
  |A NumPy tool that automatically generates Python extension modules from Fortran source files, allowing Fortran subroutines and functions to be called directly from Python with NumPy array passing. f2py is the primary path for embedding validated Fortran numerical kernels inside Python data science workflows.]

[CONCEPT|iso_c_binding|ISO_C_BINDING Module
  |A Fortran 2003 intrinsic module that provides standard C-interoperable data types (C_INT, C_DOUBLE, C_PTR) and the BIND(C) attribute for procedures, enabling Fortran code to call C functions and be called from C without compiler-specific workarounds. ISO_C_BINDING is the foundation for all modern Fortran-Python interoperability via C ABI.]

[CONCEPT|python_interface|Python-Fortran Interface
  |The interoperability layer allowing Python code to call validated Fortran numerical kernels, typically via f2py-generated extension modules or Cython/ctypes wrappers using ISO_C_BINDING. Enables gradual migration: keep performance-critical Fortran inner loops while building Python-based data pipelines, plotting, and orchestration around them.]

---

## EDGES

fortran                       -[EVOLVED_INTO]->           fortran_77
fortran_77                    -[EVOLVED_INTO]->           fortran_90
fortran_90                    -[EVOLVED_INTO]->           fortran_95
fortran_95                    -[EVOLVED_INTO]->           fortran_2003
fortran_2003                  -[EVOLVED_INTO]->           fortran_2008
fortran_2008                  -[EVOLVED_INTO]->           fortran_2018

fortran_77                    -[USES]->                   common_block
fortran_77                    -[USES]->                   implicit_typing
fortran_77                    -[USES]->                   fixed_form_source
fortran_77                    -[USES]->                   goto_statement_f
fortran_77                    -[USES]->                   arithmetic_if
fortran_77                    -[USES]->                   equivalence_statement
fortran_77                    -[USES]->                   format_statement
fortran_77                    -[USES]->                   hollerith_constant

common_block                  -[PREVENTS]->               fortran_modernization
implicit_typing               -[PREVENTS]->               fortran_modernization
equivalence_statement         -[PREVENTS]->               fortran_modernization
computed_goto                 -[PREVENTS]->               fortran_modernization
arithmetic_if                 -[PREVENTS]->               fortran_modernization
hollerith_constant            -[PREVENTS]->               fortran_modernization

goto_statement_f              -[INSTANCE_OF]->            computed_goto

equivalence_statement         -[USES]->                   common_block

fixed_form_source             -[USES]->                   format_statement

fortran_90                    -[INTRODUCES]->             module_system
fortran_90                    -[INTRODUCES]->             free_form_source
fortran_90                    -[INTRODUCES]->             allocatable_array
fortran_90                    -[INTRODUCES]->             derived_type
fortran_90                    -[INTRODUCES]->             pointer_f
fortran_90                    -[INTRODUCES]->             interface_block
fortran_90                    -[INTRODUCES]->             assumed_shape_array

fortran_95                    -[INTRODUCES]->             pure_function
fortran_95                    -[INTRODUCES]->             elemental_function

fortran_2003                  -[INTRODUCES]->             object_oriented_fortran
fortran_2003                  -[INTRODUCES]->             iso_c_binding

fortran_2008                  -[INTRODUCES]->             coarray
fortran_2008                  -[INTRODUCES]->             do_concurrent

module_system                 -[REPLACES]->               common_block

interface_block               -[ENABLES]->                pure_function
interface_block               -[ENABLES]->                elemental_function
interface_block               -[ENABLES]->                assumed_shape_array

derived_type                  -[ENABLES]->                object_oriented_fortran

iso_c_binding                 -[ENABLES]->                python_interface

python_interface              -[USES]->                   f2py

f2py                          -[WRAPS]->                  fortran

fortran_modernization         -[USES]->                   iso_c_binding
fortran_modernization         -[USES]->                   module_system

coarray                       -[REQUIRES]->               fortran_2008

cuda_fortran                  -[EXTENDS]->                fortran
openacc                       -[EXTENDS]->                fortran

mpi                           -[ENABLES]->                cfd_simulation
mpi                           -[ENABLES]->                climate_model
mpi                           -[ENABLES]->                quantum_chemistry
mpi                           -[ENABLES]->                finite_element

openmp                        -[ENABLES]->                cfd_simulation
openmp                        -[ENABLES]->                finite_element

cuda_fortran                  -[ENABLES]->                quantum_chemistry
openacc                       -[ENABLES]->                climate_model
openacc                       -[ENABLES]->                cfd_simulation

do_concurrent                 -[ENABLES]->                cfd_simulation

blas                          -[USED_BY]->                lapack
lapack                        -[USED_BY]->                scalapack
scalapack                     -[USES]->                   mpi

blas                          -[ENABLES]->                quant_finance_fortran
lapack                        -[ENABLES]->                quantum_chemistry
lapack                        -[ENABLES]->                finite_element

fftw                          -[ENABLES]->                cfd_simulation
fftw                          -[ENABLES]->                climate_model

netcdf                        -[USED_IN]->                climate_model
hdf5                          -[USED_IN]->                quantum_chemistry
hdf5                          -[USED_IN]->                cfd_simulation

namelists                     -[USED_IN]->                climate_model
namelists                     -[PREVENTS]->               fortran_modernization

gfortran                      -[COMPILES]->               fortran
ifort                         -[COMPILES]->               fortran
flang                         -[COMPILES]->               fortran
nvfortran                     -[COMPILES]->               fortran

nvfortran                     -[ENABLES]->                cuda_fortran
