import json

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from services.loan_calculator import loan_calculator

app = FastAPI()

# Set up the templates directory using a relative path
templates = Jinja2Templates(directory="templates")

@app.get("/loan-application")
async def loan_application(request: Request):
    return templates.TemplateResponse("loan-application.html", {"request": request})

@app.post("/calculate-loan")
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
    return templates.TemplateResponse("loan-result.html", {"request": request, "result": result})