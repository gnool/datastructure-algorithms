# Overview
String manipulation can normally be done very conveniently in Python using slicing. For example, for an input string s = "Hello World", if you wish to shift all elements with indices between 3 to 5 (both inclusive) to a new index 7, this can be easily done with s[:3]+s[6:10]+s[3:6]+s[10:11]. The substring shifted is "lo " and the resulting string would be "HelWorllo d".   

However, if you need to relocate a very long sub-string within the original string, and repeat this many times with random long sub-strings, this can be costly and does not scale well with string length. The running time is O(n), where n is the string length.
One way to speed up such string manipulations is to store the string in a binary search tree.

# Implementation details
In this algorithm we store all the characters in the input string in a splay tree. Each node carries one character. Each manipulation operation on string s is defined by 3 integers (i,j,k), where substring s[i:j+1] is to be moved to new index k. It is important to note that k <= n-(j-i+1). For example, it is impossible to perform operation (3,5,20) on "Hello World", since there is simply not enough elements to go before the substring to push element index 3 to index 20 (to do so we would need 17 elements after the substring; we only have 5 in this case). One should also take note that k can be smaller than i, i.e. the substring is being shifted backward.  

Here we focus only on shifting substrings around in the original string. A more general algorithm should include add and delete of substrings. To shift substrings around, we can split the splay tree into 4 subtrees (A,B,C,D in ascending key values), and merge them back in the order A,C,B,D. For "Hello World" with operation (3,5,7), this would correspond to A="Hel", B="lo ", C="Worl" and D="d". Splitting and merging subtrees in a binary search tree involves only O(log n) time. Finding the nodes at which we split the tree costs also O(log n) - this is an inherent property of all binary search trees. 

When the subtrees (i.e. substrings) are being relocated, the key values in the subtrees being moved should be updated. The *correction* for each node within the same subtree should be same, since they are shifted by the same amount. In our example above, the correction for subtree B would be +4, since it is being shifted 4 indices forward. Similary the correction for subtree C would be -3, since it is being shifted 3 indices backward.

The main idea of this algorithm is not to update the key values of each individual node in the subtrees being moved - since this would bring us back to O(n) running time. Instead, we store the correction value at the root nodes of the two subtrees being moved. We then avoid updating all its child nodes for as long as we can. The important observation here is that it does no harm withholding this update from taking place - the child nodes need to be updated only when we need them (for example when we traverse through them). Therefore, when we perform a traversal in the tree, we can simply check if the current node has a correction that needs to be applied. If yes, we apply it to the current node, and pass it down to both its child nodes. This adds an extra overhead cost to check if a node has a pending correction that needs to be applied, but it does allow us to avoid the O(n) running time.

Imagine the scenario where a subtree just moved that does not have all its nodes corrected (only the root node was corrected). If the subsequent operation involves moving 50% of this subtree to a new location, the uncorrected child nodes would now have another layer of correction. The question is: since the old correction is still retained at the parent node, would this old correction be lost? Fortunately, in order to split at any node of this uncorrected subtree, we would first need to traverse to that particular node. This process of traversing would guarantee that any pending correction would "trickle down" from the parent node to as far as the current node at which splitting shall occur. Therefore it is guaranteed that any correction would never be lost.

Finally, to reconstruct the manipulated string, simply perform an in-order traversal of the tree.

# When to use this algorithm
This algorithm is suitable when long strings need to be manipulated for many times. A speed test against a brute force approach (using Python built-in string slicing and list.append() approach) is done using the following settings:
- string length n = 300,000 
- number of (i,j,k) operations = 100,000, where 0 <= i <= j <= n-1

The current algorithm and the brute force approach took 25s and 200s respectively. Such difference is not surprising considering the different running time: O(log n) vs. O(n) for each operation (i,j,k)  
*Note: For the current algorithm, O(log n) is only possible after the O(n) construction of splay tree for the first time*

# About the rope data structure
Another well-known way of manipulating long strings efficiently is to use the [rope data structure](https://en.wikipedia.org/wiki/Rope_(data_structure)). I am not sure how much faster the rope data structure would perform in our problem here.
