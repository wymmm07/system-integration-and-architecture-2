from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Data model using Pydantic
class GaisanoEmployeeCreate(BaseModel):
    name: str
    position: str
    department: str
    store_location: str

class GaisanoEmployee(GaisanoEmployeeCreate):
    id: int

# Database connection setup
def create_connection():
    connection = sqlite3.connect("gaisano_employees.db")
    return connection

# Create table if not exists
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gaisano_employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT NOT NULL,
        department TEXT NOT NULL,
        store_location TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

create_table()

# CRUD functions
def create_gaisano_employee(employee: GaisanoEmployeeCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO gaisano_employees (name, position, department, store_location) VALUES (?, ?, ?, ?)",
                   (employee.name, employee.position, employee.department, employee.store_location))
    connection.commit()
    employee_id = cursor.lastrowid
    connection.close()
    return employee_id

def read_gaisano_employees():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM gaisano_employees")
    employees = cursor.fetchall()
    connection.close()
    return [GaisanoEmployee(id=row[0], name=row[1], position=row[2], department=row[3], store_location=row[4]) for row in employees]

def read_gaisano_employee(employee_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM gaisano_employees WHERE id=?", (employee_id,))
    employee = cursor.fetchone()
    connection.close()
    if employee:
        return GaisanoEmployee(id=employee[0], name=employee[1], position=employee[2], department=employee[3], store_location=employee[4])
    raise HTTPException(status_code=404, detail="Gaisano employee not found")

def update_gaisano_employee(employee_id: int, updated_employee: GaisanoEmployeeCreate):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE gaisano_employees SET name=?, position=?, department=?, store_location=? WHERE id=?",
                   (updated_employee.name, updated_employee.position, updated_employee.department, updated_employee.store_location, employee_id))
    connection.commit()
    connection.close()
    return {"message": "Gaisano employee updated successfully"}

def delete_gaisano_employee(employee_id: int):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM gaisano_employees WHERE id=?", (employee_id,))
    connection.commit()
    connection.close()
    return {"message": "Gaisano employee deleted successfully"}

# FastAPI endpoints
@app.post("/gaisano-employees/", response_model=GaisanoEmployee)
def create_gaisano_employee_endpoint(employee: GaisanoEmployeeCreate):
    employee_id = create_gaisano_employee(employee)
    return {"id": employee_id, **employee.dict()}

@app.get("/gaisano-employees/", response_model=List[GaisanoEmployee])
def read_gaisano_employees_endpoint():
    return read_gaisano_employees()

@app.get("/gaisano-employees/{employee_id}", response_model=GaisanoEmployee)
def read_gaisano_employee_endpoint(employee_id: int):
    return read_gaisano_employee(employee_id)

@app.put("/gaisano-employees/{employee_id}")
def update_gaisano_employee_endpoint(employee_id: int, updated_employee: GaisanoEmployeeCreate):
    return update_gaisano_employee(employee_id, updated_employee)

@app.delete("/gaisano-employees/{employee_id}")
def delete_gaisano_employee_endpoint(employee_id: int):
    return delete_gaisano_employee(employee_id)
