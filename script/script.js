
const socket = io();

// Funkcja tworząca i animująca bańkę
function createBubble(imageSrc, text, balloonId) {
  const bubble = document.createElement('div');
  bubble.classList.add('bajka');

  // Oblicz losowy punkt w promieniu wokół balona
  const radius = 450;

  // Dodaj obrazek do bańki


  const img = document.createElement('img');
  img.src = "/static/" + imageSrc;
  bubble.appendChild(img);

  // Dodaj tekst pod obrazkiem
  const textElement = document.createElement('span');
  textElement.textContent = text;
  bubble.appendChild(textElement);


  const balloon = document.querySelector(`#${balloonId} .balon`);
  if (!balloon) {
    console.error(`Balon z ID "${balloonId}" nie istnieje.`);
    return;
  }
  //zmiana obramówki
  const balloonColor = getComputedStyle(balloon).getPropertyValue('--primary-color').trim();

  img.style.border = `2px solid ${balloonColor}`;

  // Pobierz współrzędne środka balona
  const balloonRect = balloon.getBoundingClientRect();
  const balloonCenterX = balloonRect.left + balloonRect.width / 2;
  const balloonCenterY = balloonRect.top + balloonRect.height / 2;


  // Losuj kąt i punkt początkowy bańki
  // const angle = Math.random() * Math.PI * 2;
  // const centerX = window.innerWidth / 2;
  // const centerY = window.innerHeight / 2;
  // const startX = balloonCenterX + radius * Math.cos(angle);
  // const startY = balloonCenterY + radius * Math.sin(angle);


  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;

  const centerWidth = windowWidth / 3; // Szerokość środkowego 1/3 ekranu
  const startX = centerWidth + Math.random() * centerWidth; // Pozycja X w środkowym obszarze

  const startY = Math.random() > 0.5 ? -50 : windowHeight + 50; // Góra (-50) lub dół (+50)


  // Pozycjonuj bańkę w losowym punkcie
  bubble.style.left = `${startX}px`;
  bubble.style.top = `${startY}px`;

  // Oblicz przesunięcie do centrum balonu


  const deltaX = balloonCenterX - startX;
  const deltaY = balloonCenterY - startY;

  // Przekaż zmienne do CSS za pomocą właściwości --x i --y
  bubble.style.setProperty('--x', `${deltaX}px`);
  bubble.style.setProperty('--y', `${deltaY}px`);

  document.body.appendChild(bubble);
  setTimeout(() => {
    const soundNumber = Math.floor(Math.random() * 8) + 1;
    var plumpSound = document.getElementById(`plump${soundNumber}`);
    plumpSound.play();
  }, 3000)
  // Usuń bańkę po zakończeniu animacji
  bubble.addEventListener('animationend', () => {
    bubble.remove();


  });
}

// Obsługa zdarzenia "bombel" z backendu
socket.on('bombel2', (data) => {
  createBubble(data.image, data.text, "balon-niebieski");
});
socket.on('bombel1', (data) => {
  createBubble(data.image, data.text, "balon-czerwony");
});

socket.on('powieksz_balonaRED', () => {
  powiekszBalon('balon-czerwony');
});

socket.on('powieksz_balonaBLUE', () => {
  powiekszBalon('balon-niebieski');
});

function powiekszBalon(balonId) {
  setTimeout(() => {
    const balloncontainer = document.querySelector(`#${balonId}`);
    const balon = document.querySelector(`#${balonId} .balon`);
    const sznurek = document.querySelector(`#${balonId} .sznurek`);
    const trojkat = document.querySelector(`#${balonId} .trojkat`);
    let scale = parseFloat(balon.style.transform.split('(')[1]?.split(')')[0] || 0.7);
    scale += 0.01;
    balon.style.transform = `scale(${scale})`;
    //balon.style.zIndex = "";
    balloncontainer.style.zIndex = 10 + 1000 * scale;
    const newHeight = 99 * scale + 108;
    sznurek.style.top = `${newHeight}px`;
    trojkat.style.top = `${newHeight - 14}px`;
  }, 3000)
}

document.addEventListener('DOMContentLoaded', function () {
  // Słuchacz zdarzenia do zmiany na niebieski
  socket.on('zmien_na_niebieski', function () {
    zmienKąt(180);  // Przejście na kąt 190 stopni w 5 sekund
  });

  // Słuchacz zdarzenia do zmiany na czerwony
  socket.on('zmien_na_czerwony', function () {
    zmienKąt(180);  // Przejście na kąt 10 stopni w 5 sekund
  });
});
godzina = 10;

function zmienKąt(kąt) {
  const wskazówka = document.querySelector('.hour-hand');
  wskazówka.style.transform = `rotate(${godzina + kąt / 2 - 10}deg)`;  // Płynne przejście
  // Uruchamiamy animację
  setTimeout(() => {
    //wskazówka.style.transition = 'transform 5s ease-in-out';  // Ponownie dodajemy animację
    wskazówka.style.transform = `rotate(${godzina + kąt}deg)`;
    godzina = godzina + 180;  // Płynne przejście
  }, 5000);  // Małe opóźnienie dla restartu animacji

}

socket.on("boom1", () => {
  const balonCont = document.querySelector(`#balon-niebieski`);
  if (!balonCont) {
    console.error(`Balon z ID "#balon-niebieski" nie istnieje.`);
    return;
  }
  balonCont.style.animation = '';
  balonCont.offsetHeight
  balonCont.style.animation = 'floatout 3s linear forwards';
  triggerExplosion("balon-czerwony");
  setTimeout(() => {
    balonCont.remove();
    spawnNewBalloonRED() // Możesz dostosować lub usunąć tę funkcję, jeśli nie chcesz odtwarzać balonów.
    setTimeout(() => { spawnNewBalloonBLUE() }, 2500)
  }, 3000)

});
socket.on("boom2", () => {
  const balonCont = document.querySelector(`#balon-czerwony`);
  if (!balonCont) {
    console.error(`Balon z ID "#balon-czerwony" nie istnieje.`);
    return;
  }
  balonCont.style.animation = '';
  balonCont.offsetHeight
  balonCont.style.animation = 'floatout 3s linear forwards';
  triggerExplosion("balon-niebieski");
  setTimeout(() => {
    balonCont.remove();
    spawnNewBalloonBLUE() // Możesz dostosować lub usunąć tę funkcję, jeśli nie chcesz odtwarzać balonów.
    setTimeout(() => { spawnNewBalloonRED() }, 2500)
  }, 3000)
});

function triggerExplosion(balloonId) {
  // Funkcja wywołana podczas wybuchu animacji
  var explosionSound = document.getElementById('explosionSound');

  explosionSound.play();

  const balonCont = document.querySelector(`#${balloonId}`);
  if (!balonCont) {
    console.error(`Balon z ID "${balloonId}" nie istnieje.`);
    return;
  }

  const balon = balonCont.querySelector('.balon');
  const balonStyle = window.getComputedStyle(balon);
  const body = document.querySelector('body');
  const pieces = [];
  const numPieces = 150;
  const balloonRect = balon.getBoundingClientRect(); // Pobierz rozmiar balona

  // Środek balona w oknie przeglądarki
  const balloonCenterX = balloonRect.left + balloonRect.width / 2;
  const balloonCenterY = balloonRect.top + balloonRect.height / 2;
  const radius = 950; // Promień wokół balona, w którym będą rozmieszczone kawałki

  for (let i = 0; i < numPieces; i++) {
    const piece = document.createElement('div');
    piece.classList.add('piece');

    // Losowy kąt w radianach
    const angle = Math.random() * 2 * Math.PI; // Kąt w zakresie od 0 do 2π
    // Losowy promień w obrębie określonego promienia (radius)
    const randomRadius = Math.random() * radius + 50;

    // Oblicz nowe współrzędne na okręgu
    const x = balloonCenterX + randomRadius * Math.cos(angle);
    const y = balloonCenterY + randomRadius * Math.sin(angle);

    piece.style.left = `${balloonCenterX}px`; // Początkowa pozycja na osi X
    piece.style.top = `${balloonCenterY}px`;  // Początkowa pozycja na osi Y

    piece.style.background = balonStyle.background;
    // Ustawienia animacji
    piece.style.setProperty('--x', `${x - balloonCenterX}px`);
    piece.style.setProperty('--y', `${y - balloonCenterY}px`);

    pieces.push(piece);
    body.appendChild(piece);

    // Ustaw animację eksplozji
    piece.style.animation = 'explode 5s ease-out forwards';

  }
  balonCont.style.animation = ''; // Wyłącz inne animacje
  balonCont.style.animation = 'explode-balloon 0.5s ease-out forwards';

  setTimeout(() => {
    pieces.forEach(p => p.remove());
    balonCont.remove(); // Możesz dostosować lub usunąć tę funkcję, jeśli nie chcesz odtwarzać balonów.
  }, 3000);
}

function spawnNewBalloonRED() {
  const body = document.querySelector('body');

  // Tworzenie nowego kontenera balona
  const newContainer = document.createElement('div');
  newContainer.id = "balon-czerwony";
  newContainer.classList.add('balon-container');
  newContainer.innerHTML = `
   <div class="balon" style="--primary-color: #ff5f57; --secondary-color: #e25f4f;">
      <div class="otwor"></div>
    </div>
    <div class="trojkat" style="--primary-color: #ff5f57; --secondary-color: #e25f4f;" ></div>
    <div class="sznurek">
      <svg viewBox="0 0 10 200">
        <path d="M0 0 Q10 20 0 40 T0 80 T0 120 T0 160"></path>
      </svg>
    </div>
  `;
  body.appendChild(newContainer);

}
function spawnNewBalloonBLUE() {
  const body = document.querySelector('body');

  // Tworzenie nowego kontenera balona
  const newContainer = document.createElement('div');
  newContainer.id = "balon-niebieski";
  newContainer.classList.add('balon-container');
  newContainer.innerHTML = `
   <div class="balon" style="--primary-color: #4f83e2; --secondary-color: #3b72d0;">
      <div class="otwor"></div>
    </div>
    <div class="trojkat" style="--primary-color: #4f83e2; --secondary-color: #3b72d0;" ></div>
    <div class="sznurek">
      <svg viewBox="0 0 10 200">
        <path d="M0 0 Q10 20 0 40 T0 80 T0 120 T0 160"></path>
      </svg>
    </div>
  `;
  body.appendChild(newContainer);

}


