#!/usr/bin/python3
import mysql.connector
import tasca

class Persistencia_tasca_mysql():
    def __init__(self):
        self._host="localhost"
        self._user="app"
        self._password="1234"
        self._database="todo_list"
        self._conn = mysql.connector.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database
            )
        if not self.existeixen_taules():
            self.reset_database()

    def desa(self, tasca):
        
        titol = tasca.titol
        done = tasca.done
        resultat = None
        consulta = "INSERT INTO tasques " \
                    + "(titol, done)" \
                    + f"VALUES('{titol}', {done});"
        cursor = self._conn.cursor(buffered=True)
        try:
            cursor.execute(consulta)
            tasca.id = cursor.lastrowid
            resultat = tasca
        except mysql.connector.errors.IntegrityError:
            print("[X] IntegrityError: possiblement aquesta tasca ja està registrada.")
        self._conn.commit()
        cursor.reset()
        cursor.close()
        return resultat
    
    def get_list(self):
        
        consulta = "SELECT titol, done, id FROM tasques;"
        cursor = self._conn.cursor(buffered=True)
        cursor.execute(consulta)
        llista = cursor.fetchall()
        resultat = []
        for registre in llista:
            tarea = tasca.Tasca(self, registre[0], registre[1], registre[2])
            resultat.append(tarea)
        cursor.reset()
        cursor.close()
        return resultat
    
    def modifica_tasca(self, tasca):
        resultat = None
        
        titol = tasca.titol
        done = tasca.done
        id = tasca.id
        consulta = f"update tasques set done={done}, titol='{titol}' where id={id};"
        cursor = self._conn.cursor(buffered=True)
        try:
            cursor.execute(consulta)
            resultat = tasca
        except mysql.connector.errors.IntegrityError:
            print("[X] IntegrityError: possiblement aquest titol ja existeix.")
        self._conn.commit()
        cursor.reset()
        cursor.close()
        return resultat
    
    def esborra_tasca(self, id):
        
        consulta = f"delete from tasques where id={id};"
        cursor = self._conn.cursor(buffered=True)
        cursor.execute(consulta)
        self._conn.commit()
        cursor.reset()
        cursor.close()

    def existeixen_taules(self):
        consulta = "SELECT * FROM tasques LIMIT 1;"
        cursor = self._conn.cursor(buffered=True)
        try:
            cursor.execute(consulta)
        except mysql.connector.errors.ProgrammingError:
            cursor.reset()
            cursor.close()
            return False
        cursor.close()
        return True

    def reset_database(self):
        cursor = self._conn.cursor(buffered=True)
        consulta = "DROP TABLE if exists tasques;" 
        cursor.execute(consulta)
        consulta = "CREATE TABLE if not exists tasques(id int not null auto_increment, titol TEXT UNIQUE, done BOOLEAN, primary key(id));"
        cursor.execute(consulta)
        self._conn.commit()
        cursor.reset()
        cursor.close()


def main():
    id = None
    titol = "Fer la bugada"
    persistencia = Persistencia_tasca_mysql()
    una_tasca = tasca.Tasca(persistencia, titol)
    print(persistencia.desa(una_tasca))
    tasques = persistencia.get_list()
    print("--- Lista de tasques: ---")
    for taska in tasques:
        print(taska)
        if taska.titol == titol:
            id = taska.id
            taska.titol = "Refer la bugada"
            taska.done = True
            persistencia.modifica_tasca(taska)
            print("--- Taska modificada ---")
    tasques = persistencia.get_list()
    print("\n\n--- Lista de tasques: ---")
    for taska in tasques:
        print(taska)
    if id:
        persistencia.esborra_tasca(id)
        print("--- Taska esborrada ---")

if __name__=="__main__":
    main()