import logging
from HTTPEntry import HTTPEntry
from HTTPHeader import HTTPHeader


class HTTPEntries:
    def __init__(self, entries, database):
        self.entries = []
        for idx, entry in enumerate(entries):
            self.entries.append(HTTPEntry(entry, idx, database))

