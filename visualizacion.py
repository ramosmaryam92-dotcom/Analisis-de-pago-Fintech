import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter   # CAMBIO: faltaba importar

from analisis import dinero_por_producto_y_metodo, tasas_por_region, tasas_por_riesgo
       

def formato_usd(x, pos):                      
    return f'US${x:,.0f}'


def Distribucion_montos(df,carpeta):
    #Hisotograma
    montos = df[
        (df['payment_amount'] >= 0) & ((df['payment_amount'] != 50000))
    ]['payment_amount'].dropna()
    
    # Opcional: limpiar también el 1% más extremo restante para una mejor visualización
    limite_superior = montos.quantile(0.99)
    montos_filtrados = montos[montos <= limite_superior]
    

    fig, ax = plt.subplots(figsize=(10, 6))
    # Usamos los datos filtrados
    ax.hist(montos_filtrados, bins=30, color='steelblue', edgecolor='white')

    ax.set_title('Distribución de montos de pago (Sin incluir los 277 registro de 50,000)')
    ax.set_xlabel('Monto del pago (US$)')
    ax.set_ylabel('Cantidad de pagos')
    ax.xaxis.set_major_formatter(FuncFormatter(formato_usd))

    fig.tight_layout()
    fig.savefig(carpeta / 'histograma_montos.png', dpi=150)
    plt.close(fig)
     
def region_pagos(df,carpeta):
    # 1. Datos sin los 50,000 (o filtrando lo que necesites)
    pagos_sin_50k = (df[df['payment_amount'] != 50000]
                 .groupby('region_name')['payment_amount']
                 .sum())
    regiones = pagos_sin_50k.index
    
    # 2. Datos únicamente con los de 50,000 (o el filtro exacto que buscas)
    pagos_solo_50k = (df[df['payment_amount'] == 50000]
                  .groupby('region_name')['payment_amount']
                  .sum()
                  .reindex(regiones, fill_value=0))
    
  
    x = np.arange(len(regiones))  # Las posiciones base en el eje X
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars1 = ax.bar(x - width/2, pagos_sin_50k.values, width, label='Diferentes de 50k', color='steelblue')
    bars2 = ax.bar(x + width/2, pagos_solo_50k.values, width, label='Solo de 50k', color='brown')
    
    #etiqueta de datos
    ax.bar_label(bars1, fmt=lambda val: f"${val:,.0f}", padding=3, fontsize=9)
    ax.bar_label(bars2, fmt=lambda val: f"${val:,.0f}", padding=3, fontsize=9)
    
    ax.set_title('Comparativa de pagos por región')
    ax.set_xlabel('Región', fontsize=11)
    ax.set_ylabel('Monto total (US$)', fontsize=11)
    ax.yaxis.set_major_formatter(FuncFormatter(formato_usd))

# Ponemos los nombres de las regiones en el centro de cada par de barras
    ax.set_xticks(x)
    ax.set_xticklabels(regiones)
    plt.setp(ax.get_xticklabels(), rotation=0, ha='center')   
    
    
    max_val = max(pagos_sin_50k.values.max(), pagos_solo_50k.values.max())
    ax.set_ylim(0, max_val * 1.15)
     
    ax.set_title('Volumen de pago distribuido por regiones - siendo Andina la unica que registra pagos de 50,000')
    ax.set_xlabel('Región',)
    ax.set_ylabel('Monto total (US$)')
    ax.yaxis.set_major_formatter(FuncFormatter(formato_usd))
    plt.setp(ax.get_xticklabels(), rotation=0, ha='right')
     
    ax.legend()

    
    fig.tight_layout()
    fig.savefig(carpeta / 'pagos_por_region.png', dpi=150)
    plt.close(fig)
    
def pagos_fallidos(df,carpeta):    
    df_filtrado = df[df['payment_amount'] != 50000]
    riesgo_2 = pd.crosstab(df_filtrado['risk_segment'], df_filtrado['payment_status'], normalize='index')
    
    # Filtramos únicamente las columnas 'failed' y 'chargeback' por si existen otras
    cols_interes = [col for col in ['failed', 'chargeback'] if col in riesgo_2.columns]
    riesgo_2 = riesgo_2[cols_interes]

    # 2. Creamos la figura y el eje
    fig, ax = plt.subplots(figsize=(10, 5))
    
    y = np.arange(len(riesgo_2.index))
    ancho = 0.35 # Grosor de las barras
    
    # Verificamos si tenemos ambas columnas para graficarlas de forma paralela
    if len(riesgo_2.columns) >= 2:
        col1, col2 = riesgo_2.columns[0], riesgo_2.columns[1]
        
        bars1 = ax.barh(y - ancho/2, riesgo_2[col1], ancho, label=col1, color='steelblue', edgecolor='white')
        bars2 = ax.barh(y + ancho/2, riesgo_2[col2], ancho, label=col2, color='brown', edgecolor='white')
        
        # Agregamos las etiquetas de datos a cada barra
        ax.bar_label(bars1, fmt='%.3f', padding=3, fontsize=9)
        ax.bar_label(bars2, fmt='%.3f', padding=3, fontsize=9)
        
    elif len(riesgo_2.columns) == 1:
        col1 = riesgo_2.columns[0]
        bars1 = ax.barh(y, riesgo_2[col1], ancho, label=col1, color='steelblue', edgecolor='white')
        ax.bar_label(bars1, fmt='%.3f', padding=3, fontsize=9)

    # 3. Configuraciones estéticas y de ejes
    ax.set_yticks(y)
    ax.set_yticklabels(riesgo_2.index)
    ax.set_xlabel('Proporción')
    ax.set_ylabel('Segmento de riesgo del cliente')
    ax.set_title('Tasa de Pagos Fallidos y Chargebacks por Segmento de Riesgo\n'
        'Insight: High concentra chargebacks (fraude por disputa); Medio concentra fallos técnicos.',
        fontsize=10, 
        fontweight='normal'
    )
    
    max_val = riesgo_2.values.max() if not riesgo_2.empty else 1
    ax.set_xlim(0, max_val * 1.15)
    ax.legend(title='Estado de Pago')
    
    fig.tight_layout()
    fig.savefig(carpeta / 'Pagos_fallidos.png', dpi=150)
    plt.close(fig)
    
    print("Todos los graficos se han guardado")


def graficar_todo(df, carpeta):
    """Genera los 5 gráficos en la carpeta indicada."""
    carpeta.mkdir(exist_ok=True)
    Distribucion_montos(df, carpeta)
    region_pagos(df, carpeta)
    pagos_fallidos(df, carpeta)
   



