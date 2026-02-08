# 🚀 Windows Master Utility

**La soluzione completa per pulizia e ottimizzazione Windows**

Applicazione all-in-one per mantenere il tuo PC Windows pulito, veloce e ottimizzato.

---

## ✨ Caratteristiche

### 🧹 Pulizia Sistema
- **Svuota Cestino** - Elimina tutti i file dal Cestino
- **Cancella Download Obsoleti** - Rimuove file più vecchi di 7 giorni dalla cartella Download
- **Pulisci File Temporanei** - Elimina file temporanei utente e di sistema
- **Pulisci Prefetch** - Ottimizza i tempi di avvio (richiede Admin)
- **Cancella Windows.old** - Recupera spazio eliminando vecchie installazioni Windows

### 🗑️ Rimuovi Bloatware
Rimuovi app preinstallate Windows indesiderate:
- Microsoft Edge, ToDo, Mail, Camera, People
- Paint 3D, Clipchamp, DevHome
- Notepad, Sticky Notes, Get Started
- **Microsoft Copilot**
- **Microsoft Recall**

**Dialogo di conferma** mostra sempre l'elenco delle app prima della rimozione.

### ⚙️ Ottimizzazioni
- **Disabilita Pubblicità Windows** - Rimuove ads dal menu Start e dalle impostazioni
- **Pianificazione Automatica** - Pulizia automatica ogni Domenica alle 10:00
- **Installa VS Code** - Download e installazione automatica di Visual Studio Code

### 📊 Log & Report
- Log in tempo reale con timestamp
- Icone di stato (✅ ⚠️ ❌)
- Monitoraggio operazioni completate

---

## 📥 Download

**Windows Master Utility v1.0**

📦 [WindowsMaster.exe](dist/WindowsMaster.exe) (14.3 MB)

---

## 🚀 Installazione & Uso

### Requisiti
- Windows 10 o Windows 11
- **Privilegi di Amministratore** (raccomandato per tutte le funzionalità)

### Quick Start

1. **Download** - Scarica `WindowsMaster.exe`
2. **Click Destro** sul file → Seleziona **"Esegui come amministratore"**
3. **Conferma UAC** - Approva la richiesta di elevazione privilegi
4. L'applicazione si aprirà con 4 schede disponibili

---

## 📖 Guida all'Uso

### Scheda 🧹 Pulizia Sistema

1. Seleziona le operazioni desiderate (di default tutte selezionate)
2. Click su **"🚀 AVVIA PULIZIA SISTEMA"**
3. Attendi il completamento
4. Controlla i risultati nella scheda "📊 Log & Report"

### Scheda 🗑️ Rimuovi Bloatware

1. Scorri la lista e seleziona le app da rimuovere
2. Usa **"Seleziona Tutto"** per selezionare tutte le app
3. Click su **"🗑️ RIMUOVI APP SELEZIONATE"**
4. **Conferma** nel dialogo che mostra l'elenco delle app
5. Attendi il completamento della rimozione

> ⚠️ **ATTENZIONE**: La rimozione delle app è **irreversibile**!

### Scheda ⚙️ Ottimizzazioni

**Disabilita Pubblicità:**
- Click su "Disabilita Pubblicità" (una tantum)

**Pianificazione Automatica:**
- Click "✅ Attiva" per abilitare pulizia settimanale
- Click "❌ Disattiva" per rimuovere la pianificazione

**Installa VS Code:**
- Click "Installa VS Code" per download e installazione automatici

### Scheda 📊 Log & Report

- Visualizza in tempo reale tutte le operazioni
- Ogni riga ha timestamp e icona di stato
- Click "🗑️ Pulisci Log" per cancellare il log

---

## ⚠️ Avvertenze Importanti

> [!IMPORTANT]
> **Backup Consigliato**: Prima di usare questo tool, crea un punto di ripristino Windows.
> 
> Pannello di Controllo → Sistema → Protezione sistema → Crea

> [!WARNING]
> **Bloatware Removal**: Rimuovere alcune app di sistema (es. Microsoft Edge) potrebbe causare malfunzionamenti. Usa con cautela.

> [!CAUTION]
> **Windows.old**: Cancellare Windows.old è **irreversibile**. Assicurati di non aver bisogno di rollback.

---

## 🎯 Utilizzo Raccomandato

### Prima Esecuzione
1. **Crea punto di ripristino** Windows
2. Esegui come **Amministratore**
3. Vai alla scheda "⚙️ Ottimizzazioni"
4. Disabilita pubblicità (una volta)
5. Attiva pianificazione settimanale

### Pulizia Mensile Manuale
1. Scheda "🧹 Pulizia Sistema"
2. Seleziona tutte le opzioni
3. Avvia pulizia
4. Controlla log per spazio liberato

### Setup Nuovo PC
1. Esegui come Admin
2. Scheda "🗑️ Rimuovi Bloatware"
3. Seleziona app indesiderate
4. Conferma rimozione
5. Scheda "⚙️ Ottimizzazioni"
6. Disabilita ads + pianifica pulizia

---

## 🛠️ Dettagli Tecnici

**Tecnologie:**
- Python 3.14
- CustomTkinter (UI)
- WinShell (Cestino)
- WinReg (Registry)
- PyInstaller (Build)

**Dimensione:** ~14 MB (include Python runtime e librerie)

**Admin Elevation:** UAC richiesto all'avvio (`--uac-admin` flag)

---

## 📝 Changelog

### v1.0 (Febbraio 2026)
- ✅ Pulizia completa sistema (Cestino, Downloads, Temp, Prefetch, Windows.old)
- ✅ Rimozione bloatware con dialogo di conferma
- ✅ Disabilita pubblicità Windows
- ✅ Pianificazione automatica settimanale
- ✅ Installazione VS Code
- ✅ UI moderna con tema dark e gradienti
- ✅ Log dettagliato con timestamp e icone

---

## 🆘 Risoluzione Problemi

**L'app non si avvia:**
- Verifica di avere Windows 10/11
- Esegui come Amministratore
- Disabilita temporaneamente l'antivirus

**"Alcune operazioni sono fallite":**
- Assicurati di eseguire come Amministratore
- Chiudi programmi che potrebbero bloccare file temporanei

**La pianificazione non funziona:**
- Deve essere eseguita come Amministratore
- Verifica in "Utilità di pianificazione" → Cerca "Windows_Master_Auto_Clean"

---

## 👨‍💻 Autore

**Samuele Gonnella**

---

## 📜 Licenza

Uso personale e distribuzione libera.

---

## ⭐ Supporto

Se trovi utile questo tool, considera di:
- Condividerlo con amici e colleghi
- Segnalare bug o suggerimenti

---

**Windows Master Utility** - Mantieni il tuo PC pulito e veloce! 🚀
