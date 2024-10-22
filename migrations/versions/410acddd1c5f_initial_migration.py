"""Initial migration

Revision ID: 410acddd1c5f
Revises: 
Create Date: 2024-08-17 23:52:38.571151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '410acddd1c5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('session_id', sa.UUID(), nullable=True),
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('session_id')
    )
    op.create_table('projects',
    sa.Column('project_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('sector', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('mask_face', sa.Boolean(), nullable=True),
    sa.Column('mask_fullbody', sa.Boolean(), nullable=True),
    sa.Column('mask_logo', sa.Boolean(), nullable=True),
    sa.Column('mask_location', sa.Boolean(), nullable=True),
    sa.Column('terms', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('session_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['users.session_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('project_id')
    )
    op.create_table('media',
    sa.Column('media_id', sa.UUID(), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('media_type', sa.String(length=50), nullable=True),
    sa.Column('original_file_path', sa.String(length=255), nullable=True),
    sa.Column('processed_file_path', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('session_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], ),
    sa.ForeignKeyConstraint(['session_id'], ['users.session_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('media_id')
    )
    op.create_table('pii_variables',
    sa.Column('pii_variable_id', sa.UUID(), nullable=False),
    sa.Column('media_id', sa.UUID(), nullable=True),
    sa.Column('variable_type', sa.String(length=50), nullable=True),
    sa.Column('original_value', sa.String(length=255), nullable=True),
    sa.Column('context', sa.Text(), nullable=True),
    sa.Column('generated_value', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['media_id'], ['media.media_id'], ),
    sa.PrimaryKeyConstraint('pii_variable_id')
    )
    op.create_table('process_logs',
    sa.Column('log_id', sa.UUID(), nullable=False),
    sa.Column('media_id', sa.UUID(), nullable=True),
    sa.Column('step', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('log_details', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['media_id'], ['media.media_id'], ),
    sa.PrimaryKeyConstraint('log_id')
    )
    op.create_table('reports',
    sa.Column('report_id', sa.UUID(), nullable=False),
    sa.Column('project_id', sa.UUID(), nullable=True),
    sa.Column('media_id', sa.UUID(), nullable=True),
    sa.Column('report_content', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['media_id'], ['media.media_id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], ),
    sa.PrimaryKeyConstraint('report_id')
    )
    op.create_table('context_analysis',
    sa.Column('analysis_id', sa.UUID(), nullable=False),
    sa.Column('pii_variable_id', sa.UUID(), nullable=True),
    sa.Column('llm_type', sa.String(length=50), nullable=True),
    sa.Column('context_details', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['pii_variable_id'], ['pii_variables.pii_variable_id'], ),
    sa.PrimaryKeyConstraint('analysis_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('context_analysis')
    op.drop_table('reports')
    op.drop_table('process_logs')
    op.drop_table('pii_variables')
    op.drop_table('media')
    op.drop_table('projects')
    op.drop_table('users')
    # ### end Alembic commands ###
