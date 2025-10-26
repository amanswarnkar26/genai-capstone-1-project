import logging
import os

logger = logging.getLogger("loan_navigator")
level = os.getenv("LOG_LEVEL","INFO").upper()
logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
