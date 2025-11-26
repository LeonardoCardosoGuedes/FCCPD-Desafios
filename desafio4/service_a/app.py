from flask import Flask, jsonify

app = Flask(__name__)

# Base de usuários simulada
USERS = [
    {"id": 1, "nome": "Lari", "status": "ativo", "desde": "2023-01-15"},
    {"id": 2, "nome": "Joao", "status": "ativo", "desde": "2023-03-20"},
    {"id": 3, "nome": "Maria", "status": "inativo", "desde": "2024-05-10"},
]

@app.route('/api/usuarios', methods=['GET'])
def obter_usuarios():
    """Retorna a lista de usuários como JSON."""
    return jsonify({"usuarios": USERS})

if __name__ == '__main__':
    # Porta padrão: 5000
    app.run(host='0.0.0.0', port=5000)
