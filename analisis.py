import pandas as pd
import numpy as np


def transformar(df,productos, regiones):
   

    filas_antes = len(df)
      
    # productos.csv también trae currency: se quita para no tener currency_x y currency_y.
    productos = productos.drop(columns="currency")
    df = df.merge(productos, on="product_id", how="left")
    df = df.merge(regiones, on="region_id", how="left")
    # Comprobación: el merge no puede cambiar el número de filas.
    assert len(df) == filas_antes, "El merge cambió el número de filas"
    df["region_name"] = df["region_name"].fillna("Sin cliente")
    
    
    # Fechas. Todos los pagos son de febrero de 2024: el mes no separa nada,
    # pero la consigna lo pide.
    df["mes"] = df["pay_dt"].dt.month
    df["dia_semana"] = df["pay_dt"].dt.day_name()
    
    
    # Rangos de monto (solo para los montos normales, que van de 9.99 a 48.99).
    df["rango_monto"] = pd.cut(df["payment_amount"], bins=[0, 20, 35, 50],
                               labels=["bajo", "medio", "alto"])

    # Fallos. Se separan porque no cuestan lo mismo:
    # failed = no se cobró; chargeback = se cobró y el cliente lo reclamó.
    df["es_failed"] = df["payment_status"] == "failed"
    df["es_chargeback"] = df["payment_status"] == "chargeback"
    df["es_fallido"] = df["es_failed"] | df["es_chargeback"]
    return df

 


def tasas_por_region(df):
    """Pregunta 1: ¿qué región tiene la mayor tasa de pagos fallidos y de contracargos?

    Recibe: los pagos transformados.
    Devuelve: por región, cuántos pagos hay y el % de failed, de chargeback y de los dos juntos.
    """
    tabla = df.groupby("region_name").agg(
        pagos=("payment_id", "count"),
        tasa_failed=("es_failed", "mean"),
        tasa_chargeback=("es_chargeback", "mean"),
        tasa_fallido=("es_fallido", "mean"),
    )
    # La media de True/False es la proporción. Primero se multiplica por 100 y al final se redondea.
    tabla[["tasa_failed", "tasa_chargeback", "tasa_fallido"]] = tabla[["tasa_failed", "tasa_chargeback", "tasa_fallido"]] * 100
    return tabla.round(2).sort_values("tasa_failed", ascending=False)
# Respuesta 1: Caribe tiene la mayor tasa de failed (11.06 %) y Europa la mayor de
# contracargos (3.78 %). Sumadas, Europa (14.80 %) y Caribe (14.71 %) casi empatan;
# Andina tiene 0 contracargos y queda en 10.09 %. Los 6 086 pagos sin cliente están
# todos pagados: si se borraran, la tasa global subiría de 12.27 % a 13.07 %.

def dinero_por_producto_y_metodo(df, con_50000=False):
    """Pregunta 2: ¿qué tipo de producto y qué método de pago mueven más dinero?

    Recibe: los pagos transformados y si se cuentan o no los montos de 50 000.
    Devuelve: una tabla de US$ cobrados con los productos en las filas, los métodos
    en las columnas y los totales (margins=True).
    """
    # Solo cuenta como cobrado lo que está "paid":
    # pending todavía no entra, failed nunca entró y chargeback se devolvió.
    cobrados = df[df["payment_status"] == "paid"]
    # Los -25 nunca se suman. Los 50 000 solo si se pide.
    if con_50000:
        cobrados = cobrados[cobrados["alerta_monto"] != "negativo"]
    else:
        cobrados = cobrados[cobrados["alerta_monto"] == "normal"]

    tabla = pd.pivot_table(cobrados, values="payment_amount", index="product_type",
                           columns="pay_method", aggfunc="sum", margins=True, margins_name="Total")
    return tabla.round(2)
# Respuesta 2 (sin los 50 000): Loan es el producto que más cobra (US$ 690 683)
# y card el método (US$ 741 002). Con los 56 pagos de 50 000 el ganador cambia a
# Card y a transfer (US$ 1 778 180): el primer lugar lo decidía un error de carga.
# Las celdas vacías no son ceros: Card solo se paga por transfer, y Loan y Wallet
# por card o cash.


def tasas_por_riesgo(df):
    """Pregunta 3: ¿los clientes de riesgo alto fallan más que los de riesgo bajo?

    Recibe: los pagos transformados.
    Devuelve: por segmento de riesgo, el % de failed, de chargeback y de los dos juntos.
    """
    tabla = df.groupby("risk_segment").agg(
        tasa_failed=("es_failed", "mean"),
        tasa_chargeback=("es_chargeback", "mean"),
        tasa_fallido=("es_fallido", "mean"),
    )
    tabla = (tabla * 100).round(2)
    return tabla.loc[["Low", "Medium", "High", "Sin cliente"]]   # en orden de riesgo
# Respuesta 3: sí. High falla 18.62 % y Low 9.83 %, casi el doble. Pero el tipo de
# fallo cambia: High concentra los contracargos (12.32 %, el fallo más caro) y
# Medium no tiene ninguno; Medium falla por failed (18.35 %).
