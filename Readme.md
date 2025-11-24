# 🔓 Clipboard Protection Service

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

A lightweight background service that **automatically detects and re-enables Ctrl+C/Ctrl+V** when applications try to block clipboard operations.

Perfect for bypassing restrictions in exam browsers, remote desktop software, secure environments, or any application that disables clipboard functionality.

## ✨ Features

- 🔍 **Auto-Detection** - Monitors clipboard access every 3 seconds
- 🔄 **Auto Re-enable** - Automatically restores clipboard functionality when blocked
- 📊 **Activity Logging** - Shows which applications are blocking clipboard
- 🚀 **Lightweight** - Minimal CPU and memory usage
- 🖥️ **Cross-Platform** - Works on Windows, Linux, and macOS
- ⚙️ **Non-Intrusive** - Runs silently in the background

## 🎯 Use Cases

- Exam software that disables copy/paste
- Remote desktop applications with clipboard restrictions
- Secure browsers that block clipboard operations
- Corporate software with clipboard policies
- Virtual machines with clipboard limitations
- Any application that restricts Ctrl+C/Ctrl+V

## 📋 Requirements

### Windows
- Python 3.7 or higher
- Administrator privileges (recommended)

### Linux
- Python 3.7 or higher
- X11 window system
- Root/sudo access (for some features)

### macOS
- Python 3.7 or higher
- macOS 10.10 or higher

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/divyanshugupta0/copy-paste-enable-scripts.git
cd copy-paste-enable-scripts
```

### 2. Install Dependencies

#### Windows

```bash
pip install pywin32 psutil
```

Or using requirements:
```bash
pip install -r requirements-windows.txt
```

#### Linux

```bash
# Install Python dependencies
pip install psutil

# Install system dependencies
sudo apt-get update
sudo apt-get install xdotool xclip
```

Or using requirements:
```bash
pip install -r requirements-linux.txt
sudo apt-get install xdotool xclip
```

#### macOS

```bash
pip install psutil
```

Or using requirements:
```bash
pip install -r requirements-macos.txt
```

## 🎮 Usage

### Basic Usage

Simply run the script:

```bash
python clipboard_protection_service.py
```

### Run as Background Service

#### Windows (Run as Startup Service)

1. Create a shortcut to the script
2. Press `Win + R`, type `shell:startup`, press Enter
3. Copy the shortcut to the Startup folder

Or use Task Scheduler:
```bash
# Run with elevated privileges
pythonw clipboard_protection_service.py
```

#### Linux (systemd service)

Create a service file:

```bash
sudo nano /etc/systemd/system/clipboard-protection.service
```

Add the following content:

```ini
[Unit]
Description=Clipboard Protection Service
After=network.target

[Service]
Type=simple
User=your linux machine username
ExecStart=/usr/bin/python3 /path/to/clipboard_protection_service.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable clipboard-protection.service
sudo systemctl start clipboard-protection.service
```

Check status:
```bash
sudo systemctl status clipboard-protection.service
```

#### macOS (LaunchAgent)

Create a launch agent:

```bash
nano ~/Library/LaunchAgents/com.clipboard.protection.plist
```

Add the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.clipboard.protection</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/clipboard_protection_service.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load the agent:
```bash
launchctl load ~/Library/LaunchAgents/com.clipboard.protection.plist
```

## 📊 Example Output

```
============================================================
  CLIPBOARD PROTECTION SERVICE
  Detects & Auto Re-enables Ctrl+C / Ctrl+V
============================================================
Operating System: Windows
Re-enable Interval: 3 seconds

============================================================
Windows Clipboard Protection Service - Active
============================================================
✓ Monitoring for clipboard blocking
✓ Auto re-enable interval: 3 seconds
✓ Press Ctrl+C in this terminal to stop

🔍 Monitoring clipboard access every 3 seconds...

⚠ Detected clipboard blocking by: ExamBrowser.exe
⏳ Waiting 3 seconds before re-enabling...
✓ Clipboard access restored!
✓ Ctrl+C and Ctrl+V re-enabled despite blocking attempt!
```

## ⚙️ Configuration

You can modify the re-enable interval by changing the `RECHECK_INTERVAL` variable in the script:

```python
RECHECK_INTERVAL = 3  # Seconds (default: 3)
```

Options:
- `1` - Very aggressive (high CPU usage)
- `3` - Balanced (recommended)
- `5` - Conservative (lower CPU usage)

## 🛡️ Security & Privacy

- **Local Only** - All operations happen on your local machine
- **No Network Access** - The service doesn't connect to the internet
- **No Data Collection** - No telemetry or usage data is collected
- **Open Source** - Full source code available for review

## ⚠️ Disclaimer

This tool is intended for **personal use** and **legitimate purposes** only:

- ✅ Bypassing overly restrictive software on your own device
- ✅ Improving productivity in controlled environments
- ✅ Testing clipboard functionality

**Do NOT use this tool to:**
- ❌ Violate exam integrity or academic honesty policies
- ❌ Bypass security measures in corporate environments without permission
- ❌ Circumvent legitimate security controls

**The developers are not responsible for misuse of this software.**

## 🐛 Troubleshooting

### Windows

**Issue:** "Access Denied" error
```bash
# Run as Administrator
# Right-click Command Prompt → "Run as administrator"
python clipboard_protection_service.py
```

**Issue:** Import errors
```bash
pip install --upgrade pywin32 psutil
```

### Linux

**Issue:** "Permission denied"
```bash
# Run with sudo
sudo python3 clipboard_protection_service.py
```

**Issue:** X11 errors
```bash
# Ensure xdotool and xclip are installed
sudo apt-get install xdotool xclip
```

### macOS

**Issue:** "Operation not permitted"
```bash
# Grant Accessibility permissions:
# System Preferences → Security & Privacy → Privacy → Accessibility
# Add Terminal or your Python executable
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

If you encounter any issues or have questions:

- 🐛 [Open an issue](https://github.com/divyanshugupta0/clipboard-protection-service/issues)
- 💬 [Start a discussion](https://github.com/divyanshugupta0/clipboard-protection-service/discussions)

## ⭐ Show Your Support

If this project helped you, please give it a ⭐️!

---

**Note:** Always ensure you have permission to run such tools in your environment. Respect institutional policies and legal requirements.
