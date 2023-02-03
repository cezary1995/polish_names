from os import getenv

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
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


@app.get("/names/table", response_class=HTMLResponse)
def get_table_names(request: Request) -> object:
    """By declaring response_class=HTMLResponse
     the docs UI will be able to know that the response will be HTML."""
    db_names = db.get_just_list_name()
    return templates.TemplateResponse("table_names.html", {"request": request, "names": db_names})


@app.get("/names/list", response_class=HTMLResponse)
def get_list_names(request: Request) -> object:
    """By declaring response_class=HTMLResponse
     the docs UI will be able to know that the response will be HTML."""
    db_names = db.get_just_list_name()
    return templates.TemplateResponse("list_names.html", {"request": request, "names": db_names})


@app.post("/name/is_polish")
def check_if_polish_name(item: NameItem) -> dict:
    db_names = db.get_dict_names().values()
    # konwersja z jsona na dict pythonowy
    item_dict = item.dict()
    return {"name_value": item_dict["name_value"].capitalize(),
            "is_polish": True if item_dict["name_value"].capitalize() in db_names else False}


@app.get("/name/{item_id}")
def get_name_by_id(request: Request, item_id: int):
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
