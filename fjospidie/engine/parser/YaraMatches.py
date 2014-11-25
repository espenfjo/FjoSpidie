from YaraMatch import YaraMatch
class YaraMatches(object):
    def __init__(self, matches):
        self.matches = []
        self._type = "yara"
        for match in matches:
            self.matches.append(YaraMatch(match))
