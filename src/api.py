import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
from fastapi.responses import JSONResponse

api = FastAPI()

origins = [
    "http://localhost:5173",
]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://my-json-server.typicode.com/PavleDz/todo"


class Todo(BaseModel):
    id: int
    text: str


@api.get("/todos")
async def get_todos():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/todos")
        if res.status_code == 200:
            return res.json()
        return JSONResponse(content={"error": "Unable to fetch todos"}, status_code=404)


@api.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/todos/{todo_id}")
        if res.status_code == 200:
            return res.json()
        return JSONResponse(content={"error": "Todo not found"}, status_code=404)


@api.post("/todos")
async def create_todo(new_todo: Todo):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/todos", json=new_todo.dict())
        if res.status_code == 201:
            return res.json()
        return JSONResponse(
            content={
                "error": "Failed to create todo"},
            status_code=400
        )


@api.put("/todos/{todo_id}")
async def update_todo(todo_id: int, updated_todo: Todo):
    async with httpx.AsyncClient() as client:
        res = await client.put(f"{BASE_URL}/todos/{todo_id}", json=updated_todo.dict())
        if res.status_code == 200:
            return res.json()
        return JSONResponse(
            content={
                "error": "Failed to update todo."},
            status_code=403
        )


@api.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.delete(f"{BASE_URL}/todos/{todo_id}")
        if res.status_code == 200:
            return {"detail": "Todo deleted"}
        return JSONResponse(
            content={
                "error": "Failed to delete todo."},
            status_code=403
        )

if __name__ == "__main__":
    uvicorn.run("api:api", reload=True)
