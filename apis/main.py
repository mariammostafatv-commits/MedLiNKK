"""
MedLink FastAPI Application
Main entry point for REST API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import auth, patients, visits, medical, labs, imaging, cards, search, stats

# Create FastAPI app
app = FastAPI(
    title="MedLink API",
    description="Medical Records Management System API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(visits.router, prefix="/api/visits", tags=["Visits"])
app.include_router(medical.router, prefix="/api/medical", tags=["Medical Records"])
app.include_router(labs.router, prefix="/api/labs", tags=["Lab Results"])
app.include_router(imaging.router, prefix="/api/imaging", tags=["Imaging"])
app.include_router(cards.router, prefix="/api/cards", tags=["NFC Cards"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(stats.router, prefix="/api/stats", tags=["Statistics"])

@app.get("/")
def root():
    return {
        "message": "MedLink API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)