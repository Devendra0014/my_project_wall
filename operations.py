# ✅ Final cleaned operations.py using Blueprint for all project routes
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from flask_login import login_required, current_user
from models import Project, User
from datetime import datetime

ops_bp = Blueprint('ops', __name__)

# ✅ Dashboard
@ops_bp.route('/dashboard')
@login_required
def dashboard():
    projects = Project.select().where(Project.user == current_user.id)
    return render_template('dashboard.html', projects=projects)

# ✅ profile
@ops_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.dob = request.form['dob']
        user.program = request.form['program']
        user.course = request.form['course']
        user.save()
        flash("✅ Profile updated successfully!", "success")
        return redirect('/dashboard')
    return render_template("profile.html", user=user)

# ✅ Public_profile
@ops_bp.route('/user/<username>')
def public_profile(username):
    user = User.get_or_none(User.username == username)
    if not user:
        return "User not found", 404
    projects = Project.select().where(Project.user == user)
    return render_template('public_profile.html', user=user, projects=projects)



# ✅ Add Project
@ops_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        Project.create(
            title=request.form['title'],
            description=request.form['description'],
            github_url=request.form.get('github', ''),
            tech_stack=request.form.get('tech', ''),
            team_members=request.form.get('team_members', ''),
            created_at=datetime.now(),
            user=current_user.id
        )
        flash("Project added successfully!", "success")
        return redirect('/dashboard')
    return render_template('add_edit.html', project=None)

# ✅ Edit Project
@ops_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.get_or_none(Project.id == id, Project.user == current_user.id)
    if not project:
        return "Not found", 404

    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.github_url = request.form.get('github', '')
        project.tech_stack = request.form.get('tech', '')
        project.team_members = request.form.get('team_members', '')
        project.save()
        flash("Project updated successfully!", "success")
        return redirect('/dashboard')

    return render_template('add_edit.html', project=project)

# ✅ Delete Project
@ops_bp.route('/delete/<int:id>')
@login_required
def delete_project(id):
    project = Project.get_or_none(Project.id == id, Project.user == current_user.id)
    if project:
        project.delete_instance()
        flash("Project deleted successfully!", "info")
    return redirect('/dashboard')

# ✅ Toggle Favorite
@ops_bp.route('/toggle-favorite/<int:id>')
@login_required
def toggle_favorite(id):
    project = Project.get_or_none(Project.id == id, Project.user == current_user.id)
    if project:
        project.is_favorite = not project.is_favorite
        project.save()
    return redirect('/dashboard')

