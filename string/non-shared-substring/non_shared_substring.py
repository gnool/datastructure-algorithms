# python3

class Node:
    """Node(self,node_id,parent,index,length) -> create a suffix tree node.

    Attributes:
        node_id         Node ID (0,1,2.... ; 0 for root)
                        Also used to access SuffixTree.nodes_list
        parent          Parent node's ID
        index           Used in SuffixTree.text[index...]
        length          Used in SuffixTree.text[index:index+length]
        total_length    Total string length to root; used for self.shortest() calculation
        children        Dictionary where each entry corresponds to one child node
                        Denoting child node by c,
                            key = SuffixTree.text[c.index:c.index+1]
                            value = c.node_id
    """
    def __init__(self,node_id,parent,index,length,total_length):
        self.index = index
        self.length = length
        self.node_id = node_id
        self.children = {}
        self.parent = parent
        self.total_length = total_length
        
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
        self.root = Node(0,None,None,None,0)
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
                children = current_node.children
                if first_char in children:
                    n = self.nodes_list[children[first_char]]
                    # The maximum overlap of two strings is course 1 if the outgoing edge has string length equal 1.
                    # This if-else speeds up things a little especially if n.length is consistently 1, since we avoid
                    #    - the extra overhead involved in setting up zip() and the for loop
                    #    - the redundant construction of text1 and text2
                    #    - the redundant text1==text2 (we already know they match from the dict search)
                    #    - the redundant min_index calculation
                    if n.length == 1:
                        current_node = n
                        t += 1
                        continue
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
                    string_length = len(self.text)-t-index
                    new_node = Node(self.nodes,current_node.node_id,t+index,string_length,current_node.total_length+string_length)
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
                    new_node1 = Node(self.nodes-1,current_node.node_id,n.index,overlap,current_node.total_length+overlap)
                    new_node2 = Node(self.nodes,self.nodes-1,t+index+overlap,len(self.text)-t-index-overlap,new_node1.total_length+len(self.text)-t-index-overlap)
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
        # The list 'marked' stores the list of nodes that needs to be considered when constructing shortest substring.
        marked = [0]*(self.nodes+1)
        for child in self.root.children:
            marked[self.root.children[child]] = 1
        for i in range(len(text)):
            t = 0
            current_node = self.root
            while True:
                first_char = text[t:t+1]
                children = current_node.children
                if first_char not in children:
                    break
                else:
                    n = self.nodes_list[children[first_char]]
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
                        new_node1 = Node(self.nodes,current_node.node_id,n.index,overlap,current_node.total_length+overlap)
                        marked.append(0)
                        n.index += overlap
                        n.length -= overlap
                        n.parent = self.nodes
                        new_node1.add_child(self.text[n.index:n.index+1],n.node_id)
                        new_node1.parent = current_node.node_id
                        current_node.add_child(self.text[new_node1.index:new_node1.index+1],self.nodes)
                        self.nodes_list.append(new_node1)
                        #trickle down to children
                        marked[n.node_id] = 1
                    break
            text = text[1:]
        # Once string2 is "added" to the suffix tree, we then find the shortest possible non-shared substring.
        # We start off by finding the node that promises the shortest non-shared substring.
        shortest = (None,float("inf"))
        for i, mark in enumerate(marked):
            # We only need to process those nodes marked.
            if mark == 0:
                continue
            node = self.nodes_list[i]
            parent = self.nodes_list[node.parent]
            first_char = self.text[node.index:node.index+1]
            # We cannot use this node if it only contains '#' which is not part of the original string.
            if first_char == "#":
                continue
            if parent.total_length < shortest[1]:
                shortest = (node,parent.total_length)
                # Break early if this is the shortest possible.
                # These corresponds to those nodes attached directly to root.
                if parent.total_length == 0:
                    return first_char
        # Now that we found the node that promises the shortest non-shared substring,
        # we start to trace upwards towards root and concatenate all the involved substrings.
        node = shortest[0]
        string = self.text[node.index:node.index+1]
        node = self.nodes_list[node.parent]
        while node.node_id != 0:
            substring = self.text[node.index:node.index+node.length]
            string = "".join([substring,string])
            node = self.nodes_list[node.parent]
        return string


if __name__ == '__main__':
    # Typical routine:
    #     SuffixTree(string1) to initialize
    #     Suffixtree.build() to build suffix tree
    #     SuffixTree.shortest(string2) to find shortest substring of string1 that does not appear in string2
    tree = SuffixTree(input()+"#")
    tree.build()
    shortest = tree.shortest(input()+"$")
    print(shortest)
