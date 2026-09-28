from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.schemas.schemas import HealthResponse
from app.api.endpoints import router as api_router
from app.engines.financial_engine import FinancialValidationError
from app.engines.business_analysis_engine import BusinessAnalysisValidationError

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Driven Hyper-Local Business Advisory and Financial Structuring Assistant for Rural Micro-Entrepreneurs",
    version=settings.VERSION,
)

# Exception handler for business analysis validation errors
@app.exception_handler(BusinessAnalysisValidationError)
async def business_validation_handler(request: Request, exc: BusinessAnalysisValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "message": exc.message,
                "field": exc.field,
                "code": exc.code or "BUSINESS_VALIDATION_ERROR",
            },
        },
    )

# Exception handler for deterministic financial engine validation errors
@app.exception_handler(FinancialValidationError)
async def financial_validation_handler(request: Request, exc: FinancialValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "message": exc.message,
                "field": exc.field,
                "code": exc.code or "FINANCIAL_VALIDATION_ERROR",
            },
        },
    )

# Exception handler for Pydantic / FastAPI request validation errors
@app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first_err = errors[0] if errors else {}
    loc = first_err.get("loc", [])
    field = str(loc[-1]) if loc else None
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "error": {
                "message": first_err.get("msg", "Invalid input value"),
                "field": field,
                "code": "REQUEST_VALIDATION_ERROR",
            },
        },
    )

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health endpoint required by Phase B1
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint returning system status.
    """
    return {"status": "ok"}

# Mount business advisory and financial endpoints under root and api prefix
app.include_router(api_router, tags=["BizSahayak"])
app.include_router(api_router, prefix=settings.API_PREFIX, tags=["BizSahayak V1"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
