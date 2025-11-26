from flask import Flask, jsonify

app = Flask(__name__)

PEDIDOS = [
    {"pedido_id": 101, "user_id": 1, "produto": "RTX 5090"},
    {"pedido_id": 102, "user_id": 2, "produto": "Smartphone"},
    {"pedido_id": 103, "user_id": 1, "produto": "Mouse"},
]

@app.route('/api/orders', methods=['GET'])
def listar_pedidos():
    return jsonify({"orders": PEDIDOS})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
