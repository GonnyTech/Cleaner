import customtkinter as ctk
import os
import shutil
import winshell
import datetime
import threading
import sys
import ctypes
import subprocess
import argparse

# --- Constants ---
APP_NAME = "PC Cleaner Pro"
EXE_NAME = "CleanerApp.exe"  # Expected name after PyInstaller
TASK_NAME = "PC_Cleaner_Auto_Clean"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, auto_mode=False):
        super().__init__()
        self.auto_mode = auto_mode

        if not self.auto_mode:
            self.setup_ui()
        
        if self.auto_mode:
            # Run cleaning immediately and exit
            self.perform_cleaning_sync()
            sys.exit(0)

    def setup_ui(self):
        self.title(APP_NAME)
        self.geometry("700x550")
        self.resizable(False, False)

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1) # Tabs
        self.grid_rowconfigure(2, weight=0) # Button

        # Title
        self.label_title = ctk.CTkLabel(self, text="PC CLEANER PRO", font=ctk.CTkFont(size=26, weight="bold"))
        self.label_title.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Tabs
        self.tabview = ctk.CTkTabview(self, width=660)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.tabview.add("Pulizia")
        self.tabview.add("Pianificazione")
        self.tabview.add("Log")

        # --- Tab: Pulizia ---
        self.frame_cleaning = self.tabview.tab("Pulizia")
        self.frame_cleaning.grid_columnconfigure(0, weight=1)
        
        self.check_recycle = ctk.CTkCheckBox(self.frame_cleaning, text="Svuota Cestino")
        self.check_recycle.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.check_recycle.select()

        self.check_downloads = ctk.CTkCheckBox(self.frame_cleaning, text="Cancella Download (> 7 giorni)")
        self.check_downloads.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.check_downloads.select()

        self.check_temp = ctk.CTkCheckBox(self.frame_cleaning, text="Pulisci File Temporanei (User & System)")
        self.check_temp.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.check_temp.select()

        self.check_prefetch = ctk.CTkCheckBox(self.frame_cleaning, text="Pulisci Cartella Prefetch (Richiede Admin)")
        self.check_prefetch.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.check_prefetch.select()

        self.check_windows_old = ctk.CTkCheckBox(self.frame_cleaning, text="Cancella Windows.old (Richiede Admin)")
        self.check_windows_old.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        # --- Tab: Pianificazione ---
        self.frame_sched = self.tabview.tab("Pianificazione")
        self.label_sched = ctk.CTkLabel(self.frame_sched, text="Programma la pulizia automatica settimanale (Domenica ore 10:00)")
        self.label_sched.pack(padx=20, pady=20)

        self.btn_enable_sched = ctk.CTkButton(self.frame_sched, text="Attiva Pulizia Automatica", command=self.enable_scheduling)
        self.btn_enable_sched.pack(padx=20, pady=10)

        self.btn_disable_sched = ctk.CTkButton(self.frame_sched, text="Disattiva Pulizia Automatica", command=self.disable_scheduling, fg_color="red", hover_color="#8B0000")
        self.btn_disable_sched.pack(padx=20, pady=10)

        # --- Tab: Log ---
        self.textbox_log = ctk.CTkTextbox(self.tabview.tab("Log"), width=600, height=250)
        self.textbox_log.pack(padx=10, pady=10, fill="both", expand=True)
        self.textbox_log.configure(state="disabled")

        # Action Button
        self.btn_clean = ctk.CTkButton(self, text="AVVIA PULIZIA ORA", command=self.start_cleaning_thread, height=50, font=ctk.CTkFont(size=16, weight="bold"))
        self.btn_clean.grid(row=2, column=0, padx=20, pady=20)

    def log(self, message):
        if self.auto_mode:
            print(message)
            return
        self.textbox_log.configure(state="normal")
        self.textbox_log.insert("end", f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.textbox_log.see("end")
        self.textbox_log.configure(state="disabled")

    def start_cleaning_thread(self):
        self.btn_clean.configure(state="disabled")
        threading.Thread(target=self.perform_cleaning_sync, daemon=True).start()

    def perform_cleaning_sync(self):
        import pythoncom
        pythoncom.CoInitialize()
        self.log("--- INIZIO PULIZIA ---")
        
        # Admin check for critical tasks
        is_admin = self.is_admin()

        # 1. Recycle Bin
        if self.auto_mode or self.check_recycle.get():
            self.log("Svuotando il Cestino...")
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                self.log("Cestino svuotato.")
            except Exception as e:
                self.log(f"Errore Cestino: {e}")

        # 2. Downloads (> 7 days)
        if self.auto_mode or self.check_downloads.get():
            self.clean_folder(os.path.join(os.path.expanduser("~"), "Downloads"), days=7, label="Download")

        # 3. Temp Files
        if self.auto_mode or self.check_temp.get():
            # User Temp
            self.clean_folder(os.environ.get('TEMP'), label="Temp Utente", days=0)
            # System Temp
            if is_admin:
                self.clean_folder("C:\\Windows\\Temp", label="Temp Sistema", days=0)

        # 4. Prefetch
        if (self.auto_mode or self.check_prefetch.get()) and is_admin:
            self.clean_folder("C:\\Windows\\Prefetch", label="Prefetch", days=0)

        # 5. Windows.old
        if (self.auto_mode or self.check_windows_old.get()):
            path = "C:\\Windows.old"
            if os.path.exists(path):
                if not is_admin:
                    self.log("SKIP: Windows.old richiede Admin.")
                else:
                    self.log("Cancellazione Windows.old in corso...")
                    try:
                        # Use shell 'rd' for speed and to handle locks better if possible
                        subprocess.run(["cmd", "/c", f"rd /s /q {path}"], check=True)
                        self.log("Windows.old rimosso.")
                    except Exception as e:
                        self.log(f"Errore Windows.old: {e}")

        self.log("--- PULIZIA COMPLETATA ---")
        if not self.auto_mode:
            self.btn_clean.configure(state="normal")

    def clean_folder(self, path, days=0, label=""):
        if not path or not os.path.exists(path):
            self.log(f"Cartella {label} non trovata.")
            return

        self.log(f"Pulizia {label}...")
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        count = 0
        
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
            except Exception:
                pass # Usually busy files
        self.log(f"{label}: Rimossi {count} elementi.")

    def enable_scheduling(self):
        if not self.is_admin():
            self.log("ERRORE: Devi eseguire come Admin per pianificare.")
            return

        exe_path = sys.executable if not getattr(sys, 'frozen', False) else sys.executable
        # Command to create task: weekly, Sunday at 10:00
        cmd = [
            "schtasks", "/create", "/tn", TASK_NAME, 
            "/tr", f'"{exe_path}" --auto', 
            "/sc", "weekly", "/d", "SUN", "/st", "10:00", "/f", "/rl", "highest"
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            self.log("Pianificazione attivata: ogni Domenica alle 10:00.")
        except Exception as e:
            self.log(f"Errore pianificazione: {e}")

    def disable_scheduling(self):
        if not self.is_admin():
            self.log("ERRORE: Devi eseguire come Admin per disattivare.")
            return
        try:
            subprocess.run(["schtasks", "/delete", "/tn", TASK_NAME, "/f"], check=True, capture_output=True)
            self.log("Pianificazione disattivata.")
        except Exception as e:
            self.log(f"Pianificazione non trovata o errore: {e}")

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--auto", action="store_true", help="Run in silent mode")
    args = parser.parse_args()

    app = App(auto_mode=args.auto)
    if not args.auto:
        app.mainloop()
