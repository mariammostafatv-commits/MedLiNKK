# 🚀 MedLink Quick Reference Guide

Quick commands and shortcuts for MedLink installation and usage.

---

## 📦 Installation Commands

### Windows
```cmd
# Clone repository
git clone https://github.com/yourusername/medlink.git
cd medlink

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate test data
python tests/generate_test_data.py

# Run application
python main.py
```

### macOS / Linux
```bash
# Clone repository
git clone https://github.com/yourusername/medlink.git
cd medlink

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate test data
python tests/generate_test_data.py

# Run application
python main.py
```

---

## 🔐 Default Login Credentials

### Doctor Account
```
Role: Doctor
Username: dr.ahmed.hassan
Password: password
```

### Patient Account
```
Role: Patient
Username: 29501012345678
Password: patient123
```

---

## ⌨️ Common Commands

### Virtual Environment
```bash
# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Deactivate (All platforms)
deactivate
```

### Package Management
```bash
# Install production requirements
pip install -r requirements.txt

# Install development requirements
pip install -r requirements-dev.txt

# Update all packages
pip install --upgrade -r requirements.txt

# List installed packages
pip list

# Check for outdated packages
pip list --outdated

# Uninstall package
pip uninstall package-name
```

### Application
```bash
# Run MedLink
python main.py

# Run with debugging
python -v main.py

# Generate test data
python tests/generate_test_data.py

# Run tests
python -m pytest tests/

# Run specific test
python tests/test_validators.py
```

---

## 🔧 Development Commands

### Code Quality
```bash
# Format code with Black
black .

# Lint with pylint
pylint core/ gui/ utils/

# Type checking with mypy
mypy core/ gui/ utils/

# Style checking with flake8
flake8 core/ gui/ utils/
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov=gui --cov=utils

# Run specific test file
pytest tests/test_validators.py

# Run tests verbosely
pytest -v
```

### Git Commands
```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "feat: your message"

# Push to GitHub
git push origin main

# Create new branch
git checkout -b feature/your-feature

# Pull latest changes
git pull origin main
```

---

## 💳 NFC Reader Commands

### Find Device

**Windows (CMD):**
```cmd
# Open Device Manager
devmgmt.msc

# Check "Ports (COM & LPT)" section
```

**macOS (Terminal):**
```bash
# List USB devices
ls /dev/tty.*

# Example output: /dev/tty.usbserial-14130
```

**Linux (Terminal):**
```bash
# List USB devices
ls /dev/ttyUSB*

# Example output: /dev/ttyUSB0

# Check device info
dmesg | grep tty
```

### Test NFC Reader
```bash
python tests/test_nfc_reader.py
```

---

## 📊 Project Information

### Check Python Version
```bash
python --version
# Required: 3.9 or higher
```

### Check Dependencies
```bash
pip show customtkinter
pip show cryptography
pip show reportlab
```

### View Project Structure
```bash
# Windows
tree /F

# macOS/Linux
tree
```

### Count Lines of Code
```bash
# Linux/macOS with cloc installed
cloc .

# Or use find
find . -name '*.py' | xargs wc -l
```

---

## 🗂️ File Locations

### Data Files
```
data/users.json              # User accounts (doctors, patients)
data/patients.json           # Patient records (30 samples)
data/visits.json             # Medical visits
data/lab_results.json        # Laboratory results
data/imaging_results.json    # Imaging results
data/cards.json              # NFC card mappings
```

### Configuration Files
```
config/settings.py           # Application settings
config/hardware_config.py    # NFC reader configuration
config/localization.py       # Language settings
```

### Key Modules
```
core/auth_manager.py         # Authentication
core/patient_manager.py      # Patient management
core/nfc_manager.py          # NFC operations
gui/login_window.py          # Login interface
gui/doctor_dashboard.py      # Doctor portal
gui/patient_dashboard.py     # Patient portal
```

---

## 🚨 Emergency Commands

### Reset Virtual Environment
```bash
# Remove existing venv
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Create new venv
python -m venv venv

# Activate and reinstall
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Reset Database
```bash
# Regenerate test data
python tests/generate_test_data.py

# This overwrites existing data files
```

### Clear Cache
```bash
# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} +  # Linux/macOS
# Windows: Delete __pycache__ folders manually
```

---

## 💡 Quick Tips

### Activate Virtual Environment Automatically

**Windows (PowerShell):**
```powershell
# Add to profile
echo "cd C:\MedLink" >> $PROFILE
echo ".\venv\Scripts\Activate.ps1" >> $PROFILE
```

**macOS/Linux (Bash):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo "alias medlink='cd ~/medlink && source venv/bin/activate'" >> ~/.bashrc
source ~/.bashrc

# Now just type 'medlink' to activate
```

### Create Desktop Shortcut

**Windows:**
1. Create `MedLink.bat` file:
```batch
@echo off
cd C:\MedLink
call venv\Scripts\activate
python main.py
```
2. Create shortcut to this file on desktop

**macOS:**
1. Create `MedLink.command` file:
```bash
#!/bin/bash
cd ~/medlink
source venv/bin/activate
python main.py
```
2. Make executable: `chmod +x MedLink.command`
3. Drag to Dock

---

## 📞 Getting Help

### Check Documentation
```bash
# View in browser
docs/USER_MANUAL.md
docs/TECHNICAL_DOCUMENTATION.md
docs/INSTALLATION.md
```

### Check Logs
```bash
# View application logs
tail -f logs/app.log  # Linux/macOS
type logs\app.log     # Windows
```

### System Information
```bash
# Python
python --version

# pip
pip --version

# OS (Linux/macOS)
uname -a

# OS (Windows)
systeminfo
```

---

## 🎯 Package Versions

```
Python:         3.9+
customtkinter:  5.2.0
cryptography:   41.0.7
Pillow:         10.1.0
qrcode:         7.4.2
reportlab:      4.0.7
PyPDF2:         3.0.1
python-dateutil: 2.8.2
pyserial:       3.5
```

---

## 📚 Useful Links

- **GitHub**: https://github.com/yourusername/medlink
- **Issues**: https://github.com/yourusername/medlink/issues
- **Documentation**: https://github.com/yourusername/medlink/tree/main/docs
- **Python**: https://www.python.org/
- **CustomTkinter**: https://github.com/TomSchimansky/CustomTkinter

---

<div align="center">

**MedLink Quick Reference**  
*Keep this handy for quick access to common commands!*

📖 [Full Documentation](docs/) • 🐛 [Report Bug](https://github.com/yourusername/medlink/issues) • ⭐ [Star on GitHub](https://github.com/yourusername/medlink)

</div>
