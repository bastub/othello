$(function() {
    $('button.case').on('click', function(e) {
        if (!($('#' + this.id).find('.pion_outline_noir').length)) {
            return false;
        }
        this_id = $(this).attr('id');
        
        // Supprimer tous les pions du plateau
        /*
        const pions = document.querySelectorAll('.pion');
        pions.forEach(pion => {
            pion.remove();
        });
        */
        if ($('#' + this_id).children().length > 0) {
            $('#' + this_id).children().remove();
        }
        $('#' + this_id).append('<div class="pion pion_noir"></div>');

        var nombreElementsBlancs = $('.pion_blanc').length;
        var nombreElementsNoirs = $('.pion_noir').length;
        $('#nb_pions_blanc').text(nombreElementsBlancs);
        $('#nb_pions_noir').text(nombreElementsNoirs);

        /*
        e.preventDefault()
        $.getJSON('/background_process_test', function(jd) {
            console.log(jd.pion_blanc)
            console.log(jd.pion_noir)
            for (var i = 0; i < jd.pion_noir.length; i++) {
                id = jd.pion_noir[i];
                $('#' + id).append('<div class="pion pion_noir"></div>');
            }
        });
        */
        return false;
    });
});