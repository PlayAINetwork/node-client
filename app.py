from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    
    return jsonify({'status': 'healthy',}), 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
