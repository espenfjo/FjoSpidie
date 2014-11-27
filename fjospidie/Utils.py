"""
Various helper function used by several methods or classes
"""

import hashlib

def get_md5(data):
    """
    Get the MD5sum of the passed data
    """
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()
