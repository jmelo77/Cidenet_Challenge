from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, constr
from .models import TypeStatus


class IdentificationTypeSchema(BaseModel):
    id: int
    identification_type_code: str
    description: str

    class Config:
        orm_mode = True


class CountrySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class AreaSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True         


class EmployeeResponse(BaseModel):
    id: int
    identification_type: IdentificationTypeSchema
    area: AreaSchema
    surname: str
    second_surname: str
    first_name: str
    other_names: Optional[str] = None
    identification_number: str
    country: CountrySchema
    email: EmailStr
    admission_date: date
    record_date: datetime
    status: TypeStatus

    class Config:
        orm_mode = True


class ListEmployeeResponse(BaseModel):
    status: str
    results: int
    employees: List[EmployeeResponse]


class CreateEmployeeSchema(BaseModel):
    identification_type_id: int
    area_id: int
    surname: constr(regex="^[A-Z ]*$", max_length=20)
    second_surname: constr(regex="^[A-Z ]*$", max_length=20)
    first_name: constr(regex="^[A-Z ]*$", max_length=20)
    other_names: Optional[constr(regex="^[A-Z ]*$", max_length=50)] = None
    identification_number: constr(regex="^[a-zA-Z0-9-]*$", max_length=20)
    country_id: int
    email: Optional[str] = None
    admission_date: date
    record_date: Optional[datetime]
    status: Optional[TypeStatus] = TypeStatus.ACTIVE

    class Config:
        orm_mode = True


class CreateEmployeeResponse(BaseModel):
    id: int
    identification_type_id: int
    area_id: int
    surname: str
    second_surname: str
    first_name: str
    other_names: str
    identification_number: str
    country_id: int
    email: str
    admission_date: date
    record_date: datetime
    status: TypeStatus

    class Config:
        orm_mode = True


class UpdateEmployeeSchema(BaseModel):
    identification_type_id: int
    area_id: int
    surname: constr(regex="^[A-Z ]*$", max_length=20)
    second_surname: constr(regex="^[A-Z ]*$", max_length=20)
    first_name: constr(regex="^[A-Z ]*$", max_length=20)
    other_names: Optional[constr(regex="^[A-Z ]*$", max_length=50)] = None
    identification_number: constr(regex="^[a-zA-Z0-9-]*$", max_length=20)
    country_id: int
    email: Optional[str] = None
    admission_date: date

    class Config:
        orm_mode = True


class UpdateEmployeeResponse(BaseModel):
    id: int
    identification_type_id: int
    area_id: int
    surname: str
    second_surname: str
    first_name: str
    other_names: str
    identification_number: str
    country_id: int
    email: str
    admission_date: date
    record_date: datetime
    status: TypeStatus

    class Config:
        orm_mode = True


class GetEmployeeSchema(BaseModel):
    identification_type_id: Optional[str]
    surname: Optional[str]
    second_surname: Optional[str]
    first_name: Optional[str]
    other_names: Optional[str]
    identification_number: Optional[str]
    country_id: Optional[str]
    email: Optional[str]
    status: Optional[TypeStatus]

    class Config:
        orm_mode = True


class GetEmployeeResponse(BaseModel):
    id: int
    identification_type: IdentificationTypeSchema
    area: AreaSchema
    surname: str
    second_surname: str
    first_name: str
    other_names: str
    identification_number: str
    country: CountrySchema
    email: str
    admission_date: date
    record_date: datetime
    status: TypeStatus

    class Config:
        orm_mode = True