import numpy as np
from math import exp
from sympy import symbols, lambdify, Poly
from sympy.abc import x  # variable simbólica x

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
def build_function():
    print("Selecciona el tipo de función:")
    print("1. Cociente polinomial: f(x) = P(x)/Q(x)")
    print("2. Exponencial + polinomio: f(x) = exp(x) + P(x)")

    choice = input("Opción (1 o 2): ")

    if choice == "1":
        # Entrada de coeficientes del numerador P(x)
        print("Coeficientes para P(x) (separados por coma, de menor a mayor grado):")
        P_coeffs = list(map(float, input().split(",")))

        # Entrada de coeficientes del denominador Q(x)
        print("Coeficientes para Q(x) (separados por coma, de menor a mayor grado):")
        Q_coeffs = list(map(float, input().split(",")))

        P = get_polynomial(P_coeffs)
        Q = get_polynomial(Q_coeffs)

        # lambdify convierte la expresión simbólica en una función de Python evaluable
        func = lambdify(x, P / Q, "numpy")
        return func

    elif choice == "2":
        # Entrada de coeficientes del polinomio P(x)
        print("Coeficientes para P(x) (separados por coma, de menor a mayor grado):")
        P_coeffs = list(map(float, input().split(",")))

        P = get_polynomial(P_coeffs)
        func = lambdify(x, exp(x) + P, "numpy")
        return func

    else:
        print("Opción no válida")
        exit(1)

# Función principal del programa
def main():
    # Se construye la función según la entrada del usuario
    func = build_function()

    # Entrada del intervalo de búsqueda
    print("Ingresa el intervalo de búsqueda [a, b]:")
    a = float(input("a: "))
    b = float(input("b: "))

    # Entrada de la precisión deseada
    print("Precisión deseada (epsilon):")
    epsilon = float(input("epsilon: "))

    # Se llama al algoritmo de búsqueda de Fibonacci
    x_opt, f_opt, final_interval = fibonacci_search(func, a, b, epsilon)

    # Se muestra el resultado
    print("\nResultado:")
    print(f"Óptimo aproximado x*: {x_opt}")
    print(f"f(x*): {f_opt}")
    print(f"Intervalo final: {final_interval}")

# Punto de entrada del script
if __name__ == "__main__":
    main()
