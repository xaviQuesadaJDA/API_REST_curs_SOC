import book

class App_llibres():
    
    def __init__(self):
        self._llista = []
        self._nova_id = 0
    

    def get_llibres(self):
        return self._llista
    
    def afegir_llibre(self, llibre):
        self._nova_id = self._nova_id + 1
        llibre.id = self._nova_id
        self._llista.append(llibre)
        return llibre
    
    def consulta_llibre(self, id):
        for llibre in self._llista:
            if llibre.id == id:
                return llibre
        return None 
    
def main():
    un_llibre = book.Book("hola mon!", "Xavi", "Novel.la negra", 2023)
    altre_llibre = book.Book("A10 mon!", "Daniel Llull", "Sci-Fi", 1998)

    app = App_llibres()
    app.afegir_llibre(un_llibre)
    app.afegir_llibre(altre_llibre)

    llibres = app.get_llibres()
    for llibre in llibres:
        print(llibre)

if __name__ == "__main__":
    main()