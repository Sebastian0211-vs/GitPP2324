from flask import Flask, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

@app.route('/pin/<str:cellule>/red/high', methods=['GET'])
def pin_RED_HIGH(cellule):
    if cellule == "spirale":
        pin_number = 13
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.output(pin_number, GPIO.HIGH)
    return jsonify(message=f"Cellules {cellule} a été mise en rouge"), 200

@app.route('/pin/<str:cellule>/red/down', methods=['GET'])
def pin_RED_DOWN(cellule):
    if cellule == "spirale":
        pin_number = 13 
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.output(pin_number, GPIO.LOW)
    return jsonify(message=f"Cellules {cellule} a désactivé la couleur rouge"), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify(error="Not found"), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify(error="Internal server error"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)