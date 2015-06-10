jQuery(document).ready(function ($) {
  $('#filterbox').on('keyup', function () {
    $.each($('.show'), function( key, value ) {
      if (this.getAttribute('data-show').toLowerCase().indexOf($('#filterbox').val().toLowerCase()) >= 0) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
    $.each($('.episode'), function( key, value ) {
      if (this.getAttribute('data-episode').toLowerCase().indexOf($('#filterbox').val().toLowerCase()) >= 0) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });
});
