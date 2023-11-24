from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receiveStakingInfo', methods=['POST'])
def receiveStakingInfo():
    try:
        data = request.get_json()
        received_text = data['text']
        print(f"Received text from frontend: {received_text}")
        # Process the received text as needed
        # ...
        print(received_text)
        return jsonify({'message': 'Text received successfully'}), 200
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
