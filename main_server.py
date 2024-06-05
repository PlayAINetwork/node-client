from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/task/<id>', methods=['GET'])
def get_task(id):
    s3_url ="https://87e044e966512f7b11387ff032db8cf3.r2.cloudflarestorage.com/playai/test.mp4"
    return jsonify({'s3_url': s3_url})

@app.route('/confirm', methods=['POST'])
def confirm_task():
    data = request.get_json()
    print(data)
    return jsonify({'task':"confrimed"})

if __name__ == '__main__':
   port = int(os.getenv('PORT', 4000))
   app.run(host='0.0.0.0', port=port)
