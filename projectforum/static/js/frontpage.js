$(document).ready(function() {

    $('.list-content').click(function(){
        window.location='/project/list';
    });

    $('.create-content').click(function(){
        window.location='/project/create';
    });

    $('.signup-button').click(function(){
        window.location='/profile/register/';
    });
});