#!/usr/bin/env python3
"""
calc_roi.py — Real estate investment return calculator
Usage: python3 src/tools/calc_roi.py data/listings/456_elm_st.json
"""

import json
import sys
from pathlib import Path


def calc_roi(listing_path: str) -> dict:
    with open(listing_path) as f:
        data = json.load(f)

    purchase_price = data["listing"]["list_price"]
    monthly_rent = data["rental_context"]["estimated_monthly_rent"]
    annual_taxes = data["financials"]["annual_property_taxes"]
    annual_insurance = data["financials"]["annual_insurance_estimate"]
    hoa_monthly = data["hoa"]["monthly_dues"] if data["hoa"]["exists"] else 0

    # Assumptions
    vacancy_rate = 0.05
    maintenance_pct = 0.01
    mgmt_fee_pct = 0.08
    down_payment_pct = 0.20
    interest_rate = 0.0695  # ~6.95% 30yr fixed
    loan_term_years = 30

    # Income
    gross_annual_rent = monthly_rent * 12
    effective_gross_income = gross_annual_rent * (1 - vacancy_rate)

    # Expenses (annual)
    maintenance = purchase_price * maintenance_pct
    mgmt_fee = effective_gross_income * mgmt_fee_pct
    hoa_annual = hoa_monthly * 12
    total_expenses = annual_taxes + annual_insurance + maintenance + mgmt_fee + hoa_annual

    # NOI
    noi = effective_gross_income - total_expenses

    # Mortgage
    loan_amount = purchase_price * (1 - down_payment_pct)
    monthly_rate = interest_rate / 12
    n = loan_term_years * 12
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**n) / ((1 + monthly_rate)**n - 1)
    annual_debt_service = monthly_payment * 12

    # Cash flow
    annual_cash_flow = noi - annual_debt_service
    monthly_cash_flow = annual_cash_flow / 12

    # Returns
    down_payment = purchase_price * down_payment_pct
    closing_costs = purchase_price * 0.02
    total_cash_invested = down_payment + closing_costs

    cap_rate = (noi / purchase_price) * 100
    cash_on_cash = (annual_cash_flow / total_cash_invested) * 100
    gross_yield = (gross_annual_rent / purchase_price) * 100
    grm = purchase_price / gross_annual_rent

    return {
        "property_id": data["property_id"],
        "purchase_price": purchase_price,
        "monthly_rent": monthly_rent,
        "gross_annual_rent": round(gross_annual_rent, 2),
        "effective_gross_income": round(effective_gross_income, 2),
        "total_annual_expenses": round(total_expenses, 2),
        "noi": round(noi, 2),
        "monthly_mortgage": round(monthly_payment, 2),
        "annual_debt_service": round(annual_debt_service, 2),
        "monthly_cash_flow": round(monthly_cash_flow, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "total_cash_invested": round(total_cash_invested, 2),
        "cap_rate_pct": round(cap_rate, 2),
        "cash_on_cash_pct": round(cash_on_cash, 2),
        "gross_yield_pct": round(gross_yield, 2),
        "grm": round(grm, 2),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 calc_roi.py <path_to_listing.json>")
        sys.exit(1)

    result = calc_roi(sys.argv[1])

    print("\n" + "="*50)
    print(f"ROI ANALYSIS — {result['property_id']}")
    print("="*50)
    print(f"Purchase Price:       ${result['purchase_price']:>12,.0f}")
    print(f"Monthly Rent:         ${result['monthly_rent']:>12,.0f}")
    print(f"Monthly Cash Flow:    ${result['monthly_cash_flow']:>12,.2f}")
    print(f"Annual Cash Flow:     ${result['annual_cash_flow']:>12,.2f}")
    print(f"Cap Rate:             {result['cap_rate_pct']:>11.2f}%")
    print(f"Cash-on-Cash Return:  {result['cash_on_cash_pct']:>11.2f}%")
    print(f"Gross Yield:          {result['gross_yield_pct']:>11.2f}%")
    print(f"GRM:                  {result['grm']:>12.1f}x")
    print(f"Monthly Mortgage:     ${result['monthly_mortgage']:>12,.2f}")
    print(f"Total Cash Invested:  ${result['total_cash_invested']:>12,.0f}")
    print("="*50 + "\n")

    # Also write JSON for agents to parse
    out_path = Path("data/progress") / f"roi_{result['property_id']}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"JSON output saved to: {out_path}")
