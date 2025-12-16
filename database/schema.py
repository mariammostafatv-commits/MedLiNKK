"""
Database Schema Definition for MedLink
All table structures and relationships
"""

from datetime import datetime

class DatabaseSchema:
    """Define all database tables and their structures"""
    
    @staticmethod
    def get_all_tables():
        """Get all table creation SQL statements"""
        return {
            'users': DatabaseSchema.users_table(),
            'patients': DatabaseSchema.patients_table(),
            'visits': DatabaseSchema.visits_table(),
            'prescriptions': DatabaseSchema.prescriptions_table(),
            'vital_signs': DatabaseSchema.vital_signs_table(),
            'lab_results': DatabaseSchema.lab_results_table(),
            'imaging_results': DatabaseSchema.imaging_results_table(),
            'doctor_cards': DatabaseSchema.doctor_cards_table(),
            'patient_cards': DatabaseSchema.patient_cards_table(),
            'hardware_audit_log': DatabaseSchema.hardware_audit_log_table(),
        }
    
    @staticmethod
    def users_table():
        """Doctors and staff users table"""
        return """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(50) UNIQUE NOT NULL,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(200) NOT NULL,
            email VARCHAR(150) UNIQUE,
            phone VARCHAR(20),
            specialization VARCHAR(100),
            license_number VARCHAR(50),
            hospital VARCHAR(200),
            department VARCHAR(100),
            user_type ENUM('doctor', 'nurse', 'admin', 'staff') DEFAULT 'doctor',
            is_active BOOLEAN DEFAULT TRUE,
            last_login DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_username (username),
            INDEX idx_user_id (user_id),
            INDEX idx_user_type (user_type)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def patients_table():
        """Patient information table"""
        return """
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            national_id VARCHAR(14) UNIQUE NOT NULL,
            full_name VARCHAR(200) NOT NULL,
            date_of_birth DATE NOT NULL,
            gender ENUM('male', 'female') NOT NULL,
            blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'),
            phone VARCHAR(20),
            email VARCHAR(150),
            address TEXT,
            city VARCHAR(100),
            governorate VARCHAR(100),
            emergency_contact_name VARCHAR(200),
            emergency_contact_phone VARCHAR(20),
            emergency_contact_relation VARCHAR(50),
            
            -- Medical Information
            chronic_conditions JSON,
            allergies JSON,
            current_medications JSON,
            family_history JSON,
            disabilities JSON,
            
            -- Emergency Directives
            dnr_status BOOLEAN DEFAULT FALSE,
            organ_donor BOOLEAN DEFAULT FALSE,
            power_of_attorney VARCHAR(200),
            religious_preferences TEXT,
            
            -- Lifestyle
            smoking_status ENUM('never', 'former', 'current'),
            alcohol_consumption ENUM('none', 'occasional', 'moderate', 'heavy'),
            exercise_frequency ENUM('none', 'rarely', 'weekly', 'daily'),
            dietary_preferences TEXT,
            
            -- System fields
            registered_by VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_national_id (national_id),
            INDEX idx_full_name (full_name),
            INDEX idx_phone (phone),
            FOREIGN KEY (registered_by) REFERENCES users(user_id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def visits_table():
        """Medical visits table"""
        return """
        CREATE TABLE IF NOT EXISTS visits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            visit_id VARCHAR(50) UNIQUE NOT NULL,
            patient_national_id VARCHAR(14) NOT NULL,
            doctor_id VARCHAR(50) NOT NULL,
            doctor_name VARCHAR(200) NOT NULL,
            
            visit_date DATE NOT NULL,
            visit_time TIME NOT NULL,
            hospital VARCHAR(200),
            department VARCHAR(100),
            visit_type ENUM('Consultation', 'Follow-up', 'Emergency', 'Routine') NOT NULL,
            
            chief_complaint TEXT,
            diagnosis TEXT,
            treatment_plan TEXT,
            notes TEXT,
            
            attachments JSON,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_visit_id (visit_id),
            INDEX idx_patient (patient_national_id),
            INDEX idx_doctor (doctor_id),
            INDEX idx_visit_date (visit_date),
            INDEX idx_visit_type (visit_type),
            
            FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES users(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def prescriptions_table():
        """Prescriptions related to visits"""
        return """
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            visit_id VARCHAR(50) NOT NULL,
            medication VARCHAR(200) NOT NULL,
            dosage VARCHAR(100),
            frequency VARCHAR(100),
            duration VARCHAR(50),
            instructions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            INDEX idx_visit (visit_id),
            FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def vital_signs_table():
        """Vital signs recorded during visits"""
        return """
        CREATE TABLE IF NOT EXISTS vital_signs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            visit_id VARCHAR(50) NOT NULL,
            blood_pressure VARCHAR(20),
            heart_rate VARCHAR(20),
            temperature VARCHAR(20),
            weight VARCHAR(20),
            height VARCHAR(20),
            respiratory_rate VARCHAR(20),
            oxygen_saturation VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            INDEX idx_visit (visit_id),
            FOREIGN KEY (visit_id) REFERENCES visits(visit_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def lab_results_table():
        """Laboratory test results"""
        return """
        CREATE TABLE IF NOT EXISTS lab_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            result_id VARCHAR(50) UNIQUE NOT NULL,
            patient_national_id VARCHAR(14) NOT NULL,
            ordered_by VARCHAR(50) NOT NULL,
            
            test_date DATE NOT NULL,
            lab_name VARCHAR(200),
            test_type VARCHAR(200) NOT NULL,
            status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
            
            results JSON,
            notes TEXT,
            
            external_link VARCHAR(500),
            attachment VARCHAR(500),
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_result_id (result_id),
            INDEX idx_patient (patient_national_id),
            INDEX idx_ordered_by (ordered_by),
            INDEX idx_test_date (test_date),
            INDEX idx_status (status),
            
            FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
            FOREIGN KEY (ordered_by) REFERENCES users(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def imaging_results_table():
        """Imaging and radiology results"""
        return """
        CREATE TABLE IF NOT EXISTS imaging_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            imaging_id VARCHAR(50) UNIQUE NOT NULL,
            patient_national_id VARCHAR(14) NOT NULL,
            ordered_by VARCHAR(50) NOT NULL,
            
            imaging_date DATE NOT NULL,
            imaging_center VARCHAR(200),
            imaging_type ENUM('X-Ray', 'CT', 'MRI', 'Ultrasound', 'PET', 'Other') NOT NULL,
            body_part VARCHAR(100),
            
            findings TEXT,
            radiologist VARCHAR(200),
            
            images JSON,
            external_link VARCHAR(500),
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            
            INDEX idx_imaging_id (imaging_id),
            INDEX idx_patient (patient_national_id),
            INDEX idx_ordered_by (ordered_by),
            INDEX idx_imaging_date (imaging_date),
            INDEX idx_imaging_type (imaging_type),
            
            FOREIGN KEY (patient_national_id) REFERENCES patients(national_id) ON DELETE CASCADE,
            FOREIGN KEY (ordered_by) REFERENCES users(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def doctor_cards_table():
        """NFC cards for doctors"""
        return """
        CREATE TABLE IF NOT EXISTS doctor_cards (
            id INT AUTO_INCREMENT PRIMARY KEY,
            card_uid VARCHAR(50) UNIQUE NOT NULL,
            username VARCHAR(100) NOT NULL,
            user_id VARCHAR(50),
            full_name VARCHAR(200) NOT NULL,
            card_type VARCHAR(20) DEFAULT 'doctor',
            is_active BOOLEAN DEFAULT TRUE,
            issued_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used DATETIME,
            
            INDEX idx_card_uid (card_uid),
            INDEX idx_username (username),
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def patient_cards_table():
        """NFC cards for patients"""
        return """
        CREATE TABLE IF NOT EXISTS patient_cards (
            id INT AUTO_INCREMENT PRIMARY KEY,
            card_uid VARCHAR(50) UNIQUE NOT NULL,
            national_id VARCHAR(14) NOT NULL,
            full_name VARCHAR(200) NOT NULL,
            card_type VARCHAR(20) DEFAULT 'patient',
            is_active BOOLEAN DEFAULT TRUE,
            issued_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used DATETIME,
            
            INDEX idx_card_uid (card_uid),
            INDEX idx_national_id (national_id),
            FOREIGN KEY (national_id) REFERENCES patients(national_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
    
    @staticmethod
    def hardware_audit_log_table():
        """Hardware access audit log"""
        return """
        CREATE TABLE IF NOT EXISTS hardware_audit_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            event_id VARCHAR(50) UNIQUE NOT NULL,
            timestamp DATETIME NOT NULL,
            event_type ENUM('fingerprint_login', 'nfc_card_scan', 'failed_login', 'logout', 'other') NOT NULL,
            
            user_id VARCHAR(50),
            patient_national_id VARCHAR(14),
            card_uid VARCHAR(50),
            fingerprint_id INT,
            
            success BOOLEAN DEFAULT TRUE,
            access_type VARCHAR(100),
            ip_address VARCHAR(45),
            device_name VARCHAR(100),
            
            additional_data JSON,
            
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            INDEX idx_event_id (event_id),
            INDEX idx_timestamp (timestamp),
            INDEX idx_event_type (event_type),
            INDEX idx_user_id (user_id),
            INDEX idx_patient (patient_national_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """