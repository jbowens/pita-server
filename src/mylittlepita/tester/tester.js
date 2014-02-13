/*
 * Takes a form DOM object and hits the endpoint the form
 * is setup to hit.
 */
function hit_endpoint(form) {
  // Determine the url of the endpoint we're hitting.
  var action = form.action.indexOf('file://') != -1 ? form.action.substr('file://'.length) : form.action;
  var endpoint_location = action;

  // Gather all the fields and their values
  var $inputs = $(form).find(':input');
  var fields = {};
  $inputs.each(function() {
    if (this.name && this.name != '') {
      fields[this.name] = $(this).val();
    }
  });

  var completion_handler = function(resp, http_status) {
    var endpoint_cont = $(form).closest('.endpoint');
    $(endpoint_cont).find('.status_code .code').text(http_status);
    if (resp.responseJSON) {
      // We got json back. Prettify it before displaying it.
      var pretty = JSON.stringify(resp.responseJSON, undefined, 2);
      $(endpoint_cont).find('.endpoint-response pre').text(pretty);
    } else {
      $(endpoint_cont).find('.endpoint-response pre').text(resp.responseText);
    }
  };

  $.ajax(endpoint_location, {
    type: form.method,
    data: fields,
    complete: completion_handler
  });
  console.log('Hitting endpoint: ' + form.method.toUpperCase() + ' ' + endpoint_location);
}



$(document).ready(function(e) {
  $('.endpoint form').submit(function(e) {
    e.preventDefault();
    hit_endpoint(this);
  });
});