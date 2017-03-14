$(document).ready(function () {
    $('.add-tag').on('click', function (e) {
        e.preventDefault();
        var count = $('#tag-list').children().length;
        $('#id_form-TOTAL_FORMS').attr('value', count);
        var tag_form = $('<div class="tag-form"></div>');
        var delete_button = $('<span class="glyphicon glyphicon-remove delete-tag"></span>');
        var label = $('<label for="id_form-' + count + '-tag">Tag:</label>');
        var input = $('<input id="id_form-' + count + '-tag" maxlength="25" name="form-' + count + '-tag" type="text">');
        var input_2 = $('<input id="id_form-' + count + '-id" name="form-' + count + '-id" type="hidden">');
        $('#tag-list').append(tag_form.append(delete_button).append(label).append(input).append(input_2));
    });

    $(document).on('click', '.delete-tag', function (e) {
        e.preventDefault();
        $(this).parent().hide();
    })
});
