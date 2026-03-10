# Databricks DataOps Automation Context

This repository follows a strict Colocated DAB Pattern, GitOps lifecycle, and environment isolation as defined in the DataOps Platform Design Document.

## Quick Start

1. Define variables in `databricks.yml` and targets.
2. Run `task validate` to validate the bundle.
3. Run `task deploy:sandbox` to deploy to your sandbox workspace.

## Documentation

See the `docs/` directory for design and requirements.
