from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    
    return jsonify({'status': 'healthy',}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
