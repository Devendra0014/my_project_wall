from flask import Flask,render_template,redirect,flash,request,url_for
from flask_login import LoginManager
from models import db, initialize_db, User
from auth import auth_bp
from operations import ops_bp

app = Flask(__name__)
app.secret_key = "your_secret_key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

initialize_db()

app.register_blueprint(auth_bp)
app.register_blueprint(ops_bp)


@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == int(user_id))


@app.route('/')
def home():
    return render_template('home.html', show_footer=True)

# ✅ search 
@app.route('/user-search')
def user_search():
    username = request.args.get('username')
    if not username:
        flash("Please enter a username", "warning")
        return redirect('/')
    
    user = User.get_or_none(User.username == username)
    if user:
        return redirect(url_for('ops.public_profile', username=user.username))  # ✅ Blueprint-aware
    else:
        flash("User not found", "danger")
        return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)
