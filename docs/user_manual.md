# MedLink - User Manual

## 📖 Table of Contents

- [1. Introduction](#1-introduction)
- [2. Getting Started](#2-getting-started)
- [3. Doctor Portal Guide](#3-doctor-portal-guide)
- [4. Patient Portal Guide](#4-patient-portal-guide)
- [5. NFC Smart Card Usage](#5-nfc-smart-card-usage)
- [6. Emergency Card Guide](#6-emergency-card-guide)
- [7. Frequently Asked Questions](#7-frequently-asked-questions)
- [8. Troubleshooting](#8-troubleshooting)
- [9. Tips & Best Practices](#9-tips--best-practices)
- [10. Support & Contact](#10-support--contact)

---

## 1. Introduction

### 1.1 Welcome to MedLink

**MedLink** is a comprehensive medical records management system designed to centralize and streamline healthcare information in Egypt. Whether you're a doctor managing patient records or a patient accessing your own medical history, MedLink provides a secure, user-friendly platform for all your healthcare data needs.

### 1.2 What Can MedLink Do?

**For Doctors**:
- 👨‍⚕️ Quick patient lookup using National ID or NFC card
- 📋 View complete medical histories
- ➕ Add visits, prescriptions, and diagnoses
- 🏥 Record surgeries, hospitalizations, and vaccinations
- 🚨 Generate emergency cards for patients
- 🔬 Access lab and imaging results

**For Patients**:
- 👤 View your complete medical records
- 📖 Access visit history and prescriptions
- 💾 Download emergency cards (PDF)
- 🔗 Link external lab and imaging accounts
- ⚙️ Manage emergency directives (DNR, organ donation)
- 📊 Self-report lifestyle information

---

### 1.3 System Requirements

**Minimum Requirements**:
- Windows 10/11, macOS 10.14+, or Linux Ubuntu 20.04+
- 4GB RAM
- 500MB free disk space
- Screen resolution: 1280x720 or higher
- Internet connection (for future features)

**Optional Hardware**:
- NFC card reader (R20C model recommended)
- NFC cards (Mifare Classic 1K)
- Printer (for emergency cards)

---

## 2. Getting Started

### 2.1 First Time Setup

#### Step 1: Launch MedLink

1. Locate the MedLink application on your computer
2. Double-click the icon to launch
3. Wait for the login window to appear (~3 seconds)

#### Step 2: Choose Your Role

MedLink has different interfaces for doctors and patients:

**Doctor Portal**:
- Full access to patient records
- Can add and edit medical information
- Manage multiple patients

**Patient Portal**:
- View your own records only
- Read-only access to medical history
- Download emergency cards
- Update personal preferences

---

### 2.2 Login Methods

MedLink offers **three ways to log in**:

#### Method 1: Traditional Login (Username & Password)

**For Doctors**:
1. Select "Doctor" from the role dropdown
2. Enter your username (e.g., `dr.ahmed.hassan`)
3. Enter your password
4. Click "Login"

**For Patients**:
1. Select "Patient" from the role dropdown
2. Enter your National ID as username (14 digits)
3. Enter your password
4. Click "Login"

---

#### Method 2: NFC Card Login (Recommended)

**Requirements**: NFC card reader connected to your computer

**Steps**:
1. Launch MedLink application
2. Tap your NFC card on the reader
3. System automatically logs you in (<2 seconds)
4. Dashboard opens

**Benefits**:
- ⚡ Lightning fast (2 seconds vs 20 seconds)
- 🔐 More secure (physical card required)
- 👴 Easier for elderly or disabled users
- ✅ No password to remember

---

#### Method 3: Patient Registration (New Patients Only)

If you're a new patient without an account:

1. Click "Register New Patient" button
2. Fill in the registration form:
   - **National ID**: 14-digit Egyptian ID
   - **Full Name**: Your complete name
   - **Date of Birth**: DD/MM/YYYY
   - **Gender**: Male/Female
   - **Phone Number**: 11-digit mobile number
   - **Password**: Create a secure password
   - **Confirm Password**: Re-enter password
3. Click "Register"
4. Wait for confirmation message
5. You can now log in with your National ID

---

### 2.3 Password Guidelines

**Strong Password Rules**:
- ✅ At least 8 characters long
- ✅ Mix of letters and numbers
- ✅ Include at least one uppercase letter
- ✅ Include at least one lowercase letter
- ❌ Don't use your name or National ID
- ❌ Don't use common words like "password123"

**Password Security**:
- Never share your password with anyone
- Don't write it down
- Change it regularly (every 3 months)
- Use different passwords for different accounts

---

## 3. Doctor Portal Guide

### 3.1 Dashboard Overview

After logging in as a doctor, you'll see the main dashboard:

```
┌─────────────────────────────────────────────────┐
│  [MedLink Logo]  Dr. Ahmed Hassan Mohamed    [X]│
├─────────┬───────────────────────────────────────┤
│         │                                        │
│ SIDEBAR │   MAIN CONTENT AREA                   │
│         │                                        │
│  🏠 Home│   [Search Patient]                    │
│  📋 List│   ═══════════════                      │
│  🚨 Emrg│                                        │
│  ⚙️ Sett│   Patient Card (appears after search) │
│         │                                        │
│  [Logout│   [Tabs: Profile | History | Labs...] │
│         │                                        │
│         │   Tab Content                         │
│         │                                        │
└─────────┴───────────────────────────────────────┘
```

---

### 3.2 Searching for Patients

#### Method 1: Search by National ID (Manual)

1. Locate the search box at the top of the dashboard
2. Type the patient's 14-digit National ID
3. Press **Enter** or click the **Search** button
4. Patient profile loads

**Example**: `29501012345678`

**Tips**:
- Must be exactly 14 digits
- No spaces or dashes
- If patient not found, check ID accuracy

---

#### Method 2: Search by NFC Card (Fastest)

**Requirements**: Patient must have an NFC card assigned

**Steps**:
1. Be on the doctor dashboard
2. Ask the patient to tap their NFC card on the reader
3. System automatically loads patient profile (<3 seconds)

**Benefits**:
- ⚡ Instant patient lookup
- ❌ Zero typing errors
- 👴 Works for any patient regardless of literacy
- 🚨 Perfect for emergencies

---

### 3.3 Viewing Patient Information

Once a patient is loaded, you'll see:

#### Patient Card (Top Section)

Displays critical information:
- **Name**: Patient's full name
- **Age & Gender**: Automatically calculated
- **Blood Type**: In large, colored badge
- **Allergies**: ⚠️ Highlighted in red/orange
- **Chronic Diseases**: Listed below
- **Emergency Contact**: Name, relation, phone
- **Status Badges**: DNR status, disabilities, etc.

---

#### Navigation Tabs

**Profile Tab**:
- Basic demographics
- Contact information
- Insurance details
- Emergency contact

**Medical History Tab**:
- Chronological list of visits
- Each visit shows:
  - Date and time
  - Doctor name
  - Chief complaint
  - Diagnosis
  - Treatment plan
- Click any visit to see full details

**Medical Profile Tab**:
- Surgery history
- Hospitalization records
- Vaccination records
- Family medical history
- Disability information

**Lab Results Tab**:
- All laboratory test results
- Sorted by date (newest first)
- Filter by test type
- View/download PDF reports

**Imaging Tab**:
- X-rays, CT scans, MRI, Ultrasound
- View images
- Read radiologist reports
- Download DICOM files

**Emergency Card Tab**:
- Live preview of emergency card
- Generate PDF
- Print directly

---

### 3.4 Adding a Medical Visit

**Step-by-Step Guide**:

1. **Search and load patient** (using National ID or NFC card)

2. **Click "Add Visit" button** (top-right corner)

3. **Fill in the visit form**:

   **Section 1: Basic Information**
   - **Date**: Auto-filled (today's date) or select different date
   - **Time**: Auto-filled (current time) or select
   - **Visit Type**: Choose from dropdown
     - First Visit
     - Follow-up
     - Emergency
     - Routine Check-up
     - Consultation

   **Section 2: Clinical Assessment**
   - **Chief Complaint**: Why is the patient here?
     - Example: "Persistent headache for 3 days"
   
   - **Vital Signs** (optional but recommended):
     - Blood Pressure (e.g., 120/80)
     - Heart Rate (beats per minute)
     - Temperature (°C)
     - Weight (kg)
     - Height (cm)

   **Section 3: Diagnosis & Treatment**
   - **Diagnosis**: Your medical assessment
     - Example: "Tension headache, stress-related"
   
   - **Treatment Plan**: Detailed treatment instructions
     - Medications prescribed
     - Dosage and frequency
     - Duration
     - Lifestyle recommendations
     - Follow-up instructions

   **Section 4: Prescriptions** (if any)
   - Click "Add Medication"
   - For each medication:
     - Medication name
     - Dosage (e.g., "500mg")
     - Frequency (e.g., "Twice daily")
     - Duration (e.g., "7 days")
     - Instructions (e.g., "Take with food")
   - Can add multiple medications

   **Section 5: Orders** (optional)
   - **Lab Orders**: Check tests needed
     - CBC (Complete Blood Count)
     - Lipid Profile
     - Blood Sugar
     - Liver Function
     - Kidney Function
     - Custom tests
   
   - **Imaging Orders**: Select if needed
     - X-Ray
     - CT Scan
     - MRI
     - Ultrasound

   **Section 6: Follow-Up**
   - **Follow-up Date**: When should patient return?
   - **Notes**: Any additional information
     - Patient education provided
     - Referrals made
     - Special instructions

   **Section 7: Attachments** (optional)
   - Upload prescription PDFs
   - Attach lab results
   - Include referral letters
   - Add consent forms

4. **Review all information**

5. **Click "Save Visit"** button

6. **Confirmation**: You'll see "Visit added successfully!"

7. **Visit appears in patient's history** immediately

---

### 3.5 Recording Surgery Information

**When to Use**: After patient undergoes any surgical procedure

**Steps**:

1. Load patient profile
2. Go to **"Medical Profile"** tab
3. Scroll to **"Surgery History"** section
4. Click **"Add Surgery"** button
5. Fill in the surgery form:

   **Basic Details**:
   - **Surgery Date**: When was it performed?
   - **Procedure Name**: Type of surgery
     - Examples: "Appendectomy", "Cesarean Section", "Hernia Repair"
   
   **Facility Information**:
   - **Hospital/Facility**: Where performed
   - **Surgeon Name**: Dr. who performed surgery
   - **Department**: Surgical department
   
   **Clinical Details**:
   - **Indications**: Why surgery was needed
   - **Anesthesia Type**: General, Local, Spinal, etc.
   - **Duration**: Surgery length (hours)
   - **Complications**: Any complications during/after
     - If none: Write "None"
     - If any: Describe in detail
   
   **Outcome & Recovery**:
   - **Recovery Time**: Expected time (e.g., "2-3 weeks")
   - **Outcome**: Success, Partial Success, Complications
   - **Follow-up Care**: Post-operative instructions
   - **Notes**: Any additional information

6. **Click "Save Surgery"**

7. **Surgery added to patient's record**

---

### 3.6 Recording Hospitalization

**When to Use**: When patient is admitted to hospital

**Steps**:

1. Load patient profile
2. Go to **"Medical Profile"** tab
3. Scroll to **"Hospitalization History"** section
4. Click **"Add Hospitalization"** button
5. Fill in the form:

   **Admission Details**:
   - **Admission Date**: When patient was admitted
   - **Admission Time**: Time of admission
   - **Reason for Admission**: Why hospitalized
     - Example: "Severe pneumonia"
   
   **Facility Information**:
   - **Hospital**: Which hospital
   - **Department**: Ward/Department
     - ICU, General Ward, Emergency, etc.
   - **Attending Doctor**: Primary doctor
   - **Room Number** (optional)
   
   **Clinical Information**:
   - **Diagnosis**: Primary and secondary diagnoses
   - **Treatment Summary**: What was done
     - Medications given
     - Procedures performed
     - Interventions
   - **Daily Progress Notes** (optional)
   
   **Discharge Details**:
   - **Discharge Date**: When patient left
   - **Discharge Time**: Time of discharge
   - **Outcome**: 
     - Full Recovery
     - Improved
     - Transferred
     - Against Medical Advice
     - Deceased
   - **Discharge Instructions**: Home care instructions
   - **Follow-up Appointments**: When to return

6. **Click "Save Hospitalization"**

---

### 3.7 Recording Vaccinations

**When to Use**: After administering any vaccine

**Steps**:

1. Load patient profile
2. Go to **"Medical Profile"** tab
3. Scroll to **"Vaccination Records"** section
4. Click **"Add Vaccination"** button
5. Fill in the form:

   **Vaccine Details**:
   - **Vaccine Name**: Full name
     - Examples: "COVID-19 (Pfizer)", "Influenza", "Hepatitis B"
   - **Date Administered**: When given
   - **Dose Number**: 
     - "1st dose", "2nd dose", "Booster"
   
   **Administration Details**:
   - **Location**: Where vaccine was given
     - Example: "Cairo Vaccination Center"
   - **Batch Number**: From vaccine vial
   - **Expiry Date**: Vaccine expiration
   - **Route**: IM, SC, Oral, etc.
   - **Site**: Left arm, Right arm, etc.
   
   **Schedule**:
   - **Next Dose Due**: When next dose needed
     - Leave blank if complete
   
   **Notes**:
   - Any reactions or side effects
   - Special circumstances

6. **Click "Save Vaccination"**

---

### 3.8 Documenting Family History

**Purpose**: Record family medical history for genetic risk assessment

**Steps**:

1. Load patient profile
2. Go to **"Medical Profile"** tab
3. Scroll to **"Family Medical History"** section
4. Click **"Edit Family History"** button
5. Fill in for each family member:

   **Father's Information**:
   - **Status**: Alive or Deceased
   - **Current Age** (if alive) OR **Age at Death**
   - **Cause of Death** (if deceased)
   - **Medical Conditions**: Check all that apply
     - Hypertension
     - Diabetes
     - Heart Disease
     - Cancer (specify type)
     - Stroke
     - Other (specify)
   
   **Mother's Information**:
   - Same fields as father
   
   **Siblings**:
   - Add each sibling
   - Age
   - Gender
   - Medical conditions
   - Can add multiple siblings
   
   **Genetic/Hereditary Conditions**:
   - Any known genetic disorders
   - Family patterns of disease
   - Risk factors

6. **Click "Save Family History"**

7. **System calculates genetic risk factors**

8. **Risk summary displayed**:
   - High-risk conditions highlighted
   - Recommendations for screening
   - Preventive measures suggested

---

### 3.9 Recording Disability Information

**Purpose**: Document disabilities and special needs for better care

**Steps**:

1. Load patient profile
2. Go to **"Medical Profile"** tab
3. Scroll to **"Disability & Special Needs"** section
4. Click **"Edit Disability Information"** button
5. Fill in the form:

   **Disability Status**:
   - **Has Disability**: Yes/No
   - If No, click Save and you're done
   - If Yes, continue below:
   
   **Type of Disability**:
   - Physical
   - Visual
   - Hearing
   - Cognitive
   - Speech
   - Multiple
   - Other (specify)
   
   **Mobility Needs**:
   - **Wheelchair Required**: Yes/No
   - **Walker/Cane**: Yes/No
   - **Other Aids**: Specify
   
   **Sensory Impairments**:
   - **Hearing Impairment**: None, Mild, Moderate, Severe, Profound
   - **Hearing Aid Used**: Yes/No
   - **Sign Language**: Yes/No
   - **Visual Impairment**: None, Mild, Moderate, Severe, Blind
   - **Uses Braille**: Yes/No
   
   **Communication Needs**:
   - Requires interpreter (language)
   - Requires sign language interpreter
   - Written communication preferred
   - Other (specify)
   
   **Accessibility Requirements**:
   - Wheelchair-accessible entrance
   - Elevator access needed
   - Ground floor preferred
   - Extended appointment time
   - Assistance with forms
   - Other (specify)
   
   **Additional Notes**:
   - Any other relevant information
   - Special accommodations needed
   - Emergency considerations

6. **Click "Save Disability Information"**

7. **Badge appears on patient card** for quick identification

---

### 3.10 Generating Emergency Cards

**Purpose**: Create printable emergency cards for patients to carry

**Steps**:

1. Load patient profile

2. Click **"Emergency Card"** tab

3. **Review the card preview**:
   - Patient name and photo
   - Blood type (large, prominent)
   - Allergies (highlighted)
   - Chronic diseases
   - Current medications
   - Emergency contact
   - QR code (for quick scanning)

4. **Click "Generate PDF"** button

5. **PDF opens** in new window

6. **Options**:
   - **Save**: Save PDF to computer
   - **Print**: Print directly
   - **Email**: Send to patient (future feature)

7. **Advise patient** to:
   - Print and fold card
   - Keep in wallet at all times
   - Update when information changes

**Emergency Card Uses**:
- 🚨 ER/Trauma situations
- 🚑 Ambulance personnel
- 👨‍⚕️ New doctors/hospitals
- 🌍 Travel abroad
- 🏃 Sports/Activities

---

### 3.11 Logging Out

**Important**: Always log out when finished

**Steps**:
1. Click your name (top-right corner)
2. Select **"Logout"** from dropdown
3. OR click **"Logout"** button in sidebar
4. Confirm logout
5. Login screen appears

**Security Reminder**:
- Never leave dashboard open unattended
- Always log out on shared computers
- Session expires after 30 minutes of inactivity

---

## 4. Patient Portal Guide

### 4.1 Dashboard Overview

After logging in as a patient, you'll see:

```
┌─────────────────────────────────────────────────┐
│  [MedLink Logo]  Mohamed Ali Hassan          [X]│
├─────────┬───────────────────────────────────────┤
│         │                                        │
│ SIDEBAR │   DASHBOARD OVERVIEW                  │
│         │                                        │
│  🏠 Home│   ┌─────────┬─────────┬─────────┐    │
│  📋 Hist│   │ 📊 Stats│🩺 Visits│💊 Meds  │    │
│  🔬 Labs│   └─────────┴─────────┴─────────┘    │
│  📷 Imag│                                        │
│  🚨 Card│   Recent Activity                     │
│  ⚙️ Sett│   ─────────────────                   │
│         │                                        │
│  [Logout│   • Last visit: Nov 15, 2024          │
│         │   • Lab results: 2 new                │
│         │   • Medications: 3 active             │
└─────────┴───────────────────────────────────────┘
```

---

### 4.2 Viewing Your Medical History

**Steps**:

1. Click **"Medical History"** in sidebar

2. You'll see a complete timeline of your medical visits:
   - Most recent at top
   - Each visit shows:
     - Date and time
     - Doctor's name
     - Hospital/clinic
     - Chief complaint
     - Diagnosis
     - Prescribed medications

3. **Click any visit** to see full details:
   - Complete visit notes
   - Vital signs recorded
   - Treatment plan
   - Prescriptions
   - Follow-up instructions
   - Attached documents

**Note**: All information is **read-only**. You cannot edit medical history. Only your doctor can add or modify visits.

---

### 4.3 Viewing Lab Results

**Steps**:

1. Click **"Lab Results"** in sidebar

2. You'll see all your laboratory tests:
   - Test name (e.g., "Complete Blood Count")
   - Date performed
   - Lab facility name
   - Status (Complete/Pending)

3. **Click any result** to view:
   - Individual test values
   - Reference ranges (normal values)
   - Interpretation
   - Doctor's comments

4. **Download PDF**: Click download icon to save report

**Understanding Results**:
- 🟢 Green: Values in normal range
- 🟡 Yellow: Slightly abnormal (review with doctor)
- 🔴 Red: Abnormal (consult doctor immediately)

---

### 4.4 Viewing Imaging Results

**Steps**:

1. Click **"Imaging"** in sidebar

2. You'll see all imaging studies:
   - Type (X-Ray, CT, MRI, Ultrasound)
   - Body part examined
   - Date performed
   - Imaging center

3. **Click any study** to view:
   - Radiologist's report
   - Findings
   - Impression
   - Images (if available)

4. **View Images**: Click to zoom and examine

---

### 4.5 Downloading Your Emergency Card

**Important**: Every patient should have an emergency card!

**Steps**:

1. Click **"Emergency Card"** in sidebar

2. **Review your emergency card preview**:
   - Check all information is current
   - Verify allergies listed
   - Confirm medications accurate
   - Check emergency contact

3. **If anything is outdated**:
   - Contact your doctor to update
   - OR update in Settings (contact info only)

4. **Click "Download PDF"**

5. **PDF opens** - you can:
   - Save to computer
   - Email to yourself
   - Print multiple copies

6. **Important Steps**:
   - Print the card on cardstock (thick paper)
   - Cut along the dotted lines
   - Fold in half
   - Laminate if possible (recommended)
   - Keep in your wallet at all times
   - Give copies to family members
   - Keep one in car glove compartment

**When Emergency Card is Useful**:
- 🚨 Medical emergencies
- 🚑 Ambulance calls
- 🏥 New hospital visits
- ✈️ International travel
- 🎿 Sports activities
- 🚗 Car accidents

---

### 4.6 Managing Emergency Directives

**Purpose**: Document your wishes for end-of-life care

**Steps**:

1. Click **"Settings"** in sidebar
2. Click **"Emergency Directives"** tab
3. You'll see several sections:

#### Section 1: Do Not Resuscitate (DNR)

**What is DNR?**
A DNR order tells medical staff not to perform CPR if your heart stops or you stop breathing.

**To Set DNR**:
1. Check **"I have a Do Not Resuscitate (DNR) order"**
2. Enter the date of your DNR order
3. Upload DNR document (if you have one)

**Important**: Discuss DNR with your doctor and family before setting.

---

#### Section 2: Organ Donation

**What is Organ Donation?**
Choosing to donate your organs after death to save others' lives.

**To Register as Donor**:
1. Check **"I wish to be an organ donor"**
2. Enter donor card number (if you have one)
3. Check **"I consent to blood transfusions"** (if yes)
4. Check **"I consent to tissue donation for research"** (if yes)

---

#### Section 3: Power of Attorney for Healthcare

**What is Healthcare POA?**
Designating someone to make medical decisions for you if you're unable to.

**To Designate POA**:
1. Check **"I have a healthcare power of attorney"**
2. Enter the person's information:
   - Full name
   - Relationship (spouse, child, parent, etc.)
   - Phone number
3. Enter document date (when POA was signed)
4. Upload POA document (optional)

**Important**: The person you designate should:
- Know your wishes
- Be willing to make difficult decisions
- Be legally able to serve as POA

---

#### Section 4: Living Will

**What is a Living Will?**
A document stating your wishes for medical treatment if you're terminally ill.

**To Set Living Will**:
1. Check **"I have a living will"**
2. Upload document (if you have one)

---

#### Section 5: Additional Instructions

Free text area for any other instructions:
- Religious preferences
- Cultural considerations
- Specific treatment preferences
- Who should be contacted
- Burial wishes

**Save Changes**:
- Click **"Save Emergency Directives"** button
- Confirmation message appears
- Information added to emergency card

---

### 4.7 Self-Reporting Lifestyle Information

**Purpose**: Help doctors understand your lifestyle for better care

**Steps**:

1. Click **"Settings"** in sidebar
2. Click **"Lifestyle"** tab
3. Fill in each section:

#### Smoking
- **Status**: Never / Former / Current / Occasional
- **If Current**: Cigarettes per day
- **Years Smoked**: Total years

#### Alcohol
- **Consumption**: None / Occasional / Moderate / Heavy
- **Drinks per week**: Number

#### Exercise
- **Frequency**: Daily / 4-6x week / 2-3x week / Once week / Rarely / Never
- **Type**: Walking, Running, Swimming, Gym, Sports, etc.
- **Duration**: Minutes per session

#### Diet
- **Type**: Balanced / Vegetarian / Vegan / Keto / Low-carb / Other
- **Dietary Restrictions**: List any (e.g., gluten-free, lactose-free)
- **Eating Habits**: Regular meals / Irregular / Skip meals

#### Occupation
- **Job Title**: Your current job
- **Work Environment**: Office / Field / Factory / etc.
- **Occupational Hazards**: Any exposure to harmful substances
- **Stress Level**: Low / Moderate / High / Very High

#### Sleep
- **Hours per Night**: Average sleep duration
- **Sleep Quality**: Good / Fair / Poor
- **Sleep Issues**: Insomnia / Sleep apnea / Snoring / etc.

#### Stress
- **Stress Level**: Low / Moderate / High / Very High
- **Stress Sources**: Work / Family / Financial / Health / Other

4. **Click "Save Lifestyle Information"**

**Why This Matters**:
- Helps doctors identify risk factors
- Assists in diagnosis
- Guides preventive care recommendations
- Supports treatment planning

---

### 4.8 Updating Contact Information

**Steps**:

1. Click **"Settings"** in sidebar
2. Click **"Profile"** tab
3. You can update:
   - Phone number
   - Email address
   - Home address
   - Emergency contact name
   - Emergency contact phone

4. **Click "Save Changes"**

**Note**: You cannot change:
- National ID
- Name
- Date of birth
- Blood type

To change these, contact your doctor or hospital administrator.

---

### 4.9 Linking External Accounts

**Purpose**: Connect your lab and imaging center accounts to MedLink

**Benefits**:
- Automatic result import (future feature)
- Centralized records
- No manual entry needed

**Steps**:

1. Click **"Settings"** in sidebar
2. Click **"Linked Accounts"** tab
3. Click **"Add Account"** button
4. Select account type:
   - Laboratory (Al Borg, Bio Lab, etc.)
   - Imaging Center (Scan Center, Cairo Scan, etc.)
5. Enter your account information:
   - Account ID or Patient ID from that facility
   - Username (if required)
   - Authorization code (provided by facility)
6. Click **"Link Account"**
7. System verifies connection
8. Account added to list

**Managing Linked Accounts**:
- View all linked accounts
- Sync results manually
- Unlink account if needed

---

## 5. NFC Smart Card Usage

### 5.1 What is an NFC Smart Card?

**NFC** stands for "Near Field Communication" - a wireless technology that allows devices to communicate when they're close together (within 5cm).

**NFC Smart Card for MedLink**:
- Small plastic card (like a credit card)
- Contains a unique ID number
- Linked to your MedLink account
- Enables instant login and patient lookup

**Benefits**:
- ⚡ 2-second login (vs 20+ seconds typing)
- ❌ No passwords to remember
- 🔐 More secure (physical card required)
- 👴 Easier for elderly users
- 🏥 Perfect for busy hospital environments

---

### 5.2 Getting an NFC Card

**For Doctors**:

1. Request card from hospital administrator
2. Administrator assigns card to your account
3. During assignment:
   - You'll tap your new card on the reader
   - System reads the unique ID
   - ID is linked to your doctor account
4. You receive the card
5. You can now use it for login

**For Patients**:

1. Request card during hospital visit
2. Doctor or receptionist assigns card
3. You tap the card on reader
4. System links card to your National ID
5. You receive the card
6. You can now use it for login and check-in

**Card Specifications**:
- Type: Mifare Classic 1K
- Size: Standard credit card size
- Durability: 5-10 years with normal use
- Waterproof: Yes
- Washable: Yes (but avoid harsh chemicals)

---

### 5.3 Using Your NFC Card

#### For Doctor Login

**Steps**:
1. Launch MedLink application
2. Wait for login screen (don't type anything)
3. Hold your NFC card near the reader (within 5cm)
4. Keep card steady for 1-2 seconds
5. You'll hear a beep
6. Dashboard opens automatically

**Tips**:
- Keep card flat against reader
- Don't move card during scan
- If it doesn't work, try again
- Check if reader is connected

---

#### For Patient Login

**Steps**:
1. Launch MedLink application
2. Hold your NFC card near the reader
3. Keep card steady for 1-2 seconds
4. Beep sound indicates successful scan
5. Patient dashboard opens automatically

**Advantages**:
- No need to remember National ID or password
- Great for patients with memory issues
- Works for any literacy level
- Faster than typing

---

#### For Patient Lookup (Doctor Portal)

**Scenario**: Doctor needs to access a patient's records

**Steps**:
1. Doctor is logged into dashboard
2. Patient arrives for appointment
3. Patient taps their NFC card on the reader
4. System instantly loads patient's profile
5. Doctor can start consultation immediately

**Time Saved**:
- Traditional: ~30 seconds (find ID, type, search)
- NFC Card: ~3 seconds (tap card, profile loads)
- **Savings**: 27 seconds per patient × 40 patients/day = **18 minutes saved daily!**

---

### 5.4 Card Security & Safety

#### Security Features

**What Protects Your Card**:
- Card only contains a unique ID number (like a serial number)
- No personal information stored on the card
- Card is just a "key" to your account
- System checks if card is active before allowing access
- Lost cards can be immediately deactivated

**What's NOT on the Card**:
- ❌ Your name
- ❌ National ID
- ❌ Medical information
- ❌ Passwords
- ❌ Any sensitive data

**If Someone Finds Your Card**:
- They can't read your medical information from it
- They would still need the MedLink system
- System logs all card usage
- Suspicious activity is monitored

---

#### Keeping Your Card Safe

**Do's**:
- ✅ Keep card in a protective sleeve
- ✅ Store in wallet or card holder
- ✅ Keep away from strong magnets
- ✅ Report lost card immediately
- ✅ Check card works occasionally

**Don'ts**:
- ❌ Don't bend or fold the card
- ❌ Don't expose to extreme temperatures
- ❌ Don't punch holes in the card
- ❌ Don't store near strong magnets
- ❌ Don't lend to others

---

### 5.5 Lost or Stolen Card

**If Your Card is Lost**:

**Immediate Steps**:
1. Report to hospital administrator or IT support IMMEDIATELY
2. Card will be marked as "lost" in system
3. Card can no longer be used for login
4. You'll need to use password login temporarily

**Getting a Replacement**:
1. Visit hospital administrator
2. Request new card
3. New card will be assigned to your account
4. Old card remains deactivated
5. Start using new card

**Important**:
- Report lost cards within 24 hours
- Don't delay reporting
- Old card cannot be reactivated for security

---

### 5.6 Card Troubleshooting

**Problem 1: Card Not Reading**

**Possible Causes**:
- Card not close enough to reader
- Card moved during scan
- Reader not connected
- Card damaged

**Solutions**:
1. Hold card flat against reader
2. Keep card still for 2 full seconds
3. Try different angle/position
4. Check reader connection (USB cable)
5. Try a different card (if available)
6. Contact IT support if issue persists

---

**Problem 2: "Card Not Registered" Error**

**Cause**: Card ID not linked to any account

**Solutions**:
1. Use password login instead
2. Contact administrator to assign card
3. Verify it's your card (not someone else's)

---

**Problem 3: "Card Disabled" Error**

**Cause**: Card has been deactivated (lost/stolen report)

**Solutions**:
1. If you reported it lost: Request new card
2. If you didn't report it: Contact administrator (may be system error)
3. Use password login meanwhile

---

**Problem 4: Wrong User Loaded**

**Cause**: Card is assigned to different person

**Solutions**:
1. Verify it's your card (check card sleeve/label)
2. If wrong assignment: Contact administrator
3. Card will be reassigned to correct person

---

## 6. Emergency Card Guide

### 6.1 What is an Emergency Card?

An **Emergency Medical Card** is a wallet-sized card containing your critical medical information that can save your life in an emergency.

**What's on the Card**:
- Your name and photo
- Blood type (large and prominent)
- Known allergies
- Chronic diseases
- Current medications
- Emergency contact
- QR code (for quick digital access)

**Why You Need One**:
- 🚨 Emergency rooms can access info instantly
- 🚑 Paramedics know your allergies
- 👨‍⚕️ Unconscious? Card speaks for you
- ⚠️ Prevents medication errors
- 🌍 Works anywhere (no internet needed)

---

### 6.2 When to Use Emergency Card

**Critical Situations**:
- Car accidents
- Falls or injuries
- Heart attacks or strokes
- Allergic reactions
- Unconsciousness
- Unable to communicate

**Non-Critical but Useful**:
- New doctor visits
- Hospital admissions
- Pharmacy visits
- International travel
- Sports activities
- Outdoor adventures

---

### 6.3 Creating Your Emergency Card

**Patients**:
1. Log into patient portal
2. Click "Emergency Card" in sidebar
3. Review information
4. Click "Download PDF"
5. Print on cardstock
6. Follow folding instructions

**Doctors** (for patients):
1. Load patient profile
2. Click "Emergency Card" tab
3. Review information
4. Click "Generate PDF"
5. Give to patient

---

### 6.4 Printing & Preparing Card

**Materials Needed**:
- Cardstock paper (thick paper)
- Color printer
- Scissors
- Laminating pouch (optional but recommended)
- Laminating machine (if laminating)

**Printing Instructions**:

1. **Print the PDF**:
   - Use cardstock (65-110 lb weight)
   - Print in color
   - Print at 100% scale (don't resize)
   - Use high quality setting

2. **Cut the Card**:
   - Cut along the dotted outer lines
   - Use sharp scissors for clean edges
   - Be careful with QR code area

3. **Fold the Card**:
   - Fold along the center dashed line
   - Make a sharp, clean fold
   - Align edges carefully

4. **Laminate** (Highly Recommended):
   - Place folded card in laminating pouch
   - Run through laminating machine
   - Let cool for 1 minute
   - Trim excess laminate

5. **Final Touches**:
   - Check QR code is visible
   - Verify all text is readable
   - Test QR code with phone camera

---

### 6.5 Where to Keep Emergency Cards

**Primary Card**:
- In your wallet (most important!)
- Behind your driver's license
- In dedicated card slot

**Backup Cards**:
- Give one to spouse/partner
- Keep one in car glove compartment
- Keep one in home emergency kit
- Give one to adult children
- Keep one at work desk
- Keep one in travel bag

**Don't Keep Cards**:
- ❌ In checked luggage (might get lost)
- ❌ Loose in purse/bag (might fall out)
- ❌ In phone case only (phone might die/break)

---

### 6.6 Updating Your Emergency Card

**When to Update**:
- New allergy diagnosed
- Medication changes
- New chronic disease
- Blood type correction
- Contact information changes
- Address changes

**How Often to Update**:
- Review every 6 months minimum
- Update immediately after major changes
- Replace worn/damaged cards

**Update Process**:
1. Log into MedLink
2. Doctor updates your information
3. Download new emergency card
4. Print new card
5. Destroy old card (shred it)
6. Distribute new cards

---

### 6.7 QR Code on Emergency Card

**What is the QR Code?**
- Square barcode on your card
- Contains your unique patient ID
- Can be scanned with smartphones

**How It Works**:
1. Emergency personnel scan QR code with phone camera
2. Code links to your full MedLink record (if online system available)
3. Instant access to complete medical history

**Current Status**:
- QR code contains your National ID
- Future updates will link to online portal
- Works with any smartphone camera

**Scanning Instructions** (for medical personnel):
1. Open phone camera app
2. Point camera at QR code
3. Tap notification that appears
4. Patient ID displayed
5. Enter ID into MedLink system

---

## 7. Frequently Asked Questions

### 7.1 General Questions

**Q: Is MedLink secure?**

A: Yes! MedLink uses industry-standard security:
- SHA-256 password encryption
- Fernet data encryption
- Role-based access control
- Activity logging
- 30-minute session timeout

**Q: Can I access MedLink from home?**

A: Currently, MedLink is a desktop application installed at hospitals. Future versions will include web and mobile access.

**Q: How much does MedLink cost?**

A: MedLink is provided by your healthcare facility. Check with your hospital about any fees.

**Q: What happens to my data if I switch hospitals?**

A: Your records remain in the MedLink system. If your new hospital uses MedLink, your data is immediately available. If not, you can request a data export.

---

### 7.2 Account & Login Questions

**Q: I forgot my password. What do I do?**

**For Patients**:
1. Contact your hospital's reception
2. They will verify your identity
3. They can reset your password
4. You'll receive a temporary password
5. Change it on first login

**For Doctors**:
1. Contact hospital IT department
2. Verify identity
3. Password reset within 24 hours

**Q: Can I change my username?**

**Patients**: No, your National ID is your permanent username.

**Doctors**: Contact hospital administrator to request username change.

**Q: How long does my session last?**

A: Sessions last 30 minutes of inactivity. After 30 minutes, you'll be automatically logged out for security.

**Q: Can I use MedLink on multiple computers?**

A: Yes, log in on any computer with MedLink installed. You can only have one active session at a time.

---

### 7.3 Medical Records Questions

**Q: Can I edit my medical history?**

A: No, only authorized doctors can add or edit medical records. This maintains the integrity and accuracy of your medical history.

**Q: Can I delete a visit record?**

A: No, medical records are permanent for legal and medical continuity reasons. If there's an error, contact your doctor to add a correction note.

**Q: How far back does my history go?**

A: MedLink stores your complete history from the date your hospital started using the system.

**Q: Can I get a copy of my complete medical records?**

A: Yes, you can:
- View all records online in your patient portal
- Download emergency card (summary)
- Request full data export from hospital (may require fee)

---

### 7.4 NFC Card Questions

**Q: Do I need an NFC card to use MedLink?**

A: No, NFC cards are optional. They provide faster login, but you can always use your username and password.

**Q: How much does an NFC card cost?**

A: Check with your hospital. Most hospitals provide cards free or for a small administrative fee (usually 20-50 EGP).

**Q: Can someone else use my NFC card?**

A: The card itself doesn't require additional authentication, but:
- System logs all card usage
- Suspicious activity is monitored
- Lost cards can be deactivated instantly
- Medical information can't be read from the card

**Q: What if my card stops working?**

A: Contact hospital administrator. You'll receive a replacement card. Common causes:
- Physical damage
- Strong magnetic exposure
- Normal wear after 5-10 years

**Q: Can I have multiple NFC cards?**

A: Typically one card per person. However, you can request a backup card if you need one for a different location (work vs home, for example).

---

### 7.5 Emergency Card Questions

**Q: How often should I print a new emergency card?**

A: Print a new card whenever:
- Information changes (medications, allergies, etc.)
- Card is lost or damaged
- Card becomes worn or illegible
- At least once per year as a precaution

**Q: Can I keep a digital copy on my phone instead?**

A: You can, but **always carry the physical card too**:
- Phone battery might die
- Phone might be damaged in accident
- Paper card works anywhere, anytime
- Emergency personnel expect physical cards

**Q: What if my emergency card information is outdated?**

A: Contact your doctor immediately to update your information, then print a new card. Outdated cards can be dangerous!

**Q: Can family members have copies of my emergency card?**

A: Yes! Print multiple copies and give to:
- Spouse/partner
- Adult children
- Parents
- Close relatives
- Trusted friends

---

### 7.6 Privacy Questions

**Q: Who can see my medical records?**

**Doctors**: Can see all patient records (needed for care)
**Patients**: Can only see your own records
**Admins**: Can see records for system maintenance (bound by confidentiality)
**Others**: No one else has access

**Q: Is my data shared with anyone?**

A: No. Your data stays within the MedLink system at your healthcare facility. No data is shared with:
- Other hospitals (unless you give permission)
- Government (unless legally required)
- Insurance companies (unless you authorize)
- Marketing companies (never)
- Third parties (never)

**Q: Can I request my data be deleted?**

A: Medical records have legal retention requirements (usually 25+ years). You cannot delete medical records, but you can:
- Request records be sealed (requires legal process)
- Switch to a different hospital
- Request data not be used for research (if applicable)

---

## 8. Troubleshooting

### 8.1 Login Issues

**Problem**: "Invalid username or password"

**Solutions**:
1. Check CAPS LOCK is off
2. Verify you selected correct role (Doctor/Patient)
3. Patients: Use your 14-digit National ID as username
4. Doctors: Use your assigned username
5. Try password reset if needed
6. Contact IT support if issue persists

---

**Problem**: "Account locked"

**Cause**: Too many failed login attempts (security feature)

**Solution**:
1. Wait 30 minutes, then try again
2. OR contact IT support to unlock immediately
3. Then use correct credentials

---

**Problem**: "Session expired"

**Cause**: 30 minutes of inactivity

**Solution**:
1. Click "OK" on the notification
2. Log in again
3. Your work is saved (don't worry)

---

### 8.2 NFC Card Issues

**Problem**: Card not detected

**Solutions**:
1. Hold card closer to reader (within 5cm)
2. Keep card flat against reader
3. Hold steady for full 2 seconds
4. Check USB connection of reader
5. Restart computer if needed
6. Try different card (to test reader)
7. Contact IT if reader is broken

---

**Problem**: "Card not registered"

**Solutions**:
1. Use password login instead
2. Contact administrator to verify card assignment
3. Card may need to be reassigned to you

---

**Problem**: Card reads wrong person

**Solutions**:
1. Make sure it's your card (check label)
2. If wrong card: Get your own card
3. If your card but wrong person: Contact IT to reassign

---

### 8.3 Display Issues

**Problem**: Text is too small

**Solution**:
1. Click your name (top-right)
2. Select "Settings"
3. Adjust "UI Scale" slider
4. Restart application

---

**Problem**: Screen looks cut off

**Solution**:
1. Check minimum resolution: 1280x720
2. Adjust monitor resolution in system settings
3. Maximize application window
4. Adjust UI scale (see above)

---

**Problem**: Application is slow

**Solutions**:
1. Close other programs
2. Check available RAM (need 4GB)
3. Restart computer
4. Contact IT if problem persists

---

### 8.4 Printing Issues

**Problem**: Emergency card won't print

**Solutions**:
1. Verify printer is connected and on
2. Check printer has paper
3. Check printer has ink/toner
4. Try "Print to PDF" first, then print PDF
5. Try different printer
6. Save PDF and print from another computer

---

**Problem**: Emergency card prints but QR code is blurry

**Solutions**:
1. Use higher quality print setting
2. Use better quality paper
3. Clean printer heads
4. Print at 100% scale (don't resize)
5. Generate new PDF and try again

---

### 8.5 Data Issues

**Problem**: Patient not found in search

**Solutions**:
1. Verify National ID is correct (exactly 14 digits)
2. Check for typos
3. Try typing slowly to avoid errors
4. Ask patient to verify their National ID
5. Contact administrator if patient should exist

---

**Problem**: Information is outdated

**Solutions**:
1. Contact your doctor to update information
2. Doctors: Click "Edit" and update
3. Patients: Update allowed fields in Settings
4. For medical data: Only doctors can update

---

## 9. Tips & Best Practices

### 9.1 For Doctors

**Efficient Workflow**:
- Use NFC cards for patient lookup (saves 27 seconds per patient!)
- Complete visit notes immediately (don't delay)
- Double-check medication names and dosages
- Always fill in all vital signs
- Add follow-up dates to all visits
- Use templates for common visit types

**Documentation Best Practices**:
- Be specific in diagnosis (not "stomach pain" but "acute gastritis")
- Write treatment plans clearly
- Include patient education provided
- Note any referrals made
- Document informed consent
- Record patient understanding

**Security Practices**:
- Always log out when leaving computer
- Don't share your password
- Don't leave patient records visible on screen
- Use privacy screens in public areas
- Report suspicious account activity

---

### 9.2 For Patients

**Staying Informed**:
- Check MedLink monthly for new lab results
- Download new emergency card after any changes
- Review your medications regularly
- Keep emergency contacts updated
- Report any errors to your doctor

**Emergency Preparedness**:
- Always carry your emergency card
- Give copies to family members
- Update card before travel
- Check card is not expired or damaged
- Know where your backup cards are

**Communication with Doctors**:
- Prepare questions before appointments
- Bring list of current medications
- Report all symptoms accurately
- Ask for clarification if you don't understand
- Take notes during visits

---

### 9.3 General Best Practices

**Security Habits**:
- Use strong, unique passwords
- Change passwords every 3 months
- Don't write passwords down
- Log out on shared computers
- Report lost NFC cards immediately

**Data Accuracy**:
- Verify all information is correct
- Update changes promptly
- Report errors to doctor
- Keep contact information current
- Notify of any allergies immediately

**Regular Maintenance**:
- Review your records quarterly
- Update emergency card semi-annually
- Check NFC card works monthly
- Clean up linked accounts annually

---

## 10. Support & Contact

### 10.1 Getting Help

**Technical Support**:
- Hospital IT Department
- Hours: Monday-Friday, 8 AM - 4 PM
- Phone: [Hospital IT Number]
- Email: support@medlink.eg

**Medical Records Questions**:
- Hospital Medical Records Department
- Hours: Monday-Saturday, 9 AM - 3 PM
- Phone: [Medical Records Number]

**Account Issues**:
- Hospital Administration
- Hours: Daily, 8 AM - 8 PM
- Phone: [Admin Number]

**Emergencies**:
- Call 123 (Egyptian emergency number)
- Or go directly to nearest hospital

---

### 10.2 Feedback & Suggestions

We want to hear from you!

**Submit Feedback**:
- Email: feedback@medlink.eg
- Phone: [Feedback Line]
- Online: www.medlink.eg/feedback

**What to Include**:
- What you like about MedLink
- What could be improved
- Features you'd like to see
- Problems you've encountered
- Suggestions for better usability

**Your feedback helps us improve MedLink for everyone!**

---

### 10.3 Training & Education

**For Doctors**:
- Monthly training sessions
- Video tutorials available
- Quick reference guides
- One-on-one training available

**For Patients**:
- Information sessions
- Printed guides
- Video tutorials
- Assistance at hospital reception

---

### 10.4 Additional Resources

**Online Resources** (Coming Soon):
- Video tutorials
- Quick start guides
- FAQs database
- Troubleshooting videos
- Best practices articles

**Printed Resources**:
- Quick reference card
- Emergency card instructions
- NFC card guide
- Privacy policy
- Terms of service

---

## 11. Appendix

### 11.1 Glossary of Medical Terms

**Acute**: Sudden onset, short duration
**Chronic**: Long-lasting, persistent condition
**Diagnosis**: Identification of a disease
**Prognosis**: Expected outcome of a disease
**Vital Signs**: Temperature, blood pressure, heart rate, etc.
**CBC**: Complete Blood Count (common lab test)
**CT**: Computed Tomography (imaging technique)
**MRI**: Magnetic Resonance Imaging
**DNR**: Do Not Resuscitate
**POA**: Power of Attorney

---

### 11.2 National ID Format

**Egyptian National ID Structure** (14 digits):
- Position 1: Century (2=1900s, 3=2000s)
- Positions 2-3: Year of birth
- Positions 4-5: Month of birth
- Positions 6-7: Day of birth
- Positions 8-11: Governorate code
- Position 12: Sequence number
- Position 13: Gender (odd=male, even=female)
- Position 14: Check digit

**Example**: 2 95 01 01 2345 6 7 8
- Born in 1995 (2=1900s, 95=year)
- January 1st (01-01)
- Governorate 2345
- Male (7 is odd)

---

### 11.3 Blood Type Information

**Blood Types**:
- A+ (most common in Egypt)
- O+
- B+
- AB+
- A-
- O- (universal donor)
- B-
- AB- (rarest)

**Why It Matters**:
- Crucial for blood transfusions
- Needed in emergencies
- Important for surgery
- Relevant for pregnancy

---

### 11.4 Common Allergies

**Drug Allergies**:
- Penicillin (most common)
- Sulfa drugs
- NSAIDs (ibuprofen, etc.)
- Aspirin
- Local anesthetics

**Other Allergies**:
- Latex
- Iodine (contrast dye)
- Eggs (in some vaccines)
- Nuts
- Shellfish

**Always report allergies to your doctor!**

---

## Conclusion

Thank you for using MedLink! We're committed to providing you with the best healthcare record management experience. Your health data is valuable, and we take the responsibility of safeguarding it seriously.

**Remember**:
- Keep your login credentials secure
- Always carry your emergency card
- Update information promptly
- Report any issues immediately
- Provide feedback to help us improve

**Stay healthy, stay informed, stay connected with MedLink!**

---

**MedLink User Manual**
*Version 1.0.0*
*Last Updated: November 28, 2024*

**© 2025 MedLink - Youssef Mekkkawy**

*Developed as part of CET111 course requirements*
*All sample data generated by Claude AI for demonstration purposes*

---

**End of User Manual**