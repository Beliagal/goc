# Guardian of the Code (GOC) - Intelligent Code Auditor & Refactoring Agent

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Architecture](https://img.shields.io/badge/architecture-Hexagonal%20%2F%20Ports%20%26%20Adapters-orange.svg)]()
[![Methodology](https://img.shields.io/badge/methodology-TDD%20%2F%20Mandatory-red.svg)]()

An autonomous, intelligent auditing and refactoring agent designed to elevate code quality and security within software repositories through deep semantic analysis, OWASP vulnerability detection, and the automatic application of advanced design patterns.

---

## 🌐 Language Navigation / Navegación de Idiomas
* [English Version](#english-version)
* [Versión en Español](#versión-en-español)

---

# English Version

## 1. Project Vision & Purpose
**Guardian of the Code (GOC)** serves as an automated gatekeeper for modern software engineering. By acting as an autonomous AI-driven architect, it scans source code repositories to identify critical security exploits (aligned with OWASP top 10) and architectural anti-patterns, generating production-ready, decoupled, and compliant refactoring proposals.

### Core Objectives:
* **Proactive Auditing:** Deep semantic detection of design flaws and structural security vulnerabilities.
* **Intelligent Refactoring:** Generating deterministic code changes backed by **Hexagonal Architecture** and **SOLID Principles**.
* **Quality Automation:** Seamless continuous integration with Version Control Systems (VCS) like GitHub.

---

## 2. Technical Stack & Constraints
The engine strictly operates under rigid software design rules to ensure zero architectural drift:
* **Language:** Python 3.11+
* **Framework:** FastAPI (Asynchronous entry points)
* **Architecture:** Hexagonal (Strict separation: `Domain` → `Application` → `Infrastructure`)
* **Methodology:** Test-Driven Development (TDD) via `pytest` (100% atomic coverage required)
* **AI Orchestration:** LangChain (Deterministic parsing, low temperature configurations)
* **Persistence:** PostgreSQL (Async engine via SQLAlchemy 2.0 & Alembic migrations)

---

## 3. Project Roadmap

### Phase 1: Domain Foundation (Domain Layer)
* [ ] Inmutable Value Objects (`Severity`, `VulnerabilityType`, `CWEId`) with native business rules validation.
* [ ] Aggregate Roots & Core Entities (`Repository`, `Finding`, `AuditReport`).
* [ ] Pure Inversion of Control Contracts / Ports (`CodeAnalyzerPort`, `RepositoryStoragePort`, `VCSClientPort`).
* [ ] Strongly typed, decoupled Domain Exception Hierarchy.

### Phase 2: Application Orchestration (Use Cases)
* [ ] `AnalyzeRepository` Use Case: Coordinate cloning, asynchronous multi-file parsing, and report serialization.
* [ ] `GenerateRefactorProposal` Use Case: High-level patch isolation without violating structural boundaries.
* [ ] `ExportAuditReport` Use Case: Context-preserving presentation data models (Markdown/JSON).

### Phase 3: Infrastructure Adapters
* [ ] **Persistence:** `PostgresRepositoryAdapter` utilizing SQLAlchemy data mapping and migrations.
* [ ] **AI Engine:** `LangChainAnalyzerAdapter` with deterministic prompt structural controls.
* [ ] **VCS Integration:** `GitHubAdapter` for secure repository ingestion and diff management.

### Phase 4: Entry Points
* [ ] **REST API:** Robust FastAPI routing with dependency injection schemas.
* [ ] **CLI App:** Local development command-line interface via `click` and `rich`.

---

## 4. Current Status
* **Current State:** 🏗️ **Initialization / Foundation Phase**.
* **Completed:** Repository layout scaffolded, isolated virtual environment provisioned, and deterministic dependencies locked in `requirements.txt`.
* **Next Milestone:** Implementation of the Core Domain Model (Value Objects, Entities, and Port Contracts) using strict Test-Driven Development (TDD).

---

## 5. Quick Start

### Prerequisites
* Python 3.11 or higher installed locally.
* Git Bash / WSL or compatible Linux environment terminal.

### Installation & Execution
Follow these exact steps from your root console to set up the runtime environment:

```bash
# 1. Clone or initialize the project directory structure
# 2. Spin up the isolated virtual environment
python -m venv venv

# 3. Activate the environment context
source venv/Scripts/activate

# 4. Standardize core package management utilities
python -m pip install --upgrade pip setuptools wheel

# 5. Perform a deterministic installation of locked dependencies
pip install -r requirements.txt