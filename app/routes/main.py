from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
from ..models import Project, Skill, Experience, Education, Contact, About
from .. import db, mail

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    about = About.query.first()
    projects = Project.query.order_by(Project.created_date.desc()).all()
    skills = Skill.query.all()
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    education = Education.query.order_by(Education.start_date.desc()).all()
    return render_template('main/index.html',
                         about=about,
                         projects=projects,
                         skills=skills,
                         experiences=experiences,
                         education=education)

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('main.contact'))
        
        # Save contact message to database
        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(contact)
        
        # Send email notification
        try:
            about = About.query.first()
            if about and about.email:
                msg = Message(
                    subject=f"New Contact Form Submission: {subject}",
                    sender=email,
                    recipients=[about.email],
                    body=f"From: {name} <{email}>\n\n{message}"
                )
                mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")
        
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('main/contact.html')

@bp.route('/projects')
def projects():
    projects = Project.query.order_by(Project.created_date.desc()).all()
    return render_template('main/projects.html', projects=projects)

@bp.route('/project/<int:id>')
def project_detail(id):
    project = Project.query.get_or_404(id)
    return render_template('main/project_detail.html', project=project) 