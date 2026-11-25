# Análisis de pagos Fintech




## Qué hay en esta carpeta

```
proyecto_resuelto/
├── README.md                       -> esta guía
├── mini_proyecto_m03/              -> la entrega, tal como la pedía la consigna
│   ├── main.py                     -> corre todo: limpieza -> análisis -> gráficos
│   ├── limpieza.py
│   ├── analisis.py
│   ├── visualizacion.py
│   ├── graficos/                   -> los 3 PNG
│ 
```
## En qué orden leerlo


1. **Abre `mini_proyecto_m03/README.md`.** Es lo que pedía el proyecto, escrito con la misma estructura.
2. **Abre los `.py`** en este orden: `limpieza.py` → `analisis.py` → `visualizacion.py` → `main.py`. Debajo de cada pregunta, en `analisis.py`, está la respuesta con su cifra.

## Cómo correrlo (opcional)


1. Descomprime `dataset_proyecto_final.zip` y copia `pagos_fintech.csv`, `productos.csv` y `regiones.csv` en `mini_proyecto_m03/data/`.
2. Instala lo necesario: `pip install pandas matplotlib seaborn jupyter`.
3. Entra en `mini_proyecto_m03/` y corre `python main.py`. Imprime cada resultado y vuelve a generar los gráficos.



## Hallazgos
1.Caribe tiene la mayor tasa de failed (11.06 %) y Europa la mayor de contracargos (3.78 %). Sumadas, Europa (14.80 %) y Caribe (14.71 %) casi empatan; Andina tiene 0 contracargos y queda en 10.09 %.

2.En el segmento de riesgo con los pagos fallidos,  High falla 18.62 % y Low 9.83 %, casi el doble. Pero el tipo de fallo cambia: High concentra los contracargos (12.32 %, el fallo más caro)

3.En el segmento de riesgo los pagos failed an chargeback ninguno registra pago de 50,0000 todos los 50,000 entran en status paid.


|
## Estructura del proyecto

```
mini_proyecto_m03/
├── limpieza.py        # cargar, diagnosticar, limpiar, reporte
├── analisis.py        # transformar (merge con productos y regiones) y análisis
├── visualizacion.py   # generar_graficos
├── main.py            # ejecuta todo el flujo
├── graficos/          # imágenes generadas (.png)
├── pagos_fintech.csv
├── productos.csv
└── regiones.csv
```

## Flujo de trabajo

1. **Carga** (`cargar`): lee el CSV con `keep_default_na=False, na_values=''` para conservar valores como `"NA"` que son datos reales.
2. **Diagnóstico** (`diagnosticar`): nulos, porcentaje de nulos, valores únicos y tipo de dato por columna.
3. **Limpieza** (`limpiar`): corrige tipos, textos y monedas; marca con banderas `sin_cliente` y `Valores_negativos` en lugar de borrar registros.
4. **Transformación** (`transformar`): cruza con `productos.csv` y `regiones.csv` (validando llaves `many_to_one`) y crea `mes`, `dia`, `rango` (bajo / medio / alto por cuartiles) y `es_fallido`.
5. **Análisis y gráficos**: Grafico de histograma indicando la distribucion de los montos, grafico de columnas indicando el monto pagado por region , grafico de barras indicando  la tasa de pagos fallidos por Segmento de Riesgo.
