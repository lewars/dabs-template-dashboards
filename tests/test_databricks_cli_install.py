import os
import yaml
import pytest

def get_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

class TestDatabricksCliInstallTask:
    def test_install_task_exists(self):
        """Test that the 'install' task exists in Taskfile.yml and executes the setup script."""
        assert os.path.isfile('Taskfile.yml'), "Taskfile.yml is missing."
        config = get_yaml('Taskfile.yml')
        
        assert 'tasks' in config, "Taskfile.yml missing 'tasks' block."
        tasks = config['tasks']
        assert 'install' in tasks, "Missing 'install' task in Taskfile.yml."
        
        install_task = tasks['install']
        assert 'cmds' in install_task, "'install' task missing 'cmds' list."
        
        # Verify it actually calls the databricks setup script
        cmds_str = " ".join(install_task['cmds'])
        assert 'curl' in cmds_str, "Install task should use curl to fetch the databricks setup script."
        assert 'setup.sh' in cmds_str, "Install task should execute the databricks setup script."

    def test_staging_workflow_executes_install_task(self):
        """Test that deploy-staging.yml calls 'task install' before running databricks commands."""
        workflow_path = '.github/workflows/deploy-staging.yml'
        assert os.path.isfile(workflow_path), f"{workflow_path} is missing."
        config = get_yaml(workflow_path)
        
        jobs = config.get('jobs', {})
        assert 'validate_and_deploy' in jobs, "Staging workflow missing 'validate_and_deploy' job."
        
        steps = jobs['validate_and_deploy'].get('steps', [])
        
        install_step_index = -1
        validate_step_index = -1
        
        for idx, step in enumerate(steps):
            run_cmd = step.get('run', '')
            if 'task install' in run_cmd:
                install_step_index = idx
            if 'task validate' in run_cmd or 'databricks bundle deploy' in run_cmd:
                if validate_step_index == -1:
                    validate_step_index = idx
                    
        assert install_step_index != -1, "Staging workflow does not execute 'task install'."
        assert install_step_index < validate_step_index, "Staging workflow must execute 'task install' BEFORE 'task validate' or deploy."

    def test_prod_workflow_executes_install_task(self):
        """Test that deploy-prod.yml calls 'task install' before running databricks commands."""
        workflow_path = '.github/workflows/deploy-prod.yml'
        assert os.path.isfile(workflow_path), f"{workflow_path} is missing."
        config = get_yaml(workflow_path)
        
        jobs = config.get('jobs', {})
        assert 'deploy_prod' in jobs, "Prod workflow missing 'deploy_prod' job."
        
        steps = jobs['deploy_prod'].get('steps', [])
        
        install_step_index = -1
        deploy_step_index = -1
        
        for idx, step in enumerate(steps):
            run_cmd = step.get('run', '')
            if 'task install' in run_cmd:
                install_step_index = idx
            if 'databricks bundle deploy' in run_cmd:
                deploy_step_index = idx
                
        assert install_step_index != -1, "Prod workflow does not execute 'task install'."
        assert install_step_index < deploy_step_index, "Prod workflow must execute 'task install' BEFORE deployment."
