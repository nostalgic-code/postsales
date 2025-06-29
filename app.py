from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Static API credentials
USERNAME = 'd5900938-be95-4412-95b3-50b11983e13e'
PASSWORD = '90fa0de5-250a-4e99-bd65-85b1854d9c82'

# External API endpoint
EXTERNAL_API_URL = 'http://102.33.60.228:8769/getResources/postSalesOrderV2'

@app.route('/send-order', methods=['POST'])
def send_order():
    try:
        # Get orderData from PHP frontend
        client_payload = request.get_json()

        if not client_payload or 'orderData' not in client_payload:
            return jsonify({'error': 'Missing orderData in request'}), 400

        # Inject required credentials
        full_payload = {
            'username': USERNAME,
            'password': PASSWORD,
            'orderData': client_payload['orderData']
        }

        # Forward to external API
        headers = {'Content-Type': 'application/json'}
        response = requests.post(EXTERNAL_API_URL, json=full_payload, headers=headers)

        try:
            api_response = response.json()
        except ValueError:
            api_response = {'raw_response': response.text}

        return jsonify({
            'status': response.status_code,
            'api_response': api_response
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
