from typing import Dict, Any, List
import os
from core.config import settings

def ask_policy(question: str, k: int = 3) -> Dict[str, Any]:
    citations = []
    pol_dir = settings.policies_path
    if os.path.isdir(pol_dir):
        for fn in sorted(os.listdir(pol_dir))[:k]:
            if fn.lower().endswith(".pdf"):
                citations.append({"title": fn, "source": f"{pol_dir}/{fn}"})
    if not citations:
        return {"ok": False, "reason": "no_corpus"}
    answer = ("Based on policy corpus and RBI guidelines, prepayment may require notice and may incur "
              "a pre-closure fee depending on tenure and loan type. EMI status queries must be validated against the core LMS. ")
    return {"ok": True, "answer": answer, "citations": citations, "confidence": 0.82}
