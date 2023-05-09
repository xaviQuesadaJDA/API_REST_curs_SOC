#!/usr/bin/python3

"""
radar_de_tram.py: Implementa una API REST que calcula si un cotxe ha de ser
multat a un radar de tram.
Rep com a paràmetres:
  · Distància [m]
  · Temps [s]
  · Velocitat màxima permesa al tram [Km/h]

  Els paràmetres es reben per URL de la següent forma:
  '/es-sancionable/distancia/<d>/temps/<t>/v-max/<vm>'

  I retorna el resultat en format JSON: 
  {
  "velocitat_maxima": 120,
  "velocitat_real": 123,
  "sancionable": "Marge de seguretat" 
  }

  El missatge de sancionable correspondrà a:
  - No sancionable: si la velocitat real no supera a la velocitat màxima permesa
  - Marge de seguretat: si la velocitat real supera a la velocitat màxima, però no supera
  en més d'un 10%.
  - Sancionable: si la velocitat real supera a la velocitat màxima en més del 10%
"""

import flask

app = flask.Flask(__name__)

@app.route('/es-sancionable/distancia/<d>/temps/<t>/v-max/<vm>', methods=['GET'])
def es_sancionable(d, t, vm):
    distancia = int(d)
    temps = int(t)
    v_max = int(vm)

    velocitat_real = (distancia / 1000) / (temps / (60 * 60))
    missatge = None
    if velocitat_real <= v_max:
        missatge = "No sancionable"
    elif velocitat_real <= v_max * 1.1:
        missatge = "Marge de seguretat"
    else:
        missatge = "Sancionable"
    
    return flask.jsonify({
        "velocitat_maxima": v_max,
        "velocitat_real": velocitat_real,
        "sancionable": missatge 
    })

if __name__ == "__main__":
    app.run()