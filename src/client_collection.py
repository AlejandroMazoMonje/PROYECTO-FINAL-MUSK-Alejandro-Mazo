class ClientCollection:
    def __init__(self,clients): # clients es una lista  de objetos tipo Client
        self.clients = clients

    def get_client_by_id(self,id):
        # buscamos en la lista el cliente con ese id y devolvemos el cliente completo
        for c in self.clients:
            if c.client_id == id:
                return c
        return None
    
    def clients_by_country(self,country):
        encontrados = []
        for c in self.clients:
            if c.country == country:
                encontrados.append(c)
        return encontrados
    
    