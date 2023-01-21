from app.schemas import (CreateEmployeeSchema,
                        GetEmployeeSchema,
                        UpdateEmployeeResponse,
                        UpdateEmployeeSchema)
from ..utils.app_exceptions import AppException
from sqlalchemy import func
from .main import AppService, AppCRUD
from app.models import Country, Employee, EmailDomain
from ..utils.service_result import ServiceResult
from fastapi import HTTPException


class EmployeeService(AppService):
    def get_employees(self, employee: GetEmployeeSchema, limit, offset) -> ServiceResult:
        emp = EmployeeCRUD(self.db).get_employees(employee=employee, limit=limit, offset=offset)
        return ServiceResult(emp)

    def get_employee(self, employee_id: int) -> ServiceResult:
        emp = EmployeeCRUD(self.db).get_employee(employee_id)
        if not emp:
            return ServiceResult(AppException.EmployeeGet({"employee_id": employee_id}))
        return ServiceResult(emp)

    def create_employee(self, employee: CreateEmployeeSchema) -> ServiceResult:
        emp = EmployeeCRUD(self.db).create_employee(employee)
        if not emp:
            return ServiceResult(AppException.EmployeeCreate())
        return ServiceResult(emp)

    def update_employee(self, employee_id: int, employee: UpdateEmployeeSchema) -> ServiceResult:
        emp = EmployeeCRUD(self.db).get_employee(employee_id)
        if not emp:
            return ServiceResult(AppException.EmployeeGet({"employee_id": employee_id}))
        emp_update = EmployeeCRUD(self.db).update_employee(emp=emp, employee=employee)
        return ServiceResult(emp_update)

    def delete_employee(self, employee_id: int) -> ServiceResult:
        emp = EmployeeCRUD(self.db).delete_employee(employee_id)
        return ServiceResult(emp)


class EmployeeCRUD(AppCRUD):
    def get_employees(self, employee: GetEmployeeSchema, limit, offset) -> Employee:
        query = self.db.query(Employee)
        if employee.first_name is not None and len(employee.first_name) != 0:
            query = query.filter(Employee.first_name == employee.first_name.upper())
        if employee.other_names is not None and len(employee.other_names) != 0:
            query = query.filter(Employee.other_names == employee.other_names.upper())
        if employee.surname is not None and len(employee.surname) != 0:
            query = query.filter(Employee.surname == employee.surname.upper())
        if employee.second_surname is not None and len(employee.second_surname) != 0:
            query = query.filter(Employee.second_surname == employee.second_surname.upper())
        if employee.identification_type_id is not None and len(employee.identification_type_id) != 0:
            query = query.filter(Employee.identification_type_id == employee.identification_type_id)
        if employee.identification_number is not None and len(employee.identification_number) != 0:
            query = query.filter(Employee.identification_number == employee.identification_number.upper())
        if employee.country_id is not None and len(employee.country_id) != 0:
            query = query.filter(Employee.country_id == employee.country_id)
        if employee.email is not None and len(employee.email) != 0:
            query = query.filter(Employee.email == employee.email.lower())
        if employee.status is not None or employee.status == 'active' or employee.status == 'inactive':
            query = query.filter(Employee.status == employee.status)
        result = query.offset(offset).limit(limit).all()
        return result

    def get_employee(self, employee_id: int) -> Employee:
        result = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Employee not found")

    def create_employee(self, employee: CreateEmployeeSchema) -> Employee:
        exist = False
        employee.identification_number = employee.identification_number.upper()
        result = self.db.query(Country).filter(Country.id == employee.country_id)
        for row in result:
            email_domain_id = row.email_domain_id
        result = self.db.query(EmailDomain).filter(EmailDomain.id == email_domain_id)
        for row in result:
            domain = row.domain
        email = employee.first_name.lower().replace(" ", "")+'.'+employee.surname.lower().replace(" ", "")+'@'+domain
        result = self.db.query(Employee).filter(Employee.email == email)
        for row in result:
            exist = True
        if not exist:
            employee.email = email
        else:
            result = self.db.query(func.max(Employee.id)).first()
            employee.email = employee.first_name.lower().replace(" ", "")+'.'+employee.surname.lower().replace(" ", "")+'.'+str(result[0] + 1)+'@'+domain
        emp = Employee(**employee.dict())
        self.db.add(emp)
        self.db.commit()
        self.db.refresh(emp)
        return emp

    def update_employee(self, emp: UpdateEmployeeResponse, employee: UpdateEmployeeSchema) -> Employee:
        result = self.db.query(Employee).filter(Employee.id == emp.id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        exist = False
        employee.identification_number = employee.identification_number.upper()
        result = self.db.query(Country).filter(Country.id == employee.country_id)
        for row in result:
            email_domain_id = row.email_domain_id
        result = self.db.query(EmailDomain).filter(EmailDomain.id == email_domain_id)
        for row in result:
            domain = row.domain
        email = employee.first_name.lower().replace(" ", "")+'.'+employee.surname.lower().replace(" ", "")+'@'+domain
        if email != emp.email:
            result = self.db.query(Employee).filter(Employee.email == email)
            for row in result:
                exist = True
            if not exist:
                emp.email = email
            else:
                result = self.db.query(func.max(Employee.id)).first()
                emp.email = employee.first_name.lower().replace(" ", "")+'.'+employee.surname.lower().replace(" ", "")+'.'+str(result[0] + 1)+'@'+domain
        emp.identification_type_id = employee.identification_type_id
        emp.area_id = employee.area_id
        emp.surname = employee.surname
        emp.second_surname = employee.second_surname
        emp.first_name = employee.first_name
        emp.other_names = employee.other_names
        emp.identification_number = employee.identification_number
        emp.country_id = employee.country_id
        emp.admission_date = employee.admission_date
        self.db.add(emp)
        self.db.commit()
        self.db.refresh(emp)
        return emp

    def delete_employee(self, employee_id: int) -> Employee:
        result = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Employee not found")
        self.db.delete(result)
        self.db.commit()
        return {"detail": f"Employee with employee_id={employee_id} has been deleted successfully"}
