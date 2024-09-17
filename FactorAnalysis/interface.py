import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import Factoranalysis
def run_program(file_path, var1, var2):
    # Replace this with the code that processes the file and variables
    print(f"Running program on {file_path} with variables {var1} and {var2}")
    Factoranalysis.run_Factor_analysis(file_path, int(var2), int(var1))

def browse_file():
    filename = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def submit():
    file_path = file_entry.get()
    var1 = float(var1_entry.get())
    var2 = float(var2_entry.get())
    run_program(file_path, var1, var2)

app = tk.Tk()
app.title("Factor Analysis Interface")

tk.Label(app, text="Select file:").pack(pady=5)
file_entry = tk.Entry(app, width=50)
file_entry.pack(pady=5)
tk.Button(app, text="Browse", command=browse_file).pack(pady=5)

tk.Label(app, text="topics number:").pack(pady=5)
var1_entry = tk.Entry(app)
var1_entry.pack(pady=5)

tk.Label(app, text="minimum topic size:").pack(pady=5)
var2_entry = tk.Entry(app)
var2_entry.pack(pady=5)

tk.Button(app, text="Run", command=submit).pack(pady=20)

app.mainloop()
