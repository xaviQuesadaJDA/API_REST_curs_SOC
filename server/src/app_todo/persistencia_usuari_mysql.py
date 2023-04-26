#!/usr/bin/python3
import mysql.connector
import usuari
import bcrypt

class Persistencia_usuari_mysql():
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

    def desa(self, usuari):
        
        nom = usuari.nom
        nick = usuari.nick
        password_hash = self.calcula_hash(usuari.password)
        resultat = None
        consulta = "INSERT INTO usuaris " \
                    + "(nom, nick, password_hash)" \
                    + f"VALUES('{nom}', '{nick}', '{password_hash}');"
        cursor = self._conn.cursor(buffered=True)
        try:
            cursor.execute(consulta)
            usuari.id = cursor.lastrowid
            resultat = usuari
        except mysql.connector.errors.IntegrityError:
            print("[X] IntegrityError: possiblement aquest usuari ja està registrat.")
        self._conn.commit()
        cursor.reset()
        cursor.close()
        return resultat
    
    def calcula_hash(password):
        bytes = password.encode('utf-8')
        sal = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, sal)
        return hash
    
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
        consulta_1 = "SELECT * FROM usuari LIMIT 1;"
        consulta_2 = "SELECT * FROM sessions LIMIT 1;"
        cursor_1 = self._conn.cursor(buffered=True)
        cursor_2 = self._conn.cursor(buffered=True)
        try:
            cursor_1.execute(consulta_1)
            cursor_2.execute(consulta_2)
        except mysql.connector.errors.ProgrammingError:
            cursor_1.reset()
            cursor_1.close()
            cursor_2.reset()
            cursor_2.close()
            return False
        cursor_1.close()
        cursor_2.close()
        return True

    def reset_database(self):
        cursor = self._conn.cursor(buffered=True)
        consulta = "DROP TABLE if exists sessions;" 
        cursor.execute(consulta)
        consulta = "DROP TABLE if exists usuaris;" 
        cursor.execute(consulta)
        consulta = """
        create table if not exists usuaris(
        id int not null auto_increment,
        nom text not null,
        nick text not null unique,
        password_hash text not null unique,
        primary key (id));
        """
        cursor.execute(consulta)
        consulta = """
        create table if not exists sessions(
        id int not null auto_increment,
        usuari int not null references usuaris(id) on delete cascade,
        api_key text not null unique,
        primary key (id));
        """
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