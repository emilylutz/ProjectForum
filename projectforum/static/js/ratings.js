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

    $('input[name="score"]').attr('required', true);

    $('#projectReviewForm').validate({
        ignore: [],
        rules:{
            score:{
                min:1,
            },
            comment: {
                required: true,
           }
        },
        messages:{
            score:{
                min: "Please enter in a score greater than 0.",
            },
            comment: {
                required: "Please enter a comment",
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