import tkinter as tk
from tkinter import ttk


def delete_input():
    entry1.delete(0, tk.END)

# def print_entry_input():
#     ttk.Label(root, text=entry1.get()).pack()

root = tk.Tk()
root.title("TTK Programm")
root.geometry("500x500")

button= ttk.Button(root, text="Eingabe löschen", command=delete_input, state=tk.NORMAL)
button.pack(side="top")

quit_button = ttk.Button(root, text="Programm Beenden", command=root.destroy)
quit_button.pack(side="bottom")

entry1 = ttk.Entry(root, width=40)
entry1.pack()

entry1.insert(0, "Hier kannst du schreiben!")



for item in button.keys():
    print(item, ": ", button[item])

# image = Image.open("bruce.jpg").resize((500, 500))
# photo = ImageTk.PhotoImage(image)

# label1 = ttk.Label(root, image=photo)
# label1.pack()



root.mainloop()
