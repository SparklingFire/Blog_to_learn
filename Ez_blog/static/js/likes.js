$(document).ready(function () {
  $(document).on('click', '.like', function (e) {
      e.preventDefault();
      var url = $(this).parent().attr('href');
      var likes = $(this).closest('.panel-footer').find('.total-likes');
      var dislikes = $(this).closest('.panel-footer').find('.total-dislikes');
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
