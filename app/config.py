import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
MODEL: str = os.getenv("APP_MODEL", "gpt-4o-mini")
APP_TITLE: str = os.getenv("APP_TITLE", "AI Project Idea Generator")

# Optional cost estimation (rough, adjust if you want)
COST_PER_1K_INPUT: float = float(os.getenv("COST_PER_1K_INPUT", "0.000150"))
COST_PER_1K_OUTPUT: float = float(os.getenv("COST_PER_1K_OUTPUT", "0.000600"))