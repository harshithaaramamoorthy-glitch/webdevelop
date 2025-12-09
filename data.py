from fastapi import FastAPI 
from pydantic import BaseModel 
from typing import List 
from emp import get_database_connection 
 
app = FastAPI() 
 
class User(BaseModel): 
    name: str 
    email: str 
 
# CREATE 
@app.post("/users") 
async def create_user(user: User): 
    connection = get_database_connection() 
    cursor = connection.cursor() 
    query = "INSERT INTO users (name,email) VALUES (%s,%s)" 
    values = (user.name, user.email) 
    cursor.execute(query, values) 
    connection.commit() 
    connection.close() 
    return {"message": "User created successfully"} 
 
# READ (all) 
@app.get("/users") 
async def read_users(): 
    connection = get_database_connection() 
    cursor = connection.cursor() 
    query = "SELECT * FROM users" 
    cursor.execute(query) 
    users = cursor.fetchall() 
    connection.close() 
    return users 
 
# READ (single) 
@app.get("/users/{user_id}") 
async def read_user(user_id: int): 
    connection = get_database_connection() 
    cursor = connection.cursor() 
    query = "SELECT * FROM users WHERE id = %s" 
    values = (user_id,) 
    cursor.execute(query, values) 
    user = cursor.fetchone() 
    connection.close() 
    return user 
 
# UPDATE 
@app.put("/users/{user_id}") 
async def update_user(user_id: int, user: User): 
    connection = get_database_connection() 
    cursor = connection.cursor() 
    query = "UPDATE users SET name = %s, email = %s WHERE id = %s" 
    values = (user.name, user.email, user_id) 
    cursor.execute(query, values) 
    connection.commit() 
    connection.close() 
    return {"message": "User updated successfully"} 
# DELETE 
@app.delete("/users/{user_id}") 
async def delete_user(user_id: int): 
    connection = get_database_connection() 
    cursor = connection.cursor() 
    query = "DELETE FROM users WHERE id = %s" 
    values = (user_id,) 
    cursor.execute(query, values) 
    connection.commit() 
    connection.close() 
    return {"message": "User deleted successfully"}