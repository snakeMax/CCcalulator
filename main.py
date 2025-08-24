import tkinter as tk
import numpy as np
import cv2
import pytesseract
from tkinter import filedialog
from PIL import Image


class Panel(tk.Frame):
    def __init__(self, parent, text):
        super().__init__(parent)
        label = tk.Label(self, text=text, font=("Arial", 18))
        label.grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=10)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CC Calculator")
        self.geometry("700x600")

        # Panel container
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Panels dictionary
        self.panels = {}
        # ...existing code...

        for name in ("Calculator", "Equations", "Image Reader"):
            panel = Panel(self.container, name)
            self.panels[name] = panel
            panel.grid(row=0, column=0, sticky="nsew")



            ############## Equations Panel

            if name == "Equations":
                self.eq_entry = tk.Entry(panel, font=("Arial", 24), borderwidth=2, relief="groove")
                self.eq_entry.grid(row=1, column=0, columnspan=4, pady=20, padx=20, sticky="we")

                self.eq_btn = tk.Button(panel, text="Calculate", command=self.calculate)
                self.eq_btn.grid(row=2, column=0, columnspan=4, pady=10)





            ############### Calculator Panel

            if name == "Calculator":
                self.calc_var = tk.StringVar()
                self.calc_entry = tk.Entry(panel, font=("Arial", 24), borderwidth=2, relief="groove",
                                          textvariable=self.calc_var, state="readonly")
                self.calc_entry.grid(row=1, column=0, columnspan=4, pady=20, padx=20, sticky="we")

                # Function to insert text into the entry
                def insert_char(char):
                    current = self.calc_var.get()
                    new = current + char
                    self.calc_entry.config(state="normal")
                    self.calc_var.set(new)
                    self.calc_entry.config(state="readonly")

                # Function to clear the entry
                def clear_entry():
                    self.calc_entry.config(state="normal")
                    self.calc_var.set("")
                    self.calc_entry.config(state="readonly")

                # Function to calculate
                def calculate():
                    try:
                        result = str(eval(self.calc_var.get()))
                        self.calc_entry.config(state="normal")
                        self.calc_var.set(result)
                        self.calc_entry.config(state="readonly")
                    except Exception:
                        self.calc_entry.config(state="normal")
                        self.calc_var.set("Error")
                        self.calc_entry.config(state="readonly")

                # Buttons for numbers and operators
                btns = [
                    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
                    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
                    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
                    ('0', 5, 0), ('.', 5, 1), ('C', 5, 2), ('+', 5, 3),
                    ('=', 6, 0, 4)
                ]


                for btn in btns:
                    text = btn[0]
                    row = btn[1]
                    col = btn[2]
                    colspan = btn[3] if len(btn) > 3 else 1
                    if text == 'C':
                        cmd = clear_entry
                    elif text == '=':
                        cmd = calculate
                        btn_font = ("Arial", 28, "bold")
                    else:
                        cmd = lambda t=text: insert_char(t)
                        btn_font = ("Arial", 18)
                    tk.Button(
                        panel,
                        text=text,
                        font=btn_font,
                        width=4,
                        height=2,
                        command=cmd
                    ).grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

                # Make the grid expand
                for i in range(7):
                    panel.rowconfigure(i, weight=1)
                for i in range(4):
                    panel.columnconfigure(i, weight=1)




            ############# Image Reader Panel

            if name == "Image Reader":
                self.img_label = tk.Label(panel, text="No image uploaded", font=("Arial", 14))
                self.img_label.grid(row=1, column=0, columnspan=4, pady=10)

                self.equation_var = tk.StringVar()
                self.equation_entry = tk.Entry(panel, textvariable=self.equation_var, font=("Arial", 18), width=30)
                self.equation_entry.grid(row=2, column=0, columnspan=4, pady=10)

                self.result_var = tk.StringVar()
                self.result_entry = tk.Entry(panel, textvariable=self.result_var, font=("Arial", 18), width=30, state="readonly")
                self.result_entry.grid(row=3, column=0, columnspan=4, pady=10)

                def upload_and_read():
                    file_path = filedialog.askopenfilename(
                        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
                    )
                    if file_path:
                        self.img_label.config(text=file_path)
                        # Read image with OpenCV
                        img = cv2.imread(file_path)
                        if img is not None:
                            # Convert to RGB for PIL
                            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                            pil_img = Image.fromarray(img_rgb)
                            # OCR with pytesseract
                            text = pytesseract.image_to_string(pil_img)
                            self.equation_var.set(text.strip())
                        else:
                            self.equation_var.set("Could not read image")

                def calculate_equation():
                    expr = self.equation_var.get()
                    # Print the raw OCR result for debugging
                    print(f"OCR extracted: {repr(expr)}")
                    try:
                        # Clean up the OCR result
                        expr = expr.replace('\n', '').replace('\r', '')
                        expr = expr.replace('x', '*').replace('X', '*').replace('÷', '/')
                        expr = expr.replace(' ', '')
                        # Remove any characters that are not numbers or math operators
                        import re
                        expr = re.sub(r'[^0-9\.\+\-\*\/\(\)]', '', expr)
                        print(f"Evaluating: {expr}")
                        result = str(eval(expr))
                        self.result_var.set(result)
                    except Exception as e:
                        print(f"Error: {e}")
                        self.result_var.set("Error")
                        

                tk.Button(panel, text="Upload Image", command=upload_and_read, font=("Arial", 14)).grid(row=4, column=0, columnspan=2, pady=10)
                tk.Button(panel, text="Calculate", command=calculate_equation, font=("Arial", 14)).grid(row=4, column=2, columnspan=2, pady=10)

                for i in range(5):
                    panel.rowconfigure(i, weight=1)
                for i in range(4):
                    panel.columnconfigure(i, weight=1)






        # Navigation buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x")
        for name in self.panels:
            btn = tk.Button(btn_frame, text=name, command=lambda n=name: self.show_panel(n))
            btn.pack(side="left", expand=True, fill="x")

        self.show_panel("Calculator")

    def calculate(self):
        try:
            result = eval(self.calc_entry.get())
            self.calc_entry.delete(0, tk.END)
            self.calc_entry.insert(0, str(result))
        except Exception:
            self.calc_entry.delete(0, tk.END)
            self.calc_entry.insert(0, "Error")

    def show_panel(self, name):
        panel = self.panels[name]
        panel.tkraise()


    def show_panel(self, name):
        panel = self.panels[name]
        panel.tkraise()


############### CODE




################

if __name__ == "__main__":
    app = App()
    app.mainloop()

