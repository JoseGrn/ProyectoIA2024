from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'key': 'value'}
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        return jsonify({"you sent": data}), 201
    else:
        return jsonify({"error": "Request must be JSON"}), 415

if __name__ == '__main__':
    app.run(debug=True)
