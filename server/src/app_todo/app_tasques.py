#!/usr/bin/python3
import persistencia_tasca_sqlite
import persistencia_tasca_mysql
import persistencia_usuari_mysql
import usuari
import json

RUTA_BD = "todo_list.db"

class App_tasques():
    def __init__(self):
        config = self.llegeix_configuracio()
        try:
            self._database = config["database"]
        except:
            self._database = None
        print(f"Base de dades: {self._database}")
        if self._database == "sqlite":
            self._persistencia_tasques = persistencia_tasca_sqlite.Persistencia_tasca_sqlite(RUTA_BD)
            self._persistencia_usuaris = None
            raise NotImplementedError("Falta implementar la persistencia usuari per aquest SGBD.")
        elif self._database =="mysql":
            self._persistencia_tasques = persistencia_tasca_mysql.Persistencia_tasca_mysql()
            self._persistencia_usuaris = persistencia_usuari_mysql.Persistencia_usuari_mysql()
        else:
            raise Exception("Base de dades no reconeguda!!!")
    
    def registre(self, user):
        nou_usuari = usuari.Usuari(self._persistencia_usuaris, user.nom, user.nick, user.password)
        resultat = nou_usuari.desa()
        return resultat
    
    def llegeix_configuracio(self):
        ruta_config = "./config.json"
        resultat = {}
        try:
            with open(ruta_config) as f:
                resultat = json.load(f)
        except BaseException as ex:
            print("[🤬] No he trobat el fitxer de configuracio")
        return resultat

    def afegeix_tasca(self, tasca_nova):
        tasca_nova.persistencia = self._persistencia_tasques
        tasca_nova.desa()

    def llegir_tasques(self):
        return self._persistencia_tasques.get_list()
    
    def modifica_tasca(self, tasca):
        return self._persistencia_tasques.modifica_tasca(tasca)
    
    def esborra_tasca(self, id):
        return self._persistencia_tasques.esborra_tasca(id)