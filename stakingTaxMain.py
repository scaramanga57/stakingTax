from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from mongoPriceDatabase import *
from cryptoPrice import *
import threading
from loggerConfig import setup_logger
import socket
import sys

app = Flask(__name__)
CORS()  # Enable CORS for all routes


logger = setup_logger()

def get_ip_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Connect to an external server (doesn't have to be reachable)
        s.connect(("8.8.8.8", 80))

        # Get the local IP address from the connected socket
        ip_address = s.getsockname()[0]

        # Close the socket
        s.close()
        logger.info( "My IP address is: %s", ip_address  )
        return ip_address
    except socket.error as e:
        logger.error("Unable to retrieve the IP address.")
        return None


@app.route('/returnFile/')
def returnFile():
	try:
		return send_file('./ohhey.pdf', attachment_filename='ohhey.pdf')
	except Exception as e:
		return str(e)


@app.route('/receiveStakingInfo', methods=['POST'])
def receiveStakingInfo():
    try:
        data = request.get_json()
        received_text = data['text']
        print(f"Received text from frontend: {received_text}")
        # Process the received text as needed
        # ...
        priceDatabase.getPrice(coin='', date='', currency='' )  
              
        return jsonify({'message': 'Text received successfully'}), 200
    
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500



if __name__ == '__main__':
    
    logger.info( "Staking Tax starting..."  )

    priceCoingecko = priceCoingecko()
    priceDatabase = mongoPriceDatabase( sys.argv,
                                       ["EUR", "USD"],
                                       ["Fort", "Tara", "Azero"],
                                       priceCoingecko
                                       )
    
    #start database thread
    databaseThread = threading.Thread( target=priceDatabase.run, 
                                       daemon=True,
                                       args=() 
                                       )
    databaseThread.start()
    

    #start flask
    app.run(debug=True,
            use_reloader = False,
            host=get_ip_address(), 
            port=5000
            )
    
    
    
    
    
    
