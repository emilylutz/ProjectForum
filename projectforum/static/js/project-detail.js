

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

});