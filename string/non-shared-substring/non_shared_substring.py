# python3

class Node:
    """Node(self,node_id,parent,index,length) -> create a suffix tree node.

    Attributes:
        node_id      Node ID (0,1,2.... ; 0 for root)
                     Also used to access SuffixTree.nodes_list
        parent       Parent node's ID
        index        Used in SuffixTree.text[index...]
        length       Used in SuffixTree.text[index:index+length]
        children     Dictionary where each entry corresponds to one child node
                     Denoting child node by c,
                         key = SuffixTree.text[c.index:c.index+1]
                         value = c.node_id
    """
    def __init__(self,node_id,parent,index,length):
        self.index = index
        self.length = length
        self.node_id = node_id
        self.children = {}
        self.parent = parent
        
    def add_child(self,char,node_id):
        """Adds a child to dictionary"""
        self.children[char] = node_id

class SuffixTree:
    """SuffixTree(text) -> builds suffix tree of text.

    Atributes:
        text          Input string
        nodes         Number of nodes in suffix tree (excluding root)
        root          Root node of suffix tree
        nodes_list    List containing Node object instances
    """
    def __init__(self,text):
        self.text = text
        self.nodes = 0
        self.root = Node(0,None,None,None)
        self.nodes_list = [self.root]
        
    def build(self):
        """Builds a suffix tree based on input string."""
        text = self.text
        index = 0
        for i in range(len(text)):
            t = 0
            current_node = self.root
            while True:
                first_char = text[t:t+1]
                # First checks if current node has any outgoing edge with its first character the same as first_char.
                # This part uses a dictionary for faster search in case current node has huge number of child nodes.
                if first_char in current_node.children:
                    n = self.nodes_list[current_node.children[first_char]]
                    # The maximum overlap of two strings is course 1 if the outgoing edge has string length equal 1.
                    # This if-else speeds up things a little especially if n.length is consistently 1, since we avoid
                    #    - the extra overhead involved in setting up zip() and the for loop
                    #    - the redundant construction of text1 and text2
                    #    - the redundant text1==text2 (we already know they match from the dict search)
                    #    - the redundant min_index calculation
                    if n.length == 1:
                        overlap = 1
                    else:
                        min_index = min(n.length,len(text)-t)
                        text1 = text[t:t+min_index]
                        text2 = self.text[n.index:n.index+min_index]
                        for c_i, (c1, c2) in enumerate(zip(text1,text2)):
                            if c1 != c2:
                                c_i -= 1
                                break
                        overlap = c_i+1
                # If we cannot travel down any existing edges, we create a new node and a new edge.
                else:
                    self.nodes += 1
                    new_node = Node(self.nodes,current_node.node_id,t+index,len(self.text)-t-index)
                    self.nodes_list.append(new_node)
                    current_node.add_child(first_char,self.nodes)
                    break
                # Case is simple if the entire edge matches part of the incoming string, simply go to next node.
                if n.length == overlap:
                    current_node = n
                    t += overlap
                    continue
                # Otherwise the current edge has to be broken down and new nodes have to be added.
                else:
                    self.nodes += 2
                    new_node1 = Node(self.nodes-1,current_node.node_id,n.index,overlap)
                    new_node2 = Node(self.nodes,self.nodes-1,t+index+overlap,len(self.text)-t-index-overlap)
                    new_node1.add_child(self.text[t+index+overlap:t+index+overlap+1],self.nodes)
                    n.index += overlap
                    n.length -= overlap
                    n.parent = self.nodes-1
                    new_node1.add_child(self.text[n.index:n.index+1],n.node_id)
                    current_node.add_child(self.text[new_node1.index:new_node1.index+1],self.nodes-1)
                    self.nodes_list.append(new_node1)
                    self.nodes_list.append(new_node2)
                    break
            text = text[1:]
            index += 1                # Keep tracks of where we are in the original self.text

    def shortest(self,text):
        """Returns shortest non-shared substring"""
        # The list marked stores the list of nodes that needs to be considered when constructing shortest substring.
        marked = [0]*(self.nodes+1)
        # To find the shortest non-shared substring, we pretend to construct a suffix tree from string2 based on the
        # existing suffix tree already constructed from string1. This explains the similarity of code in self.shortest
        # and self.build. We similarly travel the existing suffix tree and break edges up if necessary, but the main
        # difference is that in self.shortest, we do not need to add edges from string2.
        #
        # The strategy here is that if a node is marked, we could get its first char, travel upward to its parent and 
        # concatenate the two strings (parent's string + first char), and continue until we reach the root.
        # The reason for getting first char only is obvious - including the second char (or more) would only
        # unnecessarily make it longer.
        #
        # To maintain which nodes should be marked, we "trickle down" the marked property from parent to all its child
        # nodes if the parent's string is wholly or partially traversed when we "add" in string2 to existing suffix
        # tree. For the latter we need to also break up edge and add new node.
        for child in self.root.children:
            marked[self.root.children[child]] = 1
        for i in range(len(text)):
            t = 0
            current_node = self.root
            while True:
                first_char = text[t:t+1]
                if first_char not in current_node.children:
                    break
                else:
                    n = self.nodes_list[current_node.children[first_char]]
                    if n.length == 1:
                        overlap = 1
                    else:
                        min_index = min(n.length,len(text)-t)
                        text1 = text[t:t+min_index]
                        text2 = self.text[n.index:n.index+min_index]
                        for c_i, (c1, c2) in enumerate(zip(text1,text2)):
                            if c1 != c2:
                                c_i -= 1
                                break
                        overlap = c_i+1
                if n.length == overlap:
                    current_node = n
                    if marked[n.node_id] == 1:
                        marked[n.node_id] = 0
                        # trickle down to children
                        for child in n.children:
                            marked[n.children[child]] = 1
                    t += overlap
                    continue
                else:
                    if marked[n.node_id] == 1:
                        self.nodes += 1
                        new_node1 = Node(self.nodes,current_node.node_id,n.index,overlap)
                        marked.append(0)
                        n.index += overlap
                        n.length -= overlap
                        n.parent = self.nodes
                        new_node1.add_child(self.text[n.index:n.index+1],n.node_id)
                        new_node1.parent = current_node.node_id
                        current_node.add_child(self.text[new_node1.index:new_node1.index+1],self.nodes)
                        self.nodes_list.append(new_node1)
                        #trickle down to children
                        for child in new_node1.children:
                            marked[new_node1.children[child]] = 1
                    break
            text = text[1:]
        # Once string2 is "added" to the suffix tree, we then find the shortest possible non-shared substring
        shortest = ""
        for i, mark in enumerate(marked):
            # We only need to process those nodes marked
            if mark == 0:
                continue
            # And for these marked nodes, we only need to get the minimum from its corresponding string, i.e. its first char
            node = self.nodes_list[i]
            first_char = self.text[node.index:node.index+1]
            # Since "#" is not originally part of string1, we cannot accept "#" as first char
            if first_char == "#":
                continue
            parent_node = self.nodes_list[node.parent]
            string = first_char
            # Finally we trace upwards towards root from the current marked node and concatenate all the involved strings
            while parent_node.node_id != 0:
                parent_text = self.text[parent_node.index:parent_node.index+parent_node.length]
                string = "".join([parent_text,string])
                # Break early if existing string is already longer than shortest found previously
                if len(string) >= len(shortest):
                    if len(shortest) != 0:
                        break
                parent_node = self.nodes_list[parent_node.parent]
            if len(shortest) == 0 or len(string) < len(shortest):
                shortest = string
                # Break early if the shortest found is already at length 1 (shortest possible)
                if len(shortest) == 1:
                    return shortest
        return shortest


if __name__ == '__main__':
    # Typical routine:
    #     SuffixTree(string1) to initialize
    #     Suffixtree.build() to build suffix tree
    #     SuffixTree.shortest(string2) to find shortest substring of string1 that does not appear in string2
    tree = SuffixTree(input()+"#")
    tree.build()
    shortest = tree.shortest(input()+"$")
    print(shortest)
