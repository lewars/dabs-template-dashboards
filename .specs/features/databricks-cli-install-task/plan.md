# Implementation Plan: Add Databricks CLI Installation Task

## 1. Analysis and Validation
- **Missing Governing Documents**: Encountered missing constraint documents: `@docs/qgate.md`, `@docs/domain-driven-design-spec.md`, `@docs/domains/`, and `@docs/templates/plan.md`.
- **Deviation Note**: As `@docs/qgate.md` is not present, compliance cannot be explicitly validated against it. The plan proceeds by adhering strictly to the architecture and constraints defined in `@docs/requirements.md`, `@docs/design.md`, and the provided `GEMINI.md`.
- **Goal**: Implement a task in `Taskfile.yml` to install the Databricks CLI, and update the CI/CD workflows (`deploy-prod.yml`, `deploy-staging.yml`) to execute this task before running any Databricks CLI commands or tasks that depend on it.

## 2. Strategy
The feature will be implemented in small, testable increments to ensure compliance and correctness:

1. **Update `Taskfile.yml`**: Add a new task `install` that securely fetches and executes the official Databricks CLI installation script.
2. **Update Staging Workflow (`deploy-staging.yml`)**: Execute `task install` immediately after the Task runner setup, but before any Databricks commands (like `task validate` or deploy).
3. **Update Production Workflow (`deploy-prod.yml`)**: Execute `task install` before the production deployment step.

## 3. Execution Steps

### Step 1: Add Task to `Taskfile.yml`
- Modify `Taskfile.yml` to include an `install` task.
  ```yaml
  install:
    desc: "Installs the Databricks CLI."
    cmds:
      - curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/setup.sh | sh
    silent: true
  ```
- *Validation*: Use `task --list` to verify it appears in the task list. Test execution locally if applicable.

### Step 2: Update `.github/workflows/deploy-staging.yml`
- Insert a step named `Install Databricks CLI` utilizing the new task, placed between `Setup Task` and `Validate`.
  ```yaml
      - name: Install Databricks CLI
        run: task install
  ```
- *Validation*: Check YAML syntax and step order.

### Step 3: Update `.github/workflows/deploy-prod.yml`
- Insert a step named `Install Databricks CLI` utilizing the new task, placed right before the `Deploy to Prod` step.
  ```yaml
      - name: Install Databricks CLI
        run: task install
  ```
- *Validation*: Check YAML syntax and step order.

## 4. Final Review
- Ensure workflows remain valid GitHub Actions definitions.
- Verify that the plan aligns with the project requirement of abstracting operations using the Task runner.
