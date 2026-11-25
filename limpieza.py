import pandas as pd
import numpy as np




def cargar(carpeta):
    """Lee los tres CSV del proyecto.

    Recibe: la carpeta donde están los CSV.
    Devuelve: pagos, productos y regiones (tres DataFrames).
    """
  
    pagos = pd.read_csv(carpeta / "pagos_fintech.csv", keep_default_na=False, na_values=[""])
    productos = pd.read_csv(carpeta / "productos.csv")
    regiones = pd.read_csv(carpeta / "regiones.csv")
    return pagos, productos, regiones





def diagnosticar(df):
    """Describe los datos antes de tocarlos.

    Recibe: un DataFrame.
    Devuelve: una tabla con tipo, nulos, % de nulos y valores únicos por columna.
    """
    tabla = pd.DataFrame()
    tabla["tipo"] = df.dtypes
    tabla["nulos"] = df.isna().sum()
    tabla["pct_nulos"] = (df.isna().mean() * 100).round(2)
    tabla["unicos"] = df.nunique()
    print("payment_id repetidos:", df["payment_id"].duplicated().sum())
    return tabla

 


def limpiar(df):
    
 df = df.copy()  #se trabaja sobre una copia
 resumen = {}
 
 #payment_id repetidos. (250)
 repetido=df['payment_id'].duplicated(keep=False)
 regla= df['customer_id']== df['payment_id']+1
 copia_mala= repetido & ~regla
 resumen['copias malas de payment_id (borradas)']= copia_mala.sum()
 df=df[~copia_mala]
 
 
 
 # 2. payment_amount es texto y "12,50" viene con coma: se cambia por punto.
 
 con_coma=df['payment_amount'].str.contains(",")
 resumen['montos con coma(corregidos)']= con_coma.sum()
 df['payment_amount']=df['payment_amount'].str.replace(',','.')
 df['payment_amount']=pd.to_numeric(df['payment_amount'])
 
 #3.montos imposibles: se marcan en la columna alerta_monto.
 #-25 y valores de 50 000. porque el ultimo valor es de 49-> luego pasa a 50,000
 df['alerta_monto']= 'normal'
 df.loc[df['payment_amount'] < 0, 'alerta_monto']='valor_negativo'
 df.loc[df['payment_amount']==50000,'alerta_monto']="50000"
 resumen['montos -25 (marcados)']=(df['alerta_monto']=='valor_negativo').sum()
 resumen['montos de 50 000(marcados)']=(df['alerta_monto']=="50000").sum()
 
 #Corrigiendo el texto en la variable status- "Paidd es paid"
 resumen['Estados paidd -> paid']=(df['payment_status']=="paidd").sum()
 df['payment_status']=df['payment_status'].replace('paidd','paid')
 
 # Cambiando las monedas por USD, en base a que el catalogo de productos se cobra todo en  USD'''
 resumen['Moneda EURO/USDT -> USD']= (df['currency']!= 'USD').sum()
 df['currency'] =df['currency'].replace(['USD', 'USDT', 'EURO'], "USD")


 #Conversion de campo fechas a datetime , dejando las fechas que no existen  como NaT''' 
 
 df['pay_dt']=pd.to_datetime(df['pay_dt'], errors='coerce')
 resumen['pay_dt (fecha vacia)']=df['pay_dt'].isna().sum()
 df['signup_dt']=pd.to_datetime( df['signup_dt'], errors='coerce')
 resumen['signup_dt (fecha vacia)']=df['signup_dt'].isna().sum()
  
 #6,122 registro sin datos de cliente.
 # marco como Sin_Cliente una nueva variable porque no tienen cliente identificado, el customer_id es una mezcla del payment_id + un prefijo. '''
 
 df["sin_cliente"] = df["status_customer"].isna()
 resumen['pagos sin clientes(marcados)']=df['sin_cliente'].isna().sum()
 for columna in ["status_customer", "risk_segment", "kyc_level", "income_bracket"]:
  df[columna] = df[columna].fillna("Sin cliente")
 

 

 return df,resumen


   
