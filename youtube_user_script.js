// ==UserScript==
// @name         Demo vlclauncher
// @namespace    http://example.com/
// @version      0.1
// @description  button on youtube.com to launch video in vlc.
// @author       zvodd
// @match        *://youtube.com/*
// @include      *://*.youtube.com/*
// @grant        none
// @require      https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js
// ==/UserScript==

$(window.document).ready(function() {
    window.document.vlclaunch_this_page = function() {
        var openurl =  "vlclaunch://video/playsmallmode/?#" + window.location,
             myWindow = window.open(openurl, "myWindow", "width=200, height=100");
        myWindow.close();
        
        /*
        // Simulating a click event on hidden anchor.
        //I think im doing it wrong...
          var  launcher_el = $("#vlclauncher");
        if (launcher_el.length == 0){
            $(window.document.body).append('<a id="vlclauncher" href="'+openurl +'"></a>');   
            launcher_el = $("#vlclauncher");
        }
        launcher_el.trigger("click");
        */
    }
   var button_bar = $('#watch8-action-buttons');
    $("button.action-panel-trigger-share" ,button_bar).after('<button class="yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup action-panel-trigger action-panel-trigger-share yt-uix-tooltip"\
type="button" onclick=";vlclaunch_this_page();" title="VLC" data-tooltip-text="VLC">\
    <span class="yt-uix-button-content">VLC</span></button>')
});
