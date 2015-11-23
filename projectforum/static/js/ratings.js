$(document).ready(function() {

    $(".review-score").raty({
        score: function() {
            return $(this).attr('data-score');
        },
        readOnly: true,
        path:'/static/external/jqueryraty/images',
    });

    $("#rating").raty({
            path:'/static/external/jqueryraty/images',
        });

    $('#projectReviewDropdown').live('change', function(event) {
        $.get('/ratings/', function (data) {
            // body...
        })
        $.getJSON($(this).val(), function(snippets) {
            for(var id in snippets) {
                // updated to deal with any type of HTML
                jQuery('#' + id).html(snippets[id]);
            }
        });
    });
});