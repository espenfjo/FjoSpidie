"""
Various helper function used by several methods or classes
"""

import logging
import hashlib
import threading
import pygeoip
import dns.resolver
import os

def get_md5(data):
    """
    Get the MD5sum of the passed data
    """
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()
