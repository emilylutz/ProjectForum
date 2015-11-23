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

    $('#projectReviewForm').on('submit', function(event)) {
        if ($(this).find())
    }

    $('#projectReviewForm').validate({
       rules:{
           score:{
              min:1,
           }
       },
       messages:{
           score:{
              min: "Please enter in a score greater than 0.",
            }
       }
    })



    // $('#projectReviewDropdown').on('change', function(event) {
    //     var projectId = $(this).attr('data-projectid');
    //     var username = $(this).val();
    //     $.get('/ratings/review/' + projectId + '/' + username, function (data) {
    //         // body...
    //     });
    // });
});