import tkinter as tk

root = tk.Tk()
root.title("Hello GUI")
root.geometry("800x400")


label = tk.Label(root, text="Hello, World!")
label.pack()


root.mainloop()
