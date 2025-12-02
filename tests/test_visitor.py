# test_visits.py
import json

# Load visits
with open('data/visits.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

visits = data.get('visits', [])
print(f"Total visits in file: {len(visits)}")

# Check for test patient
patient_id = "29501012345678"
patient_visits = [v for v in visits if v.get('patient_national_id') == patient_id]
print(f"Visits for patient {patient_id}: {len(patient_visits)}")

for visit in patient_visits:
    print(f"  - {visit.get('visit_id')}: {visit.get('date')} - {visit.get('chief_complaint')}")