from flask import request, flash, redirect, url_for
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from airflow.plugins_manager import AirflowPlugin

# --- Custom Approval View ---
class CustomApprovalView(AppBuilderBaseView):
    default_view = "approve_reject"
    route_base = "/custom"

    @expose('/approve_reject', methods=['GET', 'POST'])
    @has_access
    def approve_reject(self):
        if request.method == 'POST':
            decision = request.form.get('decision')
            if decision == 'approve':
                self.approve_data()
                flash('Data Approved!', 'success')
            elif decision == 'reject':
                self.reject_data()
                flash('Data Rejected!', 'danger')
            return redirect(url_for('CustomApprovalView.approve_reject'))

        return self.render_template('approve_reject.html')

    def approve_data(self):
        print("Approval logic executed.")

    def reject_data(self):
        print("Rejection logic executed.")


# --- Custom Home View ---
class CustomHomeView(AppBuilderBaseView):
    default_view = "index"
    route_base = "/custom_home"

    @expose("/")
    def index(self):
        return self.render_template("custom_home.html")


# --- Register both views via Airflow Plugin ---
class CustomPlugin(AirflowPlugin):
    name = "custom_home_plugin"
    flask_blueprints = []
    appbuilder_views = [
        {
            "name": "Approve or Reject",
            "category": "Custom",
            "view": CustomApprovalView(),
        },
        {
            "name": "Custom Home",
            "category": "Custom",
            "view": CustomHomeView(),
        }
    ]
