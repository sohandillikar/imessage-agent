from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def receive_location():
    data = request.get_json()
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    accuracy = data.get('accuracy')
    timestamp = data.get('timestamp')
    
    print(f"Received location: {latitude}, {longitude}")
    print(f"Accuracy: {accuracy} meters")
    print(f"Timestamp: {timestamp}")
    
    # You can process the location data here
    # Save to database, send to API, etc.
    
    return jsonify({
        'status': 'success',
        'message': 'Location received',
        'received_data': {
            'latitude': latitude,
            'longitude': longitude,
            'accuracy': accuracy
        }
    })

@app.route('/location', methods=['GET'])
def get_location_page():
    return render_template('location.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
