# tasks.py
from celery import Celery
from pathlib import Path
import os

# Initialize Celery
celery = Celery('tasks')


def init_celery(app):
    """Initialize Celery with Flask app config"""
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        task_serializer='json',
        result_serializer='json',
        accept_content=['json'],
        timezone='UTC',
        enable_utc=True,
    )
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery


@celery.task(bind=True, name='tasks.process_upload')
def process_upload(self, user_id, filepath, file_type):
    """
    Asynchronously process uploaded file
    This is a placeholder for the actual processing logic
    """
    try:
        # Update task state
        self.update_state(state='PROCESSING', meta={'status': 'Processing file...'})
        
        # Simulate processing (replace with actual logic from upload_routes.py)
        import time
        time.sleep(2)  # Simulate processing time
        
        # Return result
        return {
            'status': 'completed',
            'user_id': user_id,
            'filepath': str(filepath),
            'file_type': file_type
        }
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise


@celery.task(name='tasks.generate_summary')
def generate_summary(text_content):
    """
    Asynchronously generate summary using Ollama
    """
    from summarize_utils import summarize_with_ollama
    try:
        summary = summarize_with_ollama(text_content)
        return {'status': 'success', 'summary': summary}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


@celery.task(name='tasks.cleanup_old_uploads')
def cleanup_old_uploads(days=7):
    """
    Periodically clean up old upload files
    """
    from datetime import datetime, timedelta
    import shutil
    
    base_dir = Path(__file__).resolve().parent
    upload_folder = base_dir / "uploads"
    cutoff_date = datetime.now() - timedelta(days=days)
    
    cleaned = 0
    for folder in upload_folder.iterdir():
        if folder.is_dir():
            folder_time = datetime.fromtimestamp(folder.stat().st_mtime)
            if folder_time < cutoff_date:
                shutil.rmtree(folder)
                cleaned += 1
    
    return {'status': 'success', 'cleaned_folders': cleaned}
