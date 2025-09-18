import subprocess
import time
import random
import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# ---------------------------------------------------
# Generar datasets reproducibles dentro de "datatest"
# ---------------------------------------------------
def generar_dataset(ruta_archivo, n, seed=42):
    if os.path.exists(ruta_archivo):
        return  # no lo regenero si ya existe

    random.seed(seed + n)  # semilla única para cada tamaño
    with open(ruta_archivo, "w") as f:
        f.write("tiempo,peso\n")  # header
        for _ in range(n):
            tiempo = random.randint(1, 1000)
            peso = random.randint(1, 1000)
            f.write(f"{tiempo},{peso}\n")

# ---------------------------------------------------
# Medir ejecución del script a evaluar
# ---------------------------------------------------
def medir_tiempo(script, archivo_csv):
    inicio = time.time()
    subprocess.run(["python3", script, archivo_csv], capture_output=True)
    fin = time.time()
    return fin - inicio

# ---------------------------------------------------
# Funciones de ajuste (modelos teóricos)
# ---------------------------------------------------
def modelo_lineal(n, a, b):
    return a * n + b

def modelo_nlogn(n, a, b):
    return a * n * np.log2(n) + b

# ---------------------------------------------------
# Experimento
# ---------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Benchmark de complejidad algorítmica")
    parser.add_argument("script", help="Ruta al archivo Python a evaluar (ej: batallas.py)")
    args = parser.parse_args()
    script = args.script

    # Crear carpeta datatest si no existe
    carpeta = "datatest"
    os.makedirs(carpeta, exist_ok=True)

    # Valores de tamanio_datos
    tamanio_datos = [1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000, 1024000, 2048000]
    tiempos = []

    for n in tamanio_datos:
        archivo = os.path.join(carpeta, f"dataset_{n}.csv")
        generar_dataset(archivo, n)
        t = medir_tiempo(script, archivo)
        tiempos.append(t)
        print(f"n={n}, tiempo={t:.4f} segundos")

    tamanio_datos = np.array(tamanio_datos)
    tiempos = np.array(tiempos)

    # Ajuste lineal (O(n))
    popt_lineal, _ = curve_fit(modelo_lineal, tamanio_datos, tiempos)
    ajuste_lineal = modelo_lineal(tamanio_datos, *popt_lineal)

    # Ajuste n log n (O(n log n))
    popt_nlogn, _ = curve_fit(modelo_nlogn, tamanio_datos, tiempos)
    ajuste_nlogn = modelo_nlogn(tamanio_datos, *popt_nlogn)

    # ---------------------------------------------------
    # Graficar resultados
    # ---------------------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(tamanio_datos, tiempos, "o-", label="Datos empíricos")
    plt.plot(tamanio_datos, ajuste_lineal, "--", label="Ajuste O(n)")
    plt.plot(tamanio_datos, ajuste_nlogn, "--", label="Ajuste O(n log n)")

    plt.xlabel("Tamaño de entrada (n)", fontsize=14)
    plt.ylabel("Tiempo (s)", fontsize=14)
    plt.title(f"Medición empírica de {os.path.basename(script)}", fontsize=16)
    plt.xticks(tamanio_datos, rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    print("\nCoeficientes ajuste O(n):", popt_lineal)
    print("Coeficientes ajuste O(n log n):", popt_nlogn)


if __name__ == "__main__":
    main()
