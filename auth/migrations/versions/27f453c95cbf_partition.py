"""Partition

Revision ID: 27f453c95cbf
Revises: 11acaa37e50b
Create Date: 2022-03-23 07:02:58.059475

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "27f453c95cbf"
down_revision = "11acaa37e50b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "role", ["id"])
    op.create_unique_constraint(None, "social_account", ["id"])
    op.create_unique_constraint(None, "success_history", ["id", "platform"])
    op.create_unique_constraint(None, "user", ["id"])
    op.create_unique_constraint(None, "user_role", ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user_role", type_="unique")
    op.drop_constraint(None, "user", type_="unique")
    op.drop_constraint(None, "success_history", type_="unique")
    op.drop_constraint(None, "social_account", type_="unique")
    op.drop_constraint(None, "role", type_="unique")
    # ### end Alembic commands ###