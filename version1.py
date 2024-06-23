
from flask import Flask, render_template, redirect, url_for
import socket

HOST = '192.168.1.177'  # IP del Arduino
PORT = 80  # Puerto del servidor Arduino

app = Flask(__name__)

# Estado inicial del LED
arduino_response = "LED apagado"

@app.route('/')
def index():
    global arduino_response  # Accede a la variable global
    return render_template('index.html', arduino_response=arduino_response)

@app.route('/encender_led', methods=['POST'])
def encender_led():
    global arduino_response  # Accede a la variable global
    arduino_response = send_to_arduino("a")
    return redirect(url_for('index'))

@app.route('/apagar_led', methods=['POST'])
def apagar_led():
    global arduino_response  # Accede a la variable global
    arduino_response = send_to_arduino("b")
    return redirect(url_for('index'))

def send_to_arduino(command):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(command.encode())
            response = s.recv(1024).decode().strip()
        return response
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
