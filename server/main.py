from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
import json

from services.loan_calculator import loan_calculator

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "show_loan_application": False, "show_loan_result": False, "result": None})

@app.post("/start-loan-application", response_class=HTMLResponse)
async def start_loan_application(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "show_loan_application": True, "show_loan_result": False, "result": None})

@app.post("/calculate-loan", response_class=HTMLResponse)
async def calculate_loan(
    request: Request,
    principal: float = Form(...),
    add_on_rate: float = Form(...),
    tenor: int = Form(...),
    documentary_stamp_fee: float = Form(...),
    disbursement_fees: float = Form(...),
    other_charges: float = Form(...)
):
    result = loan_calculator(principal, add_on_rate, tenor, documentary_stamp_fee, disbursement_fees, other_charges)
    result = json.loads(result)  # Convert JSON string to dictionary
    return templates.TemplateResponse("index.html", {"request": request, "show_loan_application": False, "show_loan_result": True, "result": result})

@app.get("/documentation", response_class=HTMLResponse)
async def documentation(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "show_documentation": True})

@app.get("/pricing", response_class=HTMLResponse)
async def pricing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "show_pricing": True})