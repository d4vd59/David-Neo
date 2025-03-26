import tkinter as tk # Importiert das TK Inter Modul für GUI
from datetime import datetime, timedelta # Für Zeit und Datum
from ics import Calendar # Zum Parsen von ICS-Kalenderdateien
from tkinter import messagebox # Für Popup Boxen
import requests # Zum herunterladen von Daten über HTTP

base_url = "https://intranet.bib.de/ical/5780139642c4ec77bd1f67ec885f2e92" # Link zum Stundenplan im ICAL Format inkl. Token
zeitbloecke = ["8:00 - 9:30", "9:45 - 11:15", "11:30 - 13:00", "13:45 - 15:15", "15:30 - 17:00"] # Liste mit den Zeitblöcken
wochen_offset = 0 # Offset zur aktuellen Woche (0 = diese Woche, -1 = letzte Woche, +1 = nächste Woche usw.)

root = tk.Tk() # TK Start
root.title("Stundenplan") # Fenster-Titel
root.geometry("1000x550") # Fenster-Größe
root.configure(bg="white") # Hintergrundfarbe weiß

# Oberer Frame für Suchfeld und Buttons
frame_top = tk.Frame(root, bg="white")
frame_top.pack(fill="x", pady=10, padx=10)

# Wird aufgerufen, wenn das Eingabefeld angeklickt wird
def on_entry_click(event):
    if entry.get() == "Bitte Kürzel/Klasse eingeben":
        entry.delete(0, "end") # Löscht den Platzhaltertext
        entry.config(fg="black") # Setzt Textfarbe auf schwarz

# Eingabefeld für Klassen-/Kürzel
entry = tk.Entry(frame_top, font=("Segoe UI", 10), width=20, fg="gray")
entry.insert(0, "Bitte Kürzel/Klasse eingeben") # Platzhaltertext
entry.pack(side="left", padx=5)

# Bindet die Onclick Funktion an das Eingabefeld
entry.bind("<FocusIn>", on_entry_click)

# Button zum Laden des Stundenplans
tk.Button(frame_top, text="Laden", command=lambda: lade_stundenplan(), font=("Segoe UI", 9)).pack(side="left", padx=5) 
# Navigation: Zurück zur vorherigen Woche
tk.Button(frame_top, text="←", command=lambda: woche(-1), font=("Segoe UI", 9)).pack(side="left", padx=5)
# Button "Heute" – kehrt zur aktuellen Woche zurück
tk.Button(frame_top, text="Heute", command=lambda: woche(-wochen_offset), font=("Segoe UI", 9)).pack(side="left", padx=5)
# Navigation: Vor zur nächsten Woche
tk.Button(frame_top, text="→", command=lambda: woche(1), font=("Segoe UI", 9)).pack(side="left", padx=5)

# Hauptbereich für die Stundenplan-Tabelle
table_frame = tk.Frame(root, bg="white")
table_frame.pack(expand=True, fill="both", padx=10, pady=10)

# Generiert eine Liste mit Tagesdaten für die aktuelle Woche
def generiere_tage():
    heute = datetime.today() + timedelta(weeks=wochen_offset) # Aktuelles Datum + Wochen-Offset
    start = heute - timedelta(days=heute.weekday()) # Wochenanfang (Montag)
    tage = [(start + timedelta(days=i)) for i in range(6)] # Liste: Montag bis Samstag
    tage_formatiert = [tag.strftime("%a %d.%m.") for tag in tage] # Formatierung für Anzeige
    return tage_formatiert, start.isocalendar()[1], tage # Gibt formatierte Tage, KW und rohe Datumsobjekte zurück

# Lädt den Stundenplan (ICS) und zeigt ihn an
def lade_stundenplan():
    for widget in table_frame.winfo_children():
        widget.destroy() # # Entfernt alle bisherigen Inhalte der Tabelle (alte Woche)
    zellen = [] # Leere Liste 

    kuerzel = entry.get().strip() # Liest Text aus dem Eingabefeld
    if kuerzel == "" or kuerzel == "Bitte Kürzel/Klasse eingeben":
        url = base_url # Standard-URL verwenden, wenn nichts eingegeben wurde
    else:
        url = f"{base_url}/{kuerzel}" # Ansonsten URL erweitern mit Kürzel/Klasse

    tage_formatiert, _, tage_datetime = generiere_tage()

    heute_datum = datetime.today().date()
    heute_index = -1
    for i, tag_datum in enumerate(tage_datetime):
        if tag_datum.date() == heute_datum:
            heute_index = i
            break

    try:
        response = requests.get(url)
        if response.status_code != 200 or not response.text.strip():
            raise ValueError("Fehler beim Laden des Kalenders.")
        kalender = Calendar(response.text)
    except Exception as e:
        messagebox.showerror("Fehler", f"Das Kürzel '{kuerzel}' ist ungültig oder konnte nicht geladen werden.")
        return

    font_header = ("Segoe UI", 9, "bold")
    bg_header = "#B0B0B0"

    tk.Label(table_frame, text="Block", font=font_header, bg=bg_header, width=16, padx=5, pady=5,
             bd=0.5, relief="solid", justify="center").grid(row=0, column=0, sticky="nsew")

    for j, tag in enumerate(tage_formatiert):
        bg = "#ffaceb" if j == heute_index else bg_header
        tk.Label(table_frame, text=tag, font=font_header, bg=bg, width=18, padx=5, pady=5,
                 bd=0.5, relief="solid").grid(row=0, column=j+1, sticky="nsew")

    for i, block in enumerate(zeitbloecke):
        row = []
        bg_block = "#E8E8E8"
        block_nummeriert = f"Block {i+1}\n{block}"
        tk.Label(table_frame, text=block_nummeriert, font=("Segoe UI", 9), bg=bg_block,
                 width=16, height=3, bd=0.5, relief="solid", justify="center").grid(row=i+1, column=0, sticky="nsew")

        for j in range(len(tage_formatiert)):
            bg = "#E8E8E8" if j != heute_index else "#ffaceb"
            lbl = tk.Label(table_frame, text="", font=("Segoe UI", 9), bg=bg, width=18, height=3,
                           wraplength=140, justify="center", bd=0.5, relief="solid")
            lbl.grid(row=i+1, column=j+1, sticky="nsew")
            row.append(lbl)
        zellen.append(row)

    for event in kalender.events:
        event_tag = event.begin.datetime.date()
        for i, tag_datum in enumerate(tage_datetime):
            if tag_datum.date() == event_tag:
                for k, block in enumerate(zeitbloecke):
                    start, end = block.split(" - ")
                    start_time = datetime.strptime(start, "%H:%M").time()
                    end_time = datetime.strptime(end, "%H:%M").time()
                    if start_time <= event.begin.time() <= end_time:
                        current_text = zellen[k][i].cget("text")
                        new_text = f"{current_text}\n{event.name}" if current_text else event.name
                        zellen[k][i].config(text=new_text.strip())

def woche(offset):
    global wochen_offset
    wochen_offset += offset
    lade_stundenplan()

lade_stundenplan()
root.mainloop()