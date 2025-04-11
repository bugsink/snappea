import traceback

try:
    # optional dependency: sentry_sdk. To send stuff to **Bugsink** (hopefully) when an exception occurs.
    import sentry_sdk
    sentry_sdk_is_initialized = lambda: sentry_sdk.is_initialized()  # noqa: E731
    capture_exception = sentry_sdk.capture_exception
except ImportError:
    sentry_sdk_is_initialized = lambda: False  # noqa: E731

    def capture_exception(e):
        pass


def capture_or_log_exception(e, logger):
    try:
        if sentry_sdk_is_initialized():
            capture_exception(e)
        else:
            # this gnarly approach makes it so that the logger prefixes (e.g. snappea task number, dates etc) are shown
            # for each of the lines of the traceback (though it has the disadvantage of time not standing still while
            # we iterate in the loop).
            #
            # the 3-argument signature is needed for Python 3.9 (in Python 3.10 and up .format_exception(e) is enough).
            # https://docs.python.org/3.10/library/traceback.html#traceback.print_exception
            # > If value and tb are provided, the first argument is ignored in order to provide backwards compatibility.
            for bunch_of_lines in traceback.format_exception(type(e), e, e.__traceback__):
                for line in bunch_of_lines.splitlines():
                    # Note: when .is_initialized() is True, .error is spammy (it gets captured) but we don't have that
                    # problem in this branch.
                    logger.error(line)
    except Exception as e2:
        # We just never want our error-handling code to be the cause of an error.
        print("Error in capture_or_log_exception", str(e2), "during handling of", str(e))
