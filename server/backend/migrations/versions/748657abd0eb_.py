"""empty message

Revision ID: 748657abd0eb
Revises: 5220721a4beb
Create Date: 2025-10-11 09:36:41.424756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '748657abd0eb'
down_revision: Union[str, Sequence[str], None] = '5220721a4beb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # --- Roles ---
    roles_table = sa.table(
        "roles",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("description", sa.String),
    )

    op.bulk_insert(
        roles_table,
        [
            {"id": 1, "name": "Doctor", "description": "Doctors role"},
            {"id": 2, "name": "User", "description": "Users role"},
        ],
    )

    # --- Permissions ---
    permissions_table = sa.table(
        "permissions",
        sa.column("id", sa.Integer),
        sa.column("code", sa.String),
        sa.column("name", sa.String),
        sa.column("description", sa.String),
    )

    op.bulk_insert(
        permissions_table,
        [
            {
                "id": 1,
                "code": "pages.doctor",
                "name": "Видит страницу доктора",
                "description": "",
            }
        ],
    )

    # --- Role-Permissions ---
    role_permissions_table = sa.table(
        "role_permissions",
        sa.column("role_id", sa.Integer),
        sa.column("permission_id", sa.Integer),
    )

    op.bulk_insert(
        role_permissions_table,
        [{"role_id": 1, "permission_id": 1}],
    )

    user_table = sa.table(
        'users', 
        sa.column('login'),
        sa.column('name'),
        sa.column('email'),
        sa.column('password'),
        sa.column('role_id'))
    
    op.bulk_insert(
        user_table,
        [{"login": 'psycho_doctor', "name": 'psycho_doctor', "email": 'doctor@gmail.com', 'password':'password123', 'role_id':1},
         {"login": 'user', "name": 'Login', "email": 'login@gmail.com', 'password':'password', 'role_id':2}],
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.text("DELETE FROM role_permissions WHERE role_id = 1 AND permission_id = 1"))
    op.execute(sa.text("DELETE FROM permissions WHERE id = 1"))
    op.execute(sa.text("DELETE FROM roles WHERE id IN (1, 2)"))
    op.execute(sa.text("DELETE FROM users WHERE id IN (1, 2)"))