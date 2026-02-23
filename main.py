import logging
from fastapi import FastAPI

from app.config import APP_TITLE, MODEL
from app.routes.form import router as form_router
from app.routes.result import router as result_router

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

app = FastAPI(title=APP_TITLE, version="1.0.0")

app.include_router(form_router)
app.include_router(result_router)

@app.get("/health")
async def health():
  return {"status": "ok", "model": MODEL}