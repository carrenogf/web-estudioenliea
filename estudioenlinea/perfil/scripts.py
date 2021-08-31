import pandas as pd
import numpy as np
import datetime
from plotly.offline import plot
import plotly.express as px

# ****************** REPORTES CONTADOR *******************

def emitidos_anual(tabla):
    df= pd.DataFrame(tabla)
    df['Fecha']=pd.to_datetime(df['Fecha'])
    df['Año']= df['Fecha'].dt.year
    df['Mes'] = df['Fecha'].dt.month
    df['Mes_año'] = df['Año'].map(str) + '-' +df['Mes'].map(str)
    values = ['Neto_pesos','Iva_pesos','Imp_Neto_No_Gravado','Imp_Op_Exentas']
    df_result = pd.pivot_table(df,index=['Año','Mes','Alicuota'],columns = 'Tipo',values=values,aggfunc=np.sum).fillna(0)
    df_result = df_result[['Neto_pesos','Iva_pesos','Imp_Neto_No_Gravado','Imp_Op_Exentas']]
    for columna in df_result.columns:
        if df_result[columna].sum()==0:
            df_result = df_result.drop([columna],axis=1)
    df_resumen = pd.DataFrame()
    df_resumen['Totales'] = df_result.sum()
 
    df_result= df_result.applymap("{:,.2f}".format)
    df_resumen= df_resumen.applymap("{:,.2f}".format)

    html = df_result.to_html(classes=["table-striped","text-right"], header = "true", justify = "center",table_id="tabla_resumen")
    html = html.replace('id="tabla_resumen"','id="tabla_resumen" cellpadding="3" cellspacing="0"' )
    html2 = df_resumen.to_html(classes=["table-striped","text-right"], header = "true", justify = "center",table_id="tabla_resumen")
    df_graf = df[['Mes_año','Neto_pesos']].groupby('Mes_año').sum()
    fig = px.bar(x=df_graf.index, y=df_graf['Neto_pesos'],title="Comprobantes emitidos por mes", 
                    labels={'y':'Neto en pesos','x':'Fecha'},text=df_graf.index)
    grafico = plot(fig ,output_type='div')
    return html, html2, grafico

def recibidos_anual(tabla):
    df= pd.DataFrame(tabla)
    df['Fecha']=pd.to_datetime(df['Fecha'])
    df['Año']= df['Fecha'].dt.year
    df['Mes'] = df['Fecha'].dt.month
    df['Mes_año'] = df['Año'].map(str) + '-' +df['Mes'].map(str)
    
    values = ['Neto_pesos','Iva_pesos','Imp_Neto_No_Gravado','Imp_Op_Exentas']
    df_result = pd.pivot_table(df,index=['Año','Mes','Alicuota'],columns = 'Tipo',values=values,aggfunc=np.sum).fillna(0)
    df_result = df_result[['Neto_pesos','Iva_pesos','Imp_Neto_No_Gravado','Imp_Op_Exentas']]
    for columna in df_result.columns:
        if df_result[columna].sum()==0:
            df_result = df_result.drop([columna],axis=1)
            
    df_resumen = pd.DataFrame()
    df_resumen['Totales'] = df_result.sum()
    
    df_result= df_result.applymap("{:,.2f}".format)
    df_resumen= df_resumen.applymap("{:,.2f}".format)

    html = df_result.to_html(classes=["table-striped","text-right"], header = "true", justify = "center",table_id="tabla_resumen", border=1)
    html = html.replace('id="tabla_resumen"','id="tabla_resumen" cellpadding="3" cellspacing="0"' )
    html2 = df_resumen.to_html(classes=["table-striped","text-right"], header = "true", justify = "center",table_id="tabla_resumen")
    
    df_graf = df[['Mes_año','Neto_pesos']].groupby('Mes_año').sum()
    fig = px.bar(x=df_graf.index, y=df_graf['Neto_pesos'],title="Comprobantes recibidos por mes", 
                    labels={'y':'Neto en pesos','x':'Fecha'},text=df_graf.index)
    grafico = plot(fig ,output_type='div')

    return html, html2, grafico


    # ****************** REPORTES PERFIL CLIENTE *******************

def ultimos_movimientos(df_emitidos,df_recibidos):
    df_emitidos['Fecha']=pd.to_datetime(df_emitidos['Fecha'])
    df_emitidos['Año']= df_emitidos['Fecha'].dt.year
    df_emitidos['Mes'] = df_emitidos['Fecha'].dt.month
    df_emitidos['Año_Mes'] = df_emitidos['Año'].map(str) + '-' +df_emitidos['Mes'].map(str)

    df_recibidos['Fecha']=pd.to_datetime(df_recibidos['Fecha'])
    df_recibidos['Año']= df_recibidos['Fecha'].dt.year
    df_recibidos['Mes'] = df_recibidos['Fecha'].dt.month
    df_recibidos['Año_Mes'] = df_recibidos['Año'].map(str) + '-' +df_recibidos['Mes'].map(str)

    ultimos_recibidos = df_recibidos['Año_Mes'].unique().tolist()[:6]
    ultimos_emitidos = df_emitidos['Año_Mes'].unique().tolist()[:6]
    ultimos = ultimos_emitidos+ultimos_recibidos
    ultimos_periodos = []
 
    for mes in ultimos:
        if mes not in ultimos_periodos:
             ultimos_periodos.append(mes)

    df_emitidos=df_emitidos[df_emitidos.Año_Mes.isin(ultimos_periodos)]
    df_recibidos=df_recibidos[df_recibidos.Año_Mes.isin(ultimos_periodos)]

    NC_rec = df_recibidos['Tipo'].str.contains("Nota de Crédito",case=False)
    df_recibidos.loc[NC_rec,'Total_pesos']=df_recibidos.loc[NC_rec,'Total_pesos']*(-1)

    NC_emi = df_emitidos['Tipo'].str.contains("Nota de Crédito",case=False)
    df_emitidos.loc[NC_rec,'Total_pesos']=df_emitidos.loc[NC_emi,'Total_pesos']*(-1)

    df_emitidos['Operación'] = "Ventas"
    df = pd.concat([df_emitidos,df_recibidos])
    df['Operación'].fillna('Compras', inplace = True)

    df = pd.pivot_table(df,index='Operación', columns=['Año','Mes'],values='Total_pesos',aggfunc=np.sum).fillna(0)
    df= df.applymap("{:,.2f}".format)   
    meses = df.columns
    lista_meses = []
    for mes in meses:
        print(mes)
        col = str(mes[1])+'-'+str(mes[0])
        lista_meses.append(col)

    df.columns=lista_meses

    return df.to_html(classes=["table table-striped","text-right"])