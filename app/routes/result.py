import logging
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.config import APP_TITLE
from app.helpers import call_openai_project_idea
from app.schemas import ProjectIdea, ResultResponse

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/result", response_model=ResultResponse)
async def serve_result(
  request: Request,
  theme: str = Form(...),
  domain: str = Form(...),
  constraints: str = Form(""),
  format: str = Form("json"),
):
  try:
    idea_dict, obs = call_openai_project_idea(theme, domain, constraints)
    idea = ProjectIdea(**idea_dict)

    result = ResultResponse(
      theme=theme,
      domain=domain,
      constraints=constraints,
      idea=idea,
      **obs,
    )

    if format == "html":
      return templates.TemplateResponse(
        "result.html",
        {"request": request, "title": APP_TITLE, "result": result},
      )

    return JSONResponse(content=result.model_dump())

  except Exception as e:
    logger.exception("Failed to generate result")
    # If user chose html, show error page-ish using same template
    if format == "html":
      return HTMLResponse(
        content=f"<h1>Error</h1><pre>{str(e)}</pre><p><a href='/'>Back</a></p>",
        status_code=500,
      )
    return JSONResponse(content={"error": str(e)}, status_code=500)