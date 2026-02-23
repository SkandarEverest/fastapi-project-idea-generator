from typing import List
from pydantic import BaseModel, Field

class ProjectIdea(BaseModel):
  title: str = Field(..., description="Project title")
  background: str = Field(..., description="Short background / context")
  problem_statement: str = Field(..., description="What problem is solved")
  stakeholders: List[str] = Field(..., description="Who benefits / is involved")
  data_needed: List[str] = Field(..., description="Data needed (public or collected)")
  method: str = Field(..., description="High-level method/model approach")
  evaluation: List[str] = Field(..., description="How to evaluate the solution")
  risks: List[str] = Field(..., description="Technical/ethical/security risks")
  next_steps: List[str] = Field(..., description="Immediate next actions")

class ResultResponse(BaseModel):
  theme: str
  domain: str
  constraints: str

  idea: ProjectIdea
  model: str

  prompt_tokens: int
  completion_tokens: int
  total_tokens: int
  latency_ms: float
  estimated_cost_usd: float
  timestamp: str