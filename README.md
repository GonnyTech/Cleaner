# 🚀 Windows Master Utility

**The complete solution for Windows cleaning and optimization**

An all-in-one application to keep your Windows PC clean, fast, and optimized.

---

## ✨ Features

### 🧹 System Cleaning
- **Empty Recycle Bin** - Deletes all files from the Recycle Bin
- **Delete Obsolete Downloads** - Removes files older than 7 days from the Downloads folder
- **Clean Temporary Files** - Deletes user and system temporary files
- **Clean Prefetch** - Optimizes startup times (requires Admin)
- **Delete Windows.old** - Reclaims space by deleting old Windows installations

### 🗑️ Remove Bloatware
Remove unwanted pre-installed Windows apps:
- Microsoft Edge, ToDo, Mail, Camera, People
- Paint 3D, Clipchamp, DevHome
- Notepad, Sticky Notes, Get Started
- **Microsoft Copilot**
- **Microsoft Recall**

**Confirmation dialog** always shows the list of apps before removal.

### ⚙️ Optimizations
- **Disable Windows Ads** - Removes ads from the Start menu and settings
- **Automatic Scheduling** - Automatic cleaning every Sunday at 10:00 AM
- **Install VS Code** - Automatic download and installation of Visual Studio Code
- **Install Brave Browser** - Automatic download and installation of Brave Browser

### 📊 Logs & Reports
- Real-time logging with timestamps
- Status icons (✅ ⚠️ ❌)
- Monitoring of completed operations

---

## 📥 Download

**Windows Master Utility v1.0**

📦 [WindowsMaster.exe](dist/WindowsMaster.exe) (14.3 MB)

---

## 🚀 Installation & Usage

### Requirements
- Windows 10 or Windows 11
- **Administrator Privileges** (recommended for all features)

### Quick Start

1. **Download** - Download `WindowsMaster.exe`
2. **Right Click** on the file → Select **"Run as administrator"**
3. **UAC Confirmation** - Approve the permission elevation request
4. The application will open with 4 available tabs

---

## 📖 Usage Guide

### 🧹 System Cleaning Tab

1. Select the desired operations (all selected by default)
2. Click on **"🚀 START SYSTEM CLEANING"**
3. Wait for completion
4. Check results in the "📊 Logs & Reports" tab

### 🗑️ Remove Bloatware Tab

1. Scroll through the list and select the apps to remove
2. Use **"Select All"** to select all apps
3. Click on **"🗑️ REMOVE SELECTED APPS"**
4. **Confirm** in the dialog showing the list of apps
5. Wait for removal completion

> ⚠️ **CAUTION**: App removal is **irreversible**!

### ⚙️ Optimizations Tab

**Disable Ads:**
- Click on "Disable Ads" (one-time action)

**Automatic Scheduling:**
- Click "✅ Activate" to enable weekly cleaning
- Click "❌ Deactivate" to remove the schedule

**Install VS Code / Brave:**
- Click the respective button for automatic download and installation

### 📊 Logs & Reports Tab

- View all operations in real-time
- Each line includes a timestamp and status icon
- Click "🗑️ Clean Log" to clear the log

---

## ⚠️ Important Warnings

> [!IMPORTANT]
> **Recommended Backup**: Before using this tool, create a Windows restore point.
> 
> Control Panel → System → System Protection → Create

> [!WARNING]
> **Bloatware Removal**: Removing some system apps (e.g., Microsoft Edge) might cause malfunctions. Use with caution.

> [!CAUTION]
> **Windows.old**: Deleting Windows.old is **irreversible**. Ensure you do not need to rollback.

---

## 🎯 Recommended Usage

### First Run
1. **Create a Windows restore point**
2. Run as **Administrator**
3. Go to the "⚙️ Optimizations" tab
4. Disable ads (one-time)
5. Activate weekly scheduling

### Manual Monthly Cleaning
1. "🧹 System Cleaning" tab
2. Select all options
3. Start cleaning
4. Check log for reclaimed space

### New PC Setup
1. Run as Admin
2. "🗑️ Remove Bloatware" tab
3. Select unwanted apps
4. Confirm removal
5. "⚙️ Optimizations" tab
6. Disable ads + schedule cleaning

---

## 🛠️ Technical Details

**Technologies:**
- Python 3.14
- CustomTkinter (UI)
- WinShell (Recycle Bin)
- WinReg (Registry)
- PyInstaller (Build)

**Size:** ~14 MB (includes Python runtime and libraries)

**Admin Elevation:** UAC required at startup (`--uac-admin` flag)

---

## 📝 Changelog

### v1.0 (February 2026)
- ✅ Full system cleaning (Recycle Bin, Downloads, Temp, Prefetch, Windows.old)
- ✅ Bloatware removal with confirmation dialog
- ✅ Disable Windows ads
- ✅ Automatic weekly scheduling
- ✅ VS Code installation
- ✅ Modern UI with dark theme and gradients
- ✅ Detailed log with timestamps and icons

---

## 🆘 Troubleshooting

**The app does not start:**
- Verify you have Windows 10/11
- Run as Administrator
- Temporarily disable antivirus

**"Some operations failed":**
- Ensure you are running as Administrator
- Close programs that might be blocking temporary files

**Scheduling does not work:**
- Must be run as Administrator
- Check in "Task Scheduler" → Look for "Windows_Master_Auto_Clean"

---

## 👨‍💻 Author

**Samuele Gonnella**

---

## 📜 License

This project is released under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software.

---

## ⭐ Support

If you find this tool useful, consider:
- Sharing it with friends and colleagues
- Reporting bugs or suggestions

---

**Windows Master Utility** - Keep your PC clean and fast! 🚀
