import os
import yaml
import pytest

def get_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

class TestIncrement1DirectoryStructureAndCoreConfig:
    def test_required_directories_exist(self):
        required_dirs = ['targets', 'src/dashboards', 'tests', '.github/workflows', 'resources']
        for d in required_dirs:
            assert os.path.isdir(d), f"Required directory {d} is missing."

    def test_databricks_yml_exists_and_valid(self):
        assert os.path.isfile('databricks.yml'), "databricks.yml is missing."
        config = get_yaml('databricks.yml')
        assert 'bundle' in config, "databricks.yml missing 'bundle' definition."
        assert 'name' in config['bundle'], "databricks.yml missing 'bundle.name'."
        assert 'variables' in config, "databricks.yml missing 'variables' definition."
        
        vars = config.get('variables', {})
        assert 'catalog_name' in vars, "databricks.yml missing variable 'catalog_name'."
        assert 'schema_name' in vars, "databricks.yml missing variable 'schema_name'."
        assert 'warehouse_id' in vars, "databricks.yml missing variable 'warehouse_id'."

    def test_readme_exists(self):
        assert os.path.isfile('README.md'), "README.md is missing."

class TestIncrement2EnvironmentTargets:
    def test_targets_sandbox_yml(self):
        assert os.path.isfile('targets/sandbox.yml'), "targets/sandbox.yml is missing."
        config = get_yaml('targets/sandbox.yml')
        assert 'targets' in config, "targets/sandbox.yml missing 'targets' block."
        assert 'sandbox' in config['targets'], "targets/sandbox.yml missing 'sandbox' target."
        
        sandbox = config['targets']['sandbox']
        expected_path = '/Users/${workspace.current_user.userName}/.bundle/${bundle.name}/sandbox'
        assert sandbox.get('workspace', {}).get('root_path') == expected_path, \
            f"Sandbox root_path is not '{expected_path}'"

    def test_targets_staging_yml(self):
        assert os.path.isfile('targets/staging.yml'), "targets/staging.yml is missing."
        config = get_yaml('targets/staging.yml')
        assert 'targets' in config and 'staging' in config['targets'], "targets/staging.yml missing 'staging' target."

    def test_targets_prod_yml(self):
        assert os.path.isfile('targets/prod.yml'), "targets/prod.yml is missing."
        config = get_yaml('targets/prod.yml')
        assert 'targets' in config and 'prod' in config['targets'], "targets/prod.yml missing 'prod' target."

class TestIncrement3DashboardResources:
    def test_ops_overview_json_exists(self):
        assert os.path.isfile('src/dashboards/ops_overview.json'), "src/dashboards/ops_overview.json is missing."

    def test_dashboards_yml_config(self):
        assert os.path.isfile('resources/dashboards.yml'), "resources/dashboards.yml is missing."
        config = get_yaml('resources/dashboards.yml')
        
        assert 'resources' in config, "resources/dashboards.yml missing 'resources' block."
        assert 'dashboards' in config['resources'], "resources/dashboards.yml missing 'dashboards' block."
        
        dashboards = config['resources']['dashboards']
        assert 'analytics_dashboard' in dashboards, "resources/dashboards.yml missing 'analytics_dashboard'."
        
        dash = dashboards['analytics_dashboard']
        assert dash.get('file_path') == './src/dashboards/ops_overview.json', "Incorrect file_path mapping."
        
        display_name = dash.get('display_name', '')
        assert '${bundle.target}' in display_name, "Dashboard display_name MUST include ${bundle.target} to prevent duplication."
        assert 'access_control_list' in dash or 'access_control' in dash, "Dashboard is missing access controls."

class TestIncrement4TaskfileAbstraction:
    def test_taskfile_exists_and_contains_tasks(self):
        assert os.path.isfile('Taskfile.yml'), "Taskfile.yml is missing."
        config = get_yaml('Taskfile.yml')
        assert 'tasks' in config, "Taskfile.yml missing 'tasks' block."
        
        tasks = config['tasks']
        assert 'validate' in tasks, "Missing 'validate' task."
        assert 'deploy:sandbox' in tasks, "Missing 'deploy:sandbox' task."
        assert 'teardown' in tasks, "Missing 'teardown' task."

class TestIncrement5CICDPipelines:
    def test_github_workflows_exist(self):
        assert os.path.isfile('.github/workflows/deploy-staging.yml'), ".github/workflows/deploy-staging.yml is missing."
        assert os.path.isfile('.github/workflows/deploy-prod.yml'), ".github/workflows/deploy-prod.yml is missing."

    def test_deploy_staging_workflow(self):
        config = get_yaml('.github/workflows/deploy-staging.yml')
        # Check trigger
        assert 'on' in config, "deploy-staging.yml missing 'on' trigger."
        assert 'pull_request' in config['on'], "deploy-staging.yml must trigger on PR."
        
        # Check task validate is run
        jobs_str = yaml.dump(config.get('jobs', {}))
        assert 'task validate' in jobs_str, "deploy-staging.yml MUST run 'task validate'."

    def test_deploy_prod_workflow(self):
        config = get_yaml('.github/workflows/deploy-prod.yml')
        jobs_str = yaml.dump(config.get('jobs', {}))
        assert 'DATABRICKS_HOST' in jobs_str or 'DATABRICKS_TOKEN' in jobs_str, "deploy-prod.yml MUST use secrets for SP authentication."
