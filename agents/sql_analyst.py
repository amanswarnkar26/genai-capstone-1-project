from typing import Dict, Any, List, Tuple
import sqlite3
from core.config import settings

ALLOWED_TABLES = {"loans": ["loan_id","customer_id","loan_amount","tenure","interest_rate","emi","status","topup_eligible","disbursal_date","last_payment_date","outstanding_principal"]}

def _connect():
    return sqlite3.connect(settings.sqlite_path)

def _safe_query(nlq: str, params: Dict[str, Any]) -> Tuple[str, List[Any]]:
    q = nlq.lower()
    if "emi" in q and ("status" in q or "amount" in q):
        sql = "SELECT loan_id, emi, status, last_payment_date FROM loans WHERE customer_id = ?"
        return sql, [params.get("customer_id")]
    if "top-up" in q or "topup" in q:
        sql = "SELECT loan_id, topup_eligible, outstanding_principal FROM loans WHERE customer_id = ?"
        return sql, [params.get("customer_id")]
    if "interest" in q:
        sql = "SELECT loan_id, interest_rate, tenure, emi FROM loans WHERE customer_id = ?"
        return sql, [params.get("customer_id")]
    sql = "SELECT loan_id, emi, status FROM loans WHERE customer_id = ?"
    return sql, [params.get("customer_id")]

def query(nlq: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if not params.get("customer_id"):
        return {"ok": False, "reason": "missing_customer_id"}
    sql, bind = _safe_query(nlq, params)
    try:
        con = _connect()
        cur = con.cursor()
        cur.execute(sql, bind)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        con.close()
        return {"ok": True, "sql": sql, "rows": [dict(zip(cols, r)) for r in rows]}
    except Exception as e:
        return {"ok": False, "reason": "sql_error", "error": str(e)}
