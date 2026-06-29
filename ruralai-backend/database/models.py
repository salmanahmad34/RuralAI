import uuid
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database.connection import Base

# TODO(security): Ensure sensitive database fields (such as PII) are properly encrypted/masked.

class Query(Base):
    """Model representing user queries and their master orchestration details."""
    __tablename__ = "queries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_input = Column(String, nullable=False)
    category = Column(String, nullable=False)
    language = Column(String, default="hi")
    agent_used = Column(String, nullable=False)
    response_data = Column(JSON, nullable=True)
    sources_used = Column(JSON, nullable=True)  # List of sources
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    agent_responses = relationship("AgentResponse", back_populates="query", cascade="all, delete-orphan")


class AgentResponse(Base):
    """Model representing detailed execution responses from individual domain agents."""
    __tablename__ = "agent_responses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_id = Column(String, ForeignKey("queries.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    recommendations = Column(JSON, nullable=True)  # List of recommendations
    confidence_score = Column(Float, default=1.0)
    processing_time = Column(Float, default=0.0)
    status = Column(String, nullable=False)  # success / failed
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    query = relationship("Query", back_populates="agent_responses")


class UserSession(Base):
    """Model representing interactive user sessions and interface settings."""
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_token = Column(String, unique=True, nullable=False)
    language = Column(String, default="hi")
    theme = Column(String, default="light")
    last_accessed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
