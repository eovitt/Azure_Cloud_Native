from flask import Flask, request, jsonify
from validador import validar_linha_digitavel

app = Flask(__name__)

@app.route('/validar-boleto', methods=['POST'])
def validar_boleto():
    data = request.get_json()
    linha_digitavel = data.get('linha_digitavel')

    if not linha_digitavel:
        return jsonify({'erro': 'Campo linha_digitavel é obrigatório'}), 400

    resultado = validar_linha_digitavel(linha_digitavel)

    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
