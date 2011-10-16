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
        alert("call fileupload");
        // this formData is neccessary to pass the csrf and pass uid to django
        formData: [
            { name: "uid", value: "{{ uid }}"},
            { name: "csrfmiddlewaretoken", value: "{{ csrf_token }}"}
        ],
        maxFileSize: {{ maxfilesize }},
        minFileSize: {{ minfilesize }},
        sequentialUploads: true,
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

});
