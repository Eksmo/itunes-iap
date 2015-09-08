"""
    itunes-iap
    ~~~~~~~~~~

    Itunes In-app Purchase verification api.

    :copyright: (c) 2013 Jeong YunWon - 2014 Andy Briggs
    :license: 2-clause BSD.
"""
from pkg_resources import get_distribution, DistributionNotFound

from .core import Request, Receipt
from .exceptions import InvalidReceipt, RequestError
from .shortcut import verify


try:
    VERSION = tuple(map(int, get_distribution('itunesiap').version.split('.')))
except DistributionNotFound:
    VERSION = None
