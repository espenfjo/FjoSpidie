class Node:

    def __init__(self, hostname):
        self.label = hostname
        self.id = None
        self.status = None
        self.parents = []

    def set_status(self, status):
        self.status = status

    def set_parent(self, node, status):
        import ParentNode
        parent_node = Node(node.label)
        parent_node.__class__ = ParentNode.ParentNode
        parent_node.id = node.id
        parent_node.status = status
        already_exists = False

        for existing_pnode in self.parents:
            #Does new parent match old parent? Aka have we had this connection
            # earlier
            if existing_pnode.label == node.label:
                # We have an old connection, but do we have an old connection
                # with the same HTTP status code (OK, REDIRECT etc)?
                if status == self.status:
                    existing_pnode.incrementNumberOfLinks()
                    already_exists = True
                    break
        if not already_exists:
            self.parents.append(node)

    def dotnode(self):
        return "node" + str(self.id)
