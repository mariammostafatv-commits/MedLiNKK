# MedLink - Technical Documentation

## 📋 Table of Contents

- [1. Project Overview](#1-project-overview)
- [2. System Architecture](#2-system-architecture)
- [3. Technology Stack](#3-technology-stack)
- [4. Project Structure](#4-project-structure)
- [5. Core Components](#5-core-components)
- [6. GUI Components](#6-gui-components)
- [7. NFC Smart Card System](#7-nfc-smart-card-system)
- [8. Data Models](#8-data-models)
- [9. Security Implementation](#9-security-implementation)
- [10. API Design](#10-api-design)
- [11. Installation Guide](#11-installation-guide)
- [12. Development Guidelines](#12-development-guidelines)
- [13. Testing Strategy](#13-testing-strategy)
- [14. Future Enhancements](#14-future-enhancements)

---

## 1. Project Overview

### 1.1 Purpose

**MedLink** is a comprehensive desktop-based Unified Medical Records Management System designed to address the fragmentation of healthcare records in Egypt. The system provides secure, centralized storage and management of patient medical information, enabling seamless access for healthcare providers and patients.

### 1.2 Problem Statement

The Egyptian healthcare system faces critical challenges:
- **Fragmented Records**: Medical records scattered across multiple facilities
- **Emergency Delays**: Doctors lack immediate access to patient history during emergencies
- **Duplicate Testing**: Patients undergo repeated tests due to missing historical data
- **Poor Communication**: Limited information sharing between healthcare providers
- **Paper-Based Systems**: Inefficient, error-prone, and difficult to search

### 1.3 Solution

MedLink addresses these challenges by providing:
- Centralized electronic medical records
- Real-time access to patient history
- Emergency card generation with QR codes
- NFC smart card authentication for quick access
- Comprehensive search and filtering capabilities
- Secure data management with encryption

### 1.4 Key Metrics

- **Users**: 15 doctors, 30+ patients
- **Data Storage**: JSON-based with encryption
- **Response Time**: <500ms for search operations
- **Security**: SHA-256 password hashing, Fernet encryption
- **Accessibility**: NFC card login, QR code scanning

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    MedLink Application                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐              ┌──────────────┐        │
│  │ Login System │◄────────────►│ Auth Manager │        │
│  │  + NFC Card  │              │              │        │
│  └──────┬───────┘              └──────┬───────┘        │
│         │                              │                │
│         ├──────────────┬───────────────┤                │
│         ▼              ▼               ▼                │
│  ┌─────────┐    ┌──────────┐   ┌──────────┐           │
│  │ Doctor  │    │ Patient  │   │  Admin   │           │
│  │ Portal  │    │ Portal   │   │ (Future) │           │
│  └────┬────┘    └────┬─────┘   └──────────┘           │
│       │              │                                  │
│       └──────┬───────┘                                  │
│              ▼                                           │
│  ┌───────────────────────────────────┐                 │
│  │    Core Business Logic Layer      │                 │
│  ├───────────────────────────────────┤                 │
│  │ • Patient Manager                 │                 │
│  │ • Visit Manager                   │                 │
│  │ • Lab Manager                     │                 │
│  │ • Imaging Manager                 │                 │
│  │ • Surgery Manager                 │                 │
│  │ • Hospitalization Manager         │                 │
│  │ • Vaccination Manager             │                 │
│  │ • Family History Manager          │                 │
│  │ • Disability Manager              │                 │
│  │ • NFC/Card Manager                │                 │
│  │ • Search Engine                   │                 │
│  │ • PDF Generator                   │                 │
│  └───────────────┬───────────────────┘                 │
│                  ▼                                       │
│  ┌───────────────────────────────────┐                 │
│  │    Data Management Layer          │                 │
│  ├───────────────────────────────────┤                 │
│  │ • Data Manager (CRUD)             │                 │
│  │ • Security Manager                │                 │
│  │ • Validators                      │                 │
│  │ • File Handler                    │                 │
│  └───────────────┬───────────────────┘                 │
│                  ▼                                       │
│  ┌───────────────────────────────────┐                 │
│  │      Data Storage Layer           │                 │
│  ├───────────────────────────────────┤                 │
│  │ • users.json                      │                 │
│  │ • patients.json                   │                 │
│  │ • visits.json                     │                 │
│  │ • lab_results.json                │                 │
│  │ • imaging_results.json            │                 │
│  │ • cards.json (NFC mappings)       │                 │
│  │ • attachments/ (files)            │                 │
│  └───────────────────────────────────┘                 │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Component Interaction Flow

```
User Action → GUI Component → Manager Class → Data Manager → JSON Storage
                                    ↓
                              Validators ← Security Layer
                                    ↓
                              Success/Error → UI Update
```

### 2.3 NFC Authentication Flow

```
NFC Card Tap → Card Reader → Card Manager → User Lookup → Auth Manager
                                                               ↓
                                                    Dashboard (Doctor/Patient)
```

---

## 3. Technology Stack

### 3.1 Programming Language

**Python 3.9+**
- Object-oriented design patterns
- Type hints for code clarity
- Exception handling for robustness
- Async operations for performance

### 3.2 GUI Framework

**CustomTkinter 5.2.0**
- Modern dark theme interface
- Cross-platform compatibility (Windows, macOS, Linux)
- Responsive layout design
- Professional appearance
- Easy to learn and extend

**Rationale**: CustomTkinter provides a modern aesthetic while maintaining the simplicity of tkinter, making it ideal for desktop applications that need a professional look without web framework complexity.

### 3.3 Data Storage

**JSON Files**
- Human-readable format
- Easy to debug and inspect
- No database server required
- Version control friendly
- Portable across systems

**File Structure**:
- `users.json`: System users (doctors, patients, admins)
- `patients.json`: Patient medical records
- `visits.json`: Medical visits and consultations
- `lab_results.json`: Laboratory test results
- `imaging_results.json`: Imaging and radiology results
- `cards.json`: NFC card to user mappings

### 3.4 Security Libraries

**cryptography 41.0.7**
- Fernet symmetric encryption
- Secure key generation
- AES-128 encryption standard

**hashlib (built-in)**
- SHA-256 password hashing
- Irreversible cryptographic hashing
- Salt-based security

### 3.5 PDF Generation

**ReportLab 4.0.7**
- Professional PDF creation
- Custom layouts and styling
- Embedded images and QR codes
- Medical-grade emergency cards

### 3.6 Image Processing

**Pillow (PIL) 10.1.0**
- Image viewing and display
- Format conversion (PNG, JPEG, etc.)
- Thumbnail generation
- Image manipulation

### 3.7 QR Code Generation

**qrcode 7.4.2**
- QR code generation for emergency cards
- Patient identification codes
- Quick access to medical records

### 3.8 Hardware Integration

**PySerial 3.5**
- Serial communication with NFC reader
- R20C card reader support
- Real-time card detection

### 3.9 Additional Libraries

- **python-dateutil 2.8.2**: Advanced date/time handling
- **PyPDF2 3.0.1**: PDF reading and text extraction

---

## 4. Project Structure

### 4.1 Directory Organization

```
MedLink/
│
├── main.py                          # Application entry point
│
├── config/                          # Configuration files
│   ├── __init__.py
│   ├── settings.py                  # Application settings
│   ├── localization.py              # Multi-language support
│   └── hardware_config.py           # NFC reader configuration
│
├── core/                            # Business logic layer
│   ├── __init__.py
│   ├── auth_manager.py              # Authentication & authorization
│   ├── data_manager.py              # JSON CRUD operations
│   ├── patient_manager.py           # Patient record management
│   ├── visit_manager.py             # Visit history management
│   ├── lab_manager.py               # Laboratory results
│   ├── imaging_manager.py           # Imaging results
│   ├── surgery_manager.py           # Surgery records
│   ├── hospitalization_manager.py   # Hospitalization tracking
│   ├── vaccination_manager.py       # Vaccination records
│   ├── family_history_manager.py    # Family medical history
│   ├── disability_manager.py        # Disability & special needs
│   ├── nfc_manager.py               # NFC card operations
│   ├── card_manager.py              # Card-user mapping
│   ├── search_engine.py             # Advanced search/filter
│   └── external_api.py              # External system simulation
│
├── gui/                             # User interface layer
│   ├── __init__.py
│   ├── styles.py                    # Design system & themes
│   ├── login_window.py              # Login screen (with NFC)
│   ├── doctor_dashboard.py          # Doctor portal
│   ├── patient_dashboard.py         # Patient portal
│   │
│   └── components/                  # Reusable UI components
│       ├── __init__.py
│       ├── sidebar.py               # Navigation sidebar
│       ├── patient_card.py          # Patient info card
│       ├── visit_card.py            # Visit history card
│       ├── medical_profile_tab.py   # Medical profile display
│       ├── history_tab.py           # Medical history timeline
│       ├── lab_results_tab.py       # Lab results display
│       ├── imaging_tab.py           # Imaging results display
│       ├── file_viewer.py           # File attachment viewer
│       ├── emergency_dialog.py      # Emergency card generator
│       ├── add_visit_dialog.py      # Add visit form
│       ├── add_surgery_dialog.py    # Add surgery form
│       ├── add_hospitalization_dialog.py  # Hospitalization form
│       ├── add_vaccination_dialog.py      # Vaccination form
│       ├── family_history_dialog.py       # Family history form
│       ├── disability_dialog.py           # Disability info form
│       ├── emergency_directives_manager.py # DNR, organ donor settings
│       ├── lifestyle_manager.py            # Lifestyle tracking
│       ├── patient_medical_history.py      # Patient view (read-only)
│       └── link_accounts_dialog.py         # External account linking
│
├── utils/                           # Utility functions
│   ├── __init__.py
│   ├── security.py                  # Encryption utilities
│   ├── validators.py                # Basic input validation
│   ├── enhanced_validators.py       # Advanced validation
│   ├── pdf_generator.py             # PDF creation
│   ├── qr_generator.py              # QR code generation
│   ├── export_manager.py            # Data export
│   ├── date_utils.py                # Date/time helpers
│   └── logger.py                    # Activity logging
│
├── data/                            # JSON data storage
│   ├── users.json                   # System users
│   ├── patients.json                # Patient records (30 patients)
│   ├── visits.json                  # Medical visits
│   ├── lab_results.json             # Lab results
│   ├── imaging_results.json         # Imaging results
│   └── cards.json                   # NFC card mappings
│
├── attachments/                     # File storage
│   ├── prescriptions/               # Prescription PDFs
│   ├── lab_results/                 # Lab result files
│   ├── xrays/                       # X-ray images
│   └── reports/                     # Medical reports
│
├── assets/                          # Application resources
│   ├── icons/                       # UI icons
│   ├── images/                      # Images and logos
│   └── fonts/                       # Custom fonts
│
├── tests/                           # Testing suite
│   ├── generate_test_data.py        # Test data generator
│   ├── test_scenarios.py            # Test case scenarios
│   └── test_enhanced_model.py       # Model validation tests
│
├── docs/                            # Documentation
│   ├── TECHNICAL_DOCUMENTATION.md   # This file
│   ├── USER_MANUAL.md               # User guide
│   └── API_DOCUMENTATION.md         # API reference
│
├── requirements.txt                 # Python dependencies
├── README.md                        # Project overview
└── .gitignore                       # Git ignore rules
```

### 4.2 File Count Summary

- **Core Files**: 15 manager classes
- **GUI Components**: 20+ UI components
- **Utilities**: 8 utility modules
- **Configuration**: 3 config files
- **Data Files**: 6 JSON databases
- **Total Python Files**: 50+

---

## 5. Core Components

### 5.1 Authentication Manager (`core/auth_manager.py`)

**Purpose**: Handles user authentication, session management, and role-based access control.

**Key Features**:
- Password hashing using SHA-256
- Session token generation
- Role-based access (doctor, patient, admin)
- Login attempt monitoring
- NFC card authentication support

**Methods**:
```python
def authenticate(username: str, password: str, role: str) -> Tuple[bool, dict]
    """Authenticate user with credentials"""

def register_patient(national_id: str, full_name: str, password: str) -> Tuple[bool, str]
    """Register new patient account"""

def logout(user_id: str) -> bool
    """End user session"""

def verify_session(session_token: str) -> Optional[dict]
    """Verify active session"""
```

**Security Measures**:
- Passwords never stored in plain text
- SHA-256 one-way hashing
- Session timeout after 30 minutes
- Failed login attempt tracking

---

### 5.2 Data Manager (`core/data_manager.py`)

**Purpose**: Core CRUD operations for all JSON files.

**Key Features**:
- Atomic file operations
- Data validation before write
- Backup on every write
- Thread-safe operations

**Methods**:
```python
def load_data(filename: str) -> dict
    """Load JSON data from file"""

def save_data(filename: str, data: dict) -> bool
    """Save data to JSON file"""

def find_item(filename: str, key: str, value: Any) -> Optional[dict]
    """Find item by key-value pair"""

def update_item(filename: str, item_id: Any, updated_data: dict) -> bool
    """Update existing item"""

def delete_item(filename: str, item_id: Any) -> bool
    """Delete item by ID"""
```

**File Handling**:
- UTF-8 encoding for Arabic support
- Indented JSON for readability
- Atomic writes to prevent corruption
- Automatic backups

---

### 5.3 Patient Manager (`core/patient_manager.py`)

**Purpose**: Manages patient records and medical information.

**Key Features**:
- CRUD operations for patient data
- National ID validation
- Medical history management
- Profile updates

**Methods**:
```python
def create_patient(patient_data: dict) -> Tuple[bool, str]
    """Create new patient record"""

def get_patient_by_id(national_id: str) -> Optional[dict]
    """Retrieve patient by National ID"""

def update_patient(national_id: str, updated_data: dict) -> Tuple[bool, str]
    """Update patient information"""

def get_all_patients() -> List[dict]
    """Get all patient records"""

def search_patients(query: str) -> List[dict]
    """Search patients by name or ID"""
```

**Data Validation**:
- Egyptian National ID format (14 digits)
- Blood type validation
- Phone number format
- Email validation

---

### 5.4 Visit Manager (`core/visit_manager.py`)

**Purpose**: Manages medical visits and consultations.

**Key Features**:
- Visit recording
- Prescription management
- Diagnosis tracking
- Timeline generation

**Methods**:
```python
def add_visit(visit_data: dict) -> Tuple[bool, str]
    """Add new medical visit"""

def get_patient_visits(national_id: str) -> List[dict]
    """Get all visits for patient"""

def get_visit_by_id(visit_id: str) -> Optional[dict]
    """Get specific visit details"""

def update_visit(visit_id: str, updated_data: dict) -> Tuple[bool, str]
    """Update visit information"""
```

**Visit Data Structure**:
- Date and time
- Chief complaint
- Diagnosis
- Treatment plan
- Prescriptions
- Follow-up date
- Attending doctor

---

### 5.5 Surgery Manager (`core/surgery_manager.py`)

**Purpose**: Manages surgical procedure records.

**Key Features**:
- Surgery history tracking
- Procedure documentation
- Recovery time monitoring
- Complication tracking

**Methods**:
```python
def get_patient_surgeries(national_id: str) -> List[dict]
    """Get all surgeries for patient"""

def add_surgery(national_id: str, surgery_data: dict) -> Tuple[bool, str]
    """Add surgery record"""

def update_surgery(surgery_id: str, updated_data: dict) -> Tuple[bool, str]
    """Update surgery information"""

def get_surgeries_count(national_id: str) -> int
    """Get total surgery count"""
```

**Surgery Record Fields**:
- Procedure name
- Date performed
- Hospital/facility
- Surgeon name
- Complications
- Recovery time
- Notes

---

### 5.6 Hospitalization Manager (`core/hospitalization_manager.py`)

**Purpose**: Tracks hospital admissions and stays.

**Key Features**:
- Admission/discharge tracking
- Treatment summary
- Department assignment
- Outcome documentation

**Methods**:
```python
def get_patient_hospitalizations(national_id: str) -> List[dict]
    """Get hospitalization history"""

def add_hospitalization(national_id: str, hosp_data: dict) -> Tuple[bool, str]
    """Add hospitalization record"""

def get_recent_hospitalizations(national_id: str, limit: int) -> List[dict]
    """Get most recent hospitalizations"""
```

---

### 5.7 Vaccination Manager (`core/vaccination_manager.py`)

**Purpose**: Manages vaccination records and schedules.

**Key Features**:
- Vaccination history
- Dose tracking
- Batch number recording
- Next dose reminders

**Methods**:
```python
def get_patient_vaccinations(national_id: str) -> List[dict]
    """Get vaccination records"""

def add_vaccination(national_id: str, vaccine_data: dict) -> Tuple[bool, str]
    """Add vaccination record"""

def get_vaccination_summary(national_id: str) -> dict
    """Get vaccination summary and status"""
```

---

### 5.8 Family History Manager (`core/family_history_manager.py`)

**Purpose**: Manages family medical history for genetic risk assessment.

**Key Features**:
- Parent health status
- Sibling conditions
- Genetic risk factors
- Hereditary disease tracking

**Methods**:
```python
def get_family_history(national_id: str) -> Optional[dict]
    """Get family medical history"""

def update_family_history(national_id: str, history_data: dict) -> Tuple[bool, str]
    """Update family history"""

def get_genetic_risk_summary(national_id: str) -> dict
    """Get genetic risk factors"""
```

---

### 5.9 Disability Manager (`core/disability_manager.py`)

**Purpose**: Manages disability information and accessibility needs.

**Key Features**:
- Disability type documentation
- Mobility aid requirements
- Communication needs
- Accessibility requirements

**Methods**:
```python
def get_disability_info(national_id: str) -> Optional[dict]
    """Get disability information"""

def update_disability_info(national_id: str, disability_data: dict) -> Tuple[bool, str]
    """Update disability information"""

def get_accessibility_summary(national_id: str) -> dict
    """Get accessibility needs summary"""
```

---

### 5.10 NFC Manager (`core/nfc_manager.py`)

**Purpose**: Handles NFC card reader operations.

**Key Features**:
- R20C card reader integration
- Card UID reading
- Card assignment to patients
- Serial communication

**Methods**:
```python
def connect() -> Tuple[bool, str]
    """Connect to NFC reader"""

def read_card_uid(timeout: int) -> Tuple[bool, Optional[str], str]
    """Read card UID"""

def assign_card_to_patient(national_id: str, card_type: str) -> Tuple[bool, str]
    """Assign NFC card to patient"""

def get_patient_from_card(timeout: int) -> Tuple[bool, Optional[dict], str]
    """Read card and return patient data"""
```

**Hardware Configuration**:
- Port: COM3 (configurable)
- Baudrate: 9600
- Timeout: 30 seconds
- Card Type: Mifare Classic 1K

---

### 5.11 Card Manager (`core/card_manager.py`)

**Purpose**: Maps NFC card IDs to user accounts.

**Key Features**:
- Card-to-user mapping
- Doctor card support
- Patient card support
- Card registration

**Methods**:
```python
def get_user_by_card(card_id: str) -> Optional[dict]
    """Get user info from card ID"""

def register_card(card_id: str, user_data: dict) -> bool
    """Register new card"""

def get_patient_by_card(card_id: str) -> Optional[dict]
    """Get patient from card"""
```

**Card Mapping Structure**:
```json
{
  "doctor_cards": {
    "04A1B2C3D4E5F6": {
      "username": "dr.ahmed",
      "name": "Dr. Ahmed Hassan",
      "type": "doctor"
    }
  },
  "patient_cards": {
    "04002791A1FDB6": {
      "national_id": "29501012345678",
      "name": "Mohamed Ali Hassan",
      "type": "patient"
    }
  }
}
```

---

### 5.12 Search Engine (`core/search_engine.py`)

**Purpose**: Advanced search and filtering across all records.

**Key Features**:
- Patient search by ID/name
- Visit filtering
- Lab result search
- Multi-criteria filtering

**Methods**:
```python
def search_patients(query: str) -> List[dict]
    """Search patients by multiple criteria"""

def filter_visits(patient_id: str, filters: dict) -> List[dict]
    """Filter visits by date, doctor, etc."""

def search_by_disease(disease: str) -> List[dict]
    """Find patients with specific disease"""
```

---

### 5.13 Lab Manager (`core/lab_manager.py`)

**Purpose**: Manages laboratory test results.

**Key Features**:
- Lab result storage
- Test type categorization
- Result interpretation
- External lab linking

---

### 5.14 Imaging Manager (`core/imaging_manager.py`)

**Purpose**: Manages imaging and radiology results.

**Key Features**:
- X-ray, CT, MRI, Ultrasound support
- DICOM file handling
- Radiologist reports
- Image viewing

---

### 5.15 External API (`core/external_api.py`)

**Purpose**: Simulates external system integrations.

**Key Features**:
- Lab system API simulation
- Imaging center API simulation
- Pharmacy network simulation
- Future real API integration ready

---

## 6. GUI Components

### 6.1 Design System (`gui/styles.py`)

**Purpose**: Centralized design system for consistent UI.

**Color Palette**:
```python
COLORS = {
    'primary': '#10B981',        # Green
    'secondary': '#059669',      # Dark green
    'bg_dark': '#1a1a1a',        # Dark background
    'bg_medium': '#2d2d2d',      # Medium background
    'bg_light': '#3d3d3d',       # Light background
    'text_primary': '#ffffff',   # White text
    'text_secondary': '#a0a0a0', # Gray text
    'accent': '#3b82f6',         # Blue accent
    'warning': '#f59e0b',        # Orange warning
    'danger': '#ef4444',         # Red danger
    'success': '#10b981'         # Green success
}
```

**Typography**:
```python
FONTS = {
    'heading': ('Segoe UI', 24, 'bold'),
    'subheading': ('Segoe UI', 18, 'bold'),
    'body': ('Segoe UI', 12),
    'body_bold': ('Segoe UI', 12, 'bold'),
    'small': ('Segoe UI', 10),
    'caption': ('Segoe UI', 9)
}
```

**Spacing & Sizing**:
```python
RADIUS = {
    'sm': 6,
    'md': 8,
    'lg': 12,
    'xl': 16
}

SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 20
}
```

---

### 6.2 Login Window (`gui/login_window.py`)

**Purpose**: Application entry point with authentication.

**Key Features**:
- Username/password login
- Role selection (Doctor/Patient)
- NFC card login (background scanning)
- Patient registration
- Forgot password (future)

**NFC Integration**:
- Invisible card scanning
- No UI changes during scan
- Automatic login on card tap
- Card buffer handling

**UI Elements**:
- Logo and branding
- Login form
- Role toggle
- Register button
- Status messages

---

### 6.3 Doctor Dashboard (`gui/doctor_dashboard.py`)

**Purpose**: Main interface for doctors.

**Key Features**:
- Patient search (by ID or card)
- Patient profile view
- Medical history access
- Add visit functionality
- Emergency card generation
- NFC card scanning for patient lookup

**Layout**:
```
┌──────────────────────────────────────────┐
│  [Logo]  MedLink - Dr. Ahmed Hassan    [↗]│
├──────┬───────────────────────────────────┤
│      │  [Search Patient]                 │
│ Side │  ─────────────────────────────    │
│ bar  │                                    │
│      │  Patient Profile Card              │
│ • □  │  ┌──────────────────────────┐    │
│ • ⚕  │  │ Mohamed Ali Hassan        │    │
│ • 📊 │  │ Blood: O+  Age: 30       │    │
│ • 🔬 │  │ Allergies: Penicillin    │    │
│ • 📷 │  └──────────────────────────┘    │
│ • 🚨 │                                    │
│      │  [Tabs: Profile|History|Labs...]  │
│      │  ─────────────────────────────    │
│      │  Tab Content Area                 │
│      │                                    │
└──────┴───────────────────────────────────┘
```

**Tabs**:
1. **Profile**: Basic information, demographics
2. **Medical History**: Visit timeline
3. **Medical Profile**: Surgeries, hospitalizations, vaccinations
4. **Lab Results**: Laboratory test results
5. **Imaging**: X-rays, CT scans, MRI
6. **Emergency Card**: Generate PDF card

**NFC Features**:
- Scan patient card to instantly load profile
- Scan doctor card to switch active doctor
- Background card monitoring
- Visual feedback on successful scan

---

### 6.4 Patient Dashboard (`gui/patient_dashboard.py`)

**Purpose**: Self-service portal for patients.

**Key Features**:
- View own medical records (read-only)
- Download emergency card
- Update contact information
- Link external accounts
- View lab/imaging results
- Manage emergency directives
- Lifestyle self-reporting

**Layout**:
```
┌──────────────────────────────────────────┐
│  [Logo]  MedLink - Mohamed Ali         [↗]│
├──────┬───────────────────────────────────┤
│      │  Dashboard Overview               │
│ Side │  ─────────────────────────────    │
│ bar  │  📊 Stats  🩺 Last Visit          │
│      │  ─────────────────────────────    │
│ • 🏠 │                                    │
│ • 📋 │  [Tabs: Profile|History|Labs...]  │
│ • 🔬 │  ─────────────────────────────    │
│ • 📷 │  Tab Content Area                 │
│ • 🚨 │  (Read-Only Medical Data)         │
│ • ⚙  │                                    │
│      │                                    │
└──────┴───────────────────────────────────┘
```

**Tabs**:
1. **Dashboard**: Overview statistics
2. **Medical History**: View-only history
3. **Lab Results**: View test results
4. **Imaging**: View imaging results
5. **Emergency Card**: Download PDF
6. **Settings**: Update profile, emergency directives

---

### 6.5 Component Library

#### 6.5.1 Patient Card (`gui/components/patient_card.py`)

**Purpose**: Display patient summary information.

**Features**:
- Profile photo placeholder
- Basic demographics
- Critical information (blood type, allergies)
- Emergency contact
- Status badges (DNR, disabilities)

---

#### 6.5.2 Medical Profile Tab (`gui/components/medical_profile_tab.py`)

**Purpose**: Comprehensive medical information display.

**Sections**:
- Surgery History Table
- Hospitalization Records
- Vaccination Status
- Family Medical History
- Disability & Special Needs

**Features**:
- Add new records (doctors only)
- Edit existing records
- View detailed information
- Risk assessment highlights

---

#### 6.5.3 Add Surgery Dialog (`gui/components/add_surgery_dialog.py`)

**Purpose**: Form for recording surgical procedures.

**Fields**:
- Surgery date
- Procedure name
- Hospital/facility
- Surgeon name
- Complications
- Recovery time
- Notes

**Validation**:
- Required fields
- Date format
- Maximum length constraints

---

#### 6.5.4 Add Hospitalization Dialog (`gui/components/add_hospitalization_dialog.py`)

**Purpose**: Record hospital admissions.

**Fields**:
- Admission date
- Discharge date
- Reason for admission
- Hospital name
- Department
- Attending doctor
- Diagnosis
- Treatment summary
- Outcome

---

#### 6.5.5 Add Vaccination Dialog (`gui/components/add_vaccination_dialog.py`)

**Purpose**: Record vaccinations.

**Fields**:
- Vaccine name
- Date administered
- Dose number
- Location
- Batch number
- Next dose due date

---

#### 6.5.6 Family History Dialog (`gui/components/family_history_dialog.py`)

**Purpose**: Document family medical history.

**Sections**:
- Father's health status and conditions
- Mother's health status and conditions
- Siblings information
- Genetic conditions
- Risk assessment

---

#### 6.5.7 Disability Dialog (`gui/components/disability_dialog.py`)

**Purpose**: Document disabilities and accessibility needs.

**Fields**:
- Disability type
- Mobility aids required
- Sensory impairments
- Communication needs
- Accessibility requirements
- Notes

---

#### 6.5.8 Emergency Directives Manager (`gui/components/emergency_directives_manager.py`)

**Purpose**: Patient self-service for emergency preferences.

**Sections**:
1. **DNR (Do Not Resuscitate)**
   - DNR status checkbox
   - DNR order date

2. **Organ Donation**
   - Organ donor checkbox
   - Donor card number
   - Blood transfusion consent
   - Tissue donation consent

3. **Power of Attorney**
   - Designate healthcare proxy
   - Contact information
   - Document date

4. **Advanced Directives**
   - Living will
   - Additional instructions

**Features**:
- Patient can update at any time
- Information appears on emergency card
- Respects patient autonomy

---

#### 6.5.9 Lifestyle Manager (`gui/components/lifestyle_manager.py`)

**Purpose**: Patient self-reporting of lifestyle factors.

**Categories**:
- **Smoking Status**: Never, Former, Current, Occasional
- **Alcohol Consumption**: None, Occasional, Moderate, Heavy
- **Exercise**: Frequency, type, duration
- **Diet**: Type, restrictions
- **Occupation**: Job title, hazards
- **Sleep**: Hours per night
- **Stress Level**: Low, Moderate, High

---

#### 6.5.10 Emergency Dialog (`gui/components/emergency_dialog.py`)

**Purpose**: Generate and display emergency card.

**Features**:
- Live preview of emergency card
- PDF generation button
- QR code with patient ID
- Critical information highlighted
- Print-ready format

---

#### 6.5.11 Patient Medical History (`gui/components/patient_medical_history.py`)

**Purpose**: Read-only view of medical records for patients.

**Features**:
- Complete medical history
- All records visible
- No edit capabilities
- Professional layout
- Easy navigation

---

## 7. NFC Smart Card System

### 7.1 Overview

The NFC Smart Card System provides contactless authentication and patient lookup using RFID technology. This feature enhances security, improves workflow efficiency, and provides a modern user experience.

### 7.2 Hardware Requirements

**NFC Card Reader**:
- Model: R20C USB Card Reader
- Connection: USB serial (COM port)
- Supported Cards: Mifare Classic 1K, Mifare Ultralight
- Operating Frequency: 13.56 MHz
- Reading Distance: 0-10 cm

**NFC Cards**:
- Type: Mifare Classic 1K
- Storage: 1KB (sufficient for UID)
- UID Format: 7-byte hexadecimal
- Example: `04A1B2C3D4E5F6`

### 7.3 System Architecture

```
┌─────────────────────────────────────────────┐
│           NFC Smart Card System             │
├─────────────────────────────────────────────┤
│                                             │
│  [NFC Card] → [R20C Reader] → [USB/Serial] │
│                      ↓                      │
│              [NFCManager]                   │
│                      ↓                      │
│              [CardManager]                  │
│                      ↓                      │
│            [User Authentication]            │
│                      ↓                      │
│          [Dashboard (Doctor/Patient)]       │
│                                             │
└─────────────────────────────────────────────┘
```

### 7.4 Features

#### 7.4.1 Doctor Login via NFC Card

**Workflow**:
1. Doctor approaches login screen
2. Doctor taps NFC card on reader
3. System reads card UID (e.g., `04A1B2C3D4E5F6`)
4. `CardManager` looks up doctor by UID
5. `AuthManager` authenticates doctor
6. Doctor dashboard opens automatically

**Benefits**:
- 2-second login (vs 20+ seconds typing)
- No password memorization required
- Improved security (physical card + possession)
- Professional user experience

**Code Implementation** (`gui/login_window.py`):
```python
def on_key_press(self, event):
    """Handle NFC card scanning (background)"""
    if not self.card_reading_active:
        return
    
    # Don't interfere if typing in fields
    focused = self.focus_get()
    if isinstance(focused, ctk.CTkEntry):
        return
    
    # Enter key = card scan complete
    if event.keysym == "Return":
        card_id = self.card_buffer.strip()
        self.card_buffer = ""
        
        if card_id and len(card_id) >= 8:
            self.process_card(card_id)
```

---

#### 7.4.2 Patient Login via NFC Card

**Workflow**:
1. Patient approaches login screen
2. Patient taps NFC card on reader
3. System reads card UID
4. `CardManager` retrieves patient National ID
5. `PatientManager` loads patient record
6. Patient dashboard opens automatically

**Benefits**:
- No need to remember username/password
- Quick access for patients with low technical literacy
- Suitable for elderly or disabled patients
- Secure physical authentication

---

#### 7.4.3 Patient Search via NFC Card (Doctor Portal)

**Workflow**:
1. Doctor is in dashboard
2. Patient taps card on reader
3. System reads card UID
4. Patient record loads instantly
5. Doctor can view/edit medical information

**Benefits**:
- 3-second patient lookup
- Eliminates typing errors in National ID
- Faster emergency response
- Improved patient flow

**Code Implementation** (`gui/doctor_dashboard.py`):
```python
def process_card(self, card_id: str):
    """Process scanned NFC card"""
    user_info = card_manager.get_user_by_card(card_id)
    
    if user_info:
        user_type = user_info.get('type')
        
        if user_type == 'patient':
            # Load patient record
            national_id = user_info.get('national_id')
            patient = patient_manager.get_patient_by_id(national_id)
            
            if patient:
                self.load_patient(patient)
                self.show_success(f"Patient loaded: {patient['full_name']}")
```

---

#### 7.4.4 Doctor Switching via NFC Card

**Workflow**:
1. Doctor A is logged in
2. Doctor B taps their card
3. System prompts: "Switch to Dr. B?"
4. On confirmation, Doctor A logs out
5. Doctor B dashboard opens

**Use Case**:
- Shared workstations in hospitals
- Shift changes
- Emergency handoffs

---

### 7.5 Card Assignment Process

#### 7.5.1 Assigning Card to Patient

**Admin Workflow**:
1. Open patient profile
2. Click "Assign NFC Card"
3. System prompts: "Please tap card..."
4. Patient taps new card
5. System reads UID
6. UID stored in patient record
7. Confirmation message

**Data Structure** (`data/patients.json`):
```json
{
  "national_id": "29501012345678",
  "full_name": "Mohamed Ali Hassan",
  "nfc_card_uid": "04002791A1FDB6",
  "nfc_card_assigned": true,
  "nfc_card_assignment_date": "2024-11-20",
  "nfc_card_type": "Mifare Classic 1K",
  "nfc_card_status": "active",
  "nfc_card_last_scan": "2024-11-28 10:30:00",
  "nfc_scan_count": 47
}
```

---

#### 7.5.2 Assigning Card to Doctor

**Admin Workflow**:
1. Open user management
2. Select doctor account
3. Click "Assign NFC Card"
4. Doctor taps card
5. System stores UID in `users.json`
6. Doctor can now use card for login

**Data Structure** (`data/users.json`):
```json
{
  "user_id": "D001",
  "username": "dr.ahmed.hassan",
  "full_name": "Dr. Ahmed Hassan Mohamed",
  "role": "doctor",
  "nfc_card_uid": "04A1B2C3D4E5F6",
  "biometric_enabled": true,
  "last_fingerprint_login": "2024-11-28 08:30:00"
}
```

---

### 7.6 Card Management Features

#### 7.6.1 Card Unassignment

**Purpose**: Remove card from user account.

**Use Cases**:
- Lost card
- Card malfunction
- Patient discharge
- Staff termination

**Code** (`core/nfc_manager.py`):
```python
def unassign_card(self, national_id: str) -> Tuple[bool, str]:
    """Remove card assignment from patient"""
    patient = patient_manager.get_patient_by_id(national_id)
    
    if patient and patient.get('nfc_card_assigned'):
        patient['nfc_card_uid'] = None
        patient['nfc_card_assigned'] = False
        patient['nfc_card_status'] = 'unassigned'
        
        patient_manager.update_patient(national_id, patient)
        return True, "Card unassigned successfully"
```

---

#### 7.6.2 Lost Card Reporting

**Purpose**: Mark card as lost for security.

**Workflow**:
1. Patient reports lost card
2. Admin marks card as lost
3. Card status changed to 'lost'
4. Card can no longer be used for login
5. New card must be assigned

---

#### 7.6.3 Card Audit Trail

**Logged Events**:
- Card assignment
- Card unassignment
- Successful scans
- Failed scan attempts
- Lost card reports

**Log File** (`logs/hardware_events.log`):
```
2024-11-28 10:30:15 | NFC_SCAN | Patient: 29501012345678 | Card: 04002791A1FDB6 | SUCCESS
2024-11-28 10:31:42 | NFC_SCAN | Card: 04XXXXXXXX | FAILED | Card not registered
2024-11-28 11:15:00 | CARD_ASSIGNMENT | Patient: 28803151234567 | Card: 04A1B2C3D4E5F6
```

---

### 7.7 Security Considerations

#### 7.7.1 Card Security

**Measures**:
- Card UID is not sufficient alone for login
- System validates card is assigned to active user
- Lost cards immediately disabled
- Audit trail of all card usage
- Physical possession required

**Limitations**:
- Cards can be cloned (UID-only security)
- Physical theft possible
- No PIN protection on card itself

**Future Enhancements**:
- Add PIN requirement for card login
- Use encrypted sectors on Mifare Classic
- Implement challenge-response authentication
- Add biometric verification (fingerprint)

---

#### 7.7.2 Privacy Protection

**Data Protection**:
- Card UID does not contain personal information
- UID is just a lookup key
- Actual data stored securely in database
- Card cannot be read to extract medical info

---

### 7.8 Configuration

**Hardware Configuration** (`config/hardware_config.py`):
```python
NFC_CONFIG = {
    'enabled': True,
    'port': 'COM3',            # Serial port
    'baudrate': 9600,          # Communication speed
    'timeout': 30,             # Read timeout (seconds)
    'retry_attempts': 3,       # Retry on failure
    'card_type': 'Mifare Classic 1K'
}
```

**Supported Card Types**:
- Mifare Classic 1K (1KB storage)
- Mifare Ultralight (64 bytes)
- NTAG213/215/216 (NFC Forum Type 2)

---

### 7.9 Troubleshooting

**Common Issues**:

1. **Reader Not Detected**
   - Check USB connection
   - Verify COM port in Device Manager
   - Install CH340 drivers if needed
   - Restart application

2. **Card Not Reading**
   - Ensure card is within 5cm of reader
   - Check card is not damaged
   - Verify card type is supported
   - Try different card

3. **Wrong User Loaded**
   - Check card assignment in database
   - Verify UID is correct
   - Re-assign card if needed

4. **Slow Performance**
   - Check USB hub power
   - Reduce retry attempts
   - Verify baudrate setting

---

## 8. Data Models

### 8.1 User Model

**File**: `data/users.json`

**Structure**:
```json
{
  "user_id": "D001",
  "username": "dr.ahmed.hassan",
  "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
  "role": "doctor",
  "full_name": "Dr. Ahmed Hassan Mohamed",
  "specialization": "Cardiology",
  "hospital": "Cairo University Hospital",
  "license_number": "MED-EG-12345",
  "email": "ahmed.hassan@hospital.eg",
  "phone": "01012345678",
  "years_experience": 15,
  "nfc_card_uid": "04A1B2C3D4E5F6",
  "biometric_enabled": true,
  "last_login": "2024-11-28 08:30:00",
  "created_at": "2024-11-01 00:00:00"
}
```

**Roles**:
- `doctor`: Full access to patient records
- `patient`: View own records only
- `admin`: System administration (future)
- `nurse`: Limited access (future)

---

### 8.2 Patient Model

**File**: `data/patients.json`

**Note**: All patient data in this file was generated by Claude AI for demonstration purposes. The 30 patient records include realistic Egyptian names, National IDs, medical conditions, and histories that reflect common healthcare scenarios in Egypt.

**Structure**:
```json
{
  "national_id": "29501012345678",
  "full_name": "Mohamed Ali Hassan",
  "date_of_birth": "1995-01-01",
  "age": 29,
  "gender": "Male",
  "blood_type": "O+",
  "phone": "01012345678",
  "email": "mohamed.ali@email.com",
  "address": "15 Tahrir Street, Cairo",
  
  "emergency_contact": {
    "name": "Fatma Ali",
    "relation": "Wife",
    "phone": "01087654321"
  },
  
  "chronic_diseases": ["Type 2 Diabetes", "Hypertension"],
  "allergies": ["Penicillin", "Peanuts"],
  
  "current_medications": [
    {
      "name": "Glucophage 500mg",
      "dosage": "1 tablet",
      "frequency": "Twice daily",
      "started_date": "2020-03-15"
    }
  ],
  
  "surgeries": [
    {
      "surgery_id": "SRG001-1",
      "date": "2018-05-20",
      "procedure": "Appendectomy",
      "hospital": "Cairo University Hospital",
      "surgeon": "Dr. Khaled Mahmoud",
      "complications": "None",
      "notes": "Successful procedure",
      "recovery_time": "2-3 weeks"
    }
  ],
  
  "hospitalizations": [
    {
      "hospitalization_id": "HSP001-1",
      "admission_date": "2018-05-20",
      "discharge_date": "2018-05-23",
      "reason": "Appendectomy",
      "hospital": "Cairo University Hospital",
      "department": "General Surgery",
      "attending_doctor": "Dr. Khaled Mahmoud",
      "diagnosis": "Acute appendicitis",
      "treatment_summary": "Surgical removal of appendix",
      "outcome": "Full recovery"
    }
  ],
  
  "vaccinations": [
    {
      "vaccine_name": "COVID-19 (Pfizer)",
      "date_administered": "2021-06-15",
      "dose_number": "1st dose",
      "location": "Cairo Vaccination Center",
      "batch_number": "PF12345",
      "next_dose_due": "2021-07-15"
    }
  ],
  
  "family_history": {
    "father": {
      "alive": true,
      "age": 65,
      "age_at_death": null,
      "cause_of_death": null,
      "medical_conditions": ["Hypertension", "Diabetes Type 2"]
    },
    "mother": {
      "alive": true,
      "age": 62,
      "medical_conditions": ["Hypertension"]
    },
    "siblings": [
      {
        "relation": "Brother",
        "age": 32,
        "medical_conditions": []
      }
    ],
    "genetic_conditions": [
      "Family history of diabetes",
      "Family history of cardiovascular disease"
    ]
  },
  
  "disabilities_special_needs": {
    "has_disability": false,
    "disability_type": null,
    "mobility_aids": [],
    "hearing_impairment": false,
    "visual_impairment": false,
    "cognitive_impairment": false,
    "communication_needs": [],
    "accessibility_requirements": [],
    "notes": ""
  },
  
  "emergency_directives": {
    "dnr_status": false,
    "dnr_date": null,
    "organ_donor": true,
    "organ_donor_card_number": "OD123456",
    "power_of_attorney": {
      "has_poa": true,
      "name": "Fatma Ali",
      "relation": "Wife",
      "phone": "01087654321",
      "document_date": "2022-01-15"
    },
    "living_will": false,
    "blood_transfusion_consent": true,
    "tissue_donation": true
  },
  
  "lifestyle": {
    "smoking_status": "Never",
    "alcohol_consumption": "None",
    "exercise_frequency": "2-3 times per week",
    "exercise_type": "Walking, Swimming",
    "diet_type": "Balanced",
    "dietary_restrictions": [],
    "occupation": "Engineer",
    "occupation_hazards": [],
    "sleep_hours": 7,
    "stress_level": "Moderate"
  },
  
  "insurance": {
    "provider": "Misr Insurance",
    "policy_number": "INS123456",
    "expiry": "2025-12-31",
    "coverage_type": "Comprehensive"
  },
  
  "nfc_card_uid": "04002791A1FDB6",
  "nfc_card_assigned": true,
  "nfc_card_assignment_date": "2024-11-20",
  "nfc_card_type": "Mifare Classic 1K",
  "nfc_card_status": "active",
  "nfc_card_last_scan": "2024-11-28 10:30:00",
  "nfc_scan_count": 47,
  
  "external_links": {},
  "created_at": "2024-11-01 10:00:00",
  "last_updated": "2024-11-28 10:00:00"
}
```

**Validation Rules**:
- National ID: 14 digits, Egyptian format
- Blood Type: A+, A-, B+, B-, AB+, AB-, O+, O-
- Phone: Egyptian format (01xxxxxxxxx)
- Email: Valid email format
- Age: Calculated from date of birth

---

### 8.3 Visit Model

**File**: `data/visits.json`

**Structure**:
```json
{
  "visit_id": "V001",
  "patient_national_id": "29501012345678",
  "date": "2024-11-15",
  "time": "10:30:00",
  "doctor_id": "D001",
  "doctor_name": "Dr. Ahmed Hassan Mohamed",
  "department": "Cardiology",
  "hospital": "Cairo University Hospital",
  
  "visit_type": "Follow-up",
  "chief_complaint": "Chest pain and shortness of breath",
  
  "vital_signs": {
    "blood_pressure": "140/90",
    "heart_rate": 85,
    "temperature": 37.2,
    "weight": 78.5,
    "height": 175
  },
  
  "diagnosis": "Hypertension, requires medication adjustment",
  "treatment_plan": "Increase Concor dosage, lifestyle modifications",
  
  "prescriptions": [
    {
      "medication": "Concor 10mg",
      "dosage": "1 tablet",
      "frequency": "Once daily",
      "duration": "30 days",
      "instructions": "Take in the morning"
    }
  ],
  
  "lab_orders": ["CBC", "Lipid Profile"],
  "imaging_orders": ["ECG"],
  
  "follow_up_date": "2024-12-15",
  "notes": "Patient responding well to treatment",
  
  "attachments": [
    "attachments/prescriptions/prescription_V001.pdf"
  ],
  
  "created_at": "2024-11-15 10:30:00"
}
```

---

### 8.4 Lab Result Model

**File**: `data/lab_results.json`

**Structure**:
```json
{
  "result_id": "LAB001",
  "patient_national_id": "29501012345678",
  "date": "2024-11-16",
  "lab_name": "Al Borg Medical Laboratories",
  "test_type": "Complete Blood Count (CBC)",
  "status": "completed",
  
  "results": {
    "Hemoglobin": "14.5 g/dL",
    "WBC": "7,200 cells/uL",
    "RBC": "4.8 million cells/uL",
    "Platelets": "250,000 cells/uL",
    "Hematocrit": "42%"
  },
  
  "reference_ranges": {
    "Hemoglobin": "13.5-17.5 g/dL",
    "WBC": "4,500-11,000 cells/uL"
  },
  
  "interpretation": "All values within normal range",
  "ordered_by": "D001",
  "external_link": "https://alborg.com/results/LAB001",
  "attachment": "attachments/lab_results/cbc_2024_11_16.pdf",
  
  "created_at": "2024-11-16 14:00:00"
}
```

---

### 8.5 Imaging Result Model

**File**: `data/imaging_results.json`

**Structure**:
```json
{
  "imaging_id": "IMG001",
  "patient_national_id": "29501012345678",
  "date": "2024-11-17",
  "imaging_center": "Cairo Scan Center",
  "imaging_type": "X-Ray",
  "body_part": "Chest",
  
  "findings": "Clear lung fields, normal heart size",
  "impression": "Normal chest X-ray",
  "radiologist": "Dr. Waleed Taha",
  
  "images": [
    "attachments/xrays/chest_xray_2024_11_17_1.jpg",
    "attachments/xrays/chest_xray_2024_11_17_2.jpg"
  ],
  
  "ordered_by": "D001",
  "external_link": "https://cairoscan.eg/view/IMG001",
  
  "created_at": "2024-11-17 11:00:00"
}
```

---

## 9. Security Implementation

### 9.1 Authentication Security

**Password Hashing**:
```python
import hashlib

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hash: str) -> bool:
    """Verify password against hash"""
    return hash_password(password) == hash
```

**Security Features**:
- SHA-256 one-way hashing
- No plain text passwords stored
- Password cannot be recovered
- Brute force resistant

---

### 9.2 Data Encryption

**Fernet Encryption**:
```python
from cryptography.fernet import Fernet

# Key generation
key = Fernet.generate_key()
cipher = Fernet(key)

# Encryption
encrypted_data = cipher.encrypt(data.encode())

# Decryption
decrypted_data = cipher.decrypt(encrypted_data).decode()
```

**Encrypted Fields**:
- Sensitive medical information
- Personal identification numbers
- Contact information
- Insurance details

---

### 9.3 Session Management

**Session Token**:
```python
import secrets

def generate_session_token() -> str:
    """Generate secure random session token"""
    return secrets.token_urlsafe(32)
```

**Session Storage**:
```python
sessions = {
    "token_abc123": {
        "user_id": "D001",
        "role": "doctor",
        "login_time": "2024-11-28 08:30:00",
        "expires": "2024-11-28 09:00:00"
    }
}
```

**Session Timeout**: 30 minutes of inactivity

---

### 9.4 Role-Based Access Control (RBAC)

**Permission Matrix**:

| Feature | Doctor | Patient | Admin |
|---------|--------|---------|-------|
| View Patient Records | ✅ All | ✅ Own Only | ✅ All |
| Edit Patient Records | ✅ Yes | ❌ No | ✅ Yes |
| Add Visits | ✅ Yes | ❌ No | ✅ Yes |
| View Lab Results | ✅ All | ✅ Own Only | ✅ All |
| Generate Emergency Card | ✅ Yes | ✅ Own Only | ✅ Yes |
| User Management | ❌ No | ❌ No | ✅ Yes |
| System Settings | ❌ No | ❌ No | ✅ Yes |

**Implementation**:
```python
def check_permission(user_role: str, action: str) -> bool:
    """Check if user has permission for action"""
    permissions = {
        'doctor': ['view_all_patients', 'edit_patients', 'add_visits'],
        'patient': ['view_own_records', 'update_own_profile'],
        'admin': ['all']
    }
    
    return action in permissions.get(user_role, [])
```

---

### 9.5 Input Validation

**National ID Validation**:
```python
def validate_national_id(national_id: str) -> Tuple[bool, str]:
    """Validate Egyptian National ID format"""
    # Must be exactly 14 digits
    if not national_id.isdigit() or len(national_id) != 14:
        return False, "National ID must be 14 digits"
    
    # Century digit (2 or 3)
    century = national_id[0]
    if century not in ['2', '3']:
        return False, "Invalid century digit"
    
    # Validate date portion
    year = int(national_id[1:3])
    month = int(national_id[3:5])
    day = int(national_id[5:7])
    
    if month < 1 or month > 12:
        return False, "Invalid month"
    
    if day < 1 or day > 31:
        return False, "Invalid day"
    
    return True, "Valid"
```

**SQL Injection Prevention**:
- No SQL used (JSON storage)
- All inputs validated before processing
- Type checking on all user inputs

---

### 9.6 Audit Logging

**Activity Log**:
```python
def log_activity(user_id: str, action: str, details: dict):
    """Log user activity"""
    log_entry = {
        'timestamp': get_current_datetime(),
        'user_id': user_id,
        'action': action,
        'details': details,
        'ip_address': get_client_ip(),
        'success': True
    }
    
    # Append to log file
    with open('logs/activity.log', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
```

**Logged Events**:
- User login/logout
- Patient record access
- Data modifications
- Failed login attempts
- NFC card scans
- Emergency card generation

---

## 10. API Design

### 10.1 External API Simulation

**Purpose**: Simulate integration with external healthcare systems.

**Lab System API** (`core/external_api.py`):
```python
def fetch_lab_results(patient_id: str, lab_name: str) -> List[dict]:
    """Fetch lab results from external lab system"""
    # Simulated API call
    api_url = f"https://{lab_name}.com/api/results/{patient_id}"
    
    # In production, this would make real HTTP request
    # For now, returns mock data
    
    return [
        {
            'test_type': 'CBC',
            'date': '2024-11-20',
            'results': {...}
        }
    ]
```

**Imaging System API**:
```python
def fetch_imaging_results(patient_id: str, center: str) -> List[dict]:
    """Fetch imaging results from external imaging center"""
    api_url = f"https://{center}.com/api/images/{patient_id}"
    
    return [
        {
            'imaging_type': 'X-Ray',
            'date': '2024-11-21',
            'images': [...]
        }
    ]
```

---

### 10.2 Future API Integration

**RESTful API Design** (Future Implementation):

**Endpoints**:
```
# Authentication
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh

# Patients
GET    /api/v1/patients
GET    /api/v1/patients/{national_id}
POST   /api/v1/patients
PUT    /api/v1/patients/{national_id}
DELETE /api/v1/patients/{national_id}

# Visits
GET    /api/v1/patients/{national_id}/visits
POST   /api/v1/patients/{national_id}/visits
GET    /api/v1/visits/{visit_id}
PUT    /api/v1/visits/{visit_id}

# Lab Results
GET    /api/v1/patients/{national_id}/lab-results
POST   /api/v1/lab-results

# Imaging
GET    /api/v1/patients/{national_id}/imaging
POST   /api/v1/imaging

# Emergency Card
GET    /api/v1/patients/{national_id}/emergency-card
```

**Authentication**: JWT tokens

**Response Format**:
```json
{
  "success": true,
  "data": {...},
  "message": "Operation successful",
  "timestamp": "2024-11-28T10:30:00Z"
}
```

---

## 11. Installation Guide

### 11.1 System Requirements

**Operating System**:
- Windows 10/11 (primary)
- macOS 10.14+
- Linux (Ubuntu 20.04+)

**Python**:
- Version 3.9 or higher
- pip package manager

**Hardware**:
- 4GB RAM minimum (8GB recommended)
- 500MB disk space
- USB port for NFC reader (optional)

**NFC Hardware** (optional):
- R20C USB Card Reader
- Mifare Classic 1K cards

---

### 11.2 Installation Steps

**Step 1: Install Python**

Windows:
```bash
# Download from python.org
# Check "Add Python to PATH" during installation

# Verify installation
python --version
```

macOS:
```bash
# Using Homebrew
brew install python@3.9

# Verify
python3 --version
```

Linux:
```bash
sudo apt update
sudo apt install python3.9 python3-pip

# Verify
python3 --version
```

---

**Step 2: Clone/Download Project**

```bash
# Option 1: Git clone
git clone https://github.com/yourusername/medlink.git
cd medlink

# Option 2: Download ZIP
# Extract to desired location
cd path/to/medlink
```

---

**Step 3: Install Dependencies**

```bash
# Install required packages
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

**requirements.txt**:
```
customtkinter==5.2.0
cryptography==41.0.7
Pillow==10.1.0
qrcode==7.4.2
reportlab==4.0.7
PyPDF2==3.0.1
python-dateutil==2.8.2
pyserial==3.5
```

---

**Step 4: Configure Application**

Edit `config/settings.py`:
```python
# Application settings
APP_NAME = "MedLink"
APP_VERSION = "1.0.0"

# Window settings
WINDOW_SIZE = "1400x800"
MIN_WINDOW_SIZE = (1200, 700)

# Session settings
SESSION_TIMEOUT = 30  # minutes

# Date format
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
```

Edit `config/hardware_config.py` (if using NFC):
```python
NFC_CONFIG = {
    'enabled': True,
    'port': 'COM3',        # Change to your port
    'baudrate': 9600,
    'timeout': 30
}
```

---

**Step 5: Initialize Data**

```bash
# Generate test data
python tests/generate_test_data.py

# This creates:
# - 5 patient records
# - 3 doctor accounts
# - Sample visits, lab results, imaging results
```

---

**Step 6: Run Application**

```bash
# Start MedLink
python main.py
```

**Expected Output**:
```
Starting MedLink v1.0.0...
Loading configuration...
Initializing data manager...
Starting GUI...
Login window opened
```

---

### 11.3 NFC Reader Setup (Optional)

**Step 1: Connect Hardware**
1. Plug R20C reader into USB port
2. Wait for driver installation (Windows)
3. Note the COM port (e.g., COM3)

**Step 2: Install Drivers** (Windows only)
- Download CH340 drivers from manufacturer
- Install and restart computer

**Step 3: Configure Port**
```python
# config/hardware_config.py
NFC_CONFIG = {
    'port': 'COM3',  # Your port here
    ...
}
```

**Step 4: Test Reader**
```bash
python tests/test_nfc_reader.py
```

Expected output:
```
Connecting to NFC reader on COM3...
✅ Reader connected
Waiting for card tap...
✅ Card detected: 04A1B2C3D4E5F6
```

---

### 11.4 Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'customtkinter'"**

Solution:
```bash
pip install customtkinter
```

---

**Issue: "PermissionError: [Errno 13] Permission denied"**

Solution (Windows):
```bash
# Run as administrator
# OR
pip install --user customtkinter
```

Solution (Linux/macOS):
```bash
sudo pip3 install customtkinter
```

---

**Issue: "Could not connect to NFC reader"**

Solutions:
1. Check USB connection
2. Verify COM port in Device Manager
3. Install CH340 drivers
4. Try different USB port
5. Check port permissions (Linux)

---

**Issue: "JSON decode error"**

Solution:
```bash
# Regenerate data files
python tests/generate_test_data.py
```

---

## 12. Development Guidelines

### 12.1 Code Style

**Python Style Guide**: PEP 8

**Key Conventions**:
- Indentation: 4 spaces
- Line length: 100 characters max
- Docstrings: Google style
- Type hints: Use for function parameters and returns

**Example**:
```python
def add_patient(patient_data: dict) -> Tuple[bool, str]:
    """
    Add new patient to system.
    
    Args:
        patient_data: Dictionary containing patient information
        
    Returns:
        Tuple of (success: bool, message: str)
        
    Raises:
        ValueError: If patient_data is invalid
    """
    # Validate data
    if not patient_data.get('national_id'):
        return False, "National ID required"
    
    # Save patient
    success = data_manager.save_patient(patient_data)
    
    if success:
        return True, "Patient added successfully"
    else:
        return False, "Failed to add patient"
```

---

### 12.2 Git Workflow

**Branch Strategy**:
```
main           (production-ready code)
  ├─ develop   (integration branch)
      ├─ feature/patient-portal
      ├─ feature/nfc-login
      ├─ bugfix/search-error
      └─ hotfix/critical-bug
```

**Commit Message Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Example**:
```
feat(nfc): Add NFC card login support

- Implement card reader integration
- Add card-to-user mapping
- Update login window with card scanning

Closes #42
```

---

### 12.3 Testing Guidelines

**Unit Tests**: Test individual functions

Example (`tests/test_validators.py`):
```python
import unittest
from utils.validators import validate_national_id

class TestValidators(unittest.TestCase):
    
    def test_valid_national_id(self):
        result, msg = validate_national_id("29501012345678")
        self.assertTrue(result)
    
    def test_invalid_national_id_length(self):
        result, msg = validate_national_id("123")
        self.assertFalse(result)
    
    def test_invalid_national_id_format(self):
        result, msg = validate_national_id("abcd0123456789")
        self.assertFalse(result)
```

---

**Integration Tests**: Test component interactions

Example (`tests/test_patient_workflow.py`):
```python
def test_add_patient_workflow():
    # Create patient
    patient_data = {
        'national_id': '29501012345678',
        'full_name': 'Test Patient',
        'blood_type': 'O+'
    }
    
    success, msg = patient_manager.create_patient(patient_data)
    assert success == True
    
    # Verify patient exists
    patient = patient_manager.get_patient_by_id('29501012345678')
    assert patient is not None
    assert patient['full_name'] == 'Test Patient'
```

---

### 12.4 Documentation Guidelines

**Code Documentation**:
- All modules must have docstrings
- All classes must have docstrings
- All public functions must have docstrings
- Complex logic should have inline comments

**Module Docstring Example**:
```python
"""
Patient Manager - Handle patient record operations

This module provides CRUD operations for patient records,
including creation, retrieval, updates, and deletion.

Author: MedLink Team
Created: 2024-11-01
Last Modified: 2024-11-28
"""
```

---

## 13. Testing Strategy

### 13.1 Test Data

**Generated by**: Claude AI

All test data in `data/patients.json`, `data/users.json`, and other JSON files was generated by Claude AI to provide realistic scenarios for testing and demonstration.

**Test Data Includes**:
- 30 patient records with Egyptian names and IDs
- 15 doctor accounts from various Egyptian hospitals
- Complete medical histories
- Lab results, imaging results
- Family histories, vaccinations, surgeries

**Regenerate Test Data**:
```bash
python tests/generate_test_data.py
```

---

### 13.2 Test Scenarios

#### Scenario 1: Doctor Login and Patient Search

**Steps**:
1. Start application
2. Select "Doctor" role
3. Login with username: `dr.ahmed.hassan`, password: `password`
4. Dashboard opens
5. Search for patient by National ID: `29501012345678`
6. Patient profile loads
7. Verify blood type, allergies visible

**Expected Result**: ✅ Patient loaded successfully

---

#### Scenario 2: NFC Card Login (Doctor)

**Steps**:
1. Start application
2. Tap doctor's NFC card on reader
3. System reads card UID: `04A1B2C3D4E5F6`
4. Dashboard opens automatically

**Expected Result**: ✅ Instant login (<2 seconds)

---

#### Scenario 3: Add Medical Visit

**Steps**:
1. Doctor logs in
2. Searches and loads patient
3. Click "Add Visit" button
4. Fill visit form:
   - Chief complaint: "Chest pain"
   - Diagnosis: "Angina pectoris"
   - Treatment: "Nitroglycerin prescribed"
5. Click "Save"

**Expected Result**: ✅ Visit added to history

---

#### Scenario 4: Generate Emergency Card

**Steps**:
1. Doctor loads patient profile
2. Click "Emergency Card" tab
3. Review card preview
4. Click "Download PDF"
5. PDF opens

**Expected Result**: ✅ Professional emergency card with QR code

---

#### Scenario 5: Patient Self-Service

**Steps**:
1. Patient logs in with National ID as username
2. Dashboard shows medical overview
3. Navigate to "Medical History" tab
4. View visit records (read-only)
5. Go to "Emergency Card" tab
6. Download emergency card

**Expected Result**: ✅ Patient can view records, download card

---

#### Scenario 6: NFC Patient Lookup (Doctor Portal)

**Steps**:
1. Doctor is logged in
2. Patient taps their NFC card
3. System reads card UID
4. Patient profile loads instantly

**Expected Result**: ✅ 3-second patient lookup

---

### 13.3 Performance Testing

**Metrics**:
- Login time: <2 seconds
- Patient search: <500ms
- Visit history load: <1 second
- PDF generation: <3 seconds
- NFC card read: <2 seconds

---

### 13.4 Security Testing

**Tests**:
1. SQL injection attempts (N/A - JSON storage)
2. Password brute force (rate limiting)
3. Session hijacking (token validation)
4. Unauthorized access (role checking)
5. Data encryption (verify Fernet)

---

## 14. Future Enhancements

### 14.1 Version 2.0 Features

**Database Migration**:
- Migrate from JSON to PostgreSQL/MySQL
- Better performance for large datasets
- Concurrent access support
- ACID compliance

**Web Interface**:
- React/Vue.js frontend
- RESTful API backend
- Mobile-responsive design
- Real-time updates (WebSockets)

**Mobile Apps**:
- iOS app (Swift/SwiftUI)
- Android app (Kotlin)
- Cross-platform (React Native/Flutter)
- Push notifications

---

### 14.2 Advanced Features

**AI/ML Integration**:
- Diagnosis assistance (ML models)
- Drug interaction checker
- Predictive analytics (risk assessment)
- Natural language processing (clinical notes)

**Telemedicine**:
- Video consultations
- Chat with doctor
- Remote monitoring
- Virtual waiting room

**Appointment Scheduling**:
- Calendar integration
- Automated reminders (SMS/Email)
- Waitlist management
- Online booking

---

### 14.3 Integration Plans

**Government Systems**:
- National health insurance database
- Ministry of Health records
- Electronic prescription system
- Death registry

**Healthcare Providers**:
- Hospital information systems (HIS)
- Laboratory information systems (LIS)
- Radiology information systems (RIS)
- Pharmacy management systems

**Insurance Companies**:
- Claim submission
- Pre-authorization requests
- Coverage verification
- Reimbursement tracking

---

### 14.4 Biometric Enhancements

**Fingerprint Login**:
- Already implemented in data model
- Add hardware support
- Enrollment process
- Fallback to password

**Facial Recognition**:
- Patient verification
- Anti-fraud measures
- Liveness detection

**Iris Scanning**:
- High-security areas
- Critical data access

---

### 14.5 Scalability

**Horizontal Scaling**:
- Load balancers
- Multiple app servers
- Database replication
- Caching layer (Redis)

**Cloud Deployment**:
- AWS/Azure/GCP
- Auto-scaling
- Global distribution
- Disaster recovery

---

## 15. Conclusion

### 15.1 Project Summary

MedLink represents a comprehensive solution to healthcare record fragmentation in Egypt. The system successfully demonstrates:

✅ **Technical Excellence**:
- Modern Python architecture
- Clean code organization
- Comprehensive feature set
- Professional UI/UX

✅ **Innovation**:
- NFC smart card integration
- Emergency QR codes
- Advanced search capabilities
- Complete medical records

✅ **Real-World Applicability**:
- Addresses actual healthcare problems
- Scalable architecture
- Security-first design
- User-friendly interface

---

### 15.2 Academic Achievement

**Course Requirements Met**:
- ✅ Advanced Python application
- ✅ File and data interaction
- ✅ GUI development
- ✅ Networking concepts
- ✅ Security implementation
- ✅ Real-world problem solving

**Going Beyond**:
- NFC hardware integration
- Professional-grade PDF generation
- Comprehensive data models
- 50+ Python files
- Full documentation

---

### 15.3 Contact & Support

**Developer**: Youssef
- **Institution**: Elsewedy University of Technology
- **Department**: Computer Science
- **Course**: CET111 - Introduction to Computer and Programming
- **Semester**: Fall 2025

**Skills Demonstrated**:
- Python (5 years experience)
- Laravel (2 years experience)
- AI project development
- Web scraping automation
- Full-stack development

---

### 15.4 Acknowledgments

**Special Thanks**:
- Course instructors for guidance
- Claude AI for test data generation and development assistance
- R20C hardware documentation
- Open-source community

---

### 15.5 License

This project is created for academic purposes as part of CET111 course requirements.

**© 2025 MedLink - Youssef Mekkkawy**

---

## Appendix

### A. Glossary

- **NFC**: Near Field Communication - Wireless technology for short-range data transfer
- **UID**: Unique Identifier - Unique serial number on NFC cards
- **Mifare**: Common NFC card standard
- **CRUD**: Create, Read, Update, Delete operations
- **JSON**: JavaScript Object Notation - Data storage format
- **SHA-256**: Secure Hash Algorithm - Cryptographic hash function
- **Fernet**: Symmetric encryption scheme
- **QR Code**: Quick Response Code - 2D barcode
- **DNR**: Do Not Resuscitate - Medical directive
- **POA**: Power of Attorney - Legal authorization

---

### B. File Size Reference

**Core Files**: ~15KB average
**GUI Components**: ~20KB average
**Data Files**: Variable (depends on records)
**Total Project**: ~5MB (excluding test data)

---

### C. External Resources

**Documentation**:
- CustomTkinter: https://github.com/TomSchimansky/CustomTkinter
- ReportLab: https://www.reportlab.com/docs/
- Cryptography: https://cryptography.io/

**Hardware**:
- R20C NFC Reader: Manufacturer documentation
- Mifare Cards: NXP Semiconductors specification

---

**End of Technical Documentation**

*Last Updated: November 28, 2024*
*Version: 1.0.0*
*Document Author: MedLink Development Team*