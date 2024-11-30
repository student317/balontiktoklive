from pynput import keyboard
from flask import Flask, render_template,send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('frontendGame1.html')

@app.route('/script/<path:filename>')
def serve_script(filename):
    return send_from_directory('script', filename)

def powieksz_balonaRED():
    # Wysyłanie komunikatu do klienta do powiększenia balona
    socketio.emit('powieksz_balonaRED')

    text_choice = "Napis pod obrazkiem"  # Możesz dodać dynamiczne napisy
    socketio.emit('bombel1', {'image': "download.jpg", 'text': text_choice})

def powieksz_balonaBLUE():
    # Wysyłanie komunikatu do klienta do powiększenia balona
    socketio.emit('powieksz_balonaBLUE')

    text_choice = "Napis pod obrazkiem"  # Możesz dodać dynamiczne napisy
    socketio.emit('bombel2', {'image': "download.jpg", 'text': text_choice})


def on_press(key):
    if hasattr(key, 'char') and key.char == 'z':
                socketio.emit('zmien_na_niebieski')
    if hasattr(key, 'char') and key.char == 'x':
                socketio.emit('zmien_na_czerwony')
    if hasattr(key, 'char') and key.char == 'a':
            socketio.emit('boom1')
    if hasattr(key, 'char') and key.char == 's':
            socketio.emit('boom2')
    if hasattr(key, 'char') and key.char == 'd':
            powieksz_balonaRED()
    if key == keyboard.Key.space:    
        powieksz_balonaBLUE()
if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    socketio.run(app, debug=True)
