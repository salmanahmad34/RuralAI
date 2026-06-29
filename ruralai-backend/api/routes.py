from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

from api.models import (
    QueryRequest, QueryResponse, RecommendationItem, AgentInfo, HealthCheckResponse
)
from api.security import (
    check_rate_limits, validate_query_criteria, sanitize_user_input, validate_api_key
)
from database.connection import get_db
from database.models import Query as DBQuery, AgentResponse as DBAgentResponse
from agents.master_agent import MasterAgent

router = APIRouter()
logger = logging.getLogger("Routes")
master_agent = MasterAgent()

# Metadata definitions for the 6 specialized agents
AGENTS_METADATA = {
    "agriculture": AgentInfo(
        name="Agriculture Agent",
        description="Assists with crop sowing advice, disease diagnostics, soil treatment, and market prices.",
        icon="🚜",
        capabilities=["Crop suitability forecast", "Fungal disease diagnosis", "NPK fertilizer recommendation", "Mandi rates tracker"]
    ),
    "health": AgentInfo(
        name="Health Agent",
        description="Assists with symptom checking, health centers lookup, immunization plans, and dietary tips.",
        icon="🏥",
        capabilities=["Symptom analysis guide", "Primary Health Center finder", "Vaccination scheduler", "Age-based dietary advice"]
    ),
    "education": AgentInfo(
        name="Education Agent",
        description="Matches scholarships, resolves school admissions, and provides career mapping guidance.",
        icon="🎓",
        capabilities=["Scholarship matcher", "Rural school lookup", "Scheme eligibility checker", "Career path recommendations"]
    ),
    "water": AgentInfo(
        name="Water Agent",
        description="Monitors aquifer depths, lists borewell success odds, checks water purity, and plans harvesting.",
        icon="💧",
        capabilities=["Aquifer depth reports", "Borewell success estimator", "Water safety testing rules", "Rainwater layout plans"]
    ),
    "infrastructure": AgentInfo(
        name="Infrastructure Agent",
        description="Tracks district road quality, electrical grids stability, mobile network signals, and public works.",
        icon="🛣️",
        capabilities=["PWD Road status index", "Grid load shedding schedule", "Cell tower signal indicator", "Government works dashboard"]
    ),
    "finance": AgentInfo(
        name="Finance Agent",
        description="Matches subsidies, calculates loan EMIs, and verifies qualifying welfare criteria.",
        icon="🪙",
        capabilities=["Welfare scheme finder", "Loan EMI calculator", "Credit qualifications check", "Subsidy options tracker"]
    )
}

@router.post("/query", response_model=QueryResponse, dependencies=[Depends(check_rate_limits)])
async def query_agent(
    request: QueryRequest,
    db: Session = Depends(get_db),
    api_key: Optional[str] = Depends(validate_api_key)
):
    """Orchestrate query routing, sanitization, domain computation, DB logging, and returns."""
    try:
        # 1. Input Sanitization
        sanitized_query = sanitize_user_input(request.query)
        
        # 2. Input Validation
        validate_query_criteria(sanitized_query, request.category.value, request.language.value)
        
        # 3. Master agent processing
        result = await master_agent.process_query(
            query=sanitized_query,
            category=request.category.value,
            language=request.language.value
        )
        
        # Convert recommendations dictionaries to RecommendationItem models
        recs_list = []
        for rec in result.get("recommendations", []):
            recs_list.append(RecommendationItem(
                title=rec.get("title", "Recommendation"),
                description=rec.get("description", ""),
                source=rec.get("source", "Agent"),
                confidence=rec.get("confidence", 1.0)
            ))
            
        # 4. Save to Database for audit trail
        # TODO(security): Ensure sensitive database fields (such as PII) are properly encrypted/masked.
        db_query = DBQuery(
            id=result["query_id"],
            user_input=sanitized_query,
            category=request.category.value,
            language=request.language.value,
            agent_used=result["agent_used"],
            response_data=result,
            sources_used=result["sources"]
        )
        db.add(db_query)
        
        db_response = DBAgentResponse(
            query_id=result["query_id"],
            agent_name=result["agent_used"],
            recommendations=[r.model_dump() for r in recs_list],
            confidence_score=1.0,
            processing_time=result["processing_time"],
            status="success"
        )
        db.add(db_response)
        db.commit()
        
        return QueryResponse(
            query_id=result["query_id"],
            agent_used=result["agent_used"],
            recommendations=recs_list,
            sources=result["sources"],
            language=result["language"],
            processing_time=result["processing_time"],
            timestamp=result["timestamp"],
            message=result.get("message")
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("Internal error in routing execution")
        # Save failure log in database
        import uuid
        err_id = str(uuid.uuid4())
        try:
            db_query = DBQuery(
                id=err_id,
                user_input=request.query,
                category=request.category.value,
                language=request.language.value,
                agent_used="error-handler",
                response_data={"error": str(e)},
                sources_used=["ErrorHandler"]
            )
            db.add(db_query)
            
            db_response = DBAgentResponse(
                query_id=err_id,
                agent_name="error-handler",
                recommendations=[],
                confidence_score=0.0,
                processing_time=0.0,
                status="failed",
                error_message=str(e)
            )
            db.add(db_response)
            db.commit()
        except Exception as db_err:
            logger.error(f"Failed to log exception to DB: {db_err}")
            
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """System operational validation status check."""
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )

@router.get("/agents", response_model=List[AgentInfo])
async def get_agents():
    """Retrieve capabilities and details of all 6 agents."""
    return list(AGENTS_METADATA.values())

@router.get("/agents/{category}", response_model=AgentInfo)
async def get_agent_detail(category: str):
    """Retrieve details for a specific agent category."""
    cat_clean = category.lower().strip()
    if cat_clean not in AGENTS_METADATA:
        raise HTTPException(status_code=404, detail=f"Agent category '{category}' not found.")
    return AGENTS_METADATA[cat_clean]

@router.get("/schemes/{category}", response_model=List[Dict[str, Any]])
async def get_schemes_by_category(category: str):
    """Retrieve government schemes matching a specific category category."""
    cat_clean = category.lower().strip()
    # Query matching items in the Finance MCP schemes database
    schemes = []
    
    # Filter mcp server database directly
    for s_id, s in master_agent.finance_mcp.schemes_database.items():
        # Match either by category name or general occupations
        s_type = s.get("type", "").lower()
        s_occ = s.get("eligibility", {}).get("occupation", "").lower()
        
        if cat_clean in s_type or cat_clean in s_occ or cat_clean == "all":
            schemes.append(s)
            
    # Fallback default if none matched
    if not schemes:
        schemes = [master_agent.finance_mcp.schemes_database["pm_kisan"]]
        
    return schemes

@router.post("/voice-to-text")
async def voice_to_text(file: UploadFile = File(...)):
    """Stub converting voice queries into text transcripts for localization."""
    # TODO(security): Ensure user uploads are bound to size limits and secure filenames.
    logger.info(f"Received audio upload file: {file.filename}, type: {file.content_type}")
    
    # Perform extension check
    ext = file.filename.split(".")[-1].lower() if file.filename else ""
    if ext not in ["wav", "mp3", "m4a", "ogg", "webm"]:
        raise HTTPException(status_code=400, detail="Invalid audio file format. Allowed: wav, mp3, m4a, ogg, webm")
        
    # Stub response
    return {
        "text": "मेरे खेत के टमाटर में कौन सा रोग है और इसका इलाज क्या है?",
        "language": "hi",
        "transcription_confidence": 0.96
    }
