import customtkinter as ctk
import os
import shutil
import winshell
import datetime
import threading
import sys
import ctypes
import subprocess
import winreg

# --- Constants ---
APP_NAME = "Windows Master Utility"
APP_VERSION = "v1.0"
TASK_NAME = "Windows_Master_Auto_Clean"

# Color Scheme
PRIMARY_COLOR = "#1f6feb"
SECONDARY_COLOR = "#8b5cf6"
SUCCESS_COLOR = "#238636"
WARNING_COLOR = "#fb8500"
DANGER_COLOR = "#da3633"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class WindowsMaster(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("900x650")
        self.resizable(False, False)
        
        # Bloatware apps dictionary
        self.bloatware_apps = {
            "Microsoft ToDo": "Microsoft.ToDo",
            "Mail and Calendar": "Microsoft.WindowsCommunicationsApps",
            "Camera": "Microsoft.WindowsCamera",
            "People": "Microsoft.People",
            "Notepad": "Microsoft.WindowsNotepad",
            "Microsoft Edge": "Microsoft.Edge",
            "Sticky Notes": "Microsoft.MicrosoftStickyNotes",
            "Get Started": "Microsoft.Getstarted",
            "3D Builder": "Microsoft.3DBuilder",
            "Paint 3D": "Microsoft.MSPaint",
            "Clipchamp": "Clipchamp.Clipchamp",
            "DevHome": "Microsoft.DevHome",
            "Microsoft Copilot": "Microsoft.Windows.Copilot",
            "Microsoft Recall": "Microsoft.Recall"
        }
        
        self.bloatware_vars = {}
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color=PRIMARY_COLOR, corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text=f"🚀 {APP_NAME}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=15)
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Pulizia Completa e Ottimizzazione Windows",
            font=ctk.CTkFont(size=13),
            text_color="#c9d1d9"
        )
        subtitle.pack(pady=(0, 15))
        
        # Tabview
        self.tabview = ctk.CTkTabview(self, width=860, corner_radius=10)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Create tabs
        self.tab_cleaning = self.tabview.add("🧹 Pulizia Sistema")
        self.tab_bloat = self.tabview.add("🗑️ Rimuovi Bloatware")
        self.tab_optimize = self.tabview.add("⚙️ Ottimizzazioni")
        self.tab_log = self.tabview.add("📊 Log & Report")
        
        self.setup_cleaning_tab()
        self.setup_bloatware_tab()
        self.setup_optimization_tab()
        self.setup_log_tab()
    
    def setup_cleaning_tab(self):
        frame = self.tab_cleaning
        frame.grid_columnconfigure(0, weight=1)
        
        # Info label
        info = ctk.CTkLabel(
            frame,
            text="Seleziona le operazioni di pulizia da eseguire:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.pack(pady=(10, 20), padx=20, anchor="w")
        
        # Checkboxes
        self.check_recycle = ctk.CTkCheckBox(
            frame, 
            text="♻️  Svuota Cestino",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_recycle.pack(pady=8, padx=30, anchor="w")
        self.check_recycle.select()
        
        self.check_downloads = ctk.CTkCheckBox(
            frame,
            text="📥  Cancella Download obsoleti (> 7 giorni)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_downloads.pack(pady=8, padx=30, anchor="w")
        self.check_downloads.select()
        
        self.check_temp = ctk.CTkCheckBox(
            frame,
            text="🗂️  Pulisci File Temporanei (User + System)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_temp.pack(pady=8, padx=30, anchor="w")
        self.check_temp.select()
        
        self.check_prefetch = ctk.CTkCheckBox(
            frame,
            text="⚡  Pulisci Prefetch (Richiede Admin)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_prefetch.pack(pady=8, padx=30, anchor="w")
        self.check_prefetch.select()
        
        self.check_windows_old = ctk.CTkCheckBox(
            frame,
            text="🔧  Cancella Windows.old (Richiede Admin)",
            font=ctk.CTkFont(size=13),
            checkbox_width=22,
            checkbox_height=22
        )
        self.check_windows_old.pack(pady=8, padx=30, anchor="w")
        
        # Action button
        self.btn_clean = ctk.CTkButton(
            frame,
            text="🚀 AVVIA PULIZIA SISTEMA",
            command=self.start_cleaning,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=SUCCESS_COLOR,
            hover_color="#2ea043"
        )
        self.btn_clean.pack(pady=30, padx=40, fill="x")
    
    def setup_bloatware_tab(self):
        frame = self.tab_bloat
        frame.grid_columnconfigure(0, weight=1)
        
        info = ctk.CTkLabel(
            frame,
            text="Seleziona le app preinstallate da rimuovere:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.pack(pady=(10, 15), padx=20, anchor="w")
        
        # Scrollable frame for apps
        scroll_frame = ctk.CTkScrollableFrame(frame, width=800, height=250)
        scroll_frame.pack(pady=10, padx=20, fill="x")
        
        # Create checkboxes for each bloatware app
        for app_name in self.bloatware_apps.keys():
            var = ctk.BooleanVar(value=False)
            self.bloatware_vars[app_name] = var
            
            check = ctk.CTkCheckBox(
                scroll_frame,
                text=f"❌  {app_name}",
                variable=var,
                font=ctk.CTkFont(size=13),
                checkbox_width=22,
                checkbox_height=22
            )
            check.pack(pady=5, padx=10, anchor="w")
        
        # Button frame
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=15, padx=20, fill="x")
        
        btn_select_all = ctk.CTkButton(
            btn_frame,
            text="Seleziona Tutto",
            command=self.select_all_bloatware,
            width=150,
            fg_color=SECONDARY_COLOR,
            hover_color="#7c3aed"
        )
        btn_select_all.pack(side="left", padx=5)
        
        btn_deselect_all = ctk.CTkButton(
            btn_frame,
            text="Deseleziona Tutto",
            command=self.deselect_all_bloatware,
            width=150,
            fg_color="#6e7681",
            hover_color="#484f58"
        )
        btn_deselect_all.pack(side="left", padx=5)
        
        self.btn_remove_bloat = ctk.CTkButton(
            frame,
            text="🗑️ RIMUOVI APP SELEZIONATE",
            command=self.start_bloatware_removal,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=DANGER_COLOR,
            hover_color="#b62324"
        )
        self.btn_remove_bloat.pack(pady=15, padx=40, fill="x")
    
    def setup_optimization_tab(self):
        frame = self.tab_optimize
        frame.grid_columnconfigure(0, weight=1)
        
        info = ctk.CTkLabel(
            frame,
            text="Ottimizzazioni e Configurazioni:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.pack(pady=(10, 20), padx=20, anchor="w")
        
        # Disable Ads
        ads_frame = ctk.CTkFrame(frame)
        ads_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            ads_frame,
            text="🚫 Disabilita Pubblicità Windows",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=10, padx=15, anchor="w")
        
        self.btn_disable_ads = ctk.CTkButton(
            ads_frame,
            text="Disabilita Pubblicità",
            command=self.disable_ads,
            fg_color=WARNING_COLOR,
            hover_color="#d47100"
        )
        self.btn_disable_ads.pack(pady=10, padx=15)
        
        # Scheduling
        sched_frame = ctk.CTkFrame(frame)
        sched_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            sched_frame,
            text="📅 Pianificazione Automatica (Domenica 10:00)",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=10, padx=15, anchor="w")
        
        btn_frame = ctk.CTkFrame(sched_frame, fg_color="transparent")
        btn_frame.pack(pady=10, padx=15)
        
        self.btn_enable_sched = ctk.CTkButton(
            btn_frame,
            text="✅ Attiva",
            command=self.enable_scheduling,
            width=150,
            fg_color=SUCCESS_COLOR,
            hover_color="#2ea043"
        )
        self.btn_enable_sched.pack(side="left", padx=5)
        
        self.btn_disable_sched = ctk.CTkButton(
            btn_frame,
            text="❌ Disattiva",
            command=self.disable_scheduling,
            width=150,
            fg_color=DANGER_COLOR,
            hover_color="#b62324"
        )
        self.btn_disable_sched.pack(side="left", padx=5)
        
        # VS Code Installation
        vscode_frame = ctk.CTkFrame(frame)
        vscode_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            vscode_frame,
            text="💻 Installa Visual Studio Code",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(pady=10, padx=15, anchor="w")
        
        self.btn_install_vscode = ctk.CTkButton(
            vscode_frame,
            text="Installa VS Code",
            command=self.install_vscode,
            fg_color=PRIMARY_COLOR,
            hover_color="#1f5fcf"
        )
        self.btn_install_vscode.pack(pady=10, padx=15)
    
    def setup_log_tab(self):
        frame = self.tab_log
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)
        
        info = ctk.CTkLabel(
            frame,
            text="📋 Log delle Operazioni:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        info.grid(row=0, column=0, pady=(10, 10), padx=20, sticky="w")
        
        self.textbox_log = ctk.CTkTextbox(frame, width=820, height=400, font=ctk.CTkFont(size=12))
        self.textbox_log.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.textbox_log.configure(state="disabled")
        
        # Clear log button
        btn_clear = ctk.CTkButton(
            frame,
            text="🗑️ Pulisci Log",
            command=self.clear_log,
            width=150,
            fg_color="#6e7681",
            hover_color="#484f58"
        )
        btn_clear.grid(row=2, column=0, pady=(0, 15))
    
    def log(self, message, level="INFO"):
        icon = "ℹ️" if level == "INFO" else "✅" if level == "SUCCESS" else "⚠️" if level == "WARNING" else "❌"
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", f"[{timestamp}] {icon} {message}\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")
        
        # Switch to log tab if error
        if level == "ERROR":
            self.tabview.set("📊 Log & Report")
    
    def clear_log(self):
        self.textbox_log.configure(state="normal")
        self.textbox_log.delete("1.0", "end")
        self.textbox_log.configure(state="disabled")
    
    def select_all_bloatware(self):
        for var in self.bloatware_vars.values():
            var.set(True)
    
    def deselect_all_bloatware(self):
        for var in self.bloatware_vars.values():
            var.set(False)
    
    # ===== CLEANING OPERATIONS =====
    
    def start_cleaning(self):
        self.btn_clean.configure(state="disabled", text="⏳ Pulizia in corso...")
        threading.Thread(target=self.perform_cleaning, daemon=True).start()
    
    def perform_cleaning(self):
        import pythoncom
        pythoncom.CoInitialize()
        
        self.log("=== INIZIO PULIZIA SISTEMA ===")
        is_admin = self.is_admin()
        
        if not is_admin:
            self.log("ATTENZIONE: Non si hanno privilegi di amministratore. Alcune operazioni potrebbero fallire.", "WARNING")
        
        try:
            # Recycle Bin
            if self.check_recycle.get():
                self.log("Svuotando Cestino...")
                try:
                    winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                    self.log("Cestino svuotato con successo", "SUCCESS")
                except Exception as e:
                    self.log(f"Errore svuotamento cestino: {e}", "ERROR")
            
            # Downloads
            if self.check_downloads.get():
                downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
                self.clean_folder(downloads_path, days=7, label="Download")
            
            # Temp files
            if self.check_temp.get():
                self.clean_folder(os.environ.get('TEMP'), label="Temp Utente", days=0)
                if is_admin:
                    self.clean_folder("C:\\Windows\\Temp", label="Temp Sistema", days=0)
            
            # Prefetch
            if self.check_prefetch.get():
                if is_admin:
                    self.clean_folder("C:\\Windows\\Prefetch", label="Prefetch", days=0)
                else:
                    self.log("SKIP: Prefetch richiede privilegi Admin", "WARNING")
            
            # Windows.old
            if self.check_windows_old.get():
                path = "C:\\Windows.old"
                if os.path.exists(path):
                    if not is_admin:
                        self.log("SKIP: Windows.old richiede privilegi Admin", "WARNING")
                    else:
                        self.log("Rimozione Windows.old...")
                        try:
                            subprocess.run(["cmd", "/c", f"rd /s /q {path}"], check=True, capture_output=True)
                            self.log("Windows.old rimosso con successo", "SUCCESS")
                        except Exception as e:
                            self.log(f"Errore rimozione Windows.old: {e}", "ERROR")
                else:
                    self.log("Windows.old non presente", "INFO")
            
            self.log("=== PULIZIA COMPLETATA ===", "SUCCESS")
        finally:
            self.btn_clean.configure(state="normal", text="🚀 AVVIA PULIZIA SISTEMA")
    
    def clean_folder(self, path, days=0, label=""):
        if not path or not os.path.exists(path):
            self.log(f"Cartella {label} non trovata", "WARNING")
            return
        
        self.log(f"Pulizia {label}...")
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        count = 0
        
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(item_path))
                    if mtime < cutoff:
                        if os.path.isfile(item_path) or os.path.islink(item_path):
                            os.remove(item_path)
                            count += 1
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                            count += 1
                except:
                    pass
            self.log(f"{label}: Rimossi {count} elementi", "SUCCESS")
        except Exception as e:
            self.log(f"Errore pulizia {label}: {e}", "ERROR")
    
    # ===== BLOATWARE REMOVAL =====
    
    def start_bloatware_removal(self):
        selected = {name: code for name, code in self.bloatware_apps.items() if self.bloatware_vars[name].get()}
        
        if not selected:
            self.log("Nessuna app selezionata per la rimozione", "WARNING")
            return
        
        if not self.is_admin():
            self.log("ERRORE: Privilegi di amministratore richiesti per rimuovere bloatware", "ERROR")
            return
        
        # Show confirmation dialog
        self.show_confirmation_dialog(selected)
    
    def show_confirmation_dialog(self, selected_apps):
        # Create modal dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("⚠️ Conferma Rimozione")
        dialog.geometry("500x550")
        dialog.resizable(False, False)
        
        # Make it modal
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (500 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (550 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Warning header
        warning_frame = ctk.CTkFrame(dialog, fg_color=WARNING_COLOR)
        warning_frame.pack(fill="x", padx=0, pady=0)
        
        ctk.CTkLabel(
            warning_frame,
            text="⚠️ ATTENZIONE",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        ).pack(pady=15)
        
        # Message
        ctk.CTkLabel(
            dialog,
            text="Stai per rimuovere le seguenti applicazioni:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 10), padx=20)
        
        # Scrollable list of apps
        apps_frame = ctk.CTkScrollableFrame(dialog, width=450, height=200)
        apps_frame.pack(pady=10, padx=20)
        
        for app_name in selected_apps.keys():
            ctk.CTkLabel(
                apps_frame,
                text=f"• {app_name}",
                font=ctk.CTkFont(size=13),
                anchor="w"
            ).pack(pady=3, padx=10, anchor="w")
        
        # Warning message
        ctk.CTkLabel(
            dialog,
            text="Questa operazione NON può essere annullata!",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=DANGER_COLOR
        ).pack(pady=(10, 5))
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        def on_cancel():
            dialog.destroy()
            self.log("Rimozione annullata dall'utente", "INFO")
        
        def on_confirm():
            dialog.destroy()
            self.btn_remove_bloat.configure(state="disabled", text="⏳ Rimozione in corso...")
            threading.Thread(target=self.remove_bloatware, args=(selected_apps,), daemon=True).start()
        
        # Cancel button
        btn_cancel = ctk.CTkButton(
            btn_frame,
            text="❌ Annulla",
            command=on_cancel,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6e7681",
            hover_color="#484f58"
        )
        btn_cancel.pack(side="left", padx=10)
        
        # Confirm button
        btn_confirm = ctk.CTkButton(
            btn_frame,
            text="✅ Conferma Rimozione",
            command=on_confirm,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=DANGER_COLOR,
            hover_color="#b62324"
        )
        btn_confirm.pack(side="left", padx=10)
    
    def remove_bloatware(self, selected_apps):
        import pythoncom
        pythoncom.CoInitialize()
        
        self.log("=== INIZIO RIMOZIONE BLOATWARE ===")
        total = len(selected_apps)
        
        for i, (app_name, app_code) in enumerate(selected_apps.items(), 1):
            self.log(f"[{i}/{total}] Rimozione {app_name}...")
            command = f"Get-AppxPackage *{app_code}* | Remove-AppxPackage"
            
            try:
                subprocess.run(["powershell", "-Command", command], check=True, capture_output=True)
                self.log(f"✓ {app_name} rimossa con successo", "SUCCESS")
            except:
                self.log(f"✗ Impossibile rimuovere {app_name}", "ERROR")
        
        self.log("=== RIMOZIONE BLOATWARE COMPLETATA ===", "SUCCESS")
        self.btn_remove_bloat.configure(state="normal", text="🗑️ RIMUOVI APP SELEZIONATE")
    
    # ===== OPTIMIZATIONS =====
    
    def disable_ads(self):
        if not self.is_admin():
            self.log("ERRORE: Privilegi di amministratore richiesti", "ERROR")
            return
        
        self.log("Disabilitazione pubblicità Windows...")
        self.btn_disable_ads.configure(state="disabled")
        
        try:
            paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\ContentDeliveryManager",
                r"SOFTWARE\Policies\Microsoft\Windows\CloudContent"
            ]
            for path in paths:
                key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_ALL_ACCESS)
                winreg.SetValueEx(key, "DisableWindowsConsumerFeatures", 0, winreg.REG_DWORD, 1)
                winreg.CloseKey(key)
            
            self.log("Pubblicità Windows disabilitate con successo", "SUCCESS")
        except Exception as e:
            self.log(f"Errore disabilitazione ads: {e}", "ERROR")
        finally:
            self.btn_disable_ads.configure(state="normal")
    
    def enable_scheduling(self):
        if not self.is_admin():
            self.log("ERRORE: Privilegi di amministratore richiesti", "ERROR")
            return
        
        exe_path = sys.executable if not getattr(sys, 'frozen', False) else sys.executable
        cmd = [
            "schtasks", "/create", "/tn", TASK_NAME,
            "/tr", f'"{exe_path}"',
            "/sc", "weekly", "/d", "SUN", "/st", "10:00", "/f", "/rl", "highest"
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            self.log("Pianificazione attivata: ogni Domenica alle 10:00", "SUCCESS")
        except Exception as e:
            self.log(f"Errore pianificazione: {e}", "ERROR")
    
    def disable_scheduling(self):
        if not self.is_admin():
            self.log("ERRORE: Privilegi di amministratore richiesti", "ERROR")
            return
        
        try:
            subprocess.run(["schtasks", "/delete", "/tn", TASK_NAME, "/f"], check=True, capture_output=True)
            self.log("Pianificazione disattivata", "SUCCESS")
        except:
            self.log("Nessuna pianificazione trovata", "WARNING")
    
    def install_vscode(self):
        self.log("Download VS Code in corso...")
        self.btn_install_vscode.configure(state="disabled", text="⏳ Download...")
        
        def download_install():
            try:
                download_cmd = "Invoke-WebRequest -Uri 'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user' -OutFile 'VSCodeSetup.exe'"
                subprocess.run(["powershell", "-Command", download_cmd], check=True, capture_output=True)
                
                self.log("Installazione VS Code...")
                self.btn_install_vscode.configure(text="⏳ Installazione...")
                
                install_cmd = "./VSCodeSetup.exe /VERYSILENT /NORESTART /MERGETASKS=!runcode"
                subprocess.run(["powershell", "-Command", install_cmd], check=True, capture_output=True)
                
                os.remove("VSCodeSetup.exe")
                self.log("VS Code installato con successo", "SUCCESS")
            except Exception as e:
                self.log(f"Errore installazione VS Code: {e}", "ERROR")
            finally:
                self.btn_install_vscode.configure(state="normal", text="Installa VS Code")
        
        threading.Thread(target=download_install, daemon=True).start()
    
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

if __name__ == "__main__":
    app = WindowsMaster()
    app.mainloop()
