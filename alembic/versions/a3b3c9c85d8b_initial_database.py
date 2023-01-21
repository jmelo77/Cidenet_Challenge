"""initial_database

Revision ID: a3b3c9c85d8b
Revises: 
Create Date: 2022-12-31 01:42:53.459059

"""
from alembic import op
import sqlalchemy as sa
from app.models import EmailDomain, Country, IdentificationType, Area


# revision identifiers, used by Alembic.
revision = 'a3b3c9c85d8b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('areas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('emails_domains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('identification_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identification_type_code', sa.String(length=2), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('countries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email_domain_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['email_domain_id'], ['emails_domains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employees',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identification_type_id', sa.Integer(), nullable=True),
    sa.Column('area_id', sa.Integer(), nullable=True),
    sa.Column('surname', sa.String(length=20), nullable=False),
    sa.Column('second_surname', sa.String(length=20), nullable=False),
    sa.Column('first_name', sa.String(length=20), nullable=False),
    sa.Column('other_names', sa.String(length=50), nullable=True),
    sa.Column('identification_number', sa.String(length=20), nullable=False),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=300), nullable=True),
    sa.Column('admission_date', sa.Date(), nullable=False),
    sa.Column('record_date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', name='typestatus'), server_default='ACTIVE', nullable=True),
    sa.ForeignKeyConstraint(['area_id'], ['areas.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['country_id'], ['countries.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['identification_type_id'], ['identification_types.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('identification_type_id', 'identification_number', name='uc_identification_type_id_identification_number')
    )
    op.bulk_insert(EmailDomain.__table__,
    [   
        {
        'id': 1,
        'domain':'cidenet.com.co'
        },
        {
        'id': 2,
        'domain':'cidenet.com.us'
        }
    ])
    op.bulk_insert(Country.__table__,
    [   
        {
        'id': 1,
        'name':'Colombia',
        'email_domain_id': 1
        },
        {
        'id': 2,
        'name':'Estados Unidos',
        'email_domain_id': 2
        }
    ])
    op.bulk_insert(IdentificationType.__table__,
    [   
        {
        'id': 1,
        'identification_type_code':'CC',
        'description':'Cédula de Ciudadanía'
        },
        {
        'id': 2,
        'identification_type_code':'CE',
        'description':'Cédula de Extranjería'
        },
        {
        'id': 3,
        'identification_type_code':'PA',
        'description':'Pasaporte'
        },
        {
        'id': 4,
        'identification_type_code':'PE',
        'description':'Permiso Especial'
        }
    ])
    op.bulk_insert(Area.__table__,
    [   
        {
        'id': 1,
        'name':'Administración'
        },
        {
        'id': 2,
        'name':'Financiera'
        },
        {
        'id': 3,
        'name':'Compras'
        },
        {
        'id': 4,
        'name':'Infraestructura'
        },
        {
        'id': 5,
        'name':'Operación'
        },
        {
        'id': 6,
        'name':'Talento Humano'
        },
        {
        'id': 7,
        'name':'Servicios Varios'
        }
    ])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employees')
    op.drop_table('countries')
    op.drop_table('identification_types')
    op.drop_table('emails_domains')
    op.drop_table('areas')
    # ### end Alembic commands ###
