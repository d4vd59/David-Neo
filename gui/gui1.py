import tkinter as tk

root = tk.Tk()
root.geometry("400x400")
root.minsize(width=250, height=250)
root.maxsize(width=600, height=600)
root.resizable(width=False, height=True)

label1 = tk.Label(root, text="POLSKA", bg="white")
label1.pack(side="top", expand=True, fill="both")

label2 = tk.Label(root, text="GUROM", bg="red")
label2.pack(side="bottom", expand=True,  fill="both")


root.mainloop()
