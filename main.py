
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import limpieza 
import analisis 
import visualizacion 


DATA = Path("data")
GRAFICOS = Path("graficos")


def main():
    """Corre el proyecto de principio a fin e imprime cada resultado."""
    pagos, productos, regiones = limpieza.cargar(DATA)
    print("== Diagnóstico ==")
    print(limpieza.diagnosticar(pagos))

    limpio, resumen = limpieza.limpiar(pagos)
    regiones.to_csv('regiones.csv')
    productos.to_csv('productos.csv')
    print(f"\n== Limpieza: {len(pagos)} filas antes, {len(limpio)} después ==")
    for decision, filas in resumen.items():
        print(filas, "-", decision)

    datos = analisis.transformar(limpio, productos, regiones)
    print(f"\n== Transformación: {len(datos)} filas (el merge no cambió el número) ==")

    print("\n== P1. Tasas por región (%) ==")
    print(analisis.tasas_por_region(datos))
    print("\n== P2. Dinero cobrado (US$), sin los 50 000 ==")
    print(analisis.dinero_por_producto_y_metodo(datos))
    print("\n== P2. Dinero cobrado (US$), con los 50 000 ==")
    print(analisis.dinero_por_producto_y_metodo(datos, con_50000=True))
    print("\n== P3. Tasas por segmento de riesgo (%) ==")
    print(analisis.tasas_por_riesgo(datos))

    visualizacion.graficar_todo(datos, GRAFICOS)
    print("\n== Gráficos guardados en graficos/ ==")
    


if __name__ == "__main__":
    main()