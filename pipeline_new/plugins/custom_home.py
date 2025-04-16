# # # # # # # # from flask import Blueprint, redirect, render_template, request, url_for
# # # # # # # # from flask_login import current_user
# # # # # # # # from airflow.plugins_manager import AirflowPlugin
# # # # # # # # from airflow.utils.log.logging_mixin import LoggingMixin
# # # # # # # # import logging

# # # # # # # # log = logging.getLogger(__name__)
# # # # # # # # log.warning("🔥🔥🔥 custom_home plugin loaded 🔥🔥🔥")


# # # # # # # # # Setup logger
# # # # # # # # log = LoggingMixin().log

# # # # # # # # # Create a new Flask blueprint
# # # # # # # # custom_home_bp = Blueprint(
# # # # # # # #     "custom_home", __name__,
# # # # # # # #     url_prefix="/custom",  # <== important
# # # # # # # #     template_folder="templates",
# # # # # # # #     static_folder="static"
# # # # # # # # )

# # # # # # # # @custom_home_bp.route('/')
# # # # # # # # def test_custom_home():
# # # # # # # #     from airflow.utils.log.logging_mixin import LoggingMixin
# # # # # # # #     log = LoggingMixin().log
# # # # # # # #     log.warning("🔥 Route '/custom/' hit!")

# # # # # # # #     return "✅ Custom home route is working!"


# # # # # # # # # Redirect based on role
# # # # # # # # @custom_home_bp.route('/')
# # # # # # # # def role_based_home():
# # # # # # # #     log.info("👀 Entered role_based_home route")

# # # # # # # #     if not current_user.is_authenticated:
# # # # # # # #         log.info("🔒 User not authenticated — redirecting to login")
# # # # # # # #         return redirect('/login/')

# # # # # # # #     roles = [role.name for role in current_user.roles]
# # # # # # # #     log.info(f"🔍 Authenticated user: {current_user.username}, Roles: {roles}")

# # # # # # # #     if "DataAnalyst" in roles:
# # # # # # # #         return redirect("/home-analyst")
# # # # # # # #     elif "OpsUser" in roles:
# # # # # # # #         return redirect("/home-ops")
# # # # # # # #     elif "Public" in roles:
# # # # # # # #         return redirect("/public-home")
# # # # # # # #     else:
# # # # # # # #         return redirect("/home")

# # # # # # # # # Define pages
# # # # # # # # @custom_home_bp.route('/home-analyst')
# # # # # # # # def home_analyst():
# # # # # # # #     log.info(f"📊 Rendering Analyst Home for user: {current_user.username}")
# # # # # # # #     return render_template("home_analyst.html", user=current_user)

# # # # # # # # @custom_home_bp.route('/home-ops')
# # # # # # # # def home_ops():
# # # # # # # #     log.info(f"⚙️ Rendering Ops Home for user: {current_user.username}")
# # # # # # # #     return render_template("home_ops.html", user=current_user)

# # # # # # # # @custom_home_bp.route('/public-home')
# # # # # # # # def public_home():
# # # # # # # #     log.info(f"🌐 Rendering Public Home for user: {current_user.username}")
# # # # # # # #     return render_template("public_home.html", user=current_user)

# # # # # # # # # Plugin registration
# # # # # # # # class CustomHomePlugin(AirflowPlugin):
# # # # # # # #     name = "custom_home_plugin"
# # # # # # # #     flask_blueprints = [custom_home_bp]

# # # # # # # # plugins/custom_home.py

# # # # # # # import logging
# # # # # # # from flask import Blueprint, render_template_string
# # # # # # # from airflow.plugins_manager import AirflowPlugin

# # # # # # # # Set a debug log to confirm load
# # # # # # # log = logging.getLogger(__name__)
# # # # # # # log.warning("🔥 custom_home plugin loaded")

# # # # # # # # Define the blueprint with url_prefix
# # # # # # # custom_home_bp = Blueprint(
# # # # # # #     "custom_home", __name__,
# # # # # # #     url_prefix="/custom"
# # # # # # # )

# # # # # # # @custom_home_bp.route('/')
# # # # # # # def custom_home():
# # # # # # #     return render_template_string("<h1>🎯 Hello from custom_home!</h1>")

# # # # # # # # Register plugin
# # # # # # # class CustomHomePlugin(AirflowPlugin):
# # # # # # #     name = "custom_home_plugin"
# # # # # # #     flask_blueprints = [custom_home_bp]


# # # # # # # # just temporarily for debugging
# # # # # # # # hit http://localhost:8080/custom/debug_routes
# # # # # # # from flask import current_app

# # # # # # # @custom_home_bp.route('/debug_routes')
# # # # # # # def debug_routes():
# # # # # # #     output = []
# # # # # # #     for rule in current_app.url_map.iter_rules():
# # # # # # #         output.append(f"{rule.endpoint}: {rule.rule}")
# # # # # # #     return "<br>".join(output)

# # # # # # from flask import Blueprint, redirect, render_template, request, url_for, current_app
# # # # # # from flask_login import current_user
# # # # # # from airflow.plugins_manager import AirflowPlugin

# # # # # # import logging
# # # # # # log = logging.getLogger(__name__)
# # # # # # log.warning("🔥 custom_home plugin loaded")

# # # # # # # Create blueprint
# # # # # # custom_home_bp = Blueprint(
# # # # # #     "custom_home", __name__,
# # # # # #     url_prefix="/custom",
# # # # # #     template_folder="templates",
# # # # # #     static_folder="static"
# # # # # # )

# # # # # # @custom_home_bp.route("/")
# # # # # # def role_based_home():
# # # # # #     log.warning("✅ /custom/ hit")
# # # # # #     if not current_user.is_authenticated:
# # # # # #         return redirect('/login/')
# # # # # #     roles = [r.name for r in current_user.roles]
# # # # # #     log.warning(f"User roles: {roles}")
# # # # # #     if "DataAnalyst" in roles:
# # # # # #         return redirect("/home-analyst")
# # # # # #     elif "OpsUser" in roles:
# # # # # #         return redirect("/home-ops")
# # # # # #     elif "Public" in roles:
# # # # # #         return redirect("/public-home")
# # # # # #     return redirect("/home")

# # # # # # @custom_home_bp.route("/debug_routes")
# # # # # # def debug_routes():
# # # # # #     return "<br>".join([str(rule) for rule in current_app.url_map.iter_rules()])

# # # # # # # Plugin that attaches the blueprint to the app manually
# # # # # # class CustomHomePlugin(AirflowPlugin):
# # # # # #     name = "custom_home_plugin"

# # # # # #     def on_load(self, app):
# # # # # #         log.warning("📌 Registering blueprint with app")
# # # # # #         app.register_blueprint(custom_home_bp)

# # # # # from flask import redirect, render_template, request, url_for
# # # # # from flask_login import current_user
# # # # # from flask_appbuilder import BaseView as AppBuilderBaseView, expose
# # # # # from airflow.plugins_manager import AirflowPlugin
# # # # # import logging

# # # # # log = logging.getLogger(__name__)
# # # # # log.warning("🔥 custom_home plugin loaded")

# # # # # class CustomHomeView(AppBuilderBaseView):
# # # # #     route_base = "/custom"

# # # # #     @expose("/")
# # # # #     def role_based_home(self):
# # # # #         log.warning("✅ /custom/ hit")
# # # # #         if not current_user.is_authenticated:
# # # # #             return redirect("/login/")

# # # # #         roles = [r.name for r in current_user.roles]
# # # # #         log.warning(f"User roles: {roles}")

# # # # #         if "DataAnalyst" in roles:
# # # # #             return redirect("/custom/home-analyst")
# # # # #         elif "OpsUser" in roles:
# # # # #             return redirect("/custom/home-ops")
# # # # #         elif "Public" in roles:
# # # # #             return redirect("/custom/public-home")
# # # # #         return redirect("/home")

# # # # #     @expose("/home-analyst")
# # # # #     def home_analyst(self):
# # # # #         return self.render_template("home_analyst.html", user=current_user)

# # # # #     @expose("/home-ops")
# # # # #     def home_ops(self):
# # # # #         return self.render_template("home_ops.html", user=current_user)

# # # # #     @expose("/public-home")
# # # # #     def public_home(self):
# # # # #         return self.render_template("public_home.html", user=current_user)

# # # # # # Register with Airflow's AppBuilder
# # # # # class CustomHomePlugin(AirflowPlugin):
# # # # #     name = "custom_home_plugin"
# # # # #     appbuilder_views = [
# # # # #         {
# # # # #             "name": "Custom Home",
# # # # #             "category": "Custom",
# # # # #             "view": CustomHomeView()
# # # # #         }
# # # # #     ]

# # # # from airflow.plugins_manager import AirflowPlugin
# # # # from flask_appbuilder import BaseView as AppBuilderBaseView, expose
# # # # from flask_login import current_user

# # # # class CustomHomeView(AppBuilderBaseView):
# # # #     default_view = "index"

# # # #     @expose('/')
# # # #     def index(self):
# # # #         roles = [role.name for role in current_user.roles]
# # # #         if "DataAnalyst" in roles:
# # # #             return self.render_template("home_analyst.html", user=current_user)
# # # #         elif "OpsUser" in roles:
# # # #             return self.render_template("home_ops.html", user=current_user)
# # # #         elif "Public" in roles:
# # # #             return self.render_template("public_home.html", user=current_user)
# # # #         else:
# # # #             return self.render_template("default_home.html", user=current_user)

# # # # class CustomHomePlugin(AirflowPlugin):
# # # #     name = "custom_home_plugin"
# # # #     appbuilder_views = [
# # # #         {
# # # #             "name": "Custom Home",
# # # #             "category": "Custom",
# # # #             "view": CustomHomeView(),
# # # #         }
# # # #     ]


# # # from airflow.plugins_manager import AirflowPlugin
# # # from flask_appbuilder import BaseView as AppBuilderBaseView, expose
# # # from flask_login import current_user


# # # class CustomHomeView(AppBuilderBaseView):
# # #     default_view = "index"
# # #     route_base = "/custom"  # This makes it accessible via /custom/

# # #     @expose("/")
# # #     def index(self):
# # #         return self.render_template("home_analyst.html", user=current_user)


# # # class CustomHomePlugin(AirflowPlugin):
# # #     name = "custom_home_plugin"
# # #     appbuilder_views = [
# # #         {
# # #             "name": "Custom Home",
# # #             "category": "Custom",
# # #             "view": CustomHomeView(),
# # #         }
# # #     ]

# # from airflow.plugins_manager import AirflowPlugin
# # from flask_appbuilder import BaseView as AppBuilderBaseView, expose
# # from flask_login import current_user

# # class HelloView(AppBuilderBaseView):
# #     route_base = "/hello"  # ⬅️ The URL will be /hello/

# #     @expose("/")
# #     def hello(self):
# #         return self.render_template("home_analyst.html", user=current_user)

# # class HelloPlugin(AirflowPlugin):
# #     name = "hello_plugin"
# #     appbuilder_views = [
# #         {
# #             "name": "Hello Dashboard",
# #             "category": "Custom",
# #             "view": HelloView()
# #         }
# #     ]

from airflow.plugins_manager import AirflowPlugin
from flask_appbuilder import BaseView as AppBuilderBaseView, expose
from flask_login import current_user
import os

class HelloView(AppBuilderBaseView):
    route_base = "/hello"
    template_folder = os.path.join(os.path.dirname(__file__), "custom_home", "templates")

    @expose("/")
    def role_based_home(self):
        if not current_user.is_authenticated:
            # log.info("🔒 User not authenticated — redirecting to login")
            return self.redirect('/login/')        
        # return self.render_template("home_analyst.html", user=current_user)

        elif current_user.is_authenticated:
            roles = [role.name for role in current_user.roles]

            if "DataAnalyst" in roles:
                return self.render_template("home_analyst.html", user=current_user)
            elif "OpsUser" in roles:
                return self.render_template("home_ops.html", user=current_user)
            elif "Public" in roles:
                return self.render_template("public_home.html", user=current_user)
            else:
                return self.render_template("default_home.html", user=current_user)

class HelloPlugin(AirflowPlugin):
    name = "hello_plugin"
    appbuilder_views = [
        {
            "name": "Hello Dashboard",
            "category": "Custom",
            "view": HelloView()
        }
    ]


# from airflow.plugins_manager import AirflowPlugin
# from flask_appbuilder import BaseView as AppBuilderBaseView, expose
# from flask_login import current_user
# import os

# class CustomHomeView(AppBuilderBaseView):
#     route_base = "/hello"  # This sets the base URL to /hello
#     template_folder = os.path.join(os.path.dirname(__file__), "custom_home", "templates")

#     @expose("/")
#     def role_based_home(self):
#         if not current_user.is_authenticated:
#             return self.render_template("default_home.html", user=current_user)

#         roles = [role.name for role in current_user.roles]

#         if "DataAnalyst" in roles:
#             return self.render_template("home_analyst.html", user=current_user)
#         elif "OpsUser" in roles:
#             return self.render_template("home_ops.html", user=current_user)
#         elif "Public" in roles:
#             return self.render_template("public_home.html", user=current_user)
#         else:
#             return self.render_template("default_home.html", user=current_user)

# class CustomHomePlugin(AirflowPlugin):
#     name = "custom_home_plugin"
#     appbuilder_views = [
#         {
#             "name": "Hello",
#             "category": "Custom",
#             "view": CustomHomeView(),
#         }
#     ]
