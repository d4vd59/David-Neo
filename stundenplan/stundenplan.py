import tkinter as tk
from ics import Calendar
import requests

root = tk.Tk()
root.title("Mein Stundenplan")
root.geometry("600x400")

termine_text = tk.Text(root, wrap=tk.WORD)
termine_text.pack(expand=True, fill="both")

url = "https://intranet.bib.de/ical/5780139642c4ec77bd1f67ec885f2e92"

response = requests.get(url)
response.raise_for_status()  

kalender = Calendar(response.text)
events_sorted = sorted(kalender.events, key=lambda e: e.begin)

for event in events_sorted:
    termine_text.insert(tk.END, f"{event.begin.format('DD.MM.YYYY HH:mm')} - {event.name}\n")

root.mainloop()