
from airflow.www.app import create_app
from flask_appbuilder import AppBuilder
from flask import Flask, request, flash, redirect, url_for
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder.baseviews import BaseView
from flask_appbuilder import expose
from airflow.utils.session import create_session


class CustomApprovalView(BaseView):
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


def init_custom_view(app: Flask):
    appbuilder = AppBuilder(app, session=create_session())
    appbuilder.add_view(
        CustomApprovalView,
        "Approve or Reject",
        icon="fa-check-circle",
        category="Custom",
        category_icon="fa-cogs"
    )
    return app


app = create_app()
app = init_custom_view(app)
