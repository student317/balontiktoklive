from TikTokLive import TikTokLiveClient  
from TikTokLive.events import ConnectEvent, CommentEvent,GiftEvent,LikeEvent
from TikTokLive.proto.custom_proto import ExtendedUser
# Create the client
import requests
import os

import threading




from pynput import keyboard
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('frontendGame1.html')


def run_server():
    socketio.run(app, debug=False)

# Tworzenie i uruchomienie wątku dla serwera Flask
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

print("Serwer Flask działa w tle!")

a = input("Nazwa konta: ")
client: TikTokLiveClient = TikTokLiveClient(a)


def downloadjpg(usr : ExtendedUser):
    link = usr.avatar_thumb.url_list[-1]
    nowa_nazwa = usr.unique_id + ".jpg"
    folder ="static"
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Pełna ścieżka do pliku
    sciezka_do_pliku = os.path.join(folder, nowa_nazwa)

    try:
        # Pobranie obrazu
        response = requests.get(link, stream=True)
        response.raise_for_status()  # Sprawdzenie, czy zapytanie zakończyło się powodzeniem

        # Sprawdzenie, czy treść to obraz
        if "image" not in response.headers["Content-Type"]:
            print("Podany link nie prowadzi do obrazu.")
            return
        
        # Zapis obrazu do folderu z nową nazwą
        with open(sciezka_do_pliku, "wb") as file:
            for chunk in response.iter_content(1024):  # Pobieranie w kawałkach
                file.write(chunk)
        
        print(f"Obraz zapisano jako: {sciezka_do_pliku}")
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił błąd podczas pobierania obrazu: {e}")

# Listen to an event with a decorator!
@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"Connected to @{event.unique_id} (Room ID: {client.room_id}   ")

@client.on(GiftEvent)
async def on_connect(event: GiftEvent):
    print(f"to_user  unique_id: {event.to_user.unique_id} ")
    if event.gift.diamond_count >= 99:
        socketio.emit('boom')
        ile =0
    if False: #event.gift.diamond_count :
        print(f"to_user  unique_id: {event.to_user.unique_id} user :  unique_id: {event.user.unique_id}"+
            f"img: {event.user.avatar_jpg}  gift: {event.gift.describe}  streaking: {event.streaking} "+
            f"value: {event.value}    gift name:  {event.gift.name} dimondcount {event.gift.diamond_count}")
    

ile = 0
# Or, add it manually via "client.add_listener()"
async def on_comment(event: CommentEvent) -> None:
    #print("cotami?")
    nick = event.user.unique_id
    downloadjpg(event.user)
    socketio.emit('powieksz_balona')
    global ile
    ile += 1
    text_choice = event.comment # Możesz dodać dynamiczne napisy
    socketio.emit('bombel', {'image': nick+".jpg", 'text': text_choice})
    if ile > 100:
        socketio.emit('boom')
        ile =0
    

async def on_like(event: LikeEvent) -> None:
    #print("lke?")
    nick = event.user.unique_id
    downloadjpg(event.user)
    socketio.emit('powieksz_balona')
    global ile
    ile += 1
    text_choice = "❤️" # Możesz dodać dynamiczne napisy
    socketio.emit('bombel', {'image': nick+".jpg", 'text': text_choice})
    if ile > 100:
        socketio.emit('boom')
        ile =0

#socketio.emit('boom')

    #print(f"{event.user.nickname} -> {event.comment}  img: {event.user.avatar_thumb.url_list} ")
    #print(f" img: {event.user.avatar_thumb.url_list}  img: {event.user.avatar_jpg.url_list} ")
client.add_listener(LikeEvent, on_like)
client.add_listener(CommentEvent, on_comment)

while True:
    client.run()

