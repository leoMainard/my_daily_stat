"""add_password_hash_to_users

Revision ID: daac39656bee
Revises: 4d0e0bc02193
Create Date: 2026-05-22 00:26:12.672517

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "daac39656bee"
down_revision: Union[str, Sequence[str], None] = "4d0e0bc02193"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    user_role = sa.Enum("ADMIN", "USER", name="user_role")
    user_role.create(op.get_bind(), checkfirst=True)

    op.drop_table("user_infos")
    op.add_column(
        "users",
        sa.Column(
            "firstname", sa.String(length=100), nullable=False, server_default=""
        ),
    )
    op.add_column(
        "users",
        sa.Column("lastname", sa.String(length=100), nullable=False, server_default=""),
    )
    op.add_column(
        "users",
        sa.Column(
            "password_hash", sa.String(length=255), nullable=False, server_default=""
        ),
    )
    op.alter_column("users", "role", server_default=None)
    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(length=50),
        type_=user_role,
        existing_nullable=False,
        postgresql_using="UPPER(role)::user_role",
    )
    op.alter_column("users", "role", server_default="USER")
    op.drop_column("users", "name")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "name",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
            server_default="",
        ),
    )
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("ADMIN", "USER", name="user_role"),
        type_=sa.VARCHAR(length=50),
        existing_nullable=False,
        existing_server_default=sa.text("'user'::character varying"),
        postgresql_using="role::varchar",
    )
    op.drop_column("users", "password_hash")
    op.drop_column("users", "lastname")
    op.drop_column("users", "firstname")

    sa.Enum(name="user_role").drop(op.get_bind(), checkfirst=True)
    op.create_table(
        "user_infos",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "tags",
            postgresql.JSON(astext_type=sa.Text()),
            server_default=sa.text("'[]'::json"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("user_infos_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("user_infos_pkey")),
        sa.UniqueConstraint(
            "user_id",
            name=op.f("user_infos_user_id_key"),
            postgresql_include=[],
            postgresql_nulls_not_distinct=False,
        ),
    )
    # ### end Alembic commands ###
