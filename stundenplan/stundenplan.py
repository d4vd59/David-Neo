import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

root = tk.Tk()
root.title("Wochen-Stundenplan")
root.geometry("800x400")

wochen_offset = 0
zeitbloecke = ["8:00 - 9:30", "9:45 - 11:15", "11:30 - 13:00", "13:45 - 15:15", "15:30 - 17:00"]

frame_top = tk.Frame(root)
frame_top.pack(fill="x", pady=5, padx=5)

entry = tk.Entry(frame_top, font=("Arial", 11))
entry.pack(side="left", padx=5)

for txt, cmd in [("←", -1), ("Heute", 0), ("→", 1)]:
    tk.Button(frame_top, text=txt, command=lambda c=cmd: woche(c)).pack(side="left", padx=5)

def generiere_tage():
    heute = datetime.today() + timedelta(weeks=wochen_offset)
    start = heute - timedelta(days=heute.weekday())
    return [(start + timedelta(days=i)).strftime("%a %d.%m.") for i in range(6)]

def lade_stundenplan():
    tage = generiere_tage()
    columns = ["Zeit"] + tage
    tree["columns"] = columns

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    tree.delete(*tree.get_children())

    for block in zeitbloecke:
        tree.insert("", tk.END, values=[block] + ["" for _ in tage])

def woche(offset):
    global wochen_offset
    wochen_offset = wochen_offset + offset if offset else 0
    lade_stundenplan()

style = ttk.Style()
style.configure("Treeview", rowheight=40, font=("Arial", 9))
tree = ttk.Treeview(root, show="headings")
tree.pack(expand=True, fill="both", padx=5, pady=5)

lade_stundenplan()
root.mainloop()