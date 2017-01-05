lastHighlighted = null;
bg_colors = ['#CE215B', '#E1A83E', '#71C3CA', '#39AE85']
colors = bg_colors.length
color_map = {};

function onBlur(el) {
    if (el.value == '') {
        el.value = 'http://www.';
    }
}

function onFocus(el) {
    if (el.value == el.defaultValue) {
        el.value = 'http://www.';
    }
}

// Alert user of failure
function handleFailedLoad() {
    alert("We had a problem getting the data from the site you specificed... Are there other websites you are interested in?");
}

// Function to handle highlighting of tags
function highlightButtonClicked() {
    // Get the type of tag from the id
    var id = $(this).attr('id');
    var tag = id.substring(0,id.length-3);

    // Get the appropriate class names for all of the tags
    var start_class_name = '.type-start-'+tag;
    var end_class_name = '.type-end-'+tag;

    // If tag was previously highlighted, unhighlight it
    if(lastHighlighted == tag) {
       $('.type-start-'+lastHighlighted).each(function(){
            $(this).css('background-color', 'rgba(0,0,0,0)');
        });
        $('.type-end-'+lastHighlighted).each(function(){
            $(this).css('background-color', 'rgba(0,0,0,0)');
        }); 
        lastHighlighted = null;
        return;
    }

    // If there was a previously highlighted tag, unhighlight it
    if(lastHighlighted != null) {
        $('.type-start-'+lastHighlighted).each(function(){
            $(this).css('background-color', 'rgba(0,0,0,0)');
        });
        $('.type-end-'+lastHighlighted).each(function(){
            $(this).css('background-color', 'rgba(0,0,0,0)');
        });
    }

    // Highlight the new tag
    $(start_class_name).each(function() {
        $(this).css('background-color', color_map[tag]);
    });
    $(end_class_name).each(function() {
        $(this).css('background-color', color_map[tag]);
    });

    // Remember which tag was just highlighted
    lastHighlighted = tag;
}

// Ensure that page has loaded
$(function(){
    // For catching the enter key
    $('.url-input').keyup(function(event) {
        // If enter key hit
        if(event.which == 13) {
            // Attempt to get data from server
            $.post( "/getHTML/", $('form').serialize(), function(data , success) {
                if(success == 'success') {
                    if (data['success'] == true) {
                        // Wipe data, in case of two or more lookups
                        $('.source-viewer').html('');
                        $('.tag-list').html('');

                        // Load the html into the source viewer
                        $('.source-viewer').html(data['html']);

                        // Populate the tag list in sorted order
                        sorted = data.stats.sort(function(a,b){
                            return b[1] - a[1];
                        });
                        for(var i =0; i < sorted.length; i++)
                        {
                            $('.tag-list').append(
                                '<tr id = \'' + sorted[i][0] + '-id\' class = \'one-tag\'> ' 
                                + '<td class = \'tag-button\' ' + sorted[i][0] + '\'>' + sorted[i][0] + '</td>'
                                + '<td><div class=\'tag-count\'>' + sorted[i][1] + '</div></td>'
                                + '</tr>');


                            // Set and stored color for highlighting
                            $('.tag-count').last().css('background-color', bg_colors[i%colors]);
                            color_map[sorted[i][0]] = bg_colors[i%colors];
                        }

                        // Set up the highlighting on tag click
                        $('.one-tag').each(function(){
                            $(this).click(highlightButtonClicked);
                        });

                    } else {
                        // Notify the user if there was an issue
                        handleFailedLoad();
                    }
                } else {
                    // Notify the user is there was an issue
                    handleFailedLoad();
                }
            })
        }

        // Standardize the input format
        var val = $('.url-input').val()
        $('.url-input').val('http://www.' + val.substring(11,val.length));

    }).keydown(function(event) {
        // Prevent page reload
        if(event.which == 13) {
            event.preventDefault();
        }
    });
})
