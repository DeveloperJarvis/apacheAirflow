from airflow.www.security import AirflowSecurityManager
from flask_appbuilder.security.sqla.models import Role, User
from flask_appbuilder.security.manager import AUTH_DB
from airflow import settings
from airflow.models import DagModel

def create_roles():
    from flask_appbuilder.security.sqla.manager import SecurityManager
    sm = SecurityManager()
    session = settings.Session()

    # Create or get Public role
    public_role = sm.find_role("Public") or sm.add_role("Public")
    
    # Create or get Business Analyst role
    ba_role = sm.find_role("Business Analyst") or sm.add_role("Business Analyst")

    # Give access to view and interact with a specific DAG
    ba_permissions = [
        ("can_dag_read", "DAG:approval_workflow"),
        ("can_dag_edit", "DAG:approval_workflow"),
    ]
    for perm, view_menu in ba_permissions:
        sm.add_permission_role(ba_role, sm.find_permission_view_menu(perm, view_menu))

    # Create test user with Public role
    if not sm.find_user(username="test_user"):
        sm.add_user(
            username="test_user",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            role=public_role,
            password="test123"
        )

    session.commit()

create_roles()
