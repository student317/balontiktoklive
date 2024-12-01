from TikTokLive import TikTokLiveClient  
from TikTokLive.events import ConnectEvent, CommentEvent,GiftEvent,LikeEvent
from TikTokLive.proto.custom_proto import ExtendedUser
from TikTokLive.client.errors import UserOfflineError
import time
import asyncio
# Create the client
import requests
import os
import threading


from pynput import keyboard
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)
lock = asyncio.Lock()
redsize = 0
bluesize = 0
glory = []
@app.route('/')
def index():
    return render_template('frontendGame1.html')


@app.route('/script/<path:filename>')
def serve_script(filename):
    return send_from_directory('script', filename)


def run_server():
    socketio.run(app, debug=False)

# Tworzenie i uruchomienie wątku dla serwera Flask
server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()

print("Serwer Flask działa w tle!")

import configparser

# Wczytanie konfiguracji
config = configparser.ConfigParser()
config.read('config.ini')

accontName =  config["settings"]["account_name"]
client: TikTokLiveClient = TikTokLiveClient(accontName)

MAX_RETRIES = int( config["settings"]["connect_reties"])
RETRY_DELAY = int( config["settings"]["connect_delay"])  # czas w sekundach
Tura = "RED"

def downloadjpg(usr : ExtendedUser):
    link = usr.avatar_thumb.url_list[-1]
    nowa_nazwa = usr.unique_id + ".jpg"
    folder ="static"
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Pełna ścieżka do pliku
    sciezka_do_pliku = os.path.join(folder, nowa_nazwa)

    if os.path.exists(sciezka_do_pliku):
        print(f"Plik {sciezka_do_pliku} już istnieje. Pobieranie pominięte.")
        return  # Zakończenie funkcji, jeśli plik już istnieje

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
async def on_gift(event: GiftEvent):
    global redsize
    global bluesize
    global glory
    nick = event.user.unique_id
    downloadjpg(event.user)
    print(f"to_user  unique_id: {nick} ")
    async with lock:
        value = event.gift.diamond_count * 10
        socketio.emit('powieksz_balona'+Tura,{'size': value})

        if value < 100:
            text_choice = nick   # Możesz dodać dynamiczne napisy
            socketio.emit('bombel'+Tura, {'image': nick+".jpg", 'text': text_choice, 'size':40})

        if value >= 100 and value < 990:
            text_choice = nick   # Możesz dodać dynamiczne napisy
            socketio.emit('bombel'+Tura, {'image': nick+".jpg", 'text': text_choice, 'size':50})
            glory.append((nick,Tura))
        
        if value >= 990:
            text_choice = nick   # Możesz dodać dynamiczne napisy
            socketio.emit('bombel'+Tura, {'image': nick+".jpg", 'text': text_choice, 'size':100})
            for _ in range(3):
                glory.append((nick,Tura))
        
        if Tura == "RED":
            redsize += value
        else:
            bluesize += value
    await blowUp()

# Or, add it manually via "client.add_listener()"
async def on_comment(event: CommentEvent) -> None:
    #print("cotami?")
    nick = event.user.unique_id
    global glory
    print(glory)
    czy = "Nie"
    async with lock:
        if (nick,"RED") in glory:
            glory.remove((nick,"RED"))
            czy = "RED"
        if (nick,"BLUE") in glory:
            glory.remove((nick,"BLUE"))
            czy="BLUE"
        if czy != "Nie":
            text_choice = event.comment # Możesz dodać dynamiczne napisy
            socketio.emit('bombel'+czy, {'image': nick+".jpg", 'text': text_choice, 'size':50})
    

async def on_like(event: LikeEvent) -> None:
    #print("lke?")
    global redsize
    global bluesize
    nick = event.user.unique_id
    downloadjpg(event.user)
    async with lock:
        socketio.emit('powieksz_balona'+Tura,{'size': 5})
        text_choice = "❤️" # Możesz dodać dynamiczne napisy
        socketio.emit('bombel'+Tura, {'image': nick+".jpg", 'text': text_choice, 'size':30})

        if Tura == "RED":
            redsize += 5
        else:
            bluesize += 5
    await blowUp()


async def blowUp() -> None:
    async with lock:
        global Tura
        global redsize
        global bluesize
        print(f"redsize:{redsize}")
        print(f"bluesize:{bluesize}")
        tak = False
        if redsize >= 2300:
            time.sleep(3)
            socketio.emit('boomRED')
            Tura = "BLUE"
            socketio.emit('zmien_na_kat',{'kat':5})
            tak = True
        if bluesize >= 2300:
            time.sleep(3)
            socketio.emit('boomBLUE')
            Tura = "RED"
            socketio.emit('zmien_na_kat',{'kat':185})
            tak = True
        if tak :
            redsize = 0
            bluesize = 0
           
            time.sleep(6)
#socketio.emit('boom')

    #print(f"{event.user.nickname} -> {event.comment}  img: {event.user.avatar_thumb.url_list} ")
    #print(f" img: {event.user.avatar_thumb.url_list}  img: {event.user.avatar_jpg.url_list} ")
client.add_listener(LikeEvent, on_like)
client.add_listener(CommentEvent, on_comment)


# Funkcja uruchamiająca klienta z obsługą wyjątków
async def connect_client_with_retry(client):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Próba {attempt}/{MAX_RETRIES}: Uruchamianie klienta...")
            await client.start()
            break
            # Jeśli się uda, przerywamy pętlę
        except UserOfflineError as e:
            print(f"Użytkownik jest offline: {e}")
            if attempt < MAX_RETRIES:  # Jeśli nie wyczerpaliśmy prób
                print(f"Ponawianie próby za {RETRY_DELAY} sekund...")
                time.sleep(RETRY_DELAY)
            else:
                print("Przekroczono maksymalną liczbę prób. Nie udało się połączyć.")
                return None
        except Exception as e:
            print(f"Napotkano inny błąd: {e}")
            return None   # Jeśli to nie jest błąd "offline", zakończ program
    

async def main():
    try:
        await connect_client_with_retry(client)
    except Exception as e:
        print(f"Nie można uruchomić klienta: {e}")


# Uruchomienie event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())


async def main_loop():
    global Tura
    global lock
    socketio.emit('zmien_na_kat',{'kat':180})
    Tura = "RED"
    while True:
        async with lock:
            if Tura == "RED":
                Tura = "BLUE"
            else:
                Tura = "RED"
            socketio.emit('przesun_o_i_w', {'kat': 180, 'czas': 6000})
        await asyncio.sleep(6)  # Asynchroniczne czekanie bez blokowania wątku

loop2 = asyncio.get_event_loop()
time.sleep(3)
try:
    loop2.run_until_complete(main_loop())
except Exception as e:
        print(f"Nie można uruchomić klienta: {e}")
