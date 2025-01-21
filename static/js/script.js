const socket = io();

// Ottieni i valori di total_cost, max_cost e show_progress_bar tramite data-attributes
const costInfoElement = document.getElementById('cost-info');
var totalCost = parseFloat(costInfoElement.getAttribute('data-total-cost'));
const maxCost = parseFloat(costInfoElement.getAttribute('data-max-cost'));
var showProgressBar = costInfoElement.getAttribute('data-show-progress-bar') === 'True';  // Convertilo in booleano

let requestQueue = []; // Coda per le richieste
let isProcessing = false; // Flag per gestire il processo

// Se la barra di progresso non deve essere mostrata, nascondila
if (!showProgressBar) {
    document.getElementById('progress-bar-container').style.display = 'none';
}

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

// Funzione per aggiornare il totale del costo
function updateTotalCost(costo) {
    totalCost += costo;
    calculateProgress();
}

function calculateProgress() {
    // Esegui solo se showProgressBar è true
    if (showProgressBar) {
        const progress = Math.min((totalCost / maxCost) * 100, 100);
        updateProgressBar(progress);
    }
}

function updateProgressBar(progress) {
    // Esegui solo se showProgressBar è true
    if (!showProgressBar) {
        return; // Non fare nulla se la barra non deve essere mostrata
    }

    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = progress + "%";

    // Verifica se la barra ha raggiunto il 100% solo se la barra è visibile
    if (progress === 100 && showProgressBar) {
        playCompletionSound().then(() => {
            showProgressBar = false;
            fadeOutProgressBar(); // Nascondi la barra dopo il completamento
        });
    }
}

// Funzione per riprodurre il suono quando la barra raggiunge il 100%
function playCompletionSound() {
    return new Promise((resolve) => {
        const completionSound = document.getElementById('completion-sound');
        completionSound.play(); // Riproduce il suono

        completionSound.onended = () => {
            resolve(); // Risolvi la promessa quando il suono è finito
        };
    });
}

// Funzione per fare la dissolvenza dell'intero contenitore della barra di progresso
function fadeOutProgressBar() {
    const progressBarContainer = document.getElementById('progress-bar-container');

    // Aggiungi la classe fade-out-bar-container per fare la dissolvenza
    progressBarContainer.classList.add('fade-out-bar-container');

    // Dopo la dissolvenza (1 secondo), resetta la barra per essere pronta per il riutilizzo
    setTimeout(() => {
        // Reset della barra di progresso
        const progressBar = document.getElementById('progress-bar');
        progressBar.style.width = '0%'; // Rimuovi il riempimento
    }, 1000); // Tempo di dissolvenza in millisecondi (1 secondo)
}



// Calcola e aggiorna la barra di progresso all'inizializzazione
calculateProgress();
