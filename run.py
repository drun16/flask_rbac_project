# run.py

from app import create_app

# Create the Flask app instance using the app factory
app = create_app()

if __name__ == '__main__':
    # The host='0.0.0.0' makes the server accessible from other devices on the network
    app.run(host='0.0.0.0', port=5000, debug=True)