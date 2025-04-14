from flask import Blueprint, redirect, render_template
from flask_login import current_user
from airflow.plugins_manager import AirflowPlugin

# Create a new Flask blueprint
custom_home_bp = Blueprint(
    "custom_home", __name__,
    template_folder="templates",
    static_folder="static"
)

# Redirect based on role
@custom_home_bp.route('/')
def role_based_home():
    if not current_user.is_authenticated:
        return redirect('/login/')

    roles = [role.name for role in current_user.roles]

    if "DataAnalyst" in roles:
        return redirect('/home-analyst')
    elif "OpsUser" in roles:
        return redirect('/home-ops')
    elif "Public" in roles:
        return redirect('/public-home')
    else:
        return redirect('/home')  # default Airflow UI

# Analyst homepage route
@custom_home_bp.route('/home-analyst')
def home_analyst():
    return render_template("home_analyst.html", user=current_user)

# Ops homepage route
@custom_home_bp.route('/home-ops')
def home_ops():
    return render_template("home_ops.html", user=current_user)

# Ops homepage route
@custom_home_bp.route('/public-home')
def public_home():
    return render_template("public_home.html", user=current_user)


# Register plugin
class CustomHomePlugin(AirflowPlugin):
    name = "custom_home_plugin"
    flask_blueprints = [custom_home_bp]
