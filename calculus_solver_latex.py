import tkinter as tk
from tkinter import ttk
from sympy import symbols, sympify, diff, integrate, pretty, latex
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from io import BytesIO
from PIL import Image, ImageTk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 10))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class CalculusSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculus Equation Solver (LaTeX All Steps)")
        self.x = symbols('x')
        self.status_var = tk.StringVar(value="Ready.")
        self.setup_style()
        self.create_widgets()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=("Arial", 14, "bold"), padding=8)
        style.configure('TLabel', font=("Arial", 13, "bold"))
        style.configure('Input.TEntry', font=("Arial", 18), padding=6)
        style.configure('Convert.TButton', font=("Arial", 14, "bold"), padding=8)

    def create_widgets(self):
        input_label = ttk.Label(self.root, text="Input", style='TLabel')
        input_label.grid(row=0, column=0, columnspan=5, sticky="w", padx=12, pady=(12, 0))
        self.input_var = tk.StringVar()
        input_entry = ttk.Entry(self.root, textvariable=self.input_var, style='Input.TEntry', justify='left')
        input_entry.grid(row=1, column=0, columnspan=5, sticky="ew", padx=12, pady=6, ipady=4)
        input_entry.config(background="#f0f8ff")

        self.convert_btn = None
        btns = [
            ("Derivative", self.solve_derivative, "Compute the derivative of f(x)"),
            ("Integral", self.solve_integral, "Compute the indefinite integral of f(x)"),
            ("Clear", self.clear_all, "Clear all input and output"),
            ("Convert Notation", self.convert_notation, "Convert natural notation to SymPy notation"),
            ("User Guide", self.show_user_guide, "Show user guide and examples")
        ]
        style = ttk.Style()
        style.configure('Derivative.TButton', background='#ffd699')  # light orange
        style.configure('Integral.TButton', background='#e0bbff')    # light purple
        style.configure('Clear.TButton', background='#b6fcd5')       # light green
        for i, (text, cmd, tip) in enumerate(btns):
            if text == "Derivative":
                btn = ttk.Button(self.root, text=text, command=cmd, style='Derivative.TButton')
            elif text == "Integral":
                btn = ttk.Button(self.root, text=text, command=cmd, style='Integral.TButton')
            elif text == "Clear":
                btn = ttk.Button(self.root, text=text, command=cmd, style='Clear.TButton')
            elif text == "Convert Notation":
                btn = ttk.Button(self.root, text=text, command=cmd, style='Convert.TButton')
                self.convert_btn = btn
            else:
                btn = ttk.Button(self.root, text=text, command=cmd)
            btn.grid(row=2, column=i, padx=6, pady=6, sticky="ew")
            ToolTip(btn, tip)
        self.input_var.trace_add('write', self.check_input_notation)
        self.highlight_convert_button(False)

        sol_label = ttk.Label(self.root, text="Solution (All Steps)", style='TLabel')
        sol_label.grid(row=3, column=0, columnspan=5, sticky="w", padx=12, pady=(10, 0))

        # Scrollable frame for LaTeX images
        self.sol_frame = tk.Frame(self.root, bg="#f9f9f9", bd=2, relief=tk.SUNKEN)
        self.sol_frame.grid(row=4, column=0, columnspan=5, sticky="nsew", padx=24, pady=12)
        self.sol_canvas = tk.Canvas(self.sol_frame, bg="#f9f9f9", highlightthickness=0)
        self.sol_scroll = ttk.Scrollbar(self.sol_frame, orient="vertical", command=self.sol_canvas.yview)
        self.sol_inner = tk.Frame(self.sol_canvas, bg="#f9f9f9")
        self.sol_inner.bind(
            "<Configure>", lambda e: self.sol_canvas.configure(scrollregion=self.sol_canvas.bbox("all")))
        self.sol_canvas.create_window((0, 0), window=self.sol_inner, anchor="nw")
        self.sol_canvas.configure(yscrollcommand=self.sol_scroll.set)
        self.sol_canvas.pack(side="left", fill="both", expand=True)
        self.sol_scroll.pack(side="right", fill="y")
        self.latex_imgs = []

        graph_label = ttk.Label(self.root, text="Graph", style='TLabel')
        graph_label.grid(row=5, column=0, columnspan=5, sticky="w", padx=12, pady=(10, 0))
        self.figure = plt.Figure(figsize=(6,3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        graph_widget = self.canvas.get_tk_widget()
        graph_widget.grid(row=6, column=0, columnspan=5, sticky="nsew", padx=12, pady=6)
        graph_widget.configure(height=220)  # minimum height for visibility

        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w', font=("Arial", 11))
        status_bar.grid(row=7, column=0, columnspan=5, sticky="ew", padx=0, pady=0)

        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_rowconfigure(6, weight=2)
        self.root.minsize(900, 700)

    def highlight_convert_button(self, highlight):
        if self.convert_btn:
            if highlight:
                self.convert_btn.configure(style='Convert.Highlight.TButton')
                style = ttk.Style()
                style.configure('Convert.Highlight.TButton', background='#ffe066', foreground='black')
            else:
                self.convert_btn.configure(style='Convert.TButton')
                style = ttk.Style()
                style.configure('Convert.Highlight.TButton', background='', foreground='')

    def check_input_notation(self, *args):
        import re
        expr = self.input_var.get()
        needs_convert = False
        if re.search(r'(\d)([a-zA-Z])', expr) or re.search(r'([a-zA-Z])([a-zA-Z])', expr):
            needs_convert = True
        if '^' in expr:
            needs_convert = True
        if re.search(r'(sin|cos|tan|exp|log|ln|sqrt)\s+[a-zA-Z0-9_]', expr):
            needs_convert = True
        if re.search(r'e\^', expr) or re.search(r'e\*\*', expr):
            needs_convert = True
        self.highlight_convert_button(needs_convert)

    def clear_all(self):
        self.input_var.set("")
        for widget in self.sol_inner.winfo_children():
            widget.destroy()
        self.latex_imgs.clear()
        self.ax.clear()
        self.canvas.draw()
        self.status_var.set("Cleared.")

    def convert_notation(self):
        expr = self.input_var.get()
        if expr.lower().startswith('f(x)='):
            prefix = 'f(x)='
            rhs = expr[5:]
        else:
            prefix = ''
            rhs = expr
        try:
            transformations = (standard_transformations + (implicit_multiplication_application, convert_xor))
            parsed = parse_expr(rhs, transformations=transformations)
            new_expr = prefix + str(parsed)
            self.input_var.set(new_expr)
            self.status_var.set("Converted to SymPy notation.")
        except Exception as e:
            self.status_var.set(f"Conversion failed: {e}")

    def parse_fx(self):
        expr = self.input_var.get().strip()
        if expr.lower().startswith('f(x)='):
            rhs = expr[5:].strip()
        else:
            rhs = expr
        return rhs

    def render_latex(self, latex_str):
        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, f"${latex_str}$", fontsize=13)  # smaller font size
        buf = BytesIO()
        plt.axis('off')
        plt.gca().set_axis_off()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2, transparent=True, dpi=150)
        plt.close(fig)
        buf.seek(0)
        img = Image.open(buf)
        return ImageTk.PhotoImage(img)

    def show_latex_steps(self, steps_latex):
        for widget in self.sol_inner.winfo_children():
            widget.destroy()
        self.latex_imgs.clear()
        for latex_str in steps_latex:
            img = self.render_latex(latex_str)
            self.latex_imgs.append(img)  # keep reference
            label = tk.Label(self.sol_inner, image=img, bg="#f9f9f9")
            label.pack(anchor="w", pady=6)

    def solve_derivative(self):
        from sympy import simplify
        self.status_var.set("Calculating derivative...")
        try:
            rhs = self.parse_fx()
            f = sympify(rhs)
            derivative = diff(f, self.x)
            simplified = simplify(derivative)
            steps_latex = [
                r"\text{Function: } f(x) = " + latex(f),
                r"\text{Step 1: Differentiate with respect to } x",
                r"f'(x) = " + latex(derivative),
                r"\text{Simplified Answer: } f'(x) = " + latex(simplified)
            ]
            self.show_latex_steps(steps_latex)
            self.plot_functions(f, simplified, label1="f(x)", label2="f'(x) (simplified)")
            self.status_var.set("Derivative calculated.")
        except Exception as e:
            self.show_latex_steps([r"\text{Error: }" + str(e)])
            self.status_var.set("Error in derivative calculation.")

    def solve_integral(self):
        from sympy import simplify
        self.status_var.set("Calculating integral...")
        try:
            rhs = self.parse_fx()
            f = sympify(rhs)
            integral = integrate(f, self.x)
            simplified = simplify(integral)
            steps_latex = [
                r"\text{Function: } f(x) = " + latex(f),
                r"\text{Step 1: Integrate with respect to } x",
                r"\int f(x)dx = " + latex(integral) + r" + C",
                r"\text{Simplified Answer: } \int f(x)dx = " + latex(simplified) + r" + C"
            ]
            self.show_latex_steps(steps_latex)
            self.plot_functions(f, simplified, label1="f(x)", label2="∫f(x)dx (simplified)")
            self.status_var.set("Integral calculated.")
        except Exception as e:
            self.show_latex_steps([r"\text{Error: }" + str(e)])
            self.status_var.set("Error in integral calculation.")

    def plot_functions(self, f1, f2, label1="f(x)", label2="g(x)"):
        self.ax.clear()
        try:
            f1_lambdified = lambda x: float(sympify(f1).subs(self.x, x))
            f2_lambdified = lambda x: float(sympify(f2).subs(self.x, x))
            x_vals = np.linspace(-10, 10, 400)
            y1_vals = []
            y2_vals = []
            for x in x_vals:
                try:
                    y1_vals.append(f1_lambdified(x))
                except Exception:
                    y1_vals.append(np.nan)
                try:
                    y2_vals.append(f2_lambdified(x))
                except Exception:
                    y2_vals.append(np.nan)
            if not (np.all(np.isnan(y1_vals)) and np.all(np.isnan(y2_vals))):
                self.ax.plot(x_vals, y1_vals, label=label1, color='blue', linewidth=2)
                self.ax.plot(x_vals, y2_vals, label=label2, color='red', linestyle='--', linewidth=2)
                self.ax.set_title('Graph', fontsize=14, fontweight='bold')
                self.ax.set_xlabel('x', fontsize=12)
                self.ax.set_ylabel('y', fontsize=12)
                self.ax.legend()
                self.ax.grid(True, linestyle=':')
            else:
                self.ax.text(0.5, 0.5, "Cannot plot: All values are undefined", ha='center', va='center')
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Cannot plot: {e}", ha='center', va='center')
        self.canvas.draw()

    def show_user_guide(self):
        guide = """\
Calculus Equation Solver - User Guide
====================================

1. Entering Equations:
----------------------
- You can enter equations in either natural math notation (e.g., x^2, sin x, e^x) or Pythonic/SymPy notation (e.g., x**2, sin(x), exp(x)).
- Always use the format: f(x)= ...
  Example: f(x)=x^2 + 2x + 1

2. Convert Notation:
---------------------
- If you enter an equation in natural notation, click 'Convert Notation' to automatically convert it to the required format for solving.
- Example: f(x)=sin x + e^x  →  f(x)=sin(x)+exp(x)

3. Derivative:
---------------
- Click 'Derivative' to compute the derivative of the entered function.
- The step-by-step solution and the graph of both the original function and its derivative will be shown.
- Example: f(x)=x^3 + 2x^2 - 5x + 7

4. Integral:
-------------
- Click 'Integral' to compute the indefinite integral of the entered function.
- The step-by-step solution and the graph of both the original function and its integral will be shown.
- Example: f(x)=cos x * e^x

5. Clear:
----------
- Click 'Clear' to reset the input and output areas.

6. Example Equations:
----------------------
- f(x)=x^2 + 3x + 2
- f(x)=sin x + cos x
- f(x)=e^x + ln x
- f(x)=1/(x^2 + 1)
- f(x)=sqrt x * e^-x

7. Notes:
----------
- Supported functions: sin, cos, tan, exp, ln, log, sqrt
- Use parentheses for clarity: sin(x), exp(x), etc.
- For e^x, you can use either e^x (natural) or exp(x) (SymPy).

Enjoy exploring calculus!
"""
        top = tk.Toplevel(self.root)
        top.title("User Guide")
        text = tk.Text(top, wrap="word", font=("Courier", 12), width=80, height=32)
        text.insert(tk.END, guide)
        text.config(state='disabled')
        text.pack(expand=True, fill="both")

def main():
    root = tk.Tk()
    app = CalculusSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
