class SalesCollection: 
    def __init__(self,sales): # sales es una lista de objetos tipo Sale
        self.sales = sales

    def sales_by_client(self, client_id):
        # buscamos en la lista de las ventas las que son del cliente con ese id 
        # y devolvemos la lista de todas sus compras
        ventas = []
        for s in self.sales:
            if s.client_id == client_id:
                ventas.append(s)
        return ventas
    
    def total_amount_by_client(self, client_id):
        # recorrer todas las ventas y si son de ese id de cliente ir sumando sus valores y devolver el resultado
        total = 0.0
        for s in self.sales:
            if s.client_id == client_id:
                total += s.amount
        return total

    def total_amount_by_category(self, category):
        total = 0.0
        for s in self.sales:
            if s.category == category:
                total += s.amount
        return total
    
    def average_sale_by_client(self, client_id):
        # calcular media de las ventas de un cliente
        total = 0.0
        numero_de_ventas = 0
        for s in self.sales:
            if s.client_id == client_id:
                total += s.amount
                numero_de_ventas += 1
        if numero_de_ventas==0: # por si no hay ventas de ese cliente
            return 0
        return total / numero_de_ventas        
