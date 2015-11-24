$(document).ready(function() {

    var preload_dropdowns = function() {
        var parseQueryString = function() {

            var str = window.location.search;
            var objURL = {};

            str.replace(
                new RegExp( "([^?=&]+)(=([^&]*))?", "g" ),
                function( $0, $1, $2, $3 ){
                    objURL[ $1 ] = $3;
                }
            );
            return objURL;
        };

        var params = parseQueryString();
        var sort_projects;
        try {
            sort_projects = parseInt(params["sort-projects"]);
            if (sort_projects > 8 || sort_projects < 0) {
                sort_projects = 0;
            }
        } catch(err) {
        }
        try {
            status = parseInt(params["status"]);
            if (status > 4 || status < 0) {
                status = 0;
            }
        } catch(err) {
        }
        if (isNaN(sort_projects)) {
            sort_projects = 0;
        }
        if (isNaN(status)) {
            status = 0;
        }
        $("#sort-projects").val(sort_projects);
        $("#status").val(status);
    };
    preload_dropdowns();

    $('.project-list-description').ellipsis();

    $('#button-search').click(function() {
        var url = window.location.href,
            filters = $('#keywords').val(),
            sorting = parseInt($('#sort-projects').val()),
            queryloc = url.indexOf('?'),
            ascending,
            salary = '',
            status = parseInt($('#status').val());
        // Because I'm making a new search, remove previous query vars
        if (queryloc > -1) {
            url = url.substring(0, queryloc);
        }
        // Add in the keywords or just parameter mark depending
        if (filters !== '') {
            url += '?keywords=' + filters.replace(' ', ',');
        } else {
            url += '?';
        }

        // Oddness will determine whether ascend is True or False
        if (sorting % 2 === 1) {
            ascending = 0;
        } else {
            ascending = 1;
        }
        // Interpret input (number) to determine how I'm sorting
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
        url += '&order=' + query_type + '&ascending=' + ascending;
        url += '&status=' + status + '&sort-projects=' + sorting;
        if (salary !== '') {
            url += '&salary=' + salary;
        }
        window.location.href = url;
    });

    $('.new-page').click(function() {
        var url = window.location.href;
        var page = $(this).attr("data-pageid");

        url = update(url, 'page', page);

        window.location.href = url;
    });

    var update = function updateQueryStringParameter(uri, key, value) {
        var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
        var separator = uri.indexOf('?') !== -1 ? "&" : "?";
        if (uri.match(re)) {
            return uri.replace(re, '$1' + key + "=" + value + '$2');
        }
        else {
            return uri + separator + key + "=" + value;
        }
    };

});
