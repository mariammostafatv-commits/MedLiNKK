"""
Authentication API Routes
"""
from fastapi import APIRouter, HTTPException, Depends
from api.schemas import LoginRequest, LoginResponse, RegisterRequest
from api.dependencies import create_access_token
from core.auth_manager import get_auth_manager

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    """Login with username and password"""
    auth = get_auth_manager()
    user = auth.login(request.username, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access token
    access_token = create_access_token({"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login/fingerprint")
def login_fingerprint(fingerprint_id: str):
    """Login with fingerprint"""
    auth = get_auth_manager()
    user = auth.login_with_fingerprint(fingerprint_id)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid fingerprint")
    
    access_token = create_access_token({"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/register")
def register(request: RegisterRequest):
    """Register new user"""
    auth = get_auth_manager()
    
    user_data = request.dict()
    success = auth.register_user(user_data)
    
    if not success:
        raise HTTPException(status_code=400, detail="Registration failed")
    
    return {"message": "User registered successfully"}

@router.post("/logout")
def logout():
    """Logout current user"""
    # In stateless JWT, logout is handled client-side
    return {"message": "Logged out successfully"}

@router.get("/me")
def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    return current_user