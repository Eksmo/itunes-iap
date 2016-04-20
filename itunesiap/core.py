import json
import contextlib

import requests

from . import exceptions


RECEIPT_PRODUCTION_VALIDATION_URL = "https://buy.itunes.apple.com/verifyReceipt"
RECEIPT_SANDBOX_VALIDATION_URL = "https://sandbox.itunes.apple.com/verifyReceipt"


class Request(object):
    """Validation request with raw receipt. Receipt must be base64 encoded string.
    Use `verify` method to try verification and get Receipt or exception.
    """

    def __init__(self, receipt, password=None, **kwargs):
        self.receipt = receipt
        self.password = password
        self.use_production = kwargs.get('use_production', True)
        self.use_sandbox = kwargs.get('use_sandbox', False)
        self.timeout = kwargs.get('timeout')

    def __repr__(self):
        return u'<Request(data:{}...)>'.format(self.receipt[:20])

    def verify_from(self, url):
        """
        Attempt to verify the receipt against given url.
        """
        payload = {
            'receipt-data': self.receipt
        }
        if self.password:
            payload['password'] = self.password

        try:
            response = requests.post(url, json.dumps(payload), timeout=self.timeout, verify=True)
        except requests.RequestException as e:
            raise exceptions.ConnectionError('failed to request %s: %s' % (url, e))

        if response.status_code != 200:
            raise exceptions.ItunesNotAvailable(response.status_code, response.content)

        try:
            result = json.loads(response.content.decode('utf-8'))
            status = result['status']
        except (KeyError, ValueError):
            raise exceptions.ItunesNotAvailable('invalid response', response.content)

        if status not in (0, 21006):  # ignore expired ios6 receipts
            raise exceptions.InvalidReceipt(result.get('receipt'), status=status)

        return result

    def verify(self):
        """Try verification with settings. Returns a Receipt object if successed.
        Or raise an exception. See `self.response` or `self.result` to see details.
        """
        receipt = None
        exc = None

        if not (self.use_production or self.use_sandbox):
            raise TypeError('use_production=%s use_sandbox=%s' % (self.use_production, self.use_sandbox))

        if self.use_production:
            try:
                receipt = self.verify_from(RECEIPT_PRODUCTION_VALIDATION_URL)
            except exceptions.InvalidReceipt as e:
                exc = e

        if self.use_sandbox:
            try:
                receipt = self.verify_from(RECEIPT_SANDBOX_VALIDATION_URL)
            except exceptions.InvalidReceipt as e:
                exc = e

        if receipt:
            return Receipt(receipt)

        raise exc

    @contextlib.contextmanager
    def verification_mode(self, use_production=None, use_sandbox=None):
        restore = self.use_production, self.use_sandbox
        if use_production is not None:
            self.use_production = use_production
        if use_sandbox is not None:
            self.use_sandbox = use_sandbox
        yield
        self.use_production, self.use_sandbox = restore


class Receipt(dict):
    """
    dict like interface for decoded receipt obejct.
    """
    def __init__(self, data):
        self.data = data
        self.status = data['status']
        dict.__init__(self, data['receipt'])

    def __repr__(self):
        repr = super(Receipt, self).__repr__()
        return u'<Receipt(status:{0}, {1})>'.format(self.status, repr)
