from .client import Client
from .sale import Sale
from .client_collection import ClientCollection
from .sales_collection import SalesCollection
from pathlib import Path
import json
import pandas as pd
from .functional_utils import filter_sales_by_category


def generate_report():
    with open(Path(__file__).resolve().parent.parent / "data" / "clients.json", "r", encoding="utf-8") as clientes:
        datos_clientes_json = json.load(clientes)

    lista_objetos_tipo_client = []
    for d in datos_clientes_json: 
        lista_objetos_tipo_client.append(Client(d['client_id'],d['name'],d['country'],d['signup_date']))
    lista_clientes = ClientCollection(lista_objetos_tipo_client)


    df_ventas = pd.read_csv(Path(__file__).resolve().parent.parent / "data" / "sales.csv")

    lista_objetos_tipo_sale = []
    for i in range(len(df_ventas)):
        venta = Sale(df_ventas.iloc[i]["sale_id"], df_ventas.iloc[i]["client_id"],df_ventas.iloc[i]["product"],df_ventas.iloc[i]["category"],df_ventas.iloc[i]["amount"],df_ventas.iloc[i]["date"])
        lista_objetos_tipo_sale.append(venta)
    lista_ventas = SalesCollection(lista_objetos_tipo_sale)
    print("VENTAS CREADAS:", len(lista_ventas.sales))

    # ------------------------------
    # 1) TOTAL CLIENTES 
    # ------------------------------
    print("1 total clientes")
    total_clientes = len(datos_clientes_json)
    print("\t", total_clientes) # 3

    # ------------------------------
    # 2) TOTAL VENTAS  
    # ------------------------------
    print("2 total ventas")
    total_numero_ventas = len(df_ventas)
    print("\t", total_numero_ventas) # 7

    # ------------------------------
    # 3) TOTAL DE INGRESOS POR CLIENTE
    # ------------------------------
    print("3 total ventas por cliente usando el dataframe")
    print(df_ventas.groupby("client_id")["amount"].sum())
    print("3 total ventas por cliente recorriendo clientes y usando total_amount_by_client de lista_ventas")
    for c in lista_clientes.clients:
        print(lista_ventas.total_amount_by_client(c.client_id))

    # ------------------------------
    # 4) NÚMERO DE VENTAS POR CLIENTE 
    # ------------------------------
    print("4 numero de ventas por cliente usando el dataframe")
    print(f"\t1: {len(df_ventas[df_ventas['client_id'] == 1])}") # 3
    print(f"\t2: {len(df_ventas[df_ventas['client_id'] == 2])}") # 2
    print(f"\t3: {len(df_ventas[df_ventas['client_id'] == 3])}") # 3
    print("4 numero de ventas por cliente usando el dataframe y el count")
    # usando el df y count, obtengo un dataframe
    print(df_ventas.groupby('client_id')['client_id'].count())

    print("4 numero de ventas por cliente, usando el metodo sales_by_client de ClientCollection, lo que se pide")
    for c in lista_clientes.clients:
        print(f"\t{c.client_id}: {len(lista_ventas.sales_by_client(c.client_id))}") 

    # ------------------------------
    # 5) PROMEDIO DE GASTO POR CLIENTE
    # ------------------------------
    print("5 media de gasto por cliente")
    print(df_ventas.groupby("client_id")["amount"].mean())
    print("5 media de gasto por cliente usando el metodo del ClientCollection")
    for c in lista_clientes.clients:
        print(f"\t{c.client_id}: {lista_ventas.average_sale_by_client(c.client_id)}") 

    # ------------------------------
    # 6) CLIENTE CON MAYOR GASTO POR PAÍS
    # ------------------------------
    countries = []  
    print("decir el nombre del cliente que mas ha gastado en cada pais")

    for c in lista_clientes.clients:
        if c.country in countries:
            pass
        else:
            countries.append (c.country)

    cliente_con_mayor_venta_en_cada_pais = dict()
    for country in countries:
        clientes = lista_clientes.clients_by_country(country)

        max_venta = 0
        nombre_max = ""
        for c in clientes:
            euros = lista_ventas.total_amount_by_client(c.client_id) 
            if euros > max_venta:
                max_venta = euros
                nombre_max = c.name
            print(c.name, c.country, euros)    
        cliente_con_mayor_venta_en_cada_pais[country] = nombre_max
        print(cliente_con_mayor_venta_en_cada_pais)

    # ------------------------------
    # 7) TOTAL DE VENTAS POR CATEGORÍA
    # ------------------------------
    print("EJERCICIO 7") 

    total_por_categoria = dict()
    for v in lista_ventas.sales:
        if v.category in total_por_categoria: # esta categoria ya estaba en el diccionario, en sus claves
            total_por_categoria[v.category] += float(v.amount)
        else: # es la primera vez que me encuentro con esta categoria
            total_por_categoria[v.category] = float(v.amount)
    print(total_por_categoria)
    print(df_ventas.groupby("category")["amount"].sum())

    # ------------------------------
    # 8) CLIENTE CON MÁS VENTAS EN UNA CATEGORÍA 
    # ------------------------------
    print("EJERCICIO 8") 

    ventas_electronica = filter_sales_by_category(lista_ventas.sales, "Electronics")

    cantidad_ventas_por_id = dict()
    for v in ventas_electronica:
        if v.client_id in cantidad_ventas_por_id: 
            cantidad_ventas_por_id[int(v.client_id)] += 1
        else: 
            cantidad_ventas_por_id[int(v.client_id)] = 1

    max_numero_ventas = 0
    clientes_con_mas_ventas = []

    for client_id, numero_ventas in cantidad_ventas_por_id.items():
        if numero_ventas > max_numero_ventas:
            max_numero_ventas = numero_ventas
            clientes_con_mas_ventas = []
            cliente = lista_clientes.get_client_by_id(client_id)
            clientes_con_mas_ventas.append(cliente.name)
        elif numero_ventas == max_numero_ventas:
            cliente = lista_clientes.get_client_by_id(client_id)
            clientes_con_mas_ventas.append(cliente.name)

    print(clientes_con_mas_ventas)      

    # ------------------------------
    # 9) CLIENTES DE ALTO GASTO (>500)
    # ------------------------------
    print("EJERCICIO 9")  

    high_spending_clients = []
    for c in lista_clientes.clients:
        total = lista_ventas.total_amount_by_client(c.client_id)
        if total > 500:
            print(c.client_id, c.name, total)
            high_spending_clients.append(c.name)

    # ------------------------------
    # 10) VENTAS POR MES
    # ------------------------------
    print("EJERCICIO 10")  

    df_ventas["date"] = pd.to_datetime(df_ventas["date"])
    df_ventas["year_month"] = df_ventas["date"].dt.to_period("M")
    sumas = df_ventas.groupby("year_month")["amount"].sum()
    monthly_sales = {}
    for mes, total in sumas.items():
        monthly_sales[str(mes)] = float(total)
    print(monthly_sales)

    # ------------------------------
    # 11) INFORME FINAL JSON
    # ------------------------------
    print("EJERCICIO 11")  

    informe = {}

    suma_total_ventas = float(df_ventas["amount"].sum())
    informe["summary"] = {
        "total_clients": total_clientes,
        "total_sales": total_numero_ventas,
        "total_revenue": suma_total_ventas
    }

    clientes = []
    for c in lista_clientes.clients:
        total = lista_ventas.total_amount_by_client(c.client_id)
        numero_ventas = len(lista_ventas.sales_by_client(c.client_id))
        promedio = lista_ventas.average_sale_by_client(c.client_id)
        cliente = {
            "client_id": c.client_id,
            "name": c.name,
            "total_spent": float(total),
            "sale_count": numero_ventas,
            "average_sale": round(float(promedio), 2)
        }
        clientes.append(cliente)
    informe["clients"] = clientes

    informe["top_client_by_country"] = cliente_con_mayor_venta_en_cada_pais

    informe["sales_by_category"] = total_por_categoria

    informe["high_spending_clients"] = high_spending_clients

    informe["monthly_sales"] = monthly_sales

    with open("informe.json", "w", encoding="utf-8") as f:

        json.dump(
            informe,
            f,
            indent=4,
            ensure_ascii=False
        )
    return informe
