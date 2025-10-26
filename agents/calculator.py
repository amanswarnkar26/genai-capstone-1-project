from typing import Dict, Any
from math import pow

def _emi(principal: float, annual_rate: float, months: int) -> float:
    r = annual_rate / 12.0 / 100.0
    if r == 0:
        return principal / months
    return principal * r * pow(1+r, months) / (pow(1+r, months) - 1)

def simulate_prepayment(principal: float, annual_rate: float, months_remaining: int, prepay_amount: float, mode: str = "reduce_tenure") -> Dict[str, Any]:
    if principal <= 0 or months_remaining <= 0:
        return {"ok": False, "reason": "invalid_inputs", "message": "Principal and months must be positive"}
    if prepay_amount <= 0:
        return {"ok": False, "reason": "invalid_prepay", "message": "Prepayment must be positive"}
    if prepay_amount >= principal:
        new_principal = 0.0
        return {"ok": True, "preclosure": True, "new_principal": new_principal, "new_emi": 0.0, "months_remaining": 0, "interest_saved": None}
    new_principal = principal - prepay_amount
    current_emi = _emi(principal, annual_rate, months_remaining)
    if mode == "reduce_tenure":
        emi_same = current_emi
        lo, hi = 1, months_remaining
        best = months_remaining
        for _ in range(60):
            mid = (lo+hi)//2
            if mid <= 0: break
            e = _emi(new_principal, annual_rate, mid)
            if e > emi_same:
                lo = mid + 1
            else:
                best = mid
                hi = mid - 1
        new_months = max(1, best)
        new_emi = emi_same
    else:
        new_months = months_remaining
        new_emi = _emi(new_principal, annual_rate, new_months)
    interest_saved = max(0.0, current_emi*months_remaining - new_emi*new_months - prepay_amount)
    return {"ok": True, "preclosure": False, "new_principal": new_principal, "new_emi": round(new_emi,2), "months_remaining": int(new_months), "interest_saved": round(interest_saved,2)}
