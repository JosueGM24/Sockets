import numpy as np
import matplotlib.pyplot as plt

# Solicitar el arreglo de números separados por comas
numeros_str = input("Ingrese un arreglo de números separados por comas (ejemplo: 1,0,0,1,1,0): ")
numeros = [int(x) for x in numeros_str.split(',')]

# Solicitar el valor de pulso
pulso = float(input("Ingrese el valor del pulso (puede ser decimal): "))

# Solicitar la cantidad de ciclos para la señal senoidal
ciclos = int(input("Ingrese la cantidad de ciclos para la señal senoidal: "))

# Generar las coordenadas para la gráfica cuadrada
x_cuadrada = [i * pulso for i in range(len(numeros) + 1)]
y_cuadrada = numeros + [numeros[-1]]

# Generar las coordenadas para la gráfica senoidal
t_total = np.linspace(0, len(numeros) * ciclos * 2 * np.pi, 1000 * len(numeros))
y_senoidal = np.zeros_like(t_total)

# Llenar la señal senoidal según los valores del arreglo
for i, val in enumerate(numeros):
    t_segment = np.linspace(i * ciclos * 2 * np.pi, (i + 1) * ciclos * 2 * np.pi, 1000)
    if val == 1:
        y_segment = np.sin(t_segment)
    else:
        y_segment = 0.25 * np.sin(t_segment)
    y_senoidal[i * 1000:(i + 1) * 1000] = y_segment

# Crear la figura y los ejes
fig, axs = plt.subplots(2, 1, figsize=(10, 10))

# Graficar la señal cuadrada
axs[0].step(x_cuadrada, y_cuadrada, where='post')
axs[0].set_xlabel("Tiempo (s)")
axs[0].set_ylabel("Valor")
axs[0].set_title("Gráfica del arreglo con pulsos")
axs[0].grid(True)

# Graficar la señal senoidal
axs[1].plot(t_total, y_senoidal)
axs[1].set_xlabel("Tiempo (s)")
axs[1].set_ylabel("Amplitud")
axs[1].set_title("Señal senoidal")
axs[1].grid(True)

# Mostrar la gráfica
plt.tight_layout()
plt.show()
