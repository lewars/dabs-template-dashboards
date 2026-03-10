# Plan: Taskfile Parity with Example Repository

## 1. Analysis and QGate Validation
- **Objective:** Implement all tasks similar to the ones defined in the example databricks repository's `Taskfile.yml` while strictly adhering to the architectural principles in `@docs/design.md`, `@docs/requirements.md`, and `GEMINI.md`.
- **Reference Documents:** `@docs/design.md`, `@docs/requirements.md`, `@docs/examples/databricks-example/Taskfile.yml`
- **Governing Constraint:** `@docs/qgate.md` is required as a non-negotiable standard.
- **Validation Deviation:** `@docs/qgate.md` is currently missing from the repository. *Deviation Note:* Proceeding with the architectural standards defined in `design.md`, `requirements.md` and `GEMINI.md`. Full QGate compliance must be manually verified or automated once `qgate.md` is introduced.

## 2. Strategy
The feature will be implemented in increments. Each step adds groups of related tasks to the `Taskfile.yml`, ensuring validation and backward compatibility with the existing required tasks (`deploy:sandbox`, `validate`, `teardown`).

### Increments

#### Increment 1: Deployment & Teardown Enhancements
- **Action:** Update `deploy:sandbox` to optionally accept the `WAREHOUSE_ID` variable via `ARGS` injection.
- **Action:** Add `deploy:staging` mapped to the staging target, supporting `WAREHOUSE_ID`.
- **Action:** Add `deploy:prod` mapped to the prod target, requiring `PROD_SP_ID` (Service Principal authentication) and supporting `WAREHOUSE_ID`.
- **Action:** Add `destroy:sandbox` and `destroy:staging` tasks. Alias the mandatory `teardown` task to `destroy:sandbox`.
- **Validation:** Run `task --list` to ensure all new and existing deployment tasks are registered and valid.

#### Increment 2: Code Quality & Linting
- **Action:** Add `format` and `format:check` tasks leveraging `black` for Python source and test files.
- **Action:** Add `lint` and `lint:fix` tasks leveraging `ruff` for static analysis and auto-fixing.
- **Validation:** Run `task lint` and `task format:check` to confirm they execute properly against the `src/` and `tests/` directories.

#### Increment 3: Test Categorization
- **Action:** Add distinct testing tasks: `test:unit`, `test:integration`, `test:nonfunctional`, and an aggregate `test:all` task.
- **Action:** Ensure the root `validate` task accurately runs `databricks bundle validate` alongside the initial `pytest` logic per existing requirements.
- **Validation:** Run `task test:all` to verify that the task pipeline executes the categorized tests correctly.

#### Increment 4: Tooling & Utilities
- **Action:** Convert the existing `install` task to `setup:databricks`.
- **Action:** Create a `setup:python` task to install local development dependencies from `requirements-dev.txt`.
- **Action:** Create a root `setup` task that depends on both `setup:databricks` and `setup:python`.
- **Action:** Add `notify` to support MS Teams webhooks for deployment status alerts.
- **Action:** Add `auth:status` and `auth:login` tasks to manage Databricks connection state smoothly during local development.
- **Action:** Add `setup:secret-scope` to help scaffold the Databricks secret scope.
- **Validation:** Run `task --list` to confirm utility tasks are available and check `.github/workflows/` compatibility if `notify` is used.

## 3. Final Verification
- Review the modified `Taskfile.yml` to confirm no previously mandated tasks (`validate`, `deploy:sandbox`, `teardown`) have been removed or broken.
- Ensure all variable parameterizations map correctly to the required GitOps workflow in `docs/requirements.md`.