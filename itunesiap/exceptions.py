from .utils import force_unicode


class ItunesException(Exception):

    def __init__(self, *messages):
        msg = u'\n'.join(map(force_unicode, messages))
        super(ItunesException, self).__init__(msg)


class ConnectionError(ItunesException):
    pass


class RequestError(ItunesException):
    pass


class ItunesNotAvailable(RequestError):
    pass


class InvalidReceipt(RequestError):
    codes = {
        21000: 'The App Store could not read the JSON object you provided.',
        21002: 'The data in the receipt-data property was malformed.',
        21003: 'The receipt could not be authenticated.',
        21004: 'The shared secret you provided does not match the shared secret on file for your account.',
        21005: 'The receipt server is not currently available.',
        21006: 'This receipt is valid but the subscription has expired. When this status code is returned to your server, the receipt data is also decoded and returned as part of the response.',
        21007: 'This receipt is a sandbox receipt, but it was sent to the production service for verification.',
        21008: 'This receipt is a production receipt, but it was sent to the sandbox service for verification.',
    }

    def __init__(self, *args, status=None):
        try:
            description = self.codes[status]
        except KeyError:
            pass
        else:
            self.status = status
            args = ('{}: {}'.format(status, description),) + args

        super(InvalidReceipt, self).__init__(*args)
