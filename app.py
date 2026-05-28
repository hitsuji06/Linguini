
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

conn = sqlite3.connect("linguini_pro.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa TEXT,
    producto TEXT,
    precio REAL,
    fecha TEXT
)
""")

conn.commit()

root = tk.Tk()
root.title("Linguini - Sistema de Restaurante")
root.geometry("1200x700")
root.configure(bg="#ECECEC")

pedido_actual = []

menu_items = [
    ("Hamburguesa", 120),
    ("Refresco", 35),
    ("Papas", 100),
    ("Queso +", 35),
    ("Boneless", 135),
    ("Pizza Personal", 150),
    ("Malteada", 85)
]

def agregar_producto(nombre, precio):
    pedido_actual.append((nombre, precio))
    actualizar_ticket()

def actualizar_ticket():
    ticket.delete("1.0", tk.END)

    total = 0

    for producto, precio in pedido_actual:
        ticket.insert(tk.END, f"{producto:<20} ${precio}\n")
        total += precio

    subtotal_label.config(text=f"Subtotal: ${total}")

def calcular_propina(porcentaje):
    subtotal = sum(precio for _, precio in pedido_actual)
    total = subtotal + (subtotal * porcentaje / 100)

    total_label.config(
        text=f"Total con propina ({porcentaje}%): ${total:.2f}"
    )

def guardar_pedido():
    if not pedido_actual:
        messagebox.showwarning("Aviso", "No hay productos agregados.")
        return

    mesa = mesa_var.get()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")

    for producto, precio in pedido_actual:
        cursor.execute(
            "INSERT INTO pedidos (mesa, producto, precio, fecha) VALUES (?, ?, ?, ?)",
            (mesa, producto, precio, fecha)
        )

    conn.commit()

    messagebox.showinfo(
        "Pedido Guardado",
        f"Pedido registrado correctamente en {mesa}"
    )

def limpiar():
    pedido_actual.clear()
    ticket.delete("1.0", tk.END)
    subtotal_label.config(text="Subtotal: $0")
    total_label.config(text="Total con propina: $0")

def mostrar_reportes():
    ventana = tk.Toplevel(root)
    ventana.title("Reporte de Ventas")
    ventana.geometry("500x400")

    tree = ttk.Treeview(
        ventana,
        columns=("Mesa", "Producto", "Precio", "Fecha"),
        show="headings"
    )
def ver_ticket_mesa():
    mesa_seleccionada = mesa_var.get()
    
    # Crear ventana emergente
    ventana_mesa = tk.Toplevel(root)
    ventana_mesa.title(f"Ticket Actual - {mesa_seleccionada}")
    ventana_mesa.geometry("400x500")
    ventana_mesa.configure(bg="white")
    
    # Título
    lbl_title = tk.Label(
        ventana_mesa, 
        text=f"PEDIDOS PENDIENTES: {mesa_seleccionada}", 
        font=("Arial", 16, "bold"), 
        bg="white"
    )
    lbl_title.pack(pady=15)
    
    # Área de texto para mostrar los productos
    txt_ticket = tk.Text(
        ventana_mesa, 
        width=40, 
        height=15, 
        font=("Courier", 12),
        state="disabled" # Solo lectura
    )
    txt_ticket.pack(pady=10)
    
    # Habilitar escritura temporalmente para insertar datos
    txt_ticket.config(state="normal")
    
    # Consultar a la base de datos
    cursor.execute("SELECT producto, precio FROM pedidos WHERE mesa = ?", (mesa_seleccionada,))
    rows = cursor.fetchall()
    
    total_mesa = 0
    
    if not rows:
        txt_ticket.insert(tk.END, "No hay pedidos registrados\npara esta mesa.")
    else:
        for producto, precio in rows:
            txt_ticket.insert(tk.END, f"{producto:<25} ${precio}\n")
            total_mesa += precio
            
    txt_ticket.config(state="disabled") # Bloquear edición
    
    # Mostrar Total
    lbl_total = tk.Label(
        ventana_mesa, 
        text=f"TOTAL MESA: ${total_mesa:.2f}", 
        font=("Arial", 14, "bold"), 
        fg="#E74C3C",
        bg="white"
    )
    lbl_total.pack(pady=10)
    
    # Botón para cerrar
    btn_cerrar = tk.Button(
        ventana_mesa, 
        text="Cerrar", 
        command=ventana_mesa.destroy,
        bg="#95A5A6",
        fg="white",
        font=("Arial", 10, "bold")
    )
    btn_cerrar.pack(pady=5)

    tree.heading("Mesa", text="Mesa")
    tree.heading("Producto", text="Producto")
    tree.heading("Precio", text="Precio")
    tree.heading("Fecha", text="Fecha")

    tree.pack(fill="both", expand=True)

    cursor.execute("SELECT mesa, producto, precio, fecha FROM pedidos")

    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

def realizar_corte():
    # 1. Calcular el total vendido
    cursor.execute("SELECT SUM(precio) FROM pedidos")
    resultado = cursor.fetchone()
    total_dia = resultado[0] if resultado[0] is not None else 0.0
    
    # 2. Obtener cantidad de tickets
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    num_pedidos = cursor.fetchone()[0]

    # 3. Mostrar resumen
    messagebox.showinfo(
        "CORTE DE CAJA", 
        f"Total Vendido: ${total_dia:.2f}\nPedidos Atendidos: {num_pedidos}\n\n¡Base de datos reiniciada para el siguiente turno!"
    )

    # 4. Limpiar la base de datos (Opcional: si quieres borrar el historial diario)
    cursor.execute("DELETE FROM pedidos")
    conn.commit()
    
    # 5. Limpiar la interfaz actual también
    limpiar()

header = tk.Frame(root, bg="#27AE60", height=70)
header.pack(fill="x")

title = tk.Label(
    header,
    text="LINGUINI - DEMO FUNCIONAL",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#27AE60"
)
title.pack(pady=15)

main = tk.Frame(root, bg="#ECECEC")
main.pack(fill="both", expand=True, padx=20, pady=20)

left = tk.Frame(main, bg="white", bd=2, relief="ridge")
left.pack(side="left", fill="both", expand=True, padx=10)

menu_title = tk.Label(
    left,
    text="MENÚ",
    font=("Arial", 20, "bold"),
    bg="white"
)
menu_title.pack(pady=15)

for nombre, precio in menu_items:
    row = tk.Frame(left, bg="white")
    row.pack(fill="x", padx=20, pady=8)

    label = tk.Label(
        row,
        text=f"{nombre} - ${precio}",
        font=("Arial", 13),
        bg="white"
    )
    label.pack(side="left")

    btn = tk.Button(
        row,
        text="Agregar",
        bg="#2ECC71",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda n=nombre, p=precio: agregar_producto(n, p)
    )
    btn.pack(side="right")

right = tk.Frame(main, bg="white", bd=2, relief="ridge")
right.pack(side="right", fill="both", expand=True, padx=10)

ticket_title = tk.Label(
    right,
    text="TICKET",
    font=("Arial", 20, "bold"),
    bg="white"
)
ticket_title.pack(pady=15)

mesa_var = tk.StringVar(value="Mesa 1")

mesa_combo = ttk.Combobox(
    right,
    textvariable=mesa_var,
    values=["Mesa 1", "Mesa 2", "Mesa 3", "Mesa 4", "Mesa 5"]
)
mesa_combo.pack(pady=10)

ticket = tk.Text(
    right,
    width=40,
    height=15,
    font=("Courier", 12)
)
ticket.pack(pady=10)

subtotal_label = tk.Label(
    right,
    text="Subtotal: $0",
    font=("Arial", 15, "bold"),
    bg="white"
)
subtotal_label.pack(pady=10)

propina_frame = tk.Frame(right, bg="white")
propina_frame.pack(pady=10)

for porcentaje in [10, 15, 20]:
    btn = tk.Button(
        propina_frame,
        text=f"{porcentaje}%",
        width=10,
        bg="#58D68D",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda p=porcentaje: calcular_propina(p)
    )
    btn.pack(side="left", padx=5)

total_label = tk.Label(
    right,
    text="Total con propina: $0",
    font=("Arial", 16, "bold"),
    bg="white"
)
total_label.pack(pady=15)

buttons = tk.Frame(right, bg="white")
buttons.pack(pady=20)

guardar_btn = tk.Button(
    buttons,
    text="Guardar Pedido",
    width=18,
    bg="#27AE60",
    fg="white",
    font=("Arial", 11, "bold"),
    command=guardar_pedido
)
guardar_btn.pack(side="left", padx=5)

cancelar_btn = tk.Button(
    buttons,
    text="Cancelar",
    width=18,
    bg="#E74C3C",
    fg="white",
    font=("Arial", 11, "bold"),
    command=limpiar
)
cancelar_btn.pack(side="left", padx=5)

reportes_btn = tk.Button(
    right,
    text="Ver Reportes",
    width=25,
    bg="#3498DB",
    fg="white",
    font=("Arial", 11, "bold"),
    command=mostrar_reportes
)
reportes_btn.pack(pady=10)

corte_btn = tk.Button(
    right,
    text="HACER CORTE FINAL",
    width=25,
    bg="#E74C3C",  # Color rojo para indicar acción crítica
    fg="white",
    font=("Arial", 11, "bold"),
    command=realizar_corte
)
corte_btn.pack(pady=10)

# ... (código anterior de reportes_btn)

ticket_mesa_btn = tk.Button(
    right,
    text="Ver Ticket por Mesa",
    width=25,
    bg="#F39C12",  # Color naranja para diferenciarlo
    fg="white",
    font=("Arial", 11, "bold"),
    command=ver_ticket_mesa
)
ticket_mesa_btn.pack(pady=10)

root.mainloop()
conn.close()
