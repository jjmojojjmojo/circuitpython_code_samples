'use strict';

var code_index = Array();
var index_loaded = false;
var current_script = 0;
var videoElement = document.getElementById("example");

var highlight_css_url = function(url){
    if(url !== undefined){
        localStorage.setItem("code-samples:highlight-css", url);
        return url;
    } else {
        url = localStorage.getItem("code-samples:highlight-css");
        if (url === null){
            url = "css/syntax/syntax.rainbow_dash.css";
        }
        
        localStorage.setItem("code-samples:highlight-css", url);
        return url;
    }
};

var change_highlight = function(url){
    highlight_css_url(url);
    $("#syntax-css").attr("href", url);
};

function toggleFullScreen() {
    if (!document.mozFullScreen && !document.webkitFullScreen) {
      if (videoElement.mozRequestFullScreen) {
        videoElement.mozRequestFullScreen();
      } else {
        videoElement.webkitRequestFullScreen(Element.ALLOW_KEYBOARD_INPUT);
      }
    } else {
      if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
      } else {
        document.webkitCancelFullScreen();
      }
    }
}

var next_script = function(){
    current_script += 1;
    
    load_script(current_script);
};

var previous_script = function(){
    
    current_script -= 1;
    
    load_script(current_script);
};

var display_script = function(data){
    var div = $("#example");
    div.html(data);
    var index = $("<div id='example-index'></div>");
    index.html(current_script+1);
    div.append(index);
    div.scrollTop(0);
};

var load_script = function(index){
    if (index < 0){
        index = code_index.length-1;
    }
    
    if (index >= code_index.length){
        index = 0;
    }
    
    current_script = index;
    
    var info = code_index[index];
    
    history.pushState(info, info.title, "#"+(index+1));
    
    $("#title").text(info.title);
    $("#index").text(info.index);
    $("#code-examples").val(index);
    $.get({
        url: info.link,
        success: display_script
    });
};

var refresh_dropdown = function(){
    var dropdown = $("#code-examples");
    
    dropdown.html("");
    
    for (var i=0; i<code_index.length; i++){
        var option = $("<option></option>");
        option.attr("value", i);
        option.text((i+1)+": "+code_index[i].title);
        dropdown.append(option);
    }
};

var process_index = function(data){
    var doc = $(data);
    
    var titles = doc.find("dt");
    var links = doc.find("dd a");
    
    for (var i=0; i<titles.length; i++){
        code_index.push({
            title: titles[i].textContent,
            link: links[i].href,
            source: links[i].textContent,
            index: i+1
        });
    }
    
    index_loaded = true;
    
    refresh_dropdown();
    
    load_script(current_script);
};

var process_css_index = function(data){
    var select = $("#syntax-styles");
    for (var i=0; i<data.length; i++) {
        var option = $("<option></option>");
        option.attr("value", data[i].path);
        option.text(data[i].name);
        select.append(option);
    }
    
    select.val(highlight_css_url());
    select.change();
};

var reload_css_index = function(){
    $.get({
        url: "css/syntax-index.json",
        success: process_css_index
    });
};

var reload_index = function(){
    index_loaded = false;
    $.get({
        url: "code/index.html",
        success: process_index
    });
};

var handle_keypress = function(event){
    if (event.keyCode == 13) {
        toggleFullScreen();
    }
    
    if (event.keyCode == 39) {
        next_script();
    }
    
    if (event.keyCode == 37) {
        previous_script();
    }
};

$(document).ready(function() {
    if (window.location.hash){
        current_script = parseInt(window.location.hash.substr(1))-1;
    }
    
    $(document).keydown(handle_keypress);
    $("#fullscreen").click(toggleFullScreen);
    
    $("#next").click(next_script);
    $("#previous").click(previous_script);
    $("#code-examples").change(function(){
        var select = $(this);
        load_script(parseInt(select.val()));
    });
    
    reload_index();
    reload_css_index();
    
    $("#syntax-styles").change(function(){
        change_highlight($(this).val());
        $(this).blur();
    });
});