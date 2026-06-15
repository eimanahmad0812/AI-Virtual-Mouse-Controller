import tkinter as tk

def open_calibration():
    root = tk.Tk()
    root.title("Calibration UI")
    tk.Label(root, text="Hold hand still for 5s...").pack(pady=20)
    btn = tk.Button(root, text="Start Calibration", command=lambda: print("Calibrating..."))
    btn.pack()
    root.mainloop()

if __name__ == "__main__":
    open_calibration()