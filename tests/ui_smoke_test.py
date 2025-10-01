import tkinter as tk

def run_smoke_tests():
    root = tk.Tk()
    root.title("StoryCraft MVP Smoke Test")
    root.geometry("800x600")

    # Basic label to confirm rendering

    label = tk.Label(root, text="UI Smoke Test: Window Loaded Successfully")
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    run_smoke_tests()