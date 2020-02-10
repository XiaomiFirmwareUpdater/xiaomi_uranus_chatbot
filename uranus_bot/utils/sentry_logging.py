""" sentry log options """


def sentry_before_send(event, hint):
    """ Filter exceptions before reporting with sentry """
    # pylint: disable=unused-variable
    # pylint: disable=invalid-name
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, KeyboardInterrupt):
            return None
    return event
