from typing import Dict, Any
from agents import sql_analyst, policy_guru, calculator

def route(query: str) -> str:
    q = query.lower()
    if any(k in q for k in ["what if", "simulate", "prepay", "pre-payment", "calculator"]):
        return "calc"
    if any(k in q for k in ["policy", "rbi", "prepayment", "foreclose", "pre-closure", "charges", "fees"]):
        return "policy"
    if any(k in q for k in ["emi", "loan", "interest", "topup", "top-up", "status"]):
        return "sql"
    return "sql"

def handle(query: str, params: Dict[str, Any]) -> Dict[str, Any]:
    intent = route(query)
    if intent == "sql":
        res = sql_analyst.query(query, params)
        if not res.get("ok"):
            return {"ok": False, "need_clarification": True, "message": "Please provide your customer_id to fetch EMI details."}
        return {"ok": True, "intent": "sql", "payload": res}
    if intent == "policy":
        res = policy_guru.ask_policy(query)
        if not res.get("ok") or res.get("confidence",0) < 0.75:
            return {"ok": False, "need_clarification": True, "message": "Could you specify the loan type or tenure for policy lookup?"}
        return {"ok": True, "intent": "policy", "payload": res}
    if intent == "calc":
        try:
            principal = float(params.get("principal", 0))
            rate = float(params.get("annual_rate", 0))
            months = int(params.get("months_remaining", 0))
            pre = float(params.get("prepay_amount", 0))
            mode = params.get("mode","reduce_tenure")
        except Exception:
            return {"ok": False, "need_clarification": True, "message": "Provide principal, annual_rate, months_remaining, prepay_amount."}
        res = calculator.simulate_prepayment(principal, rate, months, pre, mode)
        return {"ok": True, "intent": "calc", "payload": res}
    return {"ok": False, "message": "Unsupported intent"}
