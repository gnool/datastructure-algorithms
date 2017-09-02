# Overview
Here are two different approaches to construct a suffix tree of an input string of length S.
The first approach (suffix_tree_brute.py) uses a brute force method and runs in <code>O(S<sup>2</sup>)</code> time.
The second approach (suffix_tree_from_array.py) constructs a suffix tree from suffix array (and longest common prefix array). It runs in <code>O(S log S)</code> time.
For even faster construction one can use Ukkonen's algorithm which runs in <code>O(S)</code>.

# Note of usage
Please append a character (one which does not already appear in your input string) to your input string to mark the end of the string as otherwise the algorithm would not work correctly.
If your input string is "banana", append a "$" to it would work.
