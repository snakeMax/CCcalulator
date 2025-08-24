import tkinter as tk
import numpy as np


class Panel(tk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)
        label = tk.Label(self, text=text, font=("Arial", 18))
        label.pack(expand=True)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CC Calculator")
        self.geometry("700x500")

        # Panel container
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Panels dictionary
        self.panels = {}
        for name in ("Calculator", "Equations", "Image Reader"):
            panel = Panel(self.container, name)
            self.panels[name] = panel
            panel.grid(row=0, column=0, sticky="nsew")

        # Navigation buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x")
        for name in self.panels:
            btn = tk.Button(btn_frame, text=name, command=lambda n=name: self.show_panel(n))
            btn.pack(side="left", expand=True, fill="x")

        self.show_panel("Panel 1")

    def show_panel(self, name):
        panel = self.panels[name]
        panel.tkraise()


############### CODE








################

if __name__ == "__main__":
    app = App()
    app.mainloop()

