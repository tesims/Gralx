import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, flash, redirect, url_for, request, session, current_app, send_file, send_from_directory
from app.extensions import db
from app.models import User, Project, Media
from app.forms import DashboardForm
from app.processor.main_processor import *
import uuid
from flask import jsonify
from app.utils.pii_detector import detect_pii_in_text, get_anonymized_text
from app.utils.context_analyzer import get_context_characteristics, generate_pii_replacement
from app.utils.mask_generator import generate_text_mask
from app.models import PII_Variable, Context_Analysis, Process_Log, Report
from flask import render_template, jsonify, current_app
import traceback

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = DashboardForm()
    if form.validate_on_submit():
        if not form.terms.data:
            flash('You must accept the terms and conditions.', 'error')
            return render_template('dashboard.html', title='Dashboard', form=form)

        try:
            # Get or create user based on session
            user = User.query.filter_by(session_id=session.get('session_id')).first()
            if not user:
                user = User(session_id=uuid.uuid4(), is_anonymous=True)
                db.session.add(user)
                db.session.commit()  # Commit the user to the database

            # Create new project
            project = Project(
                name=form.project_name.data,
                description=form.prompt.data,
                user_id=user.user_id if not user.is_anonymous else None,
                session_id=user.session_id if user.is_anonymous else None,
                sector=form.sector.data,
                country=form.country.data
            )
            db.session.add(project)
            db.session.commit()  # Commit the project to the database

            # Handle file upload based on upload_type
            upload_type = form.upload_type.data
            file = getattr(form, upload_type).data

            if not file:
                raise ValueError(f"No file uploaded for {upload_type}")

            filename = secure_filename(file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER')
            if not upload_folder:
                raise ValueError("UPLOAD_FOLDER not configured")

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            media = Media(
                project_id=project.project_id,
                user_id=user.user_id if not user.is_anonymous else None,
                session_id=user.session_id if user.is_anonymous else None,
                media_type=upload_type,
                original_file_path=file_path
            )
            db.session.add(media)
            db.session.commit()  # Commit the media to the database

            flash('Your project has been created!', 'success')
            return redirect(url_for('main.project_detail', project_id=project.project_id))

        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating your project.', 'error')
            current_app.logger.error(f"Error in dashboard: {str(e)}")

    return render_template('dashboard.html', title='Dashboard', form=form)

@main_bp.route('/documentation')
def documentation():
    return render_template('documentation.html', title='Documentation')

@main_bp.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')



@main_bp.route('/project/<uuid:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    media = Media.query.filter_by(project_id=project.project_id).first()
    return render_template('project_detail.html', project=project, media=media)

@main_bp.route('/process/<uuid:project_id>', methods=['POST'])
def process_project(project_id):
    try:
        project = Project.query.get_or_404(project_id)
        
        # Hardcoded transcript
        transcript = "Patient John Doe, age 47, presents with symptoms of hypertension. He has been prescribed Lisinopril 10 mg daily, with a follow-up scheduled in two nweeks. His previous address was in the downtown area near Elm Street, but he recently moved to a residential neighborhood near Maple Avenue in Springfield."
        
        current_app.logger.info(f"Processing project: {project.name}")
        current_app.logger.info(f"Transcript: {transcript}")
        
        # Check if the audio file exists
        audio_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'test_audio3.mp3')
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
        
        return jsonify({
            'status': 'success',
            'transcript': transcript,
            'audio_url': url_for('main.download_audio', filename='test_audio3.mp3')
        })
    except Exception as e:
        current_app.logger.error(f"Error processing project: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@main_bp.route('/download_audio')
def download_audio():
    # Direct path to the file
    file_path = "/Users/academics/Documents/graxl/graxl-2/app/uploads"
    filename = "test_audio3.mp3"
    return send_from_directory(file_path, filename, as_attachment=True)
