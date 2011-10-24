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

    function EnableListView() {
      $('.details_container').hide();
      $('.viewport_minmax_container').hide();
      $('#scene_main').hide();
      $('#scene_main_1').show();
      $('.arrowLeft').hide();
      $('.arrowRight').hide();
    };

    function EnableLinearView() {
      $('.details_container').show();
      $('.viewport_minmax_container').show();
      $('#scene_main').show();
      $('#scene_main_1').hide();
      $('.arrowLeft').show();
      $('.arrowRight').show();
    };

    $('.vm_list').click(EnableListView);
    $('.vm_linear').click(EnableLinearView);


    var total_item = 0;
    var curr_item = 0;
    var file_array = null;
    function ReloadFiles() {
      // retrieve all files from server 
      $.getJSON('/list/', {'tag_list_name':''}, function(data) {
        // remove the previous items
        $('.itemnode').remove();
        total_item = data.length;

        // re-generate items
        FillInListView(data);
        FillInLinearView(data);
        file_array = data;
        return data.length;
      });
    };

    function FillInListView(data) {
      for (var i = 0 ; i < data.length ; i++) {
        var node = $('<div sortableid=' + i + '></div>');
        node.addClass('itemnode vp_list_row vp_list_row_default').appendTo('#scene_main_1');

        var col_file = $('<div class="vp_list_cell vp_list_cell_title"></div>');
        col_file.append('<span class="list-item-fileicon-container"><img src="/static/css/images/file_icon_generic_picture.png"></span>');
        col_file.append('<span class="list-item-filename-display-container"><span>' + data[i].name + '</span></span>');

        node.append(col_file);
        node.append('<div class="vp_list_cell vp_list_cell_viewer">&nbsp;</div>');
        node.append('<div class="vp_list_cell vp_list_cell_size">' + (data[i].size / 1024).toFixed(2) + 'KB</div>');
        node.append('<div class="vp_list_cell vp_list_cell_views">' + data[i].ctime + '</div>');
      }
    };

    function FillInLinearView(data) {
      for (var i = 0 ; i < data.length ; i++) {
        var left_pos = 500 + 290 * i;
        var node = $('<div class="itemnode" id="Linear_' + i + '" style="position: absolute; left: ' + left_pos + 'px">');
        node.append('<div class="thumb_outer"><div class="thumb_inner"><img src="' + data[i].url + '" class="thumb"></div></div>');
        node.append('<div class="view_cont"><div class="view"><div class="image_outer"><div class="image_caption_wrap"><div class="image_inner"><img src="' + data[i].url + '" class="image"></div></div></div></div></div>');
        node.appendTo('#scene_main');
      }
      $('#scene_main .thumb').css('height', 240);
      $('#scene_main .thumb').css('width', 240);
      $('#scene_main .thumb').css('top', -120);
      $('#scene_main .thumb').css('left', -120);
      $('#scene_main').css('width', 300 * i);
      ShowFileDetails(0);
    };

    function Linear_Next() {
      if ( curr_item == total_item - 1)
        return;
      $('.itemnode').each(function() {
        $(this).css( {left: $(this).position().left - 290 });
      });
      curr_item ++;
    };

    function Linear_Prev() {
      if ( curr_item == 0)
        return;
      $('.itemnode').each(function() {
        $(this).css( {left: $(this).position().left + 290 });
      });
      curr_item --;
    };

    function ShowFileDetails(i) {
      $('.details_container .subheader_filename').text(file_array[i].name);
    };

    $('.arrowLeft').click (Linear_Prev);
    $('.arrowRight').click (Linear_Next);

    $(document).ready(function() {
      // initialize
      $('#drag_indicator').hide();
      EnableLinearView();
      total_item = ReloadFiles();
    });

});
