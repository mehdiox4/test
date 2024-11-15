from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Initialisation des données des commandes
commandes = [
    {'id_commande': 1, 'status': 'en cours'},
    {'id_commande': 2, 'status': 'prête'},
    {'id_commande': 3, 'status': 'servie'},
]

# Route principale pour afficher l'interface HTML
@app.route('/')
def index():
    return render_template('index.html')

# API pour récupérer toutes les commandes
@app.route('/api/commandes', methods=['GET'])
def get_commandes():
    return jsonify(commandes)

# API pour ajouter une nouvelle commande
@app.route('/api/commandes', methods=['POST'])
def add_commande():
    # On récupère les données envoyées (numéro de commande et statut)
    new_commande = request.json
    if 'id_commande' not in new_commande or 'status' not in new_commande:
        return jsonify({'message': 'ID de commande et statut sont requis'}), 400
    
    # Ajout de la nouvelle commande à la liste
    commandes.append(new_commande)
    return jsonify(new_commande), 201

# API pour mettre à jour le statut d'une commande
@app.route('/api/commandes/<int:id_commande>', methods=['PUT'])
def update_commande(id_commande):
    commande = next((c for c in commandes if c['id_commande'] == id_commande), None)
    if commande:
        statut = request.json.get('status')
        commande['status'] = statut
        return jsonify(commande), 200
    else:
        return jsonify({'message': f'Commande #{id_commande} non trouvée'}), 404

# API pour supprimer une commande par son ID
@app.route('/api/commandes/<int:id_commande>', methods=['DELETE'])
def delete_commande(id_commande):
    global commandes
    commandes = [commande for commande in commandes if commande['id_commande'] != id_commande]
    return jsonify({'message': f'Commande #{id_commande} supprimée'}), 200

if __name__ == '__main__':
    app.run(debug=True)
