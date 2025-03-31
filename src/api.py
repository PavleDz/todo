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


@api.get("/todos", response_model=List[Todo])
async def get_todos():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/todos")
        if res.status_code == 200:
            return res.json()
        return JSONResponse(content={"error": "Unable to fetch todos"}, status_code=res.status_code)


@api.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/todos/{todo_id}")
        if res.status_code == 200:
            return res.json()
        return JSONResponse(content={"error": "Todo not found"}, status_code=404)


@api.post("/todos", response_model=Todo, status_code=201)
async def create_todo(new_todo: Todo):
    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/todos", json=new_todo.dict())
        if res.status_code == 201:
            return res.json()
        return JSONResponse(
            content={
                "error": "Failed to create todo. Note: my-json-server is read-only."},
            status_code=res.status_code
        )


@api.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, updated_todo: Todo):
    async with httpx.AsyncClient() as client:
        res = await client.put(f"{BASE_URL}/todos/{todo_id}", json=updated_todo.dict())
        if res.status_code == 200:
            return res.json()
        return JSONResponse(
            content={
                "error": "Failed to update todo. Note: my-json-server is read-only."},
            status_code=res.status_code
        )


@api.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.delete(f"{BASE_URL}/todos/{todo_id}")
        if res.status_code == 200:
            return {"detail": "Todo deleted"}
        return JSONResponse(
            content={
                "error": "Failed to delete todo. Note: my-json-server is read-only."},
            status_code=res.status_code
        )

if __name__ == "__main__":
    uvicorn.run("api:api", reload=True)
