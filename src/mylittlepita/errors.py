from flask import jsonify

def user_error(msg):
    """
    Should be called to return an api error response when the error
    is clearly caused by the user. For example, the user provided
    a phone number that was already in use.
    """
    # TODO: Logging still might be useful here to see how users
    # are fucking up.
    return jsonify(user_error=True, error_message=msg), 400

def api_error(msg):
    """
    Should be called to return a default api error response. This
    should be used when the client is not making valid requests,
    for whatever reason.
    """
    # TODO: Add logging of API errors. Our iOS client *should* be
    # the only client, so this *should* be indicative of an error
    # in our client. Could also be 1337 haxxors.
    return jsonify(user_error=False, error_message=msg), 400

