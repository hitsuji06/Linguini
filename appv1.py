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

modo_eliminar = False

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

        ticket.insert(
            tk.END,
            f"{producto:<20} ${precio}\n"
        )

        total += precio

    subtotal_label.config(
        text=f"Subtotal: ${total}"
    )

def calcular_propina(porcentaje):

    subtotal = sum(precio for _, precio in pedido_actual)

    total = subtotal + (subtotal * porcentaje / 100)

    total_label.config(
        text=f"Total con propina ({porcentaje}%): ${total:.2f}"
    )

def guardar_pedido():

    if not pedido_actual:

        messagebox.showwarning(
            "Aviso",
            "No hay productos agregados."
        )

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

    pedido_actual.clear()

    ticket.delete("1.0", tk.END)

    subtotal_label.config(text="Subtotal: $0")

    total_label.config(text="Total con propina: $0")

def limpiar():

    pedido_actual.clear()

    ticket.delete("1.0", tk.END)

    subtotal_label.config(text="Subtotal: $0")

    total_label.config(text="Total con propina: $0")

def mostrar_reportes():

    ventana = tk.Toplevel(root)

    ventana.title("Reporte de Ventas")

    ventana.geometry("700x500")

    ventana.configure(bg="white")

    titulo = tk.Label(
        ventana,
        text="REPORTE DE PEDIDOS POR MESA",
        font=("Arial", 18, "bold"),
        bg="white"
    )

    titulo.pack(pady=10)

    reporte_texto = tk.Text(
        ventana,
        width=80,
        height=30,
        font=("Courier", 11),
        bg="white"
    )

    reporte_texto.pack(padx=10, pady=10)

    mesas = ["Mesa 1", "Mesa 2", "Mesa 3", "Mesa 4", "Mesa 5"]

    for mesa in mesas:

        reporte_texto.insert(
            tk.END,
            f"\n{'='*50}\n"
        )

        reporte_texto.insert(
            tk.END,
            f"{mesa}\n"
        )

        reporte_texto.insert(
            tk.END,
            f"{'='*50}\n"
        )

        cursor.execute(
            "SELECT producto, precio, fecha FROM pedidos WHERE mesa = ? ORDER BY id",
            (mesa,)
        )

        pedidos = cursor.fetchall()

        if pedidos:

            total_mesa = 0

            for producto, precio, fecha in pedidos:

                reporte_texto.insert(
                    tk.END,
                    f"{producto:<25} ${precio:<8} {fecha}\n"
                )

                total_mesa += precio

            reporte_texto.insert(
                tk.END,
                f"\nTOTAL {mesa}: ${total_mesa}\n"
            )

        else:

            reporte_texto.insert(
                tk.END,
                "No hay pedidos registrados.\n"
            )

def generar_ticket_mesa():

    mesa = mesa_var.get()

    cursor.execute(
        "SELECT producto, precio, fecha FROM pedidos WHERE mesa = ? ORDER BY id",
        (mesa,)
    )

    pedidos = cursor.fetchall()

    if not pedidos:

        messagebox.showwarning(
            "Sin pedidos",
            f"No hay pedidos registrados en {mesa}"
        )

        return

    ventana_ticket = tk.Toplevel(root)

    ventana_ticket.title(f"Ticket Final - {mesa}")

    ventana_ticket.geometry("450x550")

    ventana_ticket.configure(bg="white")

    titulo = tk.Label(
        ventana_ticket,
        text="LINGUINI",
        font=("Arial", 22, "bold"),
        bg="white"
    )

    titulo.pack(pady=10)

    mesa_label = tk.Label(
        ventana_ticket,
        text=f"{mesa}",
        font=("Arial", 16, "bold"),
        bg="white"
    )

    mesa_label.pack()

    fecha_label = tk.Label(
        ventana_ticket,
        text=datetime.now().strftime("%Y-%m-%d %H:%M"),
        font=("Arial", 11),
        bg="white"
    )

    fecha_label.pack(pady=5)

    separador = tk.Label(
        ventana_ticket,
        text="------------------------------------------",
        bg="white"
    )

    separador.pack()

    total = 0

    for producto, precio, fecha in pedidos:

        producto_label = tk.Label(
            ventana_ticket,
            text=f"{producto:<20} ${precio}",
            font=("Courier", 12),
            bg="white"
        )

        producto_label.pack(anchor="w", padx=40)

        total += precio

    separador2 = tk.Label(
        ventana_ticket,
        text="------------------------------------------",
        bg="white"
    )

    separador2.pack(pady=10)

    total_ticket = tk.Label(
        ventana_ticket,
        text=f"TOTAL: ${total}",
        font=("Arial", 16, "bold"),
        bg="white"
    )

    total_ticket.pack(pady=10)

    cursor.execute(
        "DELETE FROM pedidos WHERE mesa = ?",
        (mesa,)
    )

    conn.commit()

    ticket.delete("1.0", tk.END)

    subtotal_label.config(text="Subtotal: $0")

    total_label.config(text="Total con propina: $0")

    messagebox.showinfo(
        "Mesa Liberada",
        f"{mesa} quedó disponible para nuevos clientes."
    )

    cerrar_btn = tk.Button(
        ventana_ticket,
        text="Cerrar",
        bg="#E74C3C",
        fg="white",
        font=("Arial", 11, "bold"),
        command=ventana_ticket.destroy
    )

    cerrar_btn.pack(pady=15)

def crear_producto_menu(nombre, precio):

    row = tk.Frame(left, bg="white")

    row.pack(fill="x", padx=20, pady=8)

    label = tk.Label(
        row,
        text=f"{nombre} - ${precio}",
        font=("Arial", 13),
        bg="white"
    )

    label.pack(side="left")

    def accion_producto():

        global modo_eliminar

        if modo_eliminar:

            row.destroy()

            for item in menu_items:

                if item[0] == nombre and item[1] == precio:

                    menu_items.remove(item)

                    break

            modo_eliminar = False

            messagebox.showinfo(
                "Producto Eliminado",
                f"{nombre} fue eliminado del menú."
            )

        else:

            agregar_producto(nombre, precio)

    btn = tk.Button(
        row,
        text="Agregar",
        bg="#2E85CC",
        fg="white",
        font=("Arial", 10, "bold"),
        command=accion_producto
    )

    btn.pack(side="right")

def agregar_nueva_comida():

    nombre = nombre_comida_entry.get()

    precio = precio_comida_entry.get()

    if nombre == "" or precio == "":

        messagebox.showwarning(
            "Campos Vacíos",
            "Completa el nombre y precio."
        )

        return

    try:

        precio = float(precio)

    except:

        messagebox.showerror(
            "Error",
            "El precio debe ser numérico."
        )

        return

    menu_items.append((nombre, precio))

    crear_producto_menu(nombre, precio)

    nombre_comida_entry.delete(0, tk.END)

    precio_comida_entry.delete(0, tk.END)

    messagebox.showinfo(
        "Producto Agregado",
        f"{nombre} agregado correctamente."
    )

def activar_modo_eliminar():

    global modo_eliminar

    modo_eliminar = True

    messagebox.showinfo(
        "Modo Eliminar",
        "Ahora presiona la comida que deseas eliminar."
    )

header = tk.Frame(root, bg="#2E52B2", height=70)

header.pack(fill="x")

title = tk.Label(
    header,
    text="LINGUINI",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#2E52B2"
)

title.pack(pady=10)

main = tk.Frame(root, bg="#ECECEC")

main.pack(fill="both", expand=True, padx=20, pady=20)

left = tk.Frame(main, bg="white", bd=2, relief="ridge")

left.pack(side="left", fill="both", expand=True, padx=10)

menu_title = tk.Label(
    left,
    text="MENÚ",
    font=("Arial", 24, "bold"),
    bg="white"
)

menu_title.pack(pady=15)

for nombre, precio in menu_items:

    crear_producto_menu(nombre, precio)

separador = tk.Label(
    left,
    text="---------------------------",
    bg="white",
    font=("Arial", 12)
)

separador.pack(pady=10)

nuevo_producto_label = tk.Label(
    left,
    text="Agregar Nueva Comida",
    font=("Arial", 16, "bold"),
    bg="white"
)

nuevo_producto_label.pack(pady=5)

formulario_frame = tk.Frame(left, bg="white")

formulario_frame.pack(pady=10)

nombre_label = tk.Label(
    formulario_frame,
    text="Agregar comida:",
    font=("Arial", 12, "bold"),
    bg="white"
)

nombre_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

nombre_comida_entry = tk.Entry(
    formulario_frame,
    font=("Arial", 12),
    width=20
)

nombre_comida_entry.grid(row=0, column=1, padx=5, pady=5)

precio_label = tk.Label(
    formulario_frame,
    text="Agregar precio:",
    font=("Arial", 12, "bold"),
    bg="white"
)

precio_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

precio_comida_entry = tk.Entry(
    formulario_frame,
    font=("Arial", 12),
    width=20
)

precio_comida_entry.grid(row=1, column=1, padx=5, pady=5)

agregar_comida_btn = tk.Button(
    left,
    text="Agregar al Menú",
    bg="#F39C12",
    fg="white",
    font=("Arial", 11, "bold"),
    command=agregar_nueva_comida
)

agregar_comida_btn.pack(pady=10)

eliminar_comida_btn = tk.Button(
    left,
    text="Eliminar Comida",
    bg="#C0392B",
    fg="white",
    font=("Arial", 11, "bold"),
    command=activar_modo_eliminar
)

eliminar_comida_btn.pack(pady=5)

right = tk.Frame(main, bg="white", bd=2, relief="ridge")

right.pack(side="right", fill="both", expand=True, padx=10)

ticket_title = tk.Label(
    right,
    text="TICKET",
    font=("Arial", 24, "bold"),
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
    font=("Arial", 18, "bold"),
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
        bg="#536DFE",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda p=porcentaje: calcular_propina(p)
    )

    btn.pack(side="left", padx=5)

total_label = tk.Label(
    right,
    text="Total con propina: $0",
    font=("Arial", 18, "bold"),
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

botones_extra = tk.Frame(right, bg="white")

botones_extra.pack(pady=10)

reportes_btn = tk.Button(
    botones_extra,
    text="Ver Reportes",
    width=18,
    bg="#3498DB",
    fg="white",
    font=("Arial", 11, "bold"),
    command=mostrar_reportes
)

reportes_btn.pack(side="left", padx=5)

ticket_mesa_btn = tk.Button(
    botones_extra,
    text="Ticket Mesa",
    width=18,
    bg="#8E44AD",
    fg="white",
    font=("Arial", 11, "bold"),
    command=generar_ticket_mesa
)

ticket_mesa_btn.pack(side="left", padx=5)

root.mainloop()

conn.close()