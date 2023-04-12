import flask
import app_llibres
import book
import json


app = flask.Flask(__name__)
la_meva_app_llibres = app_llibres.App_llibres()

@app.route("/")
def hola():
    return "Hola, benvingut a la meva API de llibres."

@app.route("/books", methods=["GET", "POST"])
def books():
    if flask.request.method == "GET":
        return get_books()
    elif flask.request.method == "POST":
        return post_books()
        
    
def get_books():
    llista_llibres = la_meva_app_llibres.get_llibres()
    llista_diccionari = []
    for llibre in llista_llibres:
        dic_llibre = json.loads(str(llibre))
        llista_diccionari.append(dic_llibre)
    return flask.jsonify(llista_diccionari)

def post_books():
    cos = flask.request.get_data()
    diccionari_llibre = json.loads(cos)
    llibre = book.Book(
        diccionari_llibre["title"],
        diccionari_llibre["author"],
        diccionari_llibre["genre"],
        diccionari_llibre["year"])
    la_meva_app_llibres.afegir_llibre(llibre)
    str_llibre = str(llibre)
    dic_llibre = json.loads(str_llibre)
    return flask.jsonify(dic_llibre), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0")