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
                    + f"VALUES('{nom}', '{nick}', '{password_hash.decode()}');"
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
    
    def llegeix_amb_nick(self, nick):
        consulta = f"select id, password_hash, nom from usuaris where nick = '{nick}';"
        cursor = self._conn.cursor(buffered=True)
        nou_usuari = None
        cursor.execute(consulta)
        dades = cursor.fetchone()
        cursor.reset()
        cursor.close()
        if dades:
            nou_usuari = usuari.Usuari(self, dades[2], nick, dades[1], dades[0])
        return nou_usuari

    def calcula_hash(self, password):
        bytes = password.encode('utf-8')
        sal = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, sal)
        return hash

    def existeixen_taules(self):
        consulta_1 = "SELECT * FROM usuaris LIMIT 1;"
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
    nova_persistencia = Persistencia_usuari_mysql()
    #nou_usuari = usuari.Usuari(nova_persistencia, "Adelaida", "Adi", "1234")
    #print(nou_usuari.desa())
    res = nova_persistencia.llegeix_amb_nick('Adi_2')


if __name__=="__main__":
    main()