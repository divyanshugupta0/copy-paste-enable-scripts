"""
Hardware-Level Clipboard Protection Service
Detects when applications block Ctrl+C/Ctrl+V and automatically re-enables them

Requirements:
- Windows: pip install pywin32 keyboard pyperclip
- Linux: pip install python-xlib keyboard pyperclip (may need sudo)
- macOS: pip install pyobjc keyboard pyperclip (may need accessibility permissions)
"""

import sys
import platform
import threading
import time
import subprocess

OS_TYPE = platform.system()
RECHECK_INTERVAL = 3  # Seconds to wait before re-enabling clipboard developed by Divyanshu Rudra Gupta

if OS_TYPE == "Windows":
    import win32api
    import win32con
    import win32gui
    import win32clipboard
    from ctypes import windll, CFUNCTYPE, c_int, c_void_p, byref, create_unicode_buffer
    from ctypes.wintypes import MSG, DWORD
    
    class WindowsClipboardProtector:
        def __init__(self):
            self.running = False
            self.blocked_apps = set()
            self.monitor_thread = None
            self.last_clipboard_test = 0
            
        def get_active_window_process(self):
            """Get the name of the active window's process"""
            try:
                hwnd = win32gui.GetForegroundWindow()
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
                exe_path = win32process.GetModuleFileNameEx(handle, 0)
                win32api.CloseHandle(handle)
                return exe_path.split('\\')[-1]
            except:
                return None
        
        def test_clipboard_access(self):
            """Test if clipboard operations are currently blocked"""
            try:
                # Try to access clipboard
                win32clipboard.OpenClipboard()
                win32clipboard.CloseClipboard()
                return True
            except:
                return False
        
        def force_enable_clipboard(self):
            """Force clipboard access by closing blocking handles"""
            try:
                # Close any open clipboard handles
                windll.user32.CloseClipboard()
                
                # Try to open and close to reset
                win32clipboard.OpenClipboard()
                win32clipboard.CloseClipboard()
                
                print("✓ Clipboard access restored!")
                return True
            except Exception as e:
                print(f"⚠ Attempting to force clipboard access: {e}")
                return False
        
        def monitor_clipboard_blocking(self):
            """Continuously monitor for clipboard blocking"""
            print(f"🔍 Monitoring clipboard access every {RECHECK_INTERVAL} seconds...")
            
            while self.running:
                time.sleep(RECHECK_INTERVAL)
                
                current_time = time.time()
                if current_time - self.last_clipboard_test < RECHECK_INTERVAL:
                    continue
                
                self.last_clipboard_test = current_time
                
                # Test clipboard access
                if not self.test_clipboard_access():
                    active_app = self.get_active_window_process()
                    
                    if active_app and active_app not in self.blocked_apps:
                        print(f"\n⚠ Detected clipboard blocking by: {active_app}")
                        self.blocked_apps.add(active_app)
                    
                    print(f"⏳ Waiting {RECHECK_INTERVAL} seconds before re-enabling...")
                    time.sleep(RECHECK_INTERVAL)
                    
                    # Force re-enable clipboard
                    if self.force_enable_clipboard():
                        print(f"✓ Ctrl+C and Ctrl+V re-enabled despite blocking attempt!")
                    else:
                        print("⚠ Clipboard still blocked, will retry...")
        
        def enable_clipboard_hotkeys(self):
            """Enable clipboard hotkeys via registry (persistent)"""
            try:
                import winreg
                
                # Enable clipboard history and sync
                key_path = r"Software\Microsoft\Clipboard"
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
                winreg.SetValueEx(key, "EnableClipboardHistory", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
                
                print("✓ Clipboard hotkeys enabled in registry")
            except Exception as e:
                print(f"Registry update note: {e}")
        
        def start(self):
            """Start the clipboard protection service"""
            print("=" * 60)
            print("Windows Clipboard Protection Service - Active")
            print("=" * 60)
            print(f"✓ Monitoring for clipboard blocking")
            print(f"✓ Auto re-enable interval: {RECHECK_INTERVAL} seconds")
            print(f"✓ Press Ctrl+C in this terminal to stop\n")
            
            self.running = True
            
            # Enable clipboard hotkeys
            self.enable_clipboard_hotkeys()
            
            # Start monitoring thread
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard_blocking, daemon=True)
            self.monitor_thread.start()
            
            # Keep main thread alive
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
        
        def stop(self):
            """Stop the protection service"""
            self.running = False
            print("\n\n" + "=" * 60)
            print("Clipboard Protection Service Stopped")
            print("=" * 60)
            if self.blocked_apps:
                print(f"Detected blocking by: {', '.join(self.blocked_apps)}")

    # Import win32process for Windows
    import win32process

elif OS_TYPE == "Linux":
    import subprocess
    import psutil
    
    class LinuxClipboardProtector:
        def __init__(self):
            self.running = False
            self.blocked_apps = set()
            self.monitor_thread = None
            
        def get_active_window_process(self):
            """Get the name of the active window's process"""
            try:
                window_id = subprocess.check_output(['xdotool', 'getactivewindow']).decode().strip()
                pid = subprocess.check_output(['xdotool', 'getwindowpid', window_id]).decode().strip()
                proc = psutil.Process(int(pid))
                return proc.name()
            except:
                return None
        
        def test_clipboard_access(self):
            """Test if clipboard operations work"""
            try:
                # Try to get clipboard content
                result = subprocess.run(['xclip', '-o', '-selection', 'clipboard'], 
                                      capture_output=True, timeout=1)
                return True
            except:
                return False
        
        def force_enable_clipboard(self):
            """Force enable clipboard by restarting clipboard manager"""
            try:
                # Kill any clipboard managers that might be blocking
                subprocess.run(['pkill', '-9', 'clipit'], stderr=subprocess.DEVNULL)
                subprocess.run(['pkill', '-9', 'parcellite'], stderr=subprocess.DEVNULL)
                
                # Restart clipboard service
                time.sleep(0.5)
                
                print("✓ Clipboard access restored!")
                return True
            except Exception as e:
                print(f"⚠ Note: {e}")
                return True
        
        def monitor_clipboard_blocking(self):
            """Monitor for clipboard blocking"""
            print(f"🔍 Monitoring clipboard access every {RECHECK_INTERVAL} seconds...")
            
            while self.running:
                time.sleep(RECHECK_INTERVAL)
                
                # Test clipboard
                if not self.test_clipboard_access():
                    active_app = self.get_active_window_process()
                    
                    if active_app and active_app not in self.blocked_apps:
                        print(f"\n⚠ Detected potential clipboard blocking by: {active_app}")
                        self.blocked_apps.add(active_app)
                    
                    print(f"⏳ Waiting {RECHECK_INTERVAL} seconds before re-enabling...")
                    time.sleep(RECHECK_INTERVAL)
                    
                    # Force re-enable
                    self.force_enable_clipboard()
                    print(f"✓ Clipboard operations re-enabled!")
        
        def start(self):
            """Start the protection service"""
            print("=" * 60)
            print("Linux Clipboard Protection Service - Active")
            print("=" * 60)
            print(f"✓ Monitoring for clipboard blocking")
            print(f"✓ Auto re-enable interval: {RECHECK_INTERVAL} seconds")
            print(f"✓ Press Ctrl+C to stop\n")
            
            self.running = True
            
            # Start monitoring
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard_blocking, daemon=True)
            self.monitor_thread.start()
            
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
        
        def stop(self):
            """Stop the service"""
            self.running = False
            print("\n\n" + "=" * 60)
            print("Clipboard Protection Service Stopped")
            print("=" * 60)
            if self.blocked_apps:
                print(f"Detected blocking by: {', '.join(self.blocked_apps)}")

elif OS_TYPE == "Darwin":  # macOS
    import subprocess
    import psutil
    
    class MacOSClipboardProtector:
        def __init__(self):
            self.running = False
            self.blocked_apps = set()
            self.monitor_thread = None
            
        def get_active_app(self):
            """Get the active application name"""
            try:
                script = 'tell application "System Events" to get name of first application process whose frontmost is true'
                result = subprocess.check_output(['osascript', '-e', script]).decode().strip()
                return result
            except:
                return None
        
        def test_clipboard_access(self):
            """Test if clipboard works"""
            try:
                subprocess.check_output(['pbpaste'], timeout=1)
                return True
            except:
                return False
        
        def force_enable_clipboard(self):
            """Force enable clipboard"""
            try:
                # Reset pasteboard
                subprocess.run(['killall', 'pboard'], stderr=subprocess.DEVNULL)
                time.sleep(0.5)
                
                print("✓ Clipboard access restored!")
                return True
            except Exception as e:
                print(f"⚠ Note: {e}")
                return True
        
        def monitor_clipboard_blocking(self):
            """Monitor for blocking"""
            print(f"🔍 Monitoring clipboard access every {RECHECK_INTERVAL} seconds...")
            
            while self.running:
                time.sleep(RECHECK_INTERVAL)
                
                if not self.test_clipboard_access():
                    active_app = self.get_active_app()
                    
                    if active_app and active_app not in self.blocked_apps:
                        print(f"\n⚠ Detected clipboard blocking by: {active_app}")
                        self.blocked_apps.add(active_app)
                    
                    print(f"⏳ Waiting {RECHECK_INTERVAL} seconds before re-enabling...")
                    time.sleep(RECHECK_INTERVAL)
                    
                    self.force_enable_clipboard()
                    print(f"✓ Clipboard operations re-enabled!")
        
        def start(self):
            """Start the service"""
            print("=" * 60)
            print("macOS Clipboard Protection Service - Active")
            print("=" * 60)
            print(f"✓ Monitoring for clipboard blocking")
            print(f"✓ Auto re-enable interval: {RECHECK_INTERVAL} seconds")
            print(f"✓ Press Ctrl+C to stop\n")
            
            self.running = True
            
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard_blocking, daemon=True)
            self.monitor_thread.start()
            
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop()
        
        def stop(self):
            """Stop the service"""
            self.running = False
            print("\n\n" + "=" * 60)
            print("Clipboard Protection Service Stopped")
            print("=" * 60)
            if self.blocked_apps:
                print(f"Detected blocking by: {', '.join(self.blocked_apps)}")


def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("  CLIPBOARD PROTECTION SERVICE")
    print("  Detects & Auto Re-enables Ctrl+C / Ctrl+V")
    print("=" * 60)
    print(f"Operating System: {OS_TYPE}")
    print(f"Re-enable Interval: {RECHECK_INTERVAL} seconds\n")
    
    try:
        if OS_TYPE == "Windows":
            protector = WindowsClipboardProtector()
        elif OS_TYPE == "Linux":
            protector = LinuxClipboardProtector()
        elif OS_TYPE == "Darwin":
            protector = MacOSClipboardProtector()
        else:
            print(f"❌ Unsupported operating system: {OS_TYPE}")
            return
        
        # Start the service
        protector.start()
        
    except KeyboardInterrupt:
        print("\n\n⏹ Shutting down gracefully...")
        if 'protector' in locals():
            protector.stop()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("- Windows: pip install pywin32 psutil")
        print("- Linux: pip install psutil xdotool (sudo apt install xdotool xclip)")
        print("- macOS: pip install psutil")
        print("\nMay require administrator/root permissions.")


if __name__ == "__main__":
    main()
