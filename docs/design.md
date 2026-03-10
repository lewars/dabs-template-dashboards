# DESIGN.md: Dashboard Template (Colocated DAB Pattern)

## 1. Introduction

This document defines the technical architecture for the `dabs-template-dashboards` project. It implements the **Colocated DAB Pattern**, where dashboard metadata (JSON) and infrastructure definitions (YAML) are managed as a single, atomic unit of deployment.

## 2. Architectural Principles

### 2.1 Colocated DAB Pattern

All assets required for a functional dashboard are stored within the same repository. This ensures that a specific version of a dashboard is always deployed alongside its required SQL Warehouse configurations, permissions, and parameters.

### 2.2 State Management

Resource state is managed by the Databricks Asset Bundle (DAB) framework.

* **Development**: State is tied to the individual developer's prefix to allow for isolated "Sandbox" environments.
* **Production**: State is managed via a Service Principal to ensure a single, authoritative source of truth.

## 3. Component Design

### 3.1 Resource Definitions (`resources/`)

Resources are defined using modular YAML files.

* **Dashboards**: Defined in `resources/dashboards.yml`, referencing JSON files in `src/dashboards/`.
* **Compute**: SQL Warehouse references are parameterized to point to environment-specific warehouses (e.g., `Serverless` in Dev, `Pro` in Prod).

### 3.2 Command Abstraction (Taskfile)

To reduce cognitive load and prevent CLI errors, all interactions are abstracted through `Taskfile.yml`.

* **Encapsulation**: Users run `task deploy:sandbox` instead of long-form `databricks bundle deploy` commands with multiple flags.
* **Validation**: Every deployment task is prefixed with a validation step to catch syntax errors before hitting the workspace.

### 3.3 Variable Mapping

The project uses a hierarchical variable strategy:

1. **Root Defaults**: Defined in `databricks.yml`.
2. **Target Overrides**: Defined in `targets/*.yml` (e.g., `prod.yml` sets `catalog_name` to `prod_catalog`).

## 4. Environment & Deployment Lifecycle

### 4.1 Sandbox (Local Development)

Developers use the `sandbox` target for rapid iteration.

* **Path**: `/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/sandbox`
* **Naming**: Assets are prefixed with the user's name to prevent overwriting shared resources.

### 4.2 Staging (Validation)

Triggered by Pull Requests. This environment acts as a "Pre-Flight" check where automated integration tests are run against a shared staging workspace.

### 4.3 Production (Authority)

The only environment where assets are deployed without a "Sandbox" or "Staging" suffix. Deployments are strictly controlled by the CI/CD pipeline and authenticated via Service Principal.

## 5. Security & Governance

### 5.1 Access Control

Access to dashboards is managed via the `access_control_list` block within the resource definition. This automates the assignment of "Can View" or "Can Run" permissions to specific Unity Catalog groups.

### 5.2 Secret Management

No credentials or PAT tokens are stored in the repository. Authentication relies on:

* **Local**: Environment variables or Databricks CLI configuration profiles.
* **CI/CD**: GitHub Actions secrets mapped to `DATABRICKS_HOST` and `DATABRICKS_TOKEN`.

## 6. Observability

* **Deployment Status**: MS Teams webhooks provide real-time alerts on deployment success or failure.
* **Versioning**: Every production deployment is tagged with a Semantic Version (SemVer) via `release-please`, providing a clear audit trail of dashboard changes.
