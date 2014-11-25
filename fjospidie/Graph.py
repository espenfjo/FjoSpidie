import logging
import hashlib
import pydot
from urlparse import urlparse

from Node import Node
from ParentNode import ParentNode

class Graph:

    def __init__(self, entries, nodes, report):
        self.graph = pydot.Dot(graph_type='digraph', rankdir='LR', ratio='fill', bb="'0,0,1382,108'")
        self.entries = entries
        self.nodes = nodes
        self.spidie = report

    def create_graph(self):
        self.calculate_nodes()
        self.fill_nodes()
        self.connect_nodes()
        data = self.graph.create_png()
        md5 = self.__get_md5(data)
        fs_id = None

        if not self.spidie.database.fs.exists({"md5":md5}):
            fs_id = self.spidie.database.fs.put(data, manipulate=False)
        else:
            grid_file = self.spidie.database.fs.get_version(md5=md5)
            fs_id = grid_file._id
        self.spidie.report.graph_id = fs_id

    def __get_md5(self, data):
        md5 = hashlib.md5()
        md5.update(data)
        return md5.hexdigest()


    def calculate_nodes(self):
        """ This function loops through all HTTP connections and maps all
        Nodes and ParentNodes.
        If the response header has a 301/302 (rewrite/redirect) we add the
        Location as a Node, and sets the Node from the Host header as its parent.

        All entries have at least one Host header. Add it to the Nodes list if it
        is not there already (For example from a previous Location header).

        If we have a referer header, find its Node and set it as parent for this Node
        unless we already have this Node from a previous Location
        header. Should always have its parent in the Node list."""
        for entry in self.entries:
            status = entry.response.status
            headers = entry.request.headers + entry.response.headers
            node = None
            for header in headers:
                if header.name == "Location":
                    if status == 301 or status == 302:
                        location_url = urlparse(header.value)
                        if not location_url.hostname:
                            logging.warning("Could not parse " + header.value + " into a valid domain. Skipping.")
                            break
                        location_node = Node(location_url.hostname)
                        location_node.set_status(status)
                        location_node.set_parent(node, status)
                        self.add_node_if_not_exists(location_node, entry)
                    else:
                        logging.warning("Unknown STATUS id " + str(status) + " when having Location header")

                elif header.name == "Host":
                    node = Node(header.value)
                    node.status = status
                    n = self.add_node_if_not_exists(node, entry)
                    if n:
                        node = n
                elif header.name == "Referer":
                    refURL = urlparse(header.value)
                    for pnode in self.nodes:
                        if refURL.hostname == pnode.label:
                            if len(node.parents) == 0:
                                node.set_parent(pnode, status)

    def add_node_if_not_exists(self, node, entry):
        """Adds a Node to the Node list if it is not already in the list."""
        alreadyExisting = False
        for n in self.nodes:
            # We have seen this connection earlier
            if n.label == node.label:
                alreadyExisting = True
                node = n
                return node

        if not alreadyExisting:
            node.har_entry = entry
            node.id = len(self.nodes) + 1
            self.nodes.append(node)

        return None

    def fill_nodes(self):
        """Loops through a list of Node objects and adds
          them to the GraphViz object as Dot Nodes."""
        for node in self.nodes:
            self.graph.add_node(pydot.Node(node.label))

    def connect_nodes(self):
        colours = {
            200: "green",
            204: "green",
            404: "red",
            403: "red",
            301: "orange",
            302: "yellow",
            304: "yellow"
        }
        for node in self.nodes:
            if len(node.parents) > 0:
                for parent in node.parents:
                    parent.__class__ = ParentNode
                    try:
                        colour = colours[node.status]
                    except:
                        pass
                    edge_weight = 1  # + (0.1 * parent.number_of_links)
                    edge = pydot.Edge(parent.label, node.label, color=colour)
                    self.graph.add_edge(edge)
            else:
                edge = pydot.Edge(self.nodes[0].label, node.label)
                self.graph.add_edge(edge)
