function display_form_errors(error) {
    for (var e in error){
        $('#errors-list').prepend(error[e]).fadeIn();
    }
}

$(document).ready(function (e) {
    var url = $(location).attr('pathname');
    $(document).on('click', '.answer-submit', function (e) {
        e.preventDefault();
        var form = $(this).parent();
        $.ajax({type: 'POST',
                url: url,
                data: form.serialize(),
                dataType: 'json',
                success: function (response) {
                    $('#errors-list').empty();
                    if ('error' in response){
                        display_form_errors(response.error())
                    }
                    else{
                        var date = new Date(response.datetime);

                        var panel_default = $('<div class="panel panel-default article-details" data-id=' +
                                                response.comment_pk + '></div>');

                        var panel_heading = $('<div class="panel-heading" data-id=' + response.rating_model_pk + '>Аноним ' +
                                               response.comment_name + ' ' +  date.toLocaleString() + '</div>');

                        var panel_body = $('<div class="panel-body">' + response.comment_text + '</div>');

                        var panel_footer = $('<div class="panel-footer">' +
                                             '<a href="/rate/' + response.rating_model_pk + '/like/">' +
                                             '<span class="glyphicon glyphicon-thumbs-up like" data-grade="like">' +
                                             '</span></a><span class="total-likes"> 0 </span>' +
                                             '<a href="/rate/' + response.rating_model_pk + '/dislike/">' +
                                             '<span class="glyphicon glyphicon-thumbs-down like" data-grade="dislike">' +
                                             '</span></a><span class="total-dislikes"> 0 </span>' +
                                             '</div>');

                        var answer_button = $('<div class="comment-answer">Ответить</div>');

                        if (response.auth_user == true){
                            var delete_comment = $('<div class="delete-comment"><a href="/comment/delete/' +
                                                    response.comment_pk +
                                                   '"><span class="glyphicon glyphicon-remove"></span></a></div>');
                            panel_heading.append(delete_comment);
                        }

                        var new_comment = panel_default.append(panel_heading)
                                                       .append(panel_body)
                                                       .append(panel_footer)
                                                       .append(answer_button);

                        $('#comments-list').append(new_comment);
                        $('body, html').animate({ scrollTop: $(new_comment).offset().top }, 1000);
                        form.trigger('reset');
                    }
                },
                error: function (xhr, errmsg, err) {
                    alert(xhr.status + ": " + xhr.responseText);
                }
        })
    });

    $(document).on('click', '.delete-comment', function (e) {
        e.preventDefault();
        var url = $(this).find('a:first').attr('href');
        var comment = $(this).closest('.panel-default');
        $.ajax({type: 'GET',
                url: url,
                dataType: 'json',
                success: function (response) {
                    comment.remove();
                    },
                error: function (xhr, errmsg, err) {
                    alert(xhr.status + ": " + xhr.responseText);
                    }
        })
    });

    $(document).on('click', '.comment-answer', function (e) {
        e.preventDefault();
        var new_form = $('#answer-form').clone(true).appendTo($(this).parent());
        new_form.find('.parent').val($(this).parent().attr('id'));
        $(this).attr('class', 'comment-answer-close');
        $(this).html('Закрыть');
    });

    $(document).on('click', '.comment-answer-close', function (e) {
        e.preventDefault();
        $(this).attr('class', 'comment-answer');
        $(this).html('Ответить');
        $(this).parent().find('#answer-form').remove();
    })
});
