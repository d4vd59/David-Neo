import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from ics import Calendar
import requests

base_url = "https://intranet.bib.de/ical/5780139642c4ec77bd1f67ec885f2e92" 
zeitbloecke = ["8:00 - 9:30", "9:45 - 11:15", "11:30 - 13:00", "13:45 - 15:15", "15:30 - 17:00"] 
wochen_offset = 0 

root = tk.Tk()
root.title("Wochen-Stundenplan")
root.geometry("1100x500")

frame_top = tk.Frame(root)
frame_top.pack(fill="x", pady=5, padx=5)

entry = tk.Entry(frame_top, font=("Arial", 11))
entry.pack(side="left", padx=5)

tk.Button(frame_top, text="Laden", command=lambda: lade_stundenplan()).pack(side="left", padx=5)
tk.Button(frame_top, text="←", command=lambda: woche(-1)).pack(side="left", padx=5)
tk.Button(frame_top, text="Heute", command=lambda: woche(-wochen_offset)).pack(side="left", padx=5)
tk.Button(frame_top, text="→", command=lambda: woche(1)).pack(side="left", padx=5)

def generiere_tage():
    heute = datetime.today() + timedelta(weeks=wochen_offset)
    start = heute - timedelta(days=heute.weekday())
    return [(start + timedelta(days=i)).strftime("%a %d.%m.") for i in range(6)]

def lade_stundenplan():
    kuerzel = entry.get().strip()
    url = base_url if not kuerzel else f"{base_url}/{kuerzel}"
    tage = generiere_tage()
    columns = ["Block"] + tage
    tree["columns"] = columns

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=160, anchor="center")

    tree.delete(*tree.get_children())

    kalender = Calendar(requests.get(url).text)

    for i, block in enumerate(zeitbloecke):
        values = [block] + ["" for _ in tage]
        tree.insert("", tk.END, values=values)

    for event in kalender.events:
        tag = event.begin.datetime.strftime("%a %d.%m.")
        if tag in tage:
            for i, block in enumerate(zeitbloecke):
                start, end = block.split(" - ")
                start, end = datetime.strptime(start, "%H:%M"), datetime.strptime(end, "%H:%M")
                if start.time() <= event.begin.time() <= end.time():
                    item = tree.get_children()[i]
                    idx = tage.index(tag) + 1
                    val = tree.item(item, "values")
                    val = list(val)
                    val[idx] = f"{val[idx]}\n{event.name}" if val[idx] else event.name
                    tree.item(item, values=val)

def woche(offset):
    global wochen_offset
    wochen_offset += offset
    lade_stundenplan()

style = ttk.Style()
style.configure("Treeview", rowheight=60, font=("Arial", 10))
tree = ttk.Treeview(root, show="headings")
tree.pack(expand=True, fill="both", padx=5, pady=5)

lade_stundenplan()
root.mainloop()