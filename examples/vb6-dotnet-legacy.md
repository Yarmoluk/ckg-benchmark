## META
name: VB6, Classic ASP, and Early .NET Legacy Intelligence
version: 1.0.0
domain: vb6-dotnet-legacy
description: Schema and methodology for navigating Visual Basic 6, Classic ASP, and early .NET legacy codebases — COM/ActiveX architecture, error suppression patterns, framework evolution chains, and migration blockers.
nodes: 50
edges: 91
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|vb6|Visual Basic 6
  |Microsoft's COM-based rapid application development language, dominant in Windows business software from 1998–2005. VB6 applications compile to COM ActiveX DLLs and EXEs. The runtime was officially retired in 2008 but remains in production at thousands of enterprises.]

[CONCEPT|on_error_resume_next|On Error Resume Next
  |VB6 error suppression statement that causes execution to continue on the next line after any runtime error. The application proceeds in a corrupt or undefined state with no indication of failure. The single most dangerous legacy pattern in VB6 and Classic ASP codebases — errors are silently swallowed and no tool can determine where they occurred.]

[CONCEPT|on_error_goto|On Error GoTo
  |VB6 structured error handling that transfers control to a labeled error handler on exception. The safer alternative to On Error Resume Next. Its presence signals intentional error handling; its absence in critical paths signals suppressed errors.]

[CONCEPT|err_object|Err Object
  |VB6 global error state object exposing Number, Description, and Source after a runtime error. On Error Resume Next corrupts the Err object by overwriting it at each statement — making post-hoc error diagnosis impossible in suppression-heavy code.]

[CONCEPT|com_object|COM Object
  |Component Object Model binary component exposing interfaces via IUnknown. The fundamental interoperability unit on Windows. VB6, Classic ASP, and early .NET all interact with COM objects — making COM the hidden dependency layer across all three eras.]

[CONCEPT|com_automation|COM Automation
  |COM dispatch interface (IDispatch) enabling late-bound scripting access to COM objects from VBScript, Classic ASP, and Office macros. Late binding means method names and argument types are resolved at runtime — static analysis cannot determine what is called or what parameters are expected.]

[CONCEPT|activex_dll|ActiveX DLL
  |In-process COM server compiled from VB6 or C++. Loaded into the calling process's address space. ActiveX DLLs are the primary packaging unit for VB6 business logic and must be registered in the Windows registry before use.]

[CONCEPT|activex_exe|ActiveX EXE
  |Out-of-process COM server that runs in its own process. Supports DCOM for cross-machine communication. ActiveX EXEs introduce process isolation but add marshaling overhead and registration complexity compared to ActiveX DLLs.]

[CONCEPT|dcom|DCOM (Distributed COM)
  |Microsoft extension to COM enabling COM object activation and method calls across network boundaries. DCOM configuration lives in the Windows registry and requires matching settings on both client and server machines — a common source of silent breakage during infrastructure changes.]

[CONCEPT|adodb|ADO DB (ActiveX Data Objects)
  |COM-based data access library providing Connection, Recordset, and Command objects for database interaction from VB6, Classic ASP, and early VBScript. ADODB is the universal database layer across all three eras — replaced by ADO.NET in .NET migration.]

[CONCEPT|dao|DAO (Data Access Objects)
  |Earlier Microsoft data access COM library, primarily for Jet/Access databases. Superseded by ADODB for server-side scenarios. DAO presence indicates Jet/Access data stores or very old VB4/VB5-era code that was never fully migrated to ADODB.]

[CONCEPT|regsvr32|regsvr32.exe
  |Windows utility that registers or unregisters COM DLLs and OCX controls by writing entries into the Windows registry. ActiveX DLLs do not function without regsvr32 registration — deployment is manual and machine-specific, making automated deployment pipelines impossible without wrappers.]

[CONCEPT|vb6_runtime|VB6 Runtime (MSVBVM60.DLL)
  |Microsoft Visual Basic 6 virtual machine DLL required to execute any VB6-compiled binary. Officially unsupported since 2008 but redistributed by Microsoft for compatibility. Its presence on a production server is a compliance risk indicator in regulated industries.]

[CONCEPT|type_library|COM Type Library (.tlb)
  |Binary metadata file describing a COM object's interfaces, methods, and properties. Consumed by early binding clients (VB6, C++) to enable IntelliSense and compile-time type checking. Missing or mismatched type libraries cause late-binding fallback — the source of runtime-only errors.]

[CONCEPT|vbscript|VBScript
  |Microsoft's scripting dialect of Visual Basic, interpreted at runtime with no compilation step. Used in Classic ASP pages, WSH scripts, and HTA applications. VBScript inherits VB6's On Error Resume Next semantics and COM Automation model.]

[CONCEPT|classic_asp|Classic ASP (Active Server Pages)
  |Microsoft's server-side scripting technology (1996–2002) that executes VBScript or JScript within IIS to generate HTML. Classic ASP pages mix HTML markup with inline server logic — making them resistant to refactoring, testing, and migration. Replaced by ASP.NET but persists in unmaintained intranets and portals.]

[CONCEPT|asp_response_write|Response.Write
  |Classic ASP method that emits HTML directly into the HTTP response buffer from inline VBScript. Widespread Response.Write usage indicates HTML and business logic are fully intermixed — a strong predictor of high migration cost.]

[CONCEPT|session_object|ASP Session Object
  |Classic ASP in-process session state object storing per-user data in server memory. Server-affinity requirement (sticky sessions) prevents load balancing and horizontal scaling. Session-heavy Classic ASP is architecturally incompatible with modern cloud deployment.]

[CONCEPT|global_asa|Global.asa
  |Classic ASP application lifecycle file defining Application_OnStart, Session_OnStart, Session_OnEnd, and Application_OnEnd event handlers. A single file for the entire application — a shared mutable state entry point with no encapsulation.]

[CONCEPT|iis5|IIS 5 / IIS 6
  |Microsoft Internet Information Services versions 5 and 6, the native hosting platform for Classic ASP. IIS 5/6 runs only on Windows Server 2000/2003. Dependency on IIS 5/6 is an indicator of an unmigrated Classic ASP deployment.]

[CONCEPT|ole_db|OLE DB
  |Microsoft's COM-based low-level data access API, underlying ADODB. OLE DB providers expose database-specific drivers through a COM interface. OLE DB provider availability determines which databases a VB6/Classic ASP application can reach.]

[CONCEPT|sql_server_2000|SQL Server 2000
  |Microsoft SQL Server version released in 2000, end-of-life in 2013. Commonly paired with VB6 and Classic ASP. SQL Server 2000 features (DTS packages, linked servers, text/ntext columns) create migration blockers when upgrading to modern SQL Server.]

[CONCEPT|stored_procedure|Stored Procedure
  |SQL Server procedure executed server-side containing business logic mixed with data access. VB6 and Classic ASP applications frequently offload validation, calculations, and workflow to stored procedures — making business rule extraction require both code and database analysis.]

[CONCEPT|vbnet|VB.NET
  |Visual Basic language redesigned for the .NET Framework — syntactically similar to VB6 but semantically a different language with garbage collection, strong typing, and the full .NET BCL. Not a direct upgrade path from VB6: COM assumptions, late binding, and error handling semantics differ significantly.]

[CONCEPT|winforms|Windows Forms
  |.NET Framework UI framework for desktop applications, introduced in .NET 1.0. The migration target for VB6 forms. WinForms replicates the event-driven, form-centric programming model of VB6 — making it the lowest-friction .NET migration path for desktop VB6 applications.]

[CONCEPT|net_framework_11|.NET Framework 1.0 / 1.1
  |First versions of Microsoft's managed runtime platform. Introduced Windows Forms, ASP.NET Web Forms, and ADO.NET. VB.NET 2002/2003 targets these versions. Applications on .NET 1.x cannot run on .NET Core or .NET 5+ without code changes.]

[CONCEPT|net_framework_4x|.NET Framework 4.x
  |Mature Windows-only .NET runtime (4.0–4.8). Added async/await, LINQ, WPF, WCF, and Entity Framework. The last generation of Windows-only .NET. Applications targeting 4.x can use COM interop and P/Invoke but cannot be ported to Linux or macOS.]

[CONCEPT|dotnet_core|.NET Core / .NET 5+
  |Cross-platform, open-source reimplementation of .NET. Drops COM interop, WCF server-side, Windows Forms on non-Windows, and other Windows-specific APIs. Migration from .NET Framework 4.x to .NET Core is a breaking change requiring explicit compatibility assessment.]

[CONCEPT|wpf|Windows Presentation Foundation (WPF)
  |.NET Framework vector-graphics UI framework using XAML markup. The modernization target for WinForms applications requiring rich UI. WPF introduced the MVVM pattern — a clean separation of UI and business logic that WinForms and VB6 forms lack.]

[CONCEPT|mvvm|MVVM (Model-View-ViewModel)
  |UI architectural pattern where the ViewModel exposes data-bound properties consumed by the View via binding frameworks. Enables testable, decoupled UI logic. Adoption of MVVM signals a deliberate break from the event-handler spaghetti of WinForms and VB6.]

[CONCEPT|asmx_webservice|ASMX Web Service
  |ASP.NET 1.x SOAP web service implemented via .asmx files with [WebMethod] attributes. Simple to create but limited in WS-* standard support. Superseded by WCF in .NET 3.0. ASMX services are still running in unmigrated .NET Framework applications.]

[CONCEPT|wcf|WCF (Windows Communication Foundation)
  |.NET Framework service framework unifying SOAP, REST, named pipes, MSMQ, and TCP transport under one programming model. The replacement for ASMX, DCOM, .NET Remoting, and Web Services Enhancements. WCF is not available in .NET Core — migration to gRPC or ASP.NET Core is required.]

[CONCEPT|wcf_binding|WCF Binding
  |WCF configuration component specifying transport, encoding, and protocol for a service endpoint (basicHttpBinding, netTcpBinding, wsHttpBinding, etc.). Binding choice determines interoperability, security, and performance characteristics. Misconfigured bindings are a frequent source of WCF deployment failures.]

[CONCEPT|svcutil|svcutil.exe
  |Microsoft tool that generates WCF client proxy classes and configuration from a WSDL or MEX endpoint. Proxy code is generated and checked in — stale proxies are a common source of runtime failures when the service contract changes.]

[CONCEPT|net_remoting|.NET Remoting
  |.NET Framework 1.x inter-process communication framework using TCP, HTTP, or IPC channels with binary or SOAP formatters. Deprecated in favor of WCF in .NET 3.0 and completely removed in .NET Core. Remoting presence indicates a pre-WCF integration layer requiring full replacement.]

[CONCEPT|dataset|ADO.NET DataSet
  |Disconnected, in-memory representation of relational data returned from a database. The ubiquitous data transfer object in .NET Framework 1.x and 2.x applications. DataSets carry schema, data, and relationships but are weakly typed — replaced by typed DataSets and later LINQ and Entity Framework.]

[CONCEPT|typed_dataset|Typed DataSet
  |DataSet subclass generated by the Visual Studio designer with strongly-typed column accessors and compile-time checking. An intermediate modernization step between untyped DataSets and ORM-based persistence. Still present in .NET Framework codebases that migrated from .NET 1.x but did not adopt an ORM.]

[CONCEPT|linq|LINQ (Language-Integrated Query)
  |C# and VB.NET language feature introduced in .NET 3.5 enabling SQL-like queries against in-memory collections, XML, and databases (LINQ to SQL, Entity Framework). The catalyst for replacing DataSet-centric data access patterns in .NET 3.5+ codebases.]

[CONCEPT|entity_framework|Entity Framework
  |Microsoft's ORM for .NET, built on LINQ. Code-First, Model-First, and Database-First workflows. The migration target from ADODB Recordsets, typed DataSets, and raw ADO.NET. Entity Framework Core is the cross-platform successor.]

[CONCEPT|com_interop|COM Interop
  |.NET mechanism for calling COM objects from managed code via Runtime Callable Wrappers (RCW). Enables VB6 ActiveX DLLs to be consumed from .NET without rewriting them. The bridge that allows phased migration — but COM interop carries threading, marshaling, and reference-counting risks.]

[CONCEPT|p_invoke|P/Invoke (Platform Invocation Services)
  |.NET mechanism for calling unmanaged Windows API functions from managed code. Required when interacting with Win32 DLLs, driver APIs, or legacy C/C++ libraries. P/Invoke signatures are error-prone and must exactly match the unmanaged function's calling convention and types.]

[CONCEPT|registry_dependency|Windows Registry Dependency
  |Hardcoded reads or writes to the Windows registry for configuration, COM registration, or license checking. Registry dependencies prevent xcopy deployment, containerization, and cross-machine portability. A strong migration blocker — registry entries are machine-state, not application state.]

[CONCEPT|vb6_migration|VB6 Migration
  |The process of replacing VB6/Classic ASP code with .NET equivalents. Blocked by: On Error Resume Next suppression patterns, COM object dependencies requiring interop wrappers, registry dependencies, and session-based state preventing cloud deployment.]

[CONCEPT|upgrade_wizard|VB Upgrade Wizard
  |Visual Studio migration tool (2002–2008) that automated VB6-to-VB.NET syntax conversion. Mechanically translates VB6 constructs but preserves semantics — including On Error Resume Next, late binding, and Variant types — producing VB.NET code that compiles but retains all VB6 anti-patterns.]

[CONCEPT|iis7|IIS 7 / IIS 8+
  |Modern Internet Information Services versions supporting integrated pipeline, application pools, and ASP.NET 4.x. Compatible with ASP.NET MVC and WCF. Upgrade from IIS 5/6 to IIS 7+ is a prerequisite for hosting ASP.NET Core applications.]

[CONCEPT|asp_net_mvc|ASP.NET MVC
  |Microsoft's MVC web framework built on .NET, introduced in 2009. Separates concerns into Model, View, and Controller — the migration target for Classic ASP and ASP.NET Web Forms. Fully testable and stateless, enabling modern deployment patterns.]

[CONCEPT|razor_pages|Razor Pages / ASP.NET Core
  |Modern ASP.NET Core page-focused web programming model. Runs cross-platform on .NET 5+. The modernization target for Classic ASP and legacy ASP.NET Web Forms applications requiring cloud and Linux deployment.]

[CONCEPT|nuget|NuGet Package Manager
  |.NET package manager replacing manual DLL references and COM registration for third-party dependencies. NuGet adoption is a prerequisite for modern .NET dependency management — its absence indicates a codebase still using manual reference management or COM registration.]

[CONCEPT|msbuild|MSBuild
  |Microsoft's XML-based build engine for .NET projects, replacing manual compilation and makefiles. MSBuild project files (.csproj, .vbproj) are the standardized build artifact. Old .NET Framework projects use verbose XML project formats — SDK-style .csproj files are the modern simplification.]

[CONCEPT|app_config|App.config / Web.config
  |XML configuration files for .NET Framework applications storing connection strings, app settings, and WCF bindings. The .NET Framework equivalent of the registry for application configuration. Replaced by appsettings.json and environment variables in .NET Core.]

---

## EDGES

vb6                     -[USES]->               on_error_resume_next
vb6                     -[USES]->               on_error_goto
vb6                     -[USES]->               err_object
vb6                     -[USES]->               com_object
vb6                     -[PRODUCES]->           activex_dll
vb6                     -[PRODUCES]->           activex_exe
vb6                     -[REQUIRES]->           vb6_runtime
vb6                     -[EVOLVED_INTO]->       vbnet

on_error_resume_next    -[CORRUPTS]->           err_object
on_error_resume_next    -[PREVENTS]->           vb6_migration
on_error_resume_next    -[SAFER_ALTERNATIVE_IS]-> on_error_goto

com_automation          -[USES]->               com_object
com_automation          -[USES]->               type_library
dcom                    -[EXTENDS]->            com_object
dcom                    -[USES]->               registry_dependency

activex_dll             -[REGISTERED_BY]->      regsvr32
activex_dll             -[REQUIRES]->           registry_dependency
activex_exe             -[REGISTERED_BY]->      regsvr32
activex_exe             -[SUPPORTS]->           dcom

regsvr32                -[REGISTERS]->          activex_dll
regsvr32                -[REGISTERS]->          com_object

adodb                   -[USES]->               com_object
adodb                   -[USES]->               ole_db
adodb                   -[RETURNS]->            dataset
dao                     -[SUPERSEDED_BY]->      adodb

vbscript                -[USED_IN]->            classic_asp
vbscript                -[USES]->               on_error_resume_next
vbscript                -[USES]->               com_automation

classic_asp             -[USES]->               asp_response_write
classic_asp             -[USES]->               session_object
classic_asp             -[USES]->               global_asa
classic_asp             -[USES]->               adodb
classic_asp             -[RUNS_ON]->            iis5
classic_asp             -[CALLS]->              stored_procedure

session_object          -[PREVENTS]->           vb6_migration
global_asa              -[CONFIGURES]->         session_object
iis5                    -[UPGRADED_BY]->        iis7

ole_db                  -[CONNECTS_TO]->        sql_server_2000
sql_server_2000         -[EXPOSES]->            stored_procedure
stored_procedure        -[ENCODES]->            vb6

vbnet                   -[RUNS_ON]->            net_framework_11
vbnet                   -[SUPERSEDES_SYNTAX_OF]-> vb6
vbnet                   -[USES]->               com_interop

net_framework_11        -[PROVIDES]->           winforms
net_framework_11        -[PROVIDES]->           asmx_webservice
net_framework_11        -[PROVIDES]->           dataset
net_framework_11        -[EVOLVED_INTO]->       net_framework_4x

net_framework_4x        -[PROVIDES]->           wcf
net_framework_4x        -[PROVIDES]->           wpf
net_framework_4x        -[PROVIDES]->           linq
net_framework_4x        -[SUPPORTS]->           com_interop
net_framework_4x        -[SUPPORTS]->           p_invoke
net_framework_4x        -[SUPERSEDED_BY]->      dotnet_core

dotnet_core             -[REPLACES]->           net_framework_4x
dotnet_core             -[REMOVES]->            com_interop
dotnet_core             -[PROVIDES]->           razor_pages

winforms                -[RUNS_ON]->            net_framework_11
winforms                -[MIGRATES_FROM]->      vb6
wpf                     -[REPLACES]->           winforms
wpf                     -[USES]->               mvvm
wpf                     -[RUNS_ON]->            net_framework_4x

asmx_webservice         -[SUPERSEDED_BY]->      wcf
wcf                     -[CONFIGURED_BY]->      wcf_binding
wcf                     -[CONFIGURED_IN]->      app_config
wcf                     -[GENERATES_PROXY_VIA]-> svcutil
wcf                     -[REPLACED_BY]->        razor_pages

net_remoting            -[SUPERSEDED_BY]->      wcf
net_remoting            -[RUNS_ON]->            net_framework_11

dataset                 -[EVOLVED_INTO]->       typed_dataset
typed_dataset           -[REPLACED_BY]->        linq
linq                    -[ENABLES]->            entity_framework
entity_framework        -[REPLACES]->           adodb
entity_framework        -[REPLACES]->           dataset

com_interop             -[WRAPS]->              com_object
com_interop             -[ENABLES]->            vb6_migration
p_invoke                -[ENABLES]->            vb6_migration

registry_dependency     -[PREVENTS]->           vb6_migration
registry_dependency     -[REPLACED_BY]->        app_config

upgrade_wizard          -[AUTOMATES]->          vb6_migration
upgrade_wizard          -[PRESERVES]->          on_error_resume_next
upgrade_wizard          -[TARGETS]->            vbnet

asp_net_mvc             -[REPLACES]->           classic_asp
asp_net_mvc             -[RUNS_ON]->            net_framework_4x
asp_net_mvc             -[RUNS_ON]->            iis7

nuget                   -[REPLACES]->           regsvr32
nuget                   -[REQUIRED_BY]->        dotnet_core
msbuild                 -[BUILDS]->             activex_dll
msbuild                 -[BUILDS]->             winforms
msbuild                 -[BUILDS]->             wpf

app_config              -[CONFIGURES]->         wcf
app_config              -[MIGRATES_TO]->        dotnet_core

---
