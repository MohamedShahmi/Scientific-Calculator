import tkinter as tk
import math

# Main Window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("500x700")
root.minsize(500, 700)
root.resizable(True, True)

expression = ""
equation = tk.StringVar()
memory = 0.0

entry_field = tk.Entry(root, textvariable=equation, font=('Arial', 24, 'bold'),
                       bd=10, width=30, bg="#e1f7d5", fg="black", relief="ridge", justify="right")
entry_field.grid(row=0, column=0, columnspan=4, pady=20, padx=10, ipady=20)

def update_cursor():
    entry_field.icursor(len(expression))

def press(key):
    global expression
    expression += str(key)
    equation.set(expression)
    update_cursor()

def clear():
    global expression
    expression = ""
    equation.set("")

def equalpress():
    global expression
    try:
        result = str(eval(expression.replace('^', '**')))
        equation.set(result)
        expression = result
    except:
        equation.set(" error ")
        expression = ""

# Trig Functions
def sin_func(): apply_math_func(math.sin, deg_input=True)
def cos_func(): apply_math_func(math.cos, deg_input=True)
def tan_func(): apply_math_func(math.tan, deg_input=True)

def asin_func(): apply_math_func(math.asin, rad_output=True)
def acos_func(): apply_math_func(math.acos, rad_output=True)
def atan_func(): apply_math_func(math.atan, rad_output=True)

def apply_math_func(func, deg_input=False, rad_output=False):
    global expression
    try:
        val = float(expression)
        if deg_input:
            val = math.radians(val)
        result = func(val)
        if rad_output:
            result = math.degrees(result)
        equation.set(result)
        expression = str(result)
    except:
        equation.set(" error ")
        expression = ""

def log_func():
    global expression
    try:
        result = math.log10(float(expression))
        equation.set(result)
        expression = str(result)
    except:
        equation.set(" error ")
        expression = ""

def sqrt_func():
    global expression
    try:
        result = math.sqrt(float(expression))
        equation.set(result)
        expression = str(result)
    except:
        equation.set(" error ")
        expression = ""

def factorial_func():
    global expression
    try:
        num = int(expression)
        if num < 0:
            raise ValueError
        result = math.factorial(num)
        equation.set(result)
        expression = str(result)
    except:
        equation.set(" error ")
        expression = ""

# Memory
def memory_add():
    global memory, expression
    try:
        memory += float(expression)
        equation.set(f"Stored: {memory}")
        expression = ""
    except:
        equation.set(" error ")
        expression = ""

def memory_clear():
    global memory
    memory = 0.0
    equation.set("Memory Cleared")

def memory_recall():
    global memory, expression
    expression = str(memory)
    equation.set(expression)

# Style
def style_button(btn, bg, fg):
    btn.config(bg=bg, fg=fg, font=('Arial', 16, 'bold'), relief="raised", bd=3)
    btn.bind("<Enter>", lambda e: btn.config(bg="#f39c12", fg="white"))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg, fg=fg))

# Layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
    ('sin', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('C', 5, 3),
    ('asin', 6, 0), ('acos', 6, 1), ('atan', 6, 2), ('M+', 6, 3),
    ('log', 7, 0), ('√', 7, 1), ('^', 7, 2), ('x!', 7, 3),
    ('MR', 8, 0), ('MC', 8, 1)
]

actions = {
    'C': clear,
    '=': equalpress,
    'sin': sin_func,
    'cos': cos_func,
    'tan': tan_func,
    'asin': asin_func,
    'acos': acos_func,
    'atan': atan_func,
    'log': log_func,
    '√': sqrt_func,
    '^': lambda: press('^'),
    'x!': factorial_func,
    'M+': memory_add,
    'MR': memory_recall,
    'MC': memory_clear
}

# Buttons
for (text, row, col) in buttons:
    cmd = actions.get(text, lambda t=text: press(t))
    b = tk.Button(root, text=text, width=7, height=3, command=cmd)
    style_button(b, "#3498db", "white")
    b.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

for i in range(9): root.grid_rowconfigure(i, weight=1)
for i in range(4): root.grid_columnconfigure(i, weight=1)

# Keyboard support
def key_event(event):
    key = event.char
    if key in '0123456789.+-*/^':
        press(key)
    elif key == '\r':  # Enter
        equalpress()
    elif key == '\x08':  # Backspace
        global expression
        expression = expression[:-1]
        equation.set(expression)

root.bind("<Key>", key_event)

root.mainloop()
