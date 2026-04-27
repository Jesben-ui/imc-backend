from imc import calcul_IMC, resultat_IMC
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://imc-frontend-seven.vercel.app"])

# -----------------------
# BASE EN MÉMOIRE (simple)
# -----------------------
data_store = []

# -----------------------
# ROUTE IMC (POST)
# -----------------------
@app.route("/imc", methods=["POST"])
def imc():
    data = request.json

    poids = float(data["poids"])
    taille = float(data["taille"])
    age = int(data.get("age", 0))
    sexe = data.get("sexe", "M")

    imc_value = calcul_IMC(poids, taille)
    cat = resultat_IMC(imc_value)

    record = {
        "poids": poids,
        "taille": taille,
        "age": age,
        "sexe": sexe,
        "imc": round(imc_value, 2),
        "categorie": cat
    }

    data_store.append(record)

    print("record ajouter:",record)

    return jsonify(record)

# -----------------------
# STATS GLOBALES
# -----------------------
@app.route("/stats", methods=["GET"])
def stats():
    if len(data_store) == 0:
        return jsonify({
            "moyenne": 0,
            "mediane": 0,
            "variance": 0,
            "ecart_type":0,
            "max": 0,
            "min": 0,
            "total": 0
        })

    imcs = [d["imc"] for d in data_store]

    moyenne = sum(imcs) / len(imcs)
    variance = sum((x- moyenne)**2 for x in imcs)/ len (imcs)
    ecart_type = variance ** 0.5

    #mediane

    imcs_sorted = sorted(imcs)
    n =len(imcs_sorted)

    if n % 2 == 0:
        mediane = (imcs_sorted[n//2-1] + imcs_sorted[n//2])/2
    else:    
        mediane = imcs_sorted[n//2]

    return jsonify({
        "moyenne": moyenne,
        "mediane": mediane,
        "variance":variance,
        "ecart_type":ecart_type,
        "max": max(imcs),
        "min": min(imcs),
        "total": len(imcs)
    })

# -----------------------
# TOUTES LES DONNÉES (GRAPHIQUES)
# -----------------------
@app.route("/all", methods=["GET"])
def all_data():
    return jsonify(data_store)

# -----------------------
# HOME TEST
# -----------------------
@app.route("/")
def home():
    return "API IMC OK "

# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
