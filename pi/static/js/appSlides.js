/*
 * jQuery File Upload Plugin JS Example 5.0.2
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://creativecommons.org/licenses/MIT/
 */

/*jslint nomen: true */
/*global $ */

$(function () {
    'use strict';

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload();
/*    $('#fileupload').fileupload({
        // this formData is neccessary to pass the csrf and pass uid to django
        formData: [
            { name: "uid", value: "{{ uid }}"},
            { name: "csrfmiddlewaretoken", value: "{{ csrf_token }}"}
        ],
        maxFileSize: {{ maxfilesize }},
        minFileSize: {{ minfilesize }},
        sequentialUploads: true
    });
*/

    // Load existing files:
    $.getJSON($('#fileupload form').prop('action'), function (files) {
        var fu = $('#fileupload').data('fileupload');
        fu._adjustMaxNumberOfFiles(-files.length);
        fu._renderDownload(files)
            .appendTo($('#fileupload .files'))
            .fadeIn(function () {
                // Fix for IE7 and lower:
                $(this).show();
            });
   });

    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });

    var side_menu_status = 'minimized';
    $('.viewport_minmax_button').click(function() {
      if (side_menu_status == 'minimized') {
        $(this).removeClass('minimized').addClass('maximized');
        $('.viewport_sidemenu_container').fadeIn();
        side_menu_status = 'maximized';
      } else {
        $(this).removeClass('maximized').addClass('minimized');
        $('.viewport_sidemenu_container').fadeOut();
        side_menu_status = 'minimized';
      }
    });

    $('*[option_description]').mouseover(function() {

    });

    $('.vm_list').click(function() {
      $('.details_container').hide();
      $('.viewport_minmax_container').hide();
      $('#scene_main').hide();
      $('#scene_main_1').show();
      $('.arrowLeft').hide();
      $('.arrowRight').hide();
    });

    $('.vm_linear').click(function() {
      $('.details_container').show();
      $('.viewport_minmax_container').show();
      $('#scene_main').show();
      $('#scene_main_1').hide();
      $('.arrowLeft').show();
      $('.arrowRight').show();
    });


    /* Get the curent slide */
    function currentSlide( current ) {
        $(".current_slide").text(current + " of " + $("#slides").slides("status","total") );
    }

    /* Initialize SlidesJS */
    $("#slides").slides({
        navigateEnd: function( current ) {
            currentSlide( current );
        },
        loaded: function(){
            currentSlide( 1 );
        }
    });

    /* Play/stop button */
    $(".controls").click(function(e) {
        e.preventDefault();
                
        // Example status method usage
        var slidesStatus = $("#slides").slides("status","state");
                
        if (!slidesStatus || slidesStatus === "stopped") {

            // Example play method usage
            $("#slides").slides("play");

            // Change text
            $(this).text("Stop");
        } else {
                
            // Example stop method usage
            $("#slides").slides("stop");
                    
            // Change text
            $(this).text("Play");
        }
    });

    var globalSlides = []

    function genSlides() {
        // generate new slides contents
        var allSlides = '<div id="slides">';
        for (var i = 0; i < globalSlides.length; i++) {
            var slide = '<div><img src="' + globalSlides[i].url + '" width="780" height="300"></div>';
            allSlides = allSlides + slide;
        }
        allSlides = allSlides + '</div>';

        // replace current cont with the new slides
        // Slides.js automatically expands id="slides"
        $("#slidesCont").empty();
        $("#slidesCont").append(allSlides);
        $("#slidesCont").append('<a href="#" class="controls">Play</a>');
        $("#slidesCont").append('<p class="current_slide"></p>');
        $("#slides").slides();
    }
 
    $.get('/list/', {'tag_list_name': ''}, function(data) {
        // reset the show slides
        globalSlides = data;
        // regenerate the slides show
        genSlides();
    });

    // file upload done callback
    $('#fileupload').bind('fileuploaddone', function (e, data) {
        // add newly uploaded file to slides
        for (var i = 0; i < data.result.length; i++) {
            globalSlides.push(data.result[i]);
        }

        // regenerate the slides show
        genSlides();

        // goto the newly uploaded slide
        try {
            var totalCnt = $("#slides").slides("status","total");
            $("#slides").slides("slide", totalCnt);
        } catch (err) {
            // simply catch, do nothing. currently slidesjs will not generate
            // "#slides" for a single slide.
        }
    });


    /* attach a submit handler to the form */
    $("#listFileForm").submit(function(event) {
        /* stop form from submitting normally */
        event.preventDefault(); 

        /* get some values from elements on the page: */
        var $form = $(this),
        term = $form.find('#tagListName').val(),
        url = $form.attr('action');

        /* Send the data using post and put the results in a div */
        $.get(url, {'tag_list_name' : term},
              function(data) { $("#listDiv").empty(); $("#listDiv").append(data); });
    });

    $("#readFileForm").submit(function(event) {
        /* stop form from submitting normally */
        event.preventDefault(); 

        /* get some values from elements on the page: */
        var $form = $(this),
        term = $form.find('#rFileName').val(),
        url = $form.attr('action');

        /* Send the data using post and put the results in a div */
        $.get(url, {'file_name' : term},
              function(data) { $("#fileContDiv").empty(); $("#fileContDiv").append(data); });
    });

});
