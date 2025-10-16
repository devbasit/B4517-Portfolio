from flask import Flask, render_template, request, redirect, url_for, abort, session, flash
import pandas as pd
import json
import os
import re
import markdown
from functools import wraps

app = Flask(__name__)

# --- Flask Secret Key Configuration ---
# IMPORTANT: In a real environment, this should be a long, random value 
# and stored securely, not hardcoded. This is for demonstration only.
app.config['SECRET_KEY'] = 'your_super_secret_key_for_sessions_12345'
app.config['SESSION_COOKIE_SECURE'] = True  # Recommend using HTTPS in production
app.config['SESSION_COOKIE_HTTPONLY'] = True

# --- Hardcoded Admin Credentials (For single-user CMS) ---
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password123' 

# --- Authentication Decorator ---
def login_required(f):
    """Decorator to ensure user is logged in before accessing a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash("You must be logged in to access the admin panel.", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Configuration and Data Management ---
DATA_FILE = 'portfolio_data.json'
EXCEL_DIR = '.' # Excel files are in the same directory as app.py

def load_portfolio_data():
    """Loads all portfolio content from the JSON file."""
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            if 'projects' not in data:
                 data['projects'] = {}
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Warning: {DATA_FILE} not found or invalid. Initializing empty structure.")
        return {'portfolio_title': 'Dynamic ML Portfolio', 'projects': {'home': {'title': 'Home', 'content': 'Welcome to my dynamic portfolio. Start editing on the /admin page!', 'table_filename': ''}}}

def save_portfolio_data(data):
    """Saves the current portfolio data to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Error saving data to {DATA_FILE}: {e}")

def load_excel_data(filename):
    """Converts an Excel file into a Bootstrap-styled HTML table string."""
    if not filename:
        return ""
    filepath = os.path.join(EXCEL_DIR, filename)
    if not os.path.exists(filepath):
        return f"<div class='alert alert-warning my-3' role='alert'><strong>Table Error:</strong> File '{filename}' not found at {filepath}</div>"
    try:
        df = pd.read_excel(filepath)
        return df.to_html(classes='table table-bordered table-striped table-hover content-table', index=False)
    except Exception as e:
        return f"<div class='alert alert-danger my-3' role='alert'><strong>Table Error:</strong> Could not load data from '{filename}'. Details: {e}</div>"

def generate_slug(title, existing_slugs):
    """Generates a URL-friendly slug, ensuring uniqueness."""
    base_slug = title.lower().replace(' ', '-').replace('/', '-').strip()
    base_slug = re.sub(r'[^\w\-]', '', base_slug)
    slug = base_slug
    i = 1
    # Note: existing_slugs is the entire data dictionary, so we check the 'projects' key
    while slug in existing_slugs.get('projects', {}):
        slug = f"{base_slug}-{i}"
        i += 1
    return slug if slug else f"new-project-{len(existing_slugs.get('projects', {})) + 1}"

def render_dynamic_project(slug):
    """Centralized function to fetch data, convert content, and render the project page."""
    data = load_portfolio_data()
    project = data['projects'].get(slug)

    if not project:
        abort(404)
    
    content_markdown = project.get('content', '') # Use .get for safety
    
    # 1. Replace [TABLE:filename] placeholders with HTML table
    def replace_table_placeholder(match):
        filename = match.group(1).strip()
        return load_excel_data(filename)

    content_markdown_with_tables = re.sub(r'\[TABLE:(.*?)\]', replace_table_placeholder, content_markdown)

    # 2. Convert Markdown to HTML
    content_html = markdown.markdown(content_markdown_with_tables, extensions=['extra'])
    
    # 3. Apply Bootstrap classes to images rendered by Markdown
    content_html = content_html.replace('<img src', '<img class="img-fluid rounded shadow-sm my-4" src')
    
    return render_template('index.html',
        portfolio_title=data.get('portfolio_title', "Dynamic ML Portfolio"),
        content=content_html,
        active_page_slug=slug,
        projects=data['projects'])

# --- Authentication Routes ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles admin login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple hardcoded credential check
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            flash("Logged in successfully!", "success")
            # Redirect to the admin panel after successful login
            return redirect(url_for('admin_redirect'))
        else:
            flash("Invalid credentials. Please try again.", "danger")

    # If GET request or failed POST, show the login form
    return render_template('login.html', portfolio_title=load_portfolio_data().get('portfolio_title', "Dynamic ML Portfolio"))

@app.route('/logout')
def logout():
    """Handles admin logout."""
    session.pop('logged_in', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# --- Public Project Routes (Dynamic) ---

@app.route('/')
def home():
    """Renders the Home project."""
    return render_dynamic_project('home')

@app.route('/project/<slug>')
def dynamic_project_route(slug):
    """Renders any project page based on its unique slug."""
    return render_dynamic_project(slug)

# --- Admin Interface (Now protected) ---

@app.route('/admin')
@login_required # PROTECTION
def admin_redirect():
    """Redirects the main /admin path to the home project editor."""
    return redirect(url_for('admin_edit', slug='home'))

@app.route('/admin/edit/<slug>', methods=['GET', 'POST'])
@login_required # PROTECTION
def admin_edit(slug):
    """Allows editing of an existing project's content."""
    data = load_portfolio_data()
    current_project = data['projects'].get(slug)
    message = request.args.get('message') # Get message passed from redirect/add/delete

    if not current_project:
        abort(404)

    if request.method == 'POST':
        new_title = request.form.get('project_title')
        new_content = request.form.get('project_content')
        new_slug = request.form.get('project_slug')

        if not new_title or not new_content or not new_slug:
            flash("Title, Content, and Slug cannot be empty.", "danger")
        elif new_slug != slug and new_slug in data['projects']:
            flash(f"Slug '{new_slug}' is already in use. Please choose a different one.", "danger")
        else:
            # Handle slug change: delete old entry, create new one
            if new_slug != slug:
                del data['projects'][slug]
                slug = new_slug
                
            current_project['title'] = new_title
            current_project['content'] = new_content
            
            data['portfolio_title'] = request.form.get('portfolio_title', data['portfolio_title'])

            data['projects'][slug] = current_project
            save_portfolio_data(data)
            flash(f"Content for '{new_title}' updated and saved successfully!", "success")
            
            # Redirect to the new slug if it changed
            if new_slug != request.form.get('original_slug'):
                return redirect(url_for('admin_edit', slug=new_slug))

    return render_template('admin.html', 
        data=data, 
        current_slug=slug, 
        current_project=current_project)

@app.route('/admin/add', methods=['POST'])
@login_required # PROTECTION
def admin_add():
    """Creates a new project from the admin panel."""
    data = load_portfolio_data()
    new_title = request.form.get('new_project_title')

    if not new_title:
        flash("Project title cannot be empty.", "danger")
    else:
        new_slug = generate_slug(new_title, data)
        
        if new_slug in data['projects']:
            flash(f"Could not create slug for '{new_title}'. Please try a more unique title.", "danger")
        else:
            data['projects'][new_slug] = {
                'title': new_title,
                'content': f"## {new_title}\n\nThis is the content for your new project. Use **Markdown** to format your text, and use the `[TABLE:filename.xlsx]` tag to embed tables.",
            }
            save_portfolio_data(data)
            flash(f"New project '{new_title}' created successfully!", "success")
            return redirect(url_for('admin_edit', slug=new_slug))

    return redirect(url_for('admin_edit', slug='home')) # Redirect to home edit on failure


@app.route('/admin/delete/<slug>', methods=['POST'])
@login_required # PROTECTION
def admin_delete(slug):
    """Deletes a project."""
    if slug == 'home':
        flash("Cannot delete the mandatory 'Home' project.", "danger")
        return redirect(url_for('admin_edit', slug='home'))

    data = load_portfolio_data()
    if slug in data['projects']:
        title = data['projects'][slug]['title']
        del data['projects'][slug]
        save_portfolio_data(data)
        flash(f"Project '{title}' deleted successfully.", "success")
        return redirect(url_for('admin_edit', slug='home'))
    
    flash(f"Project deletion failed: Slug '{slug}' not found.", "danger")
    return redirect(url_for('admin_edit', slug='home'))


if __name__ == '__main__':
    load_portfolio_data() 
    app.run(debug=True)
