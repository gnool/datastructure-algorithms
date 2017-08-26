# python3

class Node:
    """Node(self,node_id,index,length) -> create a suffix tree node.

    Attributes:
        node_id      Node ID (0,1,2.... ; 0 for root)
                     Also used to access SuffixTree.nodes_list
        index        Used in SuffixTree.text[index...]
        length       Used in SuffixTree.text[index:index+length]
        children     Dictionary where each entry corresponds to one child node
                     Denoting child node by c,
                         key = SuffixTree.text[c.index:c.index+1]
                         value = c.node_id
    """
    
    def __init__(self,node_id,index,length):
        self.node_id = node_id
        self.index = index
        self.length = length
        self.children = {}
        
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
        self.root = Node(0,None,None)
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
                if first_char in current_node.children:
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
                else:
                    self.nodes += 1
                    new_node = Node(self.nodes,t+index,len(self.text)-t-index)
                    self.nodes_list.append(new_node)
                    current_node.add_child(first_char,self.nodes)
                    break
                if n.length == overlap:
                    current_node = n
                    t += overlap
                    continue
                else:
                    self.nodes += 2
                    new_node1 = Node(self.nodes-1,n.index,overlap)
                    new_node2 = Node(self.nodes,t+index+overlap,len(self.text)-t-index-overlap)
                    new_node1.add_child(self.text[t+index+overlap:t+index+overlap+1],self.nodes)
                    n.index += overlap
                    n.length -= overlap
                    new_node1.add_child(self.text[n.index:n.index+1],n.node_id)
                    current_node.add_child(self.text[new_node1.index:new_node1.index+1],self.nodes-1)
                    self.nodes_list.append(new_node1)
                    self.nodes_list.append(new_node2)
                    break
            text = text[1:]
            index += 1

    def get_edges(self):
        """Returns a list of all edges in suffix tree."""
        result = []
        for node in self.nodes_list:
            for d in node.children:
                child = self.nodes_list[node.children[d]]
                result.append(self.text[child.index:child.index+child.length])
        return result


if __name__ == '__main__':
    # Typical routine:
    #     SuffixTree(string) to initialize
    #     Suffixtree.build() to build suffix tree
    #     SuffixTree.get_edges() to get list of all edges
    tree = SuffixTree(input())
    tree.build()
    print("\n".join(tree.get_edges()))
