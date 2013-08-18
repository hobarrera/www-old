function adjustBoxes() {
    group = $("div.box");
    group.css("height", "auto");

    // If they're floating boxes, make them the same height
    if ($("div.box:first").css('float') == "left") {
        var height = 0;
        group.each(function() {
            var currentHeight = $(this).height();
            if(currentHeight > height) {
                height = currentHeight;
            }
        });
        group.height(height);
    }
}

$(document).ready(function() {
    adjustBoxes();
});
$(window).resize(function() {
    adjustBoxes();
});