// Ottieni i valori di total_cost, max_cost e show_progress_bar tramite data-attributes
const costInfoElement = document.getElementById('cost-info');
var totalCost = parseFloat(costInfoElement.getAttribute('data-total-cost'));
const maxCost = parseFloat(costInfoElement.getAttribute('data-max-cost'));
var showProgressBar = costInfoElement.getAttribute('data-show-progress-bar') === 'True';  // Convertilo in booleano


// Aggiungi un listener per l'aggiornamento del totalCost
socket.on('increment-total-cost', function (data) {
    // Ricarica la pagina per applicare i nuovi valori
    var cost_to_add = data.increment;
    updateTotalCost(cost_to_add)
});

// Aggiungi un listener per l'aggiornamento dell'obiettivo
socket.on('update-goal', function (data) {
    // Ricarica la pagina per applicare il nuovo obiettivo
    window.location.reload();
});

// Se la barra di progresso non deve essere mostrata, nascondila
if (!showProgressBar) {
    document.getElementById('progress-bar-container').style.display = 'none';
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
