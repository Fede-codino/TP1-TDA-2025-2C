import sys

# Complejidad: O(n)
def cargar_datos(ruta_archivo):
    with open(ruta_archivo, "r") as f:
        filas = f.read().strip().splitlines()[1:]  # salto el header directamente
    
    datos = []
    for fila in filas:
        partes = fila.split(",")
        tiempo = int(partes[0])
        peso = int(partes[1])
        datos.append([tiempo, peso])
    
    return datos
    
# Complejidad: O(n)
def calcular_impacto(registros):
    total_tiempo = 0
    impacto = 0
    for tiempo, peso in registros:
        total_tiempo += tiempo
        impacto += total_tiempo * peso
    return impacto


# Complejidad: O(n log n)
def mejor_orden_greedy(ruta_archivo):
    registros = cargar_datos(ruta_archivo)  # O(n)
    # ordenar por T_i / B_i
    registros.sort(key=lambda par: par[0] / par[1])  # O(n log n)
    impacto = calcular_impacto(registros)  # O(n)
    return registros, impacto


def main():
    ruta_archivo = sys.argv[1]
    orden, impacto = mejor_orden_greedy(ruta_archivo)

    print(f"El orden las batallas es: {orden}")
    print(f"Coeficiente de impacto: {impacto}")
    return impacto


if __name__ == "__main__":
    main()