from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class DashboardForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired()])
    sector = SelectField('Sector', choices=[
        ('autonomous_vehicles', 'Autonomous Vehicles'),
        ('healthcare', 'Healthcare'),
        ('service', 'Retail and Customer Service'),
        ('smart_home', 'Security Systems'),
        ('smart_home', 'Smart Home Systems'),
        ('education', 'Education and Training'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    country = SelectField('Country', choices=[
        ('us', 'United States'),
        ('ca', 'Canada'),
        ('uk', 'United Kingdom'),
        ('au', 'Australia'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    mask_face = BooleanField('Face')
    mask_fullbody = BooleanField('Full-body')
    mask_logo = BooleanField('Logo')
    mask_location = BooleanField('Location')
    prompt = TextAreaField('Prompt', validators=[DataRequired()])
    upload_type = SelectField('What type of file will you be uploading?', choices=[
        ('none', 'Upload Type'),
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('image', 'Image'),
        ('video', 'Video')
    ], validators=[DataRequired()])
    audio = FileField('Upload Audio (Accepted formats: .mp3, .wav)')
    text = FileField('Upload Text File (Accepted formats: .txt, .csv, .json)')
    image = FileField('Upload Image (Accepted formats: .jpeg, .png)')
    video = FileField('Upload Video (Accepted formats: .mp4, .mov)')
    terms = BooleanField('I have read and accept the terms and conditions')
    submit = SubmitField('Submit')