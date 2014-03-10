function s4() {
  return Math.floor((1 + Math.random()) * 0x10000)
             .toString(16)
             .substring(1);
};

function guid() {
  return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         s4() + '-' + s4() + s4() + s4();
}

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
      $(this).val('');
    }
  });

  console.log(fields);

  var account_id = $('#account_id').val();
  var account_key = $('#account_key').val();
  var headers = {};
  if (account_id && account_key) {
    headers['X-PITA-ACCOUNT-ID'] = account_id;
    headers['X-PITA-SECRET'] = account_key;
  }

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
    complete: completion_handler,
    headers: headers
  });
  console.log('Hitting endpoint: ' + form.method.toUpperCase() + ' ' + endpoint_location);
}

$(document).ready(function(e) {
  $('.endpoint form').submit(function(e) {
    e.preventDefault();
    hit_endpoint(this);
  });
  $('#accounts-uuid').val(guid());
});
