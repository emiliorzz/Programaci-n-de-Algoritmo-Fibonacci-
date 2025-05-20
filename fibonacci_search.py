import numpy as np
from math import exp
from sympy import symbols, lambdify, Poly
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
    P = get_polynomial(P_coeffs)

    if choice == "1":
        # Construir la función Cociente Polinomial
        if Q_coeffs:
            Q = get_polynomial(Q_coeffs)
            func = lambdify(x, P / Q, "numpy")
        else:
            raise ValueError("Debe proporcionar coeficientes para Q(x) cuando elige la opción 1.")
    elif choice == "2":
        # Construir la función Exponencial + Polinomio
        func = lambdify(x, exp(x) + P, "numpy")
    else:
        raise ValueError("Opción no válida")

    return func


# Función que maneja la interfaz gráfica
def on_submit():
    try:
        # Obtener la opción seleccionada
        option = option_var.get()

        # Obtener los coeficientes y convertirlos en listas de floats
        P_coeffs = list(map(float, entry_P.get().split(",")))

        if option == "1":
            Q_coeffs = list(map(float, entry_Q.get().split(",")))
        else:
            Q_coeffs = None

        # Obtener intervalo y epsilon
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

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Búsqueda de Fibonacci")

# Etiquetas y campos de entrada para la interfaz
tk.Label(root, text="Selecciona el tipo de función:").grid(row=0, column=0, columnspan=2)

option_var = tk.StringVar(value="1")
tk.Radiobutton(root, text="Cociente Polinomial", variable=option_var, value="1").grid(row=1, column=0, columnspan=2)
tk.Radiobutton(root, text="Exponencial + Polinomio", variable=option_var, value="2").grid(row=2, column=0, columnspan=2)

tk.Label(root, text="Coeficientes P(x):").grid(row=3, column=0)
entry_P = tk.Entry(root)
entry_P.grid(row=3, column=1)

tk.Label(root, text="Coeficientes Q(x) (solo para opción 1):").grid(row=4, column=0)
entry_Q = tk.Entry(root)
entry_Q.grid(row=4, column=1)

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

# Iniciar la interfaz gráfica
root.mainloop()

