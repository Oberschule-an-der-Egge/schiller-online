$(document).ready(function () {

    // --- FOR DEBUGGING

    // const jsonstring = $('#session-json').text();
    // const jsonobj = JSON.parse(jsonstring);
    // const prettified = JSON.stringify(jsonobj,null,4);
    // $('#session-out').text(prettified);
    //
    // const jsonstring2 = $('#session2-json').text();
    // const jsonobj2 = JSON.parse(jsonstring2);
    // const prettified2 = JSON.stringify(jsonobj2,null,4);
    // $('#session2-out').text(prettified2);

    // --- END DEBUGGING

    // --- STEP 2: Fremdsprachen

    $('#belegverpflichtung_1').click(function () {
        if ($(this).is(':checked')) {
            $('#fremdsprache').prop('disabled', false);
            $('#freiwillig-group').hide();
        }
    });

    $('#belegverpflichtung_2').click(function () {
        if ($(this).is(':checked')) {
            $('#fremdsprache').prop('disabled', true);
            $('#freiwillig-group').show();
        }
    });

    $('#card-sprache').on('click', '#freiwillig_1', function () {
        if ($(this).is(':checked')) {
            $('#fremdsprache').prop('disabled', false);
            $('#anfaenger-group').show();
            $('#fremdsprache-group').show();
        }
    });

    $('#card-sprache').on('click', '#freiwillig_2', function () {
        if ($(this).is(':checked')) {
            $('#fremdsprache').prop('disabled', true);
            $('#anfaenger-group').hide();
            $('#fremdsprache-group').hide();
        }
    });

    // --- END STEP 2: Fremdsprachen

    // --- STEP 2: Naturwissenschaft

    // TODO / EXPERIMENTAL: Remove option nw1 from nw2, but make sure all the other options are still there
    // $('#e11_nw1').change(function () {
    //     const nw1 = $(this).find('option:selected').text();
    //     $('#e11_nw2 option').filter(function() {
    //         return $(this).text() == nw1
    //     }).remove();
    // });

    $('#card-nawi #e12_nw2').change(function () {
        const nw2 = $(this).find('option:selected').text();
        $('#q11_nw2_text').text(nw2);
        $('#q21_nw2_text').text(nw2);
        $('#q11_nw2_group').show();
    });

    $('#card-nawi').on('click', '#q11_nw2_1', function () {
        if ($(this).is(':checked')) {
            $('#q21_nw2_group').show();
        }
    });

    $('#card-nawi').on('click', '#q11_nw2_2', function () {
        if ($(this).is(':checked')) {
            $('#q21_nw2_group').hide()
            $('#q21_nw2_1, #q21_nw2_2').prop('checked', false);
        }
    });

    // --- END STEP 2: Naturwissenschaft

    // --- STEP 3: GeschichtePolitik

    $('#polq1_1').click(function () {
        if ($(this).is(':checked')) {
            $('#polq2-group').show();
        }
    });

    $('#polq1_2').click(function () {
        if ($(this).is(':checked')) {
            $('#polq2-group').hide();
            $('#polq2_1, #polq2_2').prop('checked', false);
        }
    });

    $('#gesq1_1').click(function () {
        if ($(this).is(':checked')) {
            $('#gesq2-group').show();
        }
    });

    $('#gesq1_2').click(function () {
        if ($(this).is(':checked')) {
            $('#gesq2-group').hide();
            $('#gesq2_1, #gesq2_2').prop('checked', false);
        }
    });

    // --- END STEP 3: GeschichtePolitik

    // --- STEP 3: Psychologie

    $('#psye2_1').click(function () {
        if ($(this).is(':checked')) {
            $('#psyq1-group').show();
        }
    });

    $('#psye2_2').click(function () {
        if ($(this).is(':checked')) {
            $('#psyq1-group').hide();
            $('#psyq1_1, #psyq1_2').prop('checked', false);
            $('#psyq2-group').hide();
            $('#psyq2_1, #psyq2_2').prop('checked', false);
        }
    });


    $('#card-psy').on('click', '#psyq1_1', function () {
        if ($(this).is(':checked')) {
            $('#psyq2-group').show();
        }
    });

    $('#card-psy').on('click', '#psyq1_2', function () {
        if ($(this).is(':checked')) {
            $('#psyq2-group').hide()
            $('#psyq2_1, #psyq2_2').prop('checked', false);
        }
    });

    // --- END STEP 3: Psychologie

    // --- STEP 3: Paedagogik

    $('#paeq1_1').click(function () {
        if ($(this).is(':checked')) {
            $('#paeq2-group').show();
        }
    });

    $('#paeq1_2').click(function () {
        if ($(this).is(':checked')) {
            $('#paeq2-group').hide();
            $('#paeq2_1, #paeq2_2').prop('checked', false);
        }
    });

    // --- END STEP 3: Paedagogik

    // --- STEP 3: Geographie

    $('#geoe2_1').click(function () {
        if ($(this).is(':checked')) {
            $('#geoq1-group').show();
        }
    });

    $('#geoe2_2').click(function () {
        if ($(this).is(':checked')) {
            $('#geoq1-group').hide();
            $('#geoq1_1, #geoq1_2').prop('checked', false);
            $('#geoq2-group').hide();
            $('#geoq2_1, #geoq2_2').prop('checked', false);
        }
    });


    $('#card-geo').on('click', '#geoq1_1', function () {
        if ($(this).is(':checked')) {
            $('#geoq2-group').show();
        }
    });

    $('#card-geo').on('click', '#geoq1_2', function () {
        if ($(this).is(':checked')) {
            $('#geoq2-group').hide()
            $('#geoq2_1, #geoq2_2').prop('checked', false);
        }
    });

    // --- END STEP 3: Geographie

    $('#step4 .card-header').click(function () {
        $(this).next().slideToggle()
    })

})