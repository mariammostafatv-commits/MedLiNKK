"""
MedLink Core API - Central Medical Records Hub
Main FastAPI application that receives data from external healthcare providers

Port: 8000
Author: Youssef Mekkkawy
"""
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List
from datetime import datetime
import uvicorn
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

app = FastAPI(
    title="MedLink Core API",
    description="Central medical records management system - Receives data from hospitals, labs, and imaging centers",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for desktop app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== IN-MEMORY STORAGE ====================
# In production, this would be in MySQL database
# For demo, we use simple dictionaries

PROVIDERS = {}  # Registered healthcare providers
API_TOKENS = {}  # Provider API tokens
PATIENTS_DATA = {}  # Patient medical records
API_LOGS = []  # API access logs

# Initialize with sample providers
PROVIDERS = {
    1: {
        "id": 1,
        "name": "Cairo Lab",
        "type": "laboratory",
        "contact": "info@cairolab.eg",
        "address": "123 Tahrir Square, Cairo",
        "status": "active"
    },
    2: {
        "id": 2,
        "name": "Cairo University Hospital",
        "type": "hospital",
        "contact": "info@cuh.edu.eg",
        "address": "Kasr Al Ainy Street, Cairo",
        "status": "active"
    },
    3: {
        "id": 3,
        "name": "Alexandria Imaging Center",
        "type": "imaging",
        "contact": "info@aleximaging.eg",
        "address": "Corniche Road, Alexandria",
        "status": "active"
    },
    4: {
        "id": 4,
        "name": "Misr Pharmacy Chain",
        "type": "pharmacy",
        "contact": "info@misrpharmacy.eg",
        "address": "Multiple locations",
        "status": "active"
    }
}

# Initialize with sample API tokens
API_TOKENS = {
    "CAIRO_LAB_abc123def456": {
        "provider_id": 1,
        "provider_name": "Cairo Lab",
        "token": "CAIRO_LAB_abc123def456",
        "permissions": ["submit_lab_results"],
        "created_at": "2024-12-01",
        "expires_at": "2025-12-31",
        "status": "active"
    },
    "CUH_HOSPITAL_xyz789ghi012": {
        "provider_id": 2,
        "provider_name": "Cairo University Hospital",
        "token": "CUH_HOSPITAL_xyz789ghi012",
        "permissions": ["submit_visits", "submit_surgeries", "submit_hospitalizations"],
        "created_at": "2024-12-01",
        "expires_at": "2025-12-31",
        "status": "active"
    },
    "ALEX_IMAGING_mno345pqr678": {
        "provider_id": 3,
        "provider_name": "Alexandria Imaging Center",
        "token": "ALEX_IMAGING_mno345pqr678",
        "permissions": ["submit_imaging"],
        "created_at": "2024-12-01",
        "expires_at": "2025-12-31",
        "status": "active"
    },
    "MISR_PHARMACY_stu901vwx234": {
        "provider_id": 4,
        "provider_name": "Misr Pharmacy Chain",
        "token": "MISR_PHARMACY_stu901vwx234",
        "permissions": ["submit_prescriptions"],
        "created_at": "2024-12-01",
        "expires_at": "2025-12-31",
        "status": "active"
    }
}

# ==================== SECURITY ====================

def verify_api_token(authorization: str = Header(None)):
    """Verify provider API token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header"
        )
    
    # Extract token (format: "Bearer TOKEN" or just "TOKEN")
    token = authorization.replace("Bearer ", "").strip()
    
    if token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token"
        )
    
    token_info = API_TOKENS[token]
    
    if token_info["status"] != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API token is inactive"
        )
    
    # Check expiration
    # In production, check actual date
    
    return token_info

def log_api_access(token_info: dict, endpoint: str, patient_id: str = None):
    """Log API access for audit trail"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "provider_id": token_info["provider_id"],
        "provider_name": token_info["provider_name"],
        "endpoint": endpoint,
        "patient_id": patient_id
    }
    API_LOGS.append(log_entry)
    
    # Keep only last 1000 logs
    if len(API_LOGS) > 1000:
        API_LOGS.pop(0)

# ==================== ROUTES ====================

@app.get("/")
async def root():
    """API root - health check"""
    return {
        "service": "MedLink Core API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "docs": "/docs",
            "providers": "/api/providers",
            "submit_lab": "/api/external/lab-results",
            "submit_imaging": "/api/external/imaging",
            "submit_visit": "/api/external/visits"
        }
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "providers_registered": len(PROVIDERS),
        "active_tokens": len([t for t in API_TOKENS.values() if t["status"] == "active"])
    }

# ==================== PROVIDER MANAGEMENT ====================

@app.get("/api/providers")
async def list_providers():
    """List all registered healthcare providers"""
    return {
        "total": len(PROVIDERS),
        "providers": list(PROVIDERS.values())
    }

@app.get("/api/providers/{provider_id}")
async def get_provider(provider_id: int):
    """Get specific provider details"""
    if provider_id not in PROVIDERS:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    return PROVIDERS[provider_id]

@app.get("/api/tokens")
async def list_tokens():
    """List all API tokens (admin only - for demo)"""
    return {
        "total": len(API_TOKENS),
        "tokens": [
            {
                "provider_name": t["provider_name"],
                "token": t["token"],
                "permissions": t["permissions"],
                "status": t["status"]
            }
            for t in API_TOKENS.values()
        ]
    }

# ==================== EXTERNAL PROVIDER ENDPOINTS ====================

@app.post("/api/external/lab-results")
async def submit_lab_results(
    data: dict,
    token_info: dict = Depends(verify_api_token)
):
    """
    Receive lab results from external laboratory
    
    Example:
    ```json
    {
        "patient_national_id": "29501012345678",
        "test_type": "Complete Blood Count",
        "test_date": "2024-12-15",
        "results": {
            "hemoglobin": 14.5,
            "wbc": 7200,
            "platelets": 250000
        },
        "lab_name": "Cairo Lab",
        "cost": 500.00,
        "payment_status": "paid",
        "payment_transaction_id": "TXN-123"
    }
    ```
    """
    # Verify permission
    if "submit_lab_results" not in token_info["permissions"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Validate required fields
    required = ["patient_national_id", "test_type", "results"]
    for field in required:
        if field not in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required field: {field}"
            )
    
    patient_id = data["patient_national_id"]
    
    # Initialize patient data if not exists
    if patient_id not in PATIENTS_DATA:
        PATIENTS_DATA[patient_id] = {
            "national_id": patient_id,
            "lab_results": [],
            "imaging_results": [],
            "visits": [],
            "surgeries": [],
            "hospitalizations": [],
            "prescriptions": []
        }
    
    # Add lab result
    lab_result = {
        "id": len(PATIENTS_DATA[patient_id]["lab_results"]) + 1,
        "submitted_by": token_info["provider_name"],
        "submitted_at": datetime.now().isoformat(),
        **data
    }
    
    PATIENTS_DATA[patient_id]["lab_results"].append(lab_result)
    
    # Log access
    log_api_access(token_info, "/api/external/lab-results", patient_id)
    
    return {
        "success": True,
        "message": "Lab results submitted successfully",
        "result_id": lab_result["id"],
        "patient_id": patient_id,
        "provider": token_info["provider_name"]
    }

@app.post("/api/external/imaging")
async def submit_imaging(
    data: dict,
    token_info: dict = Depends(verify_api_token)
):
    """
    Receive imaging results from imaging centers
    
    Example:
    ```json
    {
        "patient_national_id": "29501012345678",
        "imaging_type": "X-Ray",
        "body_part": "Chest",
        "imaging_date": "2024-12-15",
        "findings": "No abnormalities detected",
        "radiologist_name": "Dr. Mona Ahmed",
        "cost": 800.00,
        "payment_status": "paid"
    }
    ```
    """
    if "submit_imaging" not in token_info["permissions"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    required = ["patient_national_id", "imaging_type", "findings"]
    for field in required:
        if field not in data:
            raise HTTPException(status_code=400, detail=f"Missing field: {field}")
    
    patient_id = data["patient_national_id"]
    
    if patient_id not in PATIENTS_DATA:
        PATIENTS_DATA[patient_id] = {
            "national_id": patient_id,
            "lab_results": [],
            "imaging_results": [],
            "visits": [],
            "surgeries": [],
            "hospitalizations": [],
            "prescriptions": []
        }
    
    imaging_result = {
        "id": len(PATIENTS_DATA[patient_id]["imaging_results"]) + 1,
        "submitted_by": token_info["provider_name"],
        "submitted_at": datetime.now().isoformat(),
        **data
    }
    
    PATIENTS_DATA[patient_id]["imaging_results"].append(imaging_result)
    log_api_access(token_info, "/api/external/imaging", patient_id)
    
    return {
        "success": True,
        "message": "Imaging results submitted successfully",
        "result_id": imaging_result["id"],
        "patient_id": patient_id
    }

@app.post("/api/external/visits")
async def submit_visit(
    data: dict,
    token_info: dict = Depends(verify_api_token)
):
    """Receive medical visit records from hospitals"""
    if "submit_visits" not in token_info["permissions"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    patient_id = data.get("patient_national_id")
    if not patient_id:
        raise HTTPException(status_code=400, detail="Missing patient_national_id")
    
    if patient_id not in PATIENTS_DATA:
        PATIENTS_DATA[patient_id] = {
            "national_id": patient_id,
            "lab_results": [],
            "imaging_results": [],
            "visits": [],
            "surgeries": [],
            "hospitalizations": [],
            "prescriptions": []
        }
    
    visit = {
        "id": len(PATIENTS_DATA[patient_id]["visits"]) + 1,
        "submitted_by": token_info["provider_name"],
        "submitted_at": datetime.now().isoformat(),
        **data
    }
    
    PATIENTS_DATA[patient_id]["visits"].append(visit)
    log_api_access(token_info, "/api/external/visits", patient_id)
    
    return {
        "success": True,
        "message": "Visit record submitted successfully",
        "visit_id": visit["id"]
    }

@app.post("/api/external/surgeries")
async def submit_surgery(
    data: dict,
    token_info: dict = Depends(verify_api_token)
):
    """Receive surgery records from hospitals"""
    if "submit_surgeries" not in token_info["permissions"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    patient_id = data.get("patient_national_id")
    if not patient_id:
        raise HTTPException(status_code=400, detail="Missing patient_national_id")
    
    if patient_id not in PATIENTS_DATA:
        PATIENTS_DATA[patient_id] = {
            "national_id": patient_id,
            "lab_results": [],
            "imaging_results": [],
            "visits": [],
            "surgeries": [],
            "hospitalizations": [],
            "prescriptions": []
        }
    
    surgery = {
        "id": len(PATIENTS_DATA[patient_id]["surgeries"]) + 1,
        "submitted_by": token_info["provider_name"],
        "submitted_at": datetime.now().isoformat(),
        **data
    }
    
    PATIENTS_DATA[patient_id]["surgeries"].append(surgery)
    log_api_access(token_info, "/api/external/surgeries", patient_id)
    
    return {
        "success": True,
        "message": "Surgery record submitted successfully",
        "surgery_id": surgery["id"]
    }

@app.post("/api/external/hospitalizations")
async def submit_hospitalization(
    data: dict,
    token_info: dict = Depends(verify_api_token)
):
    """Receive hospitalization records"""
    if "submit_hospitalizations" not in token_info["permissions"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    patient_id = data.get("patient_national_id")
    if not patient_id:
        raise HTTPException(status_code=400, detail="Missing patient_national_id")
    
    if patient_id not in PATIENTS_DATA:
        PATIENTS_DATA[patient_id] = {
            "national_id": patient_id,
            "lab_results": [],
            "imaging_results": [],
            "visits": [],
            "surgeries": [],
            "hospitalizations": [],
            "prescriptions": []
        }
    
    hospitalization = {
        "id": len(PATIENTS_DATA[patient_id]["hospitalizations"]) + 1,
        "submitted_by": token_info["provider_name"],
        "submitted_at": datetime.now().isoformat(),
        **data
    }
    
    PATIENTS_DATA[patient_id]["hospitalizations"].append(hospitalization)
    log_api_access(token_info, "/api/external/hospitalizations", patient_id)
    
    return {
        "success": True,
        "message": "Hospitalization record submitted successfully",
        "hospitalization_id": hospitalization["id"]
    }

@app.post("/api/external/prescriptions")
async def submit_prescription(
    data: dict,
    token_info: dict = Depends(verify_api_token)
):
    """Receive prescription fulfillment from pharmacies"""
    if "submit_prescriptions" not in token_info["permissions"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    patient_id = data.get("patient_national_id")
    if not patient_id:
        raise HTTPException(status_code=400, detail="Missing patient_national_id")
    
    if patient_id not in PATIENTS_DATA:
        PATIENTS_DATA[patient_id] = {
            "national_id": patient_id,
            "lab_results": [],
            "imaging_results": [],
            "visits": [],
            "surgeries": [],
            "hospitalizations": [],
            "prescriptions": []
        }
    
    prescription = {
        "id": len(PATIENTS_DATA[patient_id]["prescriptions"]) + 1,
        "submitted_by": token_info["provider_name"],
        "submitted_at": datetime.now().isoformat(),
        **data
    }
    
    PATIENTS_DATA[patient_id]["prescriptions"].append(prescription)
    log_api_access(token_info, "/api/external/prescriptions", patient_id)
    
    return {
        "success": True,
        "message": "Prescription submitted successfully",
        "prescription_id": prescription["id"]
    }

# ==================== PATIENT DATA RETRIEVAL ====================

@app.get("/api/patients/{patient_id}")
async def get_patient_data(patient_id: str):
    """Get all medical data for a patient (for desktop app)"""
    if patient_id not in PATIENTS_DATA:
        return {
            "patient_id": patient_id,
            "lab_results": [],
            "imaging_results": [],
            "visits": [],
            "surgeries": [],
            "hospitalizations": [],
            "prescriptions": []
        }
    
    return PATIENTS_DATA[patient_id]

@app.get("/api/logs")
async def get_api_logs():
    """Get recent API access logs (admin only - for demo)"""
    return {
        "total": len(API_LOGS),
        "recent_logs": API_LOGS[-50:]  # Last 50 logs
    }

# ==================== PAYMENT WEBHOOK ====================

@app.post("/api/webhooks/payment-success")
async def payment_webhook(data: dict):
    """
    Receive payment confirmation from payment gateway
    
    Called automatically when payment succeeds
    """
    print(f"💰 Payment received: {data}")
    
    # In production: Update payment status in database
    # Link payment to medical record
    
    return {
        "success": True,
        "message": "Payment recorded"
    }

# ==================== RUN SERVER ====================

if __name__ == "__main__":
    print("="*60)
    print("🏥 MedLink Core API Starting...")
    print("="*60)
    print("🌐 API Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("📋 Providers: http://localhost:8000/api/providers")
    print("🔑 API Tokens: http://localhost:8000/api/tokens")
    print("="*60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )