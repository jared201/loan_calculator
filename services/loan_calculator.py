import json
from datetime import datetime, timedelta
import numpy_financial as npf

def calculate_loan_amount(principal, add_on_rate, tenor):
    total_interest = principal * (add_on_rate / 100) * (tenor / 12)
    loan_amount = principal + total_interest
    return loan_amount

def calculate_effective_interest_rate(loan_amount, add_on_rate, tenor):
    cash_flow = generate_cash_flow(loan_amount, add_on_rate, tenor, 0, 0)
    irr = calculate_irr(cash_flow)
    return irr

def calculate_fees(loan_amount, disbursement_fees, other_charges_rate, documentary_stamp_fee):
    other_charges = loan_amount * (other_charges_rate / 100)
    total_fees = disbursement_fees + other_charges + documentary_stamp_fee
    return total_fees

def generate_payment_schedule(loan_amount, interest_rate, tenor):
    monthly_rate = interest_rate / 12 / 100
    monthly_payment = npf.pmt(monthly_rate, tenor, -loan_amount)
    payment_schedule = []
    payment_date = datetime.now()
    for i in range(tenor):
        payment_date += timedelta(days=30)
        payment_schedule.append({
            "payment_date": payment_date.strftime("%Y-%m-%d"),
            "payment_amount": monthly_payment
        })
    return payment_schedule

def loan_calculator(principal, add_on_rate, tenor, documentary_stamp_fee, disbursement_fees, other_charges_rate):
    loan_amount = calculate_loan_amount(principal, add_on_rate, tenor)
    effective_interest_rate = calculate_effective_interest_rate(loan_amount, add_on_rate, tenor)
    total_fees = calculate_fees(loan_amount, disbursement_fees, other_charges_rate, documentary_stamp_fee)
    cash_flow = generate_cash_flow(loan_amount, add_on_rate, tenor, disbursement_fees, other_charges_rate)
    payment_schedule = generate_payment_schedule(loan_amount, add_on_rate, tenor)

    result = {
        "total_loan_amount": loan_amount,
        "cash_flow": cash_flow,
        "effective_interest_rate": effective_interest_rate,
        "payment_schedule": payment_schedule,
        "tenor": tenor
    }

    return json.dumps(result, indent=4)

def generate_cash_flow(loan_amount, add_on_rate, tenor, disbursement_fees, other_charges_rate):
    monthly_rate = add_on_rate / 12 / 100
    monthly_payment = npf.pmt(monthly_rate, tenor, -loan_amount)
    other_charges = loan_amount * (other_charges_rate / 100)
    cash_flow = [-loan_amount + disbursement_fees + other_charges]  # Initial disbursement
    for _ in range(tenor):
        cash_flow.append(monthly_payment)
    return cash_flow

def calculate_irr(cash_flow):
    irr = npf.irr(cash_flow)
    return irr