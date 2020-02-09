""" sentry log options """


def sentry_before_send(event, hint):
    """ Filter exceptions before reporting with sentry """
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, KeyboardInterrupt):
            return None
    return event
