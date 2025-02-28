from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..models import Project, Skill, Experience, Education, About, Contact
from .. import db
from datetime import datetime
import os
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@bp.route('/about', methods=['GET', 'POST'])
@admin_required
def about():
    about = About.query.first()
    if not about:
        about = About(name='', title='', bio='')
        db.session.add(about)
        db.session.commit()
    
    if request.method == 'POST':
        about.name = request.form.get('name')
        about.title = request.form.get('title')
        about.bio = request.form.get('bio')
        about.github = request.form.get('github')
        about.linkedin = request.form.get('linkedin')
        about.twitter = request.form.get('twitter')
        about.email = request.form.get('email')
        
        db.session.commit()
        flash('About information updated successfully!', 'success')
        return redirect(url_for('admin.about'))
    
    return render_template('admin/about.html', about=about)

@bp.route('/projects')
@admin_required
def projects():
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

@bp.route('/project/add', methods=['GET', 'POST'])
@admin_required
def add_project():
    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            description=request.form.get('description'),
            project_url=request.form.get('project_url'),
            github_url=request.form.get('github_url'),
            technologies=request.form.get('technologies'),
            image_url=request.form.get('image_url')
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html')

@bp.route('/project/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.project_url = request.form.get('project_url')
        project.github_url = request.form.get('github_url')
        project.technologies = request.form.get('technologies')
        project.image_url = request.form.get('image_url')
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/project_form.html', project=project)

@bp.route('/skills')
@admin_required
def skills():
    skills = Skill.query.all()
    return render_template('admin/skills.html', skills=skills)

@bp.route('/skill/add', methods=['GET', 'POST'])
@admin_required
def add_skill():
    if request.method == 'POST':
        skill = Skill(
            name=request.form.get('name'),
            category=request.form.get('category'),
            proficiency=request.form.get('proficiency'),
            icon=request.form.get('icon')
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skill_form.html')

@bp.route('/messages')
@admin_required
def messages():
    messages = Contact.query.order_by(Contact.created_date.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@bp.route('/message/<int:id>')
@admin_required
def view_message(id):
    message = Contact.query.get_or_404(id)
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    return render_template('admin/message_detail.html', message=message) 