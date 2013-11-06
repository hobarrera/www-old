$(function() {
    $('nav a').on('mouseover', function() {
        $(this).css({
            'border-bottom': '1px dotted'
        });
    });
    $('nav a').on('mouseleave', function() {
        $(this).css({
            'border-bottom': '0px none'
        });
    });
});