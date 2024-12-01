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
    socketio.emit('powieksz_balonaRED',{'size': 10})

    text_choice = "Napis pod obrazkiem"  # Możesz dodać dynamiczne napisy
    socketio.emit('bombelRED', {'image': "download.jpg", 'text': text_choice, 'size':20})

def powieksz_balonaBLUE():
    # Wysyłanie komunikatu do klienta do powiększenia balona
    socketio.emit('powieksz_balonaBLUE',{'size': 10})

    text_choice = "Napis pod obrazkiem"  # Możesz dodać dynamiczne napisy
    socketio.emit('bombelBLUE', {'image': "download.jpg", 'text': text_choice, 'size':30})


def on_press(key):
    if hasattr(key, 'char') and key.char == 'z':
                socketio.emit('zmien_na_kat',{'kat':180})
    if hasattr(key, 'char') and key.char == 'x':
                socketio.emit('przesun_o_i_w',{'kat':180,'czas':1000})
    if hasattr(key, 'char') and key.char == 'a':
            socketio.emit('boomRED')
    if hasattr(key, 'char') and key.char == 's':
            socketio.emit('boomBLUE')
    if hasattr(key, 'char') and key.char == 'd':
            powieksz_balonaRED()
    if key == keyboard.Key.space:    
        powieksz_balonaBLUE()
if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    socketio.run(app, debug=True)
