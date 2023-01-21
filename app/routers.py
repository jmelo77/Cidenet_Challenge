from typing import List
from . import schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from app.database import get_db
from .utils.service_result import handle_result
from .services.employee import EmployeeService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.GetEmployeeResponse])
async def get_employees(employee: schemas.GetEmployeeSchema=Depends(), db: Session = Depends(get_db), limit: int = 10, offset: int = 0):
    result = EmployeeService(db).get_employees(employee, limit, offset)
    return handle_result(result)


@router.get("/{employee_id}", status_code=status.HTTP_200_OK, response_model=schemas.EmployeeResponse)
async def get_employee(employee_id: int, db: get_db = Depends()):
    result = EmployeeService(db).get_employee(employee_id)
    return handle_result(result)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateEmployeeResponse)
async def create_employee(employee: schemas.CreateEmployeeSchema, db: get_db = Depends()):
    result = EmployeeService(db).create_employee(employee)
    return handle_result(result)


@router.put("/{employee_id}", status_code=status.HTTP_200_OK, response_model=schemas.UpdateEmployeeResponse)
async def update_employee(employee_id: int, employee_updates: schemas.UpdateEmployeeSchema, db: get_db = Depends()):
    result = EmployeeService(db).update_employee(employee_id, employee_updates)
    return handle_result(result)


@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(employee_id: int, db: get_db = Depends()):
    result = EmployeeService(db).delete_employee(employee_id)
    return handle_result(result)

