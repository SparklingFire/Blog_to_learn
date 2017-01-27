$(document).ready(function () {
  $('.like').on('click', function (e) {
      e.preventDefault();
      var url = '/rate/' + $(this).closest('.article-details').data('id') + '/' + $(this).data('grade');
      var likes = $(this).closest('.article-details').find('.total-likes');
      var dislikes = $(this).closest('.article-details').find('.total-dislikes');
      $.ajax({type: 'GET',
              url: url,
              dataType: 'json',
              success: function(response){
                  likes.html(response.likes);
                  dislikes.html(response.dislikes);
              },
              error: function (xhr, errmsg, err) {
                alert(xhr.status + ": " + xhr.responseText);}
      });
  })
});
