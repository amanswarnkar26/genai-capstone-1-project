from typing import Dict, Any

def success(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"ok": True, "data": payload}

def error(message: str, code: str = "ERR", details: Dict[str, Any] = None) -> Dict[str, Any]:
    return {"ok": False, "error": {"code": code, "message": message, "details": details or {}}}
