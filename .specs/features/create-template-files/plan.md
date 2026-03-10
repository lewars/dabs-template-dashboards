# Plan: Create All Necessary Template Files

## 1. Analysis and QGate Validation
- **Objective:** Create the Databricks Asset Bundle (DAB) template files to enforce the Colocated DAB Pattern, GitOps lifecycle, and environment isolation.
- **Reference Documents:** `@docs/design.md`, `@docs/requirements.md`
- **Governing Constraint:** `@docs/qgate.md` is required as a non-negotiable standard.
- **Validation Deviation:** `@docs/qgate.md` is currently missing from the repository. *Deviation Note:* Proceeding with the architectural standards defined in `design.md` and `requirements.md`. Full QGate compliance must be manually verified or automated once `qgate.md` is introduced.

## 2. Strategy
The feature will be implemented incrementally. Each step ensures a functional segment of the DAB template is established, culminating in a complete, deployable bundle structure.

### Increments

#### Increment 1: Directory Structure & Core Configuration
- **Action:** Scaffold the directories (`targets/`, `src/dashboards/`, `tests/`, `.github/workflows/`, `resources/`).
- **Action:** Create `databricks.yml` (The Skeleton) establishing variables (e.g., `catalog_name`, `schema_name`, `warehouse_id`) and defining the base bundle configuration without environment overrides.
- **Action:** Create an initial `README.md` explaining the project structure and usage.
- **Validation:** Ensure `databricks.yml` is well-formed YAML and defines all required variables from `requirements.md`.

#### Increment 2: Environment Targets
- **Action:** Create `targets/sandbox.yml` with the user-specific workspace path: `/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/sandbox`.
- **Action:** Create `targets/staging.yml` pointing to the shared integration layer workspace.
- **Action:** Create `targets/prod.yml` mapping to the authoritative production workspace.
- **Validation:** Verify that each target appropriately overrides `databricks.yml` variables (like catalog, schema) to guarantee strict environment isolation.

#### Increment 3: Dashboard Resources
- **Action:** Create `src/dashboards/ops_overview.json` as a baseline generic dashboard template.
- **Action:** Create `resources/dashboards.yml` mapping to the JSON file. Ensure the `display_name` utilizes `${bundle.target}` to prevent resource duplication (e.g., `display_name: "Operations Overview [${bundle.target}]"`).
- **Validation:** Validate that the dashboard YAML schema correctly scopes access permissions (e.g., Unity Catalog group ACLs).

#### Increment 4: Taskfile Abstraction
- **Action:** Create `Taskfile.yml` as the required command abstraction layer.
- **Action:** Define the `validate`, `deploy:sandbox`, and `teardown` tasks.
- **Validation:** Run `task --list` to ensure the Go Task runner correctly interprets the file and exposes only the permitted CLI wrappers.

#### Increment 5: CI/CD Pipelines
- **Action:** Create `.github/workflows/deploy-staging.yml` for the standard PR-to-main trigger, including the `task validate` and staging deployment actions.
- **Action:** Create `.github/workflows/deploy-prod.yml` capturing the Fast-Track ChatOps path (`/release` comment trigger) leveraging Service Principal authentication and Semantic Versioning via `release-please`.
- **Validation:** Check the GitHub Actions syntax using `act` (if available) or standard workflow validation tools.

#### Increment 6: Testing & Validation Layer
- **Action:** Create a placeholder test in `tests/test_integration.py` or a shell validation script that `task validate` executes alongside `databricks bundle validate`.
- **Validation:** Execute `task validate` successfully with mock test execution.

## 3. Final Verification
- Review the entire project layout against `docs/requirements.md` (Section 2: Repository Structure) and `docs/design.md` (Sections 3, 4, and 5).
- Ensure no hardcoded tokens/credentials exist.
