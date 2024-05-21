var current_player = 1
var aiVsAi = false
var gameover = false

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function json_to_html(jd) {
    // Supprimer tous les pions du plateau
    const pions = document.querySelectorAll('.pion');
    pions.forEach(pion => {
        pion.remove();
    });
    
    for (var i = 0; i < jd.pion_noir.length; i++) {
        $('#' + jd.pion_noir[i]).append('<div class="pion pion_noir"></div>');
    }
    for (var i = 0; i < jd.pion_blanc.length; i++) {
        $('#' + jd.pion_blanc[i]).append('<div class="pion pion_blanc"></div>');
    }
    for (var i = 0; i < jd.outline_pion_noir.length; i++) {
        $('#' + jd.outline_pion_noir[i]).append('<div class="pion pion_ghost pion_ghost_noir"></div>');
    }
    for (var i = 0; i < jd.outline_pion_blanc.length; i++) {
        $('#' + jd.outline_pion_blanc[i]).append('<div class="pion pion_ghost pion_ghost_blanc"></div>');
    }

    var nombreElementsBlancs = $('.pion_blanc').length;
    var nombreElementsNoirs = $('.pion_noir').length;
    
    nb_pions_blanc = document.querySelectorAll('#nb_pions_blanc');
    nb_pions_noir = document.querySelectorAll('#nb_pions_noir');

    nb_pions_blanc.forEach(nb_pion => {
        nb_pion.textContent = nombreElementsBlancs;
    });

    nb_pions_noir.forEach(nb_pion => {
        nb_pion.textContent = nombreElementsNoirs;
    });

    if (jd.gameover == true) {
        gameover = true;
        if (nombreElementsBlancs > nombreElementsNoirs) {
            $('.final_msg').text('Les blancs ont gagné !');
        }
        else {
            if (nombreElementsBlancs < nombreElementsNoirs) {
                $('.final_msg').text('Les noirs ont gagné !');
            }
            else {
                $('.final_msg').text('Egalité !');
            }
        }
    }

    current_player = jd.player;
}

function initialiser() {
    current_player = 1;
    gameover = false;
    $.getJSON('/initialisation', function(jd)  {
        json_to_html(jd);            
    });
    $('.final_msg').text(' ');
}

document.addEventListener("DOMContentLoaded", function() {
    initialiser();
});

async function ai_play_white(heuristique){
    await $.getJSON('/ai_move_white/' + heuristique, async function(jd) {
        if (current_player == 0) {
            return false
        }
        await json_to_html(jd); 
    });
    return false
}

async function ai_play_black(heuristique){
    await $.getJSON('/ai_move_black/' + heuristique, async function(jd) {
        if (current_player == 0) {
            return false
        }
        await json_to_html(jd); 
    });
    return false
}

// Lorsqu'on clique sur une case
$(async function() {
    $('button.case').on('click', async function(e) {

        if (!($('#' + this.id).find('.pion_ghost').length)) {
            return false;
        }
        this_id = $(this).attr('id');
        e.preventDefault()

        await $.getJSON('/placement/' + this_id, async function(jd)  {
            await json_to_html(jd);            
        });
        var heuristique = 1;
        if ($('.pion_noir').length + $('.pion_blanc').length == 45) {
            heuristique = 0;
        }
        while (current_player == 2) {
            await ai_play_white(heuristique);
        }

        return false;
    });
});

async function ai_vs_ai() {
    var heuristique = 1;
    while (aiVsAi && gameover == false) {
        if ($('.pion_noir').length + $('.pion_blanc').length == 45) {
            heuristique = 0;
        }
        while (current_player == 1 && aiVsAi && gameover == false) {
            await ai_play_black(heuristique);
            
        }
        while (current_player == 2 && aiVsAi && gameover == false) {
            await ai_play_white(heuristique);
        }
    }
};
    

// Lorsqu'on clique sur le bouton rejouer
$(function() {
    $('button#rejouer_Joueur').on('click', async function(e) {
        // Appeler la fonction d'initialisation lorsque le bouton est cliqué
        aiVsAi = false;
        current_player = 0;
        await sleep(100);
        e.preventDefault()
        initialiser();

        return false;
    });
});

$(function() {
    $('button#rejouer_IA').on('click', function(e) {
        // Appeler la fonction d'initialisation lorsque le bouton est cliqué        
        e.preventDefault()
        initialiser();
        aiVsAi = true;
        ai_vs_ai();

        return false;
    });
});

// Easter egg
var root = document.documentElement;

var i = 300;

var easteregg_on = false;
    
async function rainbow() {
    while (easteregg_on) {
        await sleep(10);
        root.style.setProperty('--base', i);
        i++;
    }
}

var easteregg = document.getElementById('footer_text');

$(function() {
    easteregg.addEventListener('click', async function(e) {
        if (easteregg_on) {
            easteregg_on = false;
        }
        else {
            easteregg_on = true;
            rainbow();
        }
    });
});