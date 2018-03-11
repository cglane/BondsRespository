

(function($) {
    $(document).ready(function() {
        var printHtml = function (html, css, callback) {
            var hiddenFrame = $('<iframe style="display: none"></iframe>').appendTo('body')[0];
            hiddenFrame.contentWindow.printAndRemove = function() {
                hiddenFrame.contentWindow.print();
                $(hiddenFrame).remove();
                callback()
            };
            var htmlDocument = "<!doctype html>"+
                        "<html>"+
                        "<head>"+
                            css 
                            +
                        "</head>" +
                            '<body onload="printAndRemove();">' + // Print only after document is loaded
                                html +
                            '</body>'+
                        "</html>";
            var doc = hiddenFrame.contentWindow.document.open("text/html", "replace");
            doc.write(htmlDocument);
            doc.close();
        };
        $("#print-submit").click( function(e){
            var bondId = $('#bond-id-input').val()
            var cssLink = $('#page-css').val()
            var hostname = window.location.host
            var html = jQuery('#print-bond-wrapper').html()
            var myLink = '<link rel="stylesheet" href='+cssLink+' />';

            printHtml(html, myLink, function() {
                $('#print-bond-form').submit()
            })
        })
    })
    
})(django.jQuery);