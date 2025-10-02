# api/upload_api.py
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage

from auth_utils import get_user_by_id

ns = Namespace('upload', description='File upload and processing operations')

# Models
upload_parser = ns.parser()
upload_parser.add_argument('files', location='files', type=FileStorage, required=True, action='append', help='Files to upload')

upload_response_model = ns.model('UploadResponse', {
    'message': fields.String(description='Status message'),
    'upload_id': fields.String(description='Upload ID'),
    'page_count': fields.Integer(description='Number of pages processed'),
    'price': fields.Float(description='Processing price'),
    'download_url': fields.String(description='Download URL for processed file'),
    'status': fields.String(description='Processing status')
})

task_status_model = ns.model('TaskStatus', {
    'task_id': fields.String(description='Task ID'),
    'status': fields.String(description='Task status'),
    'result': fields.Raw(description='Task result if completed')
})


@ns.route('/')
class Upload(Resource):
    @ns.doc('upload_files')
    @ns.expect(upload_parser)
    @ns.marshal_with(upload_response_model, code=202)
    @ns.response(400, 'Bad Request')
    @ns.response(413, 'File too large')
    @jwt_required()
    def post(self):
        """Upload files for processing"""
        from werkzeug.utils import secure_filename
        from pathlib import Path
        from datetime import datetime
        import os
        import uuid
        from config import Config
        from models import UploadRecord, uploads_db
        
        identity = get_jwt_identity()
        user = get_user_by_id(identity)
        
        if not user:
            ns.abort(404, 'User not found')
        
        # Check uploaded files
        uploaded_files = request.files.getlist('files')
        if not uploaded_files or uploaded_files[0].filename == '':
            ns.abort(400, 'No files uploaded')
        
        # Create upload record
        upload_id = str(uuid.uuid4())
        user_folder = Config.UPLOAD_FOLDER / upload_id
        user_folder.mkdir(parents=True, exist_ok=True)
        
        total_size_mb = 0
        page_count = 0
        
        for file in uploaded_files:
            filename = secure_filename(file.filename)
            if not filename:
                continue
            
            # Check file extension
            ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
            if ext not in Config.ALLOWED_EXTENSIONS:
                continue
            
            filepath = user_folder / filename
            file.save(filepath)
            
            file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
            total_size_mb += file_size_mb
            
            if total_size_mb > Config.MAX_TOTAL_SIZE_MB:
                import shutil
                shutil.rmtree(user_folder)
                ns.abort(413, f'Total file size exceeds {Config.MAX_TOTAL_SIZE_MB}MB limit')
            
            # Estimate page count (simplified)
            page_count += 1
        
        # Create upload record
        upload_record = UploadRecord(
            id=upload_id,
            user_id=user.id,
            filename=f"upload_{upload_id}",
            file_type='multi',
            page_count=page_count,
            status='completed',  # Simplified - no async processing for now
            created_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
            download_url=f"/api/v1/upload/{upload_id}/download"
        )
        
        uploads_db[upload_id] = upload_record
        
        return {
            'message': 'Files uploaded successfully',
            'upload_id': upload_id,
            'page_count': page_count,
            'price': round(page_count * 0.1, 2),
            'download_url': upload_record.download_url,
            'status': 'completed'
        }, 202


@ns.route('/<string:upload_id>')
@ns.param('upload_id', 'The upload identifier')
class UploadStatus(Resource):
    @ns.doc('get_upload_status')
    @ns.marshal_with(upload_response_model)
    @jwt_required()
    def get(self, upload_id):
        """Get upload processing status"""
        from models import uploads_db
        
        upload_record = uploads_db.get(upload_id)
        if not upload_record:
            ns.abort(404, 'Upload not found')
        
        identity = get_jwt_identity()
        if upload_record.user_id != identity:
            ns.abort(403, 'Access denied')
        
        return {
            'message': 'Upload status',
            'upload_id': upload_record.id,
            'page_count': upload_record.page_count,
            'price': round(upload_record.page_count * 0.1, 2),
            'download_url': upload_record.download_url,
            'status': upload_record.status
        }
