$(document).ready(function () {
    $('.subscribe').on('click', function (e) {
        e.preventDefault();
        var url = $(this).find('a').attr('href');
        $.ajax({type: 'GET',
                url: url,
                dataType: 'json',
                success: function (response) {
                    $('.subscribe').find('a').html(response.message);
                    if ($('.subscription-delete[data-pk=' + response.sub_id + ']').length == 0){

                        var delete_button =  $('<p class="subscription-delete" data-pk=' + response.sub_id +
                                           '><a href="/delete_subscription/' +
                                            response.sub_id + '/"><span class="glyphicon glyphicon-remove">');
                        var link = $('</span></a><a href="' + response.sub_url + '">' + response.article + '</a>');

                        delete_button.append(link);
                        $('#subscription-list').append(delete_button)}
                    else {
                        $('.subscription-delete[data-pk=' + response.sub_id + ']').remove();
                    }
                    },
                error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);}})
    });
    
    $('body').on('click', '.subscription-delete', function (e) {
        e.preventDefault();
        var url = $(this).find('a').attr('href');
        $(this).remove();
        $.ajax({type: 'GET',
                url: url,
                dataType: 'json',
                success: function (response) {
                    if ($('.article-details').data('obj') == response.pk){
                        $('.subscribe').find('a').html(response.message);
                    }

                },
                error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);}})
    });
});
