## META
name: Legacy Java Enterprise Monolith Intelligence
version: 1.0.0
domain: legacy-java-monolith
description: Schema and methodology for navigating legacy Java enterprise codebases — J2EE/EJB2 stacks, XML Spring configuration, Hibernate ORM, Struts MVC, and the modernization paths toward microservices and Spring Boot.
nodes: 51
edges: 83
source: Graphify.md Domain Library
license: MIT

---

## NODES

[CONCEPT|j2ee|J2EE (Java 2 Enterprise Edition)
  |Sun Microsystems enterprise Java platform specification covering EJBs, servlets, JMS, and JNDI. The canonical architecture for large Java enterprise applications from 2000–2008. Virtually all legacy Java monoliths trace their architecture to J2EE.]

[CONCEPT|ejb2|EJB 2.x (Enterprise JavaBeans)
  |Component model for distributed business logic in J2EE. Requires XML deployment descriptors, home/remote interfaces, and container-managed lifecycle. EJB 2.x code is notoriously difficult to unit-test and carries heavy boilerplate.]

[CONCEPT|ejb_jar_xml|ejb-jar.xml
  |XML deployment descriptor required for every EJB 2.x module. Declares bean names, types, transaction attributes, and security roles. The authoritative wiring document for an EJB module — but only interpretable by the application server at runtime.]

[CONCEPT|entity_bean|Entity Bean
  |EJB 2.x component representing a persistent data object, with container-managed or bean-managed persistence. Notoriously heavy and slow — replaced by Hibernate and JPA in nearly all modernization efforts.]

[CONCEPT|session_bean|Session Bean
  |EJB 2.x component encapsulating business logic. Stateless session beans are the workhorses of J2EE service layers. Their interfaces are string-referenced via JNDI, making static call graph analysis unreliable.]

[CONCEPT|mdb|Message-Driven Bean (MDB)
  |EJB 2.x component that consumes JMS messages asynchronously. No caller-visible interface — the trigger is a queue or topic event. MDB presence in a codebase indicates asynchronous processing paths invisible to static analysis.]

[CONCEPT|jndi|JNDI (Java Naming and Directory Interface)
  |Runtime lookup service for EJBs, datasources, and JMS resources. All references are string-keyed lookups resolved at runtime — the application server's namespace is the source of truth, not the source code.]

[CONCEPT|application_server|Java Application Server
  |Runtime container for J2EE applications: manages EJB lifecycle, transaction coordination, JNDI registry, and connection pooling. The deployment target for EAR and WAR files. Configuration is vendor-specific and often undocumented.]

[CONCEPT|websphere|IBM WebSphere Application Server
  |IBM's J2EE application server, dominant in banking and insurance. WebSphere-specific APIs and deployment conventions add a vendor lock-in layer on top of J2EE standards, complicating migration.]

[CONCEPT|jboss|JBoss / WildFly Application Server
  |Red Hat's open-source J2EE application server. Widely used in mid-market enterprise Java. JBoss-specific deployment descriptors (jboss.xml) exist alongside standard ejb-jar.xml, creating dual wiring artifacts.]

[CONCEPT|weblogic|Oracle WebLogic Server
  |Oracle's J2EE application server, prevalent in financial services and Oracle-stack shops. WebLogic proprietary extensions (weblogic.xml, weblogic-ejb-jar.xml) are required for full deployment and add to migration complexity.]

[CONCEPT|datasource|JNDI Datasource
  |Database connection pool registered in the application server's JNDI namespace. Java code looks up datasources by string name at runtime — the actual database URL and credentials are in server configuration, not in application source.]

[CONCEPT|hibernate|Hibernate ORM
  |Object-relational mapping framework that replaced EJB 2.x entity beans as the standard persistence layer in Java enterprise applications. Hibernate introduced HQL, session-based caching, and lazy loading — all of which create debugging complexity.]

[CONCEPT|hibernate_template|HibernateTemplate
  |Spring 2.x helper class that wraps Hibernate Session operations in a try/catch/finally pattern with automatic exception translation. Deprecated in Spring 3.x but present in millions of lines of legacy Spring+Hibernate code.]

[CONCEPT|hibernate_hbm_xml|Hibernate hbm.xml Mapping
  |XML mapping files that define how Java classes correspond to database tables in older Hibernate configurations. Precede JPA annotations — a codebase with .hbm.xml files is running Hibernate 3.x-era configuration patterns.]

[CONCEPT|xml_spring_config|Spring XML Application Context
  |Spring XML configuration files (applicationContext.xml, dispatcher-servlet.xml) containing thousands of bean definitions. Bean names are strings resolved at runtime, making static analysis unable to determine wiring without executing the context. A codebase with deep XML Spring config cannot be reliably analyzed without loading the application.]

[CONCEPT|spring_2x|Spring Framework 2.x
  |Early Spring versions that relied entirely on XML configuration for dependency injection and AOP. The dominant enterprise Java framework 2004–2009. Spring 2.x codebases are characterized by large XML files and HibernateTemplate usage.]

[CONCEPT|spring_3x|Spring Framework 3.x
  |Spring version that introduced annotation-driven configuration (@Component, @Service, @Autowired) and REST support via Spring MVC. Transitional: most Spring 3.x codebases mix XML and annotation config, making the wiring model ambiguous.]

[CONCEPT|component_scan|Spring Component Scan
  |Annotation-driven bean discovery (@ComponentScan) that eliminates explicit XML bean declarations. Beans are discovered by classpath scanning for @Component, @Service, @Repository annotations. Replaces XML bean registration but requires annotation discipline.]

[CONCEPT|annotation_config|Spring Annotation-Based Config
  |@Configuration classes and @Bean methods as a Java-native alternative to XML application contexts. Introduced in Spring 3.0. Allows static analysis to trace bean wiring through Java code rather than XML string lookups.]

[CONCEPT|spring_boot|Spring Boot
  |Convention-over-configuration Spring extension that provides embedded servers, auto-configuration, and starter dependencies. The target architecture for legacy Java modernization — eliminates application server dependency and enables containerization.]

[CONCEPT|spring_mvc|Spring MVC
  |Spring's web framework implementing the Model-View-Controller pattern via DispatcherServlet. The modernization target for Struts 1/2 and JSF applications. Spring MVC is fully compatible with both XML and annotation-based Spring configuration.]

[CONCEPT|jpa|JPA (Java Persistence API)
  |Standard Java ORM specification (JSR 338) that Hibernate implements. JPA annotations (@Entity, @ManyToOne) on domain classes replace both EJB 2.x entity beans and Hibernate hbm.xml mappings. The canonical persistence layer for modern Spring applications.]

[CONCEPT|spring_data_jpa|Spring Data JPA
  |Spring abstraction over JPA that generates repository implementations from interface method names. Eliminates boilerplate JPQL queries for CRUD operations. The target replacement for HibernateTemplate and JDBC-based data access patterns.]

[CONCEPT|struts1|Apache Struts 1.x
  |MVC web framework dominant in J2EE applications from 2001–2007. Configuration via struts-config.xml. Actions are thread-unsafe singletons with form bean coupling. Struts 1.x reached end-of-life in 2013 but persists in unmaintained codebases.]

[CONCEPT|struts2|Apache Struts 2.x
  |MVC web framework succeeding Struts 1, based on WebWork. Configuration via struts.xml and annotations. Struts 2 introduced interceptors and OGNL expression language. Known for critical CVEs (2017–2023) making unmigrated deployments high-risk.]

[CONCEPT|jsf|JavaServer Faces (JSF)
  |Java EE standard component-based web framework. Stateful server-side UI model with component trees stored in HttpSession. JSF applications carry heavy session state that complicates horizontal scaling and containerization.]

[CONCEPT|ant_build|Apache Ant Build
  |XML-based build tool predating Maven and Gradle. Ant build.xml files are procedural — every step is explicitly scripted with no dependency management or convention. Ant codebases require manual classpath management that causes classpath_hell.]

[CONCEPT|maven_pom|Maven POM (pom.xml)
  |Declarative build descriptor that introduced dependency management, lifecycle phases, and convention-over-configuration to Java builds. The prerequisite for modern CI/CD pipelines. Most legacy Java projects migrated from Ant to Maven between 2007–2015.]

[CONCEPT|gradle_build|Gradle Build
  |Groovy/Kotlin DSL build tool that supersedes Maven for new Java projects. Supports incremental compilation and build caching. The target build system for Spring Boot microservices extracted from legacy monoliths.]

[CONCEPT|war_file|WAR File (Web Application Archive)
  |Deployable unit for Java web applications. Contains servlets, JSPs, static resources, and WEB-INF/web.xml. WARs are deployed to application servers — a strong indicator of server-bound architecture incompatible with containerization.]

[CONCEPT|ear_file|EAR File (Enterprise Application Archive)
  |Top-level J2EE deployable that bundles multiple WARs and EJB JARs with a shared application.xml descriptor. EAR deployment implies hard dependencies between bundled modules and shared classpath — the primary mechanism of classpath_hell in J2EE systems.]

[CONCEPT|classpath_hell|Classpath Hell
  |Runtime conflicts from multiple incompatible versions of the same JAR on a shared classpath. Endemic in EAR deployments where modules share the application server's global classpath. Makes dependency isolation impossible without modular runtimes or containers.]

[CONCEPT|log4j_xml|log4j.xml / log4j.properties
  |Legacy logging configuration files for Apache Log4j 1.x. Their presence indicates Log4j 1.x dependency — which reached end-of-life in 2015 and contains known vulnerabilities. A reliable marker of unmaintained dependency management.]

[CONCEPT|static_analysis|Static Analysis
  |Examination of source code without execution to identify patterns, dependencies, and defects. In legacy Java monoliths, XML Spring configuration and JNDI string lookups defeat static analysis — the real wiring is only visible at runtime.]

[CONCEPT|jdbc_template|JdbcTemplate
  |Spring utility class that handles JDBC boilerplate (open/close connection, exception translation, result set mapping). Simpler than Hibernate but produces SQL-coupled code. JdbcTemplate DAOs are common in Spring 2.x codebases alongside Hibernate.]

[CONCEPT|jms|JMS (Java Message Service)
  |Standard Java API for asynchronous messaging. JMS producers and consumers are decoupled by queue/topic names registered in JNDI — making message flow invisible to static analysis. MDBs are the EJB-side consumer of JMS messages.]

[CONCEPT|messaging_middleware|Enterprise Messaging Middleware
  |Message broker infrastructure (IBM MQ, ActiveMQ, TIBCO EMS) that implements JMS. Queue and topic names are configuration-level — the dependency between a producer and consumer only exists in the middleware namespace, not the source code.]

[CONCEPT|service_locator|Service Locator Pattern
  |Anti-pattern that wraps JNDI lookups in a static utility class, making dependencies implicit and untestable. Prevalent in EJB 2.x and early Spring codebases as a workaround for the lack of dependency injection frameworks.]

[CONCEPT|god_class|God Class
  |A class that knows too much or does too much — thousands of lines, dozens of responsibilities, and dependencies throughout the codebase. The most common structural anti-pattern in monolithic Java applications.]

[CONCEPT|transaction_script|Transaction Script
  |Anti-pattern where business logic is organized as a single procedural script per use case rather than in domain objects. Common in Struts Action classes and EJB session beans where each method is a flat sequence of JDBC calls and business logic.]

[CONCEPT|monolith|Legacy Java Monolith
  |A single deployable unit (typically an EAR or WAR) containing all application functionality with shared data, shared process, and shared deployment lifecycle. Changes to any component require redeploying the entire system.]

[CONCEPT|big_ball_of_mud|Big Ball of Mud
  |Software architecture anti-pattern (Foote & Yoder 1999) where the system has no discernible structure — modules are coupled to each other with no clear boundaries or abstraction. The end state of an unmaintained monolith after years of ad-hoc patches.]

[CONCEPT|deployment_descriptor|Deployment Descriptor
  |XML configuration file (web.xml, ejb-jar.xml, application.xml) that specifies runtime behavior of a Java EE component. Pre-Java-EE-6 applications depend entirely on deployment descriptors — annotations did not replace them until Servlet 3.0 / EJB 3.1.]

[CONCEPT|bounded_context|Bounded Context
  |Domain-Driven Design concept (Evans 2003) defining the explicit boundary within which a domain model is consistent and authoritative. Identifying bounded contexts in a monolith is the prerequisite step before microservice extraction.]

[CONCEPT|strangler_fig|Strangler Fig Pattern
  |Modernization strategy (Fowler 2004) where new services are built alongside the monolith, gradually intercepting requests until the legacy component can be decommissioned. Avoids big-bang rewrite risk by keeping the legacy running throughout migration.]

[CONCEPT|microservice_extraction|Microservice Extraction
  |The process of carving a bounded context out of a monolith and deploying it as an independently deployable service with its own database and API. Requires identifying seams — data owned exclusively by one context and not shared with others.]

[CONCEPT|containerization|Containerization (Docker/OCI)
  |Packaging an application and its runtime dependencies into a portable container image. Application-server-bound J2EE applications cannot be containerized without significant refactoring — containerization is both a modernization goal and a prerequisite for cloud deployment.]

[CONCEPT|rest_api|REST API
  |HTTP-based service interface following representational state transfer constraints. The target integration pattern when extracting microservices from a monolith — replaces EJB remote interfaces, RMI, and JNDI-based inter-module communication.]

[CONCEPT|docker|Docker
  |Container runtime and image format that enables packaging Spring Boot applications with their embedded server into portable OCI images. Incompatible with EAR-style J2EE deployment without rearchitecting to eliminate application server dependencies.]

[CONCEPT|kubernetes|Kubernetes
  |Container orchestration platform for deploying, scaling, and managing containerized microservices. The target infrastructure layer for extracted microservices. Requires stateless application design — problematic for JSF and session-heavy J2EE apps.]

---

## EDGES

j2ee                    -[CONTAINS]->           ejb2
j2ee                    -[CONTAINS]->           mdb
j2ee                    -[REQUIRES]->           application_server
j2ee                    -[SPECIFIES]->          deployment_descriptor
j2ee                    -[USES]->               jndi
j2ee                    -[USES]->               jms

ejb2                    -[CONFIGURED_BY]->      ejb_jar_xml
ejb2                    -[CONTAINS]->           entity_bean
ejb2                    -[CONTAINS]->           session_bean
ejb2                    -[DEPLOYED_TO]->        application_server

jndi                    -[LOCATES]->            ejb2
jndi                    -[LOCATES]->            datasource
jndi                    -[LOCATES]->            jms
jndi                    -[DEFEATS]->            static_analysis

websphere               -[IMPLEMENTS]->         j2ee
jboss                   -[IMPLEMENTS]->         j2ee
weblogic                -[IMPLEMENTS]->         j2ee
websphere               -[RUNS]->               ear_file
jboss                   -[RUNS]->               ear_file
weblogic                -[RUNS]->               ear_file

hibernate               -[REPLACES]->           entity_bean
hibernate               -[USES]->               hibernate_hbm_xml
hibernate               -[EVOLVED_INTO]->       jpa

hibernate_template      -[WRAPS]->              hibernate
hibernate_template      -[DEPRECATED_BY]->      spring_data_jpa

xml_spring_config       -[CONFIGURES]->         hibernate
xml_spring_config       -[CONFIGURES]->         datasource
xml_spring_config       -[PREVENTS]->           static_analysis
xml_spring_config       -[WIRES]->              jdbc_template

spring_2x               -[USES]->               xml_spring_config
spring_2x               -[USES]->               hibernate_template
spring_2x               -[CONTAINS]->           spring_mvc

spring_3x               -[SUPPORTS]->           component_scan
spring_3x               -[SUPPORTS]->           annotation_config
spring_3x               -[EVOLVED_FROM]->       spring_2x

component_scan          -[REPLACES]->           xml_spring_config
annotation_config       -[REPLACES]->           xml_spring_config

spring_boot             -[REPLACES]->           xml_spring_config
spring_boot             -[ENABLES]->            containerization
spring_boot             -[EMBEDS]->             spring_mvc
spring_boot             -[USES]->               jpa

jpa                     -[REPLACES]->           hibernate_hbm_xml
jpa                     -[REPLACES]->           entity_bean
spring_data_jpa         -[IMPLEMENTS]->         jpa
spring_data_jpa         -[REPLACES]->           hibernate_template
spring_data_jpa         -[REPLACES]->           jdbc_template

ant_build               -[SUPERSEDED_BY]->      maven_pom
maven_pom               -[SUPERSEDED_BY]->      gradle_build
maven_pom               -[PRODUCES]->           war_file
maven_pom               -[PRODUCES]->           ear_file

war_file                -[COMPONENT_OF]->       ear_file
war_file                -[DEPLOYED_TO]->        application_server
ear_file                -[CAUSES]->             classpath_hell
ear_file                -[DEPLOYED_TO]->        application_server
classpath_hell          -[PREVENTS]->           containerization

deployment_descriptor   -[REQUIRED_BY]->        ear_file
deployment_descriptor   -[REPLACED_BY]->        annotation_config

struts1                 -[RUNS_ON]->            j2ee
struts2                 -[RUNS_ON]->            j2ee
jsf                     -[RUNS_ON]->            j2ee
struts1                 -[SUPERSEDED_BY]->      struts2
struts1                 -[REPLACED_BY]->        spring_mvc
struts2                 -[REPLACED_BY]->        spring_mvc
jsf                     -[REPLACED_BY]->        spring_mvc

jdbc_template           -[WRAPS]->              datasource

mdb                     -[CONSUMES]->           jms
jms                     -[DELIVERED_BY]->       messaging_middleware
messaging_middleware    -[REGISTERED_IN]->      jndi

service_locator         -[ANTIPATTERN_FOR]->    jndi
service_locator         -[REPLACED_BY]->        xml_spring_config
god_class               -[INSTANCE_OF]->        big_ball_of_mud
transaction_script      -[INSTANCE_OF]->        big_ball_of_mud
monolith                -[CONTAINS]->           god_class
monolith                -[DEGRADES_INTO]->      big_ball_of_mud
monolith                -[REQUIRES]->           bounded_context

log4j_xml               -[SIGNALS]->            static_analysis

bounded_context         -[ENABLES]->            microservice_extraction
microservice_extraction -[USES]->               strangler_fig
microservice_extraction -[TARGETS]->            spring_boot
microservice_extraction -[EXPOSES]->            rest_api

spring_boot             -[DEPLOYED_AS]->        docker
docker                  -[ORCHESTRATED_BY]->    kubernetes
containerization        -[IMPLEMENTED_BY]->     docker

---
