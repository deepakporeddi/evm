from __future__ import annotations
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://smartcity:smartcity@localhost:5432/evm")
SQL_ECHO = os.getenv("SQL_ECHO", "0") == "1"
