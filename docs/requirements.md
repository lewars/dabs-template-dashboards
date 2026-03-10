# Requirements: Databricks Asset Bundle (DAB) Project Template

## 1. Project Objective

To provide a standardized blueprint for Databricks dashboard projects that prevents resource duplication and enforces a structured deployment lifecycle through GitOps and ChatOps as defined in the DataOps Platform Design Document.

## 2. Repository Structure

The project follows a Colocated DAB Pattern, ensuring infrastructure and business logic reside in the same version-controlled unit:

```text
├── databricks.yml          # Main coordinator (The "Skeleton")
├── Taskfile.yml            # Command abstraction (Task runner)
├── .github/workflows/      # CI/CD (Standard & Fast-Track paths)
├── targets/                # Environment-specific overrides
│   ├── sandbox.yml         # User-specific dev areas
│   ├── staging.yml         # Automated integration layer
│   └── prod.yml            # Restricted source of truth
├── src/
│   └── dashboards/         # Dashboard JSON definitions
├── tests/                  # Integration & validation scripts
└── README.md

```

## 3. Environment Isolation & Naming

To prevent the critical issue of resource duplication where assets with identical names are overwritten, the template implements:

* **Sandbox Isolation**: Every user/branch has a unique namespace. Target path: `/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/sandbox`.
* **Target-Based Logic**: All resources must include `${bundle.target}` in their `display_name` to distinguish between environments (e.g., "Executive Dashboard [Staging]").

## 4. Automation & CLI Interface

Raw CLI commands are prohibited in the development workflow. The template utilizes a **Taskfile** to wrap complex operations:

* **task deploy:sandbox**: Deploys the current branch to the user's personal workspace.
* **task validate**: Executes `databricks bundle validate` and runs `pytest` for unit/integration logic.
* **task teardown**: Removes sandbox resources to optimize cloud spend.

## 5. CI/CD Integration (Dual-Path Strategy)

The template’s GitHub Actions support two distinct deployment flows:

| Path | Trigger | Actions |
| --- | --- | --- |
| **Standard Path** | PR Merge to `main` | Deploys to Staging -> Runs Integration Tests -> Triggers `release-please` for Prod. |
| **Fast-Track** | `/release` comment | Bypasses standard cycle; immediate merge and Production deployment (ChatOps). |

## 6. Versioning & Governance

* **Semantic Versioning**: The template is compatible with `release-please`. Commit messages must follow **Conventional Commits** (e.g., `feat:`, `fix:`) to trigger automated version bumps.
* **Production Security**: Production deployments are restricted to **Service Principals** to protect environment integrity.
* **Notifications**: Automated feedback is sent via **MS Teams Webhooks** for release start, success, or failure.

## 7. Technical Standards

* **No Hardcoding**: All Workspace URLs, IDs, and Catalog names must be parameterized via variables.
* **Unity Catalog**: Use `${var.catalog_name}` and `${var.schema_name}` to ensure data isolation.
* **Local Testing**: Support for `act` to allow developers to run GitHub Actions locally.

## Reference Documents
- **Core Requirements**: Refer to `docs/requirements.md` for the functional specifications, environment strategy, and project objectives. All generated code must align with the "Dual-Path" CI/CD strategy and "Sandbox Isolation" rules defined there.
- **docs/design.md**: Defines the "How" (Architecture, Colocated Pattern logic, Resource Relationship mapping).
- **docs/databricks.md (External)**: The master platform design document for the broader DataOps ecosystem.
