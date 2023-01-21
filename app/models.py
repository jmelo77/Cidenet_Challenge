import enum
from .database import Base
from sqlalchemy import TIMESTAMP, Column, Date, ForeignKey, Integer, Enum, String, text, UniqueConstraint
from sqlalchemy.orm import relationship


class TypeStatus(enum.Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class EmailDomain(Base):
    __tablename__ = 'emails_domains'
    id = Column(Integer, primary_key=True)
    domain = Column(String(length=50), nullable=False)
    country = relationship("Country", back_populates="emaildomain", uselist=False)

    def __init__(self, domain):
        self.domain = domain

    def __repr__(self):
        return f'EmailDomain({self.domain})'
    def __str__(self):
        return self.domain


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    email_domain_id = Column(Integer, ForeignKey("emails_domains.id"))
    emaildomain = relationship("EmailDomain", back_populates="country")
    employees = relationship("Employee")

    def __init__(self, name, email_domain_id):
        self.name = name
        self.email_domain_id = email_domain_id

    def __repr__(self):
        return f'Country({self.name}, {self.email_domain_id})'
    def __str__(self):
        return self.name


class IdentificationType(Base):
    __tablename__ = 'identification_types'
    id = Column(Integer, primary_key=True)
    identification_type_code = Column(String(length=2), nullable=False)
    description = Column(String(length=50), nullable=False)
    employees = relationship("Employee")

    def __init__(self, identification_type_code, description):
        self.identification_type_code = identification_type_code
        self.description = description

    def __repr__(self):
        return f'IdentificationType({self.identification_type_code}, {self.description})'
    def __str__(self):
        return self.description


class Area(Base):
    __tablename__ = 'areas'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    employees = relationship("Employee")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Areas({self.name})'
    def __str__(self):
        return self.name


class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        UniqueConstraint('identification_type_id', 'identification_number', name='uc_identification_type_id_identification_number'),
    )
    id = Column(Integer, primary_key=True)
    identification_type_id = Column(Integer, ForeignKey("identification_types.id", ondelete='CASCADE'))
    area_id = Column(Integer, ForeignKey("areas.id", ondelete='CASCADE'))
    surname = Column(String(length=20), nullable=False)
    second_surname = Column(String(length=20), nullable=False)
    first_name = Column(String(length=20), nullable=False)
    other_names = Column(String(length=50), nullable=True, default='')
    identification_number = Column(String(length=20), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete='CASCADE'))
    email = Column(String(length=300), unique=True, nullable=True, default='')
    admission_date = Column(Date(), nullable=False)
    record_date = Column(TIMESTAMP(timezone=True),
                        nullable=True, server_default=text("now()"))
    status = Column(Enum(TypeStatus), nullable=True, server_default="ACTIVE")

    area = relationship("Area", back_populates="employees")
    country = relationship("Country", back_populates="employees")
    identification_type = relationship("IdentificationType", back_populates="employees")


    def __init__(self, area_id, identification_type_id, surname, second_surname, first_name, other_names, identification_number, country_id, email, admission_date, record_date, status):
        self.area_id = area_id
        self.identification_type_id = identification_type_id
        self.surname = surname
        self.second_surname = second_surname
        self.first_name = first_name
        self.other_names = other_names
        self.identification_number = identification_number
        self.country_id = country_id
        self.email = email
        self.admission_date = admission_date
        self.record_date = record_date
        self.status = status

    def __repr__(self):
        return f'Employee({self.surname}, {self.second_surname}, {self.first_name})'
    def __str__(self):
        return f'Employee({self.surname}, {self.second_surname}, {self.first_name})'