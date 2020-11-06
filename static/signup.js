
$('#passcode, #confirm_passcode').on('keyup', function () {
    if ($('#passcode').val() == $('#confirm_passcode').val()) {
      $('#message').html('Matching').css('color', 'green');
    } else 
      $('#message').html('Not Matching').css('color', 'red');
  });