

$(document).ready(function() {

    // JQuery code to be added in here.
    $('.accept_applicant').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");
        var applicantusername;
        applicantusername = $(this).attr("data-applicantusername");

        $.get('/project/'+projectid+'/accept_applicant/'+applicantusername, function(data){
                    location.reload();
                });
    });

    $('#apply_button').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");

        $.get('/project/'+projectid+'/apply/', function(data){
                    location.reload();
                });
    });

    $('#withdraw_application_button').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");

        $.get('/project/'+projectid+'/withdraw_application/', function(data){
                    location.reload();
                });
    });

    $('#mark_complete').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");

        $.get('/project/'+projectid+'/mark_complete/', function(data){
                    location.reload();
                });
    });

    $('#cancel_project').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");

        $.get('/project/'+projectid+'/cancel_project/', function(data){
                    location.reload();
                });
    });

    $('#reopen_project').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");

        $.get('/project/'+projectid+'/reopen_project/', function(data){
                    location.reload();
                });
    });

    $('#reopen_applications').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");

        $.get('/project/'+projectid+'/reopen_applications/', function(data){
                    location.reload();
                });
    });

    $('#close_applications').click(function(){
        var projectid;
        projectid = $(this).attr("data-projectid");

        $.get('/project/'+projectid+'/close_applications/', function(data){
                    location.reload();
                });
    });

    function addBookmark () {
        var projectid;
        projectid = $(this).attr("data-projectid");
        $.get('/project/'+projectid+'/bookmark_add/', function(data){
            $('a#projectBookmark')
                .addClass('active')
                .attr('title','Remove from bookmarks')
                .unbind('click')
                .bind('click', removeBookmark);
                });

    }

    function removeBookmark () {
        var projectid;
        projectid = $(this).attr("data-projectid");
        $.get('/project/'+projectid+'/bookmark_remove/', function(data){
            $('a#projectBookmark')
                .removeClass('active')
                .attr('title','Bookmark this project')
                .unbind('click')
                .bind('click', addBookmark);
            });
    }

    if ($('a#projectBookmark').hasClass('active')) {
        $('a#projectBookmark').bind('click', removeBookmark)
    } else {
        $('a#projectBookmark').bind('click', addBookmark)
    }

    $('#projectReviewForm').validate({
        ignore: [],
        rules:{
            score:{
                required: true,
            },
            comment: {
                required: true,
           }
        },
        messages:{
            score:{
                required: "Please enter in a score greater than 0.",
            },
            comment: {
                required: "Please enter a comment",
            }
        }
    });

    $('.reviewEditable').on('click', function(event) {
        var review = $(this).parent()[0];
        reviewid = $(review).attr("data-reviewid");
        var oldText = $(review).find('.review-comment').html();
        var editTextArea = $('<textarea />');
        editTextArea.val(oldText);
        $(review).find('.review-comment').replaceWith(editTextArea);
        var old_score = $(review).find('.review-score').attr('data-score');
        $(review).find('.review-score').replaceWith('<div class="editRating"></div>');
        $('.editRating').raty({
            score: old_score,
            path:'/static/external/jqueryraty/images',
        });
        $(this).text('Submit');
        $(this).unbind('click');
        $(this).bind('click', submitEdit)
    });

    function submitEdit() {
        var review = $(this).parent()[0];
        var reviewid = $(review).attr("data-reviewid");
        rating_score =  $(review).find('input[type=hidden]').val();
        rating_comment = $(review).find('textarea').val();
        if (rating_comment == "") {
            return false;
        }
        post_data = {
            score : rating_score,
            comment: rating_comment,
        };
        $.post('/ratings/review/edit/' + reviewid, post_data, function(data) {
            location.reload();
        });
    }

});