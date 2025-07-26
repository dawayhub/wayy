from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    id:int
    task:str
    done:bool = False


templates = Jinja2Templates(directory="templates")

# Temporary storage for todos (in-memory)
todos: List[dict] = []

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/create-todo")
def create_todo(item: str = Form(...)):
    todos.append({"task": item, "done": False})
    return RedirectResponse("/", status_code=303)

@app.post("/toggle-todo/{id}")
def toggle_todo(id: int):
    if 0 <= id < len(todos):
        todos[id]["done"] = not todos[id]["done"]
    return RedirectResponse("/", status_code=303)

# @app.put("/put-todo/{id}")
# def update_answer(id: int, done: bool = True):
#     if 0 <= id < len(todos):
#         todos[id] = {"task": todos[id]["task"], "done": done}
#         return {"message": "Todo updated successfully"}
#     return {"error": "Invalid ID"}