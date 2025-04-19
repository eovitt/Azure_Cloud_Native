from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/store-data', methods=['POST'])
def store_data():
    data = request.json
    # Simulação de armazenamento de dados na nuvem
    response = {
        "message": "Dados armazenados com sucesso na nuvem!",
        "data": data
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)