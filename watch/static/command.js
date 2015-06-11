jQuery(document).ready(function ($) {
  function command(cmd){
    $.ajax({
      url: "/command/" + cmd,
      type: "GET",
      success: function() {
        console.log("Successfully called command: " + cmd)
      }
    });
  };
  $('#pause-button').on('click', function(event){
    command('pause');
  });
  $('#stop-button').on('click', function(event){
    command('stop');
  });
  $('#nextchapter-button').on('click', function(event){
    command('nextchapter');
  });
  $('#prevchapter-button').on('click', function(event){
    command('prevchapter');
  });
});
