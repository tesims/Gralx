from flask_sqlalchemy import SQLAlchemy
import uuid
from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = db.Column(UUID(as_uuid=True), unique=True)
    is_anonymous = db.Column(db.Boolean, default=True)

class Project(db.Model):
    __tablename__ = 'projects'
    project_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    sector = db.Column(db.String(255))
    country = db.Column(db.String(255))
    mask_face = db.Column(db.Boolean, default=False)
    mask_fullbody = db.Column(db.Boolean, default=False)
    mask_logo = db.Column(db.Boolean, default=False)
    mask_location = db.Column(db.Boolean, default=False)
    terms = db.Column(db.Boolean, default=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=True)
    session_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.session_id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Media(db.Model):
    __tablename__ = 'media'
    media_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.project_id'))
    media_type = db.Column(db.String(50))
    original_file_path = db.Column(db.String(255))
    processed_file_path = db.Column(db.String(255))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=True)
    session_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.session_id'), nullable=True)

class PII_Variable(db.Model):
    __tablename__ = 'pii_variables'
    pii_variable_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    media_id = db.Column(UUID(as_uuid=True), db.ForeignKey('media.media_id'))
    variable_type = db.Column(db.String(50))
    original_value = db.Column(db.String(255))
    context = db.Column(db.Text)
    generated_value = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Process_Log(db.Model):
    __tablename__ = 'process_logs'
    log_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    media_id = db.Column(UUID(as_uuid=True), db.ForeignKey('media.media_id'))
    step = db.Column(db.String(255))
    status = db.Column(db.String(50))
    log_details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Context_Analysis(db.Model):
    __tablename__ = 'context_analysis'
    analysis_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pii_variable_id = db.Column(UUID(as_uuid=True), db.ForeignKey('pii_variables.pii_variable_id'))
    llm_type = db.Column(db.String(50))
    context_details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    __tablename__ = 'reports'
    report_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('projects.project_id'))
    media_id = db.Column(UUID(as_uuid=True), db.ForeignKey('media.media_id'))
    report_content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)