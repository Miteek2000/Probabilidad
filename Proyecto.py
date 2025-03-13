import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk  # Para manejar imágenes

# Funciones de cálculo (sin cambios)
def combinar(n, x):
    if n < x:
        return 0
    return math.comb(n, x)

def binomial(neventos, xexitox, pprobabilidadexitos):
    q = 1 - pprobabilidadexitos
    resultado = combinar(neventos, xexitox) * (pprobabilidadexitos**xexitox) * (q**(neventos - xexitox))
    return 100 * resultado

def geometrica(x, p):
    q = 1 - p
    resultado = (q**(x - 1)) * p
    return 100 * resultado

def hipergeometrica(N, K, n, x):
    try:
        if x > K or x > n or n > N or K > N:
            return 0
        numerador = combinar(K, x) * combinar(N - K, n - x)
        denominador = combinar(N, n)
        if denominador == 0:
            return 0
        resultado = (numerador / denominador) * 100
        return resultado
    except Exception as e:
        print(f"Error en hipergeometrica: {e}")
        return 0

# Función para animar el submenú (sin cambios)
def animar_submenu(marco, altura_final, paso=10):
    altura_actual = marco.winfo_height()
    if altura_actual < altura_final:
        marco.config(height=altura_actual + paso)
        ventana.after(10, animar_submenu, marco, altura_final, paso)
    else:
        marco.config(height=altura_final)

# Función para mostrar/ocultar el submenú (sin cambios)
def toggle_submenu(distribucion):
    global submenu_visible, distribucion_actual
    distribucion_actual = distribucion

    if submenu_visible:
        animar_submenu(marco_submenu, 0)
        submenu_visible = False
    else:
        for widget in marco_submenu.winfo_children():
            widget.destroy()
        crear_botones_submenu(distribucion)
        animar_submenu(marco_submenu, 250)
        submenu_visible = True

# Función para crear los botones del submenú (sin cambios)
def crear_botones_submenu(distribucion):
    opciones = [
        "Calcular probabilidad",
        "Generar gráfica",
        "Mostrar fórmula",
        "Limpiar campos"
    ]

    for texto in opciones:
        boton = ttk.Button(marco_submenu, text=texto, command=lambda t=texto: accion_boton(t, distribucion), width=20)
        boton.pack(pady=2)

    tk.Label(marco_submenu, text="Según:", font=("Helvetica", 10)).pack(pady=10)

    botones_adicionales = [
        ("Igual (=)", "="),
        ("Por lo menos (>=)", ">="),
        ("A lo mucho (<=)", "<="),
        ("Menor que (<)", "<"),
        ("Mayor que (>)", ">"),
        ("Diferente de (!=)", "!=")
    ]

    for texto, simbolo in botones_adicionales:
        boton = ttk.Button(marco_submenu, text=texto, command=lambda s=simbolo: accion_boton_adicional(s), width=20)
        boton.pack(pady=2)

# Función para manejar las acciones de los botones adicionales (sin cambios)
def accion_boton_adicional(simbolo):
    global operador_seleccionado
    operador_seleccionado = simbolo
    recalcular_resultado()

# Función para recalcular el resultado (sin cambios)
def recalcular_resultado():
    if distribucion_actual == "Binomial":
        calcular_binomial()
    elif distribucion_actual == "Geométrica":
        calcular_geometrica()
    elif distribucion_actual == "Hipergeométrica":
        calcular_hipergeometrica()

# Función para manejar las acciones de los botones del submenú (con cambios para mostrar fórmulas)
def accion_boton(opcion, distribucion):
    if opcion == "Calcular probabilidad":
        calcular_probabilidad(distribucion)
    elif opcion == "Generar gráfica":
        generar_histograma(distribucion)
    elif opcion == "Mostrar fórmula":
        mostrar_formula(distribucion)
    elif opcion == "Limpiar campos":
        limpiar_campos()

# Función para mostrar la fórmula correspondiente
def mostrar_formula(distribucion):
    if distribucion == "Binomial":
        formula = "Fórmula Binomial:\n\nP(X = x) = C(n, x) * p^x * (1-p)^(n-x)"
    elif distribucion == "Geométrica":
        formula = "Fórmula Geométrica:\n\nP(X = x) = (1-p)^(x-1) * p"
    elif distribucion == "Hipergeométrica":
        formula = "Fórmula Hipergeométrica:\n\nP(X = x) = [C(K, x) * C(N-K, n-x)] / C(N, n)"
    else:
        formula = "Fórmula no disponible."

    messagebox.showinfo("Fórmula", formula)

# Función para generar el histograma (con cambios para mostrar la probabilidad máxima)
def generar_histograma(distribucion):
    for widget in marco_grafica.winfo_children():
        widget.destroy()

    datos = []
    etiquetas = []
    if distribucion == "Binomial":
        try:
            n = int(entry_n.get())
            p = float(entry_p.get())
            datos = [binomial(n, i, p) for i in range(n + 1)]
            etiquetas = [str(i) for i in range(n + 1)]
            titulo_grafica = f"Distribución Binomial (n={n}, p={p})"
        except ValueError:
            mostrar_error("Valores inválidos para la distribución binomial.")
            return
    elif distribucion == "Geométrica":
        try:
            p = float(entry_pg.get())
            max_ensayos = 20
            datos = [geometrica(i, p) for i in range(1, max_ensayos + 1)]
            etiquetas = [str(i) for i in range(1, max_ensayos + 1)]
            titulo_grafica = f"Distribución Geométrica (p={p})"
        except ValueError:
            mostrar_error("Valores inválidos para la distribución geométrica.")
            return
    elif distribucion == "Hipergeométrica":
        try:
            N = int(entry_N.get())
            K = int(entry_K.get())
            n = int(entry_nh.get())
            datos = [hipergeometrica(N, K, n, i) for i in range(n + 1)]
            etiquetas = [str(i) for i in range(n + 1)]
            titulo_grafica = f"Distribución Hipergeométrica (N={N}, K={K}, n={n})"
        except ValueError:
            mostrar_error("Valores inválidos para la distribución hipergeométrica.")
            return
    else:
        return

    fig, ax = plt.subplots()
    colores_pasteles = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD']
    ax.bar(etiquetas, datos, color=colores_pasteles)
    ax.set_title(titulo_grafica, fontsize=12, fontweight="bold")
    ax.set_xlabel("Valores", fontsize=10)
    ax.set_ylabel("Probabilidad (%)", fontsize=10)

    # Calcular la probabilidad máxima según el operador seleccionado
    if distribucion == "Binomial":
        x = int(entry_x.get())
    elif distribucion == "Geométrica":
        x = int(entry_xg.get())
    elif distribucion == "Hipergeométrica":
        x = int(entry_xh.get())

    probabilidad_maxima = seleccionar(operador_seleccionado, datos, x)
    ax.axhline(y=probabilidad_maxima, color='red', linestyle='--', label=f"Probabilidad: {probabilidad_maxima:.2f}%")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=marco_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Función para mostrar un mensaje de error (sin cambios)
def mostrar_error(mensaje):
    messagebox.showerror("Error", mensaje)

# Función para calcular la probabilidad según la distribución (sin cambios)
def calcular_probabilidad(distribucion):
    global operador_seleccionado

    if distribucion == "Binomial":
        campos_binomial()
    elif distribucion == "Geométrica":
        campos_geometrica()
    elif distribucion == "Hipergeométrica":
        campos_hipergeometrica()

# Función para mostrar los campos de la distribución binomial (sin cambios)
def campos_binomial():
    limpiar_campos()

    global entry_n, entry_x, entry_p
    tk.Label(ventana, text="Número de eventos (n):", font=("Helvetica", 10)).pack(pady=5)
    entry_n = ttk.Entry(ventana)
    entry_n.pack(pady=5)

    tk.Label(ventana, text="Éxitos deseados (x):", font=("Helvetica", 10)).pack(pady=5)
    entry_x = ttk.Entry(ventana)
    entry_x.pack(pady=5)

    tk.Label(ventana, text="Probabilidad de éxito (p):", font=("Helvetica", 10)).pack(pady=5)
    entry_p = ttk.Entry(ventana)
    entry_p.pack(pady=5)

    ttk.Button(ventana, text="Calcular", command=calcular_binomial).pack(pady=10)

# Función para calcular la distribución binomial (sin cambios)
def calcular_binomial():
    try:
        n = int(entry_n.get())
        x = int(entry_x.get())
        p = float(entry_p.get())

        if n < 0 or x < 0 or x > n:
            mostrar_error("Valores inválidos para la distribución binomial.")
            return
        if p < 0 or p > 1:
            mostrar_error("La probabilidad p debe estar entre 0 y 1.")
            return

        datos = [binomial(n, i, p) for i in range(n + 1)]

        resultado = seleccionar(operador_seleccionado, datos, x)
        resultado_label.config(text=f"Resultado: {resultado:.2f}%")
        generar_histograma("Binomial")
    except ValueError:
        mostrar_error("Entrada inválida. Asegúrate de ingresar números válidos.")

# Función para mostrar los campos de la distribución geométrica (sin cambios)
def campos_geometrica():
    limpiar_campos()

    global entry_xg, entry_pg
    tk.Label(ventana, text="Número de ensayos hasta el primer éxito (x):", font=("Helvetica", 10)).pack(pady=5)
    entry_xg = ttk.Entry(ventana)
    entry_xg.pack(pady=5)

    tk.Label(ventana, text="Probabilidad de éxito (p):", font=("Helvetica", 10)).pack(pady=5)
    entry_pg = ttk.Entry(ventana)
    entry_pg.pack(pady=5)

    ttk.Button(ventana, text="Calcular", command=calcular_geometrica).pack(pady=10)

# Función para calcular la distribución geométrica (sin cambios)
def calcular_geometrica():
    try:
        x = int(entry_xg.get())
        p = float(entry_pg.get())

        if x < 1 or p < 0 or p > 1:
            mostrar_error("Valores inválidos para la distribución geométrica.")
            return

        datos = [geometrica(i, p) for i in range(1, 21)]

        resultado = seleccionar(operador_seleccionado, datos, x - 1)
        resultado_label.config(text=f"Resultado: {resultado:.2f}%")
        generar_histograma("Geométrica")
    except ValueError:
        mostrar_error("Entrada inválida. Asegúrate de ingresar números válidos.")

# Función para mostrar los campos de la distribución hipergeométrica (sin cambios)
def campos_hipergeometrica():
    limpiar_campos()

    global entry_N, entry_K, entry_nh, entry_xh
    tk.Label(ventana, text="Tamaño de la población (N):", font=("Helvetica", 10)).pack(pady=5)
    entry_N = ttk.Entry(ventana)
    entry_N.pack(pady=5)

    tk.Label(ventana, text="Número de éxitos en la población (K):", font=("Helvetica", 10)).pack(pady=5)
    entry_K = ttk.Entry(ventana)
    entry_K.pack(pady=5)

    tk.Label(ventana, text="Tamaño de la muestra (n):", font=("Helvetica", 10)).pack(pady=5)
    entry_nh = ttk.Entry(ventana)
    entry_nh.pack(pady=5)

    tk.Label(ventana, text="Número de éxitos en la muestra (x):", font=("Helvetica", 10)).pack(pady=5)
    entry_xh = ttk.Entry(ventana)
    entry_xh.pack(pady=5)

    ttk.Button(ventana, text="Calcular", command=calcular_hipergeometrica).pack(pady=10)

# Función para calcular la distribución hipergeométrica (sin cambios)
def calcular_hipergeometrica():
    try:
        N = int(entry_N.get())
        K = int(entry_K.get())
        n = int(entry_nh.get())
        x = int(entry_xh.get())

        if N < 0 or K < 0 or n < 0 or x < 0 or x > n or K > N or n > N:
            mostrar_error("Valores inválidos para la distribución hipergeométrica.")
            return

        datos = [hipergeometrica(N, K, n, i) for i in range(n + 1)]

        resultado = seleccionar(operador_seleccionado, datos, x)
        resultado_label.config(text=f"Resultado: {resultado:.2f}%")
        generar_histograma("Hipergeométrica")
    except ValueError:
        mostrar_error("Entrada inválida. Asegúrate de ingresar números válidos.")

# Función para limpiar los campos de entrada (sin cambios)
def limpiar_campos():
    for widget in ventana.winfo_children():
        if widget not in [titulo, marco_botones, marco_submenu, marco_grafica, boton_salir, resultado_label]:
            widget.destroy()

# Función para aplicar el operador seleccionado (sin cambios)
def seleccionar(operator, data, x):
    if operator == "=":
        return data[x]
    elif operator == "<=":
        return sum(data[:x + 1])
    elif operator == ">=":
        return sum(data[x:])
    elif operator == "<":
        return sum(data[:x])
    elif operator == ">":
        return sum(data[x + 1:])
    elif operator == "!=":
        return sum(data) - data[x]
    else:
        return 0

# Crear la ventana principal (con cambios estéticos)
ventana = tk.Tk()
ventana.title("Calculadora de Probabilidades")
ventana.geometry("800x700")
ventana.configure(bg="#F0F0F0")  # Fondo gris claro

# Título destacado
titulo = tk.Label(ventana, text="Calculadora de Probabilidades", font=("Helvetica", 16, "bold"), bg="#F0F0F0", fg="#333")
titulo.pack(pady=10)

# Marco para los botones principales (con colores formales)
marco_botones = ttk.Frame(ventana, style="Marco.TFrame")
marco_botones.pack(side="left", padx=20, pady=10, fill="y")

# Estilo para el marco de botones
estilo = ttk.Style()
estilo.configure("Marco.TFrame", background="#FFFFFF")  # Fondo blanco
estilo.configure("TButton", font=("Helvetica", 10), background="#4C72B0", foreground="white")  # Botones azules
estilo.map("TButton", background=[("active", "#55A868")])  # Cambio de color al pasar el mouse

# Título "Menú" en el lado izquierdo
titulo_menu = tk.Label(marco_botones, text="Menú", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#333")
titulo_menu.pack(pady=10)

# Icono decorativo (dado)
try:
    imagen_dado = Image.open("dado.png")  # Asegúrate de tener una imagen llamada "dado.png"
    imagen_dado = imagen_dado.resize((50, 50), Image.ANTIALIAS)
    icono_dado = ImageTk.PhotoImage(imagen_dado)
    label_icono = tk.Label(marco_botones, image=icono_dado, bg="#FFFFFF")
    label_icono.pack(pady=10)
except Exception as e:
    print(f"No se pudo cargar el ícono: {e}")

# Marco para el submenú (inicialmente oculto)
marco_submenu = ttk.Frame(ventana, height=0, relief="sunken", borderwidth=2, style="Marco.TFrame")
marco_submenu.pack(side="left", fill="y")

# Marco para la gráfica
marco_grafica = ttk.Frame(ventana)
marco_grafica.pack(side="right", fill=tk.BOTH, expand=True)

# Label para mostrar resultados
resultado_label = tk.Label(ventana, text="Resultado: ", font=("Helvetica", 12), bg="#F0F0F0", fg="#333")
resultado_label.pack(pady=10)

# Variable para controlar la visibilidad del submenú
submenu_visible = False

# Variable global para almacenar el operador seleccionado
operador_seleccionado = "="

# Variable global para almacenar la distribución actual
distribucion_actual = None

# Crear botones principales
opciones = [
    ("Distribución Binomial", "Binomial"),
    ("Distribución Geométrica", "Geométrica"),
    ("Distribución Hipergeométrica", "Hipergeométrica")
]

for texto, distribucion in opciones:
    boton = ttk.Button(marco_botones, text=texto, command=lambda d=distribucion: toggle_submenu(d), width=20)
    boton.pack(pady=5)

# Botón de salida
boton_salir = ttk.Button(ventana, text="Salir", command=ventana.destroy)
boton_salir.pack(side="bottom", pady=10)

# Ejecutar la ventana
ventana.mainloop()