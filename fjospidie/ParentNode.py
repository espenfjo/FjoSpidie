from Node import Node


class ParentNode(Node):

    def __init__(self, hostname):
        super(ParentNode, self).__init__(hostname)
        self.number_of_links = 1

    def incrementNumberOfLinks(self):
        self.number_of_links += 1
