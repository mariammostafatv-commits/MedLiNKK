# 🚀 MedLink Installation Guide

This guide will walk you through installing MedLink on Windows, macOS, and Linux.

---

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Linux Installation](#linux-installation)
- [NFC Reader Setup](#nfc-reader-setup)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.9 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB free
- **Screen**: 1280x720 or higher resolution
- **Operating System**: 
  - Windows 10/11
  - macOS 10.14 (Mojave) or higher
  - Linux Ubuntu 20.04 or higher

### Optional Hardware
- **NFC Card Reader**: R20C USB Card Reader
- **NFC Cards**: Mifare Classic 1K cards
- **Printer**: For printing emergency cards

---

## 🪟 Windows Installation

### Step 1: Install Python

1. **Download Python**:
   - Visit: https://www.python.org/downloads/
   - Download Python 3.9 or higher
   - **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Verify Installation**:
   ```cmd
   python --version
   ```
   Should show: `Python 3.9.x` or higher

3. **Verify pip**:
   ```cmd
   pip --version
   ```

### Step 2: Clone/Download MedLink

**Option A: Using Git**
```cmd
git clone https://github.com/yourusername/medlink.git
cd medlink
```

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to `C:\MedLink\`
3. Open Command Prompt
4. Navigate to folder:
   ```cmd
   cd C:\MedLink
   ```

### Step 3: Create Virtual Environment (Recommended)

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) before your command prompt
```

### Step 4: Install Requirements

```cmd
# Install production dependencies
pip install -r requirements.txt

# Wait for installation (2-5 minutes)
```

**For Development**:
```cmd
pip install -r requirements-dev.txt
```

### Step 5: Generate Test Data

```cmd
python tests/generate_test_data.py
```

### Step 6: Run MedLink

```cmd
python main.py
```

**Success!** The MedLink login window should appear.

---

## 🍎 macOS Installation

### Step 1: Install Python

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9

# Verify installation
python3 --version
```

**Option B: Download from Python.org**
1. Visit: https://www.python.org/downloads/macos/
2. Download Python 3.9+ installer
3. Run installer

### Step 2: Clone/Download MedLink

```bash
# Using Git
git clone https://github.com/yourusername/medlink.git
cd medlink

# OR download and extract ZIP
cd ~/Downloads/medlink
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) before your command prompt
```

### Step 4: Install Requirements

```bash
# Install production dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### Step 5: Generate Test Data

```bash
python tests/generate_test_data.py
```

### Step 6: Run MedLink

```bash
python main.py
```

**Success!** The MedLink login window should appear.

---

## 🐧 Linux Installation

### Step 1: Install Python

**Ubuntu/Debian:**
```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3.9 python3.9-venv python3-pip

# Verify installation
python3.9 --version
```

**Fedora/RHEL:**
```bash
# Install Python
sudo dnf install python39 python3-pip

# Verify installation
python3.9 --version
```

### Step 2: Clone/Download MedLink

```bash
# Using Git
git clone https://github.com/yourusername/medlink.git
cd medlink

# OR download and extract ZIP
cd ~/Downloads/medlink
```

### Step 3: Create Virtual Environment

```bash
# Create virtual environment
python3.9 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) before your command prompt
```

### Step 4: Install Requirements

```bash
# Install production dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### Step 5: Install System Dependencies (if needed)

Some distributions may need additional system packages:

```bash
# Ubuntu/Debian
sudo apt install python3-tk python3-dev

# Fedora/RHEL
sudo dnf install python3-tkinter python3-devel
```

### Step 6: Generate Test Data

```bash
python tests/generate_test_data.py
```

### Step 7: Run MedLink

```bash
python main.py
```

**Success!** The MedLink login window should appear.

---

## 💳 NFC Reader Setup

### Hardware Requirements
- **Model**: R20C USB Card Reader
- **Cards**: Mifare Classic 1K
- **Connection**: USB 2.0 or higher

### Windows Setup

1. **Connect Reader**:
   - Plug R20C reader into USB port
   - Windows should automatically install drivers

2. **Find COM Port**:
   - Open Device Manager (Windows + X → Device Manager)
   - Expand "Ports (COM & LPT)"
   - Note the COM port (e.g., COM3)

3. **Install CH340 Drivers** (if needed):
   - Download from: http://www.wch-ic.com/downloads/CH341SER_EXE.html
   - Run installer
   - Restart computer

4. **Configure MedLink**:
   - Open `config/hardware_config.py`
   - Update port:
   ```python
   NFC_CONFIG = {
       'enabled': True,
       'port': 'COM3',  # Your COM port
       'baudrate': 9600,
       'timeout': 30
   }
   ```

### macOS Setup

1. **Connect Reader**:
   - Plug R20C reader into USB port
   - macOS should recognize it automatically

2. **Find Device**:
   ```bash
   ls /dev/tty.*
   ```
   Look for `/dev/tty.usbserial-*`

3. **Configure MedLink**:
   ```python
   NFC_CONFIG = {
       'enabled': True,
       'port': '/dev/tty.usbserial-14130',  # Your device
       'baudrate': 9600,
       'timeout': 30
   }
   ```

### Linux Setup

1. **Connect Reader**:
   - Plug R20C reader into USB port

2. **Find Device**:
   ```bash
   ls /dev/ttyUSB*
   ```
   Should show `/dev/ttyUSB0` or similar

3. **Add User to dialout Group**:
   ```bash
   sudo usermod -a -G dialout $USER
   # Logout and login again
   ```

4. **Configure MedLink**:
   ```python
   NFC_CONFIG = {
       'enabled': True,
       'port': '/dev/ttyUSB0',  # Your device
       'baudrate': 9600,
       'timeout': 30
   }
   ```

### Test NFC Reader

```bash
python tests/test_nfc_reader.py
```

Expected output:
```
Connecting to NFC reader on COM3...
✅ Reader connected
Waiting for card tap...
[Tap a card]
✅ Card detected: 04A1B2C3D4E5F6
```

---

## ✅ Verifying Installation

### Check All Components

```bash
# Activate virtual environment first
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Verify Python packages
pip list

# Should see:
# - customtkinter (5.2.0)
# - cryptography (41.0.7)
# - Pillow (10.1.0)
# - qrcode (7.4.2)
# - reportlab (4.0.7)
# - PyPDF2 (3.0.1)
# - python-dateutil (2.8.2)
# - pyserial (3.5)
```

### Test Run

```bash
# Run main application
python main.py
```

**Expected Result**: Login window appears with:
- MedLink logo
- Role selection (Doctor/Patient)
- Username and password fields
- Register button

### Test Login

**Doctor Login**:
- Role: Doctor
- Username: `dr.ahmed.hassan`
- Password: `password`

**Patient Login**:
- Role: Patient
- Username: `29501012345678`
- Password: `patient123`

---

## 🔧 Troubleshooting

### Problem: "Python not found"

**Windows**:
```cmd
# Check if Python is in PATH
where python

# If not found, reinstall Python with "Add to PATH" checked
```

**macOS/Linux**:
```bash
# Try python3 instead of python
python3 --version

# Add alias to .bashrc or .zshrc
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

---

### Problem: "pip not found"

**All Platforms**:
```bash
# Install pip
python -m ensurepip --upgrade

# OR
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

---

### Problem: "ModuleNotFoundError: No module named 'customtkinter'"

**Solution**:
```bash
# Make sure virtual environment is activated
# Then reinstall requirements
pip install -r requirements.txt
```

---

### Problem: "Permission denied" (macOS/Linux)

**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# OR use sudo (not recommended for venv)
sudo pip install -r requirements.txt
```

---

### Problem: "tkinter not found" (Linux)

**Solution**:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter
```

---

### Problem: NFC Reader Not Detected

**Windows**:
1. Check Device Manager for yellow warning
2. Install CH340 drivers
3. Try different USB port
4. Restart computer

**macOS/Linux**:
1. Check USB connection
2. Verify device with `ls /dev/tty*`
3. Check permissions (dialout group on Linux)
4. Try different USB port

---

### Problem: Application Won't Start

**Check Python Version**:
```bash
python --version
# Must be 3.9 or higher
```

**Check All Dependencies**:
```bash
pip list | grep -E "customtkinter|cryptography|Pillow|qrcode|reportlab"
```

**Run with Debug**:
```bash
python -v main.py
# Shows detailed error messages
```

**Check File Permissions**:
```bash
# macOS/Linux
chmod +x main.py
```

---

### Problem: Slow Performance

**Solutions**:
1. Close other applications
2. Check RAM usage (need 4GB free)
3. Update graphics drivers
4. Use SSD instead of HDD
5. Disable antivirus temporarily

---

### Problem: Can't Generate Emergency Cards

**Solutions**:
1. Check ReportLab installed:
   ```bash
   pip show reportlab
   ```
2. Check write permissions to output folder
3. Try different output location
4. Check disk space

---

## 📞 Getting Help

If you encounter issues not listed here:

1. **Check Documentation**:
   - [Technical Documentation](docs/TECHNICAL_DOCUMENTATION.md)
   - [User Manual](docs/USER_MANUAL.md)

2. **Search GitHub Issues**:
   - Someone may have had the same problem

3. **Open New Issue**:
   - Go to GitHub Issues
   - Provide detailed error message
   - Include Python version and OS

4. **Contact Support**:
   - Email: support@medlink.eg

---

## 🎉 Installation Complete!

Congratulations! You've successfully installed MedLink.

### Next Steps:

1. **Read the User Manual**: `docs/USER_MANUAL.md`
2. **Explore Sample Data**: 30 patients, 15 doctors pre-loaded
3. **Try NFC Cards**: If you have the hardware
4. **Generate Emergency Cards**: Test PDF creation
5. **Provide Feedback**: Help us improve!

---

**Happy using MedLink!** 🏥

---

<div align="center">

**Built with ❤️ for better healthcare**

[Report Bug](https://github.com/yourusername/medlink/issues) • [Request Feature](https://github.com/yourusername/medlink/issues)

</div>
