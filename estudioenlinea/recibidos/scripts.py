import pandas as pd
from datetime import datetime
from .models import ComprobantesRecibidos, Contribuyente
def extrae(path):
    data = pd.read_excel(path)
    data.columns = data.iloc[0]
    data =data.drop(0)
    data=data.fillna(0)
    data["Neto_pesos"] = data["Imp. Neto Gravado"]*data["Tipo Cambio"]
    data["Iva_pesos"] = data["IVA"]*data["Tipo Cambio"]
    data["Total_pesos"] = data["Imp. Total"]*data["Tipo Cambio"]
    data["alicuota"] = data["Iva_pesos"]/data["Neto_pesos"]
    data["alicuota"] = (data["alicuota"]*100).round(2)
    data.loc[(data.alicuota>21,'alicuota')]=21
    data.loc[(data.alicuota==20.99,'alicuota')]=21
    #data.loc[(data["alicuota"]<21)&(data["alicuota"]>10.5),"alicuota"]
    data = data.dropna()

    #reemplazar espacion es nombre de columnas
    columnas = []
    for columna in data.columns:
        try:
            columna = columna.replace(" ","_")
            columnas.append(columna)
        except:
            pass
    data.columns = columnas
    return data   

def mis_comprobantes_recibidos(tabla,contribuyente):
    formato_fecha = "%d/%m/%Y"
    formato_fecha_req = "%Y-%m-%d"
    lista = []
    for renglon in tabla:
        #comprobar si la factura no está en la base de datos
        if not ComprobantesRecibidos.objects.filter(Cuit=renglon['Nro._Doc._Emisor']).filter(Punto_de_Venta=renglon['Punto_de_Venta']).filter(Numero_Desde=renglon['Número_Desde']).exists():        
            d = ComprobantesRecibidos()
            d.Contribuyente =Contribuyente.objects.get(id = contribuyente)
            fecha_comp = datetime.strptime(renglon['Fecha'],formato_fecha)
            fecha_comp = datetime.strftime(fecha_comp, formato_fecha_req)
            d.Fecha=fecha_comp
            d.Tipo=renglon['Tipo']
            d.Punto_de_Venta=renglon['Punto_de_Venta']
            d.Numero_Desde=renglon['Número_Desde']
            d.Cuit=renglon['Nro._Doc._Emisor']
            d.Denominacion_Emisor=renglon['Denominación_Emisor']
            d.Tipo_Cambio=renglon['Tipo_Cambio']
            d.Moneda=renglon['Moneda']
            d.Imp_Neto_Gravado=renglon['Imp._Neto_Gravado']
            d.Imp_Neto_No_Gravado=renglon['Imp._Neto_No_Gravado']
            d.Imp_Op_Exentas=renglon['Imp._Op._Exentas']
            d.IVA=renglon['IVA']
            d.Imp_Total=renglon['Imp._Total']
            d.Neto_pesos=renglon['Neto_pesos']
            d.Iva_pesos=renglon['Iva_pesos']
            d.Total_pesos=renglon['Total_pesos']
            d.Alicuota=renglon['alicuota']
            lista.append(d)
    return lista

