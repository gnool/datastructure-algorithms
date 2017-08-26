# python3

import random as rand
import timeit

# Node of a splay tree
class Node:
    """Node of a splay tree

    Attributes:
        key            tuple of (key,value), where value is a char
        left           left child node
        right          right child node
        parent         parent node
        correction     correction factor
    """
    def __init__(self, key, left, right, parent, correction):
        (self.key, self.left, self.right, self.parent, self.correction) = (key, left, right, parent, correction)

class SplayTree:
    """SplayTree data structure for fast string manipulation

    Atributes:
        s              input string to be manipulated
        root           root node of splay tree
    """
    def __init__(self, string):
        self.s = string
        self.root = None
        self._init_tree(self.s,None,1,0,len(self.s)-1)

    def _init_tree(self,s,parent,left,start,end):
        """Builds a balanced binary search tree"""
        half = (end+start)//2
        node = Node((half,s[half]),None,None,None,None)
        self.root = node
        if start <= half-1:
            self._build_tree(s,node,1,start,half-1)
        if end >= half+1:
            self._build_tree(s,node,0,half+1,end)

    def _build_tree(self,s,parent,left,start,end):
        """Recursive method used by self.init_tree()"""
        half = (end+start)//2
        node = Node((half,s[half]),None,None,None,None)
        node.parent = parent
        if left:
            node.parent.left = node
        else:
            node.parent.right = node
        if start <= half-1:
            self._build_tree(s,node,1,start,half-1)
        if end >= half+1:
            self._build_tree(s,node,0,half+1,end)
      
    def _inorder_traverse(self,node):
        """Perform in-order traversal and constructs the final output string."""
        if node.correction != None:
            self._correct(node)
        if node.left != None:
            self._inorder_traverse(node.left)
        self.s.append(node.key[1])
        if node.right != None:
            self._inorder_traverse(node.right)

    def _split(self, root, key):
        """Split the tree -> split-key will always follow right subtree"""
        # First find the target key
        target, root = self._find(root, key)
        if target == None:
            return (root, None)
        # Then splay it to root
        right = self._splay(target)
        left = right.left
        right.left = None
        # Detach its left node as root of a new subtree
        if left != None:
            left.parent = None
        # Update parent of child node
        if right.right != None:
            right.right.parent = right
        return (left, right)

    def _merge(self, left, right):
        """Merge two tree -> root node will be the smallest node of right subtree"""
        if left == None:
            return right
        if right == None:
            return left
        # First find the smallest node in right subtree.
        while right.left != None:
            right = right.left
        # Then splay it to root, and attach left subtree's root to it.
        right = self._splay(right)
        right.left = left
        left.parent = right
        return right

    def _find(self, root, key):
        """Return target node (or its successor) and new root of tree."""
        node = root
        last = root
        target = None
        while node != None:
            if node.correction != None:
                self._correct(node)
            if node.key[0] >= key and (target == None or node.key[0] < target.key[0]):
                target = node
            last = node
            if node.key[0] == key:
                break    
            if node.key[0] < key:
                node = node.right
            else: 
                node = node.left
        root = self._splay(last)
        return target, root

    def _splay(self, node):
        """Splay node -> node will be new root"""
        if node == None:
            return None
        while node.parent != None:
            if node.parent.parent == None:
                self._smallrotate(node)
                break
            self._bigrotate(node)
        return node

    def _smallrotate(self, node):
        """Perform small rotation on input node."""
        parent = node.parent
        if parent == None:
            return
        grandparent = parent.parent
        if parent.left == node:
            m = node.right
            if m != None:
                m.parent = parent
            node.right = parent
            parent.left = m
            parent.parent = node
        else:
            m = node.left
            if m != None:
                m.parent = parent
            node.left = parent
            parent.right = m
            parent.parent = node
        node.parent = grandparent
        if grandparent != None:
            if grandparent.left == parent:
                grandparent.left = node
            else: 
                grandparent.right = node

    def _bigrotate(self, node):
        """Perform big rotation on node -> either zig-zig or zig-zag"""
        if node.parent.left == node and node.parent.parent.left == node.parent:
            # Zig-zig
            self._smallrotate(node.parent)
            self._smallrotate(node)
        elif node.parent.right == node and node.parent.parent.right == node.parent:
            # Zig-zig
            self._smallrotate(node.parent)
            self._smallrotate(node)    
        else: 
            # Zig-zag
            self._smallrotate(node)
            self._smallrotate(node)

    def _correct(self, node):
        """Pass corrections to both childs."""
        if node.left != None:
            if node.left.correction != None:
                node.left.correction += node.correction
            else:
                node.left.correction = node.correction
        if node.right != None:
            if node.right.correction != None:
                node.right.correction += node.correction
            else:
                node.right.correction = node.correction
        # At the end the node is fully corrected while the correction is passed down to its child nodes.
        node.key = (node.key[0]+node.correction,node.key[1])
        node.correction = None
  
    def process(self, i, j, k):
        """Perform string manipulation -> shift s[i:j+1] to new location starting at index k"""
        if i==k:
            return
        # Find the locations at which we split our tree into 4 parts
        shift = abs(k-i)
        length = j-i+1
        if k > i:
            loc1 = i
            loc2 = j+1
            loc3 = j+shift+1
        else:
            loc1 = k
            loc2 = i
            loc3 = j+1
        # Split tree into 4 parts
        root3, root4 = self._split(self.root,loc3)
        root2, root3 = self._split(root3,loc2)
        root1, root2 = self._split(root2,loc1)
        # Revise the roots before merging the split trees     
        if k > i:
            root2.correction = shift
            root3.correction = -1*length
        else:
            root2.correction = length
            root3.correction = -1*shift
        self._correct(root2)
        self._correct(root3)
        self.root = self._merge(self._merge(self._merge(root1,root3),root2),root4)

    def result(self):
        """Return the manipulated string."""
        self.s = []
        self._inorder_traverse(self.root)
        self.s = "".join(self.s)
        return self.s


class SpeedTest:
    """Speed comparison between tree-based and naive approaches.

    Attributes:
        naive       time taken for naive approach
        fast        time taken for tree-based approach
        length      string length to be tested
        repeat      number of times to repeat
    """
    def __init__(self,length,repeat):
        self.naive = 0
        self.fast = 0
        self.length = length
        self.repeat = repeat

    def _naive(self,s,i,j,k):
        """Direct string slicing to manipulate string"""
        if k == i:
            return s
        elif k > i:
            ans = s[0:i]
            ans.extend(s[j+1:j+1+k-i])
            ans.extend(s[i:j+1])
            ans.extend(s[j+1+k-i:])
            return ans
        else:
            ans = s[0:k]
            ans.extend(s[i:j+1])
            ans.extend(s[k:i])
            ans.extend(s[j+1:])
            return ans

    def start(self):
        """Start speed test."""
        # First prepare the required strings and operations
        pool = 'abcdefghijklmnopqrstuvwxyz'
        s = []
        for _ in range(self.length):
            s.append(pool[rand.randint(0,25)])
        oplist = []
        for _ in range(self.repeat):
            i = rand.randint(0,self.length-1)
            j = rand.randint(i,self.length-1)
            k = rand.randint(0,self.length-(j-i+1))
            oplist.append((i,j,k))

        # Using tree-based approach
        time = timeit.default_timer()
        tree = SplayTree(s)
        for i,j,k in oplist:
            tree.process(i,j,k)
        tree_result = tree.result()
        self.fast = timeit.default_timer()-time

        # Using naive approach
        s1 = s    # preserve the original string s
        time = timeit.default_timer()
        a = timeit.default_timer()
        for i,j,k in oplist:
            s1 = self._naive(s1,i,j,k)
        naive_result = "".join(s1)
        self.naive = timeit.default_timer()-time
        return (self.fast,self.naive)
        

if __name__ == '__main__':
    #speed = SpeedTest(300000,100000)
    #(fast, naive) = speed.start()
    #print(fast,naive)
    rope = SplayTree(input())
    q = int(input())
    for _ in range(q):
        i, j, k = map(int, input().split())
        rope.process(i, j, k)
    print(rope.result())
