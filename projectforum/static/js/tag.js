var Tag = (function() {
    var getTagsWithText = function(tags_input, text) {
        return tags_input
            .children()
            .filter(function () {
                return $(this).html() == text;
            });
    };

    var start = function(tagLabelId, tagDivId, maxLength) {
        maxLength = maxLength || 100;

        var tags_input = $('#' + tagLabelId);
        tags_input.hide();

        var initial_tags = tags_input.children().map(function(){
           return $.trim($(this).text());
        }).get();

        var tokenfield = $('#' + tagDivId).tokenfield();
        tokenfield.tokenfield('setTokens', initial_tags);
        tokenfield
            .on('tokenfield:createtoken', function (e) {
                var tag = e.attrs.label;
                if (tag.length > maxLength) {
                    return;
                }
                tags_input.append('<option selected="selected">' + tag
                    + '</option>');
            })
            .on('tokenfield:createdtoken', function (e) {
                var tag = e.attrs.label;
                if (tag.length > maxLength
                    || getTagsWithText(tags_input, tag).length > 1) {
                    $(e.relatedTarget).addClass('invalid');
                }
            })
            .on('tokenfield:edittoken', function (e) {
                var tag = e.attrs.label;
                if (tag.length > maxLength) {
                    return;
                }
                var same = getTagsWithText(tags_input, tag);
                if (same.length == 2) {
                    tokenfield
                        .siblings()
                        .find("span:contains('" + tag + "')")
                        .parent('.invalid')
                        .removeClass('invalid');
                }
                same.last().remove();
            })
            .on('tokenfield:removedtoken', function (e) {
                var tag = e.attrs.label;
                if (tag.length > maxLength) {
                    return;
                }
                var same = getTagsWithText(tags_input, tag);
                if (same.length == 2) {
                    tokenfield
                        .siblings()
                        .find("span:contains('" + tag + "')")
                        .parent('.invalid')
                        .removeClass('invalid');
                }
                same.last().remove();
            });
        return {
            tokenfield: tokenfield,
            tags_input: tags_input,
        };
    }

    var link = function(tagfield, optionInputSelector) {
        $('#' + optionInputSelector).change(function() {
            tokens = tagfield.tokenfield.tokenfield('getTokens', false)
                                        .map(function(x) {
                                            return x.value
                                        });
            value = $(this).val();
            if ($(this).is(":checked")) {
                if (getTagsWithText(tagfield.tags_input, value).length == 0) {
                    tokens.push(value);
                }
            } else {
                tokens = tokens.filter(function(x) {
                    return x != value;
                });
            }
            tagfield.tags_input.empty()
            tagfield.tokenfield.tokenfield('setTokens', tokens);
        });
    }

    return {
        start: start,
        link: link,
    };
})();
