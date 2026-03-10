"""
Workflow Automation & Data Pipeline Engine
Schedule jobs, automate tasks, and orchestrate data workflows
"""

import json
import os
from datetime import datetime, timedelta
import pandas as pd


class WorkflowEngine:
    """
    Manage and execute data workflows
    """
    
    def __init__(self, workflows_dir='data/workflows'):
        self.workflows_dir = workflows_dir
        os.makedirs(workflows_dir, exist_ok=True)
        self.workflows = {}
        self.load_workflows()
    
    def load_workflows(self):
        """Load saved workflows from disk"""
        if os.path.exists(self.workflows_dir):
            for file in os.listdir(self.workflows_dir):
                if file.endswith('.json'):
                    with open(os.path.join(self.workflows_dir, file), 'r') as f:
                        workflow = json.load(f)
                        self.workflows[workflow['id']] = workflow
    
    def create_workflow(self, name, description, steps):
        """
        Create a new workflow
        
        Args:
            name: Workflow name
            description: Description
            steps: List of step dictionaries with 'type' and 'config'
        """
        workflow_id = f"wf_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        workflow = {
            'id': workflow_id,
            'name': name,
            'description': description,
            'steps': steps,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        self.workflows[workflow_id] = workflow
        self.save_workflow(workflow)
        
        return workflow_id
    
    def save_workflow(self, workflow):
        """Save workflow to disk"""
        filepath = os.path.join(self.workflows_dir, f"{workflow['id']}.json")
        with open(filepath, 'w') as f:
            json.dump(workflow, f, indent=2)
    
    def execute_workflow(self, workflow_id, input_data=None):
        """
        Execute a workflow
        
        Returns:
            dict: Execution results
        """
        if workflow_id not in self.workflows:
            return {'error': 'Workflow not found'}
        
        workflow = self.workflows[workflow_id]
        results = {
            'workflow_id': workflow_id,
            'started_at': datetime.now().isoformat(),
            'steps_completed': [],
            'status': 'running'
        }
        
        current_data = input_data
        
        try:
            for idx, step in enumerate(workflow['steps']):
                step_result = self.execute_step(step, current_data)
                
                results['steps_completed'].append({
                    'step_number': idx + 1,
                    'step_type': step['type'],
                    'status': 'success' if not step_result.get('error') else 'failed',
                    'output': step_result
                })
                
                if step_result.get('error'):
                    results['status'] = 'failed'
                    results['error'] = step_result['error']
                    break
                
                current_data = step_result.get('data', current_data)
            
            if results['status'] == 'running':
                results['status'] = 'completed'
            
            results['completed_at'] = datetime.now().isoformat()
            results['final_output'] = current_data
            
        except Exception as e:
            results['status'] = 'failed'
            results['error'] = str(e)
        
        return results
    
    def execute_step(self, step, input_data):
        """Execute a single workflow step"""
        step_type = step['type']
        config = step.get('config', {})
        
        try:
            if step_type == 'load_data':
                # Load data from file
                filepath = config.get('filepath')
                if filepath.endswith('.csv'):
                    data = pd.read_csv(filepath)
                elif filepath.endswith('.xlsx'):
                    data = pd.read_excel(filepath)
                else:
                    return {'error': 'Unsupported file type'}
                
                return {'data': data, 'message': f'Loaded {len(data)} rows'}
            
            elif step_type == 'filter_data':
                # Filter data based on condition
                column = config.get('column')
                operator = config.get('operator', '==')
                value = config.get('value')
                
                if operator == '==':
                    filtered = input_data[input_data[column] == value]
                elif operator == '>':
                    filtered = input_data[input_data[column] > value]
                elif operator == '<':
                    filtered = input_data[input_data[column] < value]
                else:
                    filtered = input_data
                
                return {'data': filtered, 'message': f'Filtered to {len(filtered)} rows'}
            
            elif step_type == 'aggregate':
                # Aggregate data
                group_by = config.get('group_by')
                agg_func = config.get('function', 'count')
                agg_column = config.get('column')
                
                if agg_func == 'count':
                    result = input_data.groupby(group_by).size().reset_index(name='count')
                elif agg_func == 'sum':
                    result = input_data.groupby(group_by)[agg_column].sum().reset_index()
                elif agg_func == 'mean':
                    result = input_data.groupby(group_by)[agg_column].mean().reset_index()
                else:
                    result = input_data
                
                return {'data': result, 'message': 'Aggregation complete'}
            
            elif step_type == 'save_data':
                # Save data to file
                filepath = config.get('filepath')
                
                if filepath.endswith('.csv'):
                    input_data.to_csv(filepath, index=False)
                elif filepath.endswith('.xlsx'):
                    input_data.to_excel(filepath, index=False)
                
                return {'data': input_data, 'message': f'Saved to {filepath}'}
            
            elif step_type == 'transform':
                # Apply transformation
                transform_type = config.get('transform_type')
                column = config.get('column')
                
                if transform_type == 'uppercase':
                    input_data[column] = input_data[column].str.upper()
                elif transform_type == 'lowercase':
                    input_data[column] = input_data[column].str.lower()
                elif transform_type == 'fill_na':
                    fill_value = config.get('fill_value', 0)
                    input_data[column] = input_data[column].fillna(fill_value)
                
                return {'data': input_data, 'message': 'Transformation applied'}
            
            else:
                return {'error': f'Unknown step type: {step_type}'}
        
        except Exception as e:
            return {'error': str(e)}
    
    def list_workflows(self):
        """List all workflows"""
        return [
            {
                'id': wf['id'],
                'name': wf['name'],
                'description': wf['description'],
                'steps_count': len(wf['steps']),
                'created_at': wf['created_at']
            }
            for wf in self.workflows.values()
        ]
    
    def delete_workflow(self, workflow_id):
        """Delete a workflow"""
        if workflow_id in self.workflows:
            filepath = os.path.join(self.workflows_dir, f"{workflow_id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
            del self.workflows[workflow_id]
            return True
        return False


class ScheduledJob:
    """
    Represent a scheduled job
    """
    
    def __init__(self, job_id, workflow_id, schedule_type, schedule_config):
        self.job_id = job_id
        self.workflow_id = workflow_id
        self.schedule_type = schedule_type  # 'daily', 'weekly', 'monthly', 'cron'
        self.schedule_config = schedule_config
        self.last_run = None
        self.next_run = self.calculate_next_run()
        self.enabled = True
    
    def calculate_next_run(self):
        """Calculate next run time based on schedule"""
        now = datetime.now()
        
        if self.schedule_type == 'daily':
            hour = self.schedule_config.get('hour', 0)
            minute = self.schedule_config.get('minute', 0)
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            if next_run <= now:
                next_run += timedelta(days=1)
            
            return next_run
        
        elif self.schedule_type == 'weekly':
            # Simplified weekly scheduling
            return now + timedelta(days=7)
        
        elif self.schedule_type == 'hourly':
            return now + timedelta(hours=1)
        
        else:
            return now + timedelta(days=1)
    
    def should_run(self):
        """Check if job should run now"""
        if not self.enabled:
            return False
        
        return datetime.now() >= self.next_run
    
    def mark_completed(self):
        """Mark job as completed and calculate next run"""
        self.last_run = datetime.now()
        self.next_run = self.calculate_next_run()


class JobScheduler:
    """
    Manage scheduled jobs
    """
    
    def __init__(self, jobs_dir='data/jobs'):
        self.jobs_dir = jobs_dir
        os.makedirs(jobs_dir, exist_ok=True)
        self.jobs = {}
        self.load_jobs()
    
    def load_jobs(self):
        """Load saved jobs"""
        if os.path.exists(self.jobs_dir):
            for file in os.listdir(self.jobs_dir):
                if file.endswith('.json'):
                    with open(os.path.join(self.jobs_dir, file), 'r') as f:
                        job_data = json.load(f)
                        job = ScheduledJob(
                            job_data['job_id'],
                            job_data['workflow_id'],
                            job_data['schedule_type'],
                            job_data['schedule_config']
                        )
                        job.enabled = job_data.get('enabled', True)
                        self.jobs[job.job_id] = job
    
    def create_job(self, workflow_id, schedule_type, schedule_config):
        """Create a new scheduled job"""
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        job = ScheduledJob(job_id, workflow_id, schedule_type, schedule_config)
        self.jobs[job_id] = job
        self.save_job(job)
        return job_id
    
    def save_job(self, job):
        """Save job to disk"""
        filepath = os.path.join(self.jobs_dir, f"{job.job_id}.json")
        job_data = {
            'job_id': job.job_id,
            'workflow_id': job.workflow_id,
            'schedule_type': job.schedule_type,
            'schedule_config': job.schedule_config,
            'enabled': job.enabled,
            'last_run': job.last_run.isoformat() if job.last_run else None,
            'next_run': job.next_run.isoformat() if job.next_run else None
        }
        
        with open(filepath, 'w') as f:
            json.dump(job_data, f, indent=2)
    
    def list_jobs(self):
        """List all jobs"""
        return [
            {
                'job_id': job.job_id,
                'workflow_id': job.workflow_id,
                'schedule_type': job.schedule_type,
                'enabled': job.enabled,
                'last_run': job.last_run.isoformat() if job.last_run else 'Never',
                'next_run': job.next_run.isoformat() if job.next_run else 'N/A'
            }
            for job in self.jobs.values()
        ]
    
    def get_pending_jobs(self):
        """Get jobs that should run now"""
        return [job for job in self.jobs.values() if job.should_run()]
