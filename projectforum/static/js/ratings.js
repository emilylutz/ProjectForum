$(document).ready(function() {

    $(".review-score").raty({
        score: function() {
            return $(this).attr('data-score');
        },
        readOnly: true,
        path:'/static/external/jqueryraty/images',
    });

    $(".average-score").raty({
        score: function() {
            return $(this).attr('data-score');
        },
        halfShow: true,
        readOnly: true,
        path:'/static/external/jqueryraty/images',
    });

    $("#rating").raty({
            path:'/static/external/jqueryraty/images',
    });

});