function subscription_counter(data) {
    $('.sub-counter').html('Подписки ( ' + data + ' )');
}


$(document).ready(function () {
    $('.subscribe').on('click', function (e) {
        e.preventDefault();
        var url = $(this).find('a').attr('href');
        var article_url = $(location).attr('pathname');
        $.ajax({
            type: 'GET',
            url: url,
            dataType: 'json',
            success: function (response) {
                $('.subscribe').find('a').html(response.message);
                if (response.message === 'Отписаться'){
                    var subscription = $('<div class="subscription" data-pk="' + response.sub_id + '"></div>');
                    var subscription_delete = $('<a class="subscription-delete" href="/delete_subscription/' +
                        response.sub_id + '/"><small><span class="glyphicon glyphicon-remove"></span></small></a>');
                    var subscription_link = $('<a href="' + article_url + '">' + response.article + '</a>');

                    subscription.append(subscription_delete).append(subscription_link).append(' ( 0 )');
                    $('#subscription-list').append(subscription);
                }
                else{
                    $('.subscription[data-pk=' + response.sub_id + ']').remove();
                }
                return subscription_counter(response.sub_counter);
            }
            }
        )
    });

    $(document).on('click', '.subscription-delete', function (e) {
        e.preventDefault();
        var url = $(this).parent().find('.subscription-delete').attr('href');
        $(this).parent().remove();
        $.ajax({type: 'GET',
                url: url,
                dataType: 'json',
                success: function (response) {
                    if ($('.article-details').data('obj') == response.pk){
                        $('.subscribe').find('a').html(response.message);
                    }
                    return subscription_counter(response.sub_counter);
                },
                error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);}})
    });

    $('.sub-counter').on('click', function (e) {
        e.preventDefault();
        $('#subscription-list').slideToggle();
    });
});
