import tkinter as tk
from tkinter import messagebox

def iniciar_sesion():
    correo = entry_correo.get()
    password = entry_password.get()
    
    if correo and password:
        messagebox.showinfo("Login", f"Intentando ingresar con: {correo}")
    else:
        messagebox.showwarning("Error", "Por favor, completa todos los campos")

ventana = tk.Tk()
ventana.title("Linguini")
ventana.geometry("300x250")
ventana.resizable(False, False)

frame = tk.Frame(ventana, padx=20, pady=20)
frame.pack(expand=True)

label_titulo = tk.Label(frame, text="Bienvenido a Linguini", font=("Arial", 14, "bold"))
label_titulo.pack(pady=(0, 20))

label_correo = tk.Label(frame, text="Correo Electrónico:")
label_correo.pack(anchor="w")
entry_correo = tk.Entry(frame, width=30)
entry_correo.pack(pady=(0, 10))

label_password = tk.Label(frame, text="Contraseña:")
label_password.pack(anchor="w")
entry_password = tk.Entry(frame, width=30, show="*") 
entry_password.pack(pady=(0, 20))

btn_login = tk.Button(frame, text="Iniciar Sesión", command=iniciar_sesion, bg="#4CAF50", fg="white", width=15)
btn_login.pack()

ventana.mainloop()