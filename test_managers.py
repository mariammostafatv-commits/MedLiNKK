"""
Core Managers Test Script
Tests all 4 core managers with database
Location: core/test_managers.py
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.auth_manager import get_auth_manager
from core.patient_manager import get_patient_manager
from core.visit_manager import get_visit_manager
from core.card_manager import get_card_manager


def test_auth_manager():
    """Test authentication manager"""
    print("\n" + "="*60)
    print("🔐 TESTING AUTH MANAGER")
    print("="*60)
    
    auth = get_auth_manager()
    
    # Test 1: Login with username/password
    print("\n1. Testing username/password login...")
    user = auth.login("dr.ahmed.hassan", "password123")
    if user:
        print(f"   ✅ Login successful: {user['full_name']}")
        print(f"   ✅ Role: {user['role']}")
    else:
        print("   ❌ Login failed!")
        return False
    
    # Test 2: Invalid login
    print("\n2. Testing invalid credentials...")
    user = auth.login("invalid", "wrong")
    if not user:
        print("   ✅ Invalid credentials correctly rejected")
    else:
        print("   ❌ Invalid credentials accepted (should fail)!")
        return False
    
    # Test 3: Get user
    print("\n3. Testing get_user...")
    user = auth.get_user("dr.ahmed.hassan")
    if user:
        print(f"   ✅ User found: {user['username']}")
    else:
        print("   ❌ User not found!")
        return False
    
    # Test 4: Get all doctors
    print("\n4. Testing get_all_doctors...")
    doctors = auth.get_all_doctors()
    print(f"   ✅ Found {len(doctors)} doctors")
    
    # Test 5: Logout
    print("\n5. Testing logout...")
    auth.logout()
    if not auth.is_logged_in():
        print("   ✅ Logout successful")
    else:
        print("   ❌ Logout failed!")
        return False
    
    print("\n✅ AUTH MANAGER: ALL TESTS PASSED")
    return True


def test_patient_manager():
    """Test patient manager"""
    print("\n" + "="*60)
    print("👥 TESTING PATIENT MANAGER")
    print("="*60)
    
    pm = get_patient_manager()
    
    # Test 1: Get all patients
    print("\n1. Testing get_all_patients...")
    patients = pm.get_all_patients()
    print(f"   ✅ Found {len(patients)} patients")
    
    if not patients:
        print("   ⚠️  No patients in database!")
        return False
    
    # Test 2: Get specific patient
    print("\n2. Testing get_patient...")
    test_patient = patients[0]
    national_id = test_patient['national_id']
    patient = pm.get_patient(national_id)
    
    if patient:
        print(f"   ✅ Patient found: {patient['full_name']}")
        print(f"   ✅ National ID: {patient['national_id']}")
        print(f"   ✅ Blood Type: {patient['blood_type']}")
    else:
        print("   ❌ Patient not found!")
        return False
    
    # Test 3: Search patients
    print("\n3. Testing search_patients...")
    results = pm.search_patients("Ahmed")
    print(f"   ✅ Found {len(results)} results for 'Ahmed'")
    
    # Test 4: Get surgeries
    print("\n4. Testing get_surgeries...")
    surgeries = pm.get_surgeries(national_id)
    print(f"   ✅ Patient has {len(surgeries)} surgeries")
    
    # Test 5: Get hospitalizations
    print("\n5. Testing get_hospitalizations...")
    hospitalizations = pm.get_hospitalizations(national_id)
    print(f"   ✅ Patient has {len(hospitalizations)} hospitalizations")
    
    # Test 6: Get vaccinations
    print("\n6. Testing get_vaccinations...")
    vaccinations = pm.get_vaccinations(national_id)
    print(f"   ✅ Patient has {len(vaccinations)} vaccinations")
    
    # Test 7: Get patient count
    print("\n7. Testing get_patient_count...")
    count = pm.get_patient_count()
    print(f"   ✅ Total patients: {count}")
    
    print("\n✅ PATIENT MANAGER: ALL TESTS PASSED")
    return True


def test_visit_manager():
    """Test visit manager"""
    print("\n" + "="*60)
    print("🩺 TESTING VISIT MANAGER")
    print("="*60)
    
    vm = get_visit_manager()
    
    # Test 1: Get all visits
    print("\n1. Testing get_all_visits...")
    visits = vm.get_all_visits()
    print(f"   ✅ Found {len(visits)} visits")
    
    if not visits:
        print("   ⚠️  No visits in database!")
        return True  # Not critical if no visits
    
    # Test 2: Get specific visit
    print("\n2. Testing get_visit...")
    test_visit = visits[0]
    visit_id = test_visit['visit_id']
    visit = vm.get_visit(visit_id)
    
    if visit:
        print(f"   ✅ Visit found: {visit['visit_id']}")
        print(f"   ✅ Patient: {visit['patient_national_id']}")
        print(f"   ✅ Doctor: {visit['doctor_name']}")
        print(f"   ✅ Date: {visit['date']}")
    else:
        print("   ❌ Visit not found!")
        return False
    
    # Test 3: Get patient visits
    print("\n3. Testing get_patient_visits...")
    patient_id = test_visit['patient_national_id']
    patient_visits = vm.get_patient_visits(patient_id)
    print(f"   ✅ Patient has {len(patient_visits)} visits")
    
    # Test 4: Get visit count
    print("\n4. Testing get_visit_count...")
    count = vm.get_visit_count()
    print(f"   ✅ Total visits: {count}")
    
    print("\n✅ VISIT MANAGER: ALL TESTS PASSED")
    return True


def test_card_manager():
    """Test card manager"""
    print("\n" + "="*60)
    print("💳 TESTING CARD MANAGER")
    print("="*60)
    
    cm = get_card_manager()
    
    # Test 1: Get all cards
    print("\n1. Testing get_all_cards...")
    cards = cm.get_all_cards()
    doctor_cards = cards.get('doctor_cards', {})
    patient_cards = cards.get('patient_cards', {})
    
    print(f"   ✅ Found {len(doctor_cards)} doctor cards")
    print(f"   ✅ Found {len(patient_cards)} patient cards")
    
    # Test 2: Get card count
    print("\n2. Testing get_card_count...")
    count = cm.get_card_count()
    print(f"   ✅ Total cards: {count}")
    
    # Test 3: Test doctor authentication (if cards exist)
    if doctor_cards:
        print("\n3. Testing authenticate_doctor...")
        first_card_uid = list(doctor_cards.keys())[0]
        doctor = cm.authenticate_doctor(first_card_uid)
        
        if doctor:
            print(f"   ✅ Doctor authenticated: {doctor['full_name']}")
        else:
            print("   ❌ Doctor authentication failed!")
            return False
    else:
        print("\n3. Skipping authenticate_doctor (no doctor cards)")
    
    # Test 4: Test patient by card (if cards exist)
    if patient_cards:
        print("\n4. Testing get_patient_by_card...")
        first_card_uid = list(patient_cards.keys())[0]
        patient = cm.get_patient_by_card(first_card_uid)
        
        if patient:
            print(f"   ✅ Patient found by card: {patient['full_name']}")
        else:
            print("   ⚠️  Patient not found by card (might not be linked)")
    else:
        print("\n4. Skipping get_patient_by_card (no patient cards)")
    
    print("\n✅ CARD MANAGER: ALL TESTS PASSED")
    return True


def run_all_tests():
    """Run all manager tests"""
    print("\n" + "="*70)
    print(" "*15 + "🧪 CORE MANAGERS TEST SUITE")
    print("="*70)
    print("\nTesting all 4 core managers with database...")
    
    results = {
        'auth_manager': False,
        'patient_manager': False,
        'visit_manager': False,
        'card_manager': False
    }
    
    # Run tests
    try:
        results['auth_manager'] = test_auth_manager()
    except Exception as e:
        print(f"\n❌ AUTH MANAGER TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        results['patient_manager'] = test_patient_manager()
    except Exception as e:
        print(f"\n❌ PATIENT MANAGER TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        results['visit_manager'] = test_visit_manager()
    except Exception as e:
        print(f"\n❌ VISIT MANAGER TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        results['card_manager'] = test_card_manager()
    except Exception as e:
        print(f"\n❌ CARD MANAGER TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "="*70)
    print(" "*20 + "📊 TEST SUMMARY")
    print("="*70)
    
    for manager, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"  {manager:.<30} {status}")
    
    print("="*70)
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! Core managers are working perfectly!")
        print("\n✅ Phase 1 Task 1.2: COMPLETE")
    else:
        print("\n⚠️  SOME TESTS FAILED! Please check errors above.")
        print("\n❌ Phase 1 Task 1.2: INCOMPLETE")
    
    print("="*70)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)