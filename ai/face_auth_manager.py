"""
MedLink Face Authentication Manager
Uses DeepFace for team member recognition
"""

from deepface import DeepFace
import cv2
import os
import json
from datetime import datetime
from pathlib import Path
import shutil

class FaceAuthManager:
    def __init__(self, base_path="data"):
        self.base_path = Path(base_path)
        self.faces_db = self.base_path / "team_faces"
        self.config_file = self.base_path / "face_config.json"
        print(f"🎭 Initializing FaceAuthManager at {self.base_path}")
        print(f"🎭 Config file: {self.config_file}")

        # Create directories
        self.faces_db.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self):
        """Load face recognition configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_config(self):
        """Save face recognition configuration"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def register_team_member(self, username, full_name, role, photo_path):
        """
        Register a new team member with their face
        
        Args:
            username: Unique username
            full_name: Full name of team member
            role: Role (e.g., 'doctor', 'admin')
            photo_path: Path to photo file
        
        Returns:
            dict: Success status and message
        """
        try:
            # Create user folder
            user_folder = self.faces_db / username
            user_folder.mkdir(exist_ok=True)
            
            # Verify face exists in photo
            try:
                faces = DeepFace.extract_faces(
                    img_path=photo_path,
                    enforce_detection=True,
                    detector_backend='opencv'
                )
                
                if not faces:
                    return {
                        "success": False,
                        "message": "No face detected in photo!"
                    }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Face detection failed: {str(e)}"
                }
            
            # Copy photo to user folder
            photo_name = f"{username}_main.jpg"
            destination = user_folder / photo_name
            shutil.copy(photo_path, destination)
            
            # Save user config
            self.config[username] = {
                "full_name": full_name,
                "role": role,
                "registered_at": datetime.now().isoformat(),
                "photo_count": 1
            }
            self._save_config()
            
            return {
                "success": True,
                "message": f"✅ {full_name} registered successfully!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def add_photo(self, username, photo_path):
        """Add additional photo for better recognition"""
        try:
            user_folder = self.faces_db / username
            if not user_folder.exists():
                return {
                    "success": False,
                    "message": "User not registered!"
                }
            
            # Count existing photos
            photo_count = len(list(user_folder.glob("*.jpg")))
            
            # Copy new photo
            photo_name = f"{username}_{photo_count + 1}.jpg"
            destination = user_folder / photo_name
            shutil.copy(photo_path, destination)
            
            # Update config
            self.config[username]["photo_count"] = photo_count + 1
            self._save_config()
            
            return {
                "success": True,
                "message": f"✅ Photo added! Total: {photo_count + 1}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def recognize_from_webcam(self, camera_index=0):
        """
        Recognize team member from webcam
        
        Args:
            camera_index: Webcam index (default: 0)
        
        Returns:
            dict: Recognition result with username and confidence
        """
        temp_photo = self.base_path / "temp_face.jpg"
        
        try:
            # Check if database is empty
            if not self.config:
                return {
                    "success": False,
                    "message": "❌ No team members registered yet!"
                }
            
            # Capture frame from webcam
            cap = cv2.VideoCapture(camera_index)
            
            if not cap.isOpened():
                return {
                    "success": False,
                    "message": "❌ Could not open webcam!"
                }
            
            # Read frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return {
                    "success": False,
                    "message": "❌ Could not capture frame!"
                }
            
            # Save temporary frame
            cv2.imwrite(str(temp_photo), frame)
            
            # Find matching face
            result = DeepFace.find(
                img_path=str(temp_photo),
                db_path=str(self.faces_db),
                model_name="Facenet512",
                enforce_detection=False,
                silent=True
            )
            
            # Clean up temp file
            if temp_photo.exists():
                temp_photo.unlink()
            
            # Check if any matches found
            if len(result) > 0 and len(result[0]) > 0:
                # Get best match
                best_match = result[0].iloc[0]
                matched_path = Path(best_match['identity'])
                username = matched_path.parent.name
                
                # Get user info
                user_info = self.config.get(username, {})
                
                # Distance < 0.4 is considered a good match for Facenet512
                confidence = 1 - (best_match['distance'] / 1.5)
                confidence = max(0, min(1, confidence)) * 100  # Convert to percentage
                
                if best_match['distance'] < 0.6:  # Good match threshold
                    return {
                        "success": True,
                        "username": username,
                        "full_name": user_info.get("full_name", username),
                        "role": user_info.get("role", "unknown"),
                        "confidence": round(confidence, 2),
                        "message": f"✅ Welcome {user_info.get('full_name', username)}!"
                    }
                else:
                    return {
                        "success": False,
                        "message": "❌ Face not recognized with high confidence"
                    }
            else:
                return {
                    "success": False,
                    "message": "❌ No matching face found in database"
                }
                
        except Exception as e:
            # Clean up temp file if exists
            if temp_photo.exists():
                temp_photo.unlink()
            
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }
    
    def get_registered_users(self):
        """Get list of all registered users"""
        return [
            {
                "username": username,
                "full_name": data.get("full_name", username),
                "role": data.get("role", "unknown"),
                "registered_at": data.get("registered_at", "N/A"),
                "photo_count": data.get("photo_count", 0)
            }
            for username, data in self.config.items()
        ]
    
    def remove_user(self, username):
        """Remove a registered user"""
        try:
            user_folder = self.faces_db / username
            
            if user_folder.exists():
                shutil.rmtree(user_folder)
            
            if username in self.config:
                del self.config[username]
                self._save_config()
            
            return {
                "success": True,
                "message": f"✅ {username} removed successfully!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Error: {str(e)}"
            }


# Quick test
if __name__ == "__main__":
    print("🎭 MedLink Face Recognition Test")
    print("=" * 50)
    
    manager = FaceAuthManager()
    
    # Show registered users
    users = manager.get_registered_users()
    print(f"\n📋 Registered users: {len(users)}")
    for user in users:
        print(f"   - {user['full_name']} ({user['username']}) - {user['role']}")
    
    # Test recognition
    print("\n📷 Testing face recognition...")
    print("Position your face in front of the camera...")
    
    import time
    time.sleep(2)
    
    result = manager.recognize_from_webcam()
    print(f"\n{result['message']}")
    if result['success']:
        print(f"   Username: {result['username']}")
        print(f"   Role: {result['role']}")
        print(f"   Confidence: {result['confidence']}%")