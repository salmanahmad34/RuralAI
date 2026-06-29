from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class CategoryEnum(str, Enum):
    agriculture = "agriculture"
    health = "health"
    education = "education"
    water = "water"
    infrastructure = "infrastructure"
    finance = "finance"

class LanguageEnum(str, Enum):
    hi = "hi"
    en = "en"
    mr = "mr"
    ta = "ta"

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=5, max_length=500, description="Query text from user")
    category: CategoryEnum = Field(..., description="Rural category for the query")
    language: LanguageEnum = Field(default=LanguageEnum.hi, description="Language preference")
    user_id: Optional[str] = Field(default=None, description="Optional unique identifier of the user")

class RecommendationItem(BaseModel):
    title: str = Field(..., description="Actionable recommendation title")
    description: str = Field(..., description="Detailed description of the recommendation")
    source: Optional[str] = Field(default=None, description="Source of the recommendation data")
    confidence: Optional[float] = Field(default=1.0, ge=0.0, le=1.0, description="Agent confidence score")

class QueryResponse(BaseModel):
    query_id: str = Field(..., description="UUID of the processed query log")
    agent_used: str = Field(..., description="The name of the agent that resolved the query")
    recommendations: List[RecommendationItem] = Field(default=[], description="List of recommendation items")
    sources: List[str] = Field(default=[], description="List of raw source references")
    language: str = Field(..., description="Resolved language code")
    processing_time: float = Field(..., description="Execution duration in seconds")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    message: Optional[str] = Field(default=None, description="Additional status or feedback messages")

class AgentInfo(BaseModel):
    name: str = Field(..., description="Display name of the agent")
    description: str = Field(..., description="Role and purpose details")
    icon: str = Field(..., description="Icon representation or emoji")
    capabilities: List[str] = Field(..., description="Detailed skill list of the agent")

class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="API operational health status")
    timestamp: str = Field(..., description="Current system time ISO format")
