let requestQueue = []; // Coda per le richieste
let isProcessing = false; // Flag per gestire il processo

// Funzione principale per gestire la coda delle richieste
function processQueue() {
    if (requestQueue.length === 0 || isProcessing) {
        return; // Se la coda è vuota o stiamo già elaborando, esci
    }

    isProcessing = true; // Imposta il flag a true per indicare che stiamo elaborando

    const currentRequest = requestQueue.shift(); // Prendi la richiesta più vecchia
    var image_src = currentRequest.image_src;
    var audio_src = currentRequest.audio_src;
    var testo = currentRequest.testo;
    var costo = currentRequest.costo;

    // Aggiorna il costo totale
    updateTotalCost(costo);

    // Aggiorna l'immagine e l'audio
    document.getElementById('image').src = image_src;
    document.getElementById('audio').src = audio_src;
    document.getElementById('testo').innerHTML = testo;

    // Riproduci audio e mostra l'immagine
    playSoundAndShowImage().then(() => {
        isProcessing = false; // Imposta il flag a false al termine del processo
        processQueue(); // Elenca la prossima richiesta nella coda
    });
}

// Aggiungi un listener per le richieste in arrivo
socket.on("incoming-request", function (data) {
    var image_src = data["data"]["image_src"];
    var audio_src = data["data"]["audio_src"];
    var testo = data["data"]["testo"];
    var costo = data["data"]["costo"];

    // Aggiungi la richiesta alla coda
    requestQueue.push({ image_src, audio_src, testo, costo });

    // Avvia il processo della coda se non è già in corso
    processQueue();
});

// Funzione per riprodurre audio e mostrare immagine
function playSoundAndShowImage() {
    return new Promise((resolve) => {
        const image_container = document.getElementById('image_container');
        const audio = document.getElementById('audio');

        // Mostra l'immagine e il testo
        image_container.classList.add('fade-in'); // Aggiungi la classe per il fade in
        image_container.classList.remove('fade-out'); // Assicurati che non sia in fade out
        image_container.style.opacity = 1;

        audio.play();

        // Attendere che l'audio finisca per risolvere la promessa
        audio.onended = () => {
            image_container.classList.remove('fade-in'); // Rimuovi la classe per il fade in
            image_container.classList.add('fade-out'); // Aggiungi la classe per il fade out
            image_container.style.opacity = 0;
            resolve(); // Risolvi la promessa quando l'audio è finito
        };
    });
}
