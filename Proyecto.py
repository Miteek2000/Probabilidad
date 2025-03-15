import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk  # Para manejar imágenes

# Funciones de cálculo
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

# Nueva función para la distribución de Bernoulli
def bernoulli(x, p):
    if x not in [0, 1]:
        return 0
    return (p**x) * ((1 - p)**(1 - x)) * 100

# Nueva función para la distribución de Poisson
def poisson(x, lam):
    if x < 0 or lam < 0:
        return 0
    return (math.exp(-lam) * (lam**x) / math.factorial(x)) * 100

# Función para animar el submenú
def animar_submenu(marco, altura_final, paso=10):
    altura_actual = marco.winfo_height()
    if altura_actual < altura_final:
        marco.config(height=altura_actual + paso)
        ventana.after(10, animar_submenu, marco, altura_final, paso)
    else:
        marco.config(height=altura_final)

# Función para mostrar/ocultar el submenú
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

# Función para crear los botones del submenú
def crear_botones_submenu(distribucion):
    opciones = [
        "Calcular probabilidad",
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

# Función para manejar las acciones de los botones adicionales
def accion_boton_adicional(simbolo):
    global operador_seleccionado
    operador_seleccionado = simbolo
    recalcular_resultado()
    generar_histograma(distribucion_actual)  # Actualizar la gráfica al cambiar el operador

# Función para recalcular el resultado
def recalcular_resultado():
    if distribucion_actual == "Binomial":
        calcular_binomial()
    elif distribucion_actual == "Geométrica":
        calcular_geometrica()
    elif distribucion_actual == "Hipergeométrica":
        calcular_hipergeometrica()
    elif distribucion_actual == "Bernoulli":
        calcular_bernoulli()
    elif distribucion_actual == "Poisson":
        calcular_poisson()

# Función para manejar las acciones de los botones del submenú
def accion_boton(opcion, distribucion):
    if opcion == "Calcular probabilidad":
        calcular_probabilidad(distribucion)
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
    elif distribucion == "Bernoulli":
        formula = "Fórmula de Bernoulli:\n\nP(X = x) = p^x * (1-p)^(1-x)"
    elif distribucion == "Poisson":
        formula = "Fórmula de Poisson:\n\nP(X = x) = (e^(-λ) * λ^x) / x!"
    else:
        formula = "Fórmula no disponible."

    messagebox.showinfo("Fórmula", formula)

# Función para generar el histograma
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
            x = int(entry_x.get())  # Valor de x para resaltar
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
            x = int(entry_xg.get())  # Valor de x para resaltar
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
            x = int(entry_xh.get())  # Valor de x para resaltar
        except ValueError:
            mostrar_error("Valores inválidos para la distribución hipergeométrica.")
            return
    elif distribucion == "Bernoulli":
        try:
            p = float(entry_pb.get())
            datos = [bernoulli(i, p) for i in [0, 1]]
            etiquetas = ["0", "1"]
            titulo_grafica = f"Distribución de Bernoulli (p={p})"
            x = int(entry_xb.get())  # Valor de x para resaltar
        except ValueError:
            mostrar_error("Valores inválidos para la distribución de Bernoulli.")
            return
    elif distribucion == "Poisson":
        try:
            lam = float(entry_lam.get())
            max_eventos = 20
            datos = [poisson(i, lam) for i in range(max_eventos + 1)]
            etiquetas = [str(i) for i in range(max_eventos + 1)]
            titulo_grafica = f"Distribución de Poisson (λ={lam})"
            x = int(entry_xpois.get())  # Valor de x para resaltar
        except ValueError:
            mostrar_error("Valores inválidos para la distribución de Poisson.")
            return
    else:
        return

    # Crear una lista de colores para las barras
    colores = ['#FFB6C1'] * len(datos)  # Color pastel rosa claro por defecto
    if distribucion == "Bernoulli":
        if x == 0:
            colores[0] = '#ADD8E6'  # Color pastel azul claro para x=0
        else:
            colores[1] = '#ADD8E6'  # Color pastel azul claro para x=1
    else:
        if x < len(datos):
            colores[x] = '#ADD8E6'  # Color pastel azul claro para el valor de x

    # Crear el gráfico
    fig, ax = plt.subplots()
    ax.bar(etiquetas, datos, color=colores)
    ax.set_title(titulo_grafica)
    ax.set_xlabel("Valores")
    ax.set_ylabel("Probabilidad (%)")

    # Mostrar el gráfico en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=marco_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Función para mostrar un mensaje de error
def mostrar_error(mensaje):
    messagebox.showerror("Error", mensaje)

# Función para calcular la probabilidad según la distribución
def calcular_probabilidad(distribucion):
    global operador_seleccionado

    if distribucion == "Binomial":
        campos_binomial()
    elif distribucion == "Geométrica":
        campos_geometrica()
    elif distribucion == "Hipergeométrica":
        campos_hipergeometrica()
    elif distribucion == "Bernoulli":
        campos_bernoulli()
    elif distribucion == "Poisson":
        campos_poisson()

# Función para mostrar los campos de la distribución binomial
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

# Función para calcular la distribución binomial
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

# Función para mostrar los campos de la distribución geométrica
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

# Función para calcular la distribución geométrica
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

# Función para mostrar los campos de la distribución hipergeométrica
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

# Función para calcular la distribución hipergeométrica
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

# Función para mostrar los campos de la distribución de Bernoulli
def campos_bernoulli():
    limpiar_campos()

    global entry_xb, entry_pb
    tk.Label(ventana, text="Resultado (x, 0 o 1):", font=("Helvetica", 10)).pack(pady=5)
    entry_xb = ttk.Entry(ventana)
    entry_xb.pack(pady=5)

    tk.Label(ventana, text="Probabilidad de éxito (p):", font=("Helvetica", 10)).pack(pady=5)
    entry_pb = ttk.Entry(ventana)
    entry_pb.pack(pady=5)

    ttk.Button(ventana, text="Calcular", command=calcular_bernoulli).pack(pady=10)

# Función para calcular la distribución de Bernoulli
def calcular_bernoulli():
    try:
        x = int(entry_xb.get())
        p = float(entry_pb.get())

        if x not in [0, 1] or p < 0 or p > 1:
            mostrar_error("Valores inválidos para la distribución de Bernoulli.")
            return

        resultado = bernoulli(x, p)
        resultado_label.config(text=f"Resultado: {resultado:.2f}%")
        generar_histograma("Bernoulli")
    except ValueError:
        mostrar_error("Entrada inválida. Asegúrate de ingresar números válidos.")

# Función para mostrar los campos de la distribución de Poisson
def campos_poisson():
    limpiar_campos()

    global entry_xpois, entry_lam
    tk.Label(ventana, text="Número de eventos (x):", font=("Helvetica", 10)).pack(pady=5)
    entry_xpois = ttk.Entry(ventana)
    entry_xpois.pack(pady=5)

    tk.Label(ventana, text="Tasa de ocurrencia (λ):", font=("Helvetica", 10)).pack(pady=5)
    entry_lam = ttk.Entry(ventana)
    entry_lam.pack(pady=5)

    ttk.Button(ventana, text="Calcular", command=calcular_poisson).pack(pady=10)

# Función para calcular la distribución de Poisson
def calcular_poisson():
    try:
        x = int(entry_xpois.get())
        lam = float(entry_lam.get())

        if x < 0 or lam < 0:
            mostrar_error("Valores inválidos para la distribución de Poisson.")
            return

        resultado = poisson(x, lam)
        resultado_label.config(text=f"Resultado: {resultado:.2f}%")
        generar_histograma("Poisson")
    except ValueError:
        mostrar_error("Entrada inválida. Asegúrate de ingresar números válidos.")

# Función para limpiar los campos de entrada
def limpiar_campos():
    for widget in ventana.winfo_children():
        if widget not in [titulo, marco_botones, marco_submenu, marco_grafica, boton_salir, resultado_label]:
            widget.destroy()

# Función para aplicar el operador seleccionado
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

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de Probabilidades")
ventana.geometry("800x700")
ventana.configure(bg="#E6F3FF")  # Fondo pastel azul claro

# Título destacado
titulo = tk.Label(ventana, text="Calculadora de Probabilidades", font=("Helvetica", 16, "bold"), bg="#E6F3FF", fg="#333")
titulo.pack(pady=10)

# Marco para los botones principales
marco_botones = ttk.Frame(ventana, style="Marco.TFrame")
marco_botones.pack(side="left", padx=20, pady=10, fill="y")

# Estilo para el marco de botones
estilo = ttk.Style()
estilo.configure("Marco.TFrame", background="#FFE6F3")  # Color pastel rosa claro

# Título "Menú" en el lado izquierdo
titulo_menu = tk.Label(marco_botones, text="Menú", font=("Helvetica", 14, "bold"), bg="#FFE6F3", fg="#333")
titulo_menu.pack(pady=10)

# Icono decorativo (dado)
try:
    imagen_dado = Image.open("dado.png")  # Asegúrate de tener una imagen llamada "dado.png"
    imagen_dado = imagen_dado.resize((50, 50), Image.ANTIALIAS)
    icono_dado = ImageTk.PhotoImage(imagen_dado)
    label_icono = tk.Label(marco_botones, image=icono_dado, bg="#FFE6F3")
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
resultado_label = tk.Label(ventana, text="Resultado: ", font=("Helvetica", 12), bg="#E6F3FF", fg="#333")
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
    ("Distribución Hipergeométrica", "Hipergeométrica"),
    ("Distribución de Bernoulli", "Bernoulli"),  # Nuevo botón
    ("Distribución de Poisson", "Poisson")       # Nuevo botón
]

for texto, distribucion in opciones:
    boton = ttk.Button(marco_botones, text=texto, command=lambda d=distribucion: toggle_submenu(d), width=20)
    boton.pack(pady=5)

# Botón de salida
boton_salir = ttk.Button(ventana, text="Salir", command=ventana.destroy)
boton_salir.pack(side="bottom", pady=10)

# Ejecutar la ventana
ventana.mainloop()