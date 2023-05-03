#!/usr/bin/python3
import uuid
import persistencia_tasca_sqlite
import persistencia_tasca_mysql
import persistencia_usuari_mysql
import usuari
import json, bcrypt

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
        # TODO prohibir l'accés a usuaris no identificats
        tasca_nova.persistencia = self._persistencia_tasques
        tasca_nova.desa()

    def llegir_tasques(self):
        return self._persistencia_tasques.get_list()
    
    def modifica_tasca(self, tasca):
        # TODO prohibir l'accés a usuaris no identificats
        return self._persistencia_tasques.modifica_tasca(tasca)
    
    def esborra_tasca(self, id):
        # TODO prohibir l'accés a usuaris no identificats
        return self._persistencia_tasques.esborra_tasca(id)
    
    def login(self, nick, password):
        usuari_passat_pel_client = usuari.Usuari(self._persistencia_usuaris, None, nick, password)
        usuari_de_base_dades = usuari_passat_pel_client.llegeix_amb_nick()
        if not usuari_de_base_dades:
            return None
        comparacio = bcrypt.checkpw(
            password.encode('utf-8'), 
            usuari_de_base_dades.password.encode('utf-8'))
        if comparacio:
            api_key = uuid.uuid4()
            usuari_de_base_dades.desa_api_key(api_key)
            return api_key
        return None
    
    def llegeix_usuari_amb_api_key(self, x_api_key):
        return self._persistencia_usuaris.llegeix_usuari_amb_api_key(x_api_key)
