import numpy as np
from math import exp
from sympy import symbols, lambdify, Poly, exp
from sympy.abc import x
import tkinter as tk
from tkinter import messagebox


# Genera los primeros n números de Fibonacci
def fibonacci_numbers(n):
    fibs = [1, 1]
    for i in range(2, n):
        fibs.append(fibs[-1] + fibs[-2])
    return fibs

# Determina el número mínimo de términos de Fibonacci necesarios para una precisión epsilon en el intervalo [a, b]
def required_fib_index(epsilon, a, b):
    fibs = [1, 1]
    n = 2
    while (b - a) / epsilon > fibs[-1]:
        fibs.append(fibs[-1] + fibs[-2])
        n += 1
    fibs.append(fibs[-1] + fibs[-2])  # Asegura fibs[n] existe
    return n, fibs


# Implementación principal del algoritmo de búsqueda de Fibonacci
def fibonacci_search(func, a, b, epsilon):
    n, fibs = required_fib_index(epsilon, a, b)
    k = 0
    L = b - a

    # Se calculan los dos puntos iniciales dentro del intervalo
    x1 = a + fibs[n - 2] / fibs[n] * L
    x2 = a + fibs[n - 1] / fibs[n] * L
    f1 = func(x1)
    f2 = func(x2)

    # Repetimos el proceso hasta que quede un intervalo suficientemente pequeño
    for i in range(1, n - 1):
        if f1 > f2:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + fibs[n - i - 1] / fibs[n - i] * (b - a)
            f2 = func(x2)
        else:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + fibs[n - i - 2] / fibs[n - i] * (b - a)
            f1 = func(x1)

    x_opt = (a + b) / 2  # punto óptimo aproximado
    return x_opt, func(x_opt), (a, b)


# Construye un polinomio a partir de una lista de coeficientes
def get_polynomial(coeffs):
    return sum(c * x**i for i, c in enumerate(coeffs))


# Construye la función simbólica en base a la elección del usuario
def build_function(choice, P_coeffs, Q_coeffs=None):
    # Se crea P(x) como un polinomio
    P = get_polynomial(P_coeffs)

    if choice == "1":
        # Crear la función Cociente Polinomial: P(x)/Q(x)
        if Q_coeffs:
            Q = get_polynomial(Q_coeffs)
            func = lambdify(x, P / Q, "numpy")  # Convertir P(x)/Q(x) en función de Python
        else:
            raise ValueError("Debe proporcionar coeficientes para Q(x) cuando elige la opción 1.")
    elif choice == "2":
        # Crear la función Exponencial + Polinomio: exp(x) + P(x)
        func = lambdify(x, exp(x) + P, "numpy")  # Convertir exp(x) + P(x) en función de Python
    else:
        raise ValueError("Opción no válida")

    return func


# Función que maneja la interfaz gráfica
def on_submit():
    try:
        # Obtener la opción seleccionada
        option = option_var.get()

        # Obtener los coeficientes y convertirlos en listas de floats
        if not entry_P.get():  # Verificar si el campo de P(x) está vacío
            raise ValueError("Debe ingresar los coeficientes de P(x).")

        # Si la opción es 1 (Cociente Polinomial), se espera una lista de coeficientes
        if option == "1":
            P_coeffs = list(map(float, entry_P.get().split(",")))
        else:
            # Si es opción 2 (Exponencial + Polinomio), se espera un solo coeficiente
            P_coeffs = [float(entry_P.get())]

        # Si se está usando la opción 1, necesitamos Q(x)
        if option == "1":
            if not entry_Q.get():  # Verificar si el campo de Q(x) está vacío
                raise ValueError("Debe ingresar los coeficientes de Q(x) cuando selecciona la opción 1.")
            Q_coeffs = list(map(float, entry_Q.get().split(",")))
        else:
            Q_coeffs = None  # Si es opción 2, no necesitamos Q(x)

        # Obtener intervalo y epsilon
        if not entry_a.get() or not entry_b.get() or not entry_epsilon.get():  # Verificar campos vacíos
            raise ValueError("Debe ingresar los valores para el intervalo [a, b] y la precisión (epsilon).")
        
        a = float(entry_a.get())
        b = float(entry_b.get())
        epsilon = float(entry_epsilon.get())

        # Crear la función
        func = build_function(option, P_coeffs, Q_coeffs)

        # Ejecutar la búsqueda de Fibonacci
        x_opt, f_opt, final_interval = fibonacci_search(func, a, b, epsilon)

        # Mostrar el resultado
        result_label.config(text=f"Óptimo aproximado x*: {x_opt}\n"
                                f"f(x*): {f_opt}\n"
                                f"Intervalo final: {final_interval}")

    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", "Ocurrió un error inesperado: " + str(e))


# Función para actualizar la visibilidad del campo de Q(x)
def update_Q_visibility(option):
    if option == "1":
        entry_Q.grid(row=4, column=1)
        label_Q.grid(row=4, column=0)
        p_hint_label.config(text="Ej: 1,2,3 para P(x) = 1 + 2x + 3x²")
    else:
        entry_Q.grid_forget()
        label_Q.grid_forget()
        p_hint_label.config(text="Solo un coeficiente. Ej: 4 para P(x) = 4")



# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Búsqueda de Fibonacci")

# Etiquetas y campos de entrada para la interfaz
tk.Label(root, text="Selecciona el tipo de función:").grid(row=0, column=0, columnspan=2)

option_var = tk.StringVar(value="1")
tk.Radiobutton(root, text="Cociente Polinomial", variable=option_var, value="1", command=lambda: update_Q_visibility("1")).grid(row=1, column=0, columnspan=2)
tk.Radiobutton(root, text="Exponencial + Polinomio", variable=option_var, value="2", command=lambda: update_Q_visibility("2")).grid(row=2, column=0, columnspan=2)

tk.Label(root, text="Coeficientes P(x):").grid(row=3, column=0)
entry_P = tk.Entry(root)
entry_P.grid(row=3, column=1)
p_hint_label = tk.Label(root, text="", fg="gray")
p_hint_label.grid(row=3, column=2, sticky="w")

label_Q = tk.Label(root, text="Coeficientes Q(x) (solo para opción 1):")
entry_Q = tk.Entry(root)

tk.Label(root, text="Intervalo [a, b]:").grid(row=5, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=5, column=1)
entry_b = tk.Entry(root)
entry_b.grid(row=5, column=2)

tk.Label(root, text="Precisión (epsilon):").grid(row=6, column=0)
entry_epsilon = tk.Entry(root)
entry_epsilon.grid(row=6, column=1)

# Botón de ejecución
submit_button = tk.Button(root, text="Ejecutar", command=on_submit)
submit_button.grid(row=7, column=0, columnspan=3)

# Etiqueta para mostrar los resultados
result_label = tk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=3)

# Inicializar la visibilidad de Q(x)
update_Q_visibility(option_var.get())

root.mainloop()
