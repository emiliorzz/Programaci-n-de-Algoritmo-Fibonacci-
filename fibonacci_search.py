import tkinter as tk
from tkinter import messagebox

# Función Fibonacci (esto se mantiene como está en tu código original)
def fibonacci_search(func, a, b, epsilon):
    fibs = [1, 1]
    n = 2
    while (b - a) / epsilon > fibs[-1]:
        fibs.append(fibs[-1] + fibs[-2])
        n += 1

    x1 = a + fibs[n - 2] / fibs[n] * (b - a)
    x2 = a + fibs[n - 1] / fibs[n] * (b - a)
    
    while (b - a) > epsilon:
        if func(x1) < func(x2):
            b = x2
        else:
            a = x1
        n -= 1
        x1 = a + fibs[n - 2] / fibs[n] * (b - a)
        x2 = a + fibs[n - 1] / fibs[n] * (b - a)
    
    return (a + b) / 2  # Retorna el valor óptimo

# Función para llamar la búsqueda cuando el usuario presiona el botón
def on_submit():
    try:
        # Obtener los valores de los campos de entrada
        option = int(option_var.get())  # Opción seleccionada
        a = float(entry_a.get())  # Valor de 'a'
        b = float(entry_b.get())  # Valor de 'b'
        epsilon = float(entry_epsilon.get())  # Valor de 'epsilon'
        
        # Selección de la función que el usuario desea
        if option == 1:
            func = lambda x: (x**2)  # Función ejemplo: x^2 (cociente polinomial)
        elif option == 2:
            func = lambda x: (x**2 + 3*x + 2)  # Función ejemplo: x^2 + 3x + 2 (exponencial + polinomio)
        else:
            messagebox.showerror("Error", "Opción inválida.")
            return

        # Llamar a la función fibonacci_search
        result = fibonacci_search(func, a, b, epsilon)

        # Mostrar el resultado en el mensaje
        messagebox.showinfo("Resultado", f"El valor óptimo es: {result}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error: {e}")

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Búsqueda de Fibonacci")

# Crear y colocar los widgets (campos de texto, botones, etc.)
tk.Label(root, text="Seleccionar opción:").grid(row=0, column=0)
option_var = tk.StringVar(value="1")
tk.Radiobutton(root, text="Función cociente polinomial (x^2)", variable=option_var, value="1").grid(row=1, column=0)
tk.Radiobutton(root, text="Función exponencial + polinomio (x^2 + 3x + 2)", variable=option_var, value="2").grid(row=2, column=0)

tk.Label(root, text="Intervalo (a):").grid(row=3, column=0)
entry_a = tk.Entry(root)
entry_a.grid(row=3, column=1)

tk.Label(root, text="Intervalo (b):").grid(row=4, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=4, column=1)

tk.Label(root, text="Precisión (epsilon):").grid(row=5, column=0)
entry_epsilon = tk.Entry(root)
entry_epsilon.grid(row=5, column=1)

# Botón para ejecutar
submit_button = tk.Button(root, text="Ejecutar", command=on_submit)
submit_button.grid(row=6, column=0, columnspan=2)

# Iniciar la aplicación
root.mainloop()
