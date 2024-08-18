import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, flash, redirect, url_for, request, session, current_app, send_file
from app.extensions import db
from app.models import User, Project, Media
from app.forms import DashboardForm
import uuid
from app.processing import process_video, process_audio, process_image, process_text

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

@main_bp.route('/project/<uuid:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    media = Media.query.filter_by(project_id=project.project_id).first()
    print(f"Displaying project: {project.name}")
    if media:
        print(f"Associated media: {media.media_type}")
    return render_template('project_detail.html', project=project, media=media)

@main_bp.route('/documentation')
def documentation():
    return render_template('documentation.html', title='Documentation')

@main_bp.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')