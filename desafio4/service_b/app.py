import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# URL do serviço A (passada via docker-compose ou usa valor padrão)
SERVICE_A_URL = os.environ.get(
    'SERVICE_A_URL',
    'http://service-a:5000/api/usuarios'
)

@app.route('/api/info-usuarios', methods=['GET'])
def consumir_servico_a():
    """Consulta o Serviço A e combina as informações dos usuários."""
    try:
        resposta = requests.get(SERVICE_A_URL, timeout=5)
        resposta.raise_for_status()

        dados = resposta.json().get("usuarios", [])

        mensagens = []
        for usuario in dados:
            nome = usuario.get("nome")
            status = usuario.get("status")
            desde = usuario.get("desde")

            frase = f"Usuário {nome} está {status} desde {desde}."
            mensagens.append(frase)

        return jsonify({
            "status": "ok",
            "fonte": SERVICE_A_URL,
            "mensagens_combinadas": mensagens
        })

    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": "erro",
            "mensagem": "Não foi possível conectar ao Serviço A."
        }), 503

    except Exception as e:
        return jsonify({
            "status": "erro",
            "mensagem": str(e)
        }), 500


if __name__ == '__main__':
    # Porta diferente da do serviço A
    app.run(host='0.0.0.0', port=5001)
