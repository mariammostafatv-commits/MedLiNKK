"""
MySQL Shell Installer Module
A comprehensive installer and checker for MySQL Shell on Windows

Usage:
    from mysql_shell_installer import MySQLShellManager
    
    manager = MySQLShellManager()
    
    # Check if installed
    if manager.is_installed():
        info = manager.get_installation_info()
        print(f"Installed: {info['version']}")
    else:
        # Install it
        success = manager.install(silent=True)
"""

import requests
from bs4 import BeautifulSoup
from pathlib import Path
import shutil
from tqdm import tqdm
from enum import Enum
from colorama import Fore, Style, init
import subprocess
import time
import ctypes
import sys
import winreg
import os

# Initialize colorama for Windows
init(autoreset=True)


class Status(Enum):
    PENDING = "⏳"
    SUCCESS = "✅"
    FAILED = "❌"
    RUNNING = "🔄"


class MySQLShellManager:
    """
    MySQL Shell Installation Manager
    
    Features:
    - Check if MySQL Shell is installed
    - Get installation information
    - Download and install MySQL Shell
    - Admin privilege management
    """
    
    def __init__(self, download_folder="download_temp", silent_mode=True):
        """
        Initialize MySQL Shell Manager
        
        Args:
            download_folder (str): Folder to download installer
            silent_mode (bool): True for silent install, False for interactive
        """
        self.base_url = "https://dev.mysql.com"
        self.download_folder = Path(download_folder)
        self.silent_mode = silent_mode
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        self.download_url = None
        self.filename = None
        self.file_size = 0
        self.filepath = None
        self._installation_info = None
    
    # ==================== PUBLIC API ====================
    
    def is_installed(self):
        """
        Check if MySQL Shell is installed
        
        Returns:
            bool: True if installed, False otherwise
        """
        info = self.get_installation_info()
        return info is not None
    
    def get_installation_info(self):
        """
        Get information about installed MySQL Shell
        
        Returns:
            dict: Installation info or None if not installed
            {
                'installed': True,
                'name': 'MySQL Shell 9.5.0',
                'version': '9.5.0',
                'location': 'C:/Program Files/MySQL/...',
                'method': 'Registry|PATH|Program Files',
                'executable': 'path/to/mysqlsh.exe' (optional)
            }
        """
        if self._installation_info:
            return self._installation_info
        
        # Try all detection methods
        methods = [
            self._check_registry,
            self._check_program_files,
            self._check_path
        ]
        
        for method in methods:
            info = method()
            if info:
                self._installation_info = info
                return info
        
        return None
    
    def get_version(self):
        """
        Get installed MySQL Shell version
        
        Returns:
            str: Version string or None if not installed
        """
        info = self.get_installation_info()
        return info['version'] if info else None
    
    def get_executable_path(self):
        """
        Get path to mysqlsh.exe
        
        Returns:
            str: Path to executable or None if not found
        """
        info = self.get_installation_info()
        if info and 'executable' in info:
            return info['executable']
        
        # Try to find it
        try:
            result = subprocess.run(
                ["where", "mysqlsh"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass
        
        return None
    
    def install(self, silent=None, force_reinstall=False):
        """
        Install MySQL Shell
        
        Args:
            silent (bool): Silent install mode (None = use default)
            force_reinstall (bool): Install even if already installed
            
        Returns:
            bool: True if successful, False otherwise
        """
        if silent is not None:
            self.silent_mode = silent
        
        # Check if already installed
        if self.is_installed() and not force_reinstall:
            print(f"{Fore.GREEN}✅ MySQL Shell is already installed{Style.RESET_ALL}")
            info = self.get_installation_info()
            print(f"{Fore.CYAN}Version: {info['version']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Location: {info['location']}{Style.RESET_ALL}")
            return True
        
        # Check admin privileges
        if not self._ensure_admin_privileges():
            return False
        
        # Run installation steps
        steps = [
            ("Creating download folder", self._create_download_folder),
            ("Checking server", self._check_server),
            ("Finding download page", self._find_download_page),
            ("Getting direct link", self._get_direct_link),
            ("Checking disk space", self._check_disk_space),
            ("Downloading file", self._download_file),
            ("Installing software", self._install_software)
        ]
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚀 MySQL Shell Installation Starting{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        for step_name, step_func in steps:
            print(f"{Fore.YELLOW}🔄 {step_name}...{Style.RESET_ALL}")
            if not step_func():
                print(f"{Fore.RED}❌ Failed at: {step_name}{Style.RESET_ALL}")
                return False
            print(f"{Fore.GREEN}✅ {step_name} completed{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Installation Completed Successfully!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        # Clear cached info to force re-check
        self._installation_info = None
        
        return True
    
    def uninstall(self):
        """
        Uninstall MySQL Shell (if possible)
        
        Returns:
            bool: True if successful
        """
        info = self.get_installation_info()
        if not info:
            print(f"{Fore.YELLOW}MySQL Shell is not installed{Style.RESET_ALL}")
            return False
        
        # Check admin
        if not self._is_admin():
            print(f"{Fore.RED}❌ Administrator privileges required for uninstall{Style.RESET_ALL}")
            return False
        
        # Get uninstall string from registry
        uninstall_cmd = self._get_uninstall_command()
        if not uninstall_cmd:
            print(f"{Fore.RED}❌ Could not find uninstall command{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.YELLOW}Uninstalling MySQL Shell...{Style.RESET_ALL}")
        
        try:
            if self.silent_mode:
                # Silent uninstall
                result = subprocess.run(
                    f'msiexec.exe /x {uninstall_cmd} /qn',
                    shell=True,
                    timeout=300
                )
            else:
                # Interactive uninstall
                result = subprocess.run(
                    f'msiexec.exe /x {uninstall_cmd}',
                    shell=True,
                    timeout=300
                )
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}✅ Uninstall completed{Style.RESET_ALL}")
                self._installation_info = None
                return True
            else:
                print(f"{Fore.RED}❌ Uninstall failed with code {result.returncode}{Style.RESET_ALL}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Uninstall error: {e}{Style.RESET_ALL}")
            return False
    
    def print_status(self):
        """Print current installation status"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📊 MySQL Shell Status{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        if self.is_installed():
            info = self.get_installation_info()
            print(f"{Fore.GREEN}✅ Status: Installed{Style.RESET_ALL}\n")
            
            details = [
                ("Product Name", info.get("name", "MySQL Shell")),
                ("Version", info.get("version", "Unknown")),
                ("Install Location", info.get("location", "Unknown")),
                ("Detection Method", info.get("method", "Unknown"))
            ]
            
            if "executable" in info:
                details.append(("Executable Path", info["executable"]))
            
            for label, value in details:
                print(f"{Fore.WHITE}{label:.<25}: {Fore.GREEN}{value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Status: Not Installed{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    # ==================== PRIVATE METHODS ====================
    
    def _is_admin(self):
        """Check if running as administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def _run_as_admin(self):
        """Restart script with admin privileges"""
        try:
            if sys.argv[0].endswith('.py'):
                params = ' '.join([f'"{arg}"' for arg in sys.argv])
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            else:
                params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.argv[0], params, None, 1)
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to elevate: {e}{Style.RESET_ALL}")
            return False
        return True
    
    def _ensure_admin_privileges(self):
        """Ensure admin privileges, request if needed"""
        if self._is_admin():
            return True
        
        print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️  Administrator Privileges Required{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
        
        choice = input(f"{Fore.CYAN}Restart with admin privileges? (Y/n): {Style.RESET_ALL}").strip().lower()
        
        if choice in ['', 'y', 'yes']:
            print(f"{Fore.CYAN}🔄 Restarting...{Style.RESET_ALL}")
            time.sleep(1)
            self._run_as_admin()
            return False
        else:
            print(f"{Fore.RED}❌ Installation cancelled{Style.RESET_ALL}")
            return False
    
    def _check_registry(self):
        """Check Windows Registry for MySQL Shell"""
        try:
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]
            
            for hkey, path in registry_paths:
                try:
                    registry_key = winreg.OpenKey(hkey, path)
                    
                    for i in range(0, winreg.QueryInfoKey(registry_key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(registry_key, i)
                            subkey = winreg.OpenKey(registry_key, subkey_name)
                            
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                
                                if "mysql shell" in display_name.lower() and \
                                   "mysql server" not in display_name.lower() and \
                                   "workbench" not in display_name.lower():
                                    
                                    try:
                                        version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                    except:
                                        version = "Unknown"
                                    
                                    try:
                                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    except:
                                        install_location = "Unknown"
                                    
                                    winreg.CloseKey(subkey)
                                    winreg.CloseKey(registry_key)
                                    
                                    return {
                                        "installed": True,
                                        "name": display_name,
                                        "version": version,
                                        "location": install_location,
                                        "method": "Registry"
                                    }
                            except FileNotFoundError:
                                pass
                            
                            winreg.CloseKey(subkey)
                        except WindowsError:
                            continue
                    
                    winreg.CloseKey(registry_key)
                except WindowsError:
                    continue
        except:
            pass
        
        return None
    
    def _check_program_files(self):
        """Check Program Files for MySQL Shell"""
        possible_paths = [
            Path("C:/Program Files/MySQL"),
            Path("C:/Program Files (x86)/MySQL"),
        ]
        
        for base_path in possible_paths:
            if base_path.exists():
                for item in base_path.iterdir():
                    if item.is_dir() and "mysql shell" in item.name.lower():
                        mysqlsh_exe = item / "bin" / "mysqlsh.exe"
                        if mysqlsh_exe.exists():
                            try:
                                result = subprocess.run(
                                    [str(mysqlsh_exe), "--version"],
                                    capture_output=True,
                                    text=True,
                                    timeout=5
                                )
                                version = result.stdout.strip()
                            except:
                                version = "Unknown"
                            
                            return {
                                "installed": True,
                                "name": item.name,
                                "version": version,
                                "location": str(item),
                                "executable": str(mysqlsh_exe),
                                "method": "Program Files"
                            }
        
        return None
    
    def _check_path(self):
        """Check if mysqlsh is in PATH"""
        try:
            result = subprocess.run(
                ["mysqlsh", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                version = result.stdout.strip()
                
                try:
                    where_result = subprocess.run(
                        ["where", "mysqlsh"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    location = where_result.stdout.strip().split('\n')[0]
                except:
                    location = "In system PATH"
                
                return {
                    "installed": True,
                    "name": "MySQL Shell",
                    "version": version,
                    "location": location,
                    "method": "PATH"
                }
        except:
            pass
        
        return None
    
    def _get_uninstall_command(self):
        """Get uninstall command from registry"""
        try:
            registry_paths = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            ]
            
            for hkey, path in registry_paths:
                try:
                    registry_key = winreg.OpenKey(hkey, path)
                    
                    for i in range(0, winreg.QueryInfoKey(registry_key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(registry_key, i)
                            subkey = winreg.OpenKey(registry_key, subkey_name)
                            
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                
                                if "mysql shell" in display_name.lower():
                                    try:
                                        uninstall = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                        winreg.CloseKey(subkey)
                                        winreg.CloseKey(registry_key)
                                        
                                        # Extract product code
                                        if "{" in uninstall and "}" in uninstall:
                                            start = uninstall.index("{")
                                            end = uninstall.index("}") + 1
                                            return uninstall[start:end]
                                        
                                        return None
                                    except:
                                        pass
                            except:
                                pass
                            
                            winreg.CloseKey(subkey)
                        except:
                            continue
                    
                    winreg.CloseKey(registry_key)
                except:
                    continue
        except:
            pass
        
        return None
    
    def _create_download_folder(self):
        """Create download folder"""
        try:
            self.download_folder.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
    
    def _check_server(self):
        """Check if MySQL download server is reachable"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
    
    def _find_download_page(self):
        """Find MySQL Shell download page"""
        try:
            url = f"{self.base_url}/downloads/shell/"
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")
            buttons = soup.find_all("div", {"class": "button03"})
            
            if not buttons:
                raise ValueError("No download buttons found")
            
            download_link = None
            for button in buttons:
                link = button.find('a')
                if link and 'href' in link.attrs:
                    if 'windows' in link.get('href', '').lower():
                        download_link = self.base_url + link['href']
                        break
            
            if not download_link and buttons:
                download_link = self.base_url + buttons[0].find('a')['href']
            
            if not download_link:
                raise ValueError("Could not find download link")
            
            self.download_url = download_link
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
    
    def _get_direct_link(self):
        """Get direct download link"""
        try:
            response = self.session.get(self.download_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "lxml")
            content_div = soup.find("div", {"id": "content"})
            
            if not content_div:
                raise ValueError("Could not find content")
            
            links = content_div.find_all('a')
            if not links:
                raise ValueError("No links found")
            
            direct_link = self.base_url + links[-1]['href']
            self.filename = direct_link.split("/")[-1]
            
            # Get file size
            self.file_size = 0
            try:
                stream_response = self.session.get(direct_link, stream=True, allow_redirects=True, timeout=10)
                if 'content-length' in stream_response.headers:
                    self.file_size = int(stream_response.headers['content-length'])
                stream_response.close()
            except:
                pass
            
            self.download_url = direct_link
            
            size_mb = self.file_size / (1024 * 1024) if self.file_size > 0 else 0
            if size_mb > 0:
                print(f"{Fore.CYAN}File: {self.filename} ({size_mb:.2f} MB){Style.RESET_ALL}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
    
    def _check_disk_space(self):
        """Check disk space"""
        try:
            stat = shutil.disk_usage(self.download_folder)
            free_space = stat.free
            free_mb = free_space / (1024 * 1024)
            
            if self.file_size == 0:
                min_required = 1024 * 1024 * 1024  # 1 GB
                if free_space < min_required:
                    print(f"{Fore.RED}Low disk space: {free_mb:.2f} MB{Style.RESET_ALL}")
                    return False
            else:
                required = self.file_size * 1.1
                required_mb = required / (1024 * 1024)
                if free_space < required:
                    print(f"{Fore.RED}Need {required_mb:.2f} MB, have {free_mb:.2f} MB{Style.RESET_ALL}")
                    return False
            
            return True
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False
    
    def _download_file(self):
        """Download the installer file"""
        try:
            self.filepath = self.download_folder / self.filename
            
            response = self.session.get(self.download_url, stream=True, allow_redirects=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            if total_size > 0 and self.file_size == 0:
                self.file_size = total_size
            
            downloaded_size = 0
            
            with open(self.filepath, 'wb') as file:
                if total_size > 0:
                    with tqdm(
                        desc=self.filename,
                        total=total_size,
                        unit='iB',
                        unit_scale=True,
                        unit_divisor=1024,
                        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]'
                    ) as bar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                size = file.write(chunk)
                                downloaded_size += size
                                bar.update(size)
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            downloaded_size += file.write(chunk)
            
            if downloaded_size == 0:
                raise ValueError("No data downloaded")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            if self.filepath and self.filepath.exists():
                self.filepath.unlink()
            return False
    
    def _install_software(self):
        """Install the MSI file"""
        try:
            if not self.filepath or not self.filepath.exists():
                raise ValueError("Installation file not found")
            
            if not self._is_admin():
                raise PermissionError("Administrator privileges required")
            
            if self.silent_mode:
                cmd = [
                    'msiexec.exe', '/i', str(self.filepath.absolute()),
                    '/qn', '/norestart',
                    '/L*V', str(self.download_folder / 'install.log')
                ]
                
                print(f"{Fore.CYAN}Installing silently...{Style.RESET_ALL}")
                
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                animation = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
                idx = 0
                while process.poll() is None:
                    print(f"\r{Fore.CYAN}{animation[idx % len(animation)]} Installing...{Style.RESET_ALL}", end='', flush=True)
                    time.sleep(0.1)
                    idx += 1
                
                print("\r" + " " * 40 + "\r", end='')
                
                return_code = process.wait()
                
                if return_code in [0, 3010]:
                    return True
                else:
                    raise ValueError(f"Installation failed: {return_code}")
            else:
                cmd = ['msiexec.exe', '/i', str(self.filepath.absolute())]
                process = subprocess.Popen(cmd)
                return_code = process.wait()
                return return_code in [0, 3010]
            
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            return False


# ==================== STANDALONE CLI ====================

def main():
    """Standalone CLI interface"""
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}MySQL Shell Installer{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    manager = MySQLShellManager()
    
    # Check current status
    manager.print_status()
    
    if manager.is_installed():
        print(f"{Fore.YELLOW}Options:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Reinstall{Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Uninstall{Style.RESET_ALL}")
        print(f"{Fore.WHITE}3. Exit{Style.RESET_ALL}\n")
        
        choice = input(f"{Fore.CYAN}Choose option (1-3): {Style.RESET_ALL}").strip()
        
        if choice == "1":
            manager.install(force_reinstall=True)
        elif choice == "2":
            manager.uninstall()
        else:
            print(f"{Fore.GREEN}Exiting...{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Installation Mode:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}1. Silent (Automatic){Style.RESET_ALL}")
        print(f"{Fore.WHITE}2. Interactive (Manual){Style.RESET_ALL}\n")
        
        choice = input(f"{Fore.CYAN}Choose mode (1-2) [default: 1]: {Style.RESET_ALL}").strip()
        silent = choice != "2"
        
        manager.install(silent=silent)


if __name__ == "__main__":
    main()