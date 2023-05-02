#!/usr/bin/python3

import flask
import app_tasques
import tasca, usuari
import json

app = flask.Flask(__name__)
core_app = app_tasques.App_tasques()
@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    resultat = core_app.esborra_tasca(id)
    return "", 204

@app.route("/tasks", methods=["POST", "GET", "PUT"])
def tasks():
    if flask.request.method == "POST":
        info_body = flask.request.get_data()    #info_body = '{"title": "hola"}' -> str
        tasca_nova = json.loads(info_body)      #tasca_nova = {"title": "hola"}  -> dictionary
        objecte_tasca = tasca.Tasca(None, tasca_nova["title"]) # Object.Tasca -> tasca.Tasca
        resultat = core_app.afegeix_tasca(objecte_tasca)
        return "", 201
    elif flask.request.method == "PUT":
        info_body = flask.request.get_data()    #info_body = '{"title": "hola"}' -> str
        tasca_nova = json.loads(info_body)      #tasca_nova = {"title": "hola"}  -> dictionary
        objecte_tasca = tasca.Tasca(
            None, tasca_nova["title"], 
            tasca_nova["done"], 
            tasca_nova["id"]
            ) # Object.Tasca -> tasca.Tasca
        resultat = core_app.modifica_tasca(objecte_tasca)
        return "", 204
    elif flask.request.method == "GET":
        llista_jsons = []
        llista_tasques = core_app.llegir_tasques()
        for t in llista_tasques:
            tasca_json = str(t)                          # tasca_json -> str
            tasca_diccionary = json.loads(tasca_json)    # tasca_diccionary -> dictionary
            llista_jsons.append(tasca_diccionary)   # array de dictionaries
        return flask.jsonify(llista_jsons), 200     # retorna json + Content-type: application/json

@app.route('/registre', methods=['POST'])
def registre():
    info_body = flask.request.get_data()    
    usuari_nou = json.loads(info_body)      
    objecte_usuari = usuari.Usuari(
        None, usuari_nou["nom"], 
        usuari_nou["nick"], 
        usuari_nou["password"]
        ) 
    resultat = core_app.registre(objecte_usuari)
    if resultat:
        return "", 201
    return "", 400

@app.route('/login', methods=['POST'])
def login():
    info_body = flask.request.get_data()    
    usuari_nou = json.loads(info_body)      
    objecte_usuari = usuari.Usuari(
        None, None, 
        usuari_nou["nick"], 
        usuari_nou["password"]
        ) 
    resultat = core_app.login(objecte_usuari.nick, objecte_usuari.password)
    if resultat:
        return flask.jsonify({"api_key": resultat}), 201
    return "", 403
    

app.run(
    host="0.0.0.0",
    debug=False)