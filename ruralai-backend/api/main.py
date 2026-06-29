from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import time
import logging
from api.routes import router
from database.connection import init_db

# Configure Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MainApp")

app = FastAPI(
    title="RuralAI",
    version="1.0.0",
    description="Intelligent AI Co-Pilot for Rural Agriculture, Health, Education, Water, Infrastructure, and Finance.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Configuration
# TODO(security): Strict CORS controls. Restrict wildcard origins (*) when deploying to staging/production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Custom Middleware for request duration logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Method: {request.method} Path: {request.url.path} Status: {response.status_code} Duration: {duration:.4f}s")
    return response

# Register API Router
app.include_router(router, prefix="/api")

# Startup Events
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up RuralAI application services...")
    try:
        # Initialize Database schemas and models
        init_db()
        logger.info("Database initialized and schemas validated successfully.")
    except Exception as e:
        logger.exception("CRITICAL: Failed to initialize database on startup.")

# Shutdown Events
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down RuralAI application services...")

# Exception Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Format HTTP errors into clean unified responses."""
    logger.error(f"HTTP Error {exc.status_code} on {request.url.path}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "message": exc.detail,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Neatly serialize Pydantic validator issues."""
    logger.warning(f"Validation failure on {request.url.path}: {exc.errors()}")
    errors_summary = []
    for err in exc.errors():
        loc = " -> ".join([str(x) for x in err["loc"]])
        errors_summary.append(f"[{loc}]: {err['msg']} (type: {err['type']})")
        
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "code": 400,
            "message": "Input validation failed.",
            "details": errors_summary,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Fail close and shield technical details from end-users on unhandled exceptions."""
    logger.exception(f"Unhandled Exception on {request.url.path}")
    # TODO(security): Do not leak internal exception details to the user.
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "code": 500,
            "message": "An unexpected error occurred. Please contact system support.",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    )
