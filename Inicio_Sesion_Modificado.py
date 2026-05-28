
import sys
import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import subprocess
import sys
import os

conn = sqlite3.connect("linguini_pro.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    correo TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("SELECT * FROM usuarios WHERE correo = ?", ("admin@linguini.com",))
usuario = cursor.fetchone()

if not usuario:
    cursor.execute(
        "INSERT INTO usuarios (correo, password) VALUES (?, ?)",
        ("admin@linguini.com", "1234")
    )
    conn.commit()

def iniciar_sesion():
    correo = entry_correo.get()
    password = entry_password.get()

    cursor.execute(
        "SELECT * FROM usuarios WHERE correo = ? AND password = ?",
        (correo, password)
    )

    usuario = cursor.fetchone()

    if usuario:
        messagebox.showinfo("Login", "Inicio de sesión exitoso")
        ventana.destroy()
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_script = os.path.join(directorio_actual, "appv1.py")
        subprocess.run([sys.executable, ruta_script])
    else:
        messagebox.showerror("Error", "Correo o contraseña incorrectos")

ventana = tk.Tk()
ventana.title("Linguini Login")
ventana.geometry("300x250")
ventana.resizable(False, False)

frame = tk.Frame(ventana, padx=20, pady=20)
frame.pack(expand=True)

label_titulo = tk.Label(
    frame,
    text="Bienvenido a Linguini",
    font=("Arial", 14, "bold")
)
label_titulo.pack(pady=(0, 20))

label_correo = tk.Label(frame, text="Correo Electrónico:")
label_correo.pack(anchor="w")

entry_correo = tk.Entry(frame, width=30)
entry_correo.pack(pady=(0, 10))

label_password = tk.Label(frame, text="Contraseña:")
label_password.pack(anchor="w")

entry_password = tk.Entry(frame, width=30, show="*")
entry_password.pack(pady=(0, 20))

btn_login = tk.Button(
    frame,
    text="Iniciar Sesión",
    command=iniciar_sesion,
    bg="#4CAF50",
    fg="white",
    width=15
)
btn_login.pack()

ventana.mainloop()
