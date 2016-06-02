(function(global) {
    'use strict';
    global.document.onreadystatechange = function() {
        if (document.readyState === 'complete') {
            $("#main").removeClass("ui loading tab");
        }
    }

    $(function() {

    });
})(typeof window === 'undefined' ? this : window);
