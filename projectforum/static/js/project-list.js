$(document).ready(function() {

    // JQuery code to be added in here.
    $('.search').click(function() {
        var url = window.location.href;
        var filters = $('.keywords').val();
        var sorting = parseInt($('.sort-projects').val());
        var queryloc = url.indexOf('?');
        var ascending;
        var salary = '';
        if (queryloc > -1) {
            url = url.substring(0, queryloc);
        }
        if (filters !== '') {
            url += '?keywords=' + filters.replace(' ', ',');
        } else {
            url += '?';
        }

        if (sorting % 2 === 1) {
            ascending = 0;
        } else {
            ascending = 1;
        }
        switch(sorting) {
            case 3:
            case 4:
                query_type = 'payment';
                salary = 'lump';
                break;
            case 5:
            case 6:
                query_type = 'payment';
                salary = 'hourly';
                break;
            case 7:
            case 8:
                query_type = 'title';
                break;
            default:
                query_type = 'timestamp';
                break;
        }
        url += '&order=' + query_type;
        url += '&ascending=' + ascending;
        if (salary !== '') {
            url += '&salary=' + salary;
        }
        window.location.href = url;
    });

    $('.new_page').on('click', function() {
        console.log("BOOM");
        var url = window.location.href;
        var page;
        page = $(this).attr("page");
        if (url.indexOf('?') > -1) {
            url += '?page=' + page;
        } else {
            url += '&page=' + page;
        }
        window.location.href = url;
    });
});