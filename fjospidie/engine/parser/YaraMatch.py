class YaraMatch(object):
    def __init__(self, match):
        self.description = ''
        if match.meta['description']:
            self.description = match.meta['description']
        self.rule = match.rule
        self.tags = match.tags
