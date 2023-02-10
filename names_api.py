from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from manage_db import Database

app = FastAPI()
load_dotenv()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class NameItem(BaseModel):
    name_value: str


# Create db object
db = Database(getenv("DATABASE"))


@app.get("/", response_class=HTMLResponse)
def main_page(request: Request) -> object:
    return templates.TemplateResponse("main_page.html", {"request": request})


@app.post("/")
def get_name_info(request: Request, name=Form(...)) -> object:
    data_name = db.get_name_row_by_value(name.capitalize().rstrip())
    n, origin, meaning = data_name
    single_name_values = {'name': n, 'origin_value': origin, 'meaning_value': meaning}
    return templates.TemplateResponse("name_info.html", {"request": request, "name": single_name_values})


@app.get("/names/table", response_class=HTMLResponse)
def get_table_names(request: Request) -> object:
    """By declaring response_class=HTMLResponse
     the docs UI will be able to know that the response will be HTML."""
    db_names = db.get_just_list_name()
    return templates.TemplateResponse("table_names.html", {"request": request, "names": db_names})


@app.get("/name/{item_id}")
def get_name_by_id(request: Request, item_id: int) -> object:
    data_name = db.get_name_by_id(item_id)
    name = data_name[0]
    origin = data_name[1]
    meaning = data_name[2]
    single_name_values = {'name': name, 'origin_value': origin, 'meaning_value': meaning}
    return templates.TemplateResponse("name_info.html", {"request": request, "name": single_name_values})


@app.get("/names/{amount}", response_class=HTMLResponse)
def get_table_names_amount(request: Request, amount: int) -> object:
    names_amount = db.get_specific_amount_of_names(amount)
    return templates.TemplateResponse("table_names.html", {"request": request, "names": names_amount})


if __name__ == '__main__':
    uvicorn.run("names_api:app", host='127.0.0.1', reload=True)
