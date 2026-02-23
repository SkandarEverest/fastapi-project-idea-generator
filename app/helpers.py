import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, Tuple

from openai import OpenAI

from app.config import (
  OPENAI_API_KEY,
  MODEL,
  COST_PER_1K_INPUT,
  COST_PER_1K_OUTPUT,
)

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

SYSTEM_PROMPT = (
  "You generate ONE academic project idea. "
  "Return ONLY valid JSON. No markdown, no code fences, no extra text."
)

def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
  input_cost = (prompt_tokens / 1000) * COST_PER_1K_INPUT
  output_cost = (completion_tokens / 1000) * COST_PER_1K_OUTPUT
  return round(input_cost + output_cost, 8)

def build_user_prompt(theme: str, domain: str, constraints: str) -> str:
  return f"""
Generate ONE project idea in JSON with this exact structure:

{{
  "title": "...",
  "background": "...",
  "problem_statement": "...",
  "stakeholders": ["..."],
  "data_needed": ["..."],
  "method": "...",
  "evaluation": ["..."],
  "risks": ["..."],
  "next_steps": ["..."]
}}

Rules:
- Keep it realistic for a student project (8–12 weeks).
- Prefer public/open data or ethically collectable data.
- Make it specific enough to implement.
- Write in the same language as the user's theme (if Indonesian, respond Indonesian).
- Domain: {domain}
- Theme/Goal: {theme}
- Constraints: {constraints}
""".strip()

def _try_parse_json(raw: str) -> Dict[str, Any]:
  """
  Be robust to occasional wrappers. We still enforce JSON output,
  but this helps if the model accidentally adds fences.
  """
  text = (raw or "").strip()

  # strip common markdown fences if present
  if text.startswith("```"):
    # remove first fence line
    parts = text.split("\n")
    parts = parts[1:]  # drop ```json / ```
    # drop trailing fence if present
    if parts and parts[-1].strip().startswith("```"):
      parts = parts[:-1]
    text = "\n".join(parts).strip()

  # find first { and last } as fallback
  if not text.startswith("{"):
    l = text.find("{")
    r = text.rfind("}")
    if l != -1 and r != -1 and r > l:
      text = text[l : r + 1].strip()

  return json.loads(text)

def call_openai_project_idea(theme: str, domain: str, constraints: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
  if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing. Set it in your .env file.")

  t0 = time.perf_counter()
  user_prompt = build_user_prompt(theme, domain, constraints)

  response = client.chat.completions.create(
    model=MODEL,
    messages=[
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": user_prompt},
    ],
    temperature=0.7,
  )

  latency_ms = round((time.perf_counter() - t0) * 1000, 2)
  raw = response.choices[0].message.content or "{}"
  usage = response.usage

  prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
  completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
  total_tokens = int(getattr(usage, "total_tokens", 0) or 0)

  cost = calculate_cost(prompt_tokens, completion_tokens)

  obs = {
    "model": MODEL,
    "prompt_tokens": prompt_tokens,
    "completion_tokens": completion_tokens,
    "total_tokens": total_tokens,
    "latency_ms": latency_ms,
    "estimated_cost_usd": cost,
    "timestamp": datetime.utcnow().isoformat() + "Z",
  }

  logger.info("OBS | model=%s tokens=%d latency_ms=%s cost=%s", MODEL, total_tokens, latency_ms, cost)

  idea_dict = _try_parse_json(raw)
  return idea_dict, obs