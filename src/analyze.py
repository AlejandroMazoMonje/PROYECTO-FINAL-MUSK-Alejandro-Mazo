from client import Client
from sale import Sale
from client_collection import ClientCollection
from sales_collection import SalesCollection
from pathlib import Path
import json
import pandas as pd
from functional_utils import filter_sales_by_category
'''
c1 = Client(1,"Juan", "España", "2026/02/25")
print(c1.to_dict())

lista_clientes = ClientCollection([Client(1, "Alice", "Spain", "2022-01-01"),Client(2, "Pepe", "Spain", "2022-01-02")])
print(lista_clientes.get_client_by_id(1).name)

lista_ventas = SalesCollection([Sale("S1", 1, "Laptop", "Electronics", 100, "2023-01-01")])
print(len(lista_ventas.sales_by_client(1))) # 1
print(lista_ventas.total_amount_by_client(1)) # 100

'''

# leer el json y el csv y pasarlos a lista_clientes y lista_ventas

# leer el json de clients.json
# with open("..\data\clients.json","r",encoding = "utf-8") as clientes: antes de corregir.-----------------------------------------------------------------------
def generate_report():
    with open(Path(__file__).resolve().parent.parent / "data" / "clients.json", "r", encoding="utf-8") as clientes:
        datos_clientes_json = json.load(clientes)
# datos_clientes_json contiene una lista de diccionarios, lo que necesitamos para crear lista_clientes es una lista de Client
#print(datos_clientes_json)
    lista_objetos_tipo_client = []
    for d in datos_clientes_json: # cada d es un diccionario, un cliente
        lista_objetos_tipo_client.append(Client(d['client_id'],d['name'],d['country'],d['signup_date']))
    lista_clientes = ClientCollection(lista_objetos_tipo_client)

# leer el csv de sales.csv, obteniendo un dataframe de pandas
    df_ventas = pd.read_csv(Path(__file__).resolve().parent.parent / "data" / "sales.csv")
#print(df_ventas)
# df_ventas es un dataframe
# para lista_ventas necesito una lista de objetos tipo Sale
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
    '''
    Para cada cliente:
    Filtras sus ventas (por client_id)
    Sumas amounts.
    '''
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
    # y recorriendo los clientes que haya
    for c in lista_clientes.clients:
        print(f"\t{c.client_id}: {len(lista_ventas.sales_by_client(c.client_id))}") 



    # ------------------------------
    # 5) PROMEDIO DE GASTO POR CLIENTE
    # ------------------------------
    # usando el df y mean, obtengo un dataframe
    print("5 media de gasto por cliente")
    print(df_ventas.groupby("client_id")["amount"].mean())
    # usando el df y mean, obtengo un dataframe
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
    # countries = {c.country for c in lista_clientes.clients} # otra forma pythonista creando un conjunto ya que no admite repeticiones (como Spain)
    print(countries)

    cliente_con_mayor_venta_en_cada_pais = dict()
    for country in countries:
        clientes = lista_clientes.clients_by_country(country) # lista de Clients de ese country

        max_venta = 0
        nombre_max = ""
        for c in clientes:
            euros = lista_ventas.total_amount_by_client(c.client_id) # calcular la suma de ventas de cada cliente
            if euros > max_venta:
                max_venta = euros
                nombre_max = c.name
            print(c.name, c.country, euros)    
        # averiguar el mayor de los c anteriores, con el nombre me vale
        cliente_con_mayor_venta_en_cada_pais[country] = nombre_max
        print(cliente_con_mayor_venta_en_cada_pais)

    # ------------------------------
    # 7) TOTAL DE VENTAS POR CATEGORÍA
    # ------------------------------
        # expected_categories = {
        #     "Electronics": 699.99 + 1299.50 + 299.99 + 399.99,
        #     "Accessories": 199.99 + 89.99 + 49.99
        # }
    print("EJERCICIO 7") 
    total_por_categoria = dict()
    for v in lista_ventas.sales:
        if v.category in total_por_categoria: # esta categoria ya estaba en el diccionario, en sus claves
            total_por_categoria[v.category] += float(v.amount)
        else: # es la primera vez que me encuentro con esta categoria
            total_por_categoria[v.category] = float(v.amount)
    print(total_por_categoria)

    # con pandas:
    print(df_ventas.groupby("category")["amount"].sum())

    # ------------------------------
    # 8) CLIENTE CON MÁS VENTAS EN UNA CATEGORÍA ---------------------------------------------------------------------------------hay que poner que solo diga los que tienen mas compras de esa categoria 
    # (Electronics)
    # ------------------------------
    # Alice: 2 (Smartphone + ¨Mando)
    # Bob: 1 (Laptop)
    # Carol: 1 (Monitor)

    print("EJERCICIO 8") 

    ventas_electronica = []
    for s in lista_ventas.sales:
        if s.category == "Electronics":
            ventas_electronica.append(s)

    cantidad_ventas_por_id = dict()
    for v in ventas_electronica:
        if v.client_id in cantidad_ventas_por_id: # este cliente ya estaba en el diccionario, en sus claves
            cantidad_ventas_por_id[int(v.client_id)] += 1
        else: # es la primera vez que me encuentro con este cliente
            cantidad_ventas_por_id[int(v.client_id)] = 1

    # por si hay mas de un cliente con el mismo maximo. 

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

    '''
    dice cuantos han comprado todos de esa categoria solo necesitamos el que mas de cada categoria.

    for k,v in cantidad_ventas_por_id.items():
        print(lista_clientes.get_client_by_id(k).name, v)
    '''
    # ------------------------------
    # 9) CLIENTES DE ALTO GASTO (>500)--------------------------------------------------------------------------------leer por si hay que guardar los nombres.
    # ------------------------------

    print("EJERCICIO 9")  

    #Alice y Bob >500   
    #Carol <500 (no mostrar)

    # recorro clientes y con lista_ventas averiguo con total_amount_by_client el total de cada id
    # si es mas de 500 se muestra su nombre o se añade a una lista

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

    # sumar las venta del año-mes indicado, por ejemplo "2023-07"

    # v.date[:7] son los 7 primeros caracteres de la fecha

    '''
    fecha = pd.to_datetime(df_ventas["date"])
    year_mes = fecha.dt.to_period("M")

    print(year_mes)
    '''
    #de_mi_fecha = df_ventas["date"]=="2023-07"
    #grupos = df_ventas.groupby("date").count()
    #print(grupos)
    #print(de_mi_fecha)
    # saber solo las filas del periodo deseado

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
    '''
    informe = dict()

    suma_total_ventas = float(df_ventas["amount"].sum())
    sumario = {"total_clients": total_clientes,
                "total_sales": total_numero_ventas,
                "total_revenue": suma_total_ventas}
    informe["summary"] = sumario

    clientes = [] # lista de diccionarios
    for c in lista_clientes.clients:
        cli = dict()
        cli["client_id"] = c.client_id
        cli["name"] = c.name
        cli["total_spent"] = float(lista_ventas.total_amount_by_client(c.client_id))
        cli["sale_count"] = len(df_ventas[ df_ventas["client_id"]==c.client_id ])
        cli["average_sale"] = float(lista_ventas.average_sale_by_client(c.client_id))
        clientes.append(cli)
    informe["clients"] = clientes


    print(informe)

    with open("informe.json", "w", encoding="utf-8") as f:
        # json.dump(informe, f)
        json.dump(informe, f, indent=4, ensure_ascii=False) # mas bonito
    '''
    '''
    {
    "summary": {
        "total_clients": 7,
        "total_sales": 9,
        "total_revenue": 5000
    },

    "clients": [
        {
        "client_id": 1,
        "name": "Ana",
        "total_spent": 1000,
        "sale_count": 2,
        "average_sale" 500:
        },
        ...
    ],

    "top_client_by_country": {
        "Spain": "Alice",   nombre del cliente que mas ha comprado en este pais
        "Germany": ,
        "France": 
    },

    "sales_by_category": {
        "Electronics": 2700,  en dinero las ventas de esta categoria
        "Accessories": 
    },

    "high_spending_clients": [
        lista de los nopmbres de de los clientes que han gastado mas de 500
    ],

    "monthly_sales": {
        "2023-07": yo pondria todas las fechas
    }
    }

    '''

    informe = {}

    # SUMMARY

    suma_total_ventas = float(df_ventas["amount"].sum())
    informe["summary"] = {
        "total_clients": total_clientes,
        "total_sales": total_numero_ventas,
        "total_revenue": suma_total_ventas
    }

    # CLIENTS
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

    # TOP CLIENT BY COUNTRY

    informe["top_client_by_country"] = cliente_con_mayor_venta_en_cada_pais

    # SALES BY CATEGORY

    informe["sales_by_category"] = total_por_categoria

    # HIGH SPENDING CLIENTS

    informe["high_spending_clients"] = high_spending_clients

    # MONTHLY SALES

    informe["monthly_sales"] = monthly_sales

    # GUARDAR JSON
    with open("informe.json", "w", encoding="utf-8") as f:

        json.dump(
            informe,
            f,
            indent=4,
            ensure_ascii=False
        )
    return informe

generate_report()
